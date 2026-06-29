"""ARK admission intake membrane.

This module prepares accepted reviewed artifacts for a future observation
creation step. It does not write to ARK, persist data, or create observations.
"""

from __future__ import annotations

from types import MappingProxyType

from artifact_promotion import CandidateArtifact, PromotionDecision

from .interfaces import AdmissionCandidate


def create_admission_candidate(
    candidate_artifact: CandidateArtifact,
    promotion_decision: PromotionDecision,
) -> AdmissionCandidate:
    """Create an admission candidate from an accepted reviewed artifact.

    Inputs: CandidateArtifact and PromotionDecision.
    Outputs: AdmissionCandidate with status="ready_for_observation".
    Runtime: O(metadata key count), bounded by upstream candidate metadata caps.
    Memory: O(metadata key count) plus referenced content.
    Failure: raises ValueError unless the artifact is still a candidate, the
    decision is accepted, artifact ids match, and provenance is present and
    noncanonical.
    Deterministic: yes.
    """

    if candidate_artifact.status != "candidate":
        raise ValueError("candidate artifact status must be candidate")
    if promotion_decision.decision != "accepted":
        raise ValueError("promotion decision must be accepted")
    if candidate_artifact.artifact_id != promotion_decision.artifact_id:
        raise ValueError("promotion decision artifact_id does not match candidate")
    if candidate_artifact.provenance is None:
        raise ValueError("candidate artifact provenance is required")
    if promotion_decision.provenance is None:
        raise ValueError("promotion decision provenance is required")
    if candidate_artifact.provenance.canonical:
        raise ValueError("canonical candidate provenance cannot enter ARK admission")
    if promotion_decision.provenance.canonical:
        raise ValueError("canonical decision provenance cannot enter ARK admission")
    if candidate_artifact.provenance != promotion_decision.provenance:
        raise ValueError("promotion decision provenance must match candidate provenance")
    return AdmissionCandidate(
        artifact_id=candidate_artifact.artifact_id,
        artifact_type=candidate_artifact.artifact_type,
        content=candidate_artifact.content,
        status="ready_for_observation",
        provenance=candidate_artifact.provenance,
        request_id=candidate_artifact.provenance.request_id,
        trace_id=candidate_artifact.provenance.trace_id,
        promotion_reviewer=promotion_decision.reviewer,
        promotion_reason=promotion_decision.reason,
        metadata=MappingProxyType(dict(candidate_artifact.metadata)),
    )
