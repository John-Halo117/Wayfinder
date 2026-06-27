"""Reusable identity primitives for Wayfinder services.

Contract:
- Inputs: explicit dataclasses and primitive strings.
- Outputs: immutable records or structured failures.
- Runtime constraint: O(identity_count * alias_count) for construction, bounded by
  IdentityService(max_records, max_aliases_per_record).
- Memory assumption: O(identity_count * alias_count), bounded by constructor caps.
- Failure cases: invalid namespace, invalid RID, duplicate alias, missing identity,
  merge conflict, and exceeded resource bounds.
- Determinism: all operations are deterministic except request ID generation when
  no inbound request ID is supplied, matching legacy ARK behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from secrets import token_hex
from types import MappingProxyType
from typing import Mapping, Sequence

MAX_NAMESPACE_LENGTH = 64
MAX_KEY_LENGTH = 128
MAX_LABEL_LENGTH = 256
MAX_ALIAS_LENGTH = 256
MAX_REQUEST_ID_LENGTH = 128
DEFAULT_MAX_RECORDS = 10_000
DEFAULT_MAX_ALIASES_PER_RECORD = 32
REQUEST_ID_HEX_BYTES = 8


@dataclass(frozen=True)
class Failure:
    """Structured failure object used by non-throwing identity operations."""

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
class IdentityRecord:
    """Canonical, alias-aware identity record.

    Derived from ARK truth-spine Entity fields: entity_id, entity_type, aliases,
    canonical_label, and confidence.
    """

    rid: str
    namespace: str
    key: str
    identity_type: str
    aliases: tuple[str, ...]
    canonical_label: str
    confidence: float
    lifecycle: str = "active"


@dataclass(frozen=True)
class AliasResolution:
    """Result of resolving a RID or alias to its canonical RID."""

    status: str
    query: str
    canonical_rid: str | None
    record: IdentityRecord | None
    failure: Failure | None = None


@dataclass(frozen=True)
class MergeDecision:
    """Deterministic merge decision between two identity records."""

    status: str
    canonical_rid: str | None
    absorbed_rid: str | None
    merged_aliases: tuple[str, ...]
    confidence: float | None
    failure: Failure | None = None


@dataclass(frozen=True)
class RequestIdentity:
    """Request identifier result compatible with ARK's X-Request-ID behavior."""

    request_id: str
    generated: bool


@dataclass(frozen=True)
class HealthStatus:
    """Bounded health signal for the Identity Service."""

    status: str
    records: int
    aliases: int
    max_records: int
    max_aliases_per_record: int


def normalize_namespace(namespace: str) -> str:
    """Normalize and validate an identity namespace.

    Runtime: O(len(namespace)), capped at MAX_NAMESPACE_LENGTH.
    Memory: O(len(namespace)).
    Failure: raises ValueError for empty, oversized, or invalid namespaces.
    """

    normalized = namespace.strip().lower()
    if not normalized:
        raise ValueError("namespace is required")
    if len(normalized) > MAX_NAMESPACE_LENGTH:
        raise ValueError("namespace exceeds maximum length")
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_-")
    if any(ch not in allowed for ch in normalized):
        raise ValueError("namespace contains invalid characters")
    return normalized


def _normalize_key(key: str) -> str:
    normalized = key.strip()
    if not normalized:
        raise ValueError("identity key is required")
    if len(normalized) > MAX_KEY_LENGTH:
        raise ValueError("identity key exceeds maximum length")
    if any(ch.isspace() for ch in normalized):
        raise ValueError("identity key must not contain whitespace")
    return normalized


def _normalize_alias(alias: str) -> str:
    normalized = alias.strip().lower()
    if not normalized:
        raise ValueError("alias is required")
    if len(normalized) > MAX_ALIAS_LENGTH:
        raise ValueError("alias exceeds maximum length")
    return normalized


def _make_rid(namespace: str, key: str) -> str:
    return f"{namespace}:{key}"


def generate_request_id(inbound_request_id: str | None = None) -> RequestIdentity:
    """Return inbound request ID or generate a legacy-compatible hex ID.

    Runtime: O(len(inbound_request_id)) when supplied, capped at
    MAX_REQUEST_ID_LENGTH. Generated IDs use secrets.token_hex(8), matching
    ARK's request_id_middleware behavior.
    Memory: O(1).
    Failure: raises ValueError for empty or oversized inbound request IDs.
    """

    if inbound_request_id is not None:
        normalized = inbound_request_id.strip()
        if not normalized:
            raise ValueError("request_id is empty")
        if len(normalized) > MAX_REQUEST_ID_LENGTH:
            raise ValueError("request_id exceeds maximum length")
        return RequestIdentity(request_id=normalized, generated=False)
    return RequestIdentity(request_id=token_hex(REQUEST_ID_HEX_BYTES), generated=True)


