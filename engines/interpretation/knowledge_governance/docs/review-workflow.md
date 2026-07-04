# Review Workflow

## First Contact Intake Rule

Candidate review intake must be bounded. When compiler output exceeds one
repository limit, candidates should arrive as deterministic Candidate Pages.
Each page must preserve candidate provenance, grouping keys, review status,
and validation issues without promoting knowledge.

Streaming or paged intake is a future implementation requirement; this document
does not add a new governance engine.

Every candidate starts in `discovered`.

```text
discovered
  -> under_review
  -> approved
  -> promoted
```

Other terminal or holding states:

- `rejected`
- `deferred`
- `superseded`

No candidate may move from `discovered` directly to `approved` or `promoted`.

Every human action requires:

- reviewer
- rationale
- deterministic timestamp
- immutable review history entry
- governance event

## Merge

Merge is human-approved supersession. The source candidate is marked
`superseded`, the target candidate remains independently preserved, and evidence
is not collapsed.

## Supersession

Supersession requires a valid replacement candidate reference.
