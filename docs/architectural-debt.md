# Architectural Debt Register

Architectural debt is any known constitutional exception, compatibility shim,
duplicate ownership, deferred promotion, or legacy structure that must remain
visible until resolved.

Debt is acceptable only when it is named, bounded, owned, and tracked.

## Debt Schema

| Field | Meaning |
| --- | --- |
| ID | Stable debt identifier. |
| Type | Duplicate ownership, temporary exception, compatibility shim, legacy code, or deferred promotion. |
| Description | What is constitutionally imperfect. |
| Current Location | Where the debt exists today. |
| Canonical Target | Intended owner or resolution. |
| Risk | Low, Medium, or High. |
| Resolution Trigger | Evidence required before resolving. |
| Status | Open, Watching, or Resolved. |

## Register

| ID | Type | Description | Current Location | Canonical Target | Risk | Resolution Trigger | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DEBT-001 | Legacy code | ARK historical source remains under legacy while concepts are classified. | `engines/ark/legacy/` | Classified contracts, services, and ARK engine layers | Medium | Contract/service extraction proofs pass. | Open |
| DEBT-002 | Compatibility shim | Forge-origin executable names are preserved under Foundry. | `engines/foundry/legacy/` | `engines/foundry/` with compatibility aliases | Medium | Runtime aliases and behavior parity are proven. | Open |
| DEBT-003 | Duplicate ownership | Event contracts and event bus behavior appear in several ARK modules. Minimal reusable event mechanics are now promoted; broker transport and engine adapters remain legacy debt. | ARK legacy event schemas, GSB, NATS, WAL, transport | `contracts/events/`, `services/event-bus/` | High | Event bus consumer adapters and broker boundary proof pass. | Reduced |
| DEBT-004 | Duplicate ownership | Storage concepts appear in DuckDB, Redis state, Rust storage, and state docs. | ARK legacy storage files | `services/storage/` | High | Storage interface and adapter proof passes. | Open |
| DEBT-005 | Duplicate ownership | Identity concepts appeared beside ARK subject routing and policy rules; routing subjects are now classified as Event Bus debt. | ARK legacy identity evidence, subject routing, and policy rules | `services/identity/`, `contracts/identities/`, with subject routing under `services/event-bus/` | High | Engine adapters prove identity behavior while routing remains Event Bus-owned. | Reduced |
| DEBT-006 | Deferred implementation | Policy service ownership and scaffold exist; implementation adapters remain deferred. | ARK policy files, MCP policy, epistemic policy | `services/policy/`, `contracts/policies/` | High | Policy adapter extraction preserves behavior. | Reduced |
| DEBT-007 | Deferred implementation | Configuration service ownership and scaffold exist; loader extraction remains deferred. | ARK config/env/manifests, Jarvis env, Foundry config | `services/configuration/` | Medium | Loader extraction and precedence tests preserve behavior. | Reduced |
| DEBT-008 | Deferred promotion | Telemetry and health contracts are identified but not scaffolded. | ARK health schema, OTel, Prometheus, health docs | `services/telemetry/`, `contracts/health/` | Medium | Health contract and probe boundary proof completed. | Open |
| DEBT-009 | Boundary ambiguity | ARK capability mesh routing overlaps with Jarvis navigation concepts. | ARK mesh registry, Jarvis route language | `services/discovery/` and `engines/jarvis/` | Medium | Boundary decision and dependency proof completed. | Open |
| DEBT-010 | Engine candidates | MIDAS, VALOR, NetWatch, and Stability exist inside ARK legacy. | `engines/ark/legacy/internal/` and `cmd/` | Future canonical engines after inventory | Medium | Dedicated engine inventories completed. | Open |
| DEBT-011 | Contract gaps | Wave 1 core language contracts are promoted. Runtime and external action contract gaps remain outside Wave 1 scope. | ARK legacy and census | `contracts/*` | Medium | Runtime and action contract purity docs are created in a later wave. | Open, reduced by Wave 1 on 2026-06-27 |
| DEBT-012 | Operations coupling | Docker, compose, deployment, Traefik, Authelia, and monitoring live in ARK legacy. | `engines/ark/legacy/` | `operations/ark/` | Medium | Operations inventory and deployment parity proof completed. | Open |

## Wave 2 Debt Update

