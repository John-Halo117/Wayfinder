# Capsule Contract

## Purpose

Defines continuity packages that preserve context for future re-entry.

## Producer

Capsules

Exactly one engine produces this contract across engine boundaries.

## Consumers

Jarvis, Foundry, MICE, Domains, Internal applications, Operators

## Inputs

Asset, Context, Evidence, Provenance, State reference, Objective, owner reference, promotion reference.

## Outputs

Capsule, continuity boundary, handoff metadata, re-entry context, maturity signal.

## Invariants

- A capsule preserves continuity; it does not own generic storage.
- A capsule must reference its context and evidence.
- A capsule may contain representations without becoming the asset.
- Re-entry requires enough context to resume meaningfully.

## Failure Modes

Insufficient context, stale capsule, missing owner, weak evidence, expired relevance, or low maturity remain explicit uncertainty.

## Promotion Rules

Capsules are durable only when continuity purpose, owner, evidence, and re-entry criteria are explicit. Draft capsules remain ephemeral.

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
