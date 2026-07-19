# Promotion Audit

## Promotion Boundary

P2 correctly treats generated `Knowledge/` graph outputs as derived artifacts.
Canonical doctrine remains in constitution, canon, ADRs, contracts, roadmap,
and bootstrap documents.

## Audit Findings

| Finding | Result |
| --- | --- |
| Generated graph is not promoted as ontology. | Pass. |
| Search indexes and embeddings are non-canonical. | Pass. |
| Duplicate concepts are reported rather than merged. | Pass. |
| Conflicts remain review artifacts. | Pass. |
| Open questions are dispositioned. | Pass. |

## Promotion Risks

| Risk | Disposition |
| --- | --- |
| `Knowledge/Graph/concepts.json` contains accepted statuses for derived concepts. | Accept as generated graph status, not constitutional promotion. |
| Some historical implementation details are categorized as domain/interface concepts. | Review before ontology promotion. |
| Deprecated aliases lack closure policy. | Human decision queue. |
| RID merge/split threshold is underspecified. | Human decision queue. |
