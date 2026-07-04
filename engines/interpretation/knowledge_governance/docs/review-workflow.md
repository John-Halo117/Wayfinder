# Review Workflow

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
