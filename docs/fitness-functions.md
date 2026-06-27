# Architectural Fitness Functions

Fitness functions are objective tests for Wayfinder architecture.

They define what must remain true as the repository grows.

## Core Fitness Functions

| ID | Fitness Function | Expected Result | Evidence |
| --- | --- | --- | --- |
| FIT-001 | Every concept has exactly one canonical owner. | Pass | Ownership matrix, census |
| FIT-002 | Every engine has one primary responsibility. | Pass | Engine README |
| FIT-003 | Services remain generic and reusable. | Pass | Service README, dependency rules |
| FIT-004 | Contracts contain language only and no implementation. | Pass | Contract directories |
| FIT-005 | Reality is append-only. | Pass | ARK reality docs and tests |
| FIT-006 | Durable promotion requires proof. | Pass | Promotion registry |
| FIT-007 | Shared infrastructure is owned by services. | Pass | Census, debt register |
| FIT-008 | Shared language is owned by contracts. | Pass | Contract docs |
| FIT-009 | Legacy code is isolated and visible. | Pass | `legacy/` directories, debt register |
| FIT-010 | Dependency direction follows the dependency constitution. | Pass | Dependency rules, linter |
| FIT-011 | Engine-to-engine coupling uses contracts or services. | Pass | Dependency graph |
| FIT-012 | Architectural debt is named and tracked. | Pass | Debt register |
| FIT-013 | Promotion has rollback. | Pass | Promotion registry |
| FIT-014 | Confidence improves or debt decreases after migration. | Pass | Census, scorecard |

## Example Test Statements

### One Concept, One Home

Given a concept appears in the census, it must appear in the ownership matrix
with one canonical owner or in the debt register as unresolved.

### Engine Cohesion

Given an engine README states a primary responsibility, every non-legacy module
under that engine must support that responsibility or be listed as debt.

### Contract Purity

Given a file is under `contracts/`, it must define language, schemas,
interfaces, or validation result shape. It must not own runtime behavior.

### Service Purity

Given a file is under `services/`, it must not import from `engines/`,
`domains/`, `internal/`, or `external/`.

### Proof Before Promotion

Given a concept is listed in the promotion registry, it must include proof,
date, rollback, and confidence.

## Fitness Function Failure

A failed fitness function produces a structured finding:

```json
{
  "status": "error",
  "error_code": "FITNESS_FUNCTION_FAILED",
  "reason": "A promoted concept lacks proof.",
  "context": {
    "fitness_function": "FIT-006",
    "concept": "concept-name"
  },
  "recoverable": true
}
```

