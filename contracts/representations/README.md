# Representation Contract

## Purpose

Defines derived descriptions of assets without confusing them with the assets themselves.

## Producer

Views

Exactly one engine produces this contract across engine boundaries.

## Consumers

Interpretation, Reasoning, Jarvis, Foundry, Capsules, Domains, Internal applications

## Inputs

Asset, RID, Observation, Evidence, Context, Provenance, View request.

## Outputs

Representation, projection, view, summary, metadata, read model reference.

## Invariants

- A representation is not the asset.
- A representation may be replaced without changing asset identity.
- Representations must reference the source asset or observation when known.
- Representations do not own truth.

## Failure Modes

Missing source, stale representation, incomplete context, lossy transform, or uncertain linkage remain explicit in representation metadata.

## Promotion Rules

Representations remain ephemeral unless promoted as durable knowledge about a representation. The represented asset remains distinct.

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
