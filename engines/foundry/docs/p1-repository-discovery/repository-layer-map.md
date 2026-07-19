# Repository Layer Map

| Constitutional layer | Repository coverage | Status | Confidence |
| --- | --- | --- | --- |
| Reality | Source exports, private validation inputs, generated evidence references. | Partial; mostly external/local. | Medium |
| CivPhys | `constitution/civphys.md`, canon terms, historical TRISCA material. | Documented plus legacy material. | Medium |
| Constitution | `WAYFINDER.md`, `constitution/`, constitutional docs. | Present. | High |
| Objectives | Roadmap, programs, mission-oriented docs. | Documented. | Medium |
| Capability Grammar | `capabilities/`, contracts/capabilities, canon terms. | Early scaffold. | Medium |
| Capabilities | Named engines/services and capability docs. | Partial. | Medium |
| Contracts | `contracts/`, engine/service contract folders, schemas docs. | Present. | High |
| Services | Identity and event bus implementations; storage/configuration/policy scaffolds. | Partial implementation. | High |
| Engines | ARK, Interpretation, Views active proofs; many engine scaffolds; legacy ARK/Foundry. | Present with mixed maturity. | High |
| Domains | `domains/README.md`. | Placeholder. | Medium |
| Internal Applications | `internal/README.md`; legacy Forge UI surfaces. | Placeholder plus historical surfaces. | Medium |
| External Systems | `external/README.md`; legacy integrations/emitters. | Placeholder plus historical surfaces. | Medium |
| Operations | `operations/README.md`, `.github/workflows`, legacy deployment files. | Placeholder plus historical/active automation. | Medium |

## Evidence Pipeline Coverage

| Evidence layer | Repository components |
| --- | --- |
| Reality | `.wayfinder-validation/`, external exports, source artifacts referenced by docs. |
| Perception | `engines/ark/ingress/chatgpt_oracle/`, legacy emitters and adapters. |
| Observations | `contracts/observations/`, ARK reality ingestion models/events. |
| ARK | `engines/ark/ingress/reality_ingestion/`, `engines/ark/legacy/`, ARK docs. |
| Representations | `engines/views/knowledge_retrieval/`, `Knowledge/Indexes`, canonical language docs. |
| Focus | `engines/interpretation/knowledge_governance/`, candidate page docs. |
| Understanding | `engines/interpretation/knowledge_compiler/`, generated knowledge, canonical language. |
| Missions | `docs/programs/`, `docs/implementation-backlog.md`, roadmap docs. |
| Bearings | `contracts/bearings/`, canon bearing terms. |
| Reasoning | `engines/reasoning/README.md`, reasoning contracts/docs. |
| Navigation | `engines/jarvis/`, `engines/nomad/`, navigation-oriented canon terms. |
| Experiences | `engines/views/`, `internal/`, legacy Forge UI. |
| Actions | `engines/foundry/`, `external/`, `operations/`, legacy action/deploy surfaces. |

## Multiple Implementations

| Responsibility | Multiple observed surfaces |
| --- | --- |
| Forge/Foundry engineering runtime | `engines/ark/legacy/ark-core/forge/`, `engines/foundry/legacy/ark-core/forge/`, Foundry docs. |
| ARK runtime | Active `engines/ark/ingress/reality_ingestion/`, legacy Python/Rust/Go ARK trees. |
| Policy | `contracts/policies/`, `services/policy/`, legacy `policy_engine.py`, legacy JSON policies. |
| Storage | `contracts/storage/`, `services/storage/`, active ingestion storage module, legacy storage modules. |
| Events | `contracts/events/`, `services/event-bus/`, ARK ingestion events, legacy event schemas. |
| Views/retrieval | Active `engines/views/`, generated `Knowledge/Indexes`, docs. |

## Missing Or Placeholder Layers

| Layer | Observed state |
| --- | --- |
| Domains | Placeholder only. |
| Internal Applications | Placeholder in canonical tree; legacy UI exists under Forge. |
| External Systems | Placeholder in canonical tree; legacy integrations exist under ARK. |
| Operations | Placeholder canonical tree plus GitHub workflow and legacy deploy files. |
| Reasoning / Navigation | Mostly scaffold/documented, with Jarvis/NOMAD placeholders. |
