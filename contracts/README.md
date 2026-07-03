# Contracts

Contracts define what crosses constitutional boundaries.

Engines define how contracts are fulfilled. Contracts define the stable language exchanged between engines, services, domains, internal applications, external integrations, operations, and tooling.

Contracts contain no runtime behavior, implementation APIs, storage formats, or engine internals.

## Required Contract Set

| Contract | Producer | Primary Output |
| --- | --- | --- |
| [Observation](observations/README.md) | ARK | Observation |
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
| [Universal Asset Ingestion Pipeline](ingestion/README.md) | Universal Asset Ingestion | Ingestion stage artifacts |
| [Digital Groundskeeper Observation Report](digital-groundskeeper-observation-reports/README.md) | Digital Groundskeeper | Observation report |
| [Digital Groundskeeper Inventory](digital-groundskeeper-inventories/README.md) | Digital Groundskeeper | Digital asset inventory |
| [Digital Groundskeeper Recommendation](digital-groundskeeper-recommendations/README.md) | Digital Groundskeeper | Digital maintenance recommendation |

## Supporting Contracts

Existing supporting contracts remain canonical for shared language: identities, events, policies, permissions, health, schemas, storage, provenance, views, ingestion stage artifacts, and observe-only digital maintenance reports, digital asset inventories, and approval-gated maintenance recommendations.

## Governance Reports

- [Dependency Graph](dependency-graph.md)
- [Ownership Matrix](ownership-matrix.md)
- [Gap Analysis](gap-analysis.md)
- [Duplicate Contract Analysis](duplicate-analysis.md)
- [Constitutional Verification](verification.md)
