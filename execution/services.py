"""Execution services.

Services orchestrate domain models only. They do not persist records, create
observations, or make decisions that belong inside models.
"""

from __future__ import annotations

from .domain import (
    AcceptanceCriterion,
    ArchitecturalBudget,
    BearingReport,
    ChangeBudget,
    Context,
    Constraint,
    Decision,
    DecisionStatus,
    DriftReport,
    Focus,
    ImplementationProposal,
    Intent,
    Mission,
    ParkingLotEntry,
    ParkingLotStatus,
    Progress,
    PromotionStage,
    PromotionState,
    Scope,
)


class MissionService:
    """Create and expose mission health without owning mission rules."""

    def create_mission(
        self,
        *,
        mission_id: str,
        intent: Intent,
        scopes: tuple[Scope, ...],
        focus: Focus,
        contexts: tuple[Context, ...] = (),
        constraints: tuple[Constraint, ...] = (),
        acceptance_criteria: tuple[AcceptanceCriterion, ...] = (),
        change_budget: ChangeBudget = ChangeBudget(max_changed_files=10, max_risk_score=5),
        architectural_budget: ArchitecturalBudget = ArchitecturalBudget(max_new_dependencies=0, max_touched_domains=1),
    ) -> Mission:
        """Build a validated mission value object."""

        return Mission(
            mission_id=mission_id,
            intent=intent,
            scopes=scopes,
            focus=focus,
            contexts=contexts,
            constraints=constraints,
            acceptance_criteria=acceptance_criteria,
            change_budget=change_budget,
            architectural_budget=architectural_budget,
        )

    def health(self, mission: Mission) -> Progress:
        """Expose derived mission health."""

        return mission.progress()


class BearingCheckService:
    """Run the bearing evaluation pipeline."""

    def evaluate(self, mission: Mission, proposal: ImplementationProposal) -> BearingReport:
        return mission.evaluate_bearing(proposal)


class DriftDetectionService:
    """Run drift detection without deciding remediation."""

    def detect(self, mission: Mission, proposal: ImplementationProposal) -> DriftReport:
        return mission.detect_drift(proposal)


class PromotionService:
    """Move ideas through the explicit promotion lifecycle."""

    def capture(self, *, promotion_id: str, subject_id: str, actor: str, reason: str) -> PromotionState:
        return PromotionState(
            promotion_id=promotion_id,
            subject_id=subject_id,
            stage=PromotionStage.CAPTURED,
            actor=actor,
            reason=reason,
        )

    def transition(self, state: PromotionState, target_stage: PromotionStage | str, actor: str, reason: str) -> PromotionState:
        return state.transition(target_stage, actor=actor, reason=reason)


class ProgressService:
    """Compute progress from mission state."""

    def compute(self, mission: Mission) -> Progress:
        return mission.progress()


class ParkingLotService:
    """Capture valuable out-of-scope ideas."""

    def capture(
        self,
        *,
        entry_id: str,
        mission_id: str,
        summary: str,
        reason_out_of_scope: str,
    ) -> ParkingLotEntry:
        return ParkingLotEntry(
            entry_id=entry_id,
            mission_id=mission_id,
            summary=summary,
            reason_out_of_scope=reason_out_of_scope,
            status=ParkingLotStatus.CAPTURED,
        )


class DecisionLedgerService:
    """Create decision records without persistence side effects."""

    def record(
        self,
        *,
        decision_id: str,
        mission_id: str,
        summary: str,
        status: DecisionStatus | str,
        reason: str,
        actor: str,
        reverses_decision_id: str | None = None,
    ) -> Decision:
        return Decision(
            decision_id=decision_id,
            mission_id=mission_id,
            summary=summary,
            status=DecisionStatus(status),
            reason=reason,
            actor=actor,
            reverses_decision_id=reverses_decision_id,
        )
