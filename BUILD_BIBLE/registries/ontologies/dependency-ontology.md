# Dependency Ontology

The dependency ontology describes how capabilities affect one another.

## Relationship Fields

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

## Criticality

- `life-safety`: failure threatens human safety.
- `critical`: failure compromises shelter, sanitation, water, energy, access,
  security, or major asset protection.
- `important`: failure reduces important capability but does not immediately
  compromise critical continuity.
- `convenience`: failure reduces comfort or convenience.
- `optional`: failure affects optional capability.

## Cascading Failure Rule

Critical capabilities must publish what fails downstream when they degrade or
fail.

## Relationships

- Contract: [Dependency Contract](../../contracts/dependency-contract.md)
- Schema: [dependency.schema.json](../../schemas/dependency.schema.json)
- Related reliability: [Failure Ontology](../../lifecycle/reliability/failure-ontology.md)
- Generated artifacts: dependency graphs, impact reports, fallback maps,
  resilience reviews

