# Build Bible Compiler Model

The Build Bible compiler is the conceptual pipeline that transforms canonical
physical source into generated outputs.

No compiler implementation is defined in P3.

## Canonical Pipeline

```text
Doctrine
  -> Contracts
  -> Schemas
  -> Patterns
  -> Specifications
  -> Reality Records
  -> Validation
  -> Generation
  -> CAD
  -> BIM
  -> Bills Of Materials
  -> Construction Packages
  -> Inspection Packages
  -> Maintenance Packages
  -> Digital Twin
```

## Compiler Inputs

- doctrine
- contracts
- schemas
- ontologies
- patterns
- standards
- specifications
- reality records
- lifecycle records
- operations references when generating operating packages

## Compiler Checks

- layer validity
- schema validity
- relationship validity
- traceability completeness
- composition validity
- verification state
- generated artifact manifest completeness

## Compiler Outputs

- CAD
- BIM
- bills of materials
- construction packages
- inspection packages
- maintenance packages
- digital twin exports
- documentation
- configuration outputs

## Rule

Generated outputs are disposable. If a generated output contains new canonical
truth, that truth must be promoted back into Build Bible source.

## Relationships

- Generation contract: [Generation Contract](../generation-contract.md)
- Generated manifest schema: [generated-artifact-manifest.schema.json](../../schemas/generated-artifact-manifest.schema.json)
- Validation: [Repository Validation Standard](../validation/repository-validation-standard.md)
- Quality reports: [Generated Artifact Readiness](../reports/coverage-report-templates.md)

