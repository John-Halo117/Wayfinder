# Capability Contract

## Purpose

Defines capability availability across engine boundaries while referencing the canonical capability verb language owned by `capabilities/`.

## Producer

NOMAD

Exactly one engine produces discovered capability availability. NOMAD discovers available providers, resources, and opportunities; it does not own or redefine the universal capability grammar.

## Consumers

Jarvis, ZWLib, Foundry, MICE, Domains, Services, Internal applications

## Inputs

Canonical capability verb, Asset, Context, Objective, constraints, provider reference, resource reference, health reference, policy reference, evidence.

## Outputs

Capability availability reference, capability profile, provider option, resource option, requirement, opportunity reference, capability result reference.

## Invariants

- Capability verbs are canonical language owned by `capabilities/`.
- NOMAD owns discovery of availability, providers, resources, and opportunities.
- Capability names describe outcomes rather than implementations.
- Capabilities remain stable under changing providers.
- Capability availability is context-sensitive.
- Capability contracts do not own navigation decisions.

## Failure Modes

Unavailable provider, uncertain readiness, missing requirement, policy constraint, unavailable resource, or insufficient evidence remain explicit uncertainty.

## Promotion Rules

Capability language is durable as capability grammar. Specific provider, resource, or opportunity availability remains ephemeral until discovered and proven in context.

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
