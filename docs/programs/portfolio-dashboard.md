# Program Portfolio Dashboard

Date: 2026-06-27

This dashboard answers: where is the project right now? The canonical control table is `docs/programs/program-registry.md`.


## Planning Stack

```text
Repository -> Programs -> Roadmaps -> Milestones -> Backlog
```

Each program reports purpose, dependencies, maturity, milestones, current status, and success criteria through the program index.

## At A Glance

| Program | Current Stage | Completion % | Blockers | Current Milestone | Next Milestone | Verification State |
| --- | --- | ---: | --- | --- | --- | --- |
| Platform Substrate | Stage 2 partial | 40% | Storage/Configuration/Policy pending; planning gates before ARK | Storage Minimal Implementation Proof | Configuration Minimal Implementation Proof | Partial: Identity/Event Bus verified |
| Reality Identity (RID) | Stage 3 model | 35% | Domain identifier details remain | RID-M-004 Domain Identifiers | RID-M-005 Identity Encoding | Partial: RID-M-003 verified as planning |
| Universal Asset Ingestion | Stage 1 contracts | 20% | Acquisition boundary not planned | UAI-M-002 Acquisition | UAI-M-003 Format Detection | Pipeline contracts verified |
| Runtime Kernel | Stage 0 implied | 0% | Waiting on UAI and platform service maturity | Program definition | Runtime Kernel milestones | Not started |
| ARK Implementation | Stage 1 folded/contracts | 15% | Waiting on RID, UAI, Runtime Kernel, and platform services | ARK consumer planning | ARK integration plan | Fold/inventory verified; implementation pending |
| Engine Chain | Stage 0-1 mixed | 5% | Waiting on ARK foundation | WEAVE boundary refinement | Interpretation planning | Engine stubs verified; program pending |
| Digital Groundskeeper | Stage 1 contracts | 40% | Approval boundary not specified | DG-M-005 Approval Boundary | DG-M-006 Quarantine and Archive Plan | Observation, inventory, and recommendation contracts verified |
| Infrastructure Repository | Stage 0 program | 10% | Repository not scaffolded | Infra M-001 Repository Scaffold | Shared Infrastructure | Planning verified |
| Repository Portfolio | Stage 0 program | 10% | Planned repos not scaffolded | Portfolio repository programs | First domain repository program | Planning verified |

## Platform Service Progress

| Component | Stage | Status |
| --- | :---: | --- |
| Identity | 2 | ✅ |
| Event Bus | 2 | ✅ |
| Storage | 1 | 🔄 Next |
| Configuration | 1 | ⏳ |
| Policy | 1 | ⏳ |

## Architecture Prerequisite Progress

| Component | Stage | Status |
| --- | :---: | --- |
| RID Model | 3 | ✅ |
| Universal Asset Ingestion | 1 | ✅ |
| Runtime Kernel | 0 | ⏳ |
| ARK Integration | 1 | ⏳ |
| Digital Groundskeeper | 1 | ✅ |
| WEAVE | 0 | ⏳ |
| Interpretation | 0 | ⏳ |
| Reasoning | 0 | ⏳ |
| Views | 1 | ⏳ |
| Jarvis | 1 | ⏳ |

## Current Decision

The next architecture-planning milestone is `UAI-M-002 Acquisition`.

The next platform-service implementation milestone remains Storage, but it should follow the RID/UAI planning gates now recorded in the roadmap.

## Active Blockers

| Blocker | Blocks | Resolution |
| --- | --- | --- |
| Acquisition boundary not planned | Runtime Kernel and ARK ingestion | Complete UAI-M-002 |
| Storage implementation proof not complete | Configuration, Policy, durable platform substrate | Complete Storage Minimal Implementation Proof |
| Runtime Kernel not defined | ARK implementation sequence | Create Runtime Kernel program after UAI planning |
| Digital Groundskeeper approval boundary not specified | Observe-first digital maintenance | Complete DG-M-005 |
| `wayfinder-infra` not scaffolded | Deployment implementation | Create infrastructure repository scaffold |

## Next Three Moves

| Order | Milestone | Type | Why |
| ---: | --- | --- | --- |
| 1 | UAI-M-002 Acquisition | Planning | Applies the canonical pipeline contracts to the first ingestion stage without media adapter implementation. |
| 2 | Storage Minimal Implementation Proof | Implementation | Completes the next platform substrate service after planning gates. |
| 3 | RID-M-004 Domain Identifiers | Planning | Deepens identifier-family detail after the RID model. |
| 4 | DG-M-005 Approval Boundary | Planning | Defines explicit approval requirements before quarantine, archive, or execution planning. |
