# Layer Violation Report

## Observed Layer Issues

| ID | Issue | Evidence | Confidence | Notes |
| --- | --- | --- | --- | --- |
| P3-LV-001 | Layer bypass edges are present. | `docs/governance/architecture-drift.md` reports `layer_bypass_edges: 7`. | High | Existing report records metric; P3 does not inspect every edge. |
| P3-LV-002 | Cross-layer shortcuts remain mainly in legacy. | `docs/architecture/18-cross-cutting.md`. | High | Registered debt, not newly inferred. |
| P3-LV-003 | Canonical operations is placeholder while operations content exists in legacy deploy files and workflows. | P1 Layer Map; repository map. | Medium | Ownership gap, not implementation decision. |
| P3-LV-004 | Generated Knowledge is tracked and large. | Cross-cutting health dashboard; P2/P2.5. | High | Not a violation when treated as derived evidence. |
| P3-LV-005 | Search/index ownership crosses views, tooling, and generated Knowledge. | Cross-cutting audit. | Medium | Needs ownership clarification before service extraction. |
| P3-LV-006 | Forge appears in both ARK legacy and Foundry legacy. | P1 Multiple Implementations; ADR-0010. | High | Compatibility/history preservation explains coexistence. |

## Not Violations Under Current Evidence

- Generated Knowledge does not replace reality according to existing reports.
- Active service-to-engine violations are reported as `0`.
- Active contract-to-implementation violations are reported as `0`.
- Generated graph circular references are reported as `0`.
