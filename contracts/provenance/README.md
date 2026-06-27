# Provenance Contracts

## Purpose

Provenance Contracts define shared language for tracing observations, evidence, claims, assets, and promoted records back to their sources.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/provenance/`

## Responsibilities

- Provenance edge
- Source lineage
- Derivation reference
- Method reference
- Actor reference
- Time reference

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `provenance_id`
- `source_ref`
- `target_ref`
- `relationship_type`
- `method_ref`
- `actor_ref`
- `observed_at`
- `derived_at`
- `confidence`
- `metadata`

## Relationships

- References Observations, Evidence, Assets, Identities, Events, and Schemas.
- Supports ARK reality preservation and promotion auditability.

## Consumers

- ARK reality graph
- ARK proofs
- Event Bus metadata
- Storage metadata
- Foundry artifact lineage

## Non-Goals

- Graph algorithms
- Storage layout
- Trust scoring
- Evidence weighting
- Promotion execution

## Future Implementation Owners

ARK owns provenance behavior in reality graph; Storage may persist provenance records.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_PROVENANCE_CONTRACT",
  "reason": "The provenance contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
