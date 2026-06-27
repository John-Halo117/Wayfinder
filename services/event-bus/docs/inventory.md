# Event Bus Service Inventory

## Evidence Sources

- engines/ark/legacy/ARK_SPEC.md
- engines/ark/legacy/gsb/gsb.go
- engines/ark/legacy/internal/transport/
- engines/ark/legacy/internal/adapters/natspub/publisher.go
- engines/ark/legacy/ark/src/event/wal.rs
- engines/ark/docs/duplicate-concepts.md

## Classified Responsibilities

- publish language and boundary
- subscribe language and boundary
- routing metadata
- event metadata
- correlation identifiers
- replay support boundaries
- transport-agnostic event flow

## Classification Decision

These items are reusable infrastructure, not ARK-, Jarvis-, or Foundry-specific behavior. Wave 2 promotes the canonical service boundary without moving legacy implementations.
