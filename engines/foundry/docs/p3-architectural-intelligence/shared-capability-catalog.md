# Shared Capability Catalog

| Candidate | Observed surfaces | Possible capability class | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Identity / RID | `contracts/identities/`, `services/identity/`, ARK ingestion references. | Shared capability / service capability. | P1 Repository Model; roadmap identity chain. | High |
| Eventing / replay | `contracts/events/`, `services/event-bus/`, ARK ingestion events, legacy event schemas. | Shared capability / service capability. | P1 Multiple Implementations. | High |
| Storage | `contracts/storage/`, `services/storage/`, ARK ingestion storage, legacy storage modules. | Shared capability / kernel/service candidate. | P1 Layer Map; ADR-0007. | High |
| Policy | `contracts/policies/`, `services/policy/`, legacy policy engine/files. | Shared capability / WFP or service candidate. | P1 Multiple Implementations. | High |
| Configuration | `services/configuration/`, legacy config/env files. | Shared capability. | P1 Repository Model; cross-cutting audit. | Medium |
| Search / retrieval / indexing | `engines/views/knowledge_retrieval/`, `Knowledge/search/`, tooling/export mining. | View or shared retrieval candidate. | Cross-cutting audit; P2 boundary. | Medium |
| Compatibility aliases | Canon aliases, ADR-0010, Foundry/Forge legacy. | Foundry capability. | P1/P2.5 reports. | High |
| Source acquisition / observation sources | ChatGPT Oracle, legacy emitters, ADR-0001/0008. | UCR or ingestion capability candidate. | P1 Layer Map; ADRs. | Medium |
| Validation / governance reports | Tooling architecture intelligence, docs/governance, tests. | Foundry/governance capability. | P1 Repository Model. | Medium |

## Boundary

This catalog records candidates only. It does not decide whether candidates
must become services, kernels, UCR capabilities, WFP capabilities, or Foundry
capabilities.
