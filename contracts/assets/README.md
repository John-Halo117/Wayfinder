# Asset Contract

## Purpose

Defines the universal object crossing engine boundaries as an Asset in Context. The constitutional Asset model is owned by `constitution/assets.md` and this contract; ARK produces durable asset knowledge without owning the universal Asset abstraction.

## Producer

ARK

Exactly one engine produces durable Asset knowledge across engine boundaries. Producer here means producer of promoted asset knowledge, not owner of the universal Asset model.

## Consumers

WEAVE, Interpretation, Reasoning, Views, Jarvis, ZWLib, Capsules, MIDAS, VALOR, MICE, Domains

## Inputs

RID, Observation, Evidence, Context, Provenance, Capability profile, CivPhys profile, lifecycle state.

## Outputs

Asset reference, Asset in Context reference, lifecycle reference, ownership reference, relationship-ready asset identity.

## Invariants

- The Asset model is constitutionally owned by `constitution/assets.md` and `contracts/assets/`.
- ARK produces durable asset knowledge; it does not own the universal Asset abstraction.
- An asset is not merely a representation.
- Context changes interpretation without changing identity.
- Asset identity is stable under the Law of Theseus when invariants remain continuous.
- Asset claims require evidence.

## Failure Modes

Unknown identity, ambiguous identity, merge/split uncertainty, missing context, and unproven ownership remain explicit uncertainty.

## Promotion Rules

Asset knowledge becomes durable when identity, evidence, and provenance are sufficient for ARK promotion. Representations may be deleted without deleting the asset.

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
