# View Contracts

## Purpose

View Contracts define shared language for projections, read models, displays, and derived presentations without owning UI or storage behavior.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/views/`

## Responsibilities

- View definition
- Projection reference
- Query reference
- View state
- Refresh policy
- View provenance

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `view_id`
- `source_refs`
- `projection_type`
- `query_ref`
- `schema_ref`
- `refresh_policy`
- `generated_at`
- `provenance_ref`
- `metadata`

## Relationships

- References Observations, Events, Storage, Provenance, Schemas, and Permissions.
- Supports ARK projections and future Views engine without implementing them.

## Consumers

- ARK ephemeral projections
- Views engine
- Internal apps
- Domains

## Non-Goals

- UI implementation
- Projection algorithms
- Cache implementation
- Search implementation

## Future Implementation Owners

Views engine or internal apps own presentation behavior; services may own reusable query/search.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_VIEW_CONTRACT",
  "reason": "The view contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
