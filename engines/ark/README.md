# ARK

ARK is the Wayfinder engine for reality preservation.

## Responsibility

ARK owns preservation, provenance, append-only reality, replay, Last Verified
Reality (LVR), and preservation of explicit Source Relationships.

ARK does not own observation discovery, source parsing, reusable
infrastructure such as storage, logging, identity, scheduling, cryptography,
permissions, policy, generic search, durable relationship topology, reasoning,
or navigation. Those concepts are extracted to Observation Sources, services,
contracts, or downstream engines after behavior is proven equivalent.

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

Preserves reality by maintaining append-only observations, evidence,
provenance, explicit Source Relationships, replay, and LVR.

### Owns

Observation preservation; evidence preservation; provenance; Source
Relationship preservation; replay; LVR; proof-gated promotion into durable
reality.

### Does Not Own

Observation discovery, source parsing, storage, identity, event bus, policy,
telemetry, relationship topology, navigation, reasoning, views, domain
orchestration.

### Inputs

Observation-shaped records from Observation Sources, explicit Source
Relationships, evidence, source references, proof criteria, contract language,
Import Profiles, and supporting services.

### Outputs

Durable reality records, provenance references, evidence records, preserved
Source Relationships, replay outputs, LVR, and promoted reality knowledge.

### Dependencies

Reality, Observation Contracts, Evidence Contracts, Provenance Contracts, Identity Service, Event Bus, Storage, Policy.

### Consumers

WEAVE, Interpretation, Reasoning, Views, Jarvis, Capsules, domains, and internal applications.
