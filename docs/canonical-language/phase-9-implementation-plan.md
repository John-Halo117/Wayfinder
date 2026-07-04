# Phase 9 Implementation Plan

This plan is implementation guidance for the next phase. It is not executed in
Phase 8D.

## Phase 9A: Contracts And Schemas

- Define Canonical Language stream schemas.
- Define Statement, Chunk, Dictionary Entry, and Occurrence records.
- Define validation issue codes.
- Add deterministic fixtures.

## Phase 9B: Deterministic Normalization Library

- Implement Canonical English v1.
- Implement block, paragraph, and statement segmentation.
- Implement word and phrase extraction.
- Add replay tests.

## Phase 9C: Dictionary Proof

- Implement append-only versioned dictionaries.
- Implement frequency indexes as rebuildable views.
- Prove deterministic rebuild from fixtures.

## Phase 9D: Chunker Proof

- Implement chunk profiles.
- Prove stable numbering and content IDs.
- Validate overlap, size caps, and source boundary rules.

## Phase 9E: Compiler Integration

- Add optional compiler input path for Canonical Statements.
- Preserve current raw-observation compiler path until parity is proven.
- Compare candidate counts and provenance quality.

## Phase 9F: Retrieval Integration

- Add Statement and Chunk retrieval units.
- Preserve current promoted-knowledge retrieval behavior.
- Prove source expansion from result to raw artifact.

## Phase 9G: Oracle Adapter Readiness

- Update ChatGPT Oracle to expose Canonical Language inputs.
- Prepare Markdown and Filesystem adapters only after the substrate is proven.

## Exit Criteria

- Same input produces identical statements, chunks, dictionaries, and
  validation reports.
- Every derived artifact traces to ARK-preserved observation or artifact.
- Compiler can consume Canonical Statements without source-specific logic.
- No AI is required for normalization.
