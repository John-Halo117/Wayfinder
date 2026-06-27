# Migration Dashboard

This dashboard summarizes current migration status by engine.

It is evidence for planning. It does not move code.

## Status Legend

| Status | Meaning |
| --- | --- |
| Folded | Historical source is preserved in Wayfinder. |
| Inventoried | Files and concepts have classification evidence. |
| Census Complete | Concepts have ownership, dependency, duplication, and confidence evidence. |
| Promotion Ready | Next promotion candidate has enough evidence for a proof-backed promotion. |
| Blocked | Needs discovery, proof, or boundary decision. |

## Engines

| Engine | Inventory | Migration Status | Concepts Promoted | Concepts Remaining | Architectural Confidence | Outstanding Debt | Next Promotion Candidate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ARK | Complete Phase 1 inventory in `engines/ark/docs/inventory.md` | Folded, inventoried, census complete | Reality Preservation owner established; Wave 1 language contracts promoted; Wave 2 platform service scaffolds promoted | Policy implementation adapters, configuration implementation adapters, telemetry implementation, discovery, operations, external adapters | Medium-High | DEBT-001, DEBT-003 through DEBT-005, DEBT-008 through DEBT-012 | Telemetry service inventory |
| Foundry | Forge-origin file list in `engines/foundry/docs/ark-forge-normalization.md` | Folded, census complete, needs dedicated inventory | Foundry canonical owner established; Wave 2 platform service scaffolds promoted | Runtime rename proof, UI/app boundary, model adapters, MCP boundary, artifact storage adapters | Medium | DEBT-002 plus reduced Wave 2 implementation debt | Dedicated Foundry inventory |
| Jarvis | Minimal fold record in `engines/jarvis/docs/folding.md` | Folded, census complete, needs deeper source inventory | Navigation owner established | Bearings contracts, route candidates, navigation proofs, smart-home domain boundary | Medium-Low | DEBT-009, external integration overlap | Bearings contract and Jarvis source inventory |

## Cross-Engine Promotion Queue

| Priority | Candidate | Proposed Owner | Reason | Blocking Debt |
| --- | --- | --- | --- | --- |
| 1 | Telemetry Service Inventory | `services/telemetry/` | Health language is promoted; implementation remains in ARK/operations. | DEBT-008 |
| 2 | Discovery Boundary | `services/discovery/`, `engines/jarvis/` | Must distinguish capability registry from navigation. | DEBT-009 |
| 3 | Runtime and Action Contracts | `contracts/runtime/`, `contracts/actions/` | Remaining contract gaps outside Wave 1 core noun scope. | DEBT-011 |
| 4 | Policy Implementation Adapter Proof | `services/policy/` | Service owner is promoted; legacy evaluators remain local pending compatibility proof. | Reduced DEBT-006 |
| 5 | Configuration Implementation Adapter Proof | `services/configuration/` | Service owner is promoted; legacy loaders remain local pending precedence/redaction proof. | Reduced DEBT-007 |

## Dashboard Health

| Measure | Current State |
| --- | --- |
| Folded engines | 3 |
| Engines with census coverage | 3 |
| Engines with full inventory | 1 |
| Engines with dedicated normalization record | 2 |
| Formal promoted concepts | 25 |
| Open architectural debts | 10 open, 2 resolved, 3 reduced by Wave 2 |
| Linter implementation | Not implemented by design |

## Wave 2 Platform Substrate Status

| Service | Status | Concepts Promoted | Remaining Debt | Next Proof |
| --- | --- | --- | --- | --- |
| Identity | Promoted scaffold | RID generation, aliases, namespaces, lookup, merge semantics | Legacy ARK subject implementations still local | Compatibility tests before adapter extraction |
| Event Bus | Promoted scaffold | publish, subscribe, routing, correlation, replay boundary | ARK GSB/transport/WAL still local | Transport-agnostic interface proof |
| Storage | Promoted scaffold | persistence abstraction, object metadata, transactions, versioning hooks | ARK DuckDB/Rust/Redis state still local | Backend-neutral repository proof |
| Configuration | Promoted scaffold | loading, layered config, env abstraction, defaults, validation | ARK/Foundry/Jarvis config loaders still local | Layer precedence and redaction proof |
| Policy | Promoted scaffold | evaluation, rule execution, authorization/promotion/architecture policy references | ARK and Foundry policy evaluators still local | Contract tests against legacy decisions |

Wave 2 stopped after the five requested foundational services. Search, Discovery, Logging, Telemetry, Scheduling, Compression, and Notifications remain later-wave candidates.

## Phase 4 Implementation Proof Status

| Service | Implementation Status | Verification | Remaining Debt | Stop Point |
| --- | --- | --- | --- | --- |
| Identity | One reusable implementation promoted | 8 service tests passed; 26 legacy smoke tests passed | Engine consumers are not rewired; ARK subject routing belongs to Event Bus | Stop after Identity pending approval |
| Event Bus | Not started | Not run | Legacy routing/transport implementation remains | Await approval |
| Storage | Not started | Not run | Legacy persistence implementation remains | Await approval |
| Configuration | Not started | Not run | Legacy config loader implementation remains | Await approval |
| Policy | Not started | Not run | Legacy policy evaluators remain | Await approval |

