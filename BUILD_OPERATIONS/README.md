# Build Operations

Build Operations is the property-specific physical operations manual layer.

It describes how a specific property is operated. It does not own canonical
design intent, reusable patterns, physical doctrine, generated artifacts, or
maintenance history.

## Layer Separation

```text
BUILD_BIBLE/
  how physical systems should be specified

BUILD_OPERATIONS/
  how a specific property is operated

BUILD_BIBLE/lifecycle/service-records/
  what actually happened during maintenance or repair
```

## Owns

- property-specific operating procedures
- operating modes
- seasonal routines
- emergency actions
- active checklists
- operator handoff notes

## Does Not Own

- Build Bible doctrine
- reusable patterns
- physical specifications
- generated CAD, BIM, diagrams, or configs
- service history
- evidence records
- Wayfinder runtime operations

## Contents

- [Manuals](manuals/README.md)
- [SOPs](sops/README.md)
- [Operating Modes](operating-modes/README.md)
- [Seasonal Routines](seasonal-routines/README.md)
- [Emergency Actions](emergency-actions/README.md)
- [Checklists](checklists/README.md)
- [Templates](templates/README.md)

## Reference Rule

Operations documents reference canonical Build Bible source records. They do
not duplicate design intent, capacity, interfaces, or maintenance history.

## Lifecycle

Operations manuals change when physical systems, operating practices,
emergency procedures, seasonal routines, or verified reality change.

