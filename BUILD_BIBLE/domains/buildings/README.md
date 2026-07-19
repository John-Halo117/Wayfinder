# Buildings Domain

Owns buildings, structural systems, envelopes, roofs, foundations, major
assemblies, building spines, and building-level constraints.

Canonical here:

- building identities
- building boundaries
- structural and envelope intent
- mechanical and utility routing zones
- building serviceability strategy

## Purpose

Define reusable building classes and building-scale physical infrastructure.

## Contents

- [Building Patterns](patterns/README.md)
- main house, guest house, greenhouse, workshop, barn, root cellar, and
  equipment shelter classes

## Relationships

Depends on [Building Spine](../../doctrine/spines/building-spine.md),
[Universal Room Pattern](../spaces/universal-room-pattern.md), and
[Universal Mechanical Pattern](../spaces/universal-mechanical-pattern.md).

## Lifecycle

Building patterns are reusable classes. Specific buildings become physical
scope records with evidence, decisions, service records, and generated outputs.

## Generation Targets

Floor plans, BIM, envelope diagrams, utility risers, room data sheets,
equipment schedules, and maintenance checklists.
