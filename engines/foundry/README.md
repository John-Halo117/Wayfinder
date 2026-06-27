# Foundry

Foundry is the Wayfinder engineering engine.

## Responsibility

Foundry owns engineering workflows: code-change proposal, bounded execution,
verification, red-team checks, patch application, developer UI surfaces, and
engineering artifacts.

Forge is historical ARK terminology for this responsibility. In Wayfinder, the
canonical owner is Foundry.

## Classification

- Architectural class: Engine
- Canonical home: `engines/foundry/`
- Historical source names: Forge, forge, forge-app
- Primary capability: Execute engineering change with proof
- Supporting capabilities: Plan, Transform, Verify, Recover, Reflect,
  Communicate

## Current Fold State

Forge-labeled ARK source has been preserved under `legacy/`.

The legacy executable and module names are intentionally preserved for
compatibility. Renaming runtime entrypoints requires a separate proof-backed
compatibility phase.

## Lifecycle

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

Foundry modules must expose bounded health/status signals for input validity,
workspace readiness, model/tool availability, sandbox readiness, verification
readiness, artifact write readiness, and rollback readiness.

Expected health-check runtime: less than 5 seconds per dependency.

Expected health-check memory: less than 64 MiB above baseline process memory.

## Does Not Belong Here

- Reality preservation owned by ARK
- Navigation owned by Jarvis
- Shared identity owned by Identity Service
- Shared event routing owned by Event Bus
- Shared persistence owned by Storage
- Third-party provider adapters as canonical architecture

## Constitutional Boundary

### Purpose

Owns engineering workflows with proof.

### Owns

Engineering change proposals, verification gates, patch/workflow artifacts, rollback evidence, and proof-backed engineering change.

### Does Not Own

Canonical specifications, reality preservation, navigation, reusable services, or external provider ownership.

### Inputs

Objectives, specifications, repository context, policies, route recommendations, and capsules.

### Outputs

Proven engineering changes, verification artifacts, rollback evidence, and engineering outputs.

### Dependencies

Build Bible, Policy, Capsules, Jarvis, Storage, Identity.

### Consumers

Internal applications, operators, Build Bible, operations, and domains.

