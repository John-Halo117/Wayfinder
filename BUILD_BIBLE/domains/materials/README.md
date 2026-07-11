# Materials Domain

Owns material selections, finish systems, assemblies, durability rules,
compatibility constraints, approved products, rejected products, and spare
stock requirements.

Canonical here:

- material specifications
- approved uses
- prohibited uses
- maintenance compatibility
- replacement compatibility
- stock and sourcing constraints

## Purpose

Define material selection and maintenance standards for longevity,
repairability, modularity, environmental resistance, compatibility, inspection,
and replacement.

## Contents

- [Material Standards](material-standards.md)
- material specifications
- approved uses
- prohibited uses
- maintenance compatibility
- replacement compatibility

## Relationships

Depends on [Serviceability Invariant](../../doctrine/serviceability-invariant.md)
and [Maintenance Contract](../../contracts/maintenance-contract.md).

## Lifecycle

Material standards are reusable. Approved product records and actual installed
materials require evidence and service history.

## Generation Targets

Material schedules, finish schedules, bills of materials, replacement lists,
and maintenance calendars.
