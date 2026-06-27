# Context Contract

## Purpose

Defines the conditions under which an asset, observation, route, commitment, or proof is interpreted.

## Producer

ARK

Exactly one engine produces this contract across engine boundaries.

## Consumers

Interpretation, Reasoning, Views, Jarvis, ZWLib, Capsules, MICE, VALOR, Blackwall, Domains

## Inputs

Asset, RID, Observation, time, location, objective, actor, capability, constraints, policy, relationship, CivPhys profile.

## Outputs

Context reference, Asset in Context reference, constraint set, objective frame, actor frame.

## Invariants

- Context modifies interpretation without automatically changing identity.
- Context must remain separable from the asset.
- Context claims require evidence when made durable.
- Context must be explicit when it materially changes meaning.

## Failure Modes

Missing context, stale context, conflicting context, unknown actor, unknown objective, or ambiguous constraints are represented as uncertainty.

## Promotion Rules

Context remains ephemeral when used only for temporary interpretation. It becomes durable when ARK promotes evidence-backed contextual knowledge.

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
