# Contract Dependency Graph

Contracts flow from more foundational concepts toward more derived concepts.

```text
Reality
  ↓
Observation
  ↓
Evidence + Provenance
  ↓
Asset + Context
  ↓
Representation + Relationship + Capability
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
| Observation | Evidence | Evidence supports claims using observations. |
| Evidence | Proof | Proof evaluates evidence. |
| Provenance | Evidence | Evidence must remain traceable. |
| Asset | Context | Assets are interpreted in context. |
| Asset + Context | Relationship | Relationships connect assets under context. |
| Asset + Context | Capability | Capabilities attach to assets in context. |
| Representation | Interpretation | Representations can be interpreted. |
| Evidence + Relationship | Reasoning | Reasoning evaluates derived claims. |
| Reasoning output | Bearing | Bearings use reasoned conclusions. |
| Bearing | Recommendation | Recommendations propose routes from bearings. |
| Recommendation | Commitment | MICE may turn accepted recommendations into commitments. |
| Asset + Capability | Transformation | ZWLib maps possible transformations. |
| Context + Evidence | Capsule | Capsules preserve re-entry continuity. |
| Proof | Promotion | Promotion requires proof. |
| Promotion | Durable Knowledge | Promoted outputs become durable in canonical owners. |

## Cycle Rule

No contract may depend on a more derived contract for its own identity. Derived contracts may reference foundational contracts, but foundational contracts must not require derived contracts to exist.
