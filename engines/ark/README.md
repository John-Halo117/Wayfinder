# ARK

ARK is the Wayfinder engine for reality preservation.

## Responsibility

ARK owns observation, evidence, provenance, reality graph behavior, and proof-gated promotion into durable reality.

ARK does not own reusable infrastructure such as storage, logging, identity, scheduling, cryptography, permissions, policy, or generic search. Those concepts are extracted to services and contracts after behavior is proven equivalent.

## Current Fold State

Phase 1 is complete: the historical ARK source has been preserved under `legacy/`, and the classification evidence is in `docs/`.

## Canonical Lifecycle

```text
Ingress
  |
Reality
  |
Ephemeral
  |
Proof
  |
Promotion
  |
Core
  |
Egress
```

## Health Signal

ARK modules must expose bounded health checks for ingress validity, append-only reality writes, ephemeral proof readiness, promotion criteria, service dependency status, and egress traceability.

Expected health-check runtime: less than 5 seconds per dependency.

Expected health-check memory: less than 64 MiB above baseline process memory.

## Phase 1 Reports

- `docs/inventory.md`
- `docs/dependency-graph.md`
- `docs/duplicate-concepts.md`
- `docs/extraction-opportunities.md`
- `docs/migration-plan.md`

## Constitutional Boundary

### Purpose

Preserves reality by maintaining append-only observations, evidence, provenance, and reality graph continuity.

### Owns

Observation behavior; evidence preservation; provenance; reality graph; proof-gated promotion into durable reality.

### Does Not Own

Storage, identity, event bus, policy, telemetry, navigation, reasoning, views, domain orchestration.

### Inputs

Observations, evidence, source references, proof criteria, contract language, and supporting services.

### Outputs

Durable reality records, provenance references, evidence records, reality graph outputs, and promoted reality knowledge.

### Dependencies

Reality, Observation Contracts, Evidence Contracts, Provenance Contracts, Identity Service, Event Bus, Storage, Policy.

### Consumers

WEAVE, Interpretation, Reasoning, Views, Jarvis, Capsules, domains, and internal applications.

