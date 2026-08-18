# Building Patterns

Purpose: define reusable building classes that future properties can
instantiate without changing Build Bible doctrine.

## Profile Scope

Residential assumptions are not universal across buildings.

- **GH** — compact first-stage complete home. Space is spent reluctantly; conventional hallways and walk-in storage are not defaults.
- **MH** — long-term primary home. Space is spent intentionally; hallways, dedicated rooms, generous transitions, and larger storage are allowed when they improve ordinary life.
- **CAMPUS** — workshop, greenhouse, barn, root cellar, equipment shelter, utility/storage/animal and similar building capability. Do not force these assumptions into GH/MH.
- **SHARED** — only explicitly shared requirements propagate across GH and MH.
- **UNKNOWN_SCOPE** — historical material is quarantined until reconciled.

Both GH and MH currently have **one human-occupied story**. Stair-dependent
architecture, second occupied floors, and required inter-floor transfer/lifts
are not current residential assumptions.

Contents:

- [Main House](main-house.md) — `MH`
- [Guest House](guest-house.md) — `GH`
- [Greenhouse](greenhouse.md) — `CAMPUS`
- [Workshop](workshop.md) — `CAMPUS`
- [Barn](barn.md) — `CAMPUS`
- [Root Cellar](root-cellar.md) — `CAMPUS`
- [Equipment Shelter](equipment-shelter.md) — `CAMPUS`

A pattern is a reusable capability/constraint profile, not a mandate to build
that building or to copy every feature into another profile.

Relationships:

- Habitat scope: [Habitat Assumption Scope](../../../contracts/habitat-assumption-scope-v1.md)
- Parent doctrine: [Platform, Not Product](../../../doctrine/platform-not-product.md)
- Related contract: [Physical Scope Contract](../../../contracts/physical-scope-contract.md)
- Related schema: [physical-scope.schema.json](../../../schemas/physical-scope.schema.json)
- EDRs: [Engineering Decision Record Standard](../../../lifecycle/decisions/engineering-decision-record-standard.md)
- Metrics and review: [Metrics Rubrics](../../../governance/reviews/metrics-rubrics.md),
  [Architectural Review Checklist](../../../governance/reviews/architectural-review-checklist.md)
- Anti-patterns: [Anti-Pattern Library](../../../governance/reviews/anti-pattern-library.md)
- Reliability: [Reliability](../../../lifecycle/reliability/README.md)
- Verification: [Acceptance And Verification Standard](../../../governance/reviews/acceptance-and-verification-standard.md)
- Dependent patterns: [Building Spine](../../../doctrine/spines/building-spine.md),
  [Universal Mechanical Pattern](../../spaces/universal-mechanical-pattern.md)
- Generated targets: floor plans, BIM models, utility diagrams, equipment
  schedules, inspection checklists

Lifecycle: these are reusable classes. A property-specific building record
instantiates one or more patterns and links to evidence, decisions, and service
history.