class IdentityService:
    """Bounded in-memory identity resolver.

    The service owns reusable identity mechanics only. Persistence, policy,
    observation, evidence, and reality graph behavior remain outside this class.
    """

    def __init__(
        self,
        records: Sequence[IdentityRecord] = (),
        *,
        max_records: int = DEFAULT_MAX_RECORDS,
        max_aliases_per_record: int = DEFAULT_MAX_ALIASES_PER_RECORD,
    ) -> None:
        if max_records <= 0:
            raise ValueError("max_records must be positive")
        if max_aliases_per_record <= 0:
            raise ValueError("max_aliases_per_record must be positive")
        if len(records) > max_records:
            raise ValueError("record count exceeds configured maximum")
        self._max_records = max_records
        self._max_aliases_per_record = max_aliases_per_record
        by_rid: dict[str, IdentityRecord] = {}
        alias_index: dict[str, str] = {}
        for record in records:
            normalized = self._validate_record(record)
            if normalized.rid in by_rid:
                raise ValueError(f"duplicate rid: {normalized.rid}")
            by_rid[normalized.rid] = normalized
            for alias in normalized.aliases:
                existing = alias_index.get(alias)
                if existing is not None and existing != normalized.rid:
                    raise ValueError(f"duplicate alias: {alias}")
                alias_index[alias] = normalized.rid
        self._by_rid = MappingProxyType(by_rid)
        self._alias_index = MappingProxyType(alias_index)

    @classmethod
    def from_entities(
        cls,
        entities: Sequence[Mapping[str, object]],
        *,
        namespace: str = "entity",
        max_records: int = DEFAULT_MAX_RECORDS,
        max_aliases_per_record: int = DEFAULT_MAX_ALIASES_PER_RECORD,
    ) -> "IdentityService":
        """Build records from ARK truth-spine Entity-shaped mappings.

        Runtime: O(entity_count * alias_count), bounded by max_records and
        max_aliases_per_record. Memory follows the same bound.
        Failure: raises ValueError for missing fields or exceeded bounds.
        """

        if len(entities) > max_records:
            raise ValueError("entity count exceeds configured maximum")
        normalized_namespace = normalize_namespace(namespace)
        records: list[IdentityRecord] = []
        for entity in entities:
            entity_id = str(entity.get("entity_id", ""))
            entity_type = str(entity.get("entity_type", ""))
            canonical_label = str(entity.get("canonical_label", ""))
            aliases_value = entity.get("aliases", ())
            confidence_value = entity.get("confidence", 0.0)
            if not isinstance(aliases_value, Sequence) or isinstance(aliases_value, (str, bytes)):
                raise ValueError("aliases must be a sequence")
            if len(aliases_value) > max_aliases_per_record:
                raise ValueError("alias count exceeds configured maximum")
            aliases = tuple(str(alias) for alias in aliases_value)
            records.append(
                cls.build_record(
                    namespace=normalized_namespace,
                    key=entity_id,
                    identity_type=entity_type,
                    aliases=aliases,
                    canonical_label=canonical_label,
                    confidence=float(confidence_value),
                )
            )
        return cls(
            records,
            max_records=max_records,
            max_aliases_per_record=max_aliases_per_record,
        )

    @staticmethod
    def build_record(
        *,
        namespace: str,
        key: str,
        identity_type: str,
        aliases: Sequence[str] = (),
        canonical_label: str,
        confidence: float,
        lifecycle: str = "active",
    ) -> IdentityRecord:
        """Create a validated identity record.

        Runtime: O(alias_count), bounded by caller/service caps.
        Memory: O(alias_count).
        Failure: raises ValueError for invalid fields.
        """

        normalized_namespace = normalize_namespace(namespace)
        normalized_key = _normalize_key(key)
        normalized_aliases = tuple(dict.fromkeys(_normalize_alias(alias) for alias in aliases))
        label = canonical_label.strip()
        if not label:
            raise ValueError("canonical_label is required")
        if len(label) > MAX_LABEL_LENGTH:
            raise ValueError("canonical_label exceeds maximum length")
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        lifecycle_normalized = lifecycle.strip().lower()
        if lifecycle_normalized not in {"active", "merged", "deprecated", "unknown"}:
            raise ValueError("invalid lifecycle")
        type_normalized = identity_type.strip().lower()
        if not type_normalized:
            raise ValueError("identity_type is required")
        return IdentityRecord(
            rid=_make_rid(normalized_namespace, normalized_key),
            namespace=normalized_namespace,
            key=normalized_key,
            identity_type=type_normalized,
            aliases=normalized_aliases,
            canonical_label=label,
            confidence=confidence,
            lifecycle=lifecycle_normalized,
        )

    def resolve(self, query: str) -> AliasResolution:
        """Resolve a RID or alias to a canonical identity record.

        Runtime: O(len(query)), dictionary lookup thereafter.
        Memory: O(1).
        Failure: returns structured NOT_FOUND or INVALID_QUERY failure.
        """

        normalized = query.strip()
        if not normalized:
            failure = Failure.build("IDENTITY_INVALID_QUERY", "query is required")
            return AliasResolution("error", query, None, None, failure)
        record = self._by_rid.get(normalized)
        if record is not None:
            return AliasResolution("ok", query, record.rid, record)
        alias_rid = self._alias_index.get(normalized.lower())
        if alias_rid is not None:
            alias_record = self._by_rid[alias_rid]
            return AliasResolution("ok", query, alias_record.rid, alias_record)
        failure = Failure.build(
            "IDENTITY_NOT_FOUND",
            "identity query did not match a RID or alias",
            {"query": query},
        )
        return AliasResolution("error", query, None, None, failure)

    def merge(self, left_rid: str, right_rid: str) -> MergeDecision:
        """Return a deterministic merge decision without mutating records.

        Runtime: O(alias_count), bounded by max_aliases_per_record.
        Memory: O(alias_count).
        Failure: returns structured failure for missing or conflicting records.
        """

        left = self._by_rid.get(left_rid.strip())
        right = self._by_rid.get(right_rid.strip())
        if left is None or right is None:
            return MergeDecision(
                status="error",
                canonical_rid=None,
                absorbed_rid=None,
                merged_aliases=(),
                confidence=None,
                failure=Failure.build(
                    "IDENTITY_MERGE_NOT_FOUND",
                    "both identities must exist before merge",
                    {"left_rid": left_rid, "right_rid": right_rid},
                ),
            )
        if left.identity_type != right.identity_type:
            return MergeDecision(
                status="error",
                canonical_rid=None,
                absorbed_rid=None,
                merged_aliases=(),
                confidence=None,
                failure=Failure.build(
                    "IDENTITY_MERGE_TYPE_CONFLICT",
                    "identity types differ",
                    {"left_type": left.identity_type, "right_type": right.identity_type},
                    recoverable=False,
                ),
            )
        canonical, absorbed = (left, right)
        if right.confidence > left.confidence or (
            right.confidence == left.confidence and right.rid < left.rid
        ):
            canonical, absorbed = right, left
        merged_aliases = tuple(
            dict.fromkeys((*canonical.aliases, *absorbed.aliases, absorbed.rid, absorbed.canonical_label.lower()))
        )
        if len(merged_aliases) > self._max_aliases_per_record * 2 + 2:
            return MergeDecision(
                status="error",
                canonical_rid=None,
                absorbed_rid=None,
                merged_aliases=(),
                confidence=None,
                failure=Failure.build(
                    "IDENTITY_MERGE_ALIAS_LIMIT",
                    "merged alias set exceeds bounded limit",
                    {"limit": self._max_aliases_per_record * 2 + 2},
                ),
            )
        return MergeDecision(
            status="ok",
            canonical_rid=canonical.rid,
            absorbed_rid=absorbed.rid,
            merged_aliases=merged_aliases,
            confidence=max(left.confidence, right.confidence),
        )

    def health(self) -> HealthStatus:
        """Return bounded service health metadata.

        Runtime: O(1). Memory: O(1). Failure: none.
        """

        return HealthStatus(
            status="ok",
            records=len(self._by_rid),
            aliases=len(self._alias_index),
            max_records=self._max_records,
            max_aliases_per_record=self._max_aliases_per_record,
        )

    def _validate_record(self, record: IdentityRecord) -> IdentityRecord:
        if len(record.aliases) > self._max_aliases_per_record:
            raise ValueError("alias count exceeds configured maximum")
        expected_rid = _make_rid(normalize_namespace(record.namespace), _normalize_key(record.key))
        if record.rid != expected_rid:
            raise ValueError("rid does not match namespace and key")
        return self.build_record(
            namespace=record.namespace,
            key=record.key,
            identity_type=record.identity_type,
            aliases=record.aliases,
            canonical_label=record.canonical_label,
            confidence=record.confidence,
            lifecycle=record.lifecycle,
        )
