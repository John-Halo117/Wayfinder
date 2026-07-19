# Architectural Review Checklist

Every reusable pattern should be evaluated before being used as design input.

## Review Areas

- observability
- serviceability
- maintainability
- evolvability
- modularity
- accessibility
- isolation
- documentation
- reserve capacity
- optionality
- reliability
- upgrade paths

## Required Review Result

- pass
- pass with accepted tradeoff
- fail pending redesign
- fail pending Engineering Decision Record

## Rule

A pattern that fails serviceability, isolation, or documentation for a critical
capability cannot be treated as ready for implementation without an Engineering
Decision Record.

## Relationships

- Related metrics: [Metrics Rubrics](metrics-rubrics.md)
- Related questions: [Constitutional Review Questions](constitutional-review-questions.md)
- Related anti-patterns: [Anti-Pattern Library](anti-pattern-library.md)
- Related reliability: [Reliability](../../lifecycle/reliability/README.md)
- Generated artifacts: review checklists, acceptance packets, design risk
  registers

