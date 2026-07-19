# Degradation Models

Degradation is the gradual loss of condition, performance, or remaining service
life before failure.

## Model Classes

- batteries
- bearings
- filters
- roof systems
- sealants
- paint
- concrete
- wood
- metals
- coatings
- plumbing components
- HVAC equipment

## Required Fields

- degradation model ID
- affected material, equipment, or capability class
- wear mechanisms
- environmental influences
- inspection intervals
- expected service life
- maintenance thresholds
- replacement thresholds
- failure thresholds
- monitoring options
- uncertainty

## Predictive Maintenance Rule

When degradation can be observed before failure, maintenance should be
scheduled by condition, runtime, or exposure rather than by surprise.

## Relationships

- Parent reliability: [Reliability](README.md)
- Contract: [Reliability Contract](../../contracts/reliability-contract.md)
- Template: [Degradation Model Template](../../templates/degradation-model.md)
- Generated artifacts: replacement forecasts, inspection calendars,
  condition-based maintenance plans

