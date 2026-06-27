# Implementation Backlog

Date: 2026-06-27

This backlog converts Constitution v1 into implementation milestones. It is evidence for execution, not a new constitutional source. When this document conflicts with Constitution, Canon, Contracts, or service and engine documentation, those higher-order sources control.

## Evidence Basis

| Evidence | Finding |
| --- | --- |
| `constitution/repository.md` | Services own reusable infrastructure; engines own unique responsibilities; repository topology is responsibility-based. |
| `constitution/execution.md` | Durable promotion requires proof; execution remains separate from repository layout. |
| `contracts/events/README.md` | Event Bus produces event boundary language: envelope, metadata, routing, correlation, causation, replay. |
| `services/identity/docs/implementation-proof.md` | Identity is the only executable service implementation proof completed so far. |
| `docs/migration-dashboard.md` | Event Bus, Storage, Configuration, and Policy implementation proofs are not started. |
| `docs/architectural-debt.md` | Event Bus, Storage, Configuration, and Policy still carry reduced or open implementation debt. |

## Platform Progress

| Component | Stage | Status |
| --- | :---: | --- |
| Identity | 2 | ✅ |
| Event Bus | 2 | ✅ |
| Storage | 1 | 🔄 Next |
| Configuration | 1 | ⏳ |
| Policy | 1 | ⏳ |

## Platform Ownership

| Component | Canonical Owner | Contract Language | Current Proof |
| --- | --- | --- | --- |
| Identity | `services/identity/` | `contracts/identities/` | Minimal implementation proof complete |
| Event Bus | `services/event-bus/` | `contracts/events/` | Minimal implementation proof complete |
| Storage | `services/storage/` | `contracts/storage/` | Contracts only; next implementation proof |
| Configuration | `services/configuration/` | Configuration service contracts | Contracts only |
| Policy | `services/policy/` | `contracts/policies/`, `contracts/permissions/` | Contracts only |

## Platform Roadmap

| Order | Milestone | Target Stage | Status |
| ---: | --- | :---: | --- |
| 1 | Identity Minimal Implementation Proof | 2 | ✅ Complete |
| 2 | Event Bus Minimal Implementation Proof | 2 | ✅ Complete |
| 3 | Storage Minimal Implementation Proof | 2 | 🔄 Next |
| 4 | Configuration Minimal Implementation Proof | 2 | ⏳ Waiting on Storage |
| 5 | Policy Minimal Implementation Proof | 2 | ⏳ Waiting on Configuration |
| 6 | Identity Vertical Slice | 3 | ⏳ Waiting on platform substrate |


## Reality Identity Progress

| Component | Stage | Status |
| --- | :---: | --- |
| Identity Contracts | 1 | ✅ |
| Identity Service | 2 | ✅ |
| RID Model | 2 | 🔄 Next |
| Domain Identifiers | 1 | ⏳ |
| Identity Encoding | 1 | ⏳ |
| Identity Resolution | 2 | ⏳ |
| Provenance Integration | 1 | ⏳ |
| ARK Integration | 1 | ⏳ |
| Migration | 0 | ⏳ |
| Verification | 0 | ⏳ |

## Reality Identity Roadmap

| Milestone | Target Stage | Status |
| --- | :---: | --- |
| RID-M-001 Identity Contracts | 1 | ✅ Complete |
| RID-M-002 Identity Service | 2 | ✅ Complete |
| RID-M-003 RID Model | 3 | 🔄 Next |
| RID-M-004 Domain Identifiers | 3 | ⏳ |
| RID-M-005 Identity Encoding | 3 | ⏳ |
| RID-M-006 Identity Resolution | 3 | ⏳ |
| RID-M-007 Provenance Integration | 4 | ⏳ |
| RID-M-008 ARK Integration | 4 | ⏳ |
| RID-M-009 Migration | 5 | ⏳ |
| RID-M-010 Verification | 5 | ⏳ |


## Universal Asset Ingestion Progress

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

## Universal Asset Ingestion Roadmap

