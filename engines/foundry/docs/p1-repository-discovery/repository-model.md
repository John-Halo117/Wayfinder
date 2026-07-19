# Repository Model

## Summary

Wayfinder is organized as a constitutional monorepo with canonical top-level
owners for constitution, canon, contracts, capabilities, services, engines,
domains, internal apps, external integrations, operations, tooling, tests, and
documentation.

The repository also contains:

- Generated knowledge artifacts under `Knowledge/`.
- Local private validation artifacts under `.wayfinder-validation/`.
- Large legacy ARK and Forge-origin trees under `engines/ark/legacy/` and
  `engines/foundry/legacy/`.
- Active Stage 2 proof implementations for identity, event bus, ARK ingestion,
  interpretation, views, and export mining.

## Primary Component Map

| Component | Purpose | Inputs | Outputs | Dependencies | Dependents | Owner | Layer | Class | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `WAYFINDER.md` | Root constitutional foundation. | Eisengarten-derived worldview. | Laws, stack, execution pipeline. | None. | Whole repo. | Constitution. | Constitution. | Constitutional. | High |
| `constitution/` | Constitutional law, architecture, execution, repository rules, asset model. | Wayfinder foundation. | Protected invariants and ownership rules. | None. | All components. | Constitution. | Constitution. | Constitutional. | High |
| `canon/` | Canonical names, aliases, ontology. | Constitution. | Vocabulary and semantic ownership. | `constitution/`. | Contracts, docs, engines. | Canon. | Constitution / semantic kernel. | Constitutional. | High |
| `contracts/` | Boundary language and contract docs. | Constitution, canon. | Stable interfaces and schemas by concept. | `constitution/`, `canon/`. | Services, engines, domains. | Contracts. | Protocol. | Protocol. | High |
| `capabilities/` | Capability registry scaffold. | Constitution, contracts. | Capability vocabulary. | `constitution/`, `contracts/`. | Engines, Jarvis, domains. | Capability Registry. | Capability Grammar / Capabilities. | Capability. | Medium |
| `services/identity/` | RID and identity proof implementation. | Identity contracts. | Deterministic identity service surface. | Contracts. | ARK and future services/engines. | Identity Service. | Services. | Platform. | High |
| `services/event-bus/` | Event and replay proof implementation. | Event contracts. | Local event bus service. | Contracts. | ARK and future runtime surfaces. | Event Bus Service. | Services. | Platform. | High |
| `services/storage/` | Storage service scaffold and docs. | Storage contracts. | Boundary docs, tests scaffold. | Contracts. | ARK, governance, retrieval future consumers. | Storage Service. | Services. | Platform. | Medium |
| `services/configuration/` | Configuration service scaffold and docs. | Config docs/contracts. | Boundary docs, tests scaffold. | Contracts. | Services and engines. | Configuration Service. | Services. | Platform. | Medium |
| `services/policy/` | Policy service scaffold and docs. | Policy contracts. | Boundary docs, tests scaffold. | Contracts. | ARK, Foundry, Jarvis future consumers. | Policy Service. | Services. | Platform. | Medium |
| `engines/ark/` active ingress | ChatGPT Oracle and reality ingestion proof. | Source exports, observation records, identity/events. | Observations, artifacts, import results. | Services and ARK contracts. | Interpretation, views, tooling. | ARK. | Perception / Observations / ARK. | Runtime. | High |
| `engines/ark/legacy/` | Preserved historical ARK, integrations, emitters, deployment, Forge-origin material. | Legacy source reality. | Migration evidence and legacy runnable surfaces. | Mixed legacy dependencies. | Foundry migration, historical analysis. | ARK legacy. | Historical / mixed. | Historical. | High as inventory, low by sub-owner |
| `engines/foundry/` | Foundry engine scaffold and docs. | Constitution, repository evidence. | Proof-backed engineering docs and future surfaces. | Contracts/services. | Developers, operations. | Foundry. | Actions / proofed engineering. | Runtime / Tooling. | High |
| `engines/foundry/legacy/` | Preserved Forge-origin source under Foundry fold. | Legacy Forge source. | Compatibility evidence and migrated prompt/runtime surfaces. | Legacy Forge internals. | Foundry extraction phases. | Foundry legacy. | Historical / Foundry. | Historical. | High |
| `engines/interpretation/` | Knowledge compiler and governance proofs. | ARK records, compiler candidates. | Candidate knowledge, reviewed promotions. | ARK-shaped data. | Views and retrieval. | Interpretation. | Focus / Understanding. | Runtime. | High |
| `engines/views/` | Knowledge retrieval and presentation projections. | Promoted knowledge, governance records. | Retrieval results and view models. | Interpretation. | Users, future Jarvis. | Views. | Representations / Experiences. | View. | High |
| `engines/jarvis/` | Jarvis scaffold. | Future navigation inputs. | Placeholder docs. | Contracts and engines future. | Users. | Jarvis. | Navigation / Actions. | Participant. | Medium |
| Other engine scaffolds | Named future engines or placeholders. | README-level ownership. | Placeholder documentation. | Constitution/canon. | Future phases. | Named engine. | Varies by engine. | Capability / Runtime. | Medium |
| `domains/` | Domain orchestration placeholder. | Engines/services future. | Domain docs scaffold. | Contracts/services/engines future. | Internal apps. | Domains. | Domains / Missions. | Participant. | Medium |
| `internal/` | Internal app placeholder. | Domains and engines future. | Internal surface scaffold. | Future app dependencies. | Users/operators. | Internal Apps. | Experiences. | View. | Medium |
| `external/` | External integration placeholder. | Provider/source systems future. | Compatibility scaffold. | Contracts future. | Perception/actions. | External Integrations. | External Systems. | Participant. | Medium |
| `operations/` | Operations placeholder. | Deployable surfaces future. | Operations scaffold. | Whole runtime future. | Operators. | Operations. | Operations. | Platform. | Medium |
| `tooling/architecture_intelligence/` | Repository architecture scanner/doctor. | Repo files and rules. | Governance reports. | Stdlib. | Tests, docs/governance. | Tooling. | Cross-cutting governance tooling. | Tooling. | High |
| `tooling/export_mining/` | Export mining and generated knowledge tooling. | Export evidence. | Source manifests and knowledge outputs. | Stdlib. | Knowledge docs and tests. | Tooling. | Derived knowledge tooling. | Tooling. | High |
| `docs/` | Architecture, ADRs, governance, programs, promotions, reports. | Constitution, implementation evidence, generated reports. | Documentation and governance artifacts. | Whole repo as evidence. | All contributors. | Documentation/Governance. | Architecture / Documentation. | Documentation. | High |
| `Knowledge/` | Generated knowledge base. | Export mining and preserved source evidence. | Derived facts, relationships, indexes, reports. | Tooling/export evidence. | Reviewers/search. | Generated Knowledge. | Representations / Understanding. | Generated artifact. | Medium |
| `.wayfinder-validation/` | Local private validation outputs. | Private source imports and replay. | Local reports and generated payloads. | Local environment. | Local validation. | Local Validation. | Evidence / validation. | Generated artifact. | High |
| `tests/` | Repo-level tooling tests. | Tooling modules. | Test assertions. | Tooling. | Developers/CI. | Tests. | Verification. | Tooling. | High |
| `.github/workflows/` | Repository automation. | GitHub events. | CI/governance runs. | Tooling/tests. | Contributors. | Operations/Governance. | Operations. | Platform. | High |
