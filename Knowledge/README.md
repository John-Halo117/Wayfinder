# Wayfinder Knowledge Base

This directory is generated from historical ChatGPT export evidence.
It contains derived architecture facts, graph data, and provenance indexes.
Raw export conversations are not copied into this repository.

## Invariants

- Historical conversations are evidence, not canonical documentation.
- Every extracted fact has source conversation and message provenance.
- Generation is deterministic and uses no AI summarization.
- Reruns use stable source hashes, fact IDs, concept IDs, and relationship IDs.

## Inventory

- Source hash: `34c9594b92eea3185e75a5749a9f7bc01187b14b9289c4ac293cca0f8fc7da6a`
- Source files: 525
- Conversations: 1656
- Messages inspected: 108688
- Extracted facts: 27935
- Concepts: 40
- Relationships: 64060

## Primary Outputs

- `Graph/facts/index.json`: machine-readable extracted facts with provenance, chunked for reviewability.
- `Graph/concepts.json`: stable concept nodes.
- `Graph/relationships/index.json`: evidence-backed graph edges, chunked for reviewability.
- `Historical/timeline.md`: chronological project history index.
- `Indexes/provenance.md`: provenance and source evidence index.
