# View Contract

## Purpose

Defines shared language for projections, perspectives, visualizable slices, and presentation-ready representations of constitutional knowledge.

## Producer

Views

Exactly one engine produces view boundary language. Views present knowledge; they do not own the underlying reality, asset, reasoning, or navigation concepts.

## Consumers

Jarvis, Foundry, Domains, Internal applications, Operators, Capsules, MICE

## Inputs

Asset reference, relationship reference, representation reference, evidence, context, bearing reference, health signal, policy reference, objective frame.

## Outputs

View reference, projection reference, perspective reference, presentation context, uncertainty display reference, user-facing slice.

## Invariants

- Views are representations or projections, not the underlying asset or reality.
- Views must preserve uncertainty and provenance when material.
- A view may change without changing the asset it presents.
- Views do not own reasoning, navigation, or storage.

## Failure Modes

Missing source, stale projection, hidden uncertainty, policy constraint, incomplete context, or unsupported perspective remain explicit uncertainty or failure states.

## Promotion Rules

Views remain ephemeral by default. A view becomes durable only when promoted as a capsule artifact, specification artifact, evidence artifact, or other canonical owner output.

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
