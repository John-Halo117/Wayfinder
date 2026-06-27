# Configuration Service

## Purpose

The Configuration Service is the canonical owner of reusable platform infrastructure for configuration concerns across Wayfinder.

Wave 2 promotes the service boundary and evidence-backed public responsibilities only. Legacy engine code remains in place until a later implementation migration proves compatibility.

## Ownership

- Canonical owner: `services/configuration/`
- Public language: `contracts/schemas/`
- Promotion wave: Wave 2 Core Platform Service Promotion
- Promotion date: 2026-06-27
- Confidence: Medium-High

## Responsibilities

- configuration loading language
- layered configuration order
- environment abstraction
- defaults and override vocabulary
- configuration validation boundary
- runtime configuration access
- configuration redaction expectations

## Public Contracts

This service consumes canonical contract language and must not define competing vocabulary.

- contracts/schemas/
- contracts/policies/
- contracts/health/

## Consumers

- ARK runtime and ingress configuration
- Jarvis ingress configuration
- Foundry runtime and MCP configuration
- Services requiring explicit dependencies
- Operations deployment validation

## Dependencies

Allowed dependencies:

- `constitution/`
- `contracts/`

Forbidden dependencies:

- `engines/`
- `domains/`
- `internal/`
- `external/`
- concrete runtime infrastructure selected by an engine or deployment

## What Does Not Belong Here

- secret storage implementation
- business logic flags owned by engines
- provider-specific deployment templates
- policy evaluation

## Health Signal

A future implementation must expose a bounded health signal covering contract availability, dependency readiness, and degraded-mode status. This scaffold introduces no runtime code.

## Verification Status

- Executable code added: no
- Engine behavior changed: no
- Engine files moved: no
- Concrete technology selected: no
- Governance updated: yes
