# Knowledge Integrity Report

## Scope

Validated inherited P2 graph artifacts under `Knowledge/Graph/` and inherited
P0/P1/P2 reports.

## Structural Checks

| Check | Result | Evidence |
| --- | --- | --- |
| JSONL graph files parse. | Pass | `nodes.jsonl`, `edges.jsonl`, `entities.jsonl`, `provenance.jsonl`, `timeline.jsonl` parsed with `0` bad JSON records. |
| Edge endpoints exist. | Pass | 245,754 source/target endpoint checks; `0` missing endpoints. |
| Edges expose source and target fields. | Pass | `source_id` and `target_id` present on 122,877 edges. |
| Provenance records exist. | Pass | 30,361 provenance records. |
| Timeline records exist. | Pass | 29,631 timeline records. |
| Existing quality gate reports no circular references. | Pass | `Knowledge/reports/quality_gates.json` reports `circular_reference_count: 0`. |
| Conflicts remain explicit. | Pass with unresolved work | 344 contradiction/conflict facts remain reported. |
| Duplicate normalized groups remain explicit. | Pass with unresolved work | 4,887 duplicate groups remain reported. |
| Unresolved facts remain explicit. | Pass with unresolved work | 263 unresolved facts remain reported. |

## Integrity Findings

- Graph object identity is carried through `stable_id`, `uuid`, and domain IDs
  rather than a single uniform `id` field.
- P2 promotion boundaries are correct: generated graph artifacts remain derived
  and do not replace constitutional/canonical source documents.
- Retrieval assets under `Knowledge/search/` remain non-canonical indexes.

## Integrity Risks

| Risk | Status |
| --- | --- |
| Not every graph object was proven to have a one-to-one provenance record. | Requires future deeper graph validation. |
| Duplicate groups may contain valid historical repetition rather than true concept duplication. | Requires review. |
| Some contradictions may be historical evolution rather than active conflict. | Requires review. |
