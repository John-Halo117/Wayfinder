# Promotion Contract

## Purpose

Defines how proven outputs become durable in their canonical owner.

## Producer

ARK

Exactly one engine produces this contract across engine boundaries.

## Consumers

All engines, Services, Domains, Internal applications, Operations

## Inputs

Proof, Evidence, Provenance, Asset, Context, canonical owner, rollback context, confidence.

## Outputs

Promotion record, durable knowledge reference, canonical owner reference, rollback reference.

## Invariants

- Nothing becomes durable without proof.
- Promotion must target exactly one canonical owner.
- Promotion must reduce or preserve ownership clarity.
- Promotion must preserve rollback and provenance.

## Failure Modes

Missing proof, ambiguous owner, failed validation, duplicate ownership, unresolved contradiction, or missing rollback context block promotion.

## Promotion Rules

Promotion records are durable governance artifacts once accepted. Candidate promotions remain ephemeral until proof passes.

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
