"""ARK admission boundary interfaces.

This package defines the final membrane between accepted reviewed artifacts and
future observations. It performs no persistence and creates no observations.

Contract:
- Inputs: reviewed candidate artifact data and noncanonical provenance.
- Outputs: immutable admission records.
- Runtime constraint: O(1) plus bounded field sizes inherited from upstream
  artifact promotion and provenance records.
- Memory assumption: O(1) plus referenced artifact content.
- Failure cases: invalid status, missing provenance, canonical provenance, and
  artifact/decision mismatch are rejected by intake.
- Determinism: records are deterministic value objects.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal, Mapping

from provenance import ProvenanceRecord

AdmissionStatus = Literal["ready_for_observation", "rejected", "needs_more_evidence"]
ADMISSION_STATUSES = ("ready_for_observation", "rejected", "needs_more_evidence")


@dataclass(frozen=True)
class AdmissionCandidate:
    """Accepted artifact prepared for a later observation admission step."""

    artifact_id: str
    artifact_type: str
    content: object
    status: AdmissionStatus
    provenance: ProvenanceRecord
    request_id: str
    trace_id: str
    promotion_reviewer: str
    promotion_reason: str
    metadata: Mapping[str, object] = MappingProxyType({})


@dataclass(frozen=True)
class AdmissionResult:
    """Structured admission result with no persistence side effects."""

    status: AdmissionStatus
    candidate: AdmissionCandidate | None
    reason: str
    provenance: ProvenanceRecord | None = None


def validate_admission_status(status: str) -> AdmissionStatus:
    """Validate an admission status.

    Inputs: status string. Outputs: AdmissionStatus.
    Runtime: O(1), bounded by three statuses. Memory: O(1).
    Failure: raises ValueError for invalid status.
    Deterministic: yes.
    """

    if status not in ADMISSION_STATUSES:
        raise ValueError("admission status must be ready_for_observation, rejected, or needs_more_evidence")
    return status  # type: ignore[return-value]
