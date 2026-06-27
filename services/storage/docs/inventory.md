# Storage Service Inventory

## Evidence Sources

- engines/ark/legacy/ark/duck_client.py
- engines/ark/legacy/ark/src/storage/
- engines/ark/legacy/duckdb/
- engines/ark/legacy/internal/adapters/redisstate/store.go
- engines/ark/legacy/internal/state/README.md
- engines/foundry/README.md

## Classified Responsibilities

- abstract persistence interface
- object storage vocabulary
- metadata ownership
- versioning hooks
- transaction boundaries
- repository abstraction
- backend replaceability

## Classification Decision

These items are reusable infrastructure, not ARK-, Jarvis-, or Foundry-specific behavior. Wave 2 promotes the canonical service boundary without moving legacy implementations.
