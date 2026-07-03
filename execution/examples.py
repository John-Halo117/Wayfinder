"""Small Execution examples used by documentation and tests."""

from __future__ import annotations

from .domain import (
    AcceptanceCriterion,
    AcceptanceStatus,
    ArchitecturalBudget,
    ChangeBudget,
    Constraint,
    Context,
    Focus,
    ImplementationProposal,
    Intent,
    Mission,
    PromotionStage,
    Scope,
)
from .services import BearingCheckService, DriftDetectionService, PromotionService


def example_mission() -> Mission:
    return Mission(
        mission_id="mission:execution-initial-domain",
        intent=Intent(
            intent_id="intent:execution-domain",
            statement="Create the initial Execution domain for preserving software-building process.",
        ),
        scopes=(
            Scope("scope:models", "Execution domain models"),
            Scope("scope:services", "Thin orchestration services"),
            Scope("scope:tests", "Focused domain tests"),
            Scope("scope:task-manager", "Task management features", in_scope=False),
        ),
        focus=Focus(
            focus_id="focus:bearing",
            description="Bearing and drift evaluation",
            active_scope_id="scope:models",
        ),
        contexts=(Context("context:wayfinder-style", "Immutable dataclasses and explicit validation helpers."),),
        constraints=(Constraint("constraint:no-frameworks", "Do not introduce frameworks."),),
        acceptance_criteria=(
            AcceptanceCriterion("acceptance:models", "Models exist", AcceptanceStatus.SATISFIED),
            AcceptanceCriterion("acceptance:bearing", "Bearing report is structured", AcceptanceStatus.SATISFIED),
            AcceptanceCriterion("acceptance:docs", "README explains the domain"),
        ),
        change_budget=ChangeBudget(max_changed_files=8, max_risk_score=4),
        architectural_budget=ArchitecturalBudget(max_new_dependencies=0, max_touched_domains=1),
    )


def example_bearing_check():
    mission = example_mission()
    proposal = ImplementationProposal(
        proposal_id="proposal:bearing-service",
        summary="Add bearing check service around Mission.evaluate_bearing.",
        intent_id="intent:execution-domain",
        scope_ids=("scope:models", "scope:services"),
        addressed_acceptance_ids=("acceptance:bearing",),
        changed_files=3,
        risk_score=2,
        new_dependencies=0,
        touched_domains=1,
    )
    return BearingCheckService().evaluate(mission, proposal)


def example_drift_report():
    mission = example_mission()
    proposal = ImplementationProposal(
        proposal_id="proposal:task-board",
        summary="Add task-board workflow while building Execution.",
        intent_id="intent:execution-domain",
        scope_ids=("scope:task-manager",),
        addressed_acceptance_ids=("acceptance:models",),
        changed_files=12,
        risk_score=5,
        new_dependencies=1,
        touched_domains=2,
    )
    return DriftDetectionService().detect(mission, proposal)


def example_promotion_lifecycle():
    service = PromotionService()
    state = service.capture(
        promotion_id="promotion:execution-bearings",
        subject_id="idea:bearing-check",
        actor="example",
        reason="valuable execution concept captured",
    )
    for stage in (
        PromotionStage.RESEARCH,
        PromotionStage.SANDBOX,
        PromotionStage.PROTOTYPE,
        PromotionStage.CAPABILITY,
    ):
        state = service.transition(state, stage, actor="example", reason=f"advance to {stage.value}")
    return state
