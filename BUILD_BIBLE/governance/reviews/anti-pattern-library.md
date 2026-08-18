# Anti-Pattern Library

Anti-patterns describe physical design choices the Build Bible rejects by default.

## Canonical Sanctuary negative specification

The detailed current Sanctuary anti-pattern/failure-mode owner is:

- [Sanctuary Anti-Pattern & Failure-Mode Canon](sanctuary-anti-pattern-failure-mode-canon.md)

Its governing laws are:

> A local optimization is invalid when its displaced burden exceeds its recovered value.

> Capability that is technically present but too annoying, fragile, inaccessible, unsafe, illegible, or confusing to use is not real capability.

Every candidate Sanctuary feature is reviewed by both its positive requirement/capability compiler and this inverse compiler. The inverse compiler can dispose a candidate as `BUILD`, `DEFER`, `RESERVE/PROBE`, or `PRUNE`.

## Universal infrastructure anti-patterns

The following remain cross-domain defaults beyond Sanctuary-specific design:

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
- routine maintenance that requires destructive opening when an economical access path is feasible

## Habitat scope leakage

Reject by default:

- applying a GH-only compression rule to MH without re-qualification
- applying an MH-only comfort/space assumption to GH without re-qualification
- treating historical `UNKNOWN_SCOPE` material as a universal default
- treating conventional presence in houses as evidence that a feature is required
- treating a named mechanism as the requirement instead of the desired state
- second-story/stair/inter-floor GH/MH assumptions that conflict with the current one-occupied-story constraint

## Acceptance exception

An anti-pattern may be accepted only through an Engineering Decision Record that identifies the actual requirement, profile/scope, whole-system tradeoff, mitigation, evidence, and reevaluation/deletion trigger.

Historical anti-pattern material remains evidence/provenance. It does not become current design state merely because it appears in an older conversation or pattern.

## Relationships

- Habitat scope: [Habitat Assumption Scope](../../../contracts/habitat-assumption-scope-v1.md)
- Detailed negative specification: [Sanctuary Anti-Pattern & Failure-Mode Canon](sanctuary-anti-pattern-failure-mode-canon.md)
- Related doctrine: [Serviceability Invariant](../../doctrine/serviceability-invariant.md)
- Related review: [Architectural Review Checklist](architectural-review-checklist.md)
- Related lifecycle: [Engineering Decision Record Standard](../../lifecycle/decisions/engineering-decision-record-standard.md)
- Generated artifacts: design review warnings, inspection checklists, commissioning blockers
