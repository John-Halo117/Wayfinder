# ARK Duplicate Concept Report

Phase 1 finding: ARK contains several concepts in multiple implementation homes. These should not be rewritten yet; they should be extracted to one canonical owner and referenced from legacy ARK until behavior is proven equivalent.

| Concept | Current Duplicate Homes | Canonical Owner | Action |
| --- | --- | --- | --- |
| Contracts/events/schemas | `ark/event_schema.py`, `ark/emitter_contracts.py`, `ark/runtime_contracts.py`, `internal/contracts/*.json`, `ark/integrations/contracts.py`, `ark-core/forge/mcp/contracts.py` | `contracts/ark/` | Extract contract/service, then replace ARK-local duplicate with references. |
| Policy/rules | `policy/*.json`, `policy/policy.go`, `ark/policy_engine.py`, `ark/src/policy/*`, `ark-core/forge/mcp/policy.py`, `internal/epistemic/policy.go` | `services/policy/` | Extract contract/service, then replace ARK-local duplicate with references. |
| Storage/persistence | `ark/duck_client.py`, `ark/src/storage/*`, `duckdb/*`, `internal/adapters/redisstate/store.go`, `internal/state/README.md` | `services/storage/` | Extract contract/service, then replace ARK-local duplicate with references. |
| Event bus/transport | `gsb/gsb.go`, `internal/transport/*`, `internal/adapters/natspub/publisher.go`, `ark/src/event/wal.rs` | `services/event-bus/` | Extract contract/service, then replace ARK-local duplicate with references. |
| Identity/subjects | `ark/subjects.py`, `internal/subjects/subjects.go`, `policy/ark_identity_rules.json` | `services/identity/` | Extract contract/service, then replace ARK-local duplicate with references. |
| Runtime/config | `ark/config.py`, `internal/config/env.go`, `ark-core/forge/runtime/config.py`, `config/*.json`, `config/*.env` | `services/configuration/` | Extract contract/service, then replace ARK-local duplicate with references. |
| Cryptography/compression/security | `internal/crypto/*`, `internal/cryptofabric/*`, `ark/security.py`, `ark/src/compress/*` | `services/cryptography/` | Extract contract/service, then replace ARK-local duplicate with references. |
| Foundry behavior from Forge-origin ARK source | `ark-core/forge/*`, `scripts/ai/*`, `forge`, `forge-app`, `Forge App.*` | `engines/foundry/` | Preserve compatibility names, extract Foundry behavior, then replace ARK-local duplicate with references. |
| Observability/health | `internal/contracts/health_v1.json`, `ark/src/otel.rs`, `prometheus.yml`, `monitor-prod.sh`, `mesh heartbeat docs` | `services/telemetry/` | Extract contract/service, then replace ARK-local duplicate with references. |
