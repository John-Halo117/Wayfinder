# Anti-Pattern Library

Anti-patterns describe physical design choices the Build Bible rejects by
default.

## Canonical Anti-Patterns

### Service / infrastructure

- buried junction boxes
- hidden shutoffs
- plumbing behind permanent cabinetry without access
- avoidable single points of failure
- proprietary connectors without adapters or standards-first justification
- dead-end conduit
- unlabeled infrastructure
- non-serviceable assemblies
- inaccessible cleanouts
- inaccessible filters
- hidden dependencies
- undocumented bypasses
- routine maintenance that requires destructive wall/ceiling opening when an economical access path is feasible

### Habitat assumption leakage

- applying a GH-only compression rule to MH without re-qualification
- applying an MH-only comfort/space assumption to GH without re-qualification
- treating historical `UNKNOWN_SCOPE` material as a universal default
- treating conventional presence in houses as evidence that a feature is required
- treating a named mechanism as the requirement instead of the desired state

### Current Sanctuary / house constraints

- second-story human circulation as a default or dependency
- stair-dependent GH/MH architecture
- inter-floor laundry/grocery/material transfer as a required house capability
- person or cargo lifts whose design purpose is serving another occupied floor
- maximum square-footage reduction as the objective
- maximum spatial utilization or maximum function count as the objective
- assuming every surface, cavity, or volume must carry a secondary function
- eliminating deliberate negative/restorative space because it appears unused
- turning MH into an oversized tiny house full of constant conversions
- turning GH into a tiny-house puzzle that requires daily furniture Tetris or strength-intensive setup
- making essential daily storage depend on ladders or inaccessible upper volume
- mechanizing, powering, sensing, or automating a capability when a simpler adequate solution has lower lifecycle burden
- installing speculative future-maximum capacity merely because a future pathway/interface exists
- creating custom Polaris physical interfaces where adequate external standards or mature interoperable interfaces exist
- double-counting the same wall cavity, clearance envelope, or spatial volume for incompatible functions
- hiding maintenance/service burden merely to preserve a visually clean surface

## Profile Examples

- **GH:** a conventional hallway is not automatically prohibited, but circulation-only area must earn itself through code, access, privacy, acoustics, geometry, or another protected requirement.
- **MH:** a hallway is not an anti-pattern merely because GH minimizes them; pointless circulation is the anti-pattern.
- **Campus:** noisy, dirty, bulky, seasonal, or material-handling capability should be evaluated for campus placement rather than assumed to belong inside either house.

## Rule

An anti-pattern may be accepted only through an Engineering Decision Record
that documents the requirement, profile/scope, reason, tradeoff, mitigation,
and reevaluation trigger.

Historical anti-pattern material remains evidence/provenance. It does not become
current design state merely because it appears in an older conversation or
pattern.

## Relationships

- Habitat scope: [Habitat Assumption Scope](../../../contracts/habitat-assumption-scope-v1.md)
- Related doctrine: [Serviceability Invariant](../../doctrine/serviceability-invariant.md)
- Related review: [Architectural Review Checklist](architectural-review-checklist.md)
- Related lifecycle: [Engineering Decision Record Standard](../../lifecycle/decisions/engineering-decision-record-standard.md)
- Generated artifacts: design review warnings, inspection checklists,
  commissioning blockers
