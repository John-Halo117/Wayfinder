# Building Spine Pattern

The building spine is the primary service backbone inside a building.

## Responsibilities

- Route power, water, drainage, HVAC, data, monitoring, and controls through
  accessible service zones.
- Connect the property spine to room spines.
- Preserve replacement paths for major equipment and vertical or horizontal
  service expansion.

## Required Capabilities

- main service entry or transfer point
- electrical distribution access
- water isolation access when water is present
- drainage cleanouts when drainage is present
- ventilation or exhaust pathway when air systems are present
- data distribution point
- service clearances
- labeled access panels

## Optional Capabilities

- battery room interface
- solar inverter interface
- thermal storage
- heat recovery
- whole-building monitoring
- future riser or chase

## Interfaces

The building spine consumes property utilities and publishes room-level
interfaces. It should also expose reserved interfaces for future technologies.

## Expansion Rules

The building spine must reserve route capacity for future circuits, pipes,
ducts, cables, sensors, and equipment replacement.

## Failure Isolation

Failures should isolate by branch, room, zone, or equipment class rather than
forcing whole-building shutdown unless required for safety.

## Maintenance

Inspection should occur through mechanical rooms, service corridors, chases,
access panels, exposed utility walls, or documented removable assemblies.

## Relationships

- Parent doctrine: [Fractal Spines](../fractal-spines.md)
- Contract: [Spine Contract](../../contracts/spine-contract.md)
- Schema: [spine.schema.json](../../schemas/spine.schema.json)
- Dependent patterns: [Universal Mechanical Pattern](../../domains/spaces/universal-mechanical-pattern.md),
  [Building Patterns](../../domains/buildings/patterns/README.md)
- Generated artifacts: riser diagrams, one-line diagrams, duct maps, panel
  schedules, maintenance checklists
- Reality records: building-specific inspection and construction evidence
  instantiate this pattern.

