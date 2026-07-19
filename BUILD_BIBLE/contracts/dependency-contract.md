# Dependency Contract

Dependencies describe how capabilities rely on other scopes, resources,
interfaces, and conditions.

## Required Fields

- subject scope or capability
- provides
- requires
- consumes
- produces
- depends on
- used by
- criticality
- graceful degradation
- fallbacks
- failure propagation
- verification state

## Criticality Classes

- `life-safety`
- `critical`
- `important`
- `convenience`
- `optional`

## Invariants

- Critical dependencies must publish isolation, fallback, and recovery paths.
- Hidden dependencies are anti-patterns unless accepted by an Engineering
  Decision Record.

## Relationships

- Parent ontology: [Dependency Ontology](../registries/ontologies/dependency-ontology.md)
- Related schema: [dependency.schema.json](../schemas/dependency.schema.json)
- Related review: [Architectural Review Checklist](../governance/reviews/architectural-review-checklist.md)
- Generated artifacts: dependency graphs, cascading-failure reports,
  capability-impact maps

