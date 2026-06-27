# Recommendation Contract

## Purpose

Defines proposed routes or actions without making commitments.

## Producer

Jarvis

Exactly one engine produces this contract across engine boundaries.

## Consumers

MICE, Foundry, Domains, Internal applications, Operators

## Inputs

Bearing, Route, Objective, Capability, Evidence, Reasoning output, Context, Tradeoff Surface, Value Assessment.

## Outputs

Recommendation, rationale, route reference, confidence, uncertainty, expected consequence.

## Invariants

- A recommendation is not a commitment.
- A recommendation must cite bearing and rationale.
- A recommendation must preserve uncertainty.
- A recommendation may be rejected without changing durable knowledge.

## Failure Modes

Conflicting objectives, insufficient evidence, unavailable route, low confidence, or unmodeled tradeoff remain explicit uncertainty.

## Promotion Rules

Recommendations are ephemeral unless accepted, recorded as decision evidence, or used to support a MICE commitment.

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
