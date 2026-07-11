# Barn Pattern

The barn is a flexible agricultural, storage, livestock, and equipment support
structure.

## Required Capabilities

- weather protection
- large-item access
- durable floor or ground strategy
- storage zones
- ventilation
- pest management
- lighting or explicit no-lighting state
- service access

## Optional Capabilities

- livestock stalls
- hay storage
- equipment bay
- wash bay
- feed room
- tack room
- solar roof interface
- rainwater collection

## Constraints

Barns must handle dust, moisture, pests, impact, large doors, and changing
agricultural use without hiding critical service routes.

## Serviceability

Doors, roof drainage, structural connections, lighting, water points, and
animal-facing assemblies should be inspectable and repairable.

## Expansion

Reserve structural, electrical, water, drainage, and circulation interfaces for
future agricultural uses.

## Relationships

- Parent doctrine: [Optionality](../../../doctrine/optionality.md)
- Contracts: [Physical Scope Contract](../../../contracts/physical-scope-contract.md),
  [Capacity Contract](../../../contracts/capacity-contract.md)
- Schemas: [physical-scope.schema.json](../../../schemas/physical-scope.schema.json)
- Dependent patterns: [Livestock Domain](../../livestock/README.md),
  [Storage Domain](../../storage/README.md)
- Generated artifacts: bay plans, storage maps, maintenance checklists
- Reality records: barn surveys and service records instantiate this pattern.

