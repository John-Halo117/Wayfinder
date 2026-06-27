# Program Portfolio Dashboard

Date: 2026-06-27

This dashboard answers: where is the project right now?


## Planning Stack

```text
Repository -> Programs -> Roadmaps -> Milestones -> Backlog
```

Each program reports purpose, dependencies, maturity, milestones, current status, and success criteria through the program index.

## At A Glance

| Program | Maturity | Progress | Blockers | Next Milestone |
| --- | --- | --- | --- | --- |
| Platform Substrate | Stage 2 partial | Identity and Event Bus complete; Storage/Configuration/Policy pending | RID/UAI planning now precedes ARK, but service proofs remain valid | Storage Minimal Implementation Proof after planning gates |
| Reality Identity (RID) | Stage 2 planning foundation | Identity contracts and service proof complete | RID model not yet specified | RID-M-003 RID Model |
| Universal Asset Ingestion | Stage 0 program | Program, capabilities, roadmap, and backlog documented | Waiting on RID model | UAI-M-001 Pipeline Contracts |
| Runtime Kernel | Stage 0 implied | Named in dependency order only | Waiting on UAI and platform service maturity | Runtime Kernel Program |
| ARK Implementation | Stage 1 folded/contracts | Folded, inventoried, contract consumers known | Waiting on RID, UAI, runtime kernel, and platform services | ARK integration planning |
| Engine Chain | Stage 0-1 mixed | Engine boundaries exist | Waiting on ARK foundation | WEAVE boundary refinement |
| Infrastructure Repository | Stage 0 program | Program documented | Repository not scaffolded | Infra M-001 Repository Scaffold |
| Repository Portfolio | Stage 0 program | Portfolio doc exists | Planned repos not scaffolded | `wayfinder-infra` scaffold |

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
| RID Model | 2 | 🔄 Next |
| Universal Asset Ingestion | 0 | ⏳ |
| Runtime Kernel | 0 | ⏳ |
| ARK Integration | 1 | ⏳ |
| WEAVE | 0 | ⏳ |
| Interpretation | 0 | ⏳ |
| Reasoning | 0 | ⏳ |
| Views | 1 | ⏳ |
| Jarvis | 1 | ⏳ |

## Current Decision

The next architecture-planning milestone is `RID-M-003 RID Model`.

The next platform-service implementation milestone remains Storage, but it should follow the RID/UAI planning gates now recorded in the roadmap.

## Active Blockers

| Blocker | Blocks | Resolution |
| --- | --- | --- |
| RID model not specified | UAI pipeline contracts, full ARK implementation | Complete RID-M-003 |
| UAI pipeline contracts not specified | Runtime Kernel and ARK ingestion | Complete UAI-M-001 after RID-M-003 |
| Storage implementation proof not complete | Configuration, Policy, durable platform substrate | Complete Storage Minimal Implementation Proof |
| Runtime Kernel not defined | ARK implementation sequence | Create Runtime Kernel program after UAI planning |
| `wayfinder-infra` not scaffolded | Deployment implementation | Create infrastructure repository scaffold |

## Next Three Moves

| Order | Milestone | Type | Why |
| ---: | --- | --- | --- |
| 1 | RID-M-003 RID Model | Planning | Stabilizes the continuity anchor before ingestion and ARK. |
| 2 | UAI-M-001 Pipeline Contracts | Planning | Establishes universal ingestion before media adapters or ARK ingestion. |
| 3 | Storage Minimal Implementation Proof | Implementation | Completes the next platform substrate service after planning gates. |
