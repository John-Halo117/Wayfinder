# External World State Ontology

This document defines canonical concepts and semantic relationships only. It selects no ontology syntax, graph engine, database, schema language, or runtime.

## Canonical Concept

**External World State (EWS)** is a qualified derived representation of the external or operative reality relevant to a defined scope and as-of boundary.

`EWS != Observation`  
`EWS != Evidence`  
`EWS != Prediction`  
`EWS != View`  
`EWS != Commitment`

EWS may contain conclusions derived from those artifacts, but their epistemic types remain distinguishable.

## Relations

- `SUPPORTED_BY`: a state claim points to evidence/provenance that supports it.
- `INTERPRETS`: an interpretation candidate assigns candidate meaning to evidence/representation.
- `INFERS`: Reasoning derives a qualified state claim or conclusion.
- `SUPERSEDES`: a successor state replaces a predecessor for an explicit scope.
- `BASELINED_AGAINST`: a state is compared with an explicitly selected baseline.
- `REACHABLE_FROM`: a candidate state is achievable from another state under stated constraints/capabilities/authority/time.
- `TWIN_OF`: a maintained representation corresponds to an external referent without becoming identical to that referent.
- `PROJECTED_AS`: a canonical state is rendered as a view/presentation.
- `INVALIDATED_BY`: evidence or changed boundary conditions invalidate a state or claim.

## Canonical Distinctions

### State vs event

An event records or represents a transition occurrence. State represents a qualified condition over a scope/as-of boundary. Events may change state; they are not interchangeable with state.

### Stock vs flow vs rate vs cumulative total

These quantity semantics remain distinct inside state. A consumer must not compare or aggregate them as though they were the same property.

### Baseline vs predecessor

A predecessor is structurally prior in a supersession chain. A baseline is deliberately selected for comparison. They may be the same artifact, but that identity must not be assumed.

### Reachability vs desirability

Reachability answers whether a candidate state can be attained under constraints. Desirability, recommendation, and commitment are separate judgments.

### Twin vs reality

A twin is a representation with a referent, update path, and fidelity limits. Evidence that conflicts with the twin updates or invalidates the twin; the external referent is not changed merely because the representation changes.

## Compatibility

`Operative State` maps to EWS when used for the qualified state that drives navigation/action. `Current Head` is a deprecated alias for the same concept only where historical context proves that meaning. Neither alias creates a second ontology node.
