# Execution

Execution is the Wayfinder domain for preserving the process of building
reality.

It is not a task manager and not a project management tool. It answers whether
current work still serves the mission, whether scope is expanding, whether
constraints are being honored, and whether an idea should be captured instead
of implemented now.

## Boundary

Execution owns:

- Intent, mission, scope, focus, context, constraints, acceptance criteria.
- Change, architectural, and attention budgets.
- Structured bearing and drift reports.
- Parking lot entries for valuable out-of-scope ideas.
- Explicit promotion state for ideas and capabilities.
- Derived progress from acceptance criteria.

Execution does not own:

- Persistence.
- ARK observations.
- Task assignment.
- Project scheduling.
- Framework or runtime orchestration.

## Models

The domain models live in `execution/domain.py`.

All public records are immutable dataclasses with stable ids. Enums are used for
statuses, report kinds, drift kinds, severities, decision states, and promotion
stages. Collections and field lengths are bounded.

Progress is derived from acceptance criteria. Completion percentages are not
stored.

## Services

Services live in `execution/services.py`.

They are intentionally thin:

- `MissionService`
- `BearingCheckService`
- `DriftDetectionService`
- `PromotionService`
- `ProgressService`
- `ParkingLotService`
- `DecisionLedgerService`

Business rules remain on the models, primarily `Mission` and
`PromotionState`.

## Workspace

The Execution Workspace lives in `execution/workspace.py`.

It persists Execution state in a repository-local `.execution/` directory:

```text
.execution/
  active_mission.yaml
  parking_lot.yaml
  decisions.yaml
  history/
  completed/
```

The workspace owns file layout, YAML serialization, loading, and saving. It does
not own mission rules. Derived operations delegate to the existing Execution
services and models.

Workspace lifecycle:

```python
from execution import load_workspace

workspace = load_workspace(".")
workspace.activate_mission(mission)
progress = workspace.get_progress()
bearing_report = workspace.run_bearing_check(proposal)
drift_report = workspace.run_drift_detection(proposal)
workspace.complete_mission()
```

`activate_mission()` writes one active mission. `complete_mission()` archives
that mission under `completed/`, records a minimal completion history entry,
and clears the active mission slot.

Parking lot entries and decision ledger entries are appended through the
workspace and persisted to YAML:

```python
workspace.add_parking_lot_entry(
    entry_id="parking:future-idea",
    summary="Useful idea outside the active mission.",
    reason_out_of_scope="Current mission has a narrower scope.",
)

workspace.add_decision(
    decision_id="decision:1",
    summary="Keep services thin.",
    status="accepted",
    reason="Business rules belong in models.",
    actor="builder",
)
```

The workspace is not a CLI and does not integrate with ARK.

## Example Mission

```python
from execution.examples import example_mission

mission = example_mission()
progress = mission.progress()
```

The example mission scopes in Execution models, services, and tests while
explicitly scoping out task-manager behavior.

## Example Bearing Check

```python
from execution.examples import example_bearing_check

report = example_bearing_check()
assert report.aligned
```

Bearing checks evaluate:

- Intent alignment.
- Scope compliance.
- Focus alignment.
- Constraint compliance.
- Acceptance impact.
- Change budget compliance.
- Architectural budget compliance.

The result is a `BearingReport`, not a boolean.

## Example Drift Report

```python
from execution.examples import example_drift_report

report = example_drift_report()
assert report.has_drift
```

Drift detection can report:

- Mission drift.
- Scope drift.
- Focus drift.
- Architectural drift.
- Budget drift.

The report describes findings and evidence. It does not decide remediation.

## Example Promotion Lifecycle

```python
from execution.examples import example_promotion_lifecycle

state = example_promotion_lifecycle()
assert state.stage.value == "capability"
```

Promotion stages are:

```text
Captured -> Research -> Sandbox -> Prototype -> Capability -> Core
```

Transitions are explicit and may move one stage forward or backward. Larger
jumps must be represented as separate decisions.

## Parking Lot

Out-of-mission ideas become `ParkingLotEntry` records. This preserves
maneuverability by capturing value without silently expanding mission scope.
