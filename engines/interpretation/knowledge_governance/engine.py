"""Knowledge review and promotion engine."""

from __future__ import annotations

from engines.interpretation.knowledge_compiler.models import CandidateArtifact

from .models import GovernanceActionResult, PromotionTargetName
from .repository import CandidateRepository


class KnowledgeGovernanceEngine:
    """Human-governed facade for candidate review and promotion."""

    def __init__(self, repository: CandidateRepository | None = None) -> None:
        self._repository = repository or CandidateRepository()

    @property
    def repository(self) -> CandidateRepository:
        return self._repository

    def store_candidates(self, candidates: tuple[CandidateArtifact, ...]) -> GovernanceActionResult:
        """Store compiler-produced candidates in discovered state."""

        return self._repository.add_candidates(candidates)

    def start_review(self, candidate_id: str, *, reviewer: str, rationale: str) -> GovernanceActionResult:
        return self._repository.transition(
            candidate_id,
            "under_review",
            action="start_review",
            reviewer=reviewer,
            rationale=rationale,
        )

    def approve(self, candidate_id: str, *, reviewer: str, rationale: str) -> GovernanceActionResult:
        return self._repository.transition(
            candidate_id,
            "approved",
            action="approve",
            reviewer=reviewer,
            rationale=rationale,
        )

    def reject(self, candidate_id: str, *, reviewer: str, rationale: str) -> GovernanceActionResult:
        return self._repository.transition(
            candidate_id,
            "rejected",
            action="reject",
            reviewer=reviewer,
            rationale=rationale,
        )

    def defer(self, candidate_id: str, *, reviewer: str, rationale: str) -> GovernanceActionResult:
        return self._repository.transition(
            candidate_id,
            "deferred",
            action="defer",
            reviewer=reviewer,
            rationale=rationale,
        )

    def supersede(
        self,
        candidate_id: str,
        *,
        superseded_by: str,
        reviewer: str,
        rationale: str,
    ) -> GovernanceActionResult:
        return self._repository.transition(
            candidate_id,
            "superseded",
            action="supersede",
            reviewer=reviewer,
            rationale=rationale,
            superseded_by=superseded_by,
        )

    def merge(
        self,
        source_candidate_ids: tuple[str, ...],
        *,
        target_candidate_id: str,
        reviewer: str,
        rationale: str,
    ) -> GovernanceActionResult:
        return self._repository.merge(
            source_candidate_ids,
            target_candidate_id,
            reviewer=reviewer,
            rationale=rationale,
        )

    def promote(
        self,
        candidate_id: str,
        *,
        target: PromotionTargetName,
        reviewer: str,
        rationale: str,
        rollback: str,
    ) -> GovernanceActionResult:
        return self._repository.promote(
            candidate_id,
            target=target,
            reviewer=reviewer,
            rationale=rationale,
            rollback=rollback,
        )

    def review_views(self):
        """Return deterministic review views."""

        return self._repository.views()
