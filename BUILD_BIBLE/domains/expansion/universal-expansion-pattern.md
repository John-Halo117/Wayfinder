# Universal Expansion Pattern

Expansion is normal operation of a long-lived physical platform, but
future-readiness means preserving economical **interfaces, routes, clearances,
and options**—not pre-installing speculative future-maximum equipment.

## Rule

New capabilities consume adequate existing/reserved interfaces before requiring
reconstruction.

`future interface != installed future capacity`

## Expansion Sequence

1. Confirm the current requirement and profile/scope.
2. Use an adequate existing published interface.
3. Use reserved capacity in an existing spine/path.
4. Use an existing access panel, chase, raceway, conduit, service zone, utility
   wall, structural allowance, or reserved clearance.
5. Use a planned expansion zone.
6. Adapt/compose using existing standards and mature interoperable components.
7. Create a custom residual only after standards-first resolution documents why
   existing interfaces fail.
8. Reconstruct only after cheaper preserved options are exhausted or rejected.

## Required Expansion Metadata

Each scope should state:

- addable/reachable capabilities when known
- reserved interfaces/routes/clearances
- reserved capacity where intentionally provided
- blocked additions
- reconstruction triggers
- safety/accessibility/service constraints
- required approvals or inspections
- profile/scope (`GH`, `MH`, `CAMPUS`, etc.) where applicable
- whether the reserve is physical capacity, pathway capacity, clearance, or
  merely an option to adapt later

A valid expansion state may explicitly say `no reserve` when preserving capacity
would not earn its burden.

## Examples

Examples are illustrative, not mandatory infrastructure:

- additional generation/storage may use a reserved electrical/conduit/service
  interface if that reserve was justified;
- future communications/control devices may use an accessible standards-based
  power/data path without installing those devices now;
- future physical payloads may use qualified structural blocking/rails/mounts
  where their likely value justified the interface;
- an unknown future technology may benefit from generic power/data/structure/
  access pathways, but Polaris should not invent or populate a special interface
  merely because the technology is imaginable.

## Habitat Boundary

For current GH/MH profiles:

- both remain one human-occupied story;
- expansion must not assume an upper occupied floor, stair, or inter-floor lift;
- GH should not absorb eventual MH/Campus functions merely for completeness;
- MH should not inherit GH compression mechanisms unless independently useful;
- Campus placement should be evaluated for bulky/noisy/dirty/seasonal or
  material-handling capability before interior residential allocation.

## Failure Isolation

New capabilities must declare material failure behavior and isolation so they do
not silently compromise existing critical systems.

## Maintenance

Expansion work must update source records, generated artifacts, labels,
maintenance schedules, and digital twin state. Added interfaces must retain
inspection/removal/service paths appropriate to their consequence.

## Relationships

- Habitat scope: [Habitat Assumption Scope](../../contracts/habitat-assumption-scope-v1.md)
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
