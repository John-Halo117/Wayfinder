# Permission Contracts

## Purpose

Permission Contracts define shared language for allowed, denied, delegated, or scoped actions without implementing authorization.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/permissions/`

## Responsibilities

- Permission grant
- Permission scope
- Principal reference
- Resource reference
- Action reference
- Decision reference

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `permission_id`
- `principal_ref`
- `resource_ref`
- `action`
- `scope`
- `effect`
- `expires_at`
- `policy_ref`
- `reason`
- `metadata`

## Relationships

- Depends on Identity, Policy, Asset, Capability, and Schema language.
- Feeds future permissions/policy services.

## Consumers

- Policy service
- Internal applications
- Engines invoking actions
- External integration boundaries

## Non-Goals

- Authentication
- Authorization runtime
- User interface roles
- Provider-specific ACLs

## Future Implementation Owners

Permissions service or Policy service owns implementation after boundary proof.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_PERMISSION_CONTRACT",
  "reason": "The permission contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
