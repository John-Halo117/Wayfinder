# Program Registry

Date: 2026-06-27

The Program Registry is the canonical implementation-program control table. Every long-lived implementation program appears exactly once here.

## Evidence Summary

| Evidence | Finding |
| --- | --- |
| `ROADMAP.md` | Lists Platform, RID, UAI, Infrastructure, Portfolio, and program governance references. |
| `docs/implementation-backlog.md` | Tracks platform, RID, and UAI maturity, milestones, dependency order, and next work. |
| `docs/programs/` | Contains index, dashboard, dependency graph, release plan, and now registry/lifecycle/template/verification. |
| `docs/migration-dashboard.md` | Tracks engine and implementation proof status plus RID/UAI program status. |
| `docs/promotion-registry.md` | Tracks promoted concepts and implementation proofs; program milestones must update this when promotion occurs. |
| `docs/constitutional-scorecard.md` | Tracks governance and implementation-program health metrics. |

## Registry

| Program | Purpose | Repository | Status | Current Milestone | Current Stage | Dependencies | Downstream Consumers | Completion % | Next Recommended Work | Verification Status |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| Platform Substrate | Promote reusable services consumed by future engines. | `wayfinder` | Active | Storage Minimal Implementation Proof | Stage 2 partial | Constitution, Contracts | RID, UAI, Runtime Kernel, ARK, all engines | 40% | Complete Storage Stage 2 proof after active planning gates. | Partial: Identity/Event Bus verified; remaining services pending. |
| Reality Identity (RID) | Implement the constitutional identity model and continuity anchor. | `wayfinder` | Active | RID-M-004 Domain Identifiers | Stage 3 model | Identity Service, Asset Model | UAI, Runtime Kernel, ARK, domains | 35% | Specify domain identifier families. | Partial: RID-M-003 documented; implementation not changed. |
| Universal Asset Ingestion | Plan reusable ingestion foundation for every asset type. | `wayfinder` | Active | UAI-M-002 Acquisition | Stage 1 contracts | RID, Asset Model, ARK boundary | Runtime Kernel, ARK, WEAVE, Interpretation | 20% | Plan acquisition against the canonical pipeline contracts. | Pipeline contracts verified; acquisition pending. |
| Runtime Kernel | Define runtime execution substrate after RID and ingestion. | `wayfinder` | Proposed | Program definition | Stage 0 implied | UAI, Platform Services | ARK, engines, internal apps | 0% | Create Runtime Kernel program after UAI contracts. | Not started. |
| ARK Implementation | Rebuild reality preservation on platform services and UAI. | `wayfinder` | Planned | ARK consumer planning | Stage 1 folded/contracts | Runtime Kernel, UAI, RID, Storage, Event Bus, Identity | WEAVE, Interpretation, Reasoning, Views, Jarvis, domains | 15% | Wait for RID/UAI/runtime gates; then plan ARK integration. | Fold/inventory verified; implementation pending. |
| Engine Chain | Advance WEAVE through Jarvis after ARK foundations. | `wayfinder` | Proposed | WEAVE boundary refinement | Stage 0-1 mixed | ARK | Capsules, ZWLib, Foundry, NOMAD, MIDAS, MICE, VALOR, Blackwall, NetWatch | 5% | Defer until ARK foundation. | Engine stubs verified; program not started. |
| Digital Groundskeeper | Preserve digital system capability, continuity, attention, and maneuverability through observe-first maintenance. | `wayfinder` | Planned | DG-M-005 Approval Boundary | Stage 1 contracts | Asset Model, UAI, ARK, Storage, Policy | Operators, Operations, ARK observation ingestion, domain repositories | 40% | Define approval boundary contract. | Observation, inventory, and recommendation contracts verified; approval boundary pending. |
| Infrastructure Repository | Plan deployment implementation in `wayfinder-infra`. | `wayfinder-infra` | Planned | Infra M-001 Repository Scaffold | Stage 0 program | Platform boundaries | Operators, deployment, ARK observation surfaces | 10% | Scaffold `wayfinder-infra` repository. | Planning verified; repo not scaffolded. |
| Repository Portfolio | Track related repositories and domain programs. | Portfolio | Planned | Portfolio repository programs | Stage 0 program | Wayfinder Platform | Planned domain and infra repos | 10% | Scaffold first planned repository program. | Planning verified; repos not scaffolded. |

## Lifecycle

All programs follow the lifecycle defined in `docs/programs/program-lifecycle.md`.

```text
Proposed -> Planned -> Active -> Implementing -> Verified -> Promoted -> Operational -> Maintenance
```

## Synchronization Requirement

When a milestone completes, update this registry before considering the milestone done.
