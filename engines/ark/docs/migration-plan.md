# ARK Migration Plan

This plan preserves behavior. ARK legacy code remains intact until each extraction has tests, proof criteria, and a compatibility adapter.

## Phase 1 - Inventory and Classification

- Preserve historical source under `engines/ark/legacy/`.
- Maintain complete classification in `engines/ark/docs/inventory.md`.
- Treat `legacy/` as read-only source material except for emergency compatibility patches.

## Phase 2 - Extract Reusable Services

1. Extract storage/persistence.
2. Extract event bus/transport.
3. Extract configuration.
4. Extract policy.
5. Extract identity.
6. Extract cryptography/compression.
7. Extract telemetry and health.
8. Extract scheduling/resource control.

## Foundry Normalization Note

Forge-labeled engineering workflows from ARK are canonical Foundry material in
Wayfinder. Preserve legacy command/module names until behavior parity and
compatibility aliases are proven.

## Phase 3 - Extract Contracts

Promote implementation-free schemas for events, observations, evidence, promotion, health, runtime, external actions, identity, and policies.

## Phase 4 - Rebuild ARK Engine

- `ingress/`: bounded observation/event intake.
- `reality/`: append-only observations, evidence, provenance, and reality graph records.
- `ephemeral/`: projections, reducers, replay views, derived indexes, recognition, temporary graphs.
- `proofs/`: validation, confidence, consensus, promotion criteria.
- `core/`: durable ARK reality-preservation algorithms and promotion orchestration.
- `egress/`: verified outputs with traceability to observations and proofs.

## Phase 5 - Compatibility and Cutover

- Add adapters so legacy entrypoints consume extracted contracts/services.
- Run legacy tests before and after each extraction.
- Promote only after tests, health checks, and proof criteria pass.
- Retire duplicate implementation only after no ARK behavior depends on it.

## Failure Model

```json
{"status":"error","error_code":"UNCLASSIFIED_ARK_FILE","reason":"A file cannot be assigned a canonical Wayfinder owner from Phase 1 evidence.","context":{"file":"path"},"recoverable":true}
```

```json
{"status":"error","error_code":"BEHAVIOR_PARITY_NOT_PROVEN","reason":"An extracted service or contract does not yet prove equivalent behavior to legacy ARK.","context":{"owner":"services/name"},"recoverable":true}
```
