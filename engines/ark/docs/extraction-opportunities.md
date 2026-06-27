# ARK Service and Contract Extraction Opportunities

## Service Extraction Opportunities

| Service | Evidence | Proposed Owner | First Extraction Boundary |
| --- | --- | --- | --- |
| Storage/Persistence | DuckDB clients, Rust storage, Redis state adapter, state docs | services/storage/ | Define storage interfaces and keep ARK legacy adapters behind them. |
| Event Bus/Transport | NATS transport, GSB, WAL events, natspub adapter | services/event-bus/ | Create event publish/subscribe contract and bounded health check. |
| Identity | subjects modules and identity rules | services/identity/ | Define subject identifier schema and resolver API. |
| Policy | policy JSON, Go policy, Python policy engine, MCP policy | services/policy/ | Promote policy schemas to contracts, implementation to service. |
| Cryptography/Compression | hash/key/envelope/compress/fabric/security modules | services/cryptography/ | Expose hashing, envelopes, signing, and compression as explicit dependencies. |
| Configuration | env loaders, manifests, tiering/system invariants | services/configuration/ | Centralize config parsing, validation, and redaction. |
| Discovery/Registry | mesh registry and integration registry modules | services/discovery/ | Capability registration and lookup API. |
| Telemetry/Logging | OTel, Prometheus, health schema, runtime logs | services/telemetry/ | Standard health/status schema and bounded probes. |
| Scheduling/Resource Control | autoscaler, budgets, runtime caps | services/scheduling/ | Budget controller and scaler interface. |

## Contract Extraction Opportunities

| Contract | Evidence | Proposed Owner | Notes |
| --- | --- | --- | --- |
| Events | event_v1.json, event_schema.py, gsb, WAL | contracts/events/ | Shared event envelope must be implementation-free. |
| Observations | ingestion service, truth spine, SD-ARK ingest | contracts/observations/ | Observation schema should distinguish observation from interpretation. |
| Evidence | Bayes/TRISCA/proof paths, epistemic resolver | contracts/evidence/ | Evidence contract supports proof before promotion. |
| Promotion | promotion_v1.json, internal/promotion/engine.go | contracts/promotion/ | Promotion criteria and result schema. |
| Health | health_v1.json, mesh heartbeat, runtime checks | contracts/health/ | Bounded health signal shared across services and engines. |
| External actions | external_action_v1.json, action/action.go | contracts/actions/ | Action request/result schema independent of adapters. |
| Runtime schemas | runtime_schemas_v1.json, runtime_contracts.py | contracts/runtime/ | Execution caps, status, failure model. |
| Identity and subject routing | subjects.py, subjects.go, ark_identity_rules.json | services/identity/ and services/event-bus/ | Identity constraints belong to Identity; subject routing belongs to Event Bus. |
| Policies | definitions/policies.yaml, policy/*.json | contracts/policies/ | Policy document schema before service implementation. |
