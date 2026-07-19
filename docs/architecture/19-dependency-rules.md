# 19 Dependency Rules

Canonical dependency direction:

```text
Reality
-> Perception
-> Observations
-> ARK
-> Representations
-> Focus
-> Understanding
-> Missions
-> Bearings
-> Reasoning
-> Navigation
-> Experiences
-> Actions
```

## Rules

- Upstream layers must not depend on downstream layers.
- Actions modify reality and must be re-observed.
- Views and experiences are presentation-only.
- Knowledge and representations are derived and rebuildable.
- Engines must not own shared infrastructure.
- Services must not depend on engines.
- External integrations must remain replaceable.

## Current Violation Summary

Active Python scan found:

- service-to-engine violations: 0
- contract-to-implementation violations: 0
- generated graph cycles: 0

Known shortcuts remain visible in legacy and are tracked as debt.

## Enforcement Plan

1. Implement `tooling/linter/spec.md`.
2. Check filesystem ownership.
3. Parse Python imports.
4. Scan docs for ownership claims.
5. Flag legacy and generated exceptions separately.
6. Fail only high-confidence active violations at first.

