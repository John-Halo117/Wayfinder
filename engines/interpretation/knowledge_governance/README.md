# Knowledge Governance

Knowledge Governance reviews and promotes candidate knowledge produced by the
Knowledge Compiler.

It keeps four layers distinct:

```text
Reality
  -> Candidate Knowledge
  -> Approved Knowledge
  -> Promoted Knowledge
```

The human reviewer remains the authority. This package never promotes
autonomously, never modifies ARK, never rewrites evidence, and never edits
canonical documents directly.

## Responsibilities

- store candidate artifacts
- accept bounded Candidate Pages or grouped candidate intake when candidate
  volume exceeds one repository batch
- group related candidates
- expose deterministic review views
- preserve review history
- preserve merge and supersession history
- require human rationale for review actions
- require approval before promotion
- create durable promotion records
- retain candidate provenance in promoted artifacts
- emit deterministic governance event records

## Non-Goals

- observation generation
- ARK mutation
- provenance mutation
- autonomous reasoning
- automatic constitutional promotion
- embeddings
- vector databases
- semantic search
- navigation
- Jarvis behavior

## First Contact Scale Lesson

First Contact produced 250,000 compiler candidates and exceeded the current
100,000 candidate repository cap. Governance must remain bounded and
human-reviewed; future intake should accept deterministic Candidate Pages or
grouped pages instead of requiring a single unbounded batch.

## Documentation

- [Review workflow](docs/review-workflow.md)
- [Promotion workflow](docs/promotion-workflow.md)
- [Review views](docs/review-views.md)
- [Validation rules](docs/validation.md)
