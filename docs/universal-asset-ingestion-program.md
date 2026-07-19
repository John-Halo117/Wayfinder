# Universal Asset Ingestion Implementation Program

Date: 2026-06-27

This program adds first-class planning for Wayfinder's Universal Asset Ingestion architecture. It is planning evidence only. It does not implement an ingestion engine, refactor ARK, or change runtime behavior.

## Evidence Summary

| Evidence | Finding |
| --- | --- |
| `constitution/assets.md` | Everything Wayfinder operates on should be representable as an Asset in Context; representations are not assets. |
| `docs/reality-identity-program.md` | RID precedes Universal Asset Ingestion and full ARK implementation. |
| `engines/ark/README.md` | ARK owns preservation, provenance, append-only reality, replay, LVR, Source Relationship preservation, and proof-gated promotion, and consumes Identity, Event Bus, Storage, and Policy. |
| `capabilities/README.md` | Capability grammar is reusable verb language, not architectural layers or implementations. |
| `contracts/observations/README.md` | Observation records reality before interpretation and may reference Asset or RID. |
| `contracts/assets/README.md` | ARK produces durable asset knowledge while the Asset model remains constitutional. |
| `docs/implementation-backlog.md` | Universal Asset Ingestion is already named as a prerequisite after RID and before Runtime Kernel/ARK. |
| `docs/migration-dashboard.md` | ARK remains folded and not rewired to platform services. |

## Objective

Implement the reusable ingestion foundation for every asset type.

Universal ingestion becomes the canonical ingestion model for ARK. Media-specific pipelines are deprecated as architectural owners. Media adapters remain valid as implementation-specific adapters into the universal ingestion model.

## Ownership

| Concept | Canonical Owner | Notes |
| --- | --- | --- |
| Universal Asset model | `constitution/assets.md`, `contracts/assets/` | Defines Asset in Context and representation separation. |
| RID and identity | `constitution/assets.md`, `contracts/identities/`, `services/identity/` | RID anchors ingested assets. |
| Ingestion behavior | ARK, through future universal ingestion boundary | ARK consumes universal ingestion output for reality preservation. |
| Media adapters | Future adapter implementations | Adapters translate media-specific inputs into universal ingestion contracts. |
| Media-specific pipelines | Deprecated as canonical architecture | Media-specific logic must not own ingestion concepts. |

## Capability Planning

Universal ingestion is represented as reusable capabilities. These are not additional architectural layers.

| Capability | Purpose | Canonical Boundary |
| --- | --- | --- |
| Acquisition | Bring an external or local asset candidate under Wayfinder attention. | Capability grammar, Observation contracts |
| Detection | Determine candidate format, type, and adapter path. | Capability grammar, Representation contracts |
| Canonicalization | Produce a stable canonical representation candidate. | Representation and Schema contracts |
| Normalization | Align source-specific structure to Wayfinder language. | Contracts and adapters |
| Chunking | Split representations into bounded units for proof and retrieval. | Representation and Evidence contracts |
| Identity | Attach or propose RID and identity references. | Identity contracts and Identity Service |
| Deduplication | Detect repeated content or identity candidates without merging prematurely. | Identity, Evidence, and Proof contracts |
| Compression | Produce smaller derived representations without changing asset identity. | Capability grammar and Representation contracts |
| Content Addressing | Refer to content by integrity or address without replacing RID. | Storage, Evidence, and Provenance contracts |
| Provenance | Preserve source, custody, derivation, and transformation traces. | Provenance contracts and ARK behavior |
| Versioning | Track representation or asset knowledge versions without identity drift. | Storage and Promotion contracts |
| Entity Extraction | Extract candidate entities as evidence-backed claims. | Evidence, Identity, and ARK proof boundaries |
| Relationship Extraction | Extract candidate relationships without promoting them as truth. | Relationship, Evidence, and WEAVE boundaries |
| Embeddings | Produce derived representations for retrieval or similarity. | Ephemeral by default; Representation contracts |
| Indexing | Produce derived lookup structures. | Ephemeral by default; Search/Storage future service boundaries |

