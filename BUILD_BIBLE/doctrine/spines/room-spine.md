# Room Spine Pattern

The room spine is the local distribution and service backbone for a space.

## Responsibilities

- Publish room capabilities and constraints.
- Route local power, lighting, data, controls, air, water, drainage, and sensors
  where applicable.
- Provide clear access for maintenance and future additions.

## Required Capabilities

- local power access or explicit no-power state
- lighting interface or explicit no-lighting state
- digital twin address
- service access description
- documentation location
- reserve capacity statement

## Optional Capabilities

- water
- drainage
- ventilation
- floor drain
- occupancy sensing
- environmental sensing
- access control
- modular wall or ceiling service zone

## Interfaces

The room spine consumes building-spine services and publishes cabinet,
fixture, appliance, furniture, and equipment interfaces.

## Expansion Rules

Room additions should consume blank plates, accessible raceways, spare conduit,
utility walls, service ceilings, or cabinet spines before destructive work.

## Failure Isolation

Room-level failures should be isolatable by circuit, valve, device, fixture, or
zone where the capability is critical.

## Maintenance

Maintenance access must be visible in the room specification, including panels,
clearances, filters, cleanouts, and removable assemblies.

## Relationships

- Parent doctrine: [Fractal Spines](../fractal-spines.md)
- Contract: [Spine Contract](../../contracts/spine-contract.md)
- Schema: [spine.schema.json](../../schemas/spine.schema.json)
- Dependent patterns: [Universal Room Pattern](../../domains/spaces/universal-room-pattern.md),
  [Universal Wet Area Pattern](../../domains/spaces/universal-wet-area-pattern.md)
- Generated artifacts: room data sheets, service maps, inspection checklists
- Reality records: room observations and as-built evidence instantiate this
  pattern.

