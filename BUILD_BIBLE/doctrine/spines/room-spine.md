# Room Spine Pattern

The room spine is the local distribution/service path for a space **when the
space actually needs one**. It is not a requirement to give every room a dense
bundle of power, data, sensors, controls, or future endpoints.

## Responsibilities

- Publish applicable room/zone capabilities and constraints.
- Route local power, lighting, data, controls, air, water, drainage, or sensors
  where required.
- Provide clear access for maintenance and justified future additions.
- State explicit absence where that absence matters to design or safety.

## Profile Scope

GH/MH room-spine decisions resolve through the
[Habitat Assumption Scope](../../contracts/habitat-assumption-scope-v1.md).

A GH preference for compact service routing does not force MH into the same
endpoint density or room geometry. Conversely, an MH convenience endpoint does
not become a GH requirement.

## Required Documentation

For an instantiated room/zone, document:

- local power access or explicit no-power state, when material
- lighting interface or explicit no-lighting state, when material
- digital-twin/spatial identity
- service access description
- documentation location
- reserve/expansion statement, including `none` where appropriate

## Optional Capabilities

- water
- drainage
- ventilation
- floor drain
- occupancy sensing
- environmental sensing
- access control
- modular wall or ceiling service zone
- additional power/data endpoints

Optional capabilities are installed only when current or reasonably reachable
use justifies their cost, privacy burden, failure surface, and maintenance.

## Interfaces

The room spine consumes building-spine services and publishes applicable
cabinet, fixture, appliance, furniture, equipment, or deployable-capability
interfaces.

Prefer standards/mature interoperable interfaces before custom physical
interfaces. A reserved pathway may terminate in a blank/accessible state rather
than a populated endpoint.

## Expansion Rules

Room additions should consume existing interfaces, blank plates, accessible
raceways, spare conduit, utility walls, service cavities/ceilings where
appropriate, or cabinet spines before destructive work.

Do not add infrastructure merely because a hypothetical future device could use
it. Preserve cheap route/access optionality where justified; populate later.

## Failure Isolation

Room-level failures should be isolatable by circuit, valve, device, fixture, or
zone where the capability is critical and where the added isolation is
lifecycle-positive.

## Maintenance

Maintenance access must be visible in the room specification, including
applicable panels, clearances, filters, cleanouts, disconnects, and removable
assemblies.

## Relationships

- Habitat scope: [Habitat Assumption Scope](../../contracts/habitat-assumption-scope-v1.md)
- Parent doctrine: [Fractal Spines](../fractal-spines.md)
- Contract: [Spine Contract](../../contracts/spine-contract.md)
- Schema: [spine.schema.json](../../schemas/spine.schema.json)
- Dependent patterns: [Universal Room Pattern](../../domains/spaces/universal-room-pattern.md),
  [Universal Wet Area Pattern](../../domains/spaces/universal-wet-area-pattern.md)
- Generated artifacts: room data sheets, service maps, inspection checklists
- Reality records: room observations and as-built evidence instantiate this
  pattern.
