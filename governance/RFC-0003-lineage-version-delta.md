# RFC-0003 — Lineage / Version / Delta Semantic Primitive

Status: Accepted
Decision date: 2026-09-12
Canonical owner: Wayfinder

## Decision

Define one domain-neutral Lineage / Version / Delta semantic primitive for representing identity-preserving change through time. Media editions, laws, software, products, buildings, vehicles, standards, curricula, and Polaris artifacts are projections of this primitive, not separate comparison systems.

Wayfinder owns the meaning and invariants. Commons may package contracts. ARK stores immutable versions/evidence/history. Scribe may compile deterministic derived lineage and delta projections. Aurora may present views without redefining semantics.

## Existing capability / harvest

Wayfinder already owns identity and relationship models and contains graph/timeline/provenance material. ARK already owns version history and immutable evidence. Scribe already owns deterministic graph projections. The new primitive harvests those capabilities rather than introducing a parallel domain-specific subsystem.

## Canonical model

- `Subject`: stable identity whose state changes.
- `Version`: immutable observation/reference to one subject state.
- `Parent`: directed predecessor relation between versions of the same subject.
- `Lineage`: bounded acyclic graph induced by version-parent relations.
- `Snapshot`: comparable projection of a version as named fields/items.
- `Delta(old,new)`: directional derived comparison with `added`, `removed`, and `changed` members.
- `ViewPreset`: declarative presentation/query preference selecting fields/order/filtering; it cannot alter canonical versions or delta semantics.

A lineage may branch or converge; it is not required to be a single chain. Cycles are invalid. Missing parents are invalid unless explicitly represented as unresolved external references by a future compatible extension.

## Invariants

1. Subject identity is distinct from version identity.
2. Versions are immutable observations/references, not mutable current state.
3. Parent edges are directional: parent -> child.
4. A lineage is acyclic.
5. Every resolved parent belongs to the same subject as its child.
6. `Delta(a,b)` is directional and must not be silently treated as symmetric.
7. Added/removed/changed results are deterministic for the same normalized inputs.
8. Raw observations remain canonical; deltas and views are rebuildable derived projections.
9. Traversal and comparison must be explicitly bounded by implementations.
10. Presentation presets cannot change meaning or evidence.

## Delta semantics

For normalized key/value snapshots A (old) and B (new):

- `added`: keys in B but not A, paired with B values.
- `removed`: keys in A but not B, paired with A values.
- `changed`: keys in both where values differ, paired `(old,new)`.
- unchanged keys are omitted by default.

Outputs use stable key ordering. Equality is exact at the semantic boundary unless a domain-specific normalizer is explicitly supplied upstream.

## Cross-domain use

The same primitive supports edition cuts, statute amendments, software releases, product revisions, building design revisions, vehicle generations/configurations, standards revisions, curriculum editions, and Polaris architecture/code evolution. Domain adapters provide subject/version identifiers and normalized snapshots; they do not redefine lineage or delta.

## Ownership and compatibility

No ownership transfer occurs. This RFC adds a Wayfinder semantic model inside its existing identity/relationship/knowledge mandate. It is backward compatible and additive.

## Failure model

Implementations must reject duplicate version IDs, unknown resolved parents, cross-subject parent edges, cycles, invalid traversal bounds, and requests whose configured resource limit is exceeded. Failures are explicit and non-partial.

## Review outcome

Accepted under the repository-owner direction to implement the generalized capability. The implementation must remain bounded, deterministic, evidence-preserving, and owner-qualified.
