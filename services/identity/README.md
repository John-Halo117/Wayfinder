# Identity Service

## Purpose

The Identity Service is the canonical owner of reusable platform infrastructure for identity concerns across Wayfinder.

Wave 2 promoted the service boundary and evidence-backed public responsibilities.

Phase 4 promotes the first reusable Identity implementation proof while leaving legacy engine code and public behavior unchanged.

## Ownership

- Canonical owner: `services/identity/`
- Public language: `contracts/identities/`
- Promotion wave: Wave 2 Core Platform Service Promotion
- Promotion date: 2026-06-27
- Confidence: High

## Responsibilities

- RID generation and validation vocabulary
- canonical identity records
- alias resolution
- namespace handling
- identity lifecycle state language
- identity lookup boundaries
- merge semantics and conflict vocabulary
- legacy-compatible request ID generation

## Public Contracts

This service consumes canonical contract language and must not define competing vocabulary.

- contracts/identities/
- contracts/schemas/
- contracts/events/
- contracts/policies/

## Consumers

- ARK reality and evidence records
- Jarvis navigation subjects
- Foundry execution/session attribution
- Event Bus event actor/source metadata
- Storage object ownership metadata

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

- authentication provider integration
- authorization decisions
- domain profile data
- storage backend selection
- engine-specific subject interpretation

## Health Signal

The implementation exposes `IdentityService.health()`, a bounded health signal reporting record count, alias count, and configured resource caps.

## Verification Status

- Executable code added: yes, limited to reusable Identity infrastructure
- Engine behavior changed: no
- Engine files moved: no
- Concrete technology selected: no
- Governance updated: yes


## Implementation Proof

See `docs/implementation-proof.md` for inventory, dependency graph, consumer graph, duplicate analysis, verification, and rollback details.
