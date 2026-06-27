# Roadmap

## Phase 1 - Constitutional Foundation

- Establish the master monorepo structure.
- Define canonical ownership for constitution, contracts, capabilities,
  services, engines, domains, applications, integrations, operations, tooling,
  documentation, and tests.
- Provide repository-folding rules for existing projects.

## Phase 2 - Contracts and Capabilities

- Promote shared language into contract definitions.
- Classify stable architectural verbs as capabilities.
- Add validator-ready schemas and interface documentation.

## Phase 3 - Services and Engines

- Extract reusable infrastructure into services.
- Fold unique responsibilities into canonical engine layouts.
- Enforce the engine lifecycle from ingress through egress.

## Phase 4 - Domains and Applications

- Compose engines into domain solutions.
- Connect internal applications to domains and engines through explicit
  contracts.

## Phase 5 - Operations

- Add deployment, observability, backup, disaster recovery, and migration
  workflows.
## Implementation Program

Constitution v1 is complete. Implementation now advances through evidence-backed milestones recorded in `docs/implementation-backlog.md`.

## Platform Progress

| Component | Stage | Status |
| --- | :---: | --- |
| Identity | 2 | ✅ |
| Event Bus | 2 | ✅ |
| Storage | 1 | 🔄 Next |
| Configuration | 1 | ⏳ |
| Policy | 1 | ⏳ |

| Order | Roadmap Item | Status |
| ---: | --- | --- |
| 1 | Identity Minimal Implementation Proof | ✅ Complete |
| 2 | Event Bus Minimal Implementation Proof | ✅ Complete |
| 3 | Storage Minimal Implementation Proof | 🔄 Next |
| 4 | Configuration Minimal Implementation Proof | ⏳ Waiting on Storage |
| 5 | Policy Minimal Implementation Proof | ⏳ Waiting on Configuration |

Current platform maturity:

- Identity Service: Stage 2 - Minimal Implementation.
- Event Bus Service: Stage 2 - Minimal Implementation.
- Storage, Configuration, Policy: Stage 1 - Contracts.
- Next recommended milestone: Storage Minimal Implementation Proof.

Implementation must follow dependency order, preserve contracts, update governance evidence, and stop after each completed milestone for review.
## Infrastructure Program

The separate `wayfinder-infra` repository will implement deployment of the Wayfinder platform. It owns Docker Compose, host layout, operations, monitoring, backups, recovery, and environment configuration. It does not own Constitution, contracts, platform services, engine behavior, or application logic.

Planning lives in `docs/wayfinder-infra-program.md`. The recommended first infrastructure milestone is M-001 Repository Scaffold. No Docker implementation begins until that separate repository scaffold is created and reviewed.
## Repository Portfolio

The Wayfinder repository portfolio is tracked in `docs/wayfinder-portfolio.md`. `wayfinder` remains active as the platform repository. Planned repositories include `wayfinder-infra`, `wayfinder-home`, `wayfinder-build-bible`, `wayfinder-living-map`, `wayfinder-family`, `wayfinder-homestead`, and `wayfinder-cookbook`. Each planned repository must define purpose, owner, dependencies, maturity, next milestone, roadmap, and backlog before implementation.
## Reality Identity Program

Reality Identity (RID) is now tracked as a first-class implementation program in `docs/reality-identity-program.md`. RID is the universal continuity anchor for Wayfinder. The Constitution defines RID semantics, the Identity Service implements reusable identity capability, and ARK consumes RID.

RID implementation dependency order:

```text
Identity Service
  -> Reality ID (RID)
  -> Universal Asset Ingestion
  -> Runtime Kernel
  -> ARK
```

RID program status:

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

Recommended RID milestone: RID-M-003 RID Model.
## Universal Asset Ingestion Program

Universal Asset Ingestion is tracked as a first-class implementation program in `docs/universal-asset-ingestion-program.md`. It is the reusable ingestion foundation for every asset type and becomes the canonical ingestion model for ARK. Media-specific pipelines are deprecated as architectural owners; media adapters remain valid implementation boundaries.

Universal ingestion dependency order:

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

Universal ingestion status:

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

Recommended universal ingestion milestone: UAI-M-001 Pipeline Contracts after RID-M-003 RID Model.
## Program Governance

Implementation program governance lives in `docs/programs/`. The program index lists active and planned programs, the portfolio dashboard summarizes maturity and blockers, the cross-program dependency graph tracks program-level prerequisites, and the release plan maps milestones to target releases.

