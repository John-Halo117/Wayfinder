# Reuse Analysis

## Existing Capability First Check

| Need area | Existing capability surfaces | Reuse observation | Confidence |
| --- | --- | --- | --- |
| Identity | Identity contract and service proof. | Existing identity surface should be considered before new identity logic. | High |
| Eventing | Event contracts and event bus service proof. | Existing event bus should be considered before new event routing. | High |
| Storage | Storage contract/service scaffold, ARK storage modules, legacy storage. | Existing surfaces should be cataloged before any new persistence mechanism. | High |
| Policy | Policy contracts/service scaffold, legacy policy files. | Existing policy artifacts should be considered before new rule systems. | High |
| Search/retrieval | Views retrieval, Knowledge search DBs, export mining tools. | Existing retrieval/index surfaces should be considered before a new search service. | Medium |
| Engineering prompts | Bootstrap prompt standard and P0-P2.5 prompts. | Existing prompt standard should govern future prompts. | High |
| External adapters | ChatGPT Oracle, legacy emitters, external placeholder. | Existing observation-source patterns should be considered before new participant adapters. | Medium |

## Cheapest Constitutional Approach Ladder

P3 observed opportunities through this order:

```text
Documentation
-> Configuration
-> Reuse
-> Composition
-> Refactor
-> New implementation
```

Most P3 opportunities currently fit documentation, ownership metadata,
interface cataloging, or artifact linkage. That is an observation about cost,
not an implementation plan.
