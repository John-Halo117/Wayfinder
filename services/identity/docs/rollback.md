# Identity Service Rollback Plan

## Rollback Scope

Rollback removes the Wave 2 service scaffold and governance entries for `services/identity/` only.

## Behavior Impact

No runtime behavior rollback is required because no engine code was modified and no implementation was moved.

## Steps

1. Remove `services/identity/` scaffold files.
2. Remove the corresponding row from the Promotion Registry.
3. Revert Ownership Matrix entries for this service to legacy/deferred status.
4. Restore debt status to deferred promotion.
5. Record failed proof in the Constitutional Census.
