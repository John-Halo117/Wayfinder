# Policy Service

## Purpose

The Policy Service is the canonical owner of reusable platform infrastructure for policy concerns across Wayfinder.

Wave 2 promotes the service boundary and evidence-backed public responsibilities only. Legacy engine code remains in place until a later implementation migration proves compatibility.

## Ownership

- Canonical owner: `services/policy/`
- Public language: `contracts/policies/`
- Promotion wave: Wave 2 Core Platform Service Promotion
- Promotion date: 2026-06-27
- Confidence: High

## Responsibilities

- policy evaluation boundary
- rule execution language
- authorization policy references
- promotion policy references
- architectural policy references
- decision/result vocabulary
- policy proof hooks

## Public Contracts

This service consumes canonical contract language and must not define competing vocabulary.

- contracts/policies/
- contracts/permissions/
- contracts/promotion/
- contracts/evidence/
- contracts/schemas/

## Consumers

- ARK promotion and resolver decisions
- Foundry MCP/tool gates
- Jarvis route permission checks
- Operations governance checks
- Future services that need reusable rule evaluation

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

- permission vocabulary ownership
- identity lifecycle ownership
- engine-specific business decisions
- secret management
- configuration loading

## Health Signal

A future implementation must expose a bounded health signal covering contract availability, dependency readiness, and degraded-mode status. This scaffold introduces no runtime code.

## Verification Status

- Executable code added: no
- Engine behavior changed: no
- Engine files moved: no
- Concrete technology selected: no
- Governance updated: yes
