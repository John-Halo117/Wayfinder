# Chunking Contract

## Purpose

Defines the boundary for splitting normalized representations into bounded units suitable for evidence, retrieval, proof, or later extraction.

## Inputs

- Normalized contract-language artifact
- Canonical representation reference
- Context reference
- Evidence reference
- Provenance reference
- Chunking constraints

## Outputs

- Bounded chunk set
- Chunk-to-source relationships
- Chunk order or location references
- Chunk evidence references
- Failure or uncertainty condition

## Invariants

- Chunks remain representations or evidence units unless separately promoted as assets.
- Chunking must preserve traceability to the source representation.
- Chunking must be bounded.
- Chunking does not interpret or promote truth.

## Producer

Universal Asset Ingestion

Exactly one program produces this stage contract across the ingestion pipeline.

## Consumers

Identity Assignment, Deduplication, Compression, Content Addressing, Knowledge Extraction, ARK.

## Does Not Own

- Asset creation by default
- Identity generation
- Knowledge extraction
- Storage implementation
- Search index ownership
- ARK promotion

## Dependencies

- Semantic Normalization Contract
- Representation Contract
- Evidence Contract
- Provenance Contract
- Asset Model

## Failure Conditions

- Unbounded chunk plan
- Missing source reference
- Irreversible source loss
- Conflicting chunk order
- Oversized chunk
- Insufficient evidence trace

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Media adapter code.
- Engine refactoring.
- Durable promotion by itself.
