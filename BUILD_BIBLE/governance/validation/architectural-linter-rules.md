# Architectural Linter Rules

The architectural linter is a conceptual validation framework. P3 defines
rules; it does not implement tooling.

## Rule Classes

- duplicated doctrine
- duplicated standards
- specification inside doctrine
- generated artifacts treated as canonical
- property-specific facts inside doctrine
- operations mixed into Build Bible
- invalid layer dependencies
- missing contracts
- missing schemas
- broken composition

## Rule Outcomes

- error: invalid Build Bible source.
- warning: accepted temporarily but should be reviewed.
- info: useful improvement without blocking validity.

## Canonical Rules

| Rule ID | Severity | Description |
| --- | --- | --- |
| `BBLINT-001` | error | Doctrine duplicates another doctrine owner. |
| `BBLINT-002` | error | Standard duplicates another standard owner. |
| `BBLINT-003` | error | Doctrine contains property-specific specification. |
| `BBLINT-004` | error | Generated artifact is treated as canonical source. |
| `BBLINT-005` | error | Property-specific fact appears in doctrine. |
| `BBLINT-006` | error | Operations procedure is stored as Build Bible doctrine or pattern. |
| `BBLINT-007` | error | Document depends upward against the canonical layer order. |
| `BBLINT-008` | warning | Major pattern has no contract reference. |
| `BBLINT-009` | warning | Structured record has no schema reference. |
| `BBLINT-010` | error | Composition references missing or incompatible components. |

## Relationships

- Validation standard: [Repository Validation Standard](repository-validation-standard.md)
- Layer model: [Compiler Model](../intelligence/compiler-model.md)
- Anti-patterns: [Anti-Pattern Library](../reviews/anti-pattern-library.md)
- Reports: [Quality Report Templates](../reports/quality-report-templates.md)

