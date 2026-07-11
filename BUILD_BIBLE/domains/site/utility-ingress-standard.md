# Utility Ingress Standard

Utility ingress defines how external services enter a property and transition
into owned infrastructure.

## Required Elements

- source or provider
- entry point
- route to first owned control point
- isolation method
- metering or monitoring method
- service access
- crossing conflicts
- reserve route
- failure behavior
- evidence link

## Service Classes

- power
- water
- wastewater
- communications
- fuel
- stormwater discharge
- security or access-control connection

## Standard

Ingress should be centralized where practical, distributed where resilience or
physical reality requires it, and always documented well enough to extend or
replace without excavation by guesswork.

## Relationships

- Parent doctrine: [Serviceability Invariant](../../doctrine/serviceability-invariant.md)
- Related contract: [Interface Contract](../../contracts/interface-contract.md)
- Related schema: [interface.schema.json](../../schemas/interface.schema.json)
- Dependent patterns: [Property Spine](../../doctrine/spines/property-spine.md),
  [Utility Standards](../utilities/standards/README.md)
- Generated artifacts: utility ingress diagrams, shutoff maps, emergency
  isolation guides
- Reality records: provider records, photos, surveys, and inspections
  instantiate this standard.

