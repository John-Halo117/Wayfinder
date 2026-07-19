# Extraction Report

## Pipeline

```text
Acquire
-> Normalize
-> Extract
-> Reality Compiler
-> Canonicalization
-> Conflict Detection
-> Relationship Resolution
-> Promotion
-> Canonical Knowledge Graph
```

## Current Evidence

The existing graph was generated with deterministic marker rules and no AI
summarization according to `Knowledge/manifest.json`.

Privacy notes from the manifest:

- Raw export was not copied.
- Provenance uses IDs and hashes.
- Extraction method was deterministic marker rules.

## Validation

| Requirement | Result |
| --- | --- |
| Every object has provenance. | Supported by `Knowledge/Graph/provenance.jsonl`; full per-object proof not re-run in P2. |
| Every object has stable identity. | Supported by graph IDs and generated manifests. |
| Relationships reference graph objects. | Supported by graph files; unresolved/conflict reports remain explicit. |
| Historical artifacts remain unchanged. | Pass; P2 added wrapper artifacts only. |
| Canonical concepts remain distinct from implementations. | Pass by P2 boundary and P0/P1 inheritance. |
| Duplicate concepts are linked rather than duplicated. | Duplicates are reported, not silently merged. |
| Promotion decisions are explainable. | Promotion contract defined; existing graph remains derived unless promoted by canonical docs. |

## Embeddings

Embeddings are permitted only as retrieval indexes. The embedding manifest under
`Knowledge/search/embeddings/` is not canonical knowledge.
