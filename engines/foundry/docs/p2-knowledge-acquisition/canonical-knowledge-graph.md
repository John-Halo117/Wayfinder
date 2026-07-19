# Canonical Knowledge Graph

## Canonical Artifact

| Artifact | Path | Role |
| --- | --- | --- |
| Nodes | `Knowledge/Graph/nodes.jsonl` | Canonical derived graph nodes. |
| Edges | `Knowledge/Graph/edges.jsonl` | Canonical derived graph relationships. |
| Entities | `Knowledge/Graph/entities.jsonl` | Extracted entity/object records. |
| Provenance | `Knowledge/Graph/provenance.jsonl` | Evidence lineage records. |
| Concepts | `Knowledge/Graph/concepts.json` | Extracted concept index. |
| Sources | `Knowledge/Graph/sources.json` | Source manifest for graph inputs. |
| Timeline | `Knowledge/Graph/timeline.jsonl` | Chronological graph observations/events. |

## Observed Scale

| Measure | Count |
| --- | ---: |
| Graph nodes | 39,325 |
| Graph edges | 122,877 |
| Entity records | 28,193 |
| Provenance records | 30,361 |
| Timeline records | 29,631 |
| Concepts in manifest | 40 |
| Conversations in manifest | 1,656 |
| Messages in manifest | 108,688 |
| Facts in manifest | 27,935 |
| Relationships in manifest | 64,060 |

## Object Contract

Every canonical graph object must carry or resolve to:

- Stable ID.
- Type.
- Provenance.
- Confidence.
- Lineage.
- Promotion state.

## Canonical Boundary

- Source conversations and artifacts remain historical evidence.
- Graph records are derived and rebuildable.
- Search indexes are retrieval surfaces.
- Embeddings are retrieval indexes only and are never canonical knowledge.
