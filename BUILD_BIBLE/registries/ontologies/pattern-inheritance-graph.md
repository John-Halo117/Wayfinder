# Pattern Inheritance Graph

The pattern inheritance graph documents conceptual inheritance between reusable
patterns. It does not define implementation inheritance or file-system layout.

## Scope Line

```text
Universal Scope
  -> Physical Scope
    -> Property
    -> Building
      -> Space
        -> Room
          -> Wet Area
          -> Mechanical Area
        -> Cabinet
    -> Equipment
      -> Appliance
      -> Tool
      -> Vehicle
```

## Infrastructure Line

```text
Universal Scope
  -> Physical Scope
    -> Infrastructure
      -> Utility
        -> Water
          -> Rainwater
          -> Greywater
          -> Wastewater
        -> Energy
        -> Communications
        -> HVAC
        -> Monitoring
```

## Land Line

```text
Universal Scope
  -> Physical Scope
    -> Land
      -> Water Movement
      -> Agriculture
        -> Orchard
        -> Food Forest
        -> Greenhouse
      -> Roads And Access
```

## Rule

A pattern inherits questions, not implementation. Child patterns may specialize
capabilities and constraints but must preserve the parent contract.

## Relationships

- Root contract: [Universal Scope Contract](../../contracts/universal-scope-contract.md)
- Child contract: [Physical Scope Contract](../../contracts/physical-scope-contract.md)
- Related review: [Architectural Review Checklist](../../governance/reviews/architectural-review-checklist.md)
- Generated artifacts: pattern maps, documentation navigation, traceability
  reports

