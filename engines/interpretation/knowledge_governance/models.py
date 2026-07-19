"""Contracts for candidate review and promotion governance."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal, Mapping

from engines.interpretation.knowledge_compiler.models import CandidateArtifact

DEFAULT_REVIEWED_AT = "1970-01-01T00:00:00Z"
GOVERNANCE_VERSION = "1.0.0"
REVIEW_STATES: tuple[str, ...] = (
    "discovered",
    "under_review",
    "approved",
    "rejected",
    "deferred",
    "superseded",
    "promoted",
)
PROMOTION_TARGETS: tuple[str, ...] = (
    "glossary",
    "constitution",
    "adr_repository",
    "capsule_repository",
    "execution_backlog",
    "knowledge_repository",
)

ReviewState = Literal[
    "discovered",
    "under_review",
    "approved",
    "rejected",
    "deferred",
    "superseded",
    "promoted",
]
PromotionTargetName = Literal[
    "glossary",
    "constitution",
    "adr_repository",
    "capsule_repository",
    "execution_backlog",
    "knowledge_repository",
]


@dataclass(frozen=True)
class GovernanceLimits:
    """Bounded resource limits for one repository instance."""

    max_candidates: int = 100_000
    max_groups: int = 25_000
    max_history_entries_per_candidate: int = 512
    max_promotions: int = 100_000
    max_rationale_length: int = 4_096
    max_reviewer_length: int = 128


@dataclass(frozen=True)
class GovernanceValidationIssue:
    """Structured validation issue for review and promotion."""

    issue_id: str
    severity: Literal["info", "warning", "error"]
    error_code: str
    reason: str
    context: Mapping[str, object]
    recoverable: bool


@dataclass(frozen=True)
class ReviewHistoryEntry:
    """Immutable review state transition record."""

    action: str
    from_state: ReviewState
    to_state: ReviewState
    reviewer: str
    rationale: str
    at: str
    event_id: str


@dataclass(frozen=True)
class MergeHistoryEntry:
    """Immutable record of human-approved candidate merge intent."""

    source_candidate_ids: tuple[str, ...]
    target_candidate_id: str
    reviewer: str
    rationale: str
    at: str
    event_id: str


@dataclass(frozen=True)
class PromotionRecord:
    """Durable promoted knowledge record produced by human governance."""

    promotion_id: str
    version: int
    target: PromotionTargetName
    promoted_artifact_id: str
    candidate_ids: tuple[str, ...]
    reviewer: str
    rationale: str
    rollback: str
    promoted_at: str
    artifact: Mapping[str, Any]
    provenance: Mapping[str, Any]


@dataclass(frozen=True)
class CandidateRecord:
    """Repository-owned candidate with review and promotion history."""

    candidate: CandidateArtifact
    state: ReviewState
    version: int
    group_id: str
    created_at: str
    updated_at: str
    review_history: tuple[ReviewHistoryEntry, ...] = ()
    merge_history: tuple[MergeHistoryEntry, ...] = ()
    promotion_history: tuple[PromotionRecord, ...] = ()
    superseded_by: str | None = None


@dataclass(frozen=True)
class CandidateGroup:
    """Deterministic grouping of related candidates."""

    group_id: str
    group_key: str
    candidate_type: str
    candidate_ids: tuple[str, ...]
    title: str


@dataclass(frozen=True)
class ReviewEvent:
    """Canonical event request for governance actions."""

    event_id: str
    event_type: str
    route: str
    payload: Mapping[str, object]
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ReviewEventRecord:
    """Stored event publication result."""

    event: ReviewEvent
    status: str
    failure: GovernanceValidationIssue | None = None


@dataclass(frozen=True)
class ReviewView:
    """Deterministic candidate review view."""

    name: str
    candidate_ids: tuple[str, ...]
    generated_at: str


@dataclass(frozen=True)
class GovernanceActionResult:
    """Result for repository and engine commands."""

    status: str
    candidate_records: tuple[CandidateRecord, ...]
    promotion_records: tuple[PromotionRecord, ...] = ()
    validation_report: tuple[GovernanceValidationIssue, ...] = ()
    events: tuple[ReviewEventRecord, ...] = ()


def to_plain(value: Any) -> Any:
    """Convert governance records into JSON-ready values."""

    if hasattr(value, "__dataclass_fields__"):
        return to_plain(asdict(value))
    if isinstance(value, tuple):
        return [to_plain(item) for item in value]
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): to_plain(item) for key, item in value.items()}
    return value
