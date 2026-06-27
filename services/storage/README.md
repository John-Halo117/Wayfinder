# Storage Service

## Purpose

The Storage Service is the canonical owner of reusable platform infrastructure for storage concerns across Wayfinder.

Wave 2 promotes the service boundary and evidence-backed public responsibilities only. Legacy engine code remains in place until a later implementation migration proves compatibility.

## Ownership

- Canonical owner: `services/storage/`
- Public language: `contracts/storage/`
- Promotion wave: Wave 2 Core Platform Service Promotion
- Promotion date: 2026-06-27
- Confidence: High

## Responsibilities

- abstract persistence interface
- object storage vocabulary
- metadata ownership
- versioning hooks
- transaction boundaries
- repository abstraction
- backend replaceability

## Public Contracts

This service consumes canonical contract language and must not define competing vocabulary.

- contracts/storage/
- contracts/schemas/
- contracts/identities/
- contracts/events/

## Consumers

- ARK reality append storage
- Event Bus replay persistence
- Identity metadata persistence
- Foundry artifact references
- Future domains requiring durable state

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

- choosing DuckDB, Redis, S3, or a database
- engine-specific state machines
- semantic search/indexing
- policy evaluation

## Health Signal

A future implementation must expose a bounded health signal covering contract availability, dependency readiness, and degraded-mode status. This scaffold introduces no runtime code.

## Verification Status

- Executable code added: no
- Engine behavior changed: no
- Engine files moved: no
- Concrete technology selected: no
- Governance updated: yes
