# Provenance Contract

## Purpose

Defines shared language for tracing knowledge, claims, observations, representations, and promoted records back to their sources and transformations.

## Producer

ARK

Exactly one engine produces provenance boundary language for reality-preservation outputs.

## Consumers

Evidence, Proof, Promotion, Capsules, Views, Reasoning, VALOR, MICE, Domains, Operations

## Inputs

Observation reference, evidence reference, source reference, representation reference, actor reference, event metadata, time frame, transformation reference, context.

## Outputs

Provenance record, source chain, derivation reference, custody reference, trust boundary reference, uncertainty reference.

## Invariants

- Provenance supports knowledge about an asset; it does not define asset identity.
- Provenance is append-only once promoted.
- Transformations and custody boundaries must remain traceable.
- Missing provenance is an explicit evidence gap.

## Failure Modes

Unknown source, broken chain, conflicting custody, untrusted source, missing transformation reference, or ambiguous derivation remain explicit uncertainty.

## Promotion Rules

Provenance becomes durable when ARK promotes source and derivation evidence. Ephemeral derivation traces may guide proof but do not become durable without promotion.

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
