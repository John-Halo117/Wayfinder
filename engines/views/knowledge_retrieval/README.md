# Knowledge Retrieval

Knowledge Retrieval builds disposable indexes over promoted knowledge records.

It does not create knowledge, preserve reality, modify promoted records, reason,
navigate, approve candidates, or become a source of truth.

```text
Durable Knowledge
  -> Knowledge Indexes
  -> Retrieval Results
```

Indexes may be deleted and rebuilt at any time. Every retrieval result preserves
traceability back to the promotion record, candidate provenance, compiler output,
and supporting ARK observations.

## Implemented Indexes

- full text
- BM25
- deterministic token-vector embedding
- hybrid retrieval
- timeline
- RID / observation / promotion lookup
- concept
- capability
- acronym
- relationship traversal

## Retrieval Interfaces

- `search`
- `find`
- `lookup`
- `related`
- `timeline`
- `history`
- `neighbors`
- `autocomplete`
- `suggestions`

## Documentation

- [Architecture](docs/architecture.md)
- [Interfaces](docs/interfaces.md)
- [Index types](docs/index-types.md)
- [Validation](docs/validation.md)
