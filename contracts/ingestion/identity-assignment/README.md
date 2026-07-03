# Identity Assignment Contract

## Purpose

Defines the boundary for attaching, proposing, or resolving RID references for ingested assets, representations, chunks, or candidate entities through the Identity Service.

## Inputs

- Chunk set or normalized artifact
- Asset candidate
- Existing RID or alias reference
- Evidence reference
- Provenance reference
- Context reference
- Identity constraints

## Outputs

- RID assignment proposal
- Existing RID reference
- Alias or namespace reference
- Identity uncertainty statement
- Merge or split candidate note
- Failure condition

## Invariants

- Identity Service owns identity generation and lookup.
- RID identifies the asset or constitutional referent, not the representation.
- Identity claims require evidence and provenance.
- Merge and split remain proof-gated.

## Producer

Universal Asset Ingestion

Exactly one program produces this stage contract across the ingestion pipeline.

## Consumers

Deduplication, Content Addressing, Knowledge Extraction, ARK, WEAVE, domains.

## Does Not Own

- Reality preservation
- Durable identity promotion
- Observation or evidence ownership
- Storage persistence
- Semantic interpretation
- Deduplication decision by itself

## Dependencies

- Identity Contract
- Identity Service
- RID Model
- Asset Model
- Evidence Contract
- Provenance Contract

## Failure Conditions

- Unknown RID
- Invalid namespace
- Alias conflict
- Insufficient identity evidence
- Possible duplicate identity
- Over-broad identity candidate

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Media adapter code.
- Engine refactoring.
- Durable promotion by itself.
