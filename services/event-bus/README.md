# Event Bus Service

## Purpose

The Event Bus Service is the canonical owner of reusable platform infrastructure for event bus concerns across Wayfinder.

Wave 2 promotes the service boundary and evidence-backed public responsibilities only. Legacy engine code remains in place until a later implementation migration proves compatibility.

## Ownership

- Canonical owner: `services/event-bus/`
- Public language: `contracts/events/`
- Promotion wave: Wave 2 Core Platform Service Promotion
- Promotion date: 2026-06-27
- Confidence: High

## Responsibilities

- publish language and boundary
- subscribe language and boundary
- routing metadata
- event metadata
- correlation identifiers
- replay support boundaries
- transport-agnostic event flow

## Public Contracts

This service consumes canonical contract language and must not define competing vocabulary.

- contracts/events/
- contracts/identities/
- contracts/schemas/
- contracts/health/

## Consumers

- ARK ingestion, replay, and promotion records
- Jarvis navigation events
- Foundry task and verification events
- Operations monitoring and audit streams
- Future engines communicating through events

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

- selecting NATS, Redis, Kafka, or any broker
- domain event interpretation
- storage backend implementation
- engine workflow ownership

## Health Signal

A future implementation must expose a bounded health signal covering contract availability, dependency readiness, and degraded-mode status. This scaffold introduces no runtime code.

## Verification Status

- Executable code added: no
- Engine behavior changed: no
- Engine files moved: no
- Concrete technology selected: no
- Governance updated: yes
