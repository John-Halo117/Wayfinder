# Bundle Catalog

| Bundle ID | Bundle | Purpose | Included opportunities | Constitutional justification | Boundary | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| P4-BND-001 | Shared Infrastructure Ownership | Compose shared policy, storage, event, and search/index ownership observations. | P3-OPP-001, P3-OPP-006 | Service First; One Concept, One Home; contracts independent of implementation. | Ownership and interface coherence only; no extraction decision. | High |
| P4-BND-002 | Legacy Boundary Clarification | Compose ARK legacy, Foundry/Forge, operations, and external adapter boundary observations. | P3-OPP-003, P3-OPP-004, P3-OPP-008, P3-OPP-010 | Law of Theseus; preserve history; compatibility aliases; evidence before inference. | Cluster-level legacy boundaries only. | High |
| P4-BND-003 | Governance And Promotion Rules | Compose unresolved governance questions around capabilities, ADRs, vocabulary, aliases, and RID proof thresholds. | P3-OPP-005, P3-OPP-007, P2.5 decisions 2-7 | Proof Before Promotion; Capability First; One Concept, One Home. | Human-decision-dependent; no doctrine invented. | Medium |
| P4-BND-004 | Knowledge Artifact Health | Compose generated Knowledge boundary, conflict visibility, duplicate visibility, and graph health observations. | P3-OPP-002, P3-OPP-009 | Reality First; derived artifacts are rebuildable; evidence before conclusion. | Reporting and validation boundaries; no graph mutation. | High |
| P4-BND-005 | Participant Acquisition Boundary | Compose observation-source, external integration, and future participant acquisition boundary observations. | P3-OPP-010, P2 source coverage gaps | Reality First; ADR-0001; ADR-0008; provider replaceability. | Acquisition boundary only; no adapter implementation. | Medium |

## Opportunity Coverage

| Opportunity | Bundles |
| --- | --- |
| P3-OPP-001 | P4-BND-001 |
| P3-OPP-002 | P4-BND-004 |
| P3-OPP-003 | P4-BND-002 |
| P3-OPP-004 | P4-BND-002 |
| P3-OPP-005 | P4-BND-003 |
| P3-OPP-006 | P4-BND-001 |
| P3-OPP-007 | P4-BND-003 |
| P3-OPP-008 | P4-BND-002 |
| P3-OPP-009 | P4-BND-004 |
| P3-OPP-010 | P4-BND-002, P4-BND-005 |

P3-OPP-010 appears in two bundles because external integration boundaries are
both a legacy-boundary concern and a participant-acquisition concern.
