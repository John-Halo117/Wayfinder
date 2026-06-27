# Proof Contract

## Purpose

Defines validation artifacts that justify promotion from ephemeral state to durable knowledge.

## Producer

ARK

Exactly one engine produces this contract across engine boundaries.

## Consumers

Promotion, Build Bible, Foundry, Reasoning, MICE, Capsules, Domains

## Inputs

Evidence, Observation, Provenance, Context, Policy, contradiction, confidence, validation result.

## Outputs

Proof, confidence statement, validation result, contradiction finding, promotion readiness.

## Invariants

- Proof precedes promotion.
- Proof must reference evidence and criteria.
- Proof may fail without erasing evidence.
- Proof is scoped to a claim, context, and promotion target.

## Failure Modes

Insufficient evidence, contradiction, failed validation, low confidence, missing provenance, or ambiguous scope are represented as failed or incomplete proof.

## Promotion Rules

Proofs may become durable as promotion evidence. Failed proofs remain durable only when useful as audit or negative evidence.

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
