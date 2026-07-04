"""Event publication adapters for ARK reality ingestion."""

from __future__ import annotations

from typing import Callable, Protocol

from .models import EventPublicationRecord, IngestionFailure, RealityEvent


class EventSink(Protocol):
    """Boundary protocol used by ARK to publish events."""

    def publish(self, event: RealityEvent) -> EventPublicationRecord:
        """Publish one event request."""


class NoopEventSink:
    """Deterministic event sink for tests that do not need a bus."""

    def publish(self, event: RealityEvent) -> EventPublicationRecord:
        return EventPublicationRecord(event=event, status="ok", sequence=None)


class EventBusEventSink:
    """Adapter from ARK events to the Event Bus service contract."""

    def __init__(
        self,
        event_bus: object,
        *,
        envelope_builder: Callable[..., object],
        source: str = "ark",
        created_at: int = 0,
    ) -> None:
        self._event_bus = event_bus
        self._envelope_builder = envelope_builder
        self._source = source
        self._created_at = created_at

    def publish(self, event: RealityEvent) -> EventPublicationRecord:
        try:
            envelope = self._envelope_builder(
                event_type=event.event_type,
                source=self._source,
                route=event.route,
                payload=event.payload,
                event_id=event.event_id,
                created_at=self._created_at,
                correlation_id=event.correlation_id,
                causation_id=event.causation_id,
                metadata=event.metadata,
            )
            result = self._event_bus.publish(envelope)
        except Exception as exc:  # pragma: no cover - defensive adapter boundary
            return EventPublicationRecord(
                event=event,
                status="error",
                sequence=None,
                failure=IngestionFailure.build(
                    "EVENT_PUBLICATION_EXCEPTION",
                    str(exc),
                    {"event_id": event.event_id, "event_type": event.event_type},
                ),
            )
        if getattr(result, "status", "") == "ok":
            published = getattr(result, "envelope", None)
            return EventPublicationRecord(
                event=event,
                status="ok",
                sequence=getattr(published, "sequence", None),
            )
        failure = getattr(result, "failure", None)
        return EventPublicationRecord(
            event=event,
            status="error",
            sequence=None,
            failure=IngestionFailure.build(
                getattr(failure, "error_code", "EVENT_PUBLICATION_FAILED"),
                getattr(failure, "reason", "event publication failed"),
                dict(getattr(failure, "context", {}) or {}),
                getattr(failure, "recoverable", True),
            ),
        )
