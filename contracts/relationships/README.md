# Relationship Contract

## Purpose

Defines constitutional relationships between assets without merging their identities.

## Producer

WEAVE

Exactly one engine produces this contract across engine boundaries.

## Consumers

Interpretation, Reasoning, Views, Jarvis, ZWLib, MICE, VALOR, Domains

## Inputs

Asset, RID, Context, Evidence, Provenance, relationship type, confidence, lifecycle.

Source Relationships may be consumed as evidence when they were explicitly
present in source data and preserved by ARK.

## Outputs

Relationship, relationship topology reference, relationship evidence reference.

## Invariants

- Relationships connect assets without replacing asset identity.
- Relationships require evidence when durable.
- Relationship vocabulary remains minimal.
- A relationship is not proof by itself.
- Source Relationships are evidence, not durable topology.

## Failure Modes

Unknown endpoint, ambiguous relation, conflicting evidence, missing context, or low confidence remain explicit uncertainty.

## Promotion Rules

Relationships remain ephemeral until WEAVE can reference sufficient evidence and provenance. Durable relationships remain traceable to ARK-preserved reality.

ARK may preserve explicit Source Relationships without producing WEAVE
topology. WEAVE owns durable relationship topology after proof and promotion.

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
