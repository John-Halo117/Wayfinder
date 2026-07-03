# Implementation Program Index

Date: 2026-06-27

This is the entry point for Wayfinder implementation programs. Programs coordinate implementation work; they do not replace the Constitution, Canon, Contracts, Services, Engines, or governance records.


## Program Hierarchy

```text
Repository
  -> Programs
      -> Platform Services
      -> Reality Identity
      -> Universal Asset Ingestion
      -> Runtime Kernel
      -> ARK
      -> Digital Groundskeeper
      -> WEAVE
      -> Interpretation
      -> Reasoning
      -> Views
      -> Jarvis
      -> ...
  -> Roadmaps
  -> Milestones
  -> Backlog
```

The repository owns the evidence surface. Programs own coordinated implementation tracks. Roadmaps order each program's work. Milestones define bounded increments. Backlog items hold executable tasks and acceptance criteria.

## Program Ownership Model

Each program owns:

| Field | Meaning |
| --- | --- |
| Purpose | Why the program exists and what implementation responsibility it coordinates. |
| Dependencies | Programs, contracts, services, engines, or docs that must precede it. |
| Maturity | Current implementation stage and evidence required for the next stage. |
| Milestones | Ordered, bounded increments with acceptance criteria. |
| Current Status | Active, planned, blocked, complete, or not started. |
| Success Criteria | Conditions that prove the program improved Wayfinder without architectural drift. |
| Roadmap | Ordered milestone sequence. |
| Backlog | Concrete tasks, acceptance criteria, definitions of done, and verification requirements. |

A program does not own constitutional definitions unless its canonical owner is already in the Constitution. Program docs coordinate implementation; they do not become architecture.

## Program Portfolio

| Program | Purpose | Status | Dependencies | Current Milestone | Owner | Success Criteria | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Platform Substrate | Promote reusable services consumed by future engines. | Active | Constitution, Contracts | Storage Minimal Implementation Proof, paused behind RID/UAI planning | Wayfinder Platform | Foundational services reach Stage 2 without forbidden dependencies. | `docs/implementation-backlog.md` |
| Reality Identity (RID) | Implement the constitutional identity model and continuity anchor. | Active | Identity Service, Asset Model | RID-M-004 Domain Identifiers | Identity Service / Constitution | RID is stable, representation-independent, evidence-bound, and consumed by ARK. | `docs/reality-identity-program.md`, `docs/reality-identity-model.md` |
| Universal Asset Ingestion | Plan the reusable ingestion foundation for every asset type. | Active | RID Program, Asset Model, ARK boundary | UAI-M-002 Acquisition | ARK / Platform | Universal ingestion replaces media-specific pipeline ownership with adapters. | `docs/universal-asset-ingestion-program.md`, `contracts/ingestion/README.md` |
| Runtime Kernel | Define runtime execution substrate after RID and ingestion planning. | Not started | UAI, Platform Services | Program definition | Wayfinder Platform | Runtime execution supports platform services without owning engine behavior. | `docs/implementation-backlog.md` |
| ARK Implementation | Rebuild reality preservation on platform services and universal ingestion. | Not started | Runtime Kernel, UAI, RID, Storage, Event Bus, Identity | ARK consumer planning | ARK | ARK preserves observations/evidence/provenance without owning shared infrastructure. | `engines/ark/README.md` |
| Engine Chain | Advance WEAVE through Jarvis after ARK foundations are stable. | Not started | ARK | WEAVE boundary refinement | Engine owners | Derived engines consume upstream contracts and preserve single responsibility. | `engines/README.md` |
| Digital Groundskeeper | Preserve digital system capability, continuity, attention, and maneuverability through observe-first maintenance. | Planned | Asset Model, UAI, ARK, Storage, Policy | DG-M-005 Approval Boundary | Operations / Platform | Digital maintenance remains evidence-based, reversible, approval-gated, and capability-centered. | `docs/digital-groundskeeper-program.md`, `contracts/digital-groundskeeper-observation-reports/README.md`, `contracts/digital-groundskeeper-inventories/README.md`, `contracts/digital-groundskeeper-recommendations/README.md` |
| Infrastructure Repository | Plan deployment implementation in `wayfinder-infra`. | Planned | Platform boundaries | Infra M-001 Repository Scaffold | Operations / Infrastructure | Deployment remains replaceable and contains no platform logic. | `docs/wayfinder-infra-program.md` |
| Repository Portfolio | Track related repositories and domain programs. | Planned | Wayfinder Platform | Portfolio repository programs | Wayfinder Portfolio | Planned repos have purpose, owner, dependencies, roadmap, and backlog before implementation. | `docs/wayfinder-portfolio.md` |

## Navigation

- Program registry: `docs/programs/program-registry.md`
- Program lifecycle: `docs/programs/program-lifecycle.md`
- Program template: `docs/programs/program-template.md`
- Program governance verification: `docs/programs/verification-report.md`
- Program dashboard: `docs/programs/portfolio-dashboard.md`
- Cross-program dependency graph: `docs/programs/dependency-graph.md`
- Release plan: `docs/programs/release-plan.md`
- Platform backlog: `docs/implementation-backlog.md`
- RID program: `docs/reality-identity-program.md`
- Universal ingestion program: `docs/universal-asset-ingestion-program.md`
- Infrastructure program: `docs/wayfinder-infra-program.md`
- Repository portfolio: `docs/wayfinder-portfolio.md`

## Program Rules

- Every milestone completion must synchronize the backlog, dashboard, registry, release plan, promotion registry when relevant, and scorecard when affected.
- Every program must declare purpose, dependencies, maturity, milestones, current status, success criteria, roadmap, and backlog before implementation begins.
- Programs may plan work, maturity, milestones, blockers, and releases.
- Programs must not duplicate constitutional definitions.
- If a program changes ownership, contracts, or dependency order, governance docs must be updated.
- Implementation milestones must stop after completion for verification and review.
