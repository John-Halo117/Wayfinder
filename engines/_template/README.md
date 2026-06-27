# Engine Template

Replace this template by copying it into `engines/<engine-name>/` and updating
the engine responsibility, contracts, lifecycle, and health signal.

## Responsibility

This engine must own exactly one major responsibility.

## Lifecycle

Work enters through ingress, is grounded in append-only reality, processed in
ephemeral state, validated by proofs, promoted intentionally, executed through
core durable logic, and exposed through egress.

## Health

Every engine must expose a bounded health signal describing dependency status,
contract compatibility, and proof/promotion readiness.

