# Contributing

Every contribution must preserve the constitutional architecture.

## Required Flow

1. Classify the concept before implementation.
2. Confirm the canonical owner.
3. Prefer extension and composition.
4. Keep shared infrastructure in `services/`.
5. Keep unique responsibilities in `engines/`.
6. Treat working state as ephemeral.
7. Require proof before promotion to durable state.
8. Verify dependency direction.

## Migration Flow

Migration work must follow the Constitutional Migration Agent guidance in
`docs/constitutional-migration-agent.md`.

Do not redesign before discovery. Do not promote a concept without inventory,
classification, dependency evidence, ownership evidence, duplicate analysis,
extraction opportunities, a migration plan, verification checklist, and rollback
plan.

## ARK Compliance

Code contributions must be bounded, observable, verifiable, and explicit.

- Loops require explicit iteration or time bounds.
- Runtime and memory expectations must be documented.
- Dependencies must be passed explicitly.
- Interfaces must reject invalid inputs.
- Failures must use structured error objects or explicit exceptions.
- Outputs must be structured and testable.
