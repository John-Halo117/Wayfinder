# Spatial Bundle Standard

A spatial bundle is the complete specification for a bounded space.

## Required Fields

- identity
- purpose
- parent scope
- boundary
- spatial address
- capabilities
- constraints
- interfaces
- serviceability
- expansion capacity
- maintenance obligations
- digital twin metadata
- generated artifact targets
- reality record links

## Identity

Each space has a stable ID, human name, parent scope, lifecycle state, and
verification state.

## Purpose

Purpose describes what the space supports without locking the space to a single
furnishing or current use.

## Capabilities

Capabilities may include power, lighting, water, drainage, ventilation,
storage, work, sleep, hygiene, food preparation, access, security, monitoring,
or future expansion.

## Constraints

Constraints include dimensions, clearances, structure, moisture, fire, noise,
privacy, accessibility, air quality, load, and utility limitations.

## Interfaces

Every service entering or leaving the space must have an explicit interface.

## Serviceability

Serviceable components must publish access panels, clearances, shutoffs,
cleanouts, filters, removable assemblies, and replacement paths.

## Expansion

The spatial bundle must state what can be added through reserved interfaces and
what would require reconstruction.

## Maintenance

Maintenance obligations link to procedures, schedules, and service records.

## Digital Twin Metadata

Each spatial bundle should support digital twin state: spatial address,
capabilities, constraints, remaining capacity, service history, observations,
and last verified reality.

## Relationships

- Parent doctrine: [Fractal Spines](../../doctrine/fractal-spines.md)
- Contracts: [Physical Scope Contract](../../contracts/physical-scope-contract.md),
  [Capability Contract](../../contracts/capability-contract.md),
  [Interface Contract](../../contracts/interface-contract.md)
- Schemas: [physical-scope.schema.json](../../schemas/physical-scope.schema.json),
  [digital-twin-state.schema.json](../../schemas/digital-twin-state.schema.json)
- Dependent patterns: [Universal Room Pattern](universal-room-pattern.md),
  [Room Spine](../../doctrine/spines/room-spine.md)
- Generated artifacts: room data sheets, service maps, maintenance checklists,
  digital twin exports
- Reality records: room observations instantiate this standard.

