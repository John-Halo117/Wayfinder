# Promotion Checklist

Every promotion must answer these questions before code or ownership moves.

## Required Answers

| Question | Required Evidence |
| --- | --- |
| Is ownership clear? | Ownership matrix entry and census reference. |
| Does behavior remain unchanged? | Test output, compatibility notes, or explicit non-runtime scope. |
| Have contracts been extracted? | Contract docs or schema references with no implementation. |
| Have services been extracted? | Service boundary docs and dependency notes. |
| Is rollback documented? | Promotion registry rollback field. |
| Are tests preserved? | Existing tests retained or mapped to new owner. |
| Has duplication decreased? | Debt register update and duplicate concept report delta. |
| Is dependency direction valid? | Dependency rules check or documented exception. |
| Is proof documented? | Proof artifact path in promotion registry. |
| Is confidence updated? | Census or registry confidence field. |

## Promotion Gate

A concept may be promoted only when:

- It has exactly one proposed canonical owner.
- Public behavior is preserved or the scope is explicitly documentation-only.
- Shared language has been extracted to contracts.
- Shared infrastructure has been extracted to services or explicitly deferred.
- Rollback is documented.
- Existing tests are preserved or replaced by equivalent checks.
- Known duplication decreases or becomes explicitly bounded debt.

## Promotion Record Template

```text
Name:
Current owner:
Previous owner:
Proof:
Date:
Rollback:
Confidence:
Debt closed:
Debt opened:
```

## Failure Model

```json
{
  "status": "error",
  "error_code": "PROMOTION_GATE_FAILED",
  "reason": "Promotion lacks documented rollback.",
  "context": {
    "concept": "concept-name"
  },
  "recoverable": true
}
```

