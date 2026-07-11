# Identity And Addressing

Every physical scope must have a stable identity and a spatial address.

## Identity

Stable IDs use this shape:

```text
bb:<namespace>:<slug>
```

IDs are stable across renames. Human names may change; IDs do not.

## Namespaces

Namespaces are registered in
[registries/identity-namespaces.md](../registries/identity-namespaces.md).

## Spatial Address

Spatial addresses identify physical location relative to a parent scope.

Required fields:

- parent scope ID
- local coordinate or named location
- boundary description
- access description
- last verified date
- verification source

## Address Stability

If a physical object moves, preserve the old record in history and update the
current spatial address. Do not reuse the old address for a different object
unless a lifecycle change record explains the transition.

