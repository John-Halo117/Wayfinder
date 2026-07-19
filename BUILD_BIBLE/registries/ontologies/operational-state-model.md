# Operational State Model

Operational state describes what an active system is currently doing.

## Canonical States

- `planned`: intended but not installed.
- `installed`: physically installed but not yet accepted.
- `commissioning`: under acceptance testing.
- `normal`: operating within expected range.
- `idle`: available but not actively providing service.
- `active`: actively providing service.
- `maintenance`: intentionally unavailable or constrained for service.
- `testing`: intentionally exercised for validation.
- `fault`: degraded or failed outside expected range.
- `emergency`: operating under emergency conditions.
- `offline`: intentionally or unintentionally unavailable.
- `retired`: removed from active service.

## Rule

Operational state is not lifecycle phase. Use lifecycle for long-term asset
position and operational state for current behavior.

## Relationships

- Contract: [Operational State Contract](../../contracts/operational-state-contract.md)
- Schema: [operational-state.schema.json](../../schemas/operational-state.schema.json)
- Related lifecycle: [Property Lifecycle](../../lifecycle/property-lifecycle.md)
- Generated artifacts: operating mode guides, status dashboards, alert routing,
  emergency checklists

