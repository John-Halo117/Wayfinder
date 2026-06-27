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