| Debt ID | Concept | Previous Status | Wave 2 Status | Remaining Debt |
| --- | --- | --- | --- | --- |
| DEBT-003 | Event Bus duplication | Open | Reduced 2026-06-27; canonical owner promoted | ARK transport, GSB, and WAL implementations still local |
| DEBT-004 | Storage duplication | Open | Reduced 2026-06-27; canonical owner promoted | ARK DuckDB, Rust storage, and Redis adapters still local |
| DEBT-005 | Identity and subject-routing split | Open | Reduced 2026-06-27; Identity owner promoted and subject routing reclassified | Identity adapters remain unwired; ARK subject routing remains Event Bus debt |
| DEBT-006 | Policy service implementation | Open | Ownership/scaffold resolved 2026-06-27 | Implementation adapters and compatibility tests deferred |
| DEBT-007 | Configuration service implementation | Open | Ownership/scaffold resolved 2026-06-27 | Loader extraction and precedence tests deferred |

## Phase 4 Identity Debt Update

| Debt ID | Concept | Previous Status | Phase 4 Status | Remaining Debt |
| --- | --- | --- | --- | --- |
| DEBT-005 | Identity implementation duplication | Reduced by Wave 2 ownership promotion | Further reduced 2026-06-27; reusable identity implementation promoted | ARK subject routing is Event Bus debt; identity engine adapters not yet wired |
## M-002 Event Bus Debt Update

| Debt ID | Concept | Previous Status | M-002 Status | Remaining Debt |
| --- | --- | --- | --- | --- |
| DEBT-003 | Event Bus duplication | Reduced by Wave 2 ownership promotion | Further reduced 2026-06-27; reusable transport-neutral Event Bus implementation promoted | ARK broker transport, GSB/WAL adapters, and engine consumers are not yet rewired |

## First Contact Debt Update

These entries come from First Contact validation and Phase 8B evidence
assimilation. None are silently closed by Phase 8C.

| ID | Priority | Owner | Evidence | Impact | Dependencies | Suggested repayment | Migration path | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FC-DEBT-001 | High | Contracts | Observation contract named ARK as producer while ChatGPT Oracle emitted 110,619 observations before ARK preservation. | Contract language drift can cause future Oracles to duplicate ARK behavior. | Observation Source glossary and ontology entries. | Align producer tables and contract wording. | Update docs first; preserve runtime interfaces. | Open, reduced by Phase 8C |
| FC-DEBT-002 | High | Contracts / WEAVE / ARK | ARK preserved 217,994 explicit relationships while WEAVE was not implemented. | Relationship topology could leak into ARK. | Source Relationship ontology entry. | Clarify Source Relationship versus WEAVE topology. | Update contracts and ARK docs; implement WEAVE later only after proof. | Open, reduced by Phase 8C |
| FC-DEBT-003 | Medium | ARK | Default ARK observation cap rejected a 110,619-observation export. | Real imports need explicit bounded profiles. | Import Profile concept. | Add first-contact import profiles before larger imports. | Document profile now; implement reusable config only when needed. | Open |
| FC-DEBT-004 | High | Knowledge Compiler | Compiler reached 250,000 candidates with 34,910 low-confidence warnings. | Candidate noise blocks human review. | Governance intake design. | Add candidate grouping and Candidate Pages. | Design and test page semantics before changing compiler output. | Open |
| FC-DEBT-005 | High | Knowledge Governance | Governance repository rejected 250,000 candidates at its 100,000 cap. | Review queue cannot ingest real export-scale output. | Candidate Page and grouping. | Add bounded page intake and partial-page validation. | Add docs first; implement repository intake with tests later. | Open |
| FC-DEBT-006 | Medium | ARK / Event Bus | First Contact accumulated 328,614 event publication records. | Larger imports may consume excessive memory. | Event Bus streaming boundary. | Add streamable event publication or bounded event reporting. | Preserve current proof API; add streaming adapter later. | Open |
| FC-DEBT-007 | Medium | Repository Governance | 67 exact duplicate-content groups, mostly ARK/Foundry legacy. | Historical folders look active and duplicate ownership. | Legacy preservation manifest. | Remove duplicate mirrors after review. | Create simplification branch; keep manifest pointers and Git history. | Open |
| FC-DEBT-008 | Medium | Repository Governance | Many placeholder lifecycle readmes contain no local evidence. | Placeholder folders can appear implemented. | Engine template policy. | Mark placeholders explicitly and collapse redundant docs later. | Documentation-only clarification first; deletion only after review. | Open |
| FC-DEBT-009 | Medium | Canon | `constitution/glossary.md` lagged richer `canon/glossary.md`. | Contributors may choose conflicting canonical terms. | Canon ontology and glossary updates. | Keep `canon/` as semantic kernel and link constitution glossary to it. | Update references; avoid duplicate definitions. | Open, reduced by Phase 8C |
| FC-DEBT-010 | Low | ChatGPT Oracle | 250 `.dat` files were preserved as attachments; richer attachment metadata could improve traceability. | Attachment-to-message traceability may remain incomplete. | ChatGPT metadata evidence. | Parse attachment metadata only when it improves provenance. | Keep blobs opaque now; add parser only with tests. | Open |
