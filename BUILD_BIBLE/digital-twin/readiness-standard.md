# Digital Twin Readiness Standard

Digital twin readiness describes whether canonical source contains enough
structured information to generate and maintain a digital representation.

## Readiness Requirements

- stable identity
- spatial identity
- parent and child relationships
- capabilities
- constraints
- interfaces
- dependencies
- resource flows
- reserve capacity
- operational states
- verification state
- maintenance obligations
- reliability records
- generated artifact targets
- last verified reality

## Generation Targets

- spatial models
- CAD
- BIM
- bills of materials
- wiring diagrams
- plumbing diagrams
- maintenance plans
- inspection plans
- sensor inventories
- capability maps

## Readiness States

- `not-ready`: required identity or source relationships are missing.
- `partial`: enough information exists for limited representation.
- `ready`: core source data is complete for generation.
- `verified`: generated representation is checked against reality records.

## Rule

Digital twin readiness does not mean physical truth is verified. It means the
source is structured enough to represent and validate.

## Relationships

- Universal scope: [Universal Scope Contract](../contracts/universal-scope-contract.md)
- Digital twin state: [Digital Twin Reality State](reality-state.md)
- Validation: [Repository Validation Standard](../governance/validation/repository-validation-standard.md)
- Reports: [Coverage Report Templates](../governance/reports/coverage-report-templates.md)

