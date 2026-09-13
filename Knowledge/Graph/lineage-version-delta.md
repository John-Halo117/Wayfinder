# Lineage / Version / Delta Model

Canonical semantic owner: Wayfinder  
Status: Approved by RFC-0003

## Purpose

Represent identity-preserving change once, then reuse it everywhere. The model separates immutable observed versions from derived comparisons and presentation.

## Types

### Subject
A stable semantic identity. A subject can be a film, statute, software package, product, building design, vehicle model, standard, curriculum, repository artifact, or any other versionable object.

Required semantic field:
- `subject_id`: stable owner-qualified identifier.

### Version
An immutable reference to one observed state of a Subject.

Required semantic fields:
- `version_id`: unique within the lineage input.
- `subject_id`: subject identity.
- `parents`: zero or more predecessor version IDs.
- `snapshot`: normalized comparable mapping or projection reference.

Optional owner-defined metadata may include timestamps, labels, provenance references, evidence IDs, source IDs, and domain qualifiers. Metadata does not change the core lineage semantics.

### Lineage
A directed acyclic graph of Version nodes connected parent -> child. Branches and merges are valid. Cycles are invalid.

### Delta
A deterministic directional projection from an old snapshot to a new snapshot:
- `added[key] = new[key]` when key exists only in new.
- `removed[key] = old[key]` when key exists only in old.
- `changed[key] = {old: old[key], new: new[key]}` when both exist and differ.

Unchanged values are omitted by default.

### ViewPreset
A declarative request for how a consumer wants a lineage or delta shown: selected dimensions, ordering, grouping, filters, labels, density, or domain-specific lenses. A ViewPreset is never evidence and cannot mutate versions, lineage, or delta output.

## Validation

A conforming resolved lineage must satisfy:

1. version IDs are unique;
2. every parent ID resolves;
3. parent and child have the same `subject_id`;
4. no directed cycle exists;
5. traversal bounds are positive and explicit;
6. resource-cap exhaustion returns an explicit failure, never truncated output presented as complete.

## Determinism

Given identical normalized versions, snapshots, direction, and bounds, a conforming implementation returns identical logical results. Collections exposed as ordered results use stable lexical key/version ordering unless an owner-approved contract specifies another deterministic order.

## Evidence and state

Versions and source observations are canonical inputs. Lineage ordering, ancestry, comparisons, rollups, and UI arrangements are derived state and must be rebuildable. ARK may persist all of them, but persistence does not transfer semantic ownership.

## Domain adapters

Adapters may normalize domain objects into this model. Examples:

- media: theatrical -> director's cut -> remaster;
- law: introduced -> amended -> enacted -> codified revision;
- software: release/tag/commit ancestry and semantic snapshots;
- product: generation -> revision -> configuration;
- building: design revision / permit set / as-built state;
- vehicle: generation / trim / model-year revision;
- standards and curricula: edition / amendment / supersession;
- Polaris: architecture, contract, repository, capability, and implementation revisions.

Adapters may add dimensions but may not invert edge direction, mutate historical versions, or redefine `added`, `removed`, or `changed`.

## Presentation boundary

Aurora and applications consume lineage/delta projections and may provide timeline, fork, side-by-side, matrix, overlay, heatmap, compact-summary, or domain-specific views. These are projections of the same semantic object, not new comparison engines.
