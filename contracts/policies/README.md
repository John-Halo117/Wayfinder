# Policy Contracts

## Purpose

Policy Contracts define shared language for rules, constraints, evaluation requests, decisions, and policy provenance.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/policies/`

## Responsibilities

- Policy document
- Policy rule
- Evaluation request
- Policy decision
- Constraint
- Exception
- Policy version

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `policy_id`
- `policy_version`
- `scope`
- `rule_id`
- `condition`
- `effect`
- `decision`
- `reason`
- `evidence_ref`
- `metadata`

## Relationships

- References Evidence, Identity, Permission, Capability, Event, Health, and Schema language.
- Implemented later by Policy service.

## Consumers

- ARK policy paths
- Foundry guards
- Jarvis route checks
- Services
- Operations

## Non-Goals

- Policy engine implementation
- Authorization runtime
- Domain-specific rule ownership
- Secret management

## Future Implementation Owners

Policy Service owns implementation.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_POLICY_CONTRACT",
  "reason": "The policy contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
