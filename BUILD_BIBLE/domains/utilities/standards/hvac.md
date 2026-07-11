# HVAC Utility Standard

HVAC systems provide thermal comfort, ventilation, humidity control, filtration,
and exhaust through serviceable zones.

## Required Standard

- identify heating, cooling, ventilation, filtration, exhaust, controls, and
  condensate paths
- publish zones and dependencies
- preserve filter, coil, drain, fan, damper, and equipment access
- document replacement path for major equipment
- monitor critical indoor environmental conditions where practical

## Expansion Rule

HVAC routes should preserve capacity for future filtration, heat recovery,
zoning, sensors, electrification, and thermal storage.

## Relationships

- Parent doctrine: [Serviceability Invariant](../../../doctrine/serviceability-invariant.md)
- Contracts: [Capability Contract](../../../contracts/capability-contract.md),
  [Maintenance Contract](../../../contracts/maintenance-contract.md)
- Schemas: [capability.schema.json](../../../schemas/capability.schema.json),
  [maintenance-procedure.schema.json](../../../schemas/maintenance-procedure.schema.json)
- Dependent patterns: [HVAC Domain](../../hvac/README.md),
  [Universal Mechanical Pattern](../../spaces/universal-mechanical-pattern.md)
- Generated artifacts: duct diagrams, zone maps, filter schedules, equipment
  replacement plans
- Reality records: commissioning tests and maintenance records instantiate this
  standard.

