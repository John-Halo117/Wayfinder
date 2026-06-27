# Schema Contracts

## Purpose

Schema Contracts define shared language for schema identity, versions, validation results, compatibility, and structured failures.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/schemas/`

## Responsibilities

- Schema reference
- Schema version
- Validation result
- Compatibility result
- Structured failure
- Schema owner

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `schema_id`
- `schema_version`
- `owner`
- `compatibility`
- `validation_status`
- `errors`
- `warnings`
- `validated_at`
- `metadata`

## Relationships

- Used by every contract family.
- Supports linter, promotion, health, and runtime validation language without implementing validators.

## Consumers

- All contracts
- Services
- Engines
- Constitutional linter
- Promotion reports

## Non-Goals

- Validator implementation
- Runtime schema registry
- Code generation
- Database migrations

## Future Implementation Owners

Schema validation implementation may become tooling or a service after proof.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_SCHEMA_CONTRACT",
  "reason": "The schema contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
