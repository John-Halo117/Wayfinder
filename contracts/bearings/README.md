# Bearing Contract

## Purpose

Defines navigational orientation under uncertainty.

## Producer

Jarvis

Exactly one engine produces this contract across engine boundaries.

## Consumers

MICE, Foundry, Domains, Internal applications, Capsules, VALOR

## Inputs

Objective, Asset in Context, Capability, Evidence, Reasoning output, Context, constraints, policy, value/risk assessment.

## Outputs

Bearing, route target, navigation constraint, route confidence, route reference.

## Invariants

- Bearings orient; they do not commit.
- Bearings do not rewrite reality.
- Bearings must expose uncertainty.
- Bearings depend on objectives and context.

## Failure Modes

Insufficient evidence, conflicting objectives, unavailable capability, ambiguous route, or low confidence remain explicit uncertainty.

## Promotion Rules

Bearings usually remain ephemeral navigation state. They become durable only when preserved as evidence, recommendation history, or commitment support.

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
