# Architectural Classification

Every new concept must be classified before implementation.

Existing source code must also be classified before migration. Source code is
evidence, and evidence must be observed before it is interpreted.

Ask, in order:

1. Is this a constitutional principle?
2. Is this shared language, meaning a contract?
3. Is this a capability?
4. Is this reusable infrastructure, meaning a service?
5. Is this a unique responsibility, meaning an engine?
6. Is this a domain composition?
7. Is this an internal application?
8. Is this an external integration?
9. Is this an operational concern?
10. Is this developer tooling?

Only after classification should implementation begin.

## Placement Rules

- Constitutional principle: `constitution/`
- Shared language: `contracts/`
- Stable verb: `capabilities/`
- Reusable infrastructure: `services/`
- Unique responsibility: `engines/`
- Real-world orchestration: `domains/`
- Wayfinder-owned application: `internal/`
- Third-party integration: `external/`
- Runtime infrastructure: `operations/`
- Developer tooling: `tooling/`
