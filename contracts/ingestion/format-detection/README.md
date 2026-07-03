# Format Detection Contract

## Purpose

Defines the boundary for detecting source format, container, encoding, schema hint, and adapter path without interpreting meaning.

## Inputs

- Acquisition candidate
- Source reference
- Payload reference
- Context reference
- Evidence reference
- Adapter boundary metadata

## Outputs

- Format detection result
- Detected format or explicit unknown
- Adapter candidate
- Schema candidate
- Confidence statement
- Failure or uncertainty condition

## Invariants

- Detection does not create durable knowledge.
- Detection does not assign identity.
- Detection does not interpret semantic meaning.
- Unknown or conflicting format remains explicit.

## Producer

Universal Asset Ingestion

Exactly one program produces this stage contract across the ingestion pipeline.

## Consumers

Canonicalization, Ingestion Provenance, media adapters, ARK.

## Does Not Own

- Media conversion
- Canonicalization
- Semantic normalization
- Identity assignment
- Storage backend selection
- ARK promotion

## Dependencies

- Acquisition Contract
- Representation Contract
- Schema Contract
- Evidence Contract
- Provenance Contract

## Failure Conditions

- Unknown format
- Conflicting format signals
- Unsupported encoding
- Unsafe adapter candidate
- Missing payload reference
- Insufficient evidence

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Media adapter code.
- Engine refactoring.
- Durable promotion by itself.
