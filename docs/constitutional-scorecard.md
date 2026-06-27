# Constitutional Scorecard

The constitutional scorecard measures whether Wayfinder remains aligned with
its architecture as it grows.

This document defines metrics. It does not implement measurement.

## Scorecard Inputs

- `WAYFINDER.md`
- `constitution/`
- `contracts/`
- `services/`
- `engines/`
- `domains/`
- `docs/ownership-matrix.md`
- `docs/constitutional-census.md`
- Engine dependency graphs
- Promotion registry
- Architectural debt register

## Metrics

| Metric | Definition | Target | Evidence Source |
| --- | --- | ---: | --- |
| Canonical Ownership Coverage | Percentage of known concepts with exactly one canonical owner. | 100% | Ownership matrix, census |
| Duplicate Concept Count | Count of concepts with multiple active owners or competing implementations. | 0 | Census, debt register |
| Service Reuse Ratio | Shared infrastructure concepts consumed through services instead of engines. | Increasing | Census, dependency rules |
| Engine Cohesion | Percentage of engine concepts that support the engine's single responsibility. | 100% | Engine READMEs, census |
| Contract Purity | Percentage of contract files containing language only, with no implementation. | 100% | Contracts, linter |
| Dependency Violations | Count of forbidden architecture-layer dependencies. | 0 | Dependency rules, linter |
| Circular Dependencies | Count of dependency cycles across architectural layers. | 0 | Dependency graph, linter |
| Architectural Confidence | Distribution of concept confidence levels in the census. | High increasing | Census |
| Promotion Coverage | Percentage of promoted concepts with registry entries. | 100% | Promotion registry |
| Proof Coverage | Percentage of promotions with documented proof evidence. | 100% | Promotion registry |
| Rollback Coverage | Percentage of promotions with rollback path. | 100% | Promotion registry |
| Debt Visibility | Percentage of known exceptions recorded in the debt register. | 100% | Debt register |
| Legacy Isolation | Percentage of legacy code confined to `legacy/` or documented compatibility homes. | 100% | Engine trees, debt register |

## Scoring Bands

| Band | Score | Meaning |
| --- | ---: | --- |
| Constitutional | 95-100 | Architecture is measurable, owned, and proof-backed. |
| Stable | 85-94 | Architecture is healthy with visible bounded debt. |
| Watch | 70-84 | Drift risk exists; promotion should slow until debt is reduced. |
| At Risk | 50-69 | Canonical ownership or dependency direction is unreliable. |
| Unconstitutional | 0-49 | Architecture cannot safely absorb more migration. |

## Current Baseline

| Area | Baseline Status | Notes |
| --- | --- | --- |
| Ownership Matrix | Partial | Platform substrate, Foundry ownership, Observation, and Wave 1 core contract ownership are recorded. |
| Census | Present | ARK, Foundry, and Jarvis have concept-level census evidence. |
| Promotion Registry | Active | Twenty promotions have registry entries, including all Wave 1 core language contracts. |
| Debt Register | Created baseline | Known debts are visible; DEBT-011 is reduced by Wave 1 core language promotion; runtime/action gaps remain deferred. |
| Dependency Rules | Defined | Enforcement is specified but not implemented. |
| Linter | Specified | Implementation is deferred by design. |

## Measurement Cadence

Run this scorecard:

- Before promoting any concept.
- After adding a service, engine, domain, integration, or internal app.
- Before merging a major migration branch.
- After resolving architectural debt.

## Wave 2 Scorecard Update

| Metric | Status After Wave 2 | Evidence |
| --- | --- | --- |
| Promoted service owners | 5 foundational service owners established | Identity, Event Bus, Storage, Configuration, Policy |
| Runtime behavior preservation | Pass | No engine code moved or rewired |
| Service dependency compliance | Pass | Service scaffolds document Constitution/Contracts-only dependencies |
| Contract purity | Pass | No contract executable code added |
| Duplicate concepts | Reduced, not eliminated | Canonical owners exist; legacy implementations remain visible debt |
| Promotion coverage | Improved | Five promotion reports and one Wave 2 verification report added |
| Proof coverage | Scaffold-level proof complete | Implementation extraction requires future compatibility tests |

## Phase 4 Identity Implementation Scorecard

| Metric | Status | Evidence |
| --- | --- | --- |
| One implementation promoted | Pass | Identity only |
| Behavior preserved | Pass | No engine files changed; legacy smoke test passed |
| Service independence | Pass | Service implementation imports standard library only |
| Contract purity | Pass | No contract code added |
| Duplicate implementation reduced | Partial pass | Reusable identity mechanics now have canonical implementation; engine adapters remain deferred |
| Proof coverage | Pass | Service tests and legacy smoke test recorded |
## Constitution v1 Finalization

| Area | Status | Evidence |
| --- | --- | --- |
| Language | Pass | Contract language normalized to common Producer template. |
| Observation/Context cycle | Pass | Context no longer requires Observation for identity; Observation may reference Context. |
| Asset ownership | Pass | Asset model ownership is separated from ARK production of durable asset knowledge. |
| Capability grammar | Pass | `capabilities/` owns grammar; NOMAD owns availability discovery. |
| Governance drift | Pass | Debt, census, ownership matrix, and promotion registry wording updated for Identity, Policy, Configuration, and Wave 2 services. |
| Release readiness | Pass | `docs/constitution-v1-release-audit.md` records no Critical or Major issues. |
## Implementation Program Scorecard

| Metric | Status | Evidence |
| --- | --- | --- |
| Backlog visibility | Pass | `docs/implementation-backlog.md` defines stages, milestones, acceptance criteria, and definitions of done. |
| Dependency order | Pass | Backlog records platform-to-engine implementation order. |
| Current maturity | Pass | Backlog records Identity at Stage 2 and remaining foundational services at Stage 1. |
| Next task clarity | Pass | Event Bus Minimal Implementation Proof is the recommended next milestone. |
## M-002 Event Bus Implementation Scorecard

| Metric | Status | Evidence |
| --- | --- | --- |
| One implementation promoted | Pass | Event Bus only |
| Behavior preserved | Pass | No engine files changed; legacy event and subject smoke tests passed |
| Service independence | Pass | Event Bus implementation imports standard library only |
| Contract purity | Pass | No contract executable code added |
| Duplicate implementation reduced | Partial pass | Reusable event envelope, route matching, publish/subscribe, and replay mechanics now have canonical implementation; engine adapters remain deferred |
| Proof coverage | Pass | Service tests and legacy smoke tests recorded |

