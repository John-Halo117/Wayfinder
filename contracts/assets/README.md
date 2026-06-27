# Asset Contracts

## Purpose

Asset Contracts define shared language for durable or referenced objects that Wayfinder observes, stores, relates, or acts upon.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/assets/`

## Responsibilities

- Asset reference
- Asset type
- Asset location
- Asset ownership
- Asset metadata
- Asset lifecycle

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `asset_id`
- `asset_type`
- `owner_ref`
- `location_ref`
- `storage_ref`
- `observed_ref`
- `lifecycle_state`
- `metadata`
- `tags`

## Relationships

- References Identity, Observation, Storage, Provenance, Schema, and Permission language.
- May describe files, media, devices, documents, datasets, or physical objects without owning domain behavior.

## Consumers

- ARK reality graph
- Storage
- Domains
- External integrations
- Internal apps

## Non-Goals

- Inventory domain logic
- Filesystem implementation
- Object storage implementation
- Device integration behavior

## Future Implementation Owners

Domains own asset-specific workflows; Storage owns persistence.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_ASSET_CONTRACT",
  "reason": "The asset contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
