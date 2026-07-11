# Schemas

Schemas define machine-checkable structure for Build Bible records.

Human-readable semantics live in `contracts/`. These schemas exist so future
tools can validate compiler input before generating physical-world artifacts.

## Validation Rule

A generator must reject records that fail the schema required for its input
type. Unknown or unverified physical facts must be represented explicitly
instead of inferred silently.

## Core Schemas

- `universal-scope.schema.json`
- `physical-scope.schema.json`
- `resource-flow.schema.json`
- `dependency.schema.json`
- `reliability-record.schema.json`
- `operational-state.schema.json`
- `spine.schema.json`
- `interface.schema.json`
- `capability.schema.json`
- `maintenance-procedure.schema.json`
- `observation.schema.json`
- `decision-record.schema.json`
- `digital-twin-state.schema.json`
- `generated-artifact-manifest.schema.json`
