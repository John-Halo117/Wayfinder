# Migration Bundles

P4 records whether opportunities appear to migrate together. It does not plan
migrations.

| Bundle | Migration composition observation | Fragmentation risk |
| --- | --- | --- |
| P4-BND-001 | Shared infrastructure ownership should be considered together because policy, storage, events, and search/index all cross contracts, services, active engines, and legacy. | Isolated changes could create new duplicate owners. |
| P4-BND-002 | Legacy ARK, Foundry/Forge, operations, and external adapter boundaries should be considered together because they share compatibility and historical evidence. | Fragmented moves could lose provenance or break aliases. |
| P4-BND-003 | Governance questions should be considered together because capability status, ADR promotion, vocabulary promotion, and alias retirement all affect canonical ownership. | Separate decisions could conflict. |
| P4-BND-004 | Knowledge artifact health should be considered together because graph, reports, conflicts, duplicates, and unresolved items share validation semantics. | Treating reports separately could hide uncertainty. |
| P4-BND-005 | Participant acquisition boundaries should be considered with legacy external/adapter evidence and Knowledge source coverage gaps. | New adapters could duplicate provider-specific logic. |

## Boundary

These are migration composition observations, not migration strategies.
