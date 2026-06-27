# Promotion Contracts

## Purpose

Promotion Contracts define shared language for moving information from ephemeral or legacy status into durable canonical state after proof.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/promotion/`

## Responsibilities

- Promotion candidate
- Promotion criteria
- Promotion proof reference
- Promotion decision
- Rollback reference
- Promotion status

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `promotion_id`
- `candidate_ref`
- `from_owner`
- `to_owner`
- `criteria_refs`
- `proof_refs`
- `decision`
- `decided_at`
- `rollback_ref`
- `confidence`
- `metadata`

## Relationships

- References Evidence, Provenance, Policy, Health, Storage, and Schema language.
- Consumed by ARK proof and governance flows.

## Consumers

- ARK proofs
- Promotion registry
- Governance docs
- Future services and engines

## Non-Goals

- Promotion engine implementation
- Test runner behavior
- Storage migration
- Runtime deployment

## Future Implementation Owners

ARK owns proof-gated reality promotion behavior; governance owns registry process.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_PROMOTION_CONTRACT",
  "reason": "The promotion contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
