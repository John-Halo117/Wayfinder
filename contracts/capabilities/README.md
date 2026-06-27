# Capability Contract

## Purpose

Defines stable outcome verbs and capability availability across engine boundaries.

## Producer

NOMAD

Exactly one engine produces this contract across engine boundaries.

## Consumers

Jarvis, ZWLib, Foundry, MICE, Domains, Services, Internal applications

## Inputs

Asset, Context, Objective, constraints, provider reference, health reference, policy reference, evidence.

## Outputs

Capability, capability profile, provider option, requirement, capability result reference.

## Invariants

- Capability names describe outcomes rather than implementations.
- Capabilities remain stable under changing providers.
- Capability availability is context-sensitive.
- Capability contracts do not own navigation decisions.

## Failure Modes

Unavailable provider, uncertain readiness, missing requirement, policy constraint, or insufficient evidence remain explicit uncertainty.

## Promotion Rules

Capability language is durable as contract vocabulary. Specific provider availability remains ephemeral until discovered and proven in context.

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
