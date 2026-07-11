# Universal Scope Contract

The Universal Scope Contract is the root abstraction for every physical entity
represented by the Build Bible.

## Applies To

- property
- building
- structure
- room
- wall
- floor
- ceiling
- cabinet
- utility
- appliance
- tool
- vehicle
- tree
- pond
- orchard
- equipment
- infrastructure

## Required Fields

- identity
- purpose
- parent
- children
- spatial identity
- capabilities
- constraints
- interfaces
- dependencies
- resources
- reserve capacity
- health
- reliability
- maintenance
- evolution
- lifecycle
- verification
- documentation
- digital twin metadata
- history

## Inheritance Rule

Future scope-specific templates inherit these fields instead of redefining
common concepts. Narrower contracts may add detail, but they must not conflict
with this contract.

## Boundary Rule

The contract defines the information surface of a scope. It does not prescribe
the physical implementation of that scope.

## Relationships

- Parent doctrine: [Fractal Spines](../doctrine/fractal-spines.md),
  [Platform, Not Product](../doctrine/platform-not-product.md)
- Child contract: [Physical Scope Contract](physical-scope-contract.md)
- Related schemas: [universal-scope.schema.json](../schemas/universal-scope.schema.json),
  [physical-scope.schema.json](../schemas/physical-scope.schema.json)
- Related ontologies: [Resource Flow Ontology](../registries/ontologies/resource-flow-ontology.md),
  [Dependency Ontology](../registries/ontologies/dependency-ontology.md)
- Review standard: [Constitutional Review Questions](../governance/reviews/constitutional-review-questions.md)
- Generated artifacts: scope manifests, digital twin records, review reports,
  dependency maps, reliability maps
- Reality records: observations, inspections, service records, and evidence
  instantiate this contract.

