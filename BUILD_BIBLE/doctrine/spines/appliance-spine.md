# Appliance Spine Pattern

The appliance spine is the replaceable interface set for a maintainable
appliance or machine.

## Responsibilities

- Define how the appliance receives services, exhausts outputs, can be isolated,
  can be removed, and can be replaced.
- Preserve compatibility with future replacements.
- Prevent hidden dependencies from binding the appliance to a single model.

## Required Capabilities

- power or fuel interface when applicable
- water interface when applicable
- drainage interface when applicable
- ventilation or exhaust interface when applicable
- data or control interface when applicable
- isolation method
- removal path
- service clearance
- documentation link

## Optional Capabilities

- leak detection
- vibration monitoring
- energy monitoring
- condensate monitoring
- automatic shutoff
- spare conduit or cable path

## Interfaces

The appliance spine consumes room, cabinet, building, or equipment interfaces
and publishes service, monitoring, and replacement requirements.

## Expansion Rules

Appliance bays should preserve dimensional slack, accessible shutoffs, flexible
terminations where appropriate, and spare service capacity.

## Failure Isolation

An appliance failure should be isolatable without disabling unrelated room or
building capabilities except where safety requires broader shutdown.

## Maintenance

Routine service points, filters, cleanouts, drains, panels, and fasteners must
remain accessible after installation.

## Relationships

- Parent doctrine: [Fractal Spines](../fractal-spines.md)
- Contract: [Interface Contract](../../contracts/interface-contract.md)
- Schema: [interface.schema.json](../../schemas/interface.schema.json)
- Dependent patterns: [Equipment Domain](../../domains/equipment/README.md),
  [Universal Mechanical Pattern](../../domains/spaces/universal-mechanical-pattern.md)
- Generated artifacts: appliance cut sheets, replacement checklists, equipment
  maintenance schedules
- Reality records: equipment service records and label evidence instantiate
  this pattern.

