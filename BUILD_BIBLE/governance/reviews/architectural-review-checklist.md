# Architectural Review Checklist

Every reusable pattern should be evaluated before being used as design input.

## Scope Gate

Before evaluating a habitat/building pattern, identify its assumption scope:

- `SHARED`
- `GH`
- `MH`
- `CAMPUS`
- `UNKNOWN_SCOPE`
- `N/A`

`UNKNOWN_SCOPE` historical material is quarantined and may not silently flow
into a current GH/MH design.

For GH/MH also verify the shared protected constraint: **one human-occupied
story; no dependency on stairs or another occupied floor.**

## Review Areas

- requirement clarity: desired state is distinct from mechanism
- scope/profile correctness: GH rules do not leak into MH and vice versa
- observability
- serviceability
- maintainability
- evolvability
- modularity
- accessibility and long-term physical independence
- isolation
- documentation
- reserve capacity and option value
- optionality
- reliability and safe failure/recovery
- upgrade paths
- standards-first interface resolution
- privacy and acoustics where human occupation is involved
- human burden: setup, retrieval, lifting/holding, conversion, cleanup/reset, and maintenance
- spatial burden: dedicated area, clearance envelope, circulation-only area, and incompatible double claims
- negative/restorative space preservation
- technology dependence, telemetry, repair lock-in, and provider dependence when material

## Habitat-Specific Questions

1. What requirement does this feature actually satisfy?
2. Which profile owns it: GH, MH, Campus, or Shared?
3. Is the feature hard, preferred, optional, or merely conventional?
4. Is a named mechanism being mistaken for the requirement?
5. Does a simpler fixed/passive/manual solution satisfy the requirement with lower lifecycle burden?
6. Does spatial compression transfer cost into recurring human labor, poor access, privacy/acoustics loss, service difficulty, or safety?
7. If a transformation is proposed, will deploy/reset friction cause it to remain deployed or reduce task completion?
8. Does vertical/overhead use keep essential daily capability accessible?
9. Are wall/cavity/clearance claims mutually compatible, or is the same physical resource being counted twice?
10. Is future-proofing limited to cheap durable pathways/interfaces rather than speculative future-maximum equipment?
11. Could a noisy, dirty, bulky, seasonal, or material-handling function live more effectively elsewhere on Campus?
12. For MH, is a hallway/transition/dedicated room being rejected only because a GH compression rule was inherited?
13. For GH, is area being spent on circulation/duplication that does not materially improve a protected requirement?

## Required Review Result

- pass
- pass with accepted tradeoff
- fail pending redesign
- fail pending Engineering Decision Record

## Rule

A pattern that fails serviceability, isolation, documentation, accessibility,
profile scope, or the one-story protected constraint for a critical capability
cannot be treated as ready for implementation without an Engineering Decision
Record where the underlying requirement is still valid.

A rejected/obsolete assumption is not revived merely by writing an EDR; the EDR
must document a current requirement and why the old assumption has become valid
again under changed Reality or explicit intent.

## Relationships

- Habitat scope: [Habitat Assumption Scope](../../../contracts/habitat-assumption-scope-v1.md)
- Related metrics: [Metrics Rubrics](metrics-rubrics.md)
- Related questions: [Constitutional Review Questions](constitutional-review-questions.md)
- Related anti-patterns: [Anti-Pattern Library](anti-pattern-library.md)
- Related reliability: [Reliability](../../lifecycle/reliability/README.md)
- Generated artifacts: review checklists, acceptance packets, design risk
  registers
