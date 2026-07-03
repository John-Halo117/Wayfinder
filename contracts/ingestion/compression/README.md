# Compression Contract

## Purpose

Defines the boundary for producing compact derived representations while preserving identity, evidence, provenance, and source recoverability constraints.

## Inputs

- Chunk set
- Deduplication assessment
- Canonical representation reference
- Evidence reference
- Provenance reference
- Compression objective or constraint

## Outputs

- Compressed derived representation
- Compression trace
- Recoverability statement
- Loss statement
- Failure or uncertainty condition

## Invariants

- Compression does not change asset identity.
- Compression does not replace source evidence.
- Lossy compression risk remains explicit.
- Compressed artifacts remain representations unless promoted otherwise.

## Producer

Universal Asset Ingestion

Exactly one program produces this stage contract across the ingestion pipeline.

## Consumers

Content Addressing, Knowledge Extraction, ARK, Storage Service, Views.

## Does Not Own

- Storage implementation
- Identity assignment
- Knowledge extraction
- Source deletion
- Durable promotion
- Evidence replacement

## Dependencies

- Chunking Contract
- Deduplication Contract
- Representation Contract
- Evidence Contract
- Provenance Contract

## Failure Conditions

- Unacceptable loss
- Missing recoverability statement
- Source trace gap
- Compression objective conflict
- Integrity mismatch
- Representation confusion

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Media adapter code.
- Engine refactoring.
- Durable promotion by itself.
