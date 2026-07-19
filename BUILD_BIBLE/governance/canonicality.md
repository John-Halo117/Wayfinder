# Canonicality

Canonical information has one owner.

## Canonical Owners

- Physical identity: the narrowest owning physical scope.
- Interfaces: the provider scope that exposes the interface.
- Capabilities: the scope that provides the capability.
- Constraints: the scope or external authority that imposes the constraint.
- Maintenance procedures: `lifecycle/maintenance-schedules/` or the owning
  scope when the procedure is unique to one scope.
- Observed reality: `reality/` records with evidence and verification state.
- Generated artifacts: never canonical.

## Reference Pattern

Use a relative Markdown link to the owning document and include the stable ID
when available.

Example:

```text
See [Electrical Domain](../domains/electrical/README.md), scope `bb:domain:electrical`.
```

## Duplication Rule

Duplicated summaries are allowed only for orientation. Duplicated facts that
could affect construction, cost, safety, maintenance, or generation are not
allowed.

## Conflict Rule

When two documents conflict, the document named as canonical owner wins until a
new decision or verified observation changes the owner.

