# Event Contracts

## Purpose

Event Contracts define shared language for event envelopes, metadata, routing, correlation, causation, subscriptions, and replay cursors.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/events/`

## Responsibilities

- Event envelope
- Event metadata
- Route
- Publish request
- Subscribe request
- Correlation ID
- Causation ID
- Replay cursor

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `event_id`
- `event_type`
- `schema_version`
- `source`
- `subject_ref`
- `correlation_id`
- `causation_id`
- `occurred_at`
- `observed_at`
- `payload_ref`
- `metadata`

## Relationships

- Uses Identity, Observation, Schema, Policy, and Storage references.
- Implemented later by Event Bus service.

## Consumers

- Event Bus
- ARK ingress
- Foundry audit events
- Jarvis route events
- External adapters

## Non-Goals

- Broker implementation
- NATS-specific APIs
- Engine-specific interpretation
- Storage implementation

## Future Implementation Owners

Event Bus owns implementation.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_EVENT_CONTRACT",
  "reason": "The event contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
