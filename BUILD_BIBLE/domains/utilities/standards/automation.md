# Automation Utility Standard

Automation controls physical systems through explicit, reversible interfaces.

## Required Standard

- identify controlled physical capability
- identify manual fallback
- identify sensing dependency
- identify actuator interface
- identify failure state
- identify service and replacement path
- separate physical intent from software implementation

## Rule

Automation may consume Build Bible physical intent, but software configuration
is generated output unless a physical interface or device identity is being
specified.

## Expansion Rule

Automation should consume reserved power, data, sensor, and actuator interfaces
before requiring reconstruction.

## Relationships

- Parent doctrine: [Platform, Not Product](../../../doctrine/platform-not-product.md)
- Contracts: [Interface Contract](../../../contracts/interface-contract.md),
  [Capability Contract](../../../contracts/capability-contract.md)
- Schemas: [interface.schema.json](../../../schemas/interface.schema.json),
  [generated-artifact-manifest.schema.json](../../../schemas/generated-artifact-manifest.schema.json)
- Dependent patterns: [Monitoring Standard](monitoring.md),
  [Low-Voltage Domain](../../low-voltage/README.md)
- Generated artifacts: Home Assistant configs, ESPHome configs, control maps,
  device manifests
- Reality records: physical device observations instantiate this standard.

