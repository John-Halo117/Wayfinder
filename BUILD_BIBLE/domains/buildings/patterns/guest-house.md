# Guest House Pattern

The guest house is an independent or semi-independent residential module.

## Required Capabilities

- safe sleeping and sanitation support
- independent identity and digital twin address
- clear utility interfaces to the property or main building spine
- isolation points for power, water, waste, HVAC, communications, and security
  where present
- service access that does not require entering unrelated private spaces

## Constraints

The guest house should avoid hidden dependency on the main house except where
explicitly modeled as an interface.

## Serviceability

Service points should be reachable from exterior, mechanical, or shared service
zones when practical.

## Expansion

Guest house utility interfaces should support future conversion among guest
use, office, caregiver suite, rental, studio, or emergency housing when allowed
by site constraints.

## Relationships

- Parent doctrine: [Optionality](../../../doctrine/optionality.md)
- Contracts: [Physical Scope Contract](../../../contracts/physical-scope-contract.md),
  [Interface Contract](../../../contracts/interface-contract.md)
- Schemas: [physical-scope.schema.json](../../../schemas/physical-scope.schema.json),
  [interface.schema.json](../../../schemas/interface.schema.json)
- Dependent patterns: [Building Spine](../../../doctrine/spines/building-spine.md),
  [Utility Ingress Standard](../../site/utility-ingress-standard.md)
- Generated artifacts: detached utility plans, isolation maps, maintenance
  checklists
- Reality records: a specific guest house record instantiates this pattern.

