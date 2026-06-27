# Policy Service Promotion Report

## Summary

Wave 2 promotes `Policy Service` as canonical reusable infrastructure under `services/policy/`. This is a service boundary promotion only; legacy implementations remain untouched.

## Inventory

- engines/ark/legacy/policy/*.json
- engines/ark/legacy/policy/policy.go
- engines/ark/legacy/ark/policy_engine.py
- engines/ark/legacy/ark/src/policy/
- engines/foundry/legacy/ark-core/forge/mcp/policy.py
- engines/ark/legacy/ark-core/internal/epistemic/policy.go

## Dependency Graph

- Allowed: `constitution/`, `contracts/`
- Forbidden: engines, domains, internal applications, external integrations, operations, concrete infrastructure technologies

## Consumer Graph

- ARK promotion and resolver decisions
- Foundry MCP/tool gates
- Jarvis route permission checks
- Operations governance checks
- Future services that need reusable rule evaluation

## Ownership Decision

- Previous owner: legacy ARK source, with consumer-side references in Jarvis and/or Foundry where discovered
- Canonical owner: `services/policy/`
- Contract language: `contracts/policies/`
- Confidence: High

## Minimal Promotion

- Created or normalized `services/policy/` service scaffold.
- Added inventory, dependency graph, consumer graph, ownership report, migration plan, verification report, and rollback plan.
- Updated governance artifacts.

## Verification

- No engine code moved.
- No runtime behavior changed.
- No executable service code added.
- Contracts remain language-only.

## Rollback

Remove `services/policy/` scaffold and governance rows for this promotion. No runtime rollback is required.
