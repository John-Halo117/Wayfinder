# Identity Service Promotion Report

## Summary

Wave 2 promotes `Identity Service` as canonical reusable infrastructure under `services/identity/`. This is a service boundary promotion only; legacy implementations remain untouched.

## Inventory

- engines/ark/legacy/ark/subjects.py
- engines/ark/legacy/internal/subjects/subjects.go
- engines/ark/legacy/policy/ark_identity_rules.json
- engines/ark/docs/extraction-opportunities.md
- engines/ark/docs/duplicate-concepts.md
- engines/foundry/README.md

## Dependency Graph

- Allowed: `constitution/`, `contracts/`
- Forbidden: engines, domains, internal applications, external integrations, operations, concrete infrastructure technologies

## Consumer Graph

- ARK reality and evidence records
- Jarvis navigation subjects
- Foundry execution/session attribution
- Event Bus event actor/source metadata
- Storage object ownership metadata

## Ownership Decision

- Previous owner: legacy ARK source, with consumer-side references in Jarvis and/or Foundry where discovered
- Canonical owner: `services/identity/`
- Contract language: `contracts/identities/`
- Confidence: High

## Minimal Promotion

- Created or normalized `services/identity/` service scaffold.
- Added inventory, dependency graph, consumer graph, ownership report, migration plan, verification report, and rollback plan.
- Updated governance artifacts.

## Verification

- No engine code moved.
- No runtime behavior changed.
- No executable service code added.
- Contracts remain language-only.

## Rollback

Remove `services/identity/` scaffold and governance rows for this promotion. No runtime rollback is required.
