"""Artifact promotion review membrane.

Review decisions are records only. Accepted decisions do not persist artifacts,
create observations, or write to ARK.
"""

from __future__ import annotations

from .interfaces import (
    CandidateArtifact,
    PromotionDecision,
    normalize_reason,
    normalize_reviewer,
    validate_review_decision,
)


def review_candidate(
    candidate: CandidateArtifact,
    decision: str,
    reviewer: str,
    reason: str | None = None,
) -> PromotionDecision:
    """Review a candidate artifact without persistence side effects.

    Inputs: CandidateArtifact, decision, reviewer, optional reason.
    Outputs: PromotionDecision.
    Runtime: O(reason + reviewer length), bounded by field caps.
    Memory: O(1).
    Failure: raises ValueError for non-candidate input, invalid decision, or
    invalid reviewer/reason.
    Deterministic: yes.
    """

    if candidate.status != "candidate":
        raise ValueError("only candidate artifacts can be reviewed")
    reviewed_status = validate_review_decision(decision.strip())
    return PromotionDecision(
        artifact_id=candidate.artifact_id,
        status=reviewed_status,
        reason=normalize_reason(reason, f"candidate {reviewed_status}"),
        reviewer=normalize_reviewer(reviewer),
        provenance=candidate.provenance,
    )
