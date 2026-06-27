# Commitment Contract

## Purpose

Defines accountable promises, agreements, delegation, and consensus outcomes.

## Producer

MICE

Exactly one engine produces this contract across engine boundaries.

## Consumers

Jarvis, Foundry, Domains, Operations, Internal applications, Capsules

## Inputs

Recommendation, Identity, Objective, Policy, Context, parties, evidence, authority, acceptance.

## Outputs

Commitment, agreement, delegation record, accountability record, consensus outcome.

## Invariants

- A commitment requires accountable parties.
- A commitment is not merely a task or recommendation.
- Commitments must preserve authority and acceptance context.
- Commitments do not own execution.

## Failure Modes

Missing party, unclear authority, failed consensus, conflicting commitment, or ambiguous acceptance remain explicit uncertainty.

## Promotion Rules

Commitments become durable when MICE records accountable parties, acceptance, scope, and supporting evidence. Draft negotiations remain ephemeral.

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
