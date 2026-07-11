# Universal Expansion Pattern

Expansion is the normal operation of a long-lived physical platform.

## Rule

New capabilities consume reserved interfaces before requiring reconstruction.

## Expansion Sequence

1. Use an existing published interface.
2. Use reserved capacity in an existing spine.
3. Use an existing access panel, chase, raceway, conduit, service corridor, or
   utility wall.
4. Use a planned expansion zone.
5. Create a new interface with a decision record.
6. Reconstruct only after cheaper preserved options are exhausted or rejected.

## Required Expansion Metadata

Each scope should state:

- addable capabilities
- reserved interfaces
- reserved capacity
- blocked additions
- reconstruction triggers
- safety constraints
- required approvals or inspections

## Examples

- additional solar connects through reserved roof, conduit, inverter, panel, and
  battery interfaces
- battery bank uses reserved floor area, ventilation, fire separation, conduit,
  and monitoring
- LiDAR uses reserved power, data, mounting, sightline, and weather exposure
  constraints
- drone pad uses reserved exterior surface, charging, lighting, weather, access,
  and security interfaces
- weather station uses reserved mast or roof mount, power, data, calibration,
  and service access
- unknown technology uses published power, data, structure, access, and
  monitoring capacity without assuming its final form

## Failure Isolation

New capabilities must declare failure behavior and isolation so they do not
silently compromise existing critical systems.

## Maintenance

Expansion work must update source records, generated artifacts, labels,
maintenance schedules, and digital twin state.

## Relationships

- Parent doctrine: [Optionality](../../doctrine/optionality.md)
- Contracts: [Interface Contract](../../contracts/interface-contract.md),
  [Capacity Contract](../../contracts/capacity-contract.md),
  [Change Control](../../governance/change-control.md)
- Schemas: [interface.schema.json](../../schemas/interface.schema.json),
  [decision-record.schema.json](../../schemas/decision-record.schema.json)
- EDRs: [Engineering Decision Record Standard](../../lifecycle/decisions/engineering-decision-record-standard.md)
- Metrics and review: [Metrics Rubrics](../../governance/reviews/metrics-rubrics.md),
  [Architectural Review Checklist](../../governance/reviews/architectural-review-checklist.md)
- Anti-patterns: [Anti-Pattern Library](../../governance/reviews/anti-pattern-library.md)
- Reliability: [Reliability](../../lifecycle/reliability/README.md)
- Verification: [Acceptance And Verification Standard](../../governance/reviews/acceptance-and-verification-standard.md)
- Dependent patterns: [Property Spine](../../doctrine/spines/property-spine.md),
  [Building Spine](../../doctrine/spines/building-spine.md),
  [Room Spine](../../doctrine/spines/room-spine.md)
- Generated artifacts: expansion reserve maps, capacity reports, construction
  phase plans, regenerated diagrams
- Reality records: changes, inspections, and observations instantiate this
  pattern.
