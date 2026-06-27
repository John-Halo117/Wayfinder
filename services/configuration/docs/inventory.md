# Configuration Service Inventory

## Evidence Sources

- engines/ark/legacy/ark/config.py
- engines/ark/legacy/internal/config/env.go
- engines/ark/legacy/config/manifest.json
- engines/ark/legacy/config/ark.env
- engines/ark/legacy/ark-core/config/operating_rules.json
- engines/foundry/legacy/ark-core/forge/runtime/config.py
- engines/jarvis/ingress/.env.example

## Classified Responsibilities

- configuration loading language
- layered configuration order
- environment abstraction
- defaults and override vocabulary
- configuration validation boundary
- runtime configuration access
- configuration redaction expectations

## Classification Decision

These items are reusable infrastructure, not ARK-, Jarvis-, or Foundry-specific behavior. Wave 2 promotes the canonical service boundary without moving legacy implementations.
