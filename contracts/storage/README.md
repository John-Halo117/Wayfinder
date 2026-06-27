# Storage Contract

## Purpose

Defines shared language for persistence boundaries, object references, metadata, transactions, versioning hooks, and storage ownership.

## Producer

Storage Service

Exactly one service produces storage boundary language. Engines preserve or retrieve durable knowledge through this contract; they do not own generic storage vocabulary.

## Consumers

ARK, Capsules, Foundry, Jarvis, Event Bus, Identity Service, Policy Service, Domains, Internal applications, Operations

## Inputs

Object reference, asset reference, RID, metadata, durability intent, transaction boundary, version reference, policy reference, schema reference, provenance reference.

## Outputs

Persistence reference, object storage reference, metadata reference, transaction reference, version hook reference, storage capability reference.

## Invariants

- Storage is infrastructure, not engine knowledge.
- Storage references do not replace asset identity or evidence.
- Backends remain replaceable under the Law of Theseus.
- Transaction and version boundaries must remain explicit when relevant.

## Failure Modes

Unknown object, unavailable backend, transaction conflict, version conflict, policy constraint, metadata ambiguity, or durability failure remain explicit failure states.

## Promotion Rules

Storage state becomes durable only when the owning concept authorizes persistence. Temporary caches, projections, indexes, and derived views remain ephemeral unless intentionally promoted.

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
