# Repository Inventory

## File Counts

The bounded inventory excludes `.git/`, `.pytest_cache/`, `.wayfinder-validation/`,
and `Knowledge/` for source-tree counts.

| Area | Files |
| --- | ---: |
| `engines/` | 633 |
| `docs/` | 119 |
| `services/` | 61 |
| `contracts/` | 30 |
| `tooling/` | 17 |
| `constitution/` | 8 |
| `tests/` | 6 |
| `canon/` | 3 |
| root single files | 9 |
| `capabilities/` | 1 |
| `domains/` | 1 |
| `external/` | 1 |
| `internal/` | 1 |
| `operations/` | 1 |

Total bounded source-tree files observed: 892.

## File Types

| Type | Count |
| --- | ---: |
| Markdown | 390 |
| Python | 241 |
| Go | 75 |
| Rust | 36 |
| Shell | 34 |
| JSON | 23 |
| YAML/YML | 16 |
| Python bytecode | 10 |
| Text | 9 |
| PowerShell | 5 |
| Windows command scripts | 4 |
| TOML | 2 |
| Go module files | 2 |

## Top-Level Directories

| Path | Classification | Notes |
| --- | --- | --- |
| `canon/` | Constitutional | Canonical naming and ontology. |
| `capabilities/` | Capability | Capability registry scaffold. |
| `constitution/` | Constitutional | Laws, architecture, execution, ownership. |
| `contracts/` | Protocol | Contract boundary docs by concept. |
| `docs/` | Documentation / Architecture | ADRs, architecture, governance, programs, promotions, reports. |
| `domains/` | Participant | Domain orchestration placeholder. |
| `engines/` | Runtime | Active engines, scaffolds, and legacy source. |
| `external/` | Participant | External integration placeholder. |
| `internal/` | View | Internal app placeholder. |
| `operations/` | Platform | Operations placeholder. |
| `services/` | Platform | Cross-cutting service proofs and scaffolds. |
| `tests/` | Tooling | Repo-level tests. |
| `tooling/` | Tooling | Architecture intelligence and export mining. |
| `Knowledge/` | Generated artifact | Derived knowledge base. |
| `.wayfinder-validation/` | Generated artifact | Private local validation evidence. |
| `.github/` | Platform | GitHub workflow automation. |

## Active Source Packages

| Package | Files | Classification |
| --- | ---: | --- |
| `services/identity/` | 2 Python source files plus docs/tests | Platform service |
| `services/event-bus/` | 1 Python source file plus docs/tests | Platform service |
| `engines/ark/ingress/chatgpt_oracle/` | 4 Python source files plus docs/tests | Runtime engine ingress |
| `engines/ark/ingress/reality_ingestion/` | 5 Python source files plus docs/tests | Runtime engine ingress / ARK preservation |
| `engines/interpretation/knowledge_compiler/` | 3 Python source files | Runtime engine |
| `engines/interpretation/knowledge_governance/` | 4 Python source files | Runtime engine |
| `engines/views/knowledge_retrieval/` | 3 Python source files | View/retrieval engine |
| `engines/views/knowledge_views/` | 3 Python source files | View engine |
| `tooling/architecture_intelligence/` | 3 Python source files | Tooling |
| `tooling/export_mining/` | 4 Python source files | Tooling |

## Legacy Source Clusters

| Cluster | Observed contents | Classification |
| --- | --- | --- |
| `engines/ark/legacy/ark-core/forge/` | Forge runtime, context, control, exec, MCP, memory, models, UI, verification. | Historical / Forge-origin |
| `engines/foundry/legacy/ark-core/forge/` | Preserved Forge runtime subset under Foundry. | Historical / Foundry compatibility |
| `engines/ark/legacy/ark/` | Python and Rust ARK runtime modules, integrations, policy, storage, replay. | Historical / ARK |
| `engines/ark/legacy/internal/` | Go adapters, contracts, budget, config, runtime surfaces. | Historical / ARK |
| `engines/ark/legacy/emitters/` | Home Assistant, Jellyfin, Unifi emitters. | Historical / external source adapters |
| `engines/ark/legacy/deploy`, Dockerfiles, compose files | Deployment and operations material. | Historical / operations |

## Tests

| Test area | Primary target |
| --- | --- |
| `engines/ark/tests/` | Active ChatGPT Oracle and reality ingestion. |
| `engines/interpretation/tests/` | Knowledge compiler and governance. |
| `engines/views/tests/` | Knowledge retrieval and views. |
| `services/identity/tests/` | Identity service. |
| `services/event-bus/tests/` | Event bus service. |
| `tests/` | Architecture intelligence and export mining tooling. |
| `engines/ark/legacy/**/tests` | Legacy ARK/Forge surfaces. |
