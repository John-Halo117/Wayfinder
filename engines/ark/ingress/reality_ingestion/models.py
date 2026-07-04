"""Contracts for ARK reality ingestion.

The records in this module are ARK-owned preservation records. They accept
canonical observation-shaped inputs but do not depend on any observation source
implementation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from types import MappingProxyType
from typing import Any, Literal, Mapping

DEFAULT_PRESERVED_AT = "1970-01-01T00:00:00Z"

IssueSeverity = Literal["info", "warning", "error"]
StorageWriteStatus = Literal["preserved", "already_preserved", "error"]


@dataclass(frozen=True)
class RealityIngestionLimits:
    """Bounded resource limits for one ingestion run."""

    max_observations: int = 100_000
    max_relationships: int = 250_000
    max_artifacts: int = 100_000
    max_payload_bytes: int = 2 * 1024 * 1024
    max_provenance_keys: int = 64
    max_metadata_keys: int = 128


@dataclass(frozen=True)
class IngestionFailure:
    """Structured failure object following the Wayfinder failure model."""

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
    ) -> "IngestionFailure":
        return cls(
            status="error",
            error_code=error_code,
            reason=reason,
            context=MappingProxyType(dict(context or {})),
            recoverable=recoverable,
        )


@dataclass(frozen=True)
class IngestionValidationIssue:
    """Validation issue emitted without silently repairing the input."""

    issue_id: str
    severity: IssueSeverity
    error_code: str
    reason: str
    context: Mapping[str, object]
    recoverable: bool


@dataclass(frozen=True)
class IdentityResolutionRecord:
    """Identity lookup result consumed from the Identity Service."""

    observation_id: str
    status: str
    canonical_rid: str | None
    queries: tuple[str, ...]
    failure_code: str | None = None


@dataclass(frozen=True)
class PromotionHistoryEntry:
    """Append-only preservation history entry."""

    stage: str
    at: str
    actor: str
    evidence_hash: str


@dataclass(frozen=True)
class LastVerifiedReality:
    """ARK cursor updated only when an observation is explicitly preserved."""

    sequence: int
    observation_id: str | None
    content_hash: str | None
    updated_at: str


@dataclass(frozen=True)
class PreservedObservationRecord:
    """Durable, append-only observation preservation record."""

    preservation_id: str
    sequence: int
    observation_id: str
    source: str
    artifact_type: str
    timestamp: str | None
    original_location: str
    canonical_rid: str | None
    content_hash: str
    raw_observation: Mapping[str, object]
    provenance: Mapping[str, object]
    validation_status: str
    parsing_status: str | None
    preserved_at: str
    promotion_history: tuple[PromotionHistoryEntry, ...]


@dataclass(frozen=True)
class PreservedRelationshipRecord:
    """Durable preservation of an explicit source-provided relationship."""

    preservation_id: str
    sequence: int
    relationship_id: str
    relationship_type: str
    source_id: str
    target_id: str
    content_hash: str
    raw_relationship: Mapping[str, object]
    provenance: Mapping[str, object]
    validation_status: str
    preserved_at: str


@dataclass(frozen=True)
class StorageWriteResult:
    """Storage abstraction result for append-only writes."""

    status: StorageWriteStatus
    record: PreservedObservationRecord | PreservedRelationshipRecord | None
    failure: IngestionFailure | None = None


@dataclass(frozen=True)
class RealityReplayResult:
    """Bounded replay of preserved reality records."""

    status: str
    observations: tuple[PreservedObservationRecord, ...]
    relationships: tuple[PreservedRelationshipRecord, ...]
    next_observation_sequence: int
    next_relationship_sequence: int
    failure: IngestionFailure | None = None


@dataclass(frozen=True)
class RealityEvent:
    """Transport-neutral ARK event request."""

    event_id: str
    event_type: str
    route: str
    payload: Mapping[str, object]
    correlation_id: str | None = None
    causation_id: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class EventPublicationRecord:
    """Result of publishing an event through the event boundary."""

    event: RealityEvent
    status: str
    sequence: int | None
    failure: IngestionFailure | None = None


@dataclass(frozen=True)
class RealityIngestionResult:
    """Complete result of one ARK ingestion run."""

    status: str
    batch_id: str
    source: str
    preserved_observations: tuple[PreservedObservationRecord, ...]
    preserved_relationships: tuple[PreservedRelationshipRecord, ...]
    identity_resolutions: tuple[IdentityResolutionRecord, ...]
    validation_report: tuple[IngestionValidationIssue, ...]
    event_publications: tuple[EventPublicationRecord, ...]
    last_verified_reality: LastVerifiedReality


def to_plain(value: Any) -> Any:
    """Convert supported immutable records into JSON-ready values."""

    if hasattr(value, "__dataclass_fields__"):
        return to_plain(asdict(value))
    if isinstance(value, tuple):
        return [to_plain(item) for item in value]
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): to_plain(item) for key, item in value.items()}
    return value
