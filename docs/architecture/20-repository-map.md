# 20 Repository Map

This map assigns major repository areas to canonical layers. It is a
documentation inventory, not a file move plan.

| Path | Layer | Responsibility | Dependencies | Consumers | Status | Migration Path |
| --- | --- | --- | --- | --- | --- | --- |
| `WAYFINDER.md` | Constitution | Foundation laws and stack | none | all repo | canonical | preserve |
| `constitution/` | Constitution | immutable architecture | none/contracts references | all repo | canonical | preserve |
| `canon/` | Constitution / semantic kernel | naming, glossary, ontology | constitution | contributors, contracts | canonical | preserve; avoid duplicate glossary definitions |
| `contracts/` | Observations through Actions | boundary language | constitution | services, engines, domains | canonical | continue contract purity |
| `capabilities/` | Capability Registry | capability vocabulary | constitution, contracts | NOMAD, Jarvis, engines | canonical early | mature registry |
| `services/identity/` | Cross-cutting service | RID/identity proof | contracts | ARK, Event Bus, future engines | active canonical | add consumers after proof |
| `services/event-bus/` | Cross-cutting service | event/replay proof | contracts | ARK, future engines | active canonical | add adapters |
| `services/storage/` | Cross-cutting service | storage boundary | contracts | ARK, governance, retrieval | canonical scaffold | implement Stage 2 proof |
| `services/configuration/` | Cross-cutting service | config boundary | contracts | engines/services | scaffold | implement after Storage |
| `services/policy/` | Cross-cutting service | policy boundary | contracts | ARK, Foundry, Jarvis | scaffold | implement after Configuration |
| `engines/ark/ingress/chatgpt_oracle/` | Perception / Observations | ChatGPT Oracle | stdlib, contracts by shape | ARK ingestion | active transitional | keep source-specific |
| `engines/ark/ingress/reality_ingestion/` | ARK | preserve observations | Identity, Event Bus protocols | compiler, views, generated proofs | active canonical proof | add Storage service later |
| `engines/ark/legacy/` | Legacy | preserved historical ARK | many legacy deps | migration evidence | legacy transitional | extract with proof |
| `engines/interpretation/knowledge_compiler/` | Understanding | candidate knowledge | ARK records | governance | active canonical proof | add Candidate Pages |
| `engines/interpretation/knowledge_governance/` | Focus / Understanding | review and promotion | compiler models | retrieval/views | active canonical proof | page intake |
| `engines/views/knowledge_retrieval/` | Representations / Experiences | disposable indexes | promoted knowledge | views | active canonical proof | evaluate Search service later |
| `engines/views/knowledge_views/` | Experiences | presentation projections | retrieval | Jarvis, users | active canonical proof | keep presentation-only |
| `engines/foundry/` | Actions / proofed engineering | engineering change with proof | contracts/services | operations, developers | transitional | consolidate Forge legacy |
| `engines/foundry/legacy/` | Legacy | Forge-origin preserved code | legacy | migration evidence | legacy transitional | source-of-record + aliases |
| Other `engines/*` | Varies | constitutional placeholders | contracts/docs | future phases | mostly scaffold | add proofs only with evidence |
| `domains/` | Missions / domains | domain orchestration | contracts/services/engines | future apps | placeholder | wait for real domain workflow |
| `internal/` | Experiences | internal apps | services/engines | users/operators | placeholder | add only presentation/app surfaces |
| `external/` | Perception / compatibility | replaceable adapters | contracts/services | Observation Sources/services | placeholder | create Compatibility Layer |
| `operations/` | Actions / deployment | deployment/runbooks | all deploy targets | operators | placeholder | move ops from legacy after parity |
| `tooling/export_mining/` | Tooling / derived knowledge | export mining/compiler tools | stdlib, Knowledge | docs, reviewers | active transitional | keep tooling unless runtime path emerges |
| `Knowledge/` | Representations / Understanding | generated derived knowledge | export evidence | reviewers/search | generated transitional | mark generated; consider artifact policy |
| `.wayfinder-validation/` | Local validation | private evidence outputs | local source files | local replay | ignored local | keep untracked |
| `docs/` | Governance | analysis, ADRs, roadmaps | all evidence | contributors | active | keep linked to canonical owners |
| `tests/` | Verification | repo-level tests | active modules | CI/reviewers | active | expand with linter |

## Repository Operation Flow

Repository and filesystem changes follow progressive discovery:

```text
Observe -> Inventory -> Classify -> Build Canonical Destinations -> Simulate -> Execute -> Verify -> Report
```

Never reorganize before completing an inventory. Low-confidence items go to a
review queue. Build destination structures before moving files. Every move
must be reversible, logged, verified, and reported with confidence.
