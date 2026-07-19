# Interface Catalog

## Stable Interfaces

| Interface | Location | Owner | Consumers |
| --- | --- | --- | --- |
| Constitutional laws and stack | `WAYFINDER.md`, `constitution/` | Constitution | Whole repo |
| Canonical names and aliases | `canon/` | Canon | Contributors, contracts, docs, engines |
| Contract concept docs | `contracts/*/README.md` | Contracts | Services, engines, domains |
| Identity service | `services/identity/identity_service.py` | Identity Service | ARK and future RID consumers |
| Event bus service | `services/event-bus/event_bus_service.py` | Event Bus Service | ARK and future event consumers |
| ChatGPT Oracle CLI/API | `engines/ark/ingress/chatgpt_oracle/cli.py`, `oracle.py` | ARK ingress | ARK ingestion, tests |
| Reality ingestion pipeline | `engines/ark/ingress/reality_ingestion/pipeline.py` | ARK | Interpretation/views downstream |
| Knowledge compiler | `engines/interpretation/knowledge_compiler/compiler.py` | Interpretation | Governance |
| Knowledge governance engine | `engines/interpretation/knowledge_governance/engine.py` | Interpretation | Retrieval/views |
| Knowledge retrieval store | `engines/views/knowledge_retrieval/store.py` | Views | Knowledge views |
| Knowledge views engine | `engines/views/knowledge_views/engine.py` | Views | Users/future apps |
| Architecture doctor CLI | `tooling/architecture_intelligence/cli.py` | Tooling | Tests/governance |
| Export mining tools | `tooling/export_mining/*.py` | Tooling | Generated knowledge/tests |

## Internal Interfaces

| Interface | Location | Notes |
| --- | --- | --- |
| ARK ingestion models/events/storage | `engines/ark/ingress/reality_ingestion/` | Internal to active ARK ingestion proof. |
| ChatGPT Oracle models | `engines/ark/ingress/chatgpt_oracle/models.py` | Internal stream/source models. |
| Interpretation models/repository | `engines/interpretation/*/models.py`, `repository.py` | Internal compiler/governance records. |
| View models | `engines/views/*/models.py` | Internal retrieval/view records. |
| Service tests | `services/*/tests/` | Verification surfaces. |
| Engine tests | `engines/*/tests/` | Verification surfaces. |

## Plugin Or Compatibility Boundaries

| Boundary | Location | Classification |
| --- | --- | --- |
| Forge legacy app launchers | `engines/foundry/legacy/Forge App.*`, `forge*` | Compatibility alias boundary. |
| Forge runtime/MCP/tools | `engines/foundry/legacy/ark-core/forge/` | Historical plugin/tool boundary. |
| ARK legacy integrations | `engines/ark/legacy/ark/integrations/` | Historical external integration boundary. |
| ARK legacy emitters | `engines/ark/legacy/emitters/` | Historical source adapter boundary. |
| GitHub workflow automation | `.github/workflows/` | Operations/governance automation boundary. |
| Docker/compose deployment | `engines/ark/legacy/Dockerfile*`, `docker-compose*.yml` | Historical operations boundary. |

## Public API Indicators

P1 records these as observed likely public surfaces by name and placement:

- CLI files: `cli.py`, shell scripts, PowerShell scripts, command scripts.
- Service root modules: `identity_service.py`, `event_bus_service.py`.
- Engine root modules: `oracle.py`, `pipeline.py`, `compiler.py`, `engine.py`,
  `store.py`.
- Contract README and schema files.
- Legacy Go `cmd/*/main.go` entrypoints.
- Legacy Rust `src/main.rs` and `src/lib.rs`.
