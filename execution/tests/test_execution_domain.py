import pytest

from execution import (
    AcceptanceCriterion,
    AcceptanceStatus,
    ArchitecturalBudget,
    BearingCheckKind,
    BearingCheckService,
    BearingStatus,
    ChangeBudget,
    Constraint,
    DecisionLedgerService,
    DecisionStatus,
    DriftDetectionService,
    DriftKind,
    Focus,
    ImplementationProposal,
    Intent,
    Mission,
    MissionService,
    ParkingLotService,
    ParkingLotStatus,
    ProgressService,
    PromotionService,
    PromotionStage,
    Scope,
)
from execution.examples import (
    example_bearing_check,
    example_drift_report,
    example_mission,
    example_promotion_lifecycle,
)


def _mission() -> Mission:
    return Mission(
        mission_id="mission:execution",
        intent=Intent("intent:execution", "Create the Execution domain."),
        scopes=(
            Scope("scope:models", "Domain models"),
            Scope("scope:services", "Orchestration services"),
            Scope("scope:task-manager", "Task management", in_scope=False),
        ),
        focus=Focus("focus:models", "Build models first", active_scope_id="scope:models"),
        constraints=(Constraint("constraint:no-frameworks", "No frameworks"),),
        acceptance_criteria=(
            AcceptanceCriterion("acceptance:models", "Models exist", AcceptanceStatus.SATISFIED),
            AcceptanceCriterion("acceptance:tests", "Tests exist"),
        ),
        change_budget=ChangeBudget(max_changed_files=5, max_risk_score=3),
        architectural_budget=ArchitecturalBudget(max_new_dependencies=0, max_touched_domains=1),
    )


def test_bearing_report_is_structured_and_aligned_for_in_scope_work():
    mission = _mission()
    proposal = ImplementationProposal(
        proposal_id="proposal:models",
        summary="Add execution models.",
        intent_id="intent:execution",
        scope_ids=("scope:models",),
        addressed_acceptance_ids=("acceptance:models",),
        changed_files=2,
        risk_score=1,
        new_dependencies=0,
        touched_domains=1,
    )

    report = BearingCheckService().evaluate(mission, proposal)

    assert report.status is BearingStatus.ALIGNED
    assert report.aligned
    assert {check.kind for check in report.checks} == {
        BearingCheckKind.INTENT_ALIGNMENT,
        BearingCheckKind.SCOPE_COMPLIANCE,
        BearingCheckKind.FOCUS_ALIGNMENT,
        BearingCheckKind.CONSTRAINT_COMPLIANCE,
        BearingCheckKind.ACCEPTANCE_IMPACT,
        BearingCheckKind.CHANGE_BUDGET_COMPLIANCE,
        BearingCheckKind.ARCHITECTURAL_BUDGET_COMPLIANCE,
    }


def test_bearing_report_marks_out_of_scope_work_misaligned():
    proposal = ImplementationProposal(
        proposal_id="proposal:task-manager",
        summary="Add task manager board.",
        intent_id="intent:execution",
        scope_ids=("scope:task-manager",),
        addressed_acceptance_ids=("acceptance:models",),
        changed_files=2,
        risk_score=1,
    )

    report = BearingCheckService().evaluate(_mission(), proposal)

    assert report.status is BearingStatus.MISALIGNED
    scope_check = next(check for check in report.checks if check.kind is BearingCheckKind.SCOPE_COMPLIANCE)
    assert "scope:task-manager" in scope_check.evidence


def test_drift_report_describes_findings_without_deciding():
    proposal = ImplementationProposal(
        proposal_id="proposal:large-redesign",
        summary="Add a redesign outside the current focus.",
        intent_id="intent:other",
        scope_ids=("scope:task-manager",),
        addressed_acceptance_ids=("acceptance:models",),
        changed_files=12,
        risk_score=8,
        new_dependencies=1,
        touched_domains=3,
    )

    report = DriftDetectionService().detect(_mission(), proposal)

    assert report.has_drift
    assert {finding.kind for finding in report.findings} == {
        DriftKind.MISSION,
        DriftKind.SCOPE,
        DriftKind.FOCUS,
        DriftKind.ARCHITECTURAL,
        DriftKind.BUDGET,
    }


def test_progress_is_derived_from_acceptance_criteria():
    progress = ProgressService().compute(_mission())

    assert progress.satisfied_count == 1
    assert progress.total_count == 2
    assert progress.completion_ratio == 0.5
    assert not progress.complete


def test_parking_lot_captures_out_of_scope_idea():
    entry = ParkingLotService().capture(
        entry_id="parking:task-board",
        mission_id="mission:execution",
        summary="Task board may be useful later.",
        reason_out_of_scope="Current mission is Execution, not task management.",
    )

    assert entry.status is ParkingLotStatus.CAPTURED
    assert entry.mission_id == "mission:execution"


def test_promotion_lifecycle_is_explicit_and_reversible_one_step():
    service = PromotionService()
    captured = service.capture(
        promotion_id="promotion:bearing",
        subject_id="idea:bearing",
        actor="tester",
        reason="captured during execution design",
    )
    research = service.transition(captured, PromotionStage.RESEARCH, actor="tester", reason="needs study")
    captured_again = service.transition(research, PromotionStage.CAPTURED, actor="tester", reason="not ready")

    assert research.stage is PromotionStage.RESEARCH
    assert research.previous_stage is PromotionStage.CAPTURED
    assert captured_again.stage is PromotionStage.CAPTURED
    with pytest.raises(ValueError, match="one lifecycle step"):
        service.transition(captured_again, PromotionStage.PROTOTYPE, actor="tester", reason="skip")


def test_decision_ledger_creates_reversible_decision_record():
    decision = DecisionLedgerService().record(
        decision_id="decision:1",
        mission_id="mission:execution",
        summary="Keep services thin.",
        status=DecisionStatus.ACCEPTED,
        reason="Business rules belong in models.",
        actor="tester",
    )
    reversal = DecisionLedgerService().record(
        decision_id="decision:2",
        mission_id="mission:execution",
        summary="Reverse prior decision.",
        status=DecisionStatus.REVERSED,
        reason="New evidence changed the boundary.",
        actor="tester",
        reverses_decision_id=decision.decision_id,
    )

    assert reversal.reverses_decision_id == decision.decision_id


def test_mission_service_creates_validated_mission():
    mission = MissionService().create_mission(
        mission_id="mission:service",
        intent=Intent("intent:service", "Create through service."),
        scopes=(Scope("scope:service", "Service scope"),),
        focus=Focus("focus:service", "Service focus", active_scope_id="scope:service"),
    )

    assert mission.mission_id == "mission:service"


def test_invalid_focus_scope_fails_fast():
    with pytest.raises(ValueError, match="active_scope_id"):
        Mission(
            mission_id="mission:bad",
            intent=Intent("intent:bad", "Bad mission."),
            scopes=(Scope("scope:one", "One"),),
            focus=Focus("focus:bad", "Bad focus", active_scope_id="scope:missing"),
        )


def test_examples_are_executable():
    assert example_mission().mission_id == "mission:execution-initial-domain"
    assert example_bearing_check().status is BearingStatus.ALIGNED
    assert example_drift_report().has_drift
    assert example_promotion_lifecycle().stage is PromotionStage.CAPABILITY
