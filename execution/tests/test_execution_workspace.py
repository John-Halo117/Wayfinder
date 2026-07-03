from pathlib import Path

import yaml

from execution import (
    AcceptanceCriterion,
    AcceptanceStatus,
    ArchitecturalBudget,
    BearingStatus,
    ChangeBudget,
    Constraint,
    DecisionStatus,
    DriftKind,
    Focus,
    ImplementationProposal,
    Intent,
    Mission,
    ParkingLotStatus,
    Scope,
    load_workspace,
    save_workspace,
)


def _mission() -> Mission:
    return Mission(
        mission_id="mission:workspace",
        intent=Intent("intent:workspace", "Use Execution from disk."),
        scopes=(
            Scope("scope:workspace", "Workspace persistence"),
            Scope("scope:ark", "ARK integration", in_scope=False),
        ),
        focus=Focus("focus:workspace", "Persist and evaluate active mission", active_scope_id="scope:workspace"),
        constraints=(Constraint("constraint:no-cli", "Do not add a CLI"),),
        acceptance_criteria=(
            AcceptanceCriterion("acceptance:load-save", "Workspace loads and saves", AcceptanceStatus.SATISFIED),
            AcceptanceCriterion("acceptance:bearing", "Workspace runs bearing checks"),
        ),
        change_budget=ChangeBudget(max_changed_files=6, max_risk_score=3),
        architectural_budget=ArchitecturalBudget(max_new_dependencies=0, max_touched_domains=1),
    )


def _proposal() -> ImplementationProposal:
    return ImplementationProposal(
        proposal_id="proposal:workspace",
        summary="Implement workspace persistence.",
        intent_id="intent:workspace",
        scope_ids=("scope:workspace",),
        addressed_acceptance_ids=("acceptance:bearing",),
        changed_files=3,
        risk_score=2,
        new_dependencies=0,
        touched_domains=1,
    )


def test_workspace_load_save_creates_repository_layout(tmp_path: Path):
    workspace = load_workspace(tmp_path)

    assert workspace.workspace_path == tmp_path / ".execution"
    assert (tmp_path / ".execution" / "history").is_dir()
    assert (tmp_path / ".execution" / "completed").is_dir()
    assert (tmp_path / ".execution" / "parking_lot.yaml").exists()
    assert (tmp_path / ".execution" / "decisions.yaml").exists()

    workspace.activate_mission(_mission())
    save_workspace(workspace)
    reloaded = load_workspace(tmp_path)

    assert reloaded.get_active_mission().mission_id == "mission:workspace"
    assert reloaded.get_active_mission().intent.intent_id == "intent:workspace"


def test_mission_activation_persists_active_mission(tmp_path: Path):
    workspace = load_workspace(tmp_path)

    mission = workspace.activate_mission(_mission())

    active_data = yaml.safe_load((tmp_path / ".execution" / "active_mission.yaml").read_text(encoding="utf-8"))
    assert mission.mission_id == "mission:workspace"
    assert active_data["mission_id"] == "mission:workspace"


def test_mission_completion_archives_and_clears_active_mission(tmp_path: Path):
    workspace = load_workspace(tmp_path)
    workspace.activate_mission(_mission())

    completed = workspace.complete_mission()
    reloaded = load_workspace(tmp_path)

    assert completed.mission_id == "mission:workspace"
    assert not (tmp_path / ".execution" / "active_mission.yaml").exists()
    assert (tmp_path / ".execution" / "completed" / "mission_workspace.yaml").exists()
    assert reloaded.active_mission is None


def test_parking_lot_persistence(tmp_path: Path):
    workspace = load_workspace(tmp_path)
    workspace.activate_mission(_mission())

    entry = workspace.add_parking_lot_entry(
        entry_id="parking:ark-integration",
        summary="ARK integration will matter later.",
        reason_out_of_scope="Current workspace mission explicitly excludes ARK integration.",
    )
    reloaded = load_workspace(tmp_path)

    assert entry.status is ParkingLotStatus.CAPTURED
    assert len(reloaded.parking_lot_entries) == 1
    assert reloaded.parking_lot_entries[0].entry_id == "parking:ark-integration"


def test_decision_persistence(tmp_path: Path):
    workspace = load_workspace(tmp_path)
    workspace.activate_mission(_mission())

    decision = workspace.add_decision(
        decision_id="decision:workspace-format",
        summary="Use YAML files for workspace state.",
        status=DecisionStatus.ACCEPTED,
        reason="The requested workspace layout is YAML.",
        actor="tester",
    )
    reloaded = load_workspace(tmp_path)

    assert decision.status is DecisionStatus.ACCEPTED
    assert len(reloaded.decisions) == 1
    assert reloaded.decisions[0].decision_id == "decision:workspace-format"


def test_workspace_progress_is_derived(tmp_path: Path):
    workspace = load_workspace(tmp_path)
    workspace.activate_mission(_mission())

    progress = workspace.get_progress()

    assert progress.satisfied_count == 1
    assert progress.total_count == 2
    assert progress.completion_ratio == 0.5


def test_workspace_runs_bearing_check(tmp_path: Path):
    workspace = load_workspace(tmp_path)
    workspace.activate_mission(_mission())

    report = workspace.run_bearing_check(_proposal())

    assert report.status is BearingStatus.ALIGNED
    assert report.mission_id == "mission:workspace"


def test_workspace_runs_drift_detection(tmp_path: Path):
    workspace = load_workspace(tmp_path)
    workspace.activate_mission(_mission())
    proposal = ImplementationProposal(
        proposal_id="proposal:ark-now",
        summary="Integrate ARK immediately.",
        intent_id="intent:workspace",
        scope_ids=("scope:ark",),
        addressed_acceptance_ids=("acceptance:bearing",),
        changed_files=8,
        risk_score=4,
        new_dependencies=1,
        touched_domains=2,
    )

    report = workspace.run_drift_detection(proposal)

    assert report.has_drift
    assert {finding.kind for finding in report.findings} == {
        DriftKind.SCOPE,
        DriftKind.FOCUS,
        DriftKind.ARCHITECTURAL,
        DriftKind.BUDGET,
    }
