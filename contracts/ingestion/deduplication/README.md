# Deduplication Contract

## Purpose

Defines the boundary for identifying repeated content, repeated observations, or possible identity overlap without prematurely merging identities or discarding evidence.

## Inputs

- RID assignment proposal
- Chunk set
- Content address candidate
- Evidence reference
- Provenance reference
- Context reference
- Duplicate comparison basis

## Outputs

- Duplicate candidate assessment
- Same-content candidate
- Same-identity candidate
- Non-duplicate statement
- Confidence statement
- Failure or uncertainty condition

## Invariants

- Deduplication does not merge RIDs without proof.
- Duplicate content is distinct from duplicate identity.
- Evidence is not discarded because duplication is suspected.
- Uncertainty remains explicit.

## Producer

Universal Asset Ingestion

Exactly one program produces this stage contract across the ingestion pipeline.

## Consumers

Compression, Content Addressing, Knowledge Extraction, ARK, Storage Service.

## Does Not Own

- Identity merge
- Data deletion
- Storage garbage collection
- Truth promotion
- Policy authorization
- Reality graph ownership

## Dependencies

- Identity Assignment Contract
- Evidence Contract
- Provenance Contract
- Proof Contract
- Storage Contract

## Failure Conditions

- Insufficient comparison basis
- Conflicting duplicate signals
- Hash/address mismatch
- Identity/content confusion
- Missing provenance
- Unsafe discard recommendation

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Media adapter code.
- Engine refactoring.
- Durable promotion by itself.
