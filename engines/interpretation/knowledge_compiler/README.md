# Knowledge Compiler

The Knowledge Compiler is the first interpretation layer after ARK reality
preservation.

It consumes only canonical observations already preserved by ARK and produces
candidate knowledge. It does not preserve reality, update LVR, promote truth,
generate RIDs, navigate, search, embed, or call AI.

## Pipeline

```text
ARK preserved observations
  -> compiler validation
  -> deterministic rule execution
  -> novelty, duplicate, and contradiction checks
  -> confidence and uncertainty assignment
  -> candidate knowledge artifacts
```

## Candidate Types

- concept
- decision
- principle
- adr
- glossary
- amendment
- capsule
- todo
- novelty
- duplicate
- contradiction

## Provenance

Every candidate includes:

- compiler version
- rule set version
- supporting observations
- supporting reality IDs
- supporting conversations
- supporting messages
- source Oracles
- supporting timestamps
- import timestamps
- content hashes

## Deterministic First

This implementation uses rules, existing glossary baselines supplied through
configuration, lexical pattern matching, and deterministic scoring. AI fallback
is intentionally not implemented in this phase.

## First Contact Scale Lesson

First Contact showed that real private exports can produce more candidates
than governance can review in one bounded batch. The compiler remains
proposal-only, but future work must support Candidate Pages and grouping before
governance intake. Candidate paging must preserve candidate IDs, provenance,
confidence, uncertainty, and deterministic replay.

## Non-Goals

- source ingestion
- reality preservation
- provenance mutation
- LVR updates
- embeddings
- vector databases
- semantic search
- navigation
- knowledge graph construction
- canonical glossary or constitution edits

## Documentation

- [Architecture](docs/architecture.md)
- [Candidate schemas](docs/candidate-schemas.md)
- [Rule families](docs/rules.md)
- [Validation](docs/validation.md)
