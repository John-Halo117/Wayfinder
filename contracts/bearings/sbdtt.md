# Sparse Bipolar Dimensional Trend Tensor (SBDTT)

**Semantic owner:** Wayfinder  
**Artifact identity:** `wayfinder.sbdtt`  
**Semantic version:** `0.1.0-alpha.19`  
**Producer:** Bearing/decision-model implementations  
**Status:** Canonical evaluated-projection contract

## Purpose

SBDTT is the default cross-domain **evaluated projection** when multiple orthogonal dimensions materially change interpretation or action.

It is not a universal storage format. Raw evidence, events, identities, relations, accounting ledgers, graphs, fields, and state machines remain in their native canonical representations. SBDTT is derived from them for Bearings, comparison, prioritization, and human projection.

`Reality -> Evidence -> External World State / Domain State -> SBDTT -> Bearings / Decision / Projection`

## Canonical Coordinate

A tensor cell is addressed only by dimensions that independently change meaning. The default sparse coordinate is:

`T[domain, dimension, objective, scope, time, horizon]`

Implementations may omit axes that do not change interpretation and may add an axis only when treating it as an attribute would lose consequential information.

## Orthogonal Evaluation Fields

The following meanings are independent and MUST NOT be collapsed:

- **polarity**: positive / neutral / negative relative to the named objective;
- **operational state**: Blue / Green / Yellow / Red;
- **epistemic state**: White / Gray / Black;
- **trend**: up / stable / down, always meaning more / stable / less of the named property.

`polarity != operational state != epistemic state != trend`

Neutral means known no-material-effect. It is not unknown.

Observed trend is not forecast trajectory.

Physical magnitude is not consequence.

Membership strength or effect strength is not epistemic confidence.

## Payload

A material cell may contain:

- raw or normalized magnitude;
- named-property 1-10 magnitude where useful;
- compressed grade G1-G5;
- polarity;
- operational state;
- epistemic state;
- trend and optional trend strength;
- consequence;
- reach.

Optional attributes include duration, persistence, timing, recovery, variability, urgency, reversibility, cause, dependency, and source references. These remain attributes unless independent variation earns a coordinate axis.

## Sparse Law

Instantiate or surface only:

- material non-neutral states;
- threshold crossings;
- binding constraints;
- material opportunities;
- consequential trend changes;
- contradictions or unknowns;
- states that change a decision or action policy.

Ordinary healthy state SHOULD collapse away.

Positive and negative consequences may coexist in separate cells. Implementations MUST NOT average benefits and harms into neutrality.

## Monotonic Human Scale

When a common human-readable scale is useful:

- 1 = trace;
- 2 = very low;
- 3 = low;
- 4 = mild;
- 5 = moderate;
- 6 = material;
- 7 = high;
- 8 = very high;
- 9 = severe / exceptional;
- 10 = extreme / limiting.

Every scale MUST name the property. Larger values always mean more of that property.

Compressed grade mapping:

- 1-2 -> G1
- 3-4 -> G2
- 5-6 -> G3
- 7-8 -> G4
- 9-10 -> G5

No unnamed universal goodness score is permitted.

## Representation Stop Rule

Use the cheapest adequate representation:

1. scalar if one value preserves the decision;
2. state machine if transitions dominate;
3. graph / DAG if topology or causality dominates;
4. field if spatial variation dominates;
5. SBDTT when several orthogonal evaluated dimensions materially change interpretation or action.

Do not tensorize data merely for uniformity.

## Composition

Composition is constraint-aware, not arithmetic averaging. Implementations may use max-severity, binding-constraint, threshold, dependency-aware, or objective-specific operators as defined by the domain contract.

An aggregate MUST preserve any child state whose removal would change the resulting action, constraint, or material interpretation.

## Provenance and Reversibility

Every derived cell MUST retain enough references to recover:

- source evidence / canonical state;
- objective or concern against which polarity was evaluated;
- scale/band definition;
- transformation/operator version;
- valid time / horizon;
- uncertainty semantics.

A projection may be recomputed or discarded without loss of canonical source state.
