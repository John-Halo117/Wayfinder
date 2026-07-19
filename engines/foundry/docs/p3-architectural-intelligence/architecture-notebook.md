# Architecture Notebook

## Observations

| ID | Observation | Evidence | Constitutional reference | Confidence | Potential impact |
| --- | --- | --- | --- | --- | --- |
| P3-OBS-001 | Legacy ARK contains mixed runtime, integration, operations, policy, storage, and Forge surfaces. | P1 Repository Model; P1 Unknown Components; `docs/architecture/20-repository-map.md`. | One Concept, One Home; Service First; engine ownership. | High | Clarifies future extraction boundaries. |
| P3-OBS-002 | Shared concerns appear in contracts, services, active engines, and legacy trees. | P1 Multiple Implementations: policy, storage, events, views/retrieval. | Service First; contracts independent of implementation. | High | Reduces drift risk by identifying canonical owners. |
| P3-OBS-003 | Canonical operations is mostly placeholder while legacy deployment material is extensive. | P1 Layer Map; P1 Unknown Components; `docs/architecture/20-repository-map.md`. | Operations layer ownership; actions affect reality and are re-observed. | Medium | Improves operational traceability. |
| P3-OBS-004 | Capability registry and operational maturity remain incomplete for readiness claims. | P2.5 Human Decision Queue; P1 confidence report. | Capability First; Proof Before Promotion. | Medium | Avoids treating scaffolds as operational capabilities. |
| P3-OBS-005 | Generated Knowledge is large and useful, but must remain derived. | P2 Canonical Knowledge Graph; P2.5 Health Report; `docs/architecture/18-cross-cutting.md`. | Reality First; derived artifacts are rebuildable. | High | Prevents generated representations from replacing evidence. |
| P3-OBS-006 | Forge is preserved both as ARK legacy and Foundry legacy compatibility material. | ADR-0010; P1 Repository Model; P1 Layer Map. | Law of Theseus; One Concept, One Home; compatibility aliases. | High | Maintains compatibility while protecting Foundry ownership. |
| P3-OBS-007 | Search/index responsibility is split across retrieval, tooling, generated Knowledge, and docs. | `docs/architecture/18-cross-cutting.md`; P1 Multiple Implementations. | Service First; Views are presentation/retrieval, not truth. | Medium | Clarifies whether search remains view/tooling or becomes shared service later. |
| P3-OBS-008 | Governance reports already identify drift signals: layer bypass edges, duplicate capability terms, generated tracked artifacts. | `docs/governance/architecture-drift.md`; P2.5 Canonical Health Report. | Preserve invariants; dependency direction. | High | Gives P4 evidence for grouping architectural hygiene opportunities. |
| P3-OBS-009 | ADRs function as decision evidence, but formal amendment promotion remains unresolved. | P2.5 Updated Open Questions; Human Decision Queue. | Constitution before architecture. | Medium | Affects future doctrine changes. |
| P3-OBS-010 | Legacy module ownership is intentionally cluster-level in current maps. | P1 Unknown Components; P2.5 P3 Readiness caveats. | Evidence before inference. | High | Prevents premature decomposition. |

## Observation Rule

These observations are evidence-backed architectural findings. They are not
implementation tasks, priorities, migration plans, or schedules.
