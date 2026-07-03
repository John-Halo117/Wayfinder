# ChatGPT Export Oracle

The ChatGPT Export Oracle is ARK ingress for ChatGPT data exports.

## Responsibility

The Oracle reads a ChatGPT export, inventories every file, classifies every
artifact, parses supported artifacts, preserves provenance, and emits canonical
observations plus non-inferential relationships.

## Non-Goals

- No AI summarization.
- No embeddings.
- No semantic search.
- No reasoning.
- No navigation.
- No inferred knowledge graph.

## Inputs

- A ChatGPT export directory.
- A ChatGPT export zip file.
- A single export file for narrow parser tests.

## Outputs

- `export_inventory.json`
- `artifact_inventory.json`
- `parser_inventory.json`
- `observations.jsonl`
- `relationships.jsonl`
- `import_report.json`
- `validation_report.json`
- `unknown_artifacts.json`
- `preserved_artifacts/`

## Determinism

Observation IDs, relationship IDs, artifact IDs, validation issue IDs, and export
hashes are derived from source paths, source hashes, and parsed source
identifiers. The default import timestamp is stable so repeated imports of the
same export produce identical streams.

Callers that need a real import timestamp may pass one explicitly. Reusing the
same timestamp preserves deterministic output.

## Supported Artifacts

- `conversations.json`
- memory JSON files
- project JSON files
- prompt JSON files
- metadata JSON files
- settings/configuration JSON files
- images
- documents
- attachments
- unknown artifacts, preserved and reported

## CLI

```bash
python3 -m engines.ark.ingress.chatgpt_oracle.cli /path/to/export /path/to/output
```

## Phase 2 Deliverables

- [Export Specification](docs/export-specification.md)
- [Parser Architecture](docs/parser-architecture.md)
- [Artifact Classification](docs/artifact-classification.md)
- [Observation, Provenance, and Relationship Schemas](docs/stream-schemas.md)
- [Validation Rules](docs/validation-rules.md)
- [Import Pipeline](docs/import-pipeline.md)
- [Parser Test Suite](docs/testing.md)
