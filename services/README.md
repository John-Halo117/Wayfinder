# Services

Services are reusable primitives.

Examples include identity, storage, persistence, event bus, search, indexing,
embeddings, cache, scheduling, synchronization, logging, auditing, telemetry,
notifications, permissions, policy, cryptography, compression, plugin runtime,
and configuration.

Services may depend on contracts. Services never depend on engines.

## Platform Substrate

The initial platform substrate is:

- `identity/` - canonical identity, RID generation, aliases, namespaces,
  lifecycle, lookup, and merge semantics.
- `event-bus/` - publish, subscribe, routing, event metadata, correlation IDs,
  and replay support.
- `storage/` - abstract persistence, transactional operations, object storage,
  metadata, and versioning hooks.

These services are reusable infrastructure. Engines consume them through
contracts and explicit dependencies.
