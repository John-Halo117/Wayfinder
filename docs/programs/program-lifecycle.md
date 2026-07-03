# Program Lifecycle

Date: 2026-06-27

Every implementation program follows the same lifecycle.

```text
Proposed
  -> Planned
  -> Active
  -> Implementing
  -> Verified
  -> Promoted
  -> Operational
  -> Maintenance
```

## Lifecycle States

| State | Meaning | Entry Evidence | Exit Evidence |
| --- | --- | --- | --- |
| Proposed | Program is named as likely necessary. | Dependency or roadmap evidence exists. | Purpose, owner, dependencies, and scope are documented. |
| Planned | Program has roadmap, milestones, and backlog but no active execution. | Program doc or registry entry exists. | Current milestone is selected and accepted. |
| Active | Program is being advanced through planning or implementation milestones. | Dashboard marks a current milestone. | A milestone enters implementation or verification. |
| Implementing | Runtime, docs, or operational work is underway. | Contract-first plan and ARK checks exist where code is involved. | Tests/checks and governance updates are complete. |
| Verified | Milestone evidence passes required verification. | Verification report or command evidence exists. | Promotion decision is recorded or milestone is closed as planning-only. |
| Promoted | Output becomes durable in its canonical owner. | Promotion registry entry exists when promotion occurs. | Consumers are updated or operational rollout begins. |
| Operational | Program output is in regular use. | Health, rollback, recovery, or operating docs exist. | Maintenance cadence is defined. |
| Maintenance | Program is stable and monitored for drift. | Dashboard shows no active blocker. | New evidence or debt reactivates planning. |

## Synchronization Rules

When a milestone completes, update:

- `docs/implementation-backlog.md`
- `docs/migration-dashboard.md`
- `docs/promotion-registry.md` when promotion occurs
- `docs/programs/portfolio-dashboard.md`
- `docs/programs/release-plan.md`
- `docs/programs/program-registry.md`
- `docs/constitutional-scorecard.md` if governance, maturity, risk, proof, or release posture changed

## Completion Rule

A milestone is not complete until the registry, dashboard, release plan, and relevant backlog all agree on current status and next work.