## Maturity Model

| Stage | Meaning | Evidence Required |
| --- | --- | --- |
| Stage 0 | Program | Universal ingestion purpose, ownership, capabilities, and dependency order are documented. |
| Stage 1 | Contracts | Pipeline contracts and capability boundaries are specified. |
| Stage 2 | Minimal Implementation | A bounded ingestion foundation exists without media-specific ownership. |
| Stage 3 | Adapter Slice | One media adapter proves the universal ingestion boundary without becoming the architecture. |
| Stage 4 | ARK Integration | ARK consumes universal ingestion output without behavior drift. |
| Stage 5 | Verified Migration | Legacy media-specific pipelines are deprecated, adapted, or retired with proof. |

## Program Progress

| Component | Stage | Status |
| --- | :---: | --- |
| Pipeline Contracts | 0 | 🔄 Next |
| Acquisition | 0 | ⏳ |
| Format Detection | 0 | ⏳ |
| Canonicalization | 0 | ⏳ |
| Semantic Normalization | 0 | ⏳ |
| Chunking | 0 | ⏳ |
| Identity Integration | 0 | ⏳ |
| Content Addressing | 0 | ⏳ |
| Knowledge Extraction | 0 | ⏳ |
| ARK Integration | 0 | ⏳ |

## Dependency Order

```text
Identity
  -> Reality ID (RID)
  -> Universal Asset Ingestion
  -> Runtime Kernel
  -> ARK
  -> WEAVE
  -> Interpretation
  -> Reasoning
  -> Views
  -> Jarvis
```

Universal Asset Ingestion precedes full ARK implementation. ARK may continue preserving legacy behavior until a proof-backed integration consumes universal ingestion output.

## Milestone Roadmap

| Milestone | Target Stage | Status | Depends On |
| --- | :---: | --- | --- |
| UAI-M-001 Pipeline Contracts | 1 | 🔄 Next | RID-M-003 RID Model |
| UAI-M-002 Acquisition | 2 | ⏳ | UAI-M-001 |
| UAI-M-003 Format Detection | 2 | ⏳ | UAI-M-002 |
| UAI-M-004 Canonicalization | 2 | ⏳ | UAI-M-003 |
| UAI-M-005 Semantic Normalization | 2 | ⏳ | UAI-M-004 |
| UAI-M-006 Chunking | 2 | ⏳ | UAI-M-005 |
| UAI-M-007 Identity Integration | 3 | ⏳ | UAI-M-006, RID program |
| UAI-M-008 Content Addressing | 3 | ⏳ | UAI-M-007, Storage Service |
| UAI-M-009 Knowledge Extraction | 3 | ⏳ | UAI-M-008 |
| UAI-M-010 ARK Integration | 4 | ⏳ | UAI-M-009 |

## Milestone Dependency Graph

```text
UAI-M-001 Pipeline Contracts
  -> UAI-M-002 Acquisition
      -> UAI-M-003 Format Detection
          -> UAI-M-004 Canonicalization
              -> UAI-M-005 Semantic Normalization
                  -> UAI-M-006 Chunking
                      -> UAI-M-007 Identity Integration
                          -> UAI-M-008 Content Addressing
                              -> UAI-M-009 Knowledge Extraction
                                  -> UAI-M-010 ARK Integration
```

## Implementation Backlog

### UAI-M-001 Pipeline Contracts

Status: Next after RID-M-003.

Tasks:

- Define universal ingestion pipeline contracts as planning evidence.
- Classify inputs and outputs using Asset, RID, Observation, Evidence, Provenance, Representation, Schema, and Context language.
- Define media adapter boundaries.
- Mark media-specific pipelines as deprecated architectural owners.

Acceptance Criteria:

