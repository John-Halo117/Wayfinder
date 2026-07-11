# Waste Utility Standard

Waste systems remove or process wastewater, solids, compost, recycling, and
hazardous materials without hidden failure paths.

## Required Standard

- identify waste class
- identify route, storage, treatment, cleanout, and removal interface
- preserve access to cleanouts and inspection points
- document odor, pest, contamination, and overflow behavior
- separate incompatible waste streams

## Failure Isolation

Waste failures must publish where backup, overflow, contamination, or blocked
access will occur.

## Relationships

- Parent doctrine: [Serviceability Invariant](../../../doctrine/serviceability-invariant.md)
- Contracts: [Interface Contract](../../../contracts/interface-contract.md),
  [Maintenance Contract](../../../contracts/maintenance-contract.md)
- Schemas: [interface.schema.json](../../../schemas/interface.schema.json),
  [maintenance-procedure.schema.json](../../../schemas/maintenance-procedure.schema.json)
- Dependent patterns: [Waste Domain](../../waste/README.md),
  [Universal Wet Area Pattern](../../spaces/universal-wet-area-pattern.md)
- Generated artifacts: waste-route diagrams, cleanout maps, inspection
  checklists
- Reality records: cleanout observations and service records instantiate this
  standard.

