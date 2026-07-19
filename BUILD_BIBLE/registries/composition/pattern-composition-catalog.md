# Pattern Composition Catalog

The composition catalog records reusable pattern assemblies. It does not define
property-specific implementations.

## Universal Room Derivatives

```text
Universal Room
  + Accessibility
  + Lighting
  + Monitoring
  + Room Spine
  -> Bedroom
  -> Office
  -> Storage Room
```

## Wet Area Derivatives

```text
Universal Room
  + Wet Area
  + Room Spine
  + Water
  + Drainage
  + Ventilation
  + Monitoring
  + Serviceability
  + Digital Twin Support
  -> Bathroom
  -> Laundry
  -> Mudroom
  -> Greenhouse Work Zone
```

## Kitchen Composition

```text
Universal Room
  + Wet Area
  + Lighting
  + Ventilation
  + Storage
  + Work Surfaces
  + Appliance Spines
  + Monitoring
  + Serviceability
  -> Kitchen
```

## Workshop Composition

```text
Universal Room
  + Workshop Utility Standard
  + Power
  + Lighting
  + Ventilation
  + Storage
  + Equipment Interfaces
  + Monitoring
  + Serviceability
  -> Workshop Bay
```

## Mechanical Room Composition

```text
Universal Room
  + Universal Mechanical Pattern
  + Power
  + Water
  + Drainage
  + HVAC
  + Monitoring
  + Replacement Paths
  + Service Clearances
  -> Mechanical Room
```

## Greenhouse Composition

```text
Building Pattern
  + Wet Area
  + Agriculture
  + Water
  + Drainage
  + Ventilation
  + Monitoring
  + Sunlight
  + Thermal Control
  -> Greenhouse
```

## Barn Composition

```text
Building Pattern
  + Storage
  + Agriculture
  + Equipment Access
  + Ventilation
  + Lighting
  + Water Optionality
  + Serviceability
  -> Barn
```

## Root Cellar Composition

```text
Building Pattern
  + Storage
  + Passive Resilience
  + Ventilation
  + Moisture Management
  + Monitoring
  + Pest Resistance
  -> Root Cellar
```

## Relationships

- Composition model: [Pattern Composition Model](pattern-composition-model.md)
- Capability matrix: [Capability Matrix Template](../../templates/capability-matrix.md)
- Review: [Architectural Review Checklist](../../governance/reviews/architectural-review-checklist.md)
- Validation: [Repository Validation Standard](../../governance/validation/repository-validation-standard.md)

