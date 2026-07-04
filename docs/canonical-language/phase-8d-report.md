# Phase 8D Canonical Language Report

Date: 2026-07-03

## Objective

Design the Canonical Language subsystem before implementation. The design is
implementation-independent and applies to ChatGPT, Markdown, PDFs, email,
calendar, Home Assistant, Build Bible, filesystem, OCR, speech transcripts, and
future Oracles.

## Deliverable Map

| Deliverable | Location |
| --- | --- |
| Canonical Language Architecture | `docs/canonical-language/architecture.md` |
| Canonical Language ADR | `docs/adrs/0006-canonical-language-substrate.md` |
| Dictionary Architecture | `docs/canonical-language/dictionary-architecture.md` |
| Compression Architecture | `docs/canonical-language/compression-architecture.md` |
| Statement Architecture | `docs/canonical-language/statement-architecture.md` |
| Chunk Architecture | `docs/canonical-language/chunk-architecture.md` |
| Relationship Architecture | `docs/canonical-language/relationship-architecture.md` |
| Cross-Oracle Language Specification | `docs/canonical-language/cross-oracle-language-specification.md` |
| Storage Strategy | `docs/canonical-language/storage-strategy.md` |
| Retrieval Strategy | `docs/canonical-language/retrieval-strategy.md` |
| Space Efficiency Analysis | `docs/canonical-language/space-efficiency-analysis.md` |
| Constitutional Impact Report | `docs/canonical-language/constitutional-impact.md` |
| Updated Ontology | `canon/ontology.md` |
| Updated Glossary | `canon/glossary.md` |
| Updated Architecture Diagrams | `docs/system-architecture-v1.md` |
| Implementation Plan for Phase 9 | `docs/canonical-language/phase-9-implementation-plan.md` |

## Core Decisions

- Canonical Language is derived and rebuildable.
- Canonical Language is not reality and not knowledge.
- The primary reusable unit is the Statement.
- Chunks are bounded context windows over Statements.
- Word and Phrase dictionaries support compression and retrieval.
- Stable identity separates content IDs from occurrence IDs.
- AI may consume Canonical Statements later, but AI must never own
  normalization.

## Contract Impact

No runtime contract is added in Phase 8D. The design recommends a future
Canonical Language contract or schema set in Phase 9 after implementation
records are drafted and validated.

## Validation Scope

Phase 8D validation should confirm:

- documentation links resolve
- existing tests still pass
- no runtime subsystem was implemented
- architecture diagrams include Canonical Language as derived substrate

## Validation Results

Executed after the design update:

```bash
python3 -m pytest -s engines/ark/tests/test_chatgpt_oracle.py engines/ark/tests/test_reality_ingestion.py engines/interpretation/tests/test_knowledge_compiler.py engines/interpretation/tests/test_knowledge_governance.py engines/views/tests/test_knowledge_retrieval.py engines/views/tests/test_knowledge_views.py services/identity/tests/test_identity_service.py services/event-bus/tests/test_event_bus_service.py
python3 -m compileall engines/ark/ingress/chatgpt_oracle engines/ark/ingress/reality_ingestion engines/interpretation engines/views services/identity services/event-bus
```

Results:

- Focused tests: 47 passed.
- Compile validation: passed.
- Markdown link validation: `markdown_links_ok`.
