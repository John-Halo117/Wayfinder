# Evidence Contract

## Purpose

Defines support used to justify claims, proofs, recommendations, commitments, and promotions.

## Producer

ARK

Exactly one engine produces this contract across engine boundaries.

## Consumers

Proof, Promotion, Interpretation, Reasoning, VALOR, MIDAS, Jarvis, MICE, Blackwall

## Inputs

Observation, Provenance, Asset, RID, Context, Representation, uncertainty, source references.

## Outputs

Evidence item, evidence bundle, support weight, contradiction reference, confidence posture.

## Invariants

- Evidence supports claims but is not the claim.
- Evidence remains traceable to observation and provenance.
- Evidence may increase or decrease confidence.
- Evidence never overwrites reality.

## Failure Modes

Insufficient evidence, contradictory evidence, missing provenance, stale context, and unknown confidence remain explicit uncertainty.

## Promotion Rules

Evidence becomes durable when ARK preserves its observation/provenance links. Derived confidence remains ephemeral until proof promotes it.

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