| Milestone | Target Stage | Status |
| --- | :---: | --- |
| UAI-M-001 Pipeline Contracts | 1 | 🔄 Next after RID-M-003 |
| UAI-M-002 Acquisition | 2 | ⏳ |
| UAI-M-003 Format Detection | 2 | ⏳ |
| UAI-M-004 Canonicalization | 2 | ⏳ |
| UAI-M-005 Semantic Normalization | 2 | ⏳ |
| UAI-M-006 Chunking | 2 | ⏳ |
| UAI-M-007 Identity Integration | 3 | ⏳ |
| UAI-M-008 Content Addressing | 3 | ⏳ |
| UAI-M-009 Knowledge Extraction | 3 | ⏳ |
| UAI-M-010 ARK Integration | 4 | ⏳ |

## Maturity Model

| Stage | Meaning | Evidence Required |
| --- | --- | --- |
| Stage 0 | Constitution | Constitutional home and responsibility are documented. |
| Stage 1 | Contracts | Boundary language exists with producer, consumers, inputs, outputs, invariants, failure modes, and promotion rules. |
| Stage 2 | Minimal Implementation | A bounded, service-owned implementation exists with focused tests and no forbidden dependencies. |
| Stage 3 | Vertical Slice | At least one consumer exercises the implementation through the intended boundary without behavior drift. |
| Stage 4 | Operational | Health, observability, failure handling, and runtime operations are validated. |
| Stage 5 | Mature | Multiple consumers reuse the component; debt is low; compatibility and rollback evidence are stable. |

## Current Component Maturity

| Component | Current Stage | Evidence | Next Stage |
| --- | --- | --- | --- |
| Identity Service | Stage 2 - Minimal Implementation | `services/identity/identity_service.py`, service tests, implementation proof | Stage 3 - Vertical Slice |
| Event Bus Service | Stage 2 - Minimal Implementation | `services/event-bus/event_bus_service.py`, service tests, implementation proof | Stage 3 - Vertical Slice |
| Storage Service | Stage 1 - Contracts | `contracts/storage/README.md`, `services/storage/README.md` | Stage 2 - Minimal Implementation |
| Configuration Service | Stage 1 - Contracts | `services/configuration/README.md` | Stage 2 - Minimal Implementation |
| Policy Service | Stage 1 - Contracts | `contracts/policies/README.md`, `contracts/permissions/README.md`, `services/policy/README.md` | Stage 2 - Minimal Implementation |
| Reality ID (RID) | Stage 2 - Planning / Identity Service foundation | `constitution/assets.md`, `contracts/identities/README.md`, `services/identity/docs/implementation-proof.md` | Stage 3 - RID Model |
| Universal Asset Ingestion | Stage 0 - Program | RID program, Asset Model, ARK boundary, and `docs/universal-asset-ingestion-program.md` | Stage 1 - Pipeline Contracts |
| Runtime Kernel | Stage 0 - Constitution implied | Dependency order names it, but no canonical service home exists yet | Stage 1 - Contract and boundary evidence after RID and asset ingestion planning mature |
| ARK | Stage 1 - Contracts and Folded Evidence | ARK constitutional README, legacy fold, inventories, contracts | Stage 2 after RID, asset ingestion, and platform services can be consumed |
| WEAVE | Stage 0 - Constitution | Engine boundary exists | Stage 1 contract refinement after ARK service consumers stabilize |
| Interpretation | Stage 0 - Constitution | Engine boundary exists | Stage 1 contract refinement after ARK and WEAVE evidence |
| Reasoning | Stage 0 - Constitution | Engine boundary exists | Stage 1 contract refinement after Interpretation evidence |
| Views | Stage 1 - Contracts | View contract and engine boundary exist | Stage 2 after reasoning outputs stabilize |
| Jarvis | Stage 1 - Contracts and Folded Evidence | Jarvis boundary and folding docs exist | Stage 2 after platform services and bearings route evidence |
| Capsules | Stage 1 - Contracts | Capsule contract and engine boundary exist | Stage 2 after ARK/Jarvis slice evidence |
| ZWLib | Stage 1 - Contracts | Transformation contract and engine boundary exist | Stage 2 after capability and asset slice evidence |
| Foundry | Stage 1 - Contracts and Folded Evidence | Foundry boundary and Forge normalization evidence exist | Stage 2 after platform services mature |
| NOMAD | Stage 1 - Contracts | Capability availability contract and engine boundary exist | Stage 2 after discovery boundary proof |
| MIDAS | Stage 0 - Constitution | Engine boundary exists | Stage 1 after dedicated inventory |
| MICE | Stage 1 - Contracts | Commitment contract and engine boundary exist | Stage 2 after recommendation/commitment slice evidence |
| VALOR | Stage 1 - Contracts | Health contract and engine boundary exist | Stage 2 after telemetry/health implementation proof |
| Blackwall | Stage 1 - Contracts | Permission/policy contracts and boundary exist | Stage 2 after Policy service implementation proof |
| NetWatch | Stage 0 - Constitution | Engine boundary exists | Stage 1 after VALOR and external observation evidence |

