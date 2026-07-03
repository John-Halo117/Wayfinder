# Acquisition Contract

## Purpose

Defines the boundary for bringing an external, local, manual, or service-produced source under Wayfinder attention as an ingestion candidate.

## Inputs

- Reality source reference
- Asset candidate or observation source
- Context reference
- Actor or system source
- Objective or reason for acquisition
- Trust boundary signal
- Initial evidence or access reference

## Outputs

- Acquisition candidate
- Source reference
- Initial observation candidate
- Acquisition context
- Trust boundary note
- Failure or uncertainty condition

## Invariants

- Acquisition does not decide identity, format meaning, or truth.
- Source material is not overwritten.
- Acquisition remains evidence-ready and append-only once preserved by ARK.
- Media-specific handling is limited to the adapter boundary.

## Producer

Universal Asset Ingestion

Exactly one program produces this stage contract across the ingestion pipeline.

## Consumers

Format Detection, Ingestion Provenance, ARK, Storage Service, media adapters.

## Does Not Own

- Identity generation
- Format classification
- Canonical representation selection
- Persistence implementation
- Reality preservation
- Interpretation or knowledge extraction

## Dependencies

- Asset Model
- Observation Contract
- Evidence Contract
- Provenance Contract
- Context Contract

## Failure Conditions

- Missing source
- Unavailable source
- Untrusted source
- Incomplete context
- Unsupported access boundary
- Ambiguous acquisition target

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Media adapter code.
- Engine refactoring.
- Durable promotion by itself.
