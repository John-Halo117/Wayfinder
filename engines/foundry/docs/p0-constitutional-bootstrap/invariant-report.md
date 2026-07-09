# Invariant Report

## Protected Invariants

| Invariant | Source owner | Enforcement implication |
| --- | --- | --- |
| Reality precedes representation. | Constitution. | Derived systems cannot overwrite or replace source observations. |
| Observation precedes interpretation. | Constitution and architecture. | Parsing and import must preserve raw evidence before meaning. |
| Evidence precedes conclusion. | Constitution/assets. | Claims require provenance and proof. |
| Reality is append-only. | `WAYFINDER.md`. | Deletion or mutation of source reality requires explicit constitutional exception. |
| Capabilities outlive implementations. | Law of Theseus. | Rewrites must preserve capability continuity. |
| One concept has one home. | Constitution and canon. | New terms require ownership and alias checks. |
| Contracts stay implementation-independent. | Repository rules. | Contracts must not import or depend on engines/services. |
| Services own shared infrastructure. | Service First. | Repeated engine infrastructure should migrate to services only with proof. |
| Engines own unique responsibilities. | Repository rules. | Engines should not redefine shared language. |
| Derived artifacts are rebuildable. | Architecture and canonical language. | Indexes, views, representations, and canonical language cannot become source truth. |
| ARK preserves; it does not interpret. | Architecture and ADR-0001/0002. | Source discovery, parsing, and knowledge topology remain outside ARK preservation. |
| Actions affect reality and are re-observed. | Architecture. | Action systems cannot mark their own effects as truth without observation. |
| AI is last, not first. | Architecture principles. | Probabilistic systems may consume evidence but not own preservation or normalization. |
| Private validation remains local. | ADR-0004. | Generated private evidence must not be committed as durable public docs. |

## Protected Interfaces

- Constitution and canon definitions.
- Contracts and schemas.
- RID and identity semantics.
- ARK observation, artifact, source relationship, and provenance boundaries.
- Import Profile boundaries for large or private imports.
- Compatibility aliases for legacy integration names.
- Canonical Language traceability to ARK-preserved source reality.

## Permitted Evolution

- Implementation internals behind stable contracts.
- Storage backends after Storage service proof.
- Source-specific adapters and Oracles.
- Legacy Forge/Foundry compatibility names, provided aliases resolve to one
  canonical owner.
- Derived language, retrieval, view, and governance artifacts when they remain
  rebuildable and traceable.

## Drift Indicators

- A provider name appears in the ingestion pipeline where a substrate or
  capability interface should appear.
- A generated view becomes the only source of a fact.
- A service imports an engine.
- A contract imports implementation code.
- An engine defines reusable infrastructure without a service boundary.
- A legacy alias starts accumulating new canonical responsibilities.
