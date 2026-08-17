# Contracts

Contracts define what crosses constitutional boundaries.

Engines define how contracts are fulfilled. Contracts define the stable language exchanged between engines, services, domains, internal applications, external integrations, operations, and tooling.

Contracts contain no runtime behavior, implementation APIs, storage formats, or engine internals.

## Required Contract Set

| Contract | Producer | Primary Output |
| --- | --- | --- |
| [Observation](observations/README.md) | Observation Source role | Observation |
| [Evidence](evidence/README.md) | ARK | Evidence |
| [External World State](world-state/README.md) | Reasoning | External World State |
| [Representation](representations/README.md) | Views | Representation |
| [Asset](assets/README.md) | ARK | Asset in Context reference |
| [Context](context/README.md) | ARK | Context reference |
| [Relationship](relationships/README.md) | WEAVE | Relationship |
| [Capability](capabilities/README.md) | NOMAD | Capability/provider option |
| [Bearing](bearings/README.md) | Jarvis | Bearing |
| [Recommendation](recommendations/README.md) | Jarvis | Recommendation |
| [Commitment](commitments/README.md) | MICE | Commitment |
| [Transformation](transformations/README.md) | ZWLib | Transformation Path |
| [Capsule](capsules/README.md) | Capsules | Capsule |
| [Specification](specifications/README.md) | Build Bible | Specification |
| [Proof](proofs/README.md) | ARK | Proof |
| [Promotion](promotion/README.md) | ARK | Promotion record |

## Evaluated Projection Contracts

- [Sparse Bipolar Dimensional Trend Tensor](bearings/sbdtt.md) — default sparse cross-domain evaluated projection when several orthogonal evaluated dimensions materially change interpretation or action.
- [Environmental External-World Projection](world-state/environmental-projection.md) — environmental/local-twin semantics as a projection of EWS rather than a separate world model.
- [Spatial Scope and Jurisdiction](../ontology/spatial-scope.md) — universal spatial, jurisdictional, and functional-scope semantics.
- [Derived Classification](../ontology/classification.md) — classification as a derived relation/projection over stable identity and qualified state.

SBDTT is not a new truth store or mandatory representation. Scalars, state machines, graphs/DAGs, and fields remain preferred when they are cheaper adequate representations.

## Supporting Contracts

Existing supporting contracts remain canonical for shared language: identities, events, policies, permissions, health, schemas, storage, provenance, and views.

## First Contact Clarification

Observation Sources produce observation-shaped records. ARK preserves those
records into append-only reality. ARK may also preserve explicit Source
Relationships as evidence, while WEAVE remains the owner of durable
relationship topology.

Reasoning produces qualified External World State from evidence and
interpretations. External World State is derived state and does not replace
ARK's durable evidence/provenance record.

Jarvis/Bearing implementations may derive SBDTT projections from qualified EWS/domain state relative to a named objective. Those projections remain disposable and must preserve references sufficient to recover their source semantics.

## Governance Reports

- [Dependency Graph](dependency-graph.md)
- [Ownership Matrix](ownership-matrix.md)
- [Gap Analysis](gap-analysis.md)
- [Duplicate Contract Analysis](duplicate-analysis.md)
- [Constitutional Verification](verification.md)
