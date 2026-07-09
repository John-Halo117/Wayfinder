# Capability Bundles

| Bundle | Larger capability composed | Constituent candidates | Notes |
| --- | --- | --- | --- |
| P4-BND-001 | Shared platform capability boundary. | Identity, eventing, storage, policy, configuration, search/index. | Identity and event bus already have active proofs; others are scaffold or split. |
| P4-BND-002 | Compatibility and historical continuity capability. | Foundry/Forge aliases, legacy ARK boundaries, operations legacy, external legacy adapters. | Preserves Law of Theseus while avoiding duplicate canonical ownership. |
| P4-BND-003 | Governance and promotion capability. | Capability registry status, ADR amendment path, vocabulary promotion, alias retirement, RID proof thresholds. | Depends on human decision queue for doctrine-level changes. |
| P4-BND-004 | Knowledge health and evidence visibility capability. | Derived graph boundaries, conflicts, duplicates, unresolved reports, graph health. | Keeps knowledge useful without promoting generated artifacts to doctrine. |
| P4-BND-005 | Participant acquisition boundary capability. | Observation sources, external integrations, future participant adapters. | Composes acquisition without assuming conversations are the only source. |

## Composition Rule

Bundles compose opportunities into capability candidates only. P4 does not
declare new canonical capabilities.
