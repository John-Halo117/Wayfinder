# Utility Standards

Purpose: define reusable utility standards that physical scopes consume through
explicit interfaces.

Contents:

- [Power](power.md)
- [Water](water.md)
- [Waste](waste.md)
- [Greywater](greywater.md)
- [Rainwater](rainwater.md)
- [HVAC](hvac.md)
- [Communications](communications.md)
- [Lighting](lighting.md)
- [Monitoring](monitoring.md)
- [Security](security.md)
- [Automation](automation.md)

Relationships:

- Parent doctrine: [Serviceability Invariant](../../../doctrine/serviceability-invariant.md)
- Related contracts: [Interface Contract](../../../contracts/interface-contract.md),
  [Capability Contract](../../../contracts/capability-contract.md),
  [Capacity Contract](../../../contracts/capacity-contract.md)
- Related schemas: [interface.schema.json](../../../schemas/interface.schema.json),
  [capability.schema.json](../../../schemas/capability.schema.json)
- EDRs: [Engineering Decision Record Standard](../../../lifecycle/decisions/engineering-decision-record-standard.md)
- Metrics and review: [Metrics Rubrics](../../../governance/reviews/metrics-rubrics.md),
  [Architectural Review Checklist](../../../governance/reviews/architectural-review-checklist.md)
- Anti-patterns: [Anti-Pattern Library](../../../governance/reviews/anti-pattern-library.md)
- Reliability: [Reliability](../../../lifecycle/reliability/README.md)
- Verification: [Acceptance And Verification Standard](../../../governance/reviews/acceptance-and-verification-standard.md)
- Generated targets: one-line diagrams, utility maps, control schedules,
  sensor schedules, isolation guides

Lifecycle: utility standards are reusable classes. Property, building, room,
cabinet, and appliance records instantiate them through explicit interfaces.
