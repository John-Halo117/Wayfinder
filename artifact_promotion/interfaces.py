"""Artifact promotion boundary interfaces.

This package declares candidate and decision records only. It performs no ARK
writes and does not promote observations.

Contract:
- Inputs: explicit artifact fields and provenance.
- Outputs: immutable candidate and decision records.
- Runtime constraint: O(metadata key count), bounded by caller caps.
- Memory assumption: O(metadata key count), bounded by caller caps.
- Failure cases: invalid status values are rejected by helper validation.
- Determinism: records are deterministic value objects.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal, Mapping

from provenance import ProvenanceRecord

PromotionStatus = Literal["candidate", "accepted", "rejected", "needs_review"]
PROMOTION_STATUSES = ("candidate", "accepted", "rejected", "needs_review")
REVIEW_DECISION_STATUSES = ("accepted", "rejected", "needs_review")
MAX_ARTIFACT_ID_LENGTH = 160
MAX_ARTIFACT_TYPE_LENGTH = 96
MAX_REASON_LENGTH = 512
MAX_REVIEWER_LENGTH = 128
MAX_METADATA_KEYS = 16
MAX_METADATA_VALUE_LENGTH = 512


@dataclass(frozen=True)
class CandidateArtifact:
    """Non-observation artifact candidate awaiting explicit promotion review."""

    artifact_id: str
    artifact_type: str
    content: object
    provenance: ProvenanceRecord
    status: PromotionStatus = "candidate"
    metadata: Mapping[str, object] = MappingProxyType({})


@dataclass(frozen=True)
class PromotionDecision:
    """Promotion decision record with no persistence side effects."""

    artifact_id: str
    status: PromotionStatus
    reason: str
    reviewer: str
    provenance: ProvenanceRecord

    @property
    def decision(self) -> PromotionStatus:
        """Backward-compatible decision alias for review status.

        Inputs: none. Outputs: PromotionStatus.
        Runtime: O(1). Memory: O(1).
        Failure: none. Deterministic: yes.
        """

        return self.status


def validate_promotion_status(status: str) -> PromotionStatus:
    """Validate a promotion status.

    Inputs: status string. Outputs: PromotionStatus.
    Runtime: O(1), bounded by four statuses. Memory: O(1).
    Failure: raises ValueError for invalid status.
    Deterministic: yes.
    """

    if status not in PROMOTION_STATUSES:
        raise ValueError("promotion status must be candidate, accepted, rejected, or needs_review")
    return status  # type: ignore[return-value]


def freeze_metadata(metadata: Mapping[str, object] | None = None) -> Mapping[str, object]:
    """Return bounded immutable metadata.

    Inputs: optional metadata mapping. Outputs: immutable metadata mapping.
    Runtime: O(metadata key count), bounded by MAX_METADATA_KEYS.
    Memory: O(metadata key count).
    Failure: raises ValueError for oversized metadata.
    Deterministic: yes.
    """

    normalized = dict(metadata or {})
    if len(normalized) > MAX_METADATA_KEYS:
        raise ValueError("metadata exceeds maximum key count")
    checked: dict[str, object] = {}
    for key, value in normalized.items():
        key_text = _normalize_text(str(key), "metadata key", MAX_ARTIFACT_TYPE_LENGTH)
        if len(str(value)) > MAX_METADATA_VALUE_LENGTH:
            raise ValueError("metadata value exceeds maximum length")
        checked[key_text] = value
    return MappingProxyType(checked)


def normalize_artifact_type(artifact_type: str) -> str:
    """Normalize artifact type.

    Inputs: artifact type. Outputs: normalized artifact type.
    Runtime: O(len(artifact_type)), bounded by MAX_ARTIFACT_TYPE_LENGTH.
    Memory: O(len(artifact_type)).
    Failure: raises ValueError for missing or oversized value.
    Deterministic: yes.
    """

    return _normalize_text(artifact_type, "artifact_type", MAX_ARTIFACT_TYPE_LENGTH).lower()


def normalize_reviewer(reviewer: str) -> str:
    """Normalize reviewer id.

    Inputs: reviewer. Outputs: normalized reviewer.
    Runtime: O(len(reviewer)), bounded by MAX_REVIEWER_LENGTH.
    Memory: O(len(reviewer)).
    Failure: raises ValueError for missing or oversized value.
    Deterministic: yes.
    """

    return _normalize_text(reviewer, "reviewer", MAX_REVIEWER_LENGTH)


def normalize_reason(reason: str | None, default: str) -> str:
    """Normalize decision reason.

    Inputs: optional reason and default. Outputs: reason string.
    Runtime: O(len(reason)), bounded by MAX_REASON_LENGTH.
    Memory: O(len(reason)).
    Failure: raises ValueError for oversized value.
    Deterministic: yes.
    """

    value = default if reason is None or not reason.strip() else reason
    return _normalize_text(value, "reason", MAX_REASON_LENGTH)


def validate_review_decision(decision: str) -> PromotionStatus:
    """Validate a review decision.

    Inputs: decision string. Outputs: PromotionStatus.
    Runtime: O(1), bounded by three statuses. Memory: O(1).
    Failure: raises ValueError for invalid decision.
    Deterministic: yes.
    """

    if decision not in REVIEW_DECISION_STATUSES:
        raise ValueError("decision must be accepted, rejected, or needs_review")
    return decision  # type: ignore[return-value]


def _normalize_text(value: str, field: str, max_length: int) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field} is required")
    if len(normalized) > max_length:
        raise ValueError(f"{field} exceeds maximum length")
    return normalized
