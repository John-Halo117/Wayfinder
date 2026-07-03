# Canonicalization Contract

## Purpose

Defines the boundary for producing a canonical representation candidate from a detected source while preserving source evidence and ending media-specific logic.

## Inputs

- Format detection result
- Source representation
- Adapter candidate
- Schema candidate
- Evidence reference
- Provenance reference
- Context reference

## Outputs

- Canonical representation candidate
- Source-to-canonical relationship
- Canonical schema reference
- Transformation trace
- Confidence statement
- Failure or uncertainty condition

## Invariants

- Canonicalization never overwrites source observation.
- Canonicalization does not change RID or asset identity.
- Media-specific logic ceases after this stage.
- Canonical output remains a representation candidate until proven and promoted.

## Producer

Universal Asset Ingestion

Exactly one program produces this stage contract across the ingestion pipeline.

## Consumers

Semantic Normalization, Chunking, Ingestion Provenance, ARK, Views.

## Does Not Own

- Identity generation
- Semantic interpretation
- Truth claims
- Storage persistence
- Durable promotion
- Domain-specific schema ownership

## Dependencies

- Format Detection Contract
- Representation Contract
- Schema Contract
- Evidence Contract
- Provenance Contract
- Asset Model

## Failure Conditions

- Unsupported conversion
- Lossy conversion risk
- Invalid canonical schema candidate
- Missing source trace
- Adapter boundary violation
- Incomplete representation

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Media adapter code.
- Engine refactoring.
- Durable promotion by itself.
