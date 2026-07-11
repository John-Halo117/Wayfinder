# Monitoring Utility Standard

Monitoring systems preserve reality by sensing physical state over time.

## Required Standard

- identify measured condition
- identify sensor location and service access
- identify calibration or replacement method
- define alert thresholds and uncertainty
- distinguish observation from control
- preserve manual inspection paths

## Monitoring Classes

- water leak
- temperature
- humidity
- air quality
- power
- access
- weather
- soil moisture
- equipment state
- structural movement

## Relationships

- Parent doctrine: [Verification](../../../governance/verification.md)
- Contracts: [Capability Contract](../../../contracts/capability-contract.md),
  [Maintenance Contract](../../../contracts/maintenance-contract.md)
- Schemas: [capability.schema.json](../../../schemas/capability.schema.json),
  [digital-twin-state.schema.json](../../../schemas/digital-twin-state.schema.json)
- Dependent patterns: [Observation Points Standard](../../../reality/observations/observation-points-standard.md),
  [Digital Twin Reality State](../../../digital-twin/reality-state.md)
- Generated artifacts: sensor schedules, alert maps, maintenance calendars
- Reality records: sensor observations instantiate this standard.

