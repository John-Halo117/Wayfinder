# Dependency Model

## Canonical Direction

Dependencies point downward toward earlier constitutional authority and earlier
evidence layers. Later layers may consume earlier layers through contracts,
services, or generated read models. Earlier layers must not depend on later
layers for identity or truth.

```text
Actions
-> Experiences
-> Navigation
-> Reasoning
-> Bearings
-> Missions
-> Understanding
-> Focus
-> Representations
-> ARK
-> Observations
-> Perception
-> Reality
```

## Constitutional Dependencies

| Concept | Depends on | Must not depend on |
| --- | --- | --- |
| Constitution | Eisengarten philosophy. | Runtime convenience. |
| Canon | Constitution. | Local implementation names. |
| Contracts | Constitution, canon, capability grammar. | Services or engines. |
| Services | Contracts. | Engines. |
| Engines | Contracts, services, preserved evidence. | Domains, apps, operations. |
| Domains | Contracts, services, engines. | Internal app presentation. |
| Internal apps | Domain and engine surfaces. | Direct truth ownership. |
| External integrations | Contracts and compatibility boundaries. | Canonical provider ownership. |
| Operations | Deployable services, engines, apps. | Constitutional redefinition. |

## ADR Dependency Commitments

| ADR | Dependency commitment |
| --- | --- |
| 0001 Observation Sources | Observation Sources produce observations; ARK must not own source discovery or parsing. |
| 0002 Source Relationships | ARK preserves source relationships before topology; source edges are not a Knowledge Graph. |
| 0003 Import Profiles | Large private imports require bounded profiles and deterministic expectations. |
| 0004 Private Validation Outputs | Private validation artifacts remain local and ignored. |
| 0005 Candidate Paging | Governance intake is bounded and human-reviewed. |
| 0006 Canonical Language | Canonical Language is derived, rebuildable, source-agnostic, and not AI-owned. |
| 0007 Storage Before Runtime Kernel | Storage service proof precedes Runtime Kernel extraction. |
| 0008 Compatibility Layer | External integrations use compatibility layers to preserve replaceability. |
| 0009 Candidate Pages | Bounded candidate pages preserve reviewability without summarizing away evidence. |
| 0010 Forge Consolidation | Forge legacy consolidates under Foundry with compatibility aliases. |

## Program Dependency Chains

Reality Identity:

```text
Identity Service -> RID -> Universal Asset Ingestion -> Runtime Kernel -> ARK
```

Universal Asset Ingestion:

```text
Identity
-> RID
-> UAI
-> Runtime Kernel
-> ARK
-> WEAVE
-> Interpretation
-> Reasoning
-> Views
-> Jarvis
```

These chains are roadmap commitments, not evidence that all layers are
operational.
