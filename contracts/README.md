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
| [Standard Reference](standards/README.md) | Domain owner / Evidence | Selected external standard or interface reference |
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

## Human Interface Contract

- [Ontology Self-Resolution](human-interface-ontology-self-resolution-v1.md) — Polaris resolves canonical names, owners, operators, standards, providers, aliases, symptoms, and examples internally. Ordinary users state intent; technical names are progressive disclosure, not required vocabulary. Default human navigation is World / Life / Things / Plans / System with at most two levels exposed by default.

## Habitat Assumption Scope

- [Habitat Assumption Scope](habitat-assumption-scope-v1.md) — scopes Sanctuary/Build Bible assumptions as SHARED, GH, MH, CAMPUS, UNKNOWN_SCOPE, or N/A; makes one occupied story a shared protected constraint; prevents GH compression rules from silently contaminating MH; and quarantines unresolved historical assumptions instead of inheriting them universally.

## Corpus-Wide Survivor Operators

- [Cross-Domain Survivor Operators](cross-domain-survivor-operators-v1.md) — admitted operators, policies, projections, metrics, and verification gates recovered from the corpus-wide delta reconciliation without creating new sovereign owners.

## Standards-First Physical Resolution

Physical interfaces and subsystems must resolve requirements against applicable external standards and mature interoperable interfaces before a custom physical interface is proposed. Polaris owns selection, mapping, composition, lifecycle, and residual justification; it does not create a parallel physical standards ecosystem merely for internal naming consistency.

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
