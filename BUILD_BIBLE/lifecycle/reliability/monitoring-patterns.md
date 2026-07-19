# Monitoring Patterns

Monitoring patterns define how physical systems publish health and failure
signals.

## Patterns

- direct measurement
- proxy measurement
- threshold alert
- trend alert
- watchdog signal
- manual inspection
- periodic certification
- anomaly observation

## Required Fields

- monitored condition
- sensor or observation method
- location
- access path
- normal range
- degraded range
- failure range
- alert path
- maintenance response
- calibration or verification method

## Rule

Monitoring does not replace service access. A monitored hidden system is still
an anti-pattern if it cannot be inspected, isolated, or repaired.

## Relationships

- Parent reliability: [Reliability](README.md)
- Related utility standard: [Monitoring Utility Standard](../../domains/utilities/standards/monitoring.md)
- Related digital twin: [Digital Twin Reality State](../../digital-twin/reality-state.md)
- Generated artifacts: sensor schedules, alert maps, health dashboards

