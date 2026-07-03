# Import Pipeline

```text
Load export
  -> discover files
  -> hash files
  -> classify artifacts
  -> register export artifact
  -> parse supported artifacts
  -> emit observations
  -> emit explicit relationships
  -> validate streams
  -> write outputs
  -> preserve source artifacts by hash
```

## Bounded Operations

- File count is bounded by `OracleLimits.max_files`.
- File size is bounded by `OracleLimits.max_file_bytes`.
- JSON parse size is bounded by `OracleLimits.max_json_bytes`.
- Message relationship count is bounded by
  `OracleLimits.max_relationships_per_message`.

## Output Files

- `export_inventory.json`
- `artifact_inventory.json`
- `parser_inventory.json`
- `observations.jsonl`
- `relationships.jsonl`
- `import_report.json`
- `validation_report.json`
- `unknown_artifacts.json`
- `preserved_artifacts/`
