# Workshop Building Pattern

The workshop is a fabrication and repair platform.

## Required Capabilities

- work zones
- tool power
- lighting
- material handling
- ventilation or dust control where required
- fire and safety constraints
- storage
- serviceable utility routes
- equipment replacement paths

## Optional Capabilities

- compressed air
- dust collection
- welding zone
- finishing zone
- machine room
- vehicle bay
- clean electronics bench
- digital fabrication zone

## Constraints

Workshop design must separate incompatible hazards such as dust, ignition,
fumes, moisture, sensitive electronics, and pedestrian circulation.

## Serviceability

Machine hookups, dust ports, air drops, task lighting, receptacles, and network
interfaces should be modular and reconfigurable.

## Expansion

Reserve ceiling, wall, floor, and utility interfaces for future machines and
material handling.

## Relationships

- Parent doctrine: [Platform, Not Product](../../../doctrine/platform-not-product.md)
- Contracts: [Physical Scope Contract](../../../contracts/physical-scope-contract.md),
  [Capability Contract](../../../contracts/capability-contract.md)
- Schemas: [physical-scope.schema.json](../../../schemas/physical-scope.schema.json),
  [capability.schema.json](../../../schemas/capability.schema.json)
- Dependent patterns: [Workshops Domain](../../workshops/README.md),
  [Universal Mechanical Pattern](../../spaces/universal-mechanical-pattern.md)
- Generated artifacts: shop layout plans, tool interface schedules, safety
  inspection checklists
- Reality records: equipment records and shop inspections instantiate this
  pattern.

