# 05 Representations

Representations are derived forms created from preserved reality. They include
metadata, search indexes, embeddings, OCR, summaries, feature vectors, GIS
layers, and media derivatives.

## Owns

- Derived forms.
- Rebuildability.
- Traceability to observations/evidence.
- Explicit declaration that representation is not reality.

## Does Not Own

- Source truth.
- ARK preservation.
- Knowledge promotion.
- Navigation or actions.

## Representation Audit

| Representation | Current Status | Derived Boundary |
| --- | --- | --- |
| Metadata | Present in Oracle/Knowledge outputs | Derived and provenance-backed |
| Search indexes | `Knowledge/search/sqlite.db`, `fts5.db`, retrieval store | Disposable/rebuildable |
| Embeddings | Not generated; manifest says unavailable | Correctly absent until explicit local model |
| OCR | Not implemented | Future media/document adapter |
| Summaries | Not implemented by Oracle/miner | Correctly avoided |
| Feature vectors | Deterministic token-vector in Knowledge Retrieval | Derived index |
| GIS | Planned/evidence in docs/Knowledge | No canonical runtime implementation |

## Media Architecture

Media should move toward a unified Media Graph built on Asset, Context,
Representation, Relationship, Capability, and Provenance contracts. Media
types include music, movies, TV, books, games, podcasts, photos, video,
documents, and GIS.

Supported future dynamic views:

- playlists
- mixed-media experiences
- memory capsules
- timelines
- collages
- maps

Migration rule: media-specific pipelines may be adapters, not canonical
architecture owners.

