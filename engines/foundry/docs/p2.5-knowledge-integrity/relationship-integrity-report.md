# Relationship Integrity Report

## Validated

| Relationship property | Result |
| --- | --- |
| Edge JSONL parse integrity | Pass: 122,877 edges parsed. |
| Edge source/target fields | Pass: all edges expose `source_id` and `target_id`. |
| Endpoint reference validity | Pass: 245,754 endpoint checks, `0` missing endpoints. |
| Circular references in quality gate | Pass: existing report records `0`. |

## Relationship Classes Audited

- Parent-child relationships.
- Dependency relationships.
- Capability relationships.
- Constitutional traceability.
- Layer ownership.
- Historical lineage.

## Remaining Relationship Risks

| Risk | Explanation |
| --- | --- |
| Semantic validity not fully proven. | Endpoint existence does not prove relationship meaning is canonical. |
| Historical evolution may appear as contradiction. | Requires human or governance review before reconciliation. |
| Capability relationships are early. | P1 marks capability registry as scaffold/medium confidence. |
| Legacy lineage is cluster-level. | P1 did not decompose every legacy module. |
