# Observations

Observations record bounded claims about physical reality.

Each observation should include:

- observed scope ID
- observer
- date
- method
- measurement or description
- evidence link
- uncertainty
- affected canonical records

## Purpose

Turn physical evidence into bounded, repeatable claims that can update scope
records and digital twin state.

## Contents

- [Observation Points Standard](observation-points-standard.md)
- individual observation records
- measurement logs
- linked evidence

## Relationships

Depends on [Verification](../../governance/verification.md) and
[observation.schema.json](../../schemas/observation.schema.json).

## Lifecycle

Observations are append-only evidence records. They may supersede earlier
observations but should not erase them.

## Generation Targets

Inspection routes, sensor maps, condition reports, and digital twin updates.
