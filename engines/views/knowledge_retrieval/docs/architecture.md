# Retrieval Architecture

Knowledge Retrieval belongs to Views because it exposes derived projections over
durable knowledge.

## Boundary

Inputs:

- `PromotionRecord` from Knowledge Governance

Outputs:

- retrieval responses
- explainable ranking contributions
- index manifests
- validation reports

## Non-Goals

- raw source ingestion
- observation preservation
- candidate approval
- knowledge generation
- reasoning
- navigation
- graph database behavior

## Rebuildability

The index store supports:

- delete
- rebuild
- incremental update
- verification

Rebuilding indexes never mutates promoted knowledge.
