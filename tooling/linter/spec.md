# Constitutional Linter Specification

This document specifies the constitutional linter. It does not implement it.

## Purpose

The linter detects architectural drift before it becomes technical debt.

## Inputs

- `WAYFINDER.md`
- `constitution/`
- `contracts/`
- `services/`
- `engines/`
- `domains/`
- `internal/`
- `external/`
- `operations/`
- `docs/ownership-matrix.md`
- `docs/constitutional-census.md`
- `docs/architectural-debt.md`
- `docs/promotion-registry.md`
- `docs/dependency-rules.md`

## Output Schema

```json
{
  "status": "ok",
  "summary": {
    "checks_run": 0,
    "findings": 0
  },
  "findings": []
}
```

Finding schema:

```json
{
  "status": "error",
  "error_code": "STRING",
  "reason": "STRING",
  "context": {},
  "recoverable": true
}
```

## Required Checks

| Check | Error Code | Description |
| --- | --- | --- |
| Duplicate ownership | `DUPLICATE_CANONICAL_OWNER` | A concept has more than one canonical owner. |
| Missing ownership | `MISSING_CANONICAL_OWNER` | A concept appears in census or docs without an owner. |
| Service importing engine | `SERVICE_IMPORTS_ENGINE` | A service depends on an engine. |
| Engine importing engine | `ENGINE_IMPORTS_ENGINE` | An engine imports another engine without a contract/service boundary. |
| Contract implementation | `CONTRACT_CONTAINS_IMPLEMENTATION` | A contract directory contains executable implementation. |
| Circular dependency | `CIRCULAR_DEPENDENCY` | Architectural dependency graph contains a cycle. |
| Duplicate schema | `DUPLICATE_SCHEMA` | Equivalent schema language exists in multiple canonical homes. |
| Duplicate identity | `DUPLICATE_IDENTITY_CONCEPT` | RID, aliases, namespaces, or identity lifecycle are defined outside Identity. |
| Infrastructure duplication | `DUPLICATE_INFRASTRUCTURE` | Engine/domain/internal code owns generic infrastructure. |
| Missing documentation | `MISSING_ARCHITECTURAL_DOC` | Canonical owner lacks README or boundary docs. |
| Missing promotion proof | `MISSING_PROMOTION_PROOF` | Promotion registry entry lacks proof. |
| Missing rollback | `MISSING_ROLLBACK` | Promotion registry entry lacks rollback. |
| Legacy escape | `LEGACY_OUTSIDE_BOUNDARY` | Legacy source exists outside documented `legacy/` or debt locations. |

## File Classification Rules

The linter should classify paths by top-level directory:

- `constitution/`: constitutional knowledge
- `contracts/`: shared language only
- `capabilities/`: stable architectural verbs
- `services/`: reusable infrastructure
- `engines/`: unique responsibilities
- `domains/`: real-world composition
- `internal/`: Wayfinder-owned applications
- `external/`: replaceable integrations
- `operations/`: runtime infrastructure
- `tooling/`: developer tooling

## Contract Purity Heuristic

Flag executable files under `contracts/` unless explicitly listed as schema
validation examples with no runtime ownership.

Initial executable extensions:

- `.py`
- `.go`
- `.rs`
- `.ts`
- `.js`
- `.sh`
- `.ps1`

## Dependency Heuristic

The linter should parse imports where possible and fall back to text scanning
when needed.

Bounded scan limits:

- Maximum file size: 1 MiB per file.
- Maximum files per run: 10000.
- Maximum runtime: 60 seconds.

## Severity

| Severity | Meaning |
| --- | --- |
| P0 | Constitutional violation blocks promotion. |
| P1 | High-risk drift; must be resolved or registered as debt. |
| P2 | Medium-risk drift; may proceed with explicit debt entry. |
| P3 | Informational observation. |

## Non-Goals

- Do not enforce business logic.
- Do not rewrite files.
- Do not migrate code.
- Do not infer canonical ownership without evidence.