## Milestone Queue

### M-001: Implementation Backlog Baseline

- Stage: Program / Roadmap / Backlog
- Dependencies: Constitution v1, contract normalization, migration dashboard
- Tasks:
  - Record current component maturity.
  - Define milestone queue in dependency order.
  - Add acceptance criteria and definitions of done.
  - Update roadmap and dashboard references.
- Acceptance Criteria:
  - Backlog exists and is discoverable from `docs/README.md`.
  - Every platform service has a next implementation milestone.
  - Dependency order is explicit.
  - No runtime behavior changes.
- Definition of Done:
  - Backlog is committed as documentation evidence.
  - Verification confirms no code files changed for this milestone.

### M-002: Event Bus Minimal Implementation Proof

- Stage: Stage 2 - Minimal Implementation
- Status: Complete 2026-06-27
- Dependencies: M-001, Event Contract, Identity Service implementation proof
- Tasks:
  - Discover reusable event behavior in ARK, Jarvis, and Foundry.
  - Inventory publish, subscribe, routing, metadata, correlation, causation, and replay evidence.
  - Implement the smallest transport-neutral Event Bus service primitives supported by evidence.
  - Add focused service tests.
  - Update implementation proof and governance artifacts.
- Acceptance Criteria:
  - Service imports no engine, domain, internal, external, or operations code.
  - Contracts remain implementation-free.
  - Public behavior of legacy engines remains unchanged.
  - Tests pass for the new service and relevant legacy smoke coverage.
- Definition of Done:
  - Event Bus reaches Stage 2.
  - Duplicate event infrastructure is reduced or clearly reclassified.
  - Rollback plan is documented.

### M-003: Storage Minimal Implementation Proof

- Stage: Stage 2 - Minimal Implementation
- Dependencies: M-002, Storage Contract, Event Bus boundary evidence
- Tasks:
  - Discover reusable persistence behavior in folded engines.
  - Inventory object metadata, transaction boundaries, version hooks, and repository abstractions.
  - Implement the smallest backend-neutral storage primitives supported by evidence.
  - Add focused service tests.
- Acceptance Criteria:
  - No concrete database or backend is selected.
  - Storage remains engine-independent.
  - Object references do not replace Asset identity or Evidence.
- Definition of Done:
  - Storage reaches Stage 2 with verification and rollback evidence.

### M-004: Configuration Minimal Implementation Proof

- Stage: Stage 2 - Minimal Implementation
- Dependencies: M-003, service dependency rules
- Tasks:
  - Discover reusable configuration loading, layering, defaults, validation, and redaction behavior.
  - Implement bounded, deterministic configuration primitives supported by evidence.
  - Add tests for precedence, validation, redaction, and failure paths.
- Acceptance Criteria:
  - Configuration stays separate from business logic.
  - No engine imports are introduced.
  - Secret values are not exposed in structured failures.
- Definition of Done:
  - Configuration reaches Stage 2 with verification and rollback evidence.

### M-005: Policy Minimal Implementation Proof

