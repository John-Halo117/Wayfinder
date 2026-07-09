# Canonical Health Report

## Health Summary

| Dimension | Status |
| --- | --- |
| Source preservation | Healthy. |
| Historical immutability | Healthy. |
| Structural graph integrity | Healthy. |
| Relationship endpoint integrity | Healthy. |
| Conflict visibility | Healthy with unresolved review load. |
| Promotion explainability | Adequate for current derived status. |
| Constitutional uncertainty | Explicit but not fully resolved. |
| P3 readiness | Ready with human-decision caveats. |

## Health Signals

- `0` graph JSON parse errors in checked JSONL files.
- `0` missing edge endpoints.
- `0` circular references reported by existing quality gates.
- 344 conflicts remain visible.
- 4,887 duplicate groups remain visible.
- 263 unresolved facts remain visible.
- 10 P0 open questions now have dispositions.

## Canonical Risk Level

Medium.

Reason: structural integrity is strong, but several constitutional/governance
questions still require human decisions before automatic promotion or ontology
changes.
