# Universal Room Pattern

Every room inherits from the spatial bundle and publishes its local physical
capabilities.

## Capabilities

Each room should define:

- primary purpose
- supported secondary uses
- power capability
- lighting capability
- communications capability
- ventilation or air quality capability
- monitoring capability
- storage capability when present
- safety and egress capability when relevant
- future expansion capability

## Infrastructure

Each room should document:

- room spine
- circuits
- lighting zones
- switches or controls
- data and low-voltage routes
- HVAC supply, return, exhaust, or explicit absence
- water and drainage interfaces when present
- sensors and access-control interfaces when present
- service panels, utility walls, ceiling access, or removable assemblies

## Documentation

Each room should have:

- room data sheet
- interface list
- capacity list
- maintenance obligations
- generated artifact manifest targets
- last verified reality

## Service Access

Critical room services should be reachable through access panels, utility
walls, accessible ceilings, exposed service runs, cabinets, or adjacent service
spaces.

## Reserve Capacity

Rooms should reserve capacity for future receptacles, sensors, data, lighting,
controls, mounting, and furniture or equipment changes.

## Digital Twin

The room digital twin should track identity, spatial address, current
capabilities, constraints, interfaces, remaining capacity, maintenance, service
history, observations, and verification state.

## Maintenance

Room maintenance includes inspection of finishes, doors, windows, fixtures,
lighting, receptacles, sensors, vents, filters, drains, access panels, and
stored service documentation.

## Relationships

- Parent doctrine: [Platform, Not Product](../../doctrine/platform-not-product.md)
- Contracts: [Physical Scope Contract](../../contracts/physical-scope-contract.md),
  [Maintenance Contract](../../contracts/maintenance-contract.md)
- Schemas: [physical-scope.schema.json](../../schemas/physical-scope.schema.json),
  [digital-twin-state.schema.json](../../schemas/digital-twin-state.schema.json)
- Dependent patterns: [Spatial Bundle Standard](spatial-bundle-standard.md),
  [Room Spine](../../doctrine/spines/room-spine.md)
- Generated artifacts: room data sheets, wiring maps, lighting plans,
  maintenance schedules
- Reality records: room-specific observations instantiate this pattern.

