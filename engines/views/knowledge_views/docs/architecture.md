# Knowledge Views Architecture

Knowledge Views belongs to the Views engine. It presents promoted knowledge and
retrieval results without owning the underlying knowledge.

## Inputs

- `KnowledgeIndexStore`
- retrieval responses
- optional Knowledge Governance candidate records

## Outputs

- deterministic `ViewResult` projections
- `ViewItem` presentation records
- view definitions
- validation reports

## Non-Goals

- reality preservation
- knowledge generation
- candidate approval
- promotion
- reasoning
- navigation
- AI summarization

## Refresh Strategy

Views are regenerated from promoted knowledge, retrieval indexes, and candidate
records. They may be discarded and rebuilt without losing knowledge.
