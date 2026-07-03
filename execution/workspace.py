"""Execution workspace persistence.

The workspace loads and saves Execution records from a repository-local
`.execution` directory. It owns persistence only; mission rules remain in the
Execution domain and orchestration services.

Contract:
- Inputs: workspace path, mission records, proposals, decision fields, and
  parking lot fields.
- Outputs: immutable domain records and structured reports.
- Runtime constraint: O(serialized workspace records), bounded by domain caps.
- Memory assumption: O(serialized workspace records).
- Failure cases: missing active mission, malformed YAML, invalid domain fields,
  or non-mapping/list workspace documents raise ValueError.
- Determinism: serialization uses sorted keys and stable filenames.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .domain import (
    AcceptanceCriterion,
    AcceptanceStatus,
    ArchitecturalBudget,
    AttentionBudget,
    BearingReport,
    ChangeBudget,
    Constraint,
    ConstraintKind,
    Context,
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
    Scope,
)
from .services import (
    BearingCheckService,
    DecisionLedgerService,
    DriftDetectionService,
    ParkingLotService,
    ProgressService,
)

WORKSPACE_DIR_NAME = ".execution"
ACTIVE_MISSION_FILE = "active_mission.yaml"
PARKING_LOT_FILE = "parking_lot.yaml"
DECISIONS_FILE = "decisions.yaml"
HISTORY_DIR = "history"
COMPLETED_DIR = "completed"


@dataclass
class ExecutionWorkspace:
    """Disk-backed Execution workspace state."""

    workspace_path: Path
    active_mission: Mission | None
    parking_lot_entries: tuple[ParkingLotEntry, ...]
    decisions: tuple[Decision, ...]

    def save_workspace(self, path: str | Path | None = None) -> None:
        """Persist the current workspace state."""

        target = _resolve_workspace_path(path) if path is not None else self.workspace_path
        _ensure_layout(target)
        if self.active_mission is None:
            _remove_if_exists(target / ACTIVE_MISSION_FILE)
        else:
            _write_yaml(target / ACTIVE_MISSION_FILE, _mission_to_data(self.active_mission))
        _write_yaml(target / PARKING_LOT_FILE, [_parking_lot_entry_to_data(entry) for entry in self.parking_lot_entries])
        _write_yaml(target / DECISIONS_FILE, [_decision_to_data(decision) for decision in self.decisions])
        self.workspace_path = target

    def get_active_mission(self) -> Mission:
        """Return the active mission or fail fast."""

        if self.active_mission is None:
            raise ValueError("active mission is required")
        return self.active_mission

    def activate_mission(self, mission: Mission) -> Mission:
        """Set one active mission and persist it."""

        self.active_mission = mission
        self.save_workspace()
        return mission

    def complete_mission(self) -> Mission:
        """Archive the active mission and clear the active slot."""

        mission = self.get_active_mission()
        _ensure_layout(self.workspace_path)
        completed_path = self.workspace_path / COMPLETED_DIR / f"{_safe_filename(mission.mission_id)}.yaml"
        _write_yaml(completed_path, _mission_to_data(mission))
        history_path = self.workspace_path / HISTORY_DIR / f"completed-{_safe_filename(mission.mission_id)}.yaml"
        _write_yaml(history_path, {"event": "completed", "mission_id": mission.mission_id})
        self.active_mission = None
        self.save_workspace()
        return mission

    def add_parking_lot_entry(
        self,
        *,
        entry_id: str,
        summary: str,
        reason_out_of_scope: str,
        mission_id: str | None = None,
    ) -> ParkingLotEntry:
        """Capture an out-of-scope idea and persist it."""

        resolved_mission_id = mission_id or self.get_active_mission().mission_id
        entry = ParkingLotService().capture(
            entry_id=entry_id,
            mission_id=resolved_mission_id,
            summary=summary,
            reason_out_of_scope=reason_out_of_scope,
        )
        self.parking_lot_entries = self.parking_lot_entries + (entry,)
        self.save_workspace()
        return entry

    def add_decision(
        self,
        *,
        decision_id: str,
        summary: str,
        status: DecisionStatus | str,
        reason: str,
        actor: str,
        mission_id: str | None = None,
        reverses_decision_id: str | None = None,
    ) -> Decision:
        """Record a decision and persist it."""

        resolved_mission_id = mission_id or self.get_active_mission().mission_id
        decision = DecisionLedgerService().record(
            decision_id=decision_id,
            mission_id=resolved_mission_id,
            summary=summary,
            status=status,
            reason=reason,
            actor=actor,
            reverses_decision_id=reverses_decision_id,
        )
        self.decisions = self.decisions + (decision,)
        self.save_workspace()
        return decision

    def run_bearing_check(self, proposal: ImplementationProposal) -> BearingReport:
        """Run the bearing pipeline for the active mission."""

        return BearingCheckService().evaluate(self.get_active_mission(), proposal)

    def run_drift_detection(self, proposal: ImplementationProposal) -> DriftReport:
        """Run drift detection for the active mission."""

        return DriftDetectionService().detect(self.get_active_mission(), proposal)

    def get_progress(self) -> Progress:
        """Compute derived progress for the active mission."""

        return ProgressService().compute(self.get_active_mission())


def load_workspace(path: str | Path) -> ExecutionWorkspace:
    """Load or initialize an Execution workspace."""

    workspace_path = _resolve_workspace_path(path)
    _ensure_layout(workspace_path)
    active_mission = _load_optional_mission(workspace_path / ACTIVE_MISSION_FILE)
    parking_lot_entries = tuple(
        _parking_lot_entry_from_data(item) for item in _read_yaml_list(workspace_path / PARKING_LOT_FILE)
    )
    decisions = tuple(_decision_from_data(item) for item in _read_yaml_list(workspace_path / DECISIONS_FILE))
    return ExecutionWorkspace(
        workspace_path=workspace_path,
        active_mission=active_mission,
        parking_lot_entries=parking_lot_entries,
        decisions=decisions,
    )


def save_workspace(workspace: ExecutionWorkspace, path: str | Path | None = None) -> None:
    """Persist a loaded workspace."""

    workspace.save_workspace(path)


def _resolve_workspace_path(path: str | Path) -> Path:
    raw = Path(path)
    if raw.name == WORKSPACE_DIR_NAME:
        return raw
    return raw / WORKSPACE_DIR_NAME


def _ensure_layout(workspace_path: Path) -> None:
    workspace_path.mkdir(parents=True, exist_ok=True)
    (workspace_path / HISTORY_DIR).mkdir(exist_ok=True)
    (workspace_path / COMPLETED_DIR).mkdir(exist_ok=True)
    if not (workspace_path / PARKING_LOT_FILE).exists():
        _write_yaml(workspace_path / PARKING_LOT_FILE, [])
    if not (workspace_path / DECISIONS_FILE).exists():
        _write_yaml(workspace_path / DECISIONS_FILE, [])


def _load_optional_mission(path: Path) -> Mission | None:
    if not path.exists():
        return None
    return _mission_from_data(_read_yaml_mapping(path))


def _read_yaml_mapping(path: Path) -> dict[str, Any]:
    data = _read_yaml(path)
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must contain a mapping")
    return data


def _read_yaml_list(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = _read_yaml(path)
    if data is None:
        return []
    if not isinstance(data, list):
        raise ValueError(f"{path.name} must contain a list")
    for item in data:
        if not isinstance(item, dict):
            raise ValueError(f"{path.name} entries must be mappings")
    return data


def _read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _write_yaml(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=True)


def _remove_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()


def _mission_to_data(mission: Mission) -> dict[str, Any]:
    return {
        "mission_id": mission.mission_id,
        "intent": {"intent_id": mission.intent.intent_id, "statement": mission.intent.statement},
        "scopes": [
            {"scope_id": scope.scope_id, "description": scope.description, "in_scope": scope.in_scope}
            for scope in mission.scopes
        ],
        "focus": {
            "focus_id": mission.focus.focus_id,
            "description": mission.focus.description,
            "active_scope_id": mission.focus.active_scope_id,
        },
        "contexts": [{"context_id": context.context_id, "summary": context.summary} for context in mission.contexts],
        "constraints": [
            {
                "constraint_id": constraint.constraint_id,
                "description": constraint.description,
                "kind": constraint.kind.value,
            }
            for constraint in mission.constraints
        ],
        "acceptance_criteria": [
            {
                "criterion_id": criterion.criterion_id,
                "description": criterion.description,
                "status": criterion.status.value,
            }
            for criterion in mission.acceptance_criteria
        ],
        "change_budget": {
            "max_changed_files": mission.change_budget.max_changed_files,
            "max_risk_score": mission.change_budget.max_risk_score,
        },
        "architectural_budget": {
            "max_new_dependencies": mission.architectural_budget.max_new_dependencies,
            "max_touched_domains": mission.architectural_budget.max_touched_domains,
        },
        "attention_budget": {"max_active_items": mission.attention_budget.max_active_items},
    }


def _mission_from_data(data: dict[str, Any]) -> Mission:
    intent_data = _required_mapping(data, "intent")
    focus_data = _required_mapping(data, "focus")
    change_budget_data = _optional_mapping(data, "change_budget")
    architectural_budget_data = _optional_mapping(data, "architectural_budget")
    attention_budget_data = _optional_mapping(data, "attention_budget")
    return Mission(
        mission_id=_required_str(data, "mission_id"),
        intent=Intent(
            intent_id=_required_str(intent_data, "intent_id"),
            statement=_required_str(intent_data, "statement"),
        ),
        scopes=tuple(
            Scope(
                scope_id=_required_str(item, "scope_id"),
                description=_required_str(item, "description"),
                in_scope=bool(item.get("in_scope", True)),
            )
            for item in _optional_mapping_list(data, "scopes")
        ),
        focus=Focus(
            focus_id=_required_str(focus_data, "focus_id"),
            description=_required_str(focus_data, "description"),
            active_scope_id=_optional_str(focus_data, "active_scope_id"),
        ),
        contexts=tuple(
            Context(context_id=_required_str(item, "context_id"), summary=_required_str(item, "summary"))
            for item in _optional_mapping_list(data, "contexts")
        ),
        constraints=tuple(
            Constraint(
                constraint_id=_required_str(item, "constraint_id"),
                description=_required_str(item, "description"),
                kind=ConstraintKind(_required_str(item, "kind")),
            )
            for item in _optional_mapping_list(data, "constraints")
        ),
        acceptance_criteria=tuple(
            AcceptanceCriterion(
                criterion_id=_required_str(item, "criterion_id"),
                description=_required_str(item, "description"),
                status=AcceptanceStatus(_required_str(item, "status")),
            )
            for item in _optional_mapping_list(data, "acceptance_criteria")
        ),
        change_budget=ChangeBudget(
            max_changed_files=int(change_budget_data.get("max_changed_files", 10)),
            max_risk_score=int(change_budget_data.get("max_risk_score", 5)),
        ),
        architectural_budget=ArchitecturalBudget(
            max_new_dependencies=int(architectural_budget_data.get("max_new_dependencies", 0)),
            max_touched_domains=int(architectural_budget_data.get("max_touched_domains", 1)),
        ),
        attention_budget=AttentionBudget(max_active_items=int(attention_budget_data.get("max_active_items", 7))),
    )


def _parking_lot_entry_to_data(entry: ParkingLotEntry) -> dict[str, Any]:
    return {
        "entry_id": entry.entry_id,
        "mission_id": entry.mission_id,
        "summary": entry.summary,
        "reason_out_of_scope": entry.reason_out_of_scope,
        "status": entry.status.value,
    }


def _parking_lot_entry_from_data(data: dict[str, Any]) -> ParkingLotEntry:
    return ParkingLotEntry(
        entry_id=_required_str(data, "entry_id"),
        mission_id=_required_str(data, "mission_id"),
        summary=_required_str(data, "summary"),
        reason_out_of_scope=_required_str(data, "reason_out_of_scope"),
        status=ParkingLotStatus(_required_str(data, "status")),
    )


def _decision_to_data(decision: Decision) -> dict[str, Any]:
    return {
        "decision_id": decision.decision_id,
        "mission_id": decision.mission_id,
        "summary": decision.summary,
        "status": decision.status.value,
        "reason": decision.reason,
        "actor": decision.actor,
        "reverses_decision_id": decision.reverses_decision_id,
    }


def _decision_from_data(data: dict[str, Any]) -> Decision:
    return Decision(
        decision_id=_required_str(data, "decision_id"),
        mission_id=_required_str(data, "mission_id"),
        summary=_required_str(data, "summary"),
        status=DecisionStatus(_required_str(data, "status")),
        reason=_required_str(data, "reason"),
        actor=_required_str(data, "actor"),
        reverses_decision_id=_optional_str(data, "reverses_decision_id"),
    )


def _required_mapping(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key} is required")
    return value


def _optional_mapping(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key, {})
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be a mapping")
    return value


def _optional_mapping_list(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.get(key, [])
    if not isinstance(value, list):
        raise ValueError(f"{key} must be a list")
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(f"{key} entries must be mappings")
    return value


def _required_str(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str):
        raise ValueError(f"{key} is required")
    return value


def _optional_str(data: dict[str, Any], key: str) -> str | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string")
    return value


def _safe_filename(value: str) -> str:
    allowed = []
    for character in value:
        if character.isalnum() or character in ("-", "_"):
            allowed.append(character)
        else:
            allowed.append("_")
    return "".join(allowed)
