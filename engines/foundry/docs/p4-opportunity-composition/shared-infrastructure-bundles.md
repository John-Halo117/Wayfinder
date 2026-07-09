# Shared Infrastructure Bundles

## P4-BND-001 Shared Infrastructure Ownership

| Aspect | Composition |
| --- | --- |
| Shared capabilities | Eventing/replay, storage, policy, search/index. |
| Shared dependencies | Contracts, services, active engines, legacy surfaces. |
| Shared ownership question | Which shared concern belongs in service, engine, view, tooling, or generated artifact ownership. |
| Shared testing surface | Contract purity, service boundaries, active engine consumers, legacy compatibility. |
| Shared documentation | Ownership matrix, interface catalog, cross-cutting audit. |

## Infrastructure Composition Preference

```text
Shared capability
-> Platform
-> Kernel
-> Implementation
```

P4-BND-001 naturally produces reusable infrastructure observations, but P4 does
not decide extraction or implementation.
