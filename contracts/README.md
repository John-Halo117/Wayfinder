# Contracts

Contracts define what crosses constitutional boundaries.

Engines define how contracts are fulfilled. Contracts define the stable language exchanged between engines, services, domains, internal applications, external integrations, operations, and tooling.

Contracts contain no runtime behavior, implementation APIs, storage formats, or engine internals.

## Required Contract Set

| Contract | Producer | Primary Output |
| --- | --- | --- |
| [Observation](observations/README.md) | Observation Source role | Observation |
| [Evidence](evidence/README.md) | ARK | Evidence |
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

## Supporting Contracts

Existing supporting contracts remain canonical for shared language: identities, events, policies, permissions, health, schemas, storage, provenance, and views.

## First Contact Clarification

Observation Sources produce observation-shaped records. ARK preserves those
records into append-only reality. ARK may also preserve explicit Source
Relationships as evidence, while WEAVE remains the owner of durable
relationship topology.

## Governance Reports

- [Dependency Graph](dependency-graph.md)
- [Ownership Matrix](ownership-matrix.md)
- [Gap Analysis](gap-analysis.md)
- [Duplicate Contract Analysis](duplicate-analysis.md)
- [Constitutional Verification](verification.md)
