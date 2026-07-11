# Resource Flow Contract

Resource flows describe how a physical resource moves through a scope.

## Required Fields

- resource type
- provider or source
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
- dependencies
- failure behavior
- verification state

## Invariants

- Every resource flow must identify what enters, what leaves, what changes,
  what is stored, and what can be lost.
- Unknown flow capacity must be recorded explicitly.
- A resource flow may be designed, observed, inferred, installed, retired, or
  unverified.

## Relationships

- Parent ontology: [Resource Flow Ontology](../registries/ontologies/resource-flow-ontology.md)
- Related contract: [Interface Contract](interface-contract.md)
- Related schema: [resource-flow.schema.json](../schemas/resource-flow.schema.json)
- Generated artifacts: Sankey diagrams, utility maps, capacity reports,
  failure-impact maps

