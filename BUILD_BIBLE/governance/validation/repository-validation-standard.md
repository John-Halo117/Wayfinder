# Repository Validation Standard

Repository validation checks whether Build Bible source is coherent enough to
support review, generation, and long-term evolution.

## Validation Checks

- broken references
- missing metadata
- missing parent relationships
- orphaned documents
- circular inheritance
- circular composition
- duplicate doctrine
- duplicate patterns
- missing verification
- missing traceability
- layer violations
- composition violations
- naming violations

## Result States

- `passed`
- `warning`
- `failed`
- `not-applicable`
- `not-run`

## Failure Model

Validation failures should report:

- rule ID
- document path
- relationship or field
- reason
- canonical owner when known
- recoverable status

## Rule

Validation must preserve the distinction between source, reality record,
operations record, and generated artifact.

## Relationships

- Linter rules: [Architectural Linter Rules](architectural-linter-rules.md)
- Metadata: [Document Metadata Standard](../intelligence/document-metadata-standard.md)
- Relationship model: [Knowledge Graph Relationship Model](../intelligence/knowledge-graph-relationship-model.md)
- Reports: [Coverage Report Templates](../reports/coverage-report-templates.md)

