# Decision Record: Legal Primitive Teloi Integration

EDR ID: WAYFINDER-2026-09-12-LEGAL-PRIMITIVES  
Date: 2026-09-12  
Affected scope IDs: Teloi, legal-policy semantics, Reality semantics, decision semantics, proposal/news semantics

## Problem

Small changes to legal primitives can create effects far larger than their textual footprint. Existing policy tracking can miss these changes when it ranks by bill size, spending amount, headline salience, or domain label. At the same time, promoting favored reforms directly into Teloi would collapse objectives into mechanisms and make the system less corrigible.

## Decision

Adopt Foundational Legal Delta as a cross-domain semantic class and Legal Primitive Refactor as a stable doctrine candidate.

Teloi expresses the desired legal-system state: consequential rules should be legible, causally justified, corrigible, difficult to game, and free of arbitrary high-leverage boundaries where changing those boundaries improves the protected objectives.

Specific reforms remain candidate mechanisms. They are evaluated through typed legal-primitive deltas, explicit affected-population denominators, causal propagation, counterfactuals, externalities, distribution, institutional constraints, evidence, uncertainty, and reevaluation triggers.

Reality and operationalization layers inherit this semantic contract. They may implement detectors, propagation graphs, leverage screening, simulation, and monitoring, but they do not redefine the Telos.

## Why This Solution

It captures a recurring high-leverage phenomenon once at the highest accurate abstraction. It also preserves the distinction between desired state and implementation, allowing the system to endorse, modify, or reject individual reforms as evidence changes.

## Alternatives Considered

1. Encode each favored reform directly in Teloi. Rejected because it promotes mechanisms into objectives and causes drift.
2. Keep the capability inside labor policy only. Rejected because the same primitive-change structure occurs in tax, immigration, elections, housing, land use, welfare, healthcare, finance, trade, environmental law, procedure, criminal law, communications, AI, agriculture, and federalism.
3. Use a single legal-leverage score. Rejected as the canonical representation because it can hide non-dominated tradeoffs and uncertainty. Scalar rollups remain optional triage aids.
4. Treat only enacted statutory text as legal state. Rejected because regulation, guidance, enforcement, litigation, injunctions, and precedent can change effective law without changing the statute.

## Tradeoffs

- More semantic structure is required for policy objects.
- High-leverage detection can create false positives when a textual delta has little behavioral response.
- Counterfactual analysis adds work relative to headline tracking.
- Preserving multidimensional effects limits simple rankings, but prevents false precision.

These costs are accepted because they improve causal fidelity and reduce systematic blind spots.

## Assumptions

- Legal primitives frequently function as shared dependencies for many downstream behaviors and programs.
- Behavioral response varies by domain and must not be assumed from textual magnitude alone.
- Existing Reality, decision, and proposal systems can consume the semantic contract without Wayfinder owning their runtime implementation.

## Optionality Preserved

- No particular labor, tax, welfare, immigration, licensing, or other reform is made canonical by this decision.
- Leverage models may use qualitative, ordinal, interval, probabilistic, or quantitative components as evidence permits.
- Runtime implementations remain replaceable.

## Optionality Spent

- Wayfinder commits to treating objective/mechanism separation, affected-population denominators, uncertainty separation, causal propagation, and reevaluation as required semantics for foundational legal deltas.

## Reevaluation Triggers

- repeated cases where the primitive model fails to predict meaningful propagation
- evidence that a required field consistently adds no decision value
- discovery of a more general cross-domain representation that subsumes this model
- conflict with higher constitutional authority
- implementation experience showing systematic ambiguity or gaming

## Verification Method

A conforming implementation should be able to represent a legal delta such as a 40-to-32-hour overtime threshold without equating reduced hours with lost jobs; preserve headcount, hours, earnings, prices, output, automation, and affected populations as distinct quantities; compare no-change and alternative reforms; and revise the recommendation when observed reality diverges from the modeled causal chain.

## Relationships

- Doctrine: `BUILD_BIBLE/doctrine/legal-primitive-refactor.md`
- Schema: `BUILD_BIBLE/schemas/legal-primitive-delta.schema.json`
- Governance: `BUILD_BIBLE/governance/stable-principle-promotion.md`
- Decision standard: `BUILD_BIBLE/lifecycle/decisions/engineering-decision-record-standard.md`
