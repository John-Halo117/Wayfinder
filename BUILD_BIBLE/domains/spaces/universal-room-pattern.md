# Universal Room Pattern

A room is a bounded spatial implementation of activities/capabilities. A room
is not automatically required merely because a conventional floor plan usually
contains one, and a room need not be dedicated to a single furnishing or use.

Every instantiated room inherits from the spatial bundle and publishes the
capabilities and constraints that actually apply.

## Profile Scope

Room patterns used in GH/MH must resolve through the [Habitat Assumption Scope](../../contracts/habitat-assumption-scope-v1.md).

- GH may share/interleave intermittent capabilities more aggressively when conversion is low-friction.
- MH may dedicate rooms where privacy, acoustics, fixed infrastructure, simultaneous use, or reduced recurring friction earns the area.
- A GH compression tactic is not a universal room rule.
- A conventional MH room name is not evidence that GH needs an equivalent room.

## Capabilities

Each room should define only applicable capabilities or an explicit absence when
that absence matters:

- primary activity/capability
- supported secondary uses, if any
- power capability where present/required
- lighting capability where present/required
- communications capability where present/required
- ventilation or air-quality capability where present/required
- storage capability when present
- safety and egress capability when relevant
- privacy/acoustic requirements when relevant
- optional monitoring/sensing only when it earns its lifecycle/privacy burden
- future expansion capability only when a real low-cost interface/path is justified

`more interfaces/sensors/endpoints` is not automatically `more future-ready`.
A documented `none` is valid.

## Infrastructure

Each room should document only the infrastructure actually present or required:

- local service/distribution path, if any
- circuits
- lighting zones
- switches or controls
- data and low-voltage routes
- HVAC supply, return, exhaust, or explicit absence
- water and drainage interfaces when present
- sensors and access-control interfaces when present
- service panels, utility walls, accessible service cavities, or removable assemblies

Do not install electronics, sensors, controls, or endpoints merely because a
pathway exists.

## Spatial Use

A room may contain fixed, mobile, deployable, recessed, or boundary-integrated
capabilities. Before adding permanent dedicated area, test whether the activity
requires simultaneous use, privacy/acoustics, fixed infrastructure,
accessibility, high frequency, or whether conversion burden makes sharing worse.

Deliberate negative/restorative space is valid output and does not require a
secondary function.

## Documentation

Each room should have:

- room data sheet
- profile/scope
- interface list
- applicable capacity list
- maintenance obligations
- generated artifact manifest targets
- last verified reality

## Service Access

Critical room services should be reachable through access panels, utility
walls, accessible service cavities/ceilings where appropriate, exposed service
runs, cabinets, or adjacent service spaces. Routine service should not require
destructive opening when an economical access path can be designed in.

## Reserve Capacity

Reserve capacity is intentional option value, not a requirement to populate the
space. Rooms may preserve conduit, blocking, clearances, panel capacity, or
other interfaces without installing speculative devices/equipment.

## Digital Twin

The room digital twin should track identity, spatial address, current
capabilities, constraints, interfaces, remaining capacity, maintenance, service
history, observations, verification state, and profile/scope. It should not
infer that an unused interface must be populated.

## Maintenance

Room maintenance includes inspection of applicable finishes, doors, windows,
fixtures, lighting, receptacles, sensors, vents, filters, drains, access panels,
and stored service documentation.

## Relationships

- Habitat scope: [Habitat Assumption Scope](../../contracts/habitat-assumption-scope-v1.md)
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
