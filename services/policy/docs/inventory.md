# Policy Service Inventory

## Evidence Sources

- engines/ark/legacy/policy/*.json
- engines/ark/legacy/policy/policy.go
- engines/ark/legacy/ark/policy_engine.py
- engines/ark/legacy/ark/src/policy/
- engines/foundry/legacy/ark-core/forge/mcp/policy.py
- engines/ark/legacy/ark-core/internal/epistemic/policy.go

## Classified Responsibilities

- policy evaluation boundary
- rule execution language
- authorization policy references
- promotion policy references
- architectural policy references
- decision/result vocabulary
- policy proof hooks

## Classification Decision

These items are reusable infrastructure, not ARK-, Jarvis-, or Foundry-specific behavior. Wave 2 promotes the canonical service boundary without moving legacy implementations.
