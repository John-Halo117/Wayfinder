# Repository Folding

Repository folding moves existing projects into the Wayfinder master repository
while preserving architectural ownership.

## Contract

Input:

- A source repository or project directory.
- Its current responsibility, interfaces, dependencies, and durable state.
- Any existing tests, documentation, migrations, and operational scripts.

Output:

- A classified destination under the Wayfinder monorepo.
- Preserved source files, history notes, and ownership metadata.
- Explicit dependency direction.
- A health signal or status surface for executable modules.

Constraints:

- No source project is folded until its concept is classified.
- Existing durable reality or evidence remains append-only.
- Shared concepts are extracted into contracts, services, or capabilities.
- Engine code must follow the canonical engine structure.
- External integrations stay replaceable.

## Folding Procedure

1. Inventory the repository.
2. Identify concepts, interfaces, runtime dependencies, durable state, tests,
   and operational concerns.
3. Classify each concept using `docs/classification.md`.
4. Choose one canonical home for each concept.
5. Move implementation files to the classified destination.
6. Move shared language to `contracts/`.
7. Move reusable infrastructure to `services/`.
8. Move unique responsibilities to `engines/<engine-name>/`.
9. Move third-party adapters to `external/<system-name>/`.
10. Move app surfaces to `internal/<app-name>/`.
11. Move deployment and runtime workflows to `operations/`.
12. Move developer scripts to `tooling/`.
13. Add references instead of duplicating concepts.
14. Run tests and record any gaps.

## Required Migration Deliverables

Every migration task must produce:

1. Inventory
2. Classification table
3. Dependency graph
4. Ownership graph
5. Duplicate concept report
6. Service extraction opportunities
7. Contract extraction opportunities
8. Migration plan
9. Verification checklist
10. Rollback plan

These deliverables are evidence. Do not promote migrated concepts without them.

## Destination Examples

```text
legacy-api/              -> internal/api/
home-assistant-adapter/  -> external/home-assistant/
shared-event-store/      -> services/persistence/
reasoning-worker/        -> engines/reasoning/
inventory-product/       -> domains/inventory/
deployment-scripts/      -> operations/deployment/
codegen-cli/             -> tooling/code-generation/
```

## Failure Modes

```json
{
  "status": "error",
  "error_code": "UNCLASSIFIED_CONCEPT",
  "reason": "The source repository contains a concept without a canonical architectural owner.",
  "context": {
    "source": "path/to/source"
  },
  "recoverable": true
}
```

```json
{
  "status": "error",
  "error_code": "DEPENDENCY_DIRECTION_VIOLATION",
  "reason": "A folded module depends upward in the architectural stack.",
  "context": {
    "source": "path/to/source",
    "dependency": "path/to/dependency"
  },
  "recoverable": true
}
```

```json
{
  "status": "error",
  "error_code": "DUPLICATE_CONCEPT_OWNER",
  "reason": "A concept is defined in more than one canonical location.",
  "context": {
    "concept": "concept-name"
  },
  "recoverable": true
}
```
