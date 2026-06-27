# Identity Service Inventory

## Evidence Sources

- engines/ark/legacy/ark/subjects.py
- engines/ark/legacy/internal/subjects/subjects.go
- engines/ark/legacy/policy/ark_identity_rules.json
- engines/ark/docs/extraction-opportunities.md
- engines/ark/docs/duplicate-concepts.md
- engines/foundry/README.md

## Classified Responsibilities

- RID generation and validation vocabulary
- canonical identity records
- alias resolution
- namespace handling
- identity lifecycle state language
- identity lookup boundaries
- merge semantics and conflict vocabulary

## Classification Decision

These items are reusable infrastructure, not ARK-, Jarvis-, or Foundry-specific behavior. Wave 2 promotes the canonical service boundary without moving legacy implementations.
