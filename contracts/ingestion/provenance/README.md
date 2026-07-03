# Ingestion Provenance Contract

## Purpose

Defines the boundary for recording source, custody, derivation, adapter handoff, and transformation traces across the ingestion pipeline.

## Inputs

- Stage artifact
- Source reference
- Actor or system reference
- Time or ordering reference
- Evidence reference
- Transformation trace
- Context reference

## Outputs

- Ingestion provenance envelope
- Custody trace
- Derivation trace
- Adapter boundary trace
- Confidence or gap statement
- Failure or uncertainty condition

## Invariants

- Provenance supports knowledge but does not define asset identity.
- Every stage artifact must remain traceable.
- Missing provenance prevents durable promotion.
- Provenance records do not overwrite observations.

## Producer

Universal Asset Ingestion

Exactly one program produces this stage contract across the ingestion pipeline.

## Consumers

All ingestion stages, ARK, Evidence, Proof, Promotion, Audit.

## Does Not Own

- Identity generation
- Truth evaluation
- Storage implementation
- Policy authorization
- Reality graph behavior
- Media processing

## Dependencies

- Provenance Contract
- Evidence Contract
- Observation Contract
- Execution Semantics
- Asset Model

## Failure Conditions

- Missing custody trace
- Untrusted source chain
- Unrecorded transformation
- Ambiguous actor
- Broken source link
- Insufficient evidence for promotion

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Media adapter code.
- Engine refactoring.
- Durable promotion by itself.
