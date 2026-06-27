# Health Contract

## Purpose

Defines the shared language for readiness, liveness, dependency status, degradation, and operational confidence across Wayfinder boundaries.

## Producer

VALOR

Exactly one engine produces health assessment language. Services and engines may report status, but VALOR owns cross-boundary health assessment vocabulary.

## Consumers

Jarvis, Foundry, Blackwall, NetWatch, Operations, Domains, Internal applications, MICE

## Inputs

Asset reference, capability reference, service reference, engine reference, dependency reference, event metadata, evidence, policy reference, time frame, context.

## Outputs

Health state, readiness status, dependency status, degradation signal, confidence reference, recovery recommendation reference.

## Invariants

- Health is contextual and time-bound.
- Health reports do not replace evidence or proof.
- Readiness and liveness are distinct.
- Degradation must remain visible rather than silently normalized.

## Failure Modes

Unknown dependency, stale status, missing evidence, partial outage, conflicting health reports, or untrusted reporter remain explicit uncertainty.

## Promotion Rules

Health observations remain ephemeral for routing unless evidence-backed operational status is promoted by the relevant owner. Durable incidents, risks, or recovery records require proof.

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
