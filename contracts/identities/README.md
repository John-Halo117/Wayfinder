# Identity Contracts

## Purpose

RID is constitutionally defined in [constitution/assets.md](../../constitution/assets.md).

Identity Contracts define shared language for canonical identity, RIDs, aliases, namespaces, lookup, lifecycle, and merge semantics.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/identities/`

## Responsibilities

- RID
- Canonical identity
- Alias
- Namespace
- Identity lifecycle
- Lookup result
- Merge result

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `rid`
- `namespace`
- `local_id`
- `canonical_rid`
- `alias`
- `lifecycle_state`
- `merge_status`
- `confidence`
- `metadata_ref`

## Relationships

- Used by Observations, Events, Storage, Provenance, Assets, Permissions, Policies, and engines.
- Implemented later by the Identity Service.

## Consumers

- Identity Service
- ARK observations
- Event Bus subjects
- Storage ownership metadata
- Jarvis navigation
- Foundry operator/session references

## Non-Goals

- Authentication implementation
- Authorization policy
- Domain profiles
- Provider-specific identity adapters

## Future Implementation Owners

Identity Service owns implementation.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_IDENTITY_CONTRACT",
  "reason": "The identity contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
