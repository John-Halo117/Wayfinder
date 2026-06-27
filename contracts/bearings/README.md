# Bearing Contracts

## Purpose

Bearing Contracts define shared navigation language for direction, intent, route targets, and orientation under uncertainty.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/bearings/`

## Responsibilities

- Bearing
- Route target
- Navigation constraint
- Position reference
- Objective reference
- Route confidence

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `bearing_id`
- `objective_ref`
- `current_ref`
- `target_ref`
- `constraints`
- `confidence`
- `route_ref`
- `policy_ref`
- `metadata`

## Relationships

- References Capabilities, Objectives, Events, Evidence, Policy, and Identity language.
- Consumed by Jarvis as the navigation engine.

## Consumers

- Jarvis
- Domains
- Internal apps
- Foundry planning surfaces

## Non-Goals

- Navigation algorithms
- Route execution
- Discovery registry
- Domain workflow

## Future Implementation Owners

Jarvis owns navigation behavior.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_BEARING_CONTRACT",
  "reason": "The bearing contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
