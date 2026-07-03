# Universal Asset Ingestion Pipeline Contracts

## Purpose

Defines the constitutional contracts for the Universal Asset Ingestion pipeline. These contracts describe the artifacts that cross stage boundaries during ingestion. They do not implement media processing, storage, identity generation, or ARK reality preservation.

Universal Asset Ingestion exists to orchestrate reusable ingestion stages for every Asset in Context. It prevents media-specific pipelines from becoming separate architectural owners.

## Producer

Universal Asset Ingestion

Exactly one program produces the pipeline contract family across stage boundaries. Individual services and engines retain ownership of their own responsibilities.

## Consumers

Media adapters, Identity Service, Storage Service, ARK, WEAVE, Interpretation, Reasoning, Views, Jarvis, domains, internal applications, and future ingestion capabilities.

## Canonical Grammar

Every future ingestion path conforms to this grammar:

```text
Reality
  -> Acquire
  -> Detect
  -> Canonicalize
  -> Normalize
  -> Chunk
  -> Assign Identity
  -> Deduplicate
  -> Compress
  -> Content Address
  -> Extract Knowledge
  -> ARK
```

Provenance is required at every stage boundary. The Provenance stage contract defines the evidence envelope for source, custody, derivation, and transformation traces, but it does not create an additional architectural owner or alter the canonical execution grammar.

## Adapter Boundary

Media adapters are responsible only for converting a source asset into the canonical representation required by the shared pipeline.

After canonicalization, media-specific logic must cease. Downstream stages operate on Wayfinder constitutional language: Asset, RID, Observation, Evidence, Provenance, Representation, Schema, Context, Proof, and Promotion.

Adapters do not own ingestion, identity, persistence, interpretation, reality preservation, or durable promotion.

## Ownership

| Responsibility | Canonical Owner |
| --- | --- |
| Pipeline orchestration language | Universal Asset Ingestion contracts |
| Identity generation and lookup | Identity Service |
| RID semantics | Constitution, Identity contracts, Identity Service |
| Persistence and object storage | Storage Service |
| Reality preservation | ARK |
| Observation, Evidence, Provenance, Proof, Promotion | ARK and canonical contracts |
| Media-specific conversion | Media adapters |
| Meaning, reasoning, navigation, and action | Downstream engines through their contracts |

No capability absorbs another capability's responsibility. Pipeline contracts compose capabilities without becoming a new architectural layer above capabilities.

## Stage Contracts

| Stage | Contract | Primary Output |
| --- | --- | --- |
| Acquisition | [Acquisition](acquisition/README.md) | Acquisition candidate |
| Format Detection | [Format Detection](format-detection/README.md) | Format detection result |
| Canonicalization | [Canonicalization](canonicalization/README.md) | Canonical representation candidate |
| Semantic Normalization | [Semantic Normalization](semantic-normalization/README.md) | Normalized contract-language artifact |
| Chunking | [Chunking](chunking/README.md) | Bounded chunk set |
| Identity Assignment | [Identity Assignment](identity-assignment/README.md) | RID assignment proposal or reference |
| Deduplication | [Deduplication](deduplication/README.md) | Duplicate candidate assessment |
| Compression | [Compression](compression/README.md) | Compressed derived representation |
| Content Addressing | [Content Addressing](content-addressing/README.md) | Content address reference |
| Provenance | [Provenance](provenance/README.md) | Ingestion provenance envelope |
| Knowledge Extraction | [Knowledge Extraction](knowledge-extraction/README.md) | Evidence-backed knowledge candidates |

## Invariants

- Reality precedes ingestion.
- Acquisition precedes detection.
- Detection precedes canonicalization.
- Canonicalization ends media-specific logic.
- Normalization does not decide truth.
- Chunking does not create new assets unless later proof promotes a distinct asset.
- Identity assignment uses the Identity Service boundary.
- Deduplication does not merge identities without proof.
- Compression does not change asset identity or erase source evidence.
- Content addresses do not replace RIDs.
- Knowledge extraction produces candidates until ARK promotion.
- ARK remains the consumer responsible for durable reality preservation.

## Dependencies

- [Asset Model](../../constitution/assets.md)
- [Execution Semantics](../../constitution/execution.md)
- [Repository Responsibilities](../../constitution/repository.md)
- [Observation Contract](../observations/README.md)
- [Evidence Contract](../evidence/README.md)
- [Provenance Contract](../provenance/README.md)
- [Identity Contract](../identities/README.md)
- [Representation Contract](../representations/README.md)
- [Schema Contract](../schemas/README.md)
- [Storage Contract](../storage/README.md)

## Failure Conditions

Missing source, unsupported format, unsafe adapter boundary, failed canonicalization, ambiguous normalization, unbounded chunking, unresolved identity, duplicate uncertainty, lossy compression risk, unstable content address, missing provenance, insufficient evidence, or ARK promotion failure remain explicit uncertainty. They must not be converted into durable knowledge without proof.

## Non-Goals

- Runtime behavior.
- Media processing algorithms.
- Storage formats.
- Identity implementation.
- ARK refactoring.
- Engine migration.
- Adapter implementation.
