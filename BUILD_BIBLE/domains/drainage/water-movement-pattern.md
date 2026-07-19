# Water Movement Pattern

Water movement is a primary physical system across land, buildings, roads, and
agriculture.

## Responsibilities

- identify normal flow
- preserve overflow paths
- prevent destructive ponding
- reduce erosion
- protect foundations and roads
- support storage, infiltration, and reuse when appropriate
- expose inspection and maintenance points

## Required Capabilities

- source identification
- route description
- capacity estimate or unknown state
- overflow behavior
- inspection point
- cleanout or service method when constructed
- receiving area
- downstream consequence

## Design Rules

Buildings, roads, and utility corridors must not interrupt known water movement
without a replacement route. Hidden drainage paths must publish access and
cleanout points.

## Relationships

- Parent doctrine: [Serviceability Invariant](../../doctrine/serviceability-invariant.md),
  [Reserve Capacity](../../doctrine/reserve-capacity.md)
- Related contracts: [Capacity Contract](../../contracts/capacity-contract.md),
  [Interface Contract](../../contracts/interface-contract.md)
- Related schemas: [interface.schema.json](../../schemas/interface.schema.json),
  [physical-scope.schema.json](../../schemas/physical-scope.schema.json)
- Dependent patterns: [Property Pattern](../site/property-pattern.md),
  [Rainwater Standard](../utilities/standards/rainwater.md)
- Generated artifacts: drainage diagrams, grading plans, inspection checklists
- Reality records: storm observations, surveys, and inspection photos
  instantiate this pattern.

