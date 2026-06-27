# Evidence Contracts

## Purpose

Evidence Contracts define shared language for support, validation, confidence, and proof inputs before promotion decisions.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/evidence/`

## Responsibilities

- Evidence item
- Evidence source reference
- Support weight
- Confidence language
- Validation reference
- Contradiction reference
- Evidence bundle

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `evidence_id`
- `observation_ref`
- `claim_ref`
- `source_ref`
- `support_weight`
- `confidence`
- `validation_ref`
- `contradicts`
- `metadata`

## Relationships

- Consumes Observation language.
- Supports Provenance, Promotion, Health, Policy, and ARK proof behavior.
- May reference Identity, Event, Asset, Schema, and Storage language.

## Consumers

- ARK proofs
- ARK reality graph
- Foundry verification gates
- Jarvis route proofs
- Policy evaluation

## Non-Goals

- Bayesian algorithms
- TRISCA scoring implementation
- Promotion execution
- Reality graph storage
- Policy enforcement

## Future Implementation Owners

ARK owns proof behavior; services may later own reusable validation primitives.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_EVIDENCE_CONTRACT",
  "reason": "The evidence contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
