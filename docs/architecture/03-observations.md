# 03 Observations

Observations are source-shaped records emitted before interpretation. They are
the contract boundary between perception and ARK.

## Owns

- Observation-shaped contract language.
- Required provenance fields.
- Source references, timestamps, roles, artifact references, parsing status,
  confidence, and raw content pointers.

## Does Not Own

- Preservation.
- LVR updates.
- Durable relationship topology.
- Knowledge or views.

## Canonical Owner

- `contracts/observations/`
- `canon/ontology.md`
- ADR-0001

## Current Health

First Contact validated the observation boundary at real export scale. The
current Knowledge manifest records:

- Source files: 525
- Conversations: 1,656
- Messages inspected: 108,688
- Generated facts: 27,935

## Missing Pieces

- Observation contract enforcement should eventually be linted.
- Multiple Oracles need shared import profile vocabulary.

