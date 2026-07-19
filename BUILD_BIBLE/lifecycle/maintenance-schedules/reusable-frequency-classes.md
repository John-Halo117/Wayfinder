# Reusable Frequency Classes

Frequency classes provide consistent maintenance scheduling language.

## Classes

- `event`: after storm, freeze, outage, alarm, flood, fire, impact, or service
  anomaly
- `monthly`: high-risk or high-value recurring inspection
- `quarterly`: seasonal operational condition check
- `seasonal`: weather, drainage, agriculture, roads, and exterior systems
- `annual`: stable systems with visible deterioration or service obligations
- `runtime`: equipment maintained by hours, cycles, starts, or throughput
- `manufacturer`: interval controlled by documented manufacturer requirement
- `condition`: inspection or sensor result triggers action

## Rule

Schedules must name a class, trigger, maintained scope, procedure, and service
record location.

## Relationships

- Parent doctrine: [Verification](../../governance/verification.md)
- Contract: [Maintenance Contract](../../contracts/maintenance-contract.md)
- Schema: [maintenance-procedure.schema.json](../../schemas/maintenance-procedure.schema.json)
- Dependent patterns: [Reusable Maintenance Procedures](../../domains/maintenance/reusable-maintenance-procedures.md)
- Generated artifacts: maintenance calendars, inspection routes, service
  reminders
- Reality records: service records instantiate scheduled work.

