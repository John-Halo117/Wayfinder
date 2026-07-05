# ADR 0009: Add Candidate Pages For Bounded Knowledge Governance

Status: Proposed

Date: 2026-07-05

## Context

First Contact showed that real exports can produce candidate volumes larger
than the current governance repository cap. The Knowledge Compiler remains
proposal-only, but Governance must review candidates without requiring a single
unbounded intake batch.

`canon/ontology.md` already records Candidate Page as a proposed concept.

## Decision

Introduce Candidate Pages as deterministic, bounded slices of compiler output.
Pages preserve candidate IDs, provenance, confidence, uncertainty, grouping,
and replay identity. Governance may accept, reject, or partially fail pages
without mutating candidate meaning.

## Alternatives Considered

- Increase governance caps. Rejected because it does not improve reviewability.
- Compress candidates into summaries. Rejected because it would lose evidence.
- Promote candidates automatically. Rejected because human review is
  constitutional.

## Tradeoffs

Candidate Pages add one more review artifact, but they preserve bounded,
human-reviewable governance at export scale.

## Migration Plan

1. Define Candidate Page schema and stable page IDs.
2. Add repository intake for pages with deterministic replay.
3. Add validation for partial page failures.
4. Update review views to expose page and group context.
5. Keep existing candidate APIs during migration.
