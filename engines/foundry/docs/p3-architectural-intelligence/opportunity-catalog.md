# Opportunity Catalog

| ID | Opportunity | Evidence | Existing capability checked | Lowest-cost constitutional approach | Confidence |
| --- | --- | --- | --- | --- | --- |
| P3-OPP-001 | Clarify canonical ownership for shared policy, storage, and event concerns across contracts, services, active engines, and legacy. | P1 Multiple Implementations; architecture cross-cutting audit. | Contracts, services/policy, services/storage, services/event-bus, legacy files. | Documentation or ownership metadata before code changes. | High |
| P3-OPP-002 | Preserve generated Knowledge as inherited derived memory with explicit non-canonical boundaries. | P2/P2.5 reports; Knowledge manifest. | P2 Knowledge Inventory; P2.5 Promotion Audit. | Documentation and validation policy. | High |
| P3-OPP-003 | Clarify operations ownership where canonical operations is placeholder and legacy deployment is extensive. | P1 Layer Map; repository map. | `operations/`, `.github/workflows/`, legacy deploy files. | Documentation and classification before extraction. | Medium |
| P3-OPP-004 | Consolidate Foundry/Forge architectural understanding without renaming compatibility entrypoints. | ADR-0010; Foundry docs; P1 model. | Foundry bootstrap, Foundry legacy, ARK legacy Forge. | Alias map and source-of-record documentation. | High |
| P3-OPP-005 | Distinguish capability registry placeholders from canonical capabilities. | P1 Layer Map; P2.5 queue. | `capabilities/`, contracts/capabilities, canon terms. | Documentation/status metadata. | Medium |
| P3-OPP-006 | Separate search/index observations from view, tooling, and generated knowledge ownership. | Cross-cutting audit; P1 Multiple Implementations. | Views retrieval, export mining, Knowledge/search. | Documentation and interface cataloging. | Medium |
| P3-OPP-007 | Strengthen ADR-to-amendment traceability. | P2.5 Updated Open Questions and Human Decision Queue. | ADR index, governance docs. | Governance documentation. | Medium |
| P3-OPP-008 | Record legacy module ownership at finer granularity only when P4/P5 needs it. | P1 Unknown Components; P2.5 caveats. | P1 cluster maps. | Artifact-level inventory extension, not code movement. | High |
| P3-OPP-009 | Keep generated graph conflict/duplicate/unresolved counts visible to later architecture phases. | P2/P2.5 conflict and health reports. | Knowledge reports. | Report linkage and gates. | High |
| P3-OPP-010 | Clarify external integration boundary for legacy emitters/adapters. | P1 Unknown Components; ADR-0008. | `external/`, legacy emitters/integrations. | Compatibility boundary documentation. | Medium |

## Notes

The lowest-cost approach is an architectural observation, not an implementation
decision. P4 may group opportunities but must still avoid executing them.
