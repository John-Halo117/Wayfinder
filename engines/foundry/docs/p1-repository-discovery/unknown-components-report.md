# Unknown Components Report

P1 records unknowns without resolving them.

## Unclassified Or Partially Classified Components

| Component | Unknown |
| --- | --- |
| `engines/ark/legacy/` subtrees | Precise canonical owner for every internal legacy module is not established in P1. |
| `engines/foundry/legacy/` subtrees | Future canonical split between Foundry core, compatibility, UI, verification, and tooling remains unmapped below cluster level. |
| `Knowledge/` generated files | Individual generated facts and graph files are not mapped one-by-one to constitutional owners. |
| `.wayfinder-validation/` local outputs | Private/local payloads are classified as validation artifacts but not inspected deeply. |
| `wf` root file | File observed in inventory; exact role not classified in P1. |
| Python bytecode under source tree | Observed generated cache artifacts; ownership is generated/runtime cache. |

## Ambiguous Ownership

| Surface | Ambiguity |
| --- | --- |
| Legacy policy files | May map to contracts, policy service, ARK runtime, or operations depending on future extraction. |
| Legacy storage files | May map to ARK storage internals or future storage service. |
| Legacy integrations and emitters | May map to external compatibility, perception, or ARK ingress. |
| Legacy Forge UI | May map to Foundry internal app, internal apps, or historical compatibility. |
| Generated governance reports | Documentation artifacts, generated artifacts, and governance evidence overlap. |

## Missing Documentation

| Area | Missing or unclear |
| --- | --- |
| Standalone Eisengarten source | Not found during P0/P1 scans. |
| Constitutional amendment ledger | ADRs exist, but no separate amendment ledger was discovered. |
| Capability registry maturity | Registry exists as scaffold; exact canonical capability set remains early. |
| Legacy module ownership | Some legacy trees include mixed responsibilities without P1-level decomposition docs. |
| Operations boundaries | Canonical operations directory is placeholder while legacy deploy material exists elsewhere. |

## Constitutional Mismatches Observed As Facts

These are recorded as mapping facts, not as recommendations.

| Fact | Constitutional tension |
| --- | --- |
| Shared concerns such as policy, storage, and events appear in contracts, services, active engines, and legacy trees. | One Concept, One Home requires canonical ownership, while legacy preserves historical duplicates. |
| Forge exists in ARK legacy and Foundry legacy. | Canon resolves Forge as legacy alias to Foundry, while preserved history remains duplicated. |
| Generated knowledge is large and present in the repo. | Reality First requires generated knowledge to remain derived and subordinate to evidence. |
| Canonical operations are placeholder while legacy deployment files are extensive. | Operations ownership exists constitutionally but is not fully folded into canonical tree. |
