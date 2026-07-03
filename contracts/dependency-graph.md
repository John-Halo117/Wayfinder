# Contract Dependency Graph

Contracts flow from more foundational concepts toward more derived concepts. The graph is acyclic. Context may frame Observation, but Context does not require Observation for its own definition or identity.

```text
Reality
  ↓
Context
  ↓
Observation
  ↓
Evidence + Provenance
  ↓
Asset
  ↓
Representation + Relationship + Capability Availability
  ↓
Interpretation and Reasoning outputs through Evidence/Proof
  ↓
Bearing
  ↓
Recommendation
  ↓
Commitment
  ↓
Transformation / Capsule / Specification as durable or reusable downstream artifacts
  ↓
Promotion
```

## Contract Edges

| From | To | Meaning |
| --- | --- | --- |
| Context | Observation | Observations may reference a situational frame. |
| Observation | Evidence | Evidence supports claims using observations. |
| Provenance | Evidence | Evidence must remain traceable. |
| Evidence | Proof | Proof evaluates evidence. |
| Evidence + Provenance | Asset | Asset knowledge requires support and traceability. |
| Asset + Context | Relationship | Relationships connect assets under context. |
| Capability Grammar | Capability Availability | Capability availability references canonical verbs. |
| Asset + Context | Capability Availability | Capabilities attach to assets in context. |
| Representation | Interpretation | Representations can be interpreted. |
| Evidence + Relationship | Reasoning | Reasoning evaluates derived claims. |
| Reasoning output | Bearing | Bearings use reasoned conclusions. |
| Bearing | Recommendation | Recommendations propose routes from bearings. |
| Recommendation | Commitment | MICE may turn accepted recommendations into commitments. |
| Asset + Capability Availability | Transformation | ZWLib maps possible transformations. |
| Context + Evidence | Capsule | Capsules preserve re-entry continuity. |
| Proof | Promotion | Promotion requires proof. |
| Promotion | Durable Knowledge | Promoted outputs become durable in canonical owners. |

## Cycle Rule

No contract may depend on a more derived contract for its own identity. Derived contracts may reference foundational contracts, but foundational contracts must not require derived contracts to exist.


## Universal Asset Ingestion Contract Graph

Universal Asset Ingestion introduces stage contracts that depend on existing constitutional language. The graph remains acyclic and points from more foundational observations toward derived ingestion candidates.

```text
Reality
  ↓
Acquisition
  ↓
Format Detection
  ↓
Canonicalization
  ↓
Semantic Normalization
  ↓
Chunking
  ↓
Identity Assignment
  ↓
Deduplication
  ↓
Compression
  ↓
Content Addressing
  ↓
Knowledge Extraction
  ↓
ARK
```

Provenance is required across every edge as an evidence envelope. It does not alter the stage order or create a second owner for provenance language; canonical provenance language remains in `contracts/provenance/`.

## Universal Asset Ingestion Edges

| From | To | Meaning |
| --- | --- | --- |
| Reality | Acquisition | Source material comes under Wayfinder attention. |
| Acquisition | Format Detection | Acquired candidates can be classified by format without interpretation. |
| Format Detection | Canonicalization | Detected format selects a canonical representation path. |
| Canonicalization | Semantic Normalization | Canonical representations can be aligned to Wayfinder language. |
| Semantic Normalization | Chunking | Normalized artifacts can be split into bounded evidence-ready units. |
| Chunking | Identity Assignment | Bounded units can reference or propose identity through the Identity Service. |
| Identity Assignment | Deduplication | RID and alias evidence supports duplicate assessment. |
| Deduplication | Compression | Duplicate assessment can inform derived compact representations without deleting evidence. |
| Compression | Content Addressing | Derived and canonical representations can receive integrity references. |
| Content Addressing | Knowledge Extraction | Addressed artifacts can support evidence-backed candidate extraction. |
| Knowledge Extraction | ARK | ARK consumes candidates for proof-gated reality preservation. |
| Provenance | All Ingestion Stages | Every stage artifact must remain source and derivation traceable. |


## Digital Groundskeeper Observation Report Graph

Digital Groundskeeper reports depend on foundational reality, asset, evidence, provenance, policy, and storage language. Reports do not create durable truth or authorize action by themselves.

```text
Reality
  ↓
Observation
  ↓
Evidence + Provenance
  ↓
Asset in Context
  ↓
Digital Groundskeeper Observation Report
  ↓
Recommendation / Approval Boundary
  ↓
Future approved execution plan
```

| From | To | Meaning |
| --- | --- | --- |
| Observation | Digital Groundskeeper Observation Report | Reports begin from observed digital reality. |
| Evidence + Provenance | Digital Groundskeeper Observation Report | Facts and interpretations require support and traceability. |
| Asset in Context | Digital Groundskeeper Observation Report | Digital objects are assessed as assets supporting capabilities. |
| Policy | Approval Boundary | Policy frames what may be recommended or requires human approval. |
| Digital Groundskeeper Observation Report | Recommendation | Recommendations remain separate from action and commitment. |


## Digital Groundskeeper Inventory Graph

Digital Groundskeeper inventories depend on the Asset model and foundational evidence language. They sit between observation and interpretation in the Digital Groundskeeper execution grammar.

```text
Reality
  ↓
Observation
  ↓
Evidence + Provenance
  ↓
Asset in Context
  ↓
Digital Groundskeeper Inventory
  ↓
Digital Groundskeeper Observation Report
  ↓
Future Recommendation Contract
```

| From | To | Meaning |
| --- | --- | --- |
| Observation | Digital Groundskeeper Inventory | Inventory records what exists before interpretation. |
| Evidence + Provenance | Digital Groundskeeper Inventory | Inventory facts require support and traceability. |
| Asset in Context | Digital Groundskeeper Inventory | Digital objects are inventoried as contextual assets. |
| Relationship + Capability | Digital Groundskeeper Inventory | Inventory records dependency and capability support evidence. |
| Digital Groundskeeper Inventory | Digital Groundskeeper Observation Report | Reports consume inventory facts as evidence. |


## Digital Groundskeeper Recommendation Graph

Digital Groundskeeper recommendations depend on observation reports and inventories. They remain planning artifacts until approval and never authorize action by themselves.

```text
Digital Groundskeeper Observation Report
  ↓
Digital Groundskeeper Inventory
  ↓
Digital Groundskeeper Recommendation
  ↓
Approval Boundary
  ↓
Future Execution Plan
```

| From | To | Meaning |
| --- | --- | --- |
| Observation Report | Digital Groundskeeper Recommendation | Recommendations cite facts, interpretations, and unknowns. |
| Inventory | Digital Groundskeeper Recommendation | Recommendations cite asset, relationship, dependency, capability, and continuity evidence. |
| Policy | Approval Boundary | Policy frames what requires approval and what must not be recommended. |
| Digital Groundskeeper Recommendation | Approval Boundary | Recommendations request approval when action may follow. |
| Digital Groundskeeper Recommendation | Future Execution Plan | Only approved recommendations may feed later execution planning. |
