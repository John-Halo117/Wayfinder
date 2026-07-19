# Root Cellar Pattern

The root cellar is a passive storage environment for food, seed, and other
temperature-sensitive physical goods.

## Required Capabilities

- stable thermal behavior
- moisture management
- ventilation
- pest resistance
- cleanable storage surfaces
- drainage or explicit dry-only design
- monitoring
- safe access

## Constraints

The root cellar must treat water intrusion, mold, pests, radon, oxygen quality,
and structural load as first-class constraints.

## Serviceability

Ventilation paths, drains, shelves, sensors, doors, and seals must be
inspectable and repairable.

## Expansion

Reserve monitoring, shelving, ventilation, and drainage interfaces for future
storage modes.

## Relationships

- Parent doctrine: [Serviceability Invariant](../../../doctrine/serviceability-invariant.md)
- Contracts: [Physical Scope Contract](../../../contracts/physical-scope-contract.md),
  [Capability Contract](../../../contracts/capability-contract.md)
- Schemas: [physical-scope.schema.json](../../../schemas/physical-scope.schema.json),
  [digital-twin-state.schema.json](../../../schemas/digital-twin-state.schema.json)
- Dependent patterns: [Storage Domain](../../storage/README.md),
  [Monitoring Standard](../../utilities/standards/monitoring.md)
- Generated artifacts: storage maps, environmental monitoring plans,
  maintenance schedules
- Reality records: environmental observations instantiate this pattern.

