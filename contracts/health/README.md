# Health Contracts

## Purpose

Health Contracts define shared language for bounded status signals, readiness, dependency state, and architectural health findings.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/health/`

## Responsibilities

- Health signal
- Readiness status
- Dependency status
- Probe result
- Fitness result
- Failure finding

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `health_id`
- `subject_ref`
- `status`
- `checked_at`
- `runtime_ms`
- `dependencies`
- `findings`
- `recoverable`
- `metadata`

## Relationships

- References Events, Policies, Schemas, Capabilities, and Promotion language.
- Supports services, engines, operations, and governance.

## Consumers

- Telemetry service
- Operations
- Engines
- Services
- Constitutional linter

## Non-Goals

- Monitoring backend
- Probe implementation
- Alert routing
- Runtime remediation

## Future Implementation Owners

Telemetry service owns implementation.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_HEALTH_CONTRACT",
  "reason": "The health contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
