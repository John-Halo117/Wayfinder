# Event Contract

## Purpose

Defines the event language crossing Wayfinder boundaries: event identity, envelope, metadata, routing reference, correlation, causation, and replay position.

## Producer

Event Bus

Exactly one service produces event boundary language. Engines emit and consume events through this contract; they do not own event vocabulary.

## Consumers

ARK, Jarvis, Foundry, Capsules, MICE, Domains, Internal applications, Operations, External integrations

## Inputs

Event source, event type, payload reference, RID reference, actor reference, context reference, schema reference, policy reference, correlation reference, causation reference.

## Outputs

Event, event envelope, event metadata, event route reference, correlation ID, causation ID, replay cursor.

## Invariants

- Events describe boundary facts or requests; they do not own the durable truth they reference.
- Correlation and causation remain explicit when known.
- Event routes are transport-neutral constitutional language.
- Replay position is a reference to ordered event history, not a storage implementation.

## Failure Modes

Unknown source, invalid schema reference, missing correlation, ambiguous route, policy constraint, replay gap, or duplicate event identity remain explicit uncertainty.

## Promotion Rules

Events become durable only when the canonical owner of the referenced concept promotes the event record or evidence derived from it. Routing and delivery state remain ephemeral unless explicitly promoted as operational evidence.

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
