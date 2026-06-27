# Observation Contract

## Purpose

Defines what crosses the boundary when reality is observed before interpretation.

## Producer

ARK

Exactly one engine produces this contract across engine boundaries.

## Consumers

Evidence, Interpretation, Reasoning, Views, Jarvis, Capsules, MIDAS, Domains, Internal applications

## Inputs

Reality, Observation Source, Asset or RID, Context, time, location, actor, capability, constraints.

## Outputs

Observation, source reference, subject reference, payload reference, integrity reference, observation metadata.

## Invariants

- Observation precedes interpretation.
- Observation does not decide meaning.
- Observation is append-only once promoted.
- Observation references representations without becoming a representation.

## Failure Modes

Missing source, uncertain subject, incomplete context, conflicting observation, untrusted source, or insufficient provenance are represented as uncertainty and evidence gaps.

## Promotion Rules

Observation remains ephemeral until ARK preserves it with sufficient source, integrity, and provenance. Promoted observations become durable reality references.

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
