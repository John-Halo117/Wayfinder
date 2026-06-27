"""Transport-neutral Event Bus primitives for Wayfinder services.

Contract:
- Inputs: explicit dataclasses, primitive strings, and payload/metadata mappings.
- Outputs: immutable records or structured failures.
- Runtime constraint: O(subscriber_count + payload_size) for publish, bounded by
  EventBusService(max_subscribers, max_payload_bytes). Replay is O(limit), bounded
  by max_replay_limit.
- Memory assumption: O(max_events + max_subscribers), bounded by constructor caps.
- Failure cases: invalid route, invalid envelope, oversized payload, duplicate
  event ID, subscriber limit, replay gap, and exceeded resource bounds.
- Determinism: event routing, sequence assignment, and replay ordering are
  deterministic. Generated event IDs are deterministic within the service
  sequence so tests and proofs are stable.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from json import dumps
from types import MappingProxyType
from typing import Mapping, Sequence

MAX_EVENT_ID_LENGTH = 128
MAX_EVENT_TYPE_LENGTH = 128
MAX_SOURCE_LENGTH = 128
MAX_ROUTE_LENGTH = 256
MAX_METADATA_KEYS = 64
MAX_METADATA_KEY_LENGTH = 128
MAX_METADATA_VALUE_LENGTH = 512
DEFAULT_MAX_EVENTS = 10_000
DEFAULT_MAX_SUBSCRIBERS = 1_000
DEFAULT_MAX_PAYLOAD_BYTES = 1_048_576
DEFAULT_MAX_REPLAY_LIMIT = 1_000


@dataclass(frozen=True)
class Failure:
    """Structured failure object used by non-throwing Event Bus operations."""

    status: str
    error_code: str
    reason: str
    context: Mapping[str, object]
    recoverable: bool

    @classmethod
    def build(
        cls,
        error_code: str,
        reason: str,
        context: Mapping[str, object] | None = None,
        recoverable: bool = True,
    ) -> "Failure":
        return cls(
            status="error",
            error_code=error_code,
            reason=reason,
            context=MappingProxyType(dict(context or {})),
            recoverable=recoverable,
        )


@dataclass(frozen=True)
class EventEnvelope:
    """Canonical transport-neutral event envelope.

    Derived from ARK event fields: event_id, event_type, source, sequence,
    created_at/timestamp, payload, routing subject, and metadata tags.
    """

    event_id: str
    event_type: str
    source: str
    route: str
    payload: Mapping[str, object]
    sequence: int = 0
    created_at: int = 0
    correlation_id: str | None = None
    causation_id: str | None = None
    metadata: Mapping[str, str] = MappingProxyType({})


@dataclass(frozen=True)
class Subscription:
    """A route-pattern subscription using ARK/NATS-style wildcards."""

    subscription_id: str
    route_pattern: str


@dataclass(frozen=True)
class SubscribeResult:
    """Result of registering a subscription."""

    status: str
    subscription: Subscription | None
    failure: Failure | None = None


@dataclass(frozen=True)
class PublishResult:
    """Result of publishing an event to matching subscriptions."""

    status: str
    envelope: EventEnvelope | None
    delivered_to: tuple[str, ...]
    failure: Failure | None = None


@dataclass(frozen=True)
class ReplayResult:
    """Bounded replay result ordered by event sequence."""

    status: str
    events: tuple[EventEnvelope, ...]
    next_cursor: int
    failure: Failure | None = None


@dataclass(frozen=True)
class HealthStatus:
    """Bounded health signal for the Event Bus Service."""

    status: str
    events: int
    subscribers: int
    next_sequence: int
    max_events: int
    max_subscribers: int
    max_payload_bytes: int
    max_replay_limit: int


def _normalize_token(value: str, *, field: str, max_length: int) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field} is required")
    if len(normalized) > max_length:
        raise ValueError(f"{field} exceeds maximum length")
    return normalized


def normalize_route(route: str) -> str:
    """Normalize and validate a dot-delimited route or route pattern.

    Runtime: O(route token count), bounded by MAX_ROUTE_LENGTH.
    Memory: O(route length).
    Failure: raises ValueError for empty, oversized, malformed, or invalid routes.
    """

    normalized = _normalize_token(route, field="route", max_length=MAX_ROUTE_LENGTH).lower()
    tokens = normalized.split(".")
    if any(token == "" for token in tokens):
        raise ValueError("route contains an empty token")
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_*.->")
    for token in tokens:
        if any(ch not in allowed for ch in token):
            raise ValueError("route contains invalid characters")
        if ">" in token and token != ">":
            raise ValueError("multi-token wildcard must be its own token")
        if "*" in token and token != "*":
            raise ValueError("single-token wildcard must be its own token")
    if ">" in tokens and tokens[-1] != ">":
        raise ValueError("multi-token wildcard must be the final token")
    return normalized


def route_matches(pattern: str, route: str) -> bool:
    """Return whether a route matches an ARK/NATS-style route pattern.

    Runtime: O(max(pattern tokens, route tokens)), bounded by MAX_ROUTE_LENGTH.
    Memory: O(token count).
    Failure: raises ValueError for invalid pattern or route.
    """

    pattern_tokens = normalize_route(pattern).split(".")
    route_tokens = normalize_route(route).split(".")
    max_steps = max(len(pattern_tokens), len(route_tokens)) + 1
    pattern_index = 0
    route_index = 0
    for _ in range(max_steps):
        if pattern_index == len(pattern_tokens) and route_index == len(route_tokens):
            return True
        if pattern_index == len(pattern_tokens):
            return False
        token = pattern_tokens[pattern_index]
        if token == ">":
            return route_index < len(route_tokens)
        if route_index == len(route_tokens):
            return False
        if token != "*" and token != route_tokens[route_index]:
            return False
        pattern_index += 1
        route_index += 1
    raise ValueError("route match exceeded bounded iteration limit")


def _validate_payload(payload: Mapping[str, object], max_payload_bytes: int) -> Mapping[str, object]:
    if not isinstance(payload, Mapping):
        raise ValueError("payload must be a mapping")
    raw = dumps(dict(payload), default=str, sort_keys=True)
    if len(raw.encode("utf-8")) > max_payload_bytes:
        raise ValueError("payload exceeds maximum size")
    return MappingProxyType(dict(payload))


def _validate_metadata(metadata: Mapping[str, str] | None) -> Mapping[str, str]:
    if metadata is None:
        return MappingProxyType({})
    if not isinstance(metadata, Mapping):
        raise ValueError("metadata must be a mapping")
    if len(metadata) > MAX_METADATA_KEYS:
        raise ValueError("metadata key count exceeds maximum")
    normalized: dict[str, str] = {}
    for key, value in metadata.items():
        key_text = str(key).strip()
        if not key_text:
            raise ValueError("metadata key is required")
        if len(key_text) > MAX_METADATA_KEY_LENGTH:
            raise ValueError("metadata key exceeds maximum length")
        value_text = str(value)
        if len(value_text) > MAX_METADATA_VALUE_LENGTH:
            raise ValueError("metadata value exceeds maximum length")
        normalized[key_text] = value_text
    return MappingProxyType(normalized)


class EventBusService:
    """Bounded in-memory event bus proof.

    The service owns reusable event mechanics only. Broker selection, durable
    storage, engine workflow interpretation, and domain semantics remain outside
    this class.
    """

    def __init__(
        self,
        *,
        max_events: int = DEFAULT_MAX_EVENTS,
        max_subscribers: int = DEFAULT_MAX_SUBSCRIBERS,
        max_payload_bytes: int = DEFAULT_MAX_PAYLOAD_BYTES,
        max_replay_limit: int = DEFAULT_MAX_REPLAY_LIMIT,
    ) -> None:
        if max_events <= 0:
            raise ValueError("max_events must be positive")
        if max_subscribers <= 0:
            raise ValueError("max_subscribers must be positive")
        if max_payload_bytes <= 0:
            raise ValueError("max_payload_bytes must be positive")
        if max_replay_limit <= 0:
            raise ValueError("max_replay_limit must be positive")
        self._max_events = max_events
        self._max_subscribers = max_subscribers
        self._max_payload_bytes = max_payload_bytes
        self._max_replay_limit = max_replay_limit
        self._events: tuple[EventEnvelope, ...] = ()
        self._subscriptions: tuple[Subscription, ...] = ()
        self._next_sequence = 1
        self._next_subscription = 1

    @staticmethod
    def build_envelope(
        *,
        event_type: str,
        source: str,
        route: str,
        payload: Mapping[str, object] | None = None,
        event_id: str | None = None,
        created_at: int = 0,
        correlation_id: str | None = None,
        causation_id: str | None = None,
        metadata: Mapping[str, str] | None = None,
    ) -> EventEnvelope:
        """Create a validated event envelope without assigning sequence.

        Runtime: O(payload size + metadata count), bounded by service publish caps.
        Memory: O(payload size + metadata count).
        Failure: raises ValueError for invalid fields.
        """

        normalized_type = _normalize_token(event_type, field="event_type", max_length=MAX_EVENT_TYPE_LENGTH)
        normalized_source = _normalize_token(source, field="source", max_length=MAX_SOURCE_LENGTH)
        normalized_route = normalize_route(route)
        normalized_id = event_id.strip() if event_id is not None else ""
        if normalized_id and len(normalized_id) > MAX_EVENT_ID_LENGTH:
            raise ValueError("event_id exceeds maximum length")
        if created_at < 0:
            raise ValueError("created_at must be non-negative")
        return EventEnvelope(
            event_id=normalized_id,
            event_type=normalized_type,
            source=normalized_source,
            route=normalized_route,
            payload=MappingProxyType(dict(payload or {})),
            created_at=created_at,
            correlation_id=correlation_id.strip() if correlation_id else None,
            causation_id=causation_id.strip() if causation_id else None,
            metadata=_validate_metadata(metadata),
        )

    def subscribe(self, route_pattern: str) -> SubscribeResult:
        """Register a bounded route-pattern subscription.

        Runtime: O(subscriber_count), bounded by max_subscribers.
        Memory: O(subscriber_count).
        Failure: returns structured failure for invalid route or exhausted capacity.
        """

        try:
            normalized_pattern = normalize_route(route_pattern)
        except ValueError as exc:
            return SubscribeResult(
                status="error",
                subscription=None,
                failure=Failure.build(
                    "EVENT_ROUTE_INVALID",
                    str(exc),
                    {"route_pattern": route_pattern},
                ),
            )
        if len(self._subscriptions) >= self._max_subscribers:
            return SubscribeResult(
                status="error",
                subscription=None,
                failure=Failure.build(
                    "EVENT_SUBSCRIBER_LIMIT",
                    "subscriber count exceeds configured maximum",
                    {"max_subscribers": self._max_subscribers},
                ),
            )
        subscription = Subscription(
            subscription_id=f"sub-{self._next_subscription}",
            route_pattern=normalized_pattern,
        )
        self._next_subscription += 1
        self._subscriptions = (*self._subscriptions, subscription)
        return SubscribeResult(status="ok", subscription=subscription)

    def publish(self, envelope: EventEnvelope) -> PublishResult:
        """Append an event and return matching subscription IDs.

        Runtime: O(subscriber_count + payload size), bounded by constructor caps.
        Memory: O(event_count + delivered subscriber count), bounded by caps.
        Failure: returns structured failure for invalid envelope, duplicate ID, or full log.
        """

        if len(self._events) >= self._max_events:
            return PublishResult(
                status="error",
                envelope=None,
                delivered_to=(),
                failure=Failure.build(
                    "EVENT_LOG_LIMIT",
                    "event count exceeds configured maximum",
                    {"max_events": self._max_events},
                ),
            )
        try:
            candidate = self._normalize_envelope_for_publish(envelope)
        except ValueError as exc:
            return PublishResult(
                status="error",
                envelope=None,
                delivered_to=(),
                failure=Failure.build("EVENT_INVALID", str(exc), recoverable=True),
            )
        for existing in self._events:
            if existing.event_id == candidate.event_id:
                return PublishResult(
                    status="error",
                    envelope=None,
                    delivered_to=(),
                    failure=Failure.build(
                        "EVENT_DUPLICATE_ID",
                        "event_id already exists in event log",
                        {"event_id": candidate.event_id},
                        recoverable=False,
                    ),
                )
        delivered: list[str] = []
        for subscription in self._subscriptions:
            if route_matches(subscription.route_pattern, candidate.route):
                delivered.append(subscription.subscription_id)
        self._events = (*self._events, candidate)
        self._next_sequence += 1
        return PublishResult(status="ok", envelope=candidate, delivered_to=tuple(delivered))

    def replay(self, *, after_sequence: int = 0, limit: int | None = None) -> ReplayResult:
        """Return events after a replay cursor in sequence order.

        Runtime: O(event_count + limit), bounded by max_events and max_replay_limit.
        Memory: O(limit), bounded by max_replay_limit.
        Failure: returns structured failure for invalid cursor or limit.
        """

        if after_sequence < 0:
            return ReplayResult(
                status="error",
                events=(),
                next_cursor=after_sequence,
                failure=Failure.build("EVENT_REPLAY_CURSOR_INVALID", "after_sequence must be non-negative"),
            )
        effective_limit = self._max_replay_limit if limit is None else limit
        if effective_limit <= 0 or effective_limit > self._max_replay_limit:
            return ReplayResult(
                status="error",
                events=(),
                next_cursor=after_sequence,
                failure=Failure.build(
                    "EVENT_REPLAY_LIMIT_INVALID",
                    "replay limit must be positive and within configured maximum",
                    {"max_replay_limit": self._max_replay_limit},
                ),
            )
        selected: list[EventEnvelope] = []
        steps = 0
        for event in self._events:
            steps += 1
            if steps > self._max_events:
                return ReplayResult(
                    status="error",
                    events=(),
                    next_cursor=after_sequence,
                    failure=Failure.build("EVENT_REPLAY_BOUND_EXCEEDED", "replay exceeded event bound"),
                )
            if event.sequence > after_sequence:
                selected.append(event)
                if len(selected) >= effective_limit:
                    break
        next_cursor = selected[-1].sequence if selected else after_sequence
        return ReplayResult(status="ok", events=tuple(selected), next_cursor=next_cursor)

    def health(self) -> HealthStatus:
        """Return bounded service health metadata.

        Runtime: O(1). Memory: O(1). Failure: none.
        """

        return HealthStatus(
            status="ok",
            events=len(self._events),
            subscribers=len(self._subscriptions),
            next_sequence=self._next_sequence,
            max_events=self._max_events,
            max_subscribers=self._max_subscribers,
            max_payload_bytes=self._max_payload_bytes,
            max_replay_limit=self._max_replay_limit,
        )

    def _normalize_envelope_for_publish(self, envelope: EventEnvelope) -> EventEnvelope:
        normalized_id = envelope.event_id.strip() if envelope.event_id else f"evt-{self._next_sequence}"
        if len(normalized_id) > MAX_EVENT_ID_LENGTH:
            raise ValueError("event_id exceeds maximum length")
        payload = _validate_payload(envelope.payload, self._max_payload_bytes)
        metadata = _validate_metadata(envelope.metadata)
        return replace(
            envelope,
            event_id=normalized_id,
            event_type=_normalize_token(envelope.event_type, field="event_type", max_length=MAX_EVENT_TYPE_LENGTH),
            source=_normalize_token(envelope.source, field="source", max_length=MAX_SOURCE_LENGTH),
            route=normalize_route(envelope.route),
            payload=payload,
            sequence=self._next_sequence,
            metadata=metadata,
        )
