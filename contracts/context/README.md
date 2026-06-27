# Context Contract

## Purpose

Defines the conditions under which an asset, observation, route, commitment, or proof is interpreted. Context may frame observations, but it does not require an observation for its own definition or identity.

## Producer

ARK

Exactly one engine produces durable context knowledge across engine boundaries.

## Consumers

Observation, Interpretation, Reasoning, Views, Jarvis, ZWLib, Capsules, MICE, VALOR, Blackwall, Domains

## Inputs

Asset, RID, time, location, objective, actor, capability, constraints, policy, relationship, CivPhys profile, situational conditions.

## Outputs

Context reference, Asset in Context reference, constraint set, objective frame, actor frame, situational frame.

## Invariants

- Context can exist as a situational frame before any observation references it.
- Context modifies interpretation without automatically changing identity.
- Context must remain separable from the asset.
- Context claims require evidence when made durable.
- Context must be explicit when it materially changes meaning.

## Failure Modes

Missing context, stale context, conflicting context, unknown actor, unknown objective, or ambiguous constraints are represented as uncertainty.

## Promotion Rules

Context remains ephemeral when used only for temporary interpretation. It becomes durable when ARK promotes evidence-backed contextual knowledge. Observations may support that proof, but Context does not depend on Observation for its own identity.

## Constitutional Basis

- [Asset Model](../../constitution/assets.md)
- [Execution Semantics](../../constitution/execution.md)
- [Repository Responsibilities](../../constitution/repository.md)
- [Engine Boundaries](../../engines/README.md)

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Domain-specific schemas.
- Engine internals.
