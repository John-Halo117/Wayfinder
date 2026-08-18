# Architectural Review Checklist

Every reusable physical pattern should be evaluated before being used as design input.

## Scope Gate

Before evaluating a habitat/building pattern, identify its assumption scope:

- `SHARED`
- `GH`
- `MH`
- `CAMPUS`
- `UNKNOWN_SCOPE`
- `N/A`

`UNKNOWN_SCOPE` historical material is quarantined and may not silently flow into a current GH/MH design.

For GH/MH also verify the shared protected constraint: **one human-occupied story; no dependency on stairs or another occupied floor.**

## Positive review areas

- requirement clarity: desired state is distinct from mechanism
- scope/profile correctness: GH rules do not leak into MH and vice versa
- observability
- serviceability
- maintainability
- evolvability
- modularity only where justified
- accessibility and long-term physical independence
- isolation
- documentation
- reserve capacity and option value
- reliability and safe failure/recovery
- upgrade paths
- standards-first interface resolution
- privacy and acoustics where human occupation is involved
- human burden: setup, retrieval, lifting/holding, conversion, cleanup/reset, and maintenance
- spatial burden: dedicated area, clearance envelope, circulation-only area, and incompatible double claims
- negative/restorative space preservation
- technology dependence, telemetry, repair lock-in, and provider dependence when material

## Mandatory inverse review

Every Sanctuary candidate must also pass the [Sanctuary Anti-Pattern & Failure-Mode Canon](sanctuary-anti-pattern-failure-mode-canon.md).

The inverse review must explicitly ask:

1. What state are we trying to create?
2. Is this a real requirement or a promoted mechanism?
3. What existing capability already does it?
4. What permanent obligation does it add?
5. What failure modes does it introduce?
6. Where does displaced burden move?
7. What deploy/reset/maintenance/cleaning burden appears?
8. What happens when power/network/motor/controller/vendor fails?
9. Can it be inspected, cleaned, repaired, isolated, and replaced?
10. Does it harm calm, accessibility, security, water, fire, acoustics, privacy, or serviceability?
11. Is there a simpler static/manual solution?
12. Is there a boring industry-standard solution?
13. Does the claimed saving survive parent/whole-house recompilation?
14. Would it still be chosen after novelty wears off?

## Habitat-specific discriminators

- GH may spend less area on circulation/duplication, but cannot trade away accessibility, sleep, privacy, calm, or ordinary usability.
- MH may deliberately spend area on hallways, dedicated rooms, transitions, views, acoustics, and spaciousness where those reduce lifelong friction.
- Campus should absorb noisy, dirty, bulky, seasonal, fabrication, animal, storage, or heavy-material-handling capability when that dominates forcing it into either house.
- Vertical/overhead use never makes frequently needed capability inaccessible by default.
- Wall/cavity/clearance resources cannot be double-booked across incompatible states.
- Future-proofing preserves cheap geometry/routes/interfaces before speculative hardware.
- Mechanization follows passive/manual/assisted/powered complexity only as burden justifies.

## Required disposition

For Sanctuary candidates, use one of:

- **BUILD** — survives positive and inverse review.
- **DEFER** — useful but not sufficiently justified.
- **RESERVE / PROBE** — material uncertainty remains and cheap reversible option preservation/probing is worthwhile.
- **PRUNE** — rejected, dominated, or fails whole-system recompilation.

General pattern review may still use pass / pass-with-tradeoff / fail-pending-redesign / fail-pending-EDR, but any Sanctuary acceptance must map to one of the four dispositions above.

## Rule

A pattern that fails serviceability, isolation, documentation, accessibility, profile scope, the one-story protected constraint, or a protected inverse-compiler gate cannot be treated as ready for implementation merely because it performs its local function.

A rejected/obsolete assumption is not revived merely by writing an EDR. The EDR must document a current requirement, whole-system tradeoff, evidence, mitigation, and reevaluation/deletion trigger.

## Relationships

- Habitat scope: [Habitat Assumption Scope](../../../contracts/habitat-assumption-scope-v1.md)
- Negative specification: [Sanctuary Anti-Pattern & Failure-Mode Canon](sanctuary-anti-pattern-failure-mode-canon.md)
- Related metrics: [Metrics Rubrics](metrics-rubrics.md)
- Related questions: [Constitutional Review Questions](constitutional-review-questions.md)
- Related anti-patterns: [Anti-Pattern Library](anti-pattern-library.md)
- Related reliability: [Reliability](../../lifecycle/reliability/README.md)
- Generated artifacts: review checklists, acceptance packets, design risk registers
