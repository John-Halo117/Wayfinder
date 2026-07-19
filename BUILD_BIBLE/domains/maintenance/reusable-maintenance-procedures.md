# Reusable Maintenance Procedures

Maintenance preserves reality, serviceability, and optionality.

## Inspection Frequencies

Default frequencies are classes, not property-specific schedules:

- critical safety: monthly or by event
- water and drainage: seasonal and after major storms
- HVAC and filtration: monthly to quarterly by equipment class
- electrical visible condition: annual
- roofs, gutters, and exterior water control: seasonal
- roads and access: seasonal and after storms
- sensors and monitoring: quarterly or after alert failure
- materials and finishes: annual or by exposure
- equipment: by runtime, season, or manufacturer interval

## Expected Lifetimes

Each maintained scope should define expected service life as:

- design life
- inspection interval
- likely failure mode
- rebuild or replacement trigger
- part availability risk
- optionality impact at replacement

## Replacement Philosophy

Replacement should improve serviceability, maintain interfaces, preserve
history, and avoid consuming reserved capacity unless a decision record accepts
the tradeoff.

## Service Records

Every service record should link:

- maintained scope
- procedure
- date
- evidence
- parts used
- observations
- follow-up actions
- digital twin update

## Digital Twin Synchronization

Maintenance changes the twin when it changes current condition, capacity,
verification state, service history, or open issues.

## Relationships

- Parent doctrine: [Preserve reality through verification](../../governance/verification.md)
- Contracts: [Maintenance Contract](../../contracts/maintenance-contract.md),
  [Physical Scope Contract](../../contracts/physical-scope-contract.md)
- Schemas: [maintenance-procedure.schema.json](../../schemas/maintenance-procedure.schema.json),
  [digital-twin-state.schema.json](../../schemas/digital-twin-state.schema.json)
- EDRs: [Engineering Decision Record Standard](../../lifecycle/decisions/engineering-decision-record-standard.md)
- Metrics and review: [Metrics Rubrics](../../governance/reviews/metrics-rubrics.md),
  [Architectural Review Checklist](../../governance/reviews/architectural-review-checklist.md)
- Anti-patterns: [Anti-Pattern Library](../../governance/reviews/anti-pattern-library.md)
- Reliability: [Reliability](../../lifecycle/reliability/README.md)
- Verification: [Acceptance And Verification Standard](../../governance/reviews/acceptance-and-verification-standard.md)
- Dependent patterns: [Observation Points Standard](../../reality/observations/observation-points-standard.md),
  [Universal Room Pattern](../spaces/universal-room-pattern.md)
- Generated artifacts: maintenance schedules, inspection checklists, service
  dashboards, replacement forecasts
- Reality records: service records and observations instantiate these
  procedures.
