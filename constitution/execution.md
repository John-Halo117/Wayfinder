# Execution Semantics

Wayfinder repository organization and Wayfinder execution semantics are independent.

Repository topology is organized by responsibility. Execution describes how knowledge and action move through the system.

## Canonical Execution Flow

```text
Reality
  -> Observation Source
  -> Observation
  -> Ephemeral Computation
  -> Proof
  -> Promotion
  -> Durable Knowledge
  -> Navigation
  -> Action
```

## Execution Order

### Reality

Reality is what exists before Wayfinder represents it.

Reality is not owned by an engine. ARK preserves observations of reality, but reality itself precedes ARK.

### Observation

Observation records what was seen, received, measured, fetched, or reported.

Observation precedes interpretation. Observation does not decide what the observation means.

Observation Sources produce canonical observation-shaped records from external
source material. ARK preserves those records into append-only reality when they
satisfy the Observation Contract.

### Source Relationships

Source Relationships are explicit relationships present in source data. They
are observed before interpretation and may be preserved by ARK as source
evidence. WEAVE may later interpret, extend, or promote durable relationship
topology from preserved evidence, but source preservation is not topology
ownership.

### Import Profiles

An Import Profile bounds an import run before execution begins. It defines
resource limits, validation posture, runtime expectations, and replay behavior.
Import Profiles keep large local imports deterministic and reviewable without
changing source facts.

### Ephemeral Computation

Ephemeral computation is disposable work performed over observations, representations, evidence, routes, simulations, or candidates.

Ephemeral computation may produce projections, summaries, hypotheses, indexes, simulations, or candidate interpretations. These are not durable knowledge until proven.

Ephemeral computation should retrieve the smallest sufficient representation
needed for the current objective. It should prefer indexes over scans, metadata
over content, summaries over complete documents, relationships over exhaustive
traversal, deltas over rescans, hashes over byte comparisons, and references
over duplication.

Canonical retrieval escalates only when confidence is insufficient:

```text
Reality
  -> Root Inventory
  -> Metadata
  -> Structure
  -> Summary
  -> Relationships
  -> Candidate Selection
  -> Targeted Retrieval
  -> Full Content
```

Full content retrieval is the last step, not the default.

### Proof

Proof validates whether an ephemeral result can be trusted enough for promotion.

Proof may include validation, confidence, supporting evidence, contradiction checks, policy checks, consensus, or rollback evidence.

### Promotion

Promotion intentionally moves proven information into its canonical durable owner.

Promotion must preserve provenance and rollback context. Promotion must not create duplicate ownership.

### Durable Knowledge

Durable knowledge is promoted knowledge in its canonical home.

Durable knowledge may be consumed by engines, domains, internal applications, operations, or future proofs. It remains traceable to observation, evidence, and proof.

### Navigation

Navigation uses durable knowledge, objectives, capabilities, constraints, and uncertainty to choose bearings and routes.

Navigation does not rewrite reality. Navigation does not make commitments by itself.

### Action

Action changes the world or a system state.

Action produces new reality. The results of action must be observed again rather than assumed. This closes the execution loop through Reality and Observation.

## Promotion And Durability

Nothing becomes durable without proof.

Durability is intentional. Ephemeral state, transient computation, simulations, drafts, projections, and route candidates remain disposable until promoted.

Promotion belongs to the canonical owner of the concept being promoted. For example, observation language belongs to contracts, reality preservation behavior belongs to ARK, reusable identity implementation belongs to Identity Service, and commitments belong to MICE.

## Feedback Into Reality

Actions produce effects. Effects are not automatically knowledge.

Wayfinder must observe the effects of action, preserve evidence, and pass any durable conclusion through proof and promotion. This prevents plans, expectations, or recommendations from overwriting reality.

## Repository Topology Is Independent

The top-level repository structure is not an execution pipeline.

`constitution/`, `contracts/`, `services/`, `engines/`, `domains/`, and other top-level directories are ownership homes. They classify responsibility. They do not imply that code or concepts execute in directory order.

Engine lifecycle folders such as `ingress/`, `reality/`, `ephemeral/`, `proofs/`, `core/`, and `egress/` are local engine organization patterns. They do not replace the universal execution flow described here.
