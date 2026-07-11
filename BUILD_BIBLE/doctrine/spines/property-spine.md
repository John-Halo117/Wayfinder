# Property Spine Pattern

The property spine is the primary service and access backbone for a site.

## Responsibilities

- Organize utility ingress, site circulation, drainage, water movement,
  communications, monitoring, and future expansion corridors.
- Preserve access for maintenance vehicles, emergency response, and future
  construction.
- Keep primary routes legible enough that future work can extend them without
  rediscovering the site from scratch.

## Required Capabilities

- physical access route
- utility ingress zone
- water movement route
- drainage overflow route
- communications route
- isolation and shutoff locations
- observation points
- reserved expansion corridor

## Optional Capabilities

- site energy generation
- battery or fuel storage
- weather station
- drone landing and charging point
- perimeter monitoring
- agricultural water distribution
- robotic service routes

## Interfaces

The property spine provides interfaces to building spines, roads, drainage,
water, electrical, communications, security, agriculture, and expansion zones.

## Expansion Rules

Future services consume reserved corridors, spare conduits, accessible vaults,
and documented crossing points before trenching new routes.

## Failure Isolation

Each critical service must have an identifiable isolation point before it
branches to buildings or major site zones.

## Maintenance

The spine must support inspection without excavation except where a decision
record explicitly accepts buried inspection risk.

## Relationships

- Parent doctrine: [Fractal Spines](../fractal-spines.md)
- Contract: [Spine Contract](../../contracts/spine-contract.md)
- Schema: [spine.schema.json](../../schemas/spine.schema.json)
- Dependent patterns: [Property Pattern](../../domains/site/property-pattern.md),
  [Universal Expansion Pattern](../../domains/expansion/universal-expansion-pattern.md)
- Generated artifacts: site utility plans, drainage maps, ingress diagrams,
  inspection checklists
- Reality records: property-specific surveys, observations, and utility
  evidence instantiate this pattern.

