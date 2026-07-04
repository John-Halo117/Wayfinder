# Retrieval Interfaces

## Mutation

- `delete_indexes()`
- `rebuild(promotions)`
- `incremental_update(promotions)`
- `verify()`

## Retrieval

- `search(query, mode, limit)`
- `find(query, limit)`
- `lookup(reference_type, value, limit)`
- `related(reference, limit)`
- `timeline(conversation_id, reverse, limit)`
- `history(candidate_id, limit)`
- `neighbors(reference, limit)`
- `autocomplete(prefix, limit)`
- `suggestions(prefix, limit)`

## Result Shape

Each result includes:

- promoted knowledge document
- score
- matched terms
- ranking contributions
- promotion provenance
- supporting observations
- compiler version
- promotion version
- confidence
- uncertainty
