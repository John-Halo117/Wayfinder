# Equipment Shelter Pattern

The equipment shelter protects maintainable assets while preserving service and
replacement access.

## Required Capabilities

- weather protection
- ventilation appropriate to stored equipment
- safe access
- load-bearing storage or parking surface
- fire and spill constraints
- service clearance
- removal path

## Optional Capabilities

- charging
- fuel storage interface
- battery storage
- compressed air
- washdown
- tool storage
- remote monitoring

## Constraints

Stored equipment must not block isolation points, inspection points, drainage,
or emergency access.

## Serviceability

The shelter should allow routine service, battery access, tire access, fluid
checks, and removal without moving unrelated assets when practical.

## Expansion

Reserve power, data, ventilation, structural mounting, and drainage capacity
for future equipment classes.

## Relationships

- Parent doctrine: [Reserve Capacity](../../../doctrine/reserve-capacity.md)
- Contracts: [Physical Scope Contract](../../../contracts/physical-scope-contract.md),
  [Maintenance Contract](../../../contracts/maintenance-contract.md)
- Schemas: [physical-scope.schema.json](../../../schemas/physical-scope.schema.json),
  [maintenance-procedure.schema.json](../../../schemas/maintenance-procedure.schema.json)
- Dependent patterns: [Equipment Domain](../../equipment/README.md),
  [Universal Expansion Pattern](../../expansion/universal-expansion-pattern.md)
- Generated artifacts: storage layouts, service checklists, equipment
  replacement plans
- Reality records: equipment inventory and service records instantiate this
  pattern.

