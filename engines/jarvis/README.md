# Jarvis

Jarvis is the Wayfinder navigation engine.

## Responsibility

Jarvis owns navigation: selecting bearings, coordinating capability routes, and
guiding work through observable, bounded execution paths.

Jarvis does not own shared infrastructure. Identity, storage, persistence,
eventing, telemetry, permissions, policy, and integration primitives belong in
services or external systems.

## Classification

- Architectural class: Engine
- Canonical home: `engines/jarvis/`
- Primary capability: Navigate
- Supporting capabilities: Observe, Reason, Plan, Execute, Verify, Recover,
  Communicate
- Source repository folded from:
  `/mnt/c/Users/trevl/OneDrive/Documents/GitHub/Jarvis`

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

Jarvis modules must expose bounded health checks for:

- Contract compatibility
- Required configuration presence
- External integration reachability
- Proof readiness
- Egress availability

## Runtime Contract

Expected runtime for health checks: less than 5 seconds per dependency.

Expected memory for health checks: less than 64 MiB above baseline process
memory.

All loops must have explicit iteration or timeout bounds.

## Folded Source

Original source artifacts are preserved under `docs/source/`.

The original `.env.example` is folded into `ingress/.env.example` because it
defines external inputs and required runtime credentials.

## Constitutional Boundary

### Purpose

Navigates capabilities and routes under uncertainty.

### Owns

Bearings, routes, recommendations, navigation posture, route tradeoffs, and capability navigation behavior.

### Does Not Own

Discovery registry ownership, reasoning, commitments, reality preservation, or task execution.

### Inputs

Objectives, capabilities, views, reasoning outputs, constraints, policies, and context.

### Outputs

Bearings, routes, recommendations, navigation decisions, and route proof requirements.

### Dependencies

Reasoning, Views, Capability Contracts, Bearing Contracts, Policy, Identity.

### Consumers

Internal applications, domains, MICE, Foundry, and operators.

