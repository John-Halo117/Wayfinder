# Capability Contracts

## Purpose

Capability Contracts define shared language for stable architectural verbs, capability invocation, capability routing, and capability requirements.

The contract defines vocabulary only. It contains no implementation, executable
logic, imports, runtime behavior, or engine ownership.

## Canonical Owner

Canonical owner: `contracts/capabilities/`

## Responsibilities

- Capability name
- Capability request
- Capability provider reference
- Capability requirement
- Capability result
- Capability route reference

## Scope

This contract names shared language that may be consumed by services, engines,
domains, internal applications, external integrations, operations, and tooling.

## Public Language

- `capability_id`
- `verb`
- `provider_ref`
- `input_contract_ref`
- `output_contract_ref`
- `constraints`
- `health_ref`
- `policy_ref`
- `metadata`

## Relationships

- References Events, Policies, Permissions, Health, Schemas, and Bearings.
- Supports ARK mesh routing and Jarvis navigation without owning either implementation.

## Consumers

- Jarvis
- ARK mesh/discovery
- Foundry tool selection
- Services
- Domains

## Non-Goals

- Service registry implementation
- Navigation planning
- Tool execution
- Domain orchestration

## Future Implementation Owners

Capabilities remain contracts/capability grammar; Discovery service may implement registry behavior.

## Failure Model

Contract validation failures use the standard Wayfinder failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_CAPABILITY_CONTRACT",
  "reason": "The capability contract input is invalid.",
  "context": {},
  "recoverable": true
}
```
