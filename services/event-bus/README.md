# Event Bus Service

## Purpose

The Event Bus Service is the canonical owner of reusable platform infrastructure for event bus concerns across Wayfinder.

Wave 2 promoted the service boundary and evidence-backed public responsibilities. M-002 adds a minimal transport-neutral implementation proof while legacy engine code remains in place until a later consumer migration proves compatibility.

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

The minimal implementation exposes a bounded health signal covering event count, subscriber count, next sequence, payload bounds, replay bounds, and capacity limits.

## Verification Status

- Executable code added: yes, minimal implementation proof
- Engine behavior changed: no
- Engine files moved: no
- Concrete technology selected: no
- Governance updated: yes
