# Resource Flow Ontology

The Build Bible treats every physical resource as a flow through scopes,
interfaces, storage, transformation, consumption, recovery, loss, and egress.

## Canonical Resource Types

- water
- waste
- greywater
- stormwater
- air
- heat
- electricity
- fuel
- communications
- sunlight
- food
- materials
- people
- animals
- vehicles

## Flow Stages

- ingress
- storage
- distribution
- transformation
- consumption
- recovery
- losses
- egress
- monitoring
- constraints

## Rule

A domain may specialize a resource flow, but it should not invent a parallel
flow model. Use this ontology and add domain-specific constraints through
contracts, patterns, and scope records.

## Relationships

- Contract: [Resource Flow Contract](../../contracts/resource-flow-contract.md)
- Schema: [resource-flow.schema.json](../../schemas/resource-flow.schema.json)
- Related ontology: [Dependency Ontology](dependency-ontology.md)
- Generated artifacts: resource-flow diagrams, water maps, energy maps,
  material movement maps, capacity reports

