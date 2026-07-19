# Constitutional Impact Report

## Required Additions

| Area | Addition | Reason |
| --- | --- | --- |
| Ontology | Canonical Language, Canonical English, Statement, Chunk, Word Dictionary, Phrase Dictionary, Statement Dictionary. | Phase 8D defines a reusable derived language substrate. |
| Glossary | Same terms plus IDs and occurrence distinction. | Contributors need stable language before implementation. |
| ADR | Canonical Language as derived substrate. | Establishes non-reality, non-knowledge boundary. |
| Architecture diagrams | Insert Canonical Language between ARK and Knowledge Compiler. | Downstream compiler should consume Canonical Statements. |
| Validation rules | Rebuild determinism, provenance traceability, bounded chunking, dictionary version checks. | Prevents derived artifacts from drifting from ARK. |

## No New Engine Yet

Phase 8D does not create an engine. Implementation may later choose a service,
engine, library, or contract-backed package, but the architectural decision is
only that Canonical Language is a reusable derived substrate.

## Constitutional Invariants

- Reality remains immutable.
- Raw source artifacts remain immutable.
- Canonical Language is derived.
- Canonical Language is rebuildable.
- Canonical Language is not knowledge.
- Canonical Language is not reality.
- Every Canonical Language artifact traces to ARK-preserved reality.
- AI may consume Canonical Statements but must not own normalization.
