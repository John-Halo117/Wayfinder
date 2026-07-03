# Semantic Normalization Contract

## Purpose

Defines the boundary for aligning canonical representation fields, labels, and structures to Wayfinder constitutional language without deciding truth.

## Inputs

- Canonical representation candidate
- Schema reference
- Context reference
- Evidence reference
- Provenance reference
- Source terms or fields

## Outputs

- Normalized contract-language artifact
- Source term mapping
- Uncertainty notes
- Schema alignment statement
- Failure or uncertainty condition

## Invariants

- Normalization is not interpretation by default.
- Source terms remain traceable.
- Ambiguous mappings remain explicit.
- Normalization does not promote knowledge or merge identities.

## Producer

Universal Asset Ingestion

Exactly one program produces this stage contract across the ingestion pipeline.

## Consumers

Chunking, Identity Assignment, Knowledge Extraction, ARK, Interpretation.

## Does Not Own

- Truth evaluation
- Reasoning
- Identity merge
- Policy decision
- Reality preservation
- Domain-specific ontology ownership

## Dependencies

- Canonicalization Contract
- Schema Contract
- Context Contract
- Evidence Contract
- Provenance Contract

## Failure Conditions

- Ambiguous field mapping
- Missing schema reference
- Conflicting source terms
- Unsupported structure
- Lost source trace
- Over-normalization risk

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Media adapter code.
- Engine refactoring.
- Durable promotion by itself.
