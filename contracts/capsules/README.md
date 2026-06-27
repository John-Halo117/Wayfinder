# Capsule Contracts

## Purpose

Capsule Contracts define shared language for continuity packages that preserve context, state references, evidence, and handoff boundaries.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/capsules/`

## Responsibilities

- Capsule
- Continuity boundary
- Context reference
- State reference
- Evidence bundle reference
- Handoff metadata

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `capsule_id`
- `purpose`
- `context_refs`
- `state_refs`
- `evidence_refs`
- `owner_ref`
- `created_at`
- `expires_at`
- `promotion_ref`
- `metadata`

## Relationships

- References Identity, Evidence, Provenance, Storage, Events, Schemas, and Promotion language.
- Supports the future Capsules engine.

## Consumers

- Capsules engine
- Foundry sessions
- Jarvis navigation continuity
- ARK preservation workflows

## Non-Goals

- Capsule runtime
- Compression implementation
- Storage implementation
- Session UI

## Future Implementation Owners

Capsules engine owns continuity behavior; Storage owns persistence.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_CAPSULE_CONTRACT",
  "reason": "The capsule contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
