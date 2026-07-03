# Content Addressing Contract

## Purpose

Defines the boundary for referring to ingested content by integrity or address while keeping content addresses distinct from RIDs.

## Inputs

- Canonical representation candidate
- Chunk set
- Compressed representation
- Evidence reference
- Provenance reference
- Storage boundary metadata

## Outputs

- Content address reference
- Integrity reference
- Address-to-source relationship
- Address confidence statement
- Failure or uncertainty condition

## Invariants

- Content addresses do not replace RIDs.
- Content addressing does not imply durable truth.
- Addressed content remains traceable to source evidence.
- Storage owns persistence, not identity.

## Producer

Universal Asset Ingestion

Exactly one program produces this stage contract across the ingestion pipeline.

## Consumers

Knowledge Extraction, ARK, Storage Service, Evidence, Provenance.

## Does Not Own

- RID generation
- Persistence backend selection
- Asset identity ownership
- ARK promotion
- Semantic extraction
- Deletion policy

## Dependencies

- Compression Contract
- Storage Contract
- Evidence Contract
- Provenance Contract
- Identity Contract
- Asset Model

## Failure Conditions

- Unstable address
- Integrity mismatch
- Missing source relationship
- Address/RID confusion
- Storage boundary ambiguity
- Unsupported content reference

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Media adapter code.
- Engine refactoring.
- Durable promotion by itself.
