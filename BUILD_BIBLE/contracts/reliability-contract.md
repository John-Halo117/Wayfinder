# Reliability Contract

Reliability describes whether a physical capability can continue to provide
intended service over time, stress, degradation, maintenance, and failure.

## Required Fields

- scope or capability ID
- intended function
- operational states
- known failure modes
- degradation model
- inspection standard
- verification standard
- monitoring pattern
- recovery procedure
- resilience pattern
- maintenance obligations
- fallback behavior
- service history links

## Invariants

- Failure is one part of reliability, not the whole model.
- Degradation must be modeled separately from sudden failure.
- Reliable systems publish detection, isolation, repair, recovery, and
  verification paths.

## Relationships

- Reliability architecture: [Reliability](../lifecycle/reliability/README.md)
- Related schema: [reliability-record.schema.json](../schemas/reliability-record.schema.json)
- Related templates: [Reliability Record Template](../templates/reliability-record.md),
  [Degradation Model Template](../templates/degradation-model.md)
- Generated artifacts: reliability reviews, maintenance forecasts,
  monitoring schedules, recovery checklists

