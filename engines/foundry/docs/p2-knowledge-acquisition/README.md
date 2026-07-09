# Foundry P2 Knowledge Acquisition

P2 constructs the inherited Canonical Knowledge Graph artifact by acquiring and
organizing knowledge as provenance-backed evidence.

This pass preserves existing source and generated knowledge artifacts. It does
not rewrite historical conversations, delete source material, merge concepts
without evidence, or treat embeddings as canonical.

## Inheritance

- Bootstrap artifacts.
- P0 constitutional artifacts.
- P1 repository discovery artifacts.
- Existing generated `Knowledge/` graph artifacts.

## Outputs

- [Canonical Knowledge Graph](canonical-knowledge-graph.md)
- [Eisengarten Corpus](eisengarten-corpus.md)
- [Wayfinder Corpus](wayfinder-corpus.md)
- [Historical Corpus](historical-corpus.md)
- [Relationship Graph](relationship-graph.md)
- [Timeline](timeline.md)
- [Promotion Report](promotion-report.md)
- [Conflict Report](conflict-report.md)
- [Knowledge Inventory](knowledge-inventory.md)
- [Extraction Report](extraction-report.md)

## Boundary

Everything downstream of source reality is derived. Embeddings, FTS indexes,
SQLite search databases, and reports are retrieval or review surfaces, not
canonical ontology.
