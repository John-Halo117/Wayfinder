# Dependency Graph

## Architectural Dependency Graph

```text
constitution
-> canon
-> contracts
-> services
-> engines
-> domains
-> internal
-> operations
```

External integrations attach through contracts and engine/service boundaries.
Tooling and docs consume repository evidence and produce governance artifacts.
Generated knowledge consumes preserved/exported evidence and tooling outputs.

## Active Python Cluster Imports

| Cluster | Internal imports observed |
| --- | --- |
| `ark.chatgpt_oracle` | `.models`, `.oracle` |
| `ark.reality_ingestion` | `.events`, `.models`, `.pipeline`, `.storage` |
| `services.identity` | `.identity_service`, `services.identity` |
| `services.event-bus` | No internal repo imports observed in bounded scan. |
| `interpretation.knowledge_compiler` | `.compiler`, `.models` |
| `interpretation.knowledge_governance` | `.engine`, `.models`, `.repository`, `engines.interpretation.knowledge_compiler.models` |
| `views.knowledge_retrieval` | `.models`, `.store`, `engines.interpretation.knowledge_governance.models` |
| `views.knowledge_views` | `.engine`, `.models`, `engines.interpretation.knowledge_governance.models`, `engines.views.knowledge_retrieval.models`, `engines.views.knowledge_retrieval.store` |
| `tooling.architecture_intelligence` | `.doctor` |
| `tooling.export_mining` | `.mine_wayfinder_export` |
| repo-level tests | `tooling.architecture_intelligence.doctor`, `tooling.export_mining.*` |

## Observed Active Flow

```text
services.identity
services.event-bus
-> engines.ark.ingress.reality_ingestion
-> engines.interpretation.knowledge_compiler
-> engines.interpretation.knowledge_governance
-> engines.views.knowledge_retrieval
-> engines.views.knowledge_views
```

The scan records imports and documented flow. It does not assert runtime
completeness.

## Legacy Dependency Clusters

| Cluster | Observed pattern |
| --- | --- |
| `legacy.ark` | Dense relative imports inside Forge, ARK Python modules, integrations, emitters, Go and Rust runtime components. |
| `legacy.foundry` | Preserved Forge relative imports under Foundry fold; mirrors a subset of Forge runtime, model, UI, transform, and verification surfaces. |
| legacy deployment | Dockerfiles, compose files, shell scripts, Traefik, Authelia, Prometheus, GitHub workflows. |
| legacy contracts/policy | JSON schemas and policy files embedded under ARK legacy. |

## Circular Dependencies

No active circular dependency was proven by the bounded static cluster scan.
Existing governance documentation reports generated graph circular references
as `0`. Legacy clusters were not decomposed deeply enough in P1 to prove or
disprove internal cycles.
