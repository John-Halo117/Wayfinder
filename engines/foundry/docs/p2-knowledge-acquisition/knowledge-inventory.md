# Knowledge Inventory

## Existing Generated Knowledge

| Path | Role |
| --- | --- |
| `Knowledge/Graph/` | Graph nodes, edges, provenance, relationships, facts, concepts, timeline. |
| `Knowledge/Indexes/` | Human-readable indexes for concepts, provenance, sources. |
| `Knowledge/reports/` | Conflicts, duplicates, unresolved items, timeline, quality gates. |
| `Knowledge/search/fts5.db` | Full-text retrieval index. |
| `Knowledge/search/sqlite.db` | Search/retrieval database. |
| `Knowledge/search/embeddings/manifest.json` | Embedding index manifest. |
| `Knowledge/ADR/`, `Architecture/`, `Constitution/`, `Decisions/`, `Domains/`, `Glossary/`, `Historical/`, `OpenQuestions/`, `Patterns/`, `Pipelines/`, `Requirements/`, `Research/` | Generated knowledge sections. |

## Source Participant Coverage

| Participant/source type | Current coverage |
| --- | --- |
| ChatGPT exports | Present through generated `Knowledge/` manifest and first-contact docs. |
| Markdown/docs | Present through repository docs and bootstrap artifacts. |
| ADRs | Present under `docs/adrs/` and generated `Knowledge/ADR/`. |
| Git history | Not acquired as P2 graph input in this pass. |
| PDFs/books/journals | No repository-local source corpus found in P2 scan. |
| Claude/Gemini exports | No repository-local source corpus found in P2 scan. |
