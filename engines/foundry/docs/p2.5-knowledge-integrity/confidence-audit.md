# Confidence Audit

## High Confidence

| Area | Evidence |
| --- | --- |
| Bootstrap sequence and required artifacts | `bootstrap.yaml`, `bootstrap.lock`, bootstrap validation report. |
| Constitutional layer ownership | P0 model, `constitution/`, `docs/architecture/`. |
| Repository component map | P1 repository model and inventory. |
| Graph structural parse integrity | P2.5 JSONL validation. |
| Edge endpoint validity | 245,754 endpoint checks with `0` missing endpoints. |

## Medium Confidence

| Area | Reason |
| --- | --- |
| Eisengarten corpus | Present through `WAYFINDER.md`, standalone source missing. |
| Amendment model | ADRs exist; amendment ledger not found. |
| Vocabulary promotion | Canonical naming exists; promotion authority not explicit. |
| Generated graph semantic correctness | Structure is strong; semantic conflicts remain reported. |

## Low Confidence

| Area | Reason |
| --- | --- |
| Operational maturity requirements | No canonical maturity implementation found in P2.5 scope. |
| Complete legacy module ownership | P1 maps legacy at cluster level. |
| Git history knowledge acquisition | Not present in current graph. |
| Non-ChatGPT participant coverage | No Claude/Gemini/PDF/book/journal corpora found locally. |

## Review Triggers

- Low-confidence canonical concepts.
- Weakly supported relationships.
- Sparse evidence concepts.
- Conflicting evidence with high architectural impact.
- Generated concepts marked accepted but not reflected in constitution/canon.
