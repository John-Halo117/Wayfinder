# External World State Contract

**Semantic owner:** Wayfinder  
**Artifact identity:** `wayfinder.external-world-state`  
**Semantic version:** `0.1.0-alpha.18`  
**Producer:** Reasoning  
**Compatibility:** additive alpha contract; legacy `Operative State` and `Current Head` names are accepted as compatibility aliases only  
**Supersession:** canonicalizes the previously distributed EWS / Operative-State concept without selecting an implementation

## Purpose

External World State (EWS) is the smallest qualified, current-enough representation of reality required for downstream navigation, planning, comparison, execution, and verification.

EWS is **derived state**, not raw reality and not a durable-evidence store. It is produced from qualified evidence and reasoned conclusions while preserving uncertainty, provenance references, scope, time, and material unresolved contradictions.

The core flow is:

`Observation -> Evidence -> Interpretation -> Reasoning -> External World State -> Bearing/Recommendation/Commitment`

This contract defines what may cross the Reasoning boundary as world state. It defines no storage engine, graph database, serialization format, API, runtime, synchronization mechanism, or implementation language.

## Required Semantic Fields

An EWS artifact must carry enough information to preserve these meanings, regardless of representation:

- **scope** — the population, system, place, object, task, or domain for which the state is asserted;
- **as-of** — the observation/inference time boundary to which the state applies;
- **claims** — qualified state assertions or relations;
- **epistemic type** — observation, inference, estimate, prediction, assumption, preference, recommendation, contested claim, or unknown where material;
- **evidence references** — links to the evidence/provenance supporting state claims rather than copied evidence masquerading as state;
- **uncertainty** — confidence, ambiguity, unknowns, contradictions, or bounds at the cheapest adequate resolution;
- **validity / staleness conditions** — known conditions under which the state must be recomputed, invalidated, or treated as stale;
- **supersession linkage** — predecessor/successor relationship when this state replaces another qualified state.

Implementations may use additional fields, but may not erase these distinctions when they are material to a downstream decision.

## State Relations

### Baseline

A **Baseline** is an explicitly selected comparison state for a specified objective, scope, population, metric, or counterfactual. A baseline is not automatically "the previous state" and must preserve its selection rule.

### Successor

A **Successor** is a state that validly supersedes a predecessor for a defined scope. Succession does not imply improvement. A successor may be better, worse, mixed, equivalent, or unknown relative to a baseline.

### Reachability

**Reachability** is the qualified relation between a current state and a candidate state under known constraints, capabilities, authority, and time. Reachable is not the same as desirable, recommended, or committed.

### Twin

A **Twin** is a maintained representation tied to an external referent and updated through evidence. A twin is not the referent itself. Fidelity, coverage, staleness, uncertainty, and provenance remain explicit.

## Compatibility Aliases

- `External World State` / `EWS` — canonical name.
- `Operative State` — accepted compatibility alias when it means the qualified state used for action/navigation.
- `Current Head` — deprecated compatibility alias; consumers must not infer branch-head, ledger-head, or evidence-head semantics from this name.

Aliases are retrieval/migration aids, not independent models. New semantic artifacts should emit the canonical name.

## Ownership and Boundaries

- **Wayfinder** owns the semantic definition and compatibility rules for EWS.
- **Reasoning** produces EWS artifacts from evidence and interpretations.
- **ARK** owns durable evidence/provenance; EWS references that reality record rather than replacing it.
- **Interpretation** owns candidate meanings, not final world-state inference.
- **Jarvis** consumes EWS to produce Bearings and Recommendations; it does not redefine reality state.
- **MICE / execution systems** may consume state and commitments but do not gain authority merely by possessing a state representation.
- **Views / Aurora / applications** project EWS for humans; a presentation is not canonical state.

Capability and authority remain orthogonal. A state claim never grants permission to act.

## Invariants

1. Reality outranks the model; contradictory qualified evidence can invalidate EWS.
2. Evidence and state are distinct artifacts.
3. Unknown is preserved as unknown; missing data is not false.
4. Predictions are not silently promoted to observations or current facts.
5. Scope, population, denominator, time, and units travel with quantitative state when material.
6. Derived representations preserve provenance sufficient to re-evaluate consequential claims.
7. Supersession is explicit; consumers must not rely on filename order or wall-clock recency alone.
8. Stale state may be useful but must not present as current state once its validity conditions fail.
9. No consumer may mutate canonical evidence by editing EWS.
10. Presentation-specific simplification may compress redundancy, not consequential meaning.

## Implementation Obligation

Executable implementations live in implementing repositories/components. They must demonstrate contract conformance, deterministic behavior where semantics require it, uncertainty/provenance preservation, invalidation/recomputation behavior, and compatibility handling before claiming support for this contract.
