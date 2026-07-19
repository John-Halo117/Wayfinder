# Property Lifecycle

Every physical asset follows a lifecycle. The lifecycle describes long-term
position, not current operating mode.

## Phases

- `acquire`
- `observe`
- `plan`
- `prepare`
- `build`
- `commission`
- `operate`
- `maintain`
- `expand`
- `renew`
- `retire`

## Rule

Lifecycle phase is separate from operational state. A pump may be in the
`operate` lifecycle phase while its operational state is `maintenance` or
`fault`.

## Phase Expectations

- acquire: preserve evidence, constraints, and known unknowns.
- observe: record reality before changing it.
- plan: decide intent and interfaces.
- prepare: protect access, staging, utilities, and safety.
- build: implement physical change.
- commission: verify acceptance criteria.
- operate: use the capability within documented constraints.
- maintain: preserve serviceability and update history.
- expand: add capability through reserved interfaces first.
- renew: restore or improve capability at end of service life.
- retire: remove active service while preserving history.

## Relationships

- Related state model: [Operational State Model](../registries/ontologies/operational-state-model.md)
- Related contract: [Operational State Contract](../contracts/operational-state-contract.md)
- Related review: [Acceptance And Verification Standard](../governance/reviews/acceptance-and-verification-standard.md)
- Generated artifacts: lifecycle dashboards, phase checklists, commissioning
  checklists, retirement records

