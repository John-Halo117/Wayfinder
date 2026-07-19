# First Contact Constitutional Change Log

Date: 2026-07-03
Milestone: `v0.2-first-contact`

## Summary

Phase 8C aligned constitutional language with First Contact evidence. The
changes clarify existing boundaries; they do not add engines, Reasoning,
Jarvis, embeddings, a Knowledge Graph, or additional Oracles.

## Changes

| Area | Change | Evidence | Files |
| --- | --- | --- | --- |
| Observation Source | Promoted Observation Source as the producer of observation-shaped records. | ChatGPT Oracle emitted 110,619 observations before ARK preservation. | `constitution/architecture.md`, `constitution/execution.md`, `contracts/observations/README.md`, `canon/glossary.md`, `canon/ontology.md` |
| ARK | Clarified ARK as preservation authority for observations, provenance, Source Relationships, replay, and LVR. | ARK preserved 110,619 observations and replay validated. | `constitution/architecture.md`, `engines/ark/README.md`, `engines/ark/ingress/reality_ingestion/README.md` |
| Source Relationship | Defined explicit source relationships as evidence preserved by ARK, distinct from WEAVE topology. | ARK preserved 217,994 explicit relationships while WEAVE was not implemented. | `contracts/relationships/README.md`, `canon/glossary.md`, `canon/ontology.md`, `docs/system-architecture-v1.md` |
| Import Profile | Added bounded import posture to execution semantics and ARK docs. | Default ARK cap rejected the real export; validation succeeded with explicit caps. | `constitution/execution.md`, `constitution/architecture.md`, `engines/ark/ingress/reality_ingestion/README.md` |
| Private Validation Artifacts | Documented that generated validation payloads remain local and ignored. | First Contact produced large private generated outputs under `.wayfinder-validation/`. | `constitution/repository.md`, `docs/developer-handbook.md`, `.gitignore` |
| Candidate Page | Added ontology/glossary and future governance intake language. | Compiler hit 250,000 candidate cap; governance hit 100,000 candidate cap. | `canon/ontology.md`, `canon/glossary.md`, governance and compiler docs |
| Opaque Attachment | Added ontology/glossary term for preserved unparsed attachments. | First Contact classified 250 `.dat` source files and normalized 700 attachment artifacts. | `canon/ontology.md`, `canon/glossary.md` |
| Provenance Fields | Added `source_file` and `source_hash` as additive Oracle provenance fields. | First Contact required explicit source traceability. | Oracle models, Oracle schema docs, provenance contract |

## Non-Changes

- No new engines were added.
- No Reasoning or Jarvis implementation was added.
- No additional Oracles were added.
- No embeddings or semantic search were added.
- No Knowledge Graph was implemented.
- No historical material was deleted.

## ADRs

- `docs/adrs/0001-observation-sources.md`
- `docs/adrs/0002-source-relationships.md`
- `docs/adrs/0003-import-profiles.md`
- `docs/adrs/0004-private-validation-outputs.md`
- `docs/adrs/0005-candidate-paging-governance-intake.md`
