# Wayfinder System Architecture v1

This document records the end-to-end system architecture for the knowledge
pipeline established through the Phase 2-7 implementation work.

It is an orientation document. Canonical ownership remains with the Constitution,
contracts, services, and engine README files.

## Canonical Data Pipeline

The Truth Pipeline:

```text
Reality
  |
  v
Observation Sources
(Oracles / Integrations)
  |
  v
Observation Contract
  |
  v
ARK
Reality Preservation Engine
  |
  v
Canonical Language
(Derived Language Substrate)
  |
  v
Knowledge Compiler
(Candidate Knowledge)
  |
  v
Knowledge Governance
(Review / Promotion)
  |
  v
Durable Knowledge
  |
  v
Knowledge Retrieval Indexes
(Disposable)
  |
  v
Knowledge Views
  |
  v
Continuity Capsules
  |
  v
Reasoning
(Future)
  |
  v
Jarvis
(Future)
```

## Constitutional Rule

Only ARK preserves reality.

Observation Sources produce canonical observation-shaped records.

ARK preserves observations and explicit Source Relationships.

WEAVE owns durable relationship topology.

Everything below ARK is derived.

Everything below ARK can be rebuilt, except explicitly promoted durable
knowledge records.

## Engine Dependency Graph

```text
Reality
  |
  v
Oracles
  |
  v
ARK
  |\
  | +--> Identity Service
  | +--> Storage Service
  | +--> Event Bus
  | +--> Policy / Configuration
  |
  v
Canonical Language
  |
  v
Knowledge Compiler
  |
  v
Knowledge Governance
  |
  v
Knowledge Retrieval
  |
  v
Knowledge Views
  |
  v
Continuity Capsules
  |
  v
Reasoning
  |
  v
Jarvis
```

Every dependency points downward or sideways into a supporting service boundary.
No lower layer may depend on a higher layer.

## Constitutional Layer Model

```text
Layer 0   Reality
Layer 1   Observation Sources / Oracles
Layer 2   Observation Contract
Layer 3   ARK / Reality Preservation
Layer 4   Canonical Language / Derived Language Substrate
Layer 5   Interpretation / Knowledge Compiler
Layer 6   Governance / Knowledge Governance
Layer 7   Durable Knowledge
Layer 8   Retrieval
Layer 9   Views
Layer 10  Capsules
Layer 11  Reasoning
Layer 12  Navigation / Jarvis
```

## Supporting Services

Supporting services are horizontal capabilities available to multiple layers.
They provide reusable infrastructure and do not own layer-specific business
logic.

```text
Identity
Storage
Configuration
Policy
Event Bus
Discovery / NOMAD
Telemetry / VALOR
Relationship Topology / WEAVE
```

## Information Flow

```text
Reality
  |
  v
Observation Source
  |
  v
Observation
  |
  v
Evidence
  |
  v
Preservation
  |
  v
Canonical Language
  |
  v
Candidate Knowledge
  |
  v
Review
  |
  v
Promotion
  |
  v
Durable Knowledge
  |
  v
Indexes
  |
  v
Views
  |
  v
Capsules
  |
  v
Reasoning
  |
  v
Navigation
```

## Ownership Model

```text
Reality              owns itself
Oracles              observe
ARK                  preserves observations, Source Relationships, provenance, replay, and LVR
Canonical Language   normalizes derived language
Knowledge Compiler   proposes
Knowledge Governance approves
Durable Knowledge    remembers
Retrieval            indexes
Views                project
Capsules             compress continuity
Reasoning            evaluates
Jarvis               navigates
```

## Constitutional Invariants

- Reality is never modified.
- Observations are append-only.
- Provenance is never discarded.
- Observation Sources discover and parse; ARK preserves.
- Source Relationships are explicit source evidence; WEAVE owns durable topology.
- Identity is owned by the Identity Service.
- Relationship topology is owned by WEAVE.
- ARK preserves reality but does not reason.
- Canonical Language is derived, rebuildable, and not knowledge.
- The Knowledge Compiler proposes but never preserves.
- Knowledge Governance promotes but never rewrites history.
- Durable Knowledge is the canonical knowledge store.
- Retrieval indexes are disposable.
- Views never own knowledge.
- Capsules preserve continuity, not reality.
- Reasoning never changes knowledge.
- Jarvis never becomes a source of truth.

## Replaceability Boundaries

These implementations can be replaced independently as long as constitutional
contracts remain stable:

- Observation Sources
- Import Profiles
- Canonical Language implementation
- Storage backend
- Search backend
- Embedding model
- Retrieval implementation
- View implementation
- Capsule implementation
- Reasoning implementation
- Navigation implementation

## Future Engines

Planned but intentionally not implemented here:

1. Reasoning Engine
2. Jarvis Navigation Engine
3. Sandbox / Simulation
4. Execution Engine
5. Mission Engine
6. Affordance Engine
7. Opportunity Bundle Engine
8. Attention Filter

These consume approved knowledge rather than raw observations.

## System Philosophy

```text
Observe Reality
  |
  v
Preserve Reality
  |
  v
Interpret Reality
  |
  v
Govern Knowledge
  |
  v
Remember Knowledge
  |
  v
Retrieve Knowledge
  |
  v
Project Knowledge
  |
  v
Compress Continuity
  |
  v
Reason
  |
  v
Navigate
```

Every stage has exactly one primary responsibility.

Every stage is independently replaceable.

Every stage preserves the constitutional separation between reality, knowledge,
and navigation.

## First Contact Alignment

First Contact validated the following refinements:

- Observation Sources produce observation-shaped records; ARK preserves them.
- ARK may preserve explicit Source Relationships without owning WEAVE topology.
- Import Profiles are required for large private imports.
- Candidate paging and grouped governance intake are required before real
  export-scale candidate review.
- Private validation outputs under `.wayfinder-validation/` remain local and
  must not be committed.

## Canonical References

- Constitution: [constitution/](../constitution/README.md)
- Engine boundaries: [engines/README.md](../engines/README.md)
- Observation Contract: [contracts/observations/README.md](../contracts/observations/README.md)
- Promotion Contract: [contracts/promotion/README.md](../contracts/promotion/README.md)
- View Contract: [contracts/views/README.md](../contracts/views/README.md)
- ARK: [engines/ark/README.md](../engines/ark/README.md)
- Interpretation: [engines/interpretation/README.md](../engines/interpretation/README.md)
- Views: [engines/views/README.md](../engines/views/README.md)
- Capsules: [engines/capsules/README.md](../engines/capsules/README.md)
- Reasoning: [engines/reasoning/README.md](../engines/reasoning/README.md)
- Jarvis: [engines/jarvis/README.md](../engines/jarvis/README.md)