- Stage: Stage 2 - Minimal Implementation
- Dependencies: M-004, Policy and Permission contracts
- Tasks:
  - Discover reusable policy evaluation and rule execution behavior.
  - Separate policy decisions from permission ownership boundaries.
  - Implement the smallest contract-backed evaluator supported by evidence.
  - Add compatibility tests against legacy decisions where available.
- Acceptance Criteria:
  - Policy does not duplicate Permission language.
  - Policy service imports no engine code.
  - Decisions expose rule basis, uncertainty, and failure modes.
- Definition of Done:
  - Policy reaches Stage 2 with verification and rollback evidence.

### M-006: Identity Vertical Slice

- Stage: Stage 3 - Vertical Slice
- Dependencies: M-002 through M-005 as needed by the selected consumer
- Tasks:
  - Select one bounded consumer path that can use Identity without behavior drift.
  - Add adapter or integration only after compatibility proof.
  - Preserve legacy behavior and tests.
- Acceptance Criteria:
  - At least one consumer uses Identity through the service boundary.
  - No engine-specific identity ownership remains in the selected path.
- Definition of Done:
  - Identity reaches Stage 3 for one verified slice.


### RID-M-003: RID Model

- Stage: Stage 3 - RID Model
- Dependencies: RID-M-001 Identity Contracts, RID-M-002 Identity Service, Asset Model
- Tasks:
  - Define RID model as implementation planning.
  - Clarify namespace families, stability rules, merge/split semantics, and representation independence.
  - Define how RIDs relate to Assets, Observations, Evidence, Provenance, Representations, Relationships, and Events.
  - Identify validation requirements and failure modes for later implementation.
- Acceptance Criteria:
  - Identity ownership remains singular.
  - ARK remains a consumer of RID.
  - RID precedes Universal Asset Ingestion and full ARK implementation.
  - No implementation files change.
- Definition of Done:
  - RID model planning is documented.
  - Dependency graph is acyclic.
  - Maturity and roadmap tables are updated.


### UAI-M-001: Pipeline Contracts

- Stage: Stage 1 - Contracts
- Dependencies: RID-M-003 RID Model, Asset Model, Observation/Evidence/Provenance contracts
- Tasks:
  - Define universal ingestion pipeline contracts as planning evidence.
  - Classify acquisition, detection, canonicalization, normalization, chunking, identity, content addressing, extraction, and ARK integration boundaries.
  - Define media adapter boundaries and deprecate media-specific pipelines as architectural owners.
  - Preserve capability grammar without adding new architectural layers.
- Acceptance Criteria:
  - Universal ingestion precedes full ARK implementation.
  - Pipeline contracts are implementation-free.
  - Media adapters are the only media-specific implementation boundary.
  - No implementation files change.
- Definition of Done:
  - Dependency graph is acyclic.
  - Maturity and roadmap tables are updated.
  - ARK remains the consumer of universal ingestion output.

## Dependency Order

```text
Identity
  -> Reality ID (RID)
  -> Universal Asset Ingestion
  -> Event Bus
  -> Storage
  -> Configuration
  -> Policy
  -> Runtime Kernel
  -> ARK
  -> WEAVE
  -> Interpretation
  -> Reasoning
  -> Views
  -> Jarvis
  -> Capsules
  -> ZWLib
  -> Foundry
  -> NOMAD
  -> MIDAS
  -> MICE
  -> VALOR
  -> Blackwall
  -> NetWatch
```

## Verification Gates

Every milestone must verify:

- Constitution satisfied.
- Contracts satisfied.
- Tests pass or non-execution is justified.
- Ownership preserved.
- Dependency graph remains acyclic.
- No architectural drift introduced.
- Governance artifacts updated.
- Runtime behavior unchanged unless the milestone explicitly proves a behavior-preserving replacement.

## Recommended Next Task

RID-M-003: RID Model.

Reason: RID remains the immediate prerequisite. After RID-M-003, the next architecture prerequisite is UAI-M-001 Pipeline Contracts. Storage remains the next platform service proof after these planning milestones.
