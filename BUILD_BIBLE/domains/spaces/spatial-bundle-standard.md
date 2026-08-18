# Spatial Bundle Standard

A spatial bundle is the complete specification for a bounded space.

## Required Fields

- identity
- purpose
- parent scope
- habitat/building profile when applicable
- boundary
- spatial address
- capabilities
- constraints
- interfaces
- serviceability
- expansion/option capacity
- maintenance obligations
- digital twin metadata
- generated artifact targets
- reality record links

## Identity and Scope

Each space has a stable ID, human name, parent scope, lifecycle state, and
verification state.

For Sanctuary residential work, the space must also resolve to `GH`, `MH`,
`CAMPUS`, `SHARED`, or another explicit applicable scope. Historical
`UNKNOWN_SCOPE` assumptions do not automatically apply.

## Purpose

Purpose describes what the space supports without locking the space to a single
furnishing, room noun, or current use.

A conventional room name is not itself a requirement. An activity/capability
may terminate at a slot, pocket, niche, passage, nook, alcove, zone, or room if
that smaller primitive satisfies the actual need.

## Capabilities

Capabilities may include power, lighting, water, drainage, ventilation,
storage, work, sleep, hygiene, food preparation, access, security, monitoring,
or future expansion, but only applicable capabilities are instantiated.

A space may support multiple state-compatible functions when active/parked/
service states do not conflict. Co-occupancy must not counterfeit simultaneous
capacity.

## Spatial Resource Accounting

Where material, distinguish:

- dedicated floor area
- circulation-only area
- wall surface
- wall/cavity depth
- overhead/interstitial volume
- under-surface volume
- reach-accessible volume
- clearance/swing/service envelopes
- deliberately unallocated/negative space
- temporal availability

Do not double-count the same cavity, clearance, or volume for incompatible
functions. Structure, fire, moisture, insulation, acoustics, accessibility,
egress, utilities, and service obligations reserve capacity before optional
secondary uses.

## Constraints

Constraints include dimensions, clearances, structure, moisture, fire, noise,
privacy, accessibility, air quality, load, utility limitations, profile scope,
and human conversion/setup burden where relevant.

## Interfaces

Every service entering or leaving the space must have an explicit interface.
Existing standards and mature interoperable interfaces are preferred before
custom physical interfaces.

An interface/pathway may exist without an installed endpoint or payload.
Future-ready does not mean fully populated.

## Serviceability

Serviceable components must publish applicable access panels, clearances,
shutoffs, cleanouts, filters, removable assemblies, and replacement paths.
Concealment never cancels service requirements.

## Expansion

The spatial bundle must state what can be added through reserved interfaces and
what would require reconstruction. Unused interfaces, clearances, pathways,
structural capacity, and negative space may represent option value without
being treated as unfinished work.

## Maintenance

Maintenance obligations link to procedures, schedules, and service records.

## Digital Twin Metadata

Each spatial bundle should support digital twin state: spatial address,
profile/scope, capabilities, constraints, remaining capacity, service history,
observations, and last verified reality.

## Relationships

- Habitat scope: [Habitat Assumption Scope](../../contracts/habitat-assumption-scope-v1.md)
- Parent doctrine: [Fractal Spines](../../doctrine/fractal-spines.md)
- Contracts: [Physical Scope Contract](../../contracts/physical-scope-contract.md),
  [Capability Contract](../../contracts/capability-contract.md),
  [Interface Contract](../../contracts/interface-contract.md)
- Schemas: [physical-scope.schema.json](../../schemas/physical-scope.schema.json),
  [digital-twin-state.schema.json](../../schemas/digital-twin-state.schema.json)
- Dependent patterns: [Universal Room Pattern](universal-room-pattern.md),
  [Room Spine](../../doctrine/spines/room-spine.md)
- Generated artifacts: room/space data sheets, service maps, spatial-resource
  ledgers, maintenance checklists, digital twin exports
- Reality records: room/space observations instantiate this standard.
