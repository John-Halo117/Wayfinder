# Operational State Contract

Operational states describe what an active physical system is currently doing.

Operational state is distinct from lifecycle phase. A system may be in the
`operate` lifecycle phase while its operational state is `normal`,
`maintenance`, `fault`, or `offline`.

## Canonical States

- `planned`
- `installed`
- `commissioning`
- `normal`
- `idle`
- `active`
- `maintenance`
- `testing`
- `fault`
- `emergency`
- `offline`
- `retired`

## Required Fields

- state name
- entry condition
- exit condition
- allowed actions
- prohibited actions
- monitoring expectations
- failure escalation
- documentation requirement

## Relationships

- State model: [Operational State Model](../registries/ontologies/operational-state-model.md)
- Related schema: [operational-state.schema.json](../schemas/operational-state.schema.json)
- Related operations boundary: [BUILD_OPERATIONS](../../BUILD_OPERATIONS/README.md)
- Generated artifacts: operating mode guides, alarm response guides,
  maintenance checklists

