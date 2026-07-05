# ADR-0006: Treat Canonical Language As Derived Substrate

Status: Accepted

Date: 2026-07-03

## Architecture Sections

- [05 Representations](../architecture/05-representations.md)
- [07 Understanding](../architecture/07-understanding.md)
- [18 Cross-Cutting Systems](../architecture/18-cross-cutting.md)

## Context

First Contact validated the observation-preservation pipeline. Future Oracles
will produce language from ChatGPT, Markdown, PDFs, email, calendar, OCR,
speech, Home Assistant, filesystem, and Build Bible sources. Without a shared
language substrate, each Oracle or compiler path would duplicate
normalization, chunking, and statement extraction.

## Decision

Canonical Language is a deterministic, rebuildable, source-agnostic
normalization and compression substrate downstream of ARK and upstream of the
Knowledge Compiler. Canonical Language artifacts are derived from
ARK-preserved reality. They are not reality and not knowledge.

The primary reusable unit is the Statement. Chunks are bounded context windows
over Statements. Word and Phrase dictionaries support compression and
retrieval.

## Consequences

- Future AI consumes Canonical Statements, not raw conversations.
- AI must not own normalization.
- Raw source artifacts remain immutable and preserved by ARK.
- Canonical Language can be deleted and rebuilt from ARK-preserved reality.
- Phase 9 can implement the subsystem without deciding the core ontology.

## Evidence

- Phase 8D design brief.
- First Contact evidence that the compiler currently performs source-near
  sentence extraction and retrieval currently maintains token indexes.
- Phase 8C established Observation Sources and ARK preservation boundaries.

## Rollback

Rollback only if at least two future Oracles prove that shared language
normalization creates more ambiguity than duplication. Until then, source-local
normalization should be treated as temporary.