- Pipeline contracts are implementation-free.
- Universal ingestion does not create a new architectural layer above capabilities.
- Media adapters are the only media-specific implementation boundary.
- ARK remains the reality preservation consumer.

### UAI-M-002 Acquisition

Status: Planned.

Tasks:

- Plan acquisition of local files, remote objects, service exports, event streams, and manual inputs.
- Define source references, trust boundary, and initial observation relationship.

Acceptance Criteria:

- Acquisition does not decide identity or meaning.
- Acquisition output is bounded and evidence-ready.

### UAI-M-003 Format Detection

Status: Planned.

Tasks:

- Plan detection of media type, container type, encoding, and adapter candidate.
- Keep detection separate from interpretation.

Acceptance Criteria:

- Detection failure remains explicit.
- Detection does not create durable knowledge without proof.

### UAI-M-004 Canonicalization

Status: Planned.

Tasks:

- Plan canonical representation candidates.
- Preserve source representation and provenance.

Acceptance Criteria:

- Canonicalization does not overwrite observation.
- Representation changes do not change RID.

### UAI-M-005 Semantic Normalization

Status: Planned.

Tasks:

- Plan normalization from source-specific fields into Wayfinder contract language.
- Preserve ambiguity and source terms where needed.

Acceptance Criteria:

- Normalization is not interpretation by default.
- Uncertain mappings remain explicit.

### UAI-M-006 Chunking

Status: Planned.

Tasks:

- Plan bounded chunking for text, documents, media metadata, events, and structured records.
- Define chunk identity relationship to the source asset and representation.

Acceptance Criteria:

- Chunks remain representations or evidence units, not assets unless separately promoted.
- Chunking is bounded and reversible enough for proof.

### UAI-M-007 Identity Integration

Status: Planned.

Tasks:

- Attach candidate RID references through Identity Service boundaries.
- Plan alias, merge, split, and unknown identity handling.

Acceptance Criteria:

- RID claims are evidence-backed.
- Identity Service remains the reusable implementation owner.

### UAI-M-008 Content Addressing

Status: Planned.

Tasks:

- Plan integrity and content addressing references.
- Separate content address from RID.

Acceptance Criteria:

- Content address does not replace asset identity.
- Storage and provenance boundaries are respected.

### UAI-M-009 Knowledge Extraction

Status: Planned.

Tasks:

- Plan entity extraction, relationship extraction, embeddings, and indexing as evidence-producing or ephemeral capabilities.
- Keep extraction outputs unpromoted until proof.

Acceptance Criteria:

- Extracted knowledge remains candidate evidence until ARK proof/promotion.
- WEAVE owns durable relationship topology after promotion, not ingestion.

### UAI-M-010 ARK Integration

Status: Planned.

Tasks:

- Plan how ARK consumes universal ingestion output as observations, evidence, provenance, and asset knowledge.
- Do not refactor ARK until compatibility proof exists.

Acceptance Criteria:

- ARK consumes universal ingestion without owning media-specific pipelines.
- Runtime behavior remains unchanged until proof-backed migration.

## Deprecated Architecture

Media-specific pipelines are deprecated as canonical ingestion architecture. They may remain temporarily as compatibility shims or adapters, but they must not own acquisition, detection, canonicalization, normalization, identity, provenance, or extraction concepts.

## Validation

| Check | Result |
| --- | --- |
| Dependency graph remains acyclic | Pass |
| Universal Ingestion precedes full ARK implementation | Pass |
| No implementation files changed by this planning task | Pass |
| Existing roadmap remains valid | Pass |
| No additional architectural layers introduced | Pass |
| Media-specific pipelines deprecated as owners, not forcibly removed | Pass |

## Recommended Next Milestone

UAI-M-001 Pipeline Contracts, after RID-M-003 RID Model.

Reason: Universal ingestion depends on RID stability. Pipeline contracts should be planned before acquisition, detection, adapters, or ARK integration.
