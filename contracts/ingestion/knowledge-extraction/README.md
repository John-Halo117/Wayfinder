# Knowledge Extraction Contract

## Purpose

Defines the boundary for extracting evidence-backed candidate claims, entities, relationships, capabilities, and observations from ingested artifacts before ARK promotion.

## Inputs

- Content address reference
- Compressed or canonical representation
- Chunk set
- RID reference or identity proposal
- Evidence reference
- Provenance envelope
- Context reference

## Outputs

- Knowledge candidate
- Claim candidate
- Entity candidate
- Relationship candidate
- Capability candidate
- Evidence bundle reference
- Failure or uncertainty condition

## Invariants

- Extraction produces candidates, not durable truth.
- ARK owns promotion into durable reality preservation.
- Extracted knowledge remains evidence-bound and provenance-traceable.
- Uncertainty and absence are represented explicitly.

## Producer

Universal Asset Ingestion

Exactly one program produces this stage contract across the ingestion pipeline.

## Consumers

ARK, WEAVE, Interpretation, Reasoning, Views, Jarvis, domains.

## Does Not Own

- Durable promotion
- Reality graph ownership
- Reasoning conclusions
- Navigation recommendations
- Identity merge
- Policy decisions

## Dependencies

- Content Addressing Contract
- Identity Assignment Contract
- Evidence Contract
- Provenance Contract
- Proof Contract
- Asset Model
- Relationship Contract
- Capability Contract

## Failure Conditions

- Insufficient evidence
- Ambiguous claim
- Conflicting extraction
- Missing RID context
- Unsupported extraction target
- Promotion criteria not met

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Media adapter code.
- Engine refactoring.
- Durable promotion by itself.
