# Building Spine Pattern

The building spine is the primary service backbone inside a building. It is a
routing/service abstraction, not a requirement to centralize every control or
to populate every possible endpoint.

## Responsibilities

- Route applicable power, water, drainage, HVAC, data, monitoring, and controls
  through accessible service zones.
- Connect the property spine to local room/zone interfaces where those
  interfaces are actually needed.
- Preserve replacement paths for major equipment and service expansion.
- Keep critical local isolation/control possible where a single central failure
  would create unnecessary loss of capability.

For current GH/MH profiles, the building spine must fit a **one human-occupied
story** design. Vertical service routing inside walls/ceilings/chases is not a
second-story assumption.

## Required Capabilities

- main service entry or transfer point
- electrical distribution access when electrical service is present
- water isolation access when water is present
- drainage cleanouts when drainage is present
- ventilation or exhaust pathway when air systems are present
- data distribution point when networked services are present
- service clearances
- labeled/identifiable access points

## Optional Capabilities

- battery/storage interface
- solar inverter interface
- thermal storage
- heat recovery
- whole-building monitoring
- future chase/raceway/conduit capacity
- local zone control/isolation

Optional means optional. A pathway or blank interface does not imply installing
a sensor, controller, endpoint, battery, or other payload now.

## Interfaces

The building spine consumes property utilities and publishes local interfaces.
Reserved future interfaces should be standards-based or use mature interoperable
components where adequate.

## Expansion Rules

Reserve inexpensive, durable route/access capacity where the likely future
benefit justifies it. Do not reserve every imaginable endpoint and do not install
future-maximum equipment merely because a route exists.

For additions, prefer in order:

1. an adequate existing interface;
2. spare capacity on the existing path/backbone;
3. a reserved accessible path/clearance;
4. a standards-based adapter/extension;
5. a custom residual only after standards-first resolution.

## Failure Isolation

Failures should isolate by branch, room, zone, or equipment class rather than
forcing whole-building shutdown unless safety or the physical topology requires
it.

## Maintenance

Inspection should occur through mechanical rooms, utility walls, service
cavities/chases, access panels, exterior/shared service zones, or documented
removable assemblies. Dedicated service corridors are allowed where their area
and access benefit earn them; they are not a universal residential requirement.

## Relationships

- Habitat scope: [Habitat Assumption Scope](../../contracts/habitat-assumption-scope-v1.md)
- Parent doctrine: [Fractal Spines](../fractal-spines.md)
- Contract: [Spine Contract](../../contracts/spine-contract.md)
- Schema: [spine.schema.json](../../schemas/spine.schema.json)
- Dependent patterns: [Universal Mechanical Pattern](../../domains/spaces/universal-mechanical-pattern.md),
  [Building Patterns](../../domains/buildings/patterns/README.md)
- Generated artifacts: service distribution diagrams, one-line diagrams, duct
  maps, panel schedules, maintenance checklists
- Reality records: building-specific inspection and construction evidence
  instantiate this pattern.
