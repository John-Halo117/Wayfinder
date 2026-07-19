# Cabinet Spine Pattern

The cabinet spine is the local backbone for built-ins, storage walls, benches,
and service-integrated furniture.

## Responsibilities

- Organize local power, lighting, low-voltage, storage, ventilation, drainage,
  or specialty service interfaces inside a cabinet-class assembly.
- Preserve replacement and access without destroying surrounding finishes.
- Publish mounting, load, and clearance constraints.

## Required Capabilities

- stable cabinet identity
- attachment method
- access method
- service void or explicit no-service-void state
- load limit
- replacement path

## Optional Capabilities

- task lighting
- receptacles
- sensors
- ventilation
- water
- drainage
- appliance bay
- removable back panel

## Interfaces

Cabinet spines consume room-spine services and publish fixture, appliance,
storage, tool, or device interfaces.

## Expansion Rules

Cabinets that may later host appliances, sensors, charging, or automation must
preserve spare power, data path, ventilation, and removable service surfaces.

## Failure Isolation

Cabinet-integrated services should be disconnectable without removing the
entire cabinet when practical.

## Maintenance

Access panels, removable drawers, toe-kick panels, and labeled junctions are
preferred over hidden cavities.

## Relationships

- Parent doctrine: [Fractal Spines](../fractal-spines.md)
- Contract: [Spine Contract](../../contracts/spine-contract.md)
- Schema: [spine.schema.json](../../schemas/spine.schema.json)
- Dependent patterns: [Furniture Domain](../../domains/furniture/README.md),
  [Storage Domain](../../domains/storage/README.md)
- Generated artifacts: cabinet shop drawings, wiring maps, service checklists
- Reality records: cabinet as-built observations instantiate this pattern.

