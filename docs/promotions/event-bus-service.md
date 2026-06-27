# Event Bus Service Promotion Report

## Summary

Wave 2 promotes `Event Bus Service` as canonical reusable infrastructure under `services/event-bus/`. This is a service boundary promotion only; legacy implementations remain untouched.

## Inventory

- engines/ark/legacy/ARK_SPEC.md
- engines/ark/legacy/gsb/gsb.go
- engines/ark/legacy/internal/transport/
- engines/ark/legacy/internal/adapters/natspub/publisher.go
- engines/ark/legacy/ark/src/event/wal.rs
- engines/ark/docs/duplicate-concepts.md

## Dependency Graph

- Allowed: `constitution/`, `contracts/`
- Forbidden: engines, domains, internal applications, external integrations, operations, concrete infrastructure technologies

## Consumer Graph

- ARK ingestion, replay, and promotion records
- Jarvis navigation events
- Foundry task and verification events
- Operations monitoring and audit streams
- Future engines communicating through events

## Ownership Decision

- Previous owner: legacy ARK source, with consumer-side references in Jarvis and/or Foundry where discovered
- Canonical owner: `services/event-bus/`
- Contract language: `contracts/events/`
- Confidence: High

## Minimal Promotion

- Created or normalized `services/event-bus/` service scaffold.
- Added inventory, dependency graph, consumer graph, ownership report, migration plan, verification report, and rollback plan.
- Updated governance artifacts.

## Verification

- No engine code moved.
- No runtime behavior changed.
- No executable service code added.
- Contracts remain language-only.

## Rollback

Remove `services/event-bus/` scaffold and governance rows for this promotion. No runtime rollback is required.
