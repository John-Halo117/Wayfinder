# Promotion Registry

The promotion registry records concepts that have moved from legacy,
ephemeral, duplicated, or uncertain ownership into a canonical Wayfinder home.

Nothing is considered promoted unless it has an entry here.

## Registry Schema

| Field | Meaning |
| --- | --- |
| Name | Concept or responsibility being promoted. |
| Current Owner | Canonical owner after promotion. |
| Previous Owner | Prior owner or source of evidence. |
| Proof | Evidence that behavior, semantics, and ownership are preserved. |
| Date | Promotion date in `YYYY-MM-DD` format. |
| Rollback | How to restore prior behavior or ownership if proof fails. |
| Confidence | Low, Medium, or High. |

## Promoted Concepts

| Name | Current Owner | Previous Owner | Proof | Date | Rollback | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Wayfinder Constitution | `constitution/` | Initial prompt and repository foundation | `WAYFINDER.md`, `constitution/laws.md`, `constitution/architecture.md` | 2026-06-27 | Restore foundation docs from Git history or initial prompt evidence. | High |
| Platform Substrate: Identity | `services/identity/`, `contracts/identities/` | ARK identity/subjects evidence, Wayfinder substrate phase | `services/identity/README.md`, `contracts/identities/README.md`, `docs/ownership-matrix.md` | 2026-06-27 | Reclassify as unpromoted substrate and restore ownership to census evidence. | Medium |
| Platform Substrate: Event Bus | `services/event-bus/`, `contracts/events/` | ARK event backbone evidence, Wayfinder substrate phase | `services/event-bus/README.md`, `contracts/events/README.md`, `docs/ownership-matrix.md` | 2026-06-27 | Reclassify as unpromoted substrate and restore ownership to ARK event evidence. | Medium |
| Platform Substrate: Storage | `services/storage/`, `contracts/storage/` | ARK storage/persistence evidence, Wayfinder substrate phase | `services/storage/README.md`, `contracts/storage/README.md`, `docs/ownership-matrix.md` | 2026-06-27 | Reclassify as unpromoted substrate and restore ownership to ARK storage evidence. | Medium |
| Foundry Canonical Owner | `engines/foundry/` | Forge-origin ARK source | `engines/foundry/README.md`, `engines/foundry/docs/ark-forge-normalization.md` | 2026-06-27 | Keep Forge-origin material under ARK legacy as behavioral authority. | Medium |
| Observation Contract | `contracts/observations/` | ARK ingestion, truth-spine, and census evidence | `contracts/observations/README.md`, `docs/promotions/observation-contract.md` | 2026-06-27 | Remove `contracts/observations/README.md` and revert this promotion's governance updates. | High |
| Evidence Contract | `contracts/evidence/` | ARK legacy proof, Bayes, epistemic, TRISCA evidence | `contracts/evidence/README.md`, `docs/promotions/evidence-contract.md` | 2026-06-27 | Revert `contracts/evidence/README.md` and this promotion's governance updates. | High |
| Provenance Contract | `contracts/provenance/` | ARK truth-spine provenance edge and lineage evidence | `contracts/provenance/README.md`, `docs/promotions/provenance-contract.md` | 2026-06-27 | Revert `contracts/provenance/README.md` and this promotion's governance updates. | High |
| Identity Contract | `contracts/identities/` | ARK subjects, identity rules, substrate identity evidence | `contracts/identities/README.md`, `docs/promotions/identities-contract.md` | 2026-06-27 | Revert `contracts/identities/README.md` and this promotion's governance updates. | High |
| Asset Contract | `contracts/assets/` | ARK truth-spine raw artifact/entity/object evidence and Wayfinder contract vocabulary | `contracts/assets/README.md`, `docs/promotions/assets-contract.md` | 2026-06-27 | Revert `contracts/assets/README.md` and this promotion's governance updates. | High |
| Event Contract | `contracts/events/` | ARK event schema, NATS/GSB, internal event contracts, Event Bus substrate evidence | `contracts/events/README.md`, `docs/promotions/events-contract.md` | 2026-06-27 | Revert `contracts/events/README.md` and this promotion's governance updates. | High |
| Policy Contract | `contracts/policies/` | ARK policy rules, policy engine, Foundry MCP policy evidence | `contracts/policies/README.md`, `docs/promotions/policies-contract.md` | 2026-06-27 | Revert `contracts/policies/README.md` and this promotion's governance updates. | High |
| Permission Contract | `contracts/permissions/` | Wayfinder policy/permissions vocabulary and access boundary evidence | `contracts/permissions/README.md`, `docs/promotions/permissions-contract.md` | 2026-06-27 | Revert `contracts/permissions/README.md` and this promotion's governance updates. | High |
| Capability Contract | `contracts/capabilities/` | ARK mesh capability routing, Jarvis navigation, Foundry tool selection evidence | `contracts/capabilities/README.md`, `docs/promotions/capabilities-contract.md` | 2026-06-27 | Revert `contracts/capabilities/README.md` and this promotion's governance updates. | High |
| Bearing Contract | `contracts/bearings/` | Jarvis navigation and Wayfinder bearings vocabulary evidence | `contracts/bearings/README.md`, `docs/promotions/bearings-contract.md` | 2026-06-27 | Revert `contracts/bearings/README.md` and this promotion's governance updates. | High |
| View Contract | `contracts/views/` | ARK projections/reducers/views and Wayfinder Views engine vocabulary evidence | `contracts/views/README.md`, `docs/promotions/views-contract.md` | 2026-06-27 | Revert `contracts/views/README.md` and this promotion's governance updates. | High |
| Capsule Contract | `contracts/capsules/` | Wayfinder Capsules continuity vocabulary and Foundry/Jarvis continuity consumer evidence | `contracts/capsules/README.md`, `docs/promotions/capsules-contract.md` | 2026-06-27 | Revert `contracts/capsules/README.md` and this promotion's governance updates. | High |
| Promotion Contract | `contracts/promotion/` | ARK promotion engine, promotion_v1 schema, governance promotion evidence | `contracts/promotion/README.md`, `docs/promotions/promotion-contract.md` | 2026-06-27 | Revert `contracts/promotion/README.md` and this promotion's governance updates. | High |
| Health Contract | `contracts/health/` | ARK health schema, mesh heartbeat, telemetry and governance health evidence | `contracts/health/README.md`, `docs/promotions/health-contract.md` | 2026-06-27 | Revert `contracts/health/README.md` and this promotion's governance updates. | High |
| Schema Contract | `contracts/schemas/` | ARK runtime schemas, internal contracts, existing schema contract evidence | `contracts/schemas/README.md`, `docs/promotions/schemas-contract.md` | 2026-06-27 | Revert `contracts/schemas/README.md` and this promotion's governance updates. | High |

## Pending Promotion Candidates

| Name | Proposed Owner | Evidence | Status |
| --- | --- | --- | --- |
| Telemetry Service | `services/telemetry/` | `docs/constitutional-census.md`, `contracts/health/README.md` | Pending future wave; do not promote during Wave 2 |
| Discovery Service | `services/discovery/` | ARK mesh evidence and Jarvis navigation overlap | Needs boundary proof |
| ARK Evidence Behavior | `engines/ark/proofs/` | `contracts/evidence/README.md`, ARK proof evidence | Pending engine behavior promotion |
| ARK Promotion Behavior | `engines/ark/proofs/`, `engines/ark/core/` | `contracts/promotion/README.md`, ARK promotion evidence | Pending engine behavior promotion |

## Wave 2 Core Platform Service Promotions

| Name | Current Owner | Previous Owner | Proof | Date | Rollback | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Identity Service | `services/identity/` | ARK subjects modules and identity rules | `docs/promotions/identity-service.md` | 2026-06-27 | Remove service scaffold/governance entries; no runtime rollback | High |
| Event Bus Service | `services/event-bus/` | ARK GSB, transport adapters, event WAL | `docs/promotions/event-bus-service.md` | 2026-06-27 | Remove service scaffold/governance entries; no runtime rollback | High |
| Storage Service | `services/storage/` | ARK DuckDB, Rust storage, Redis state adapters | `docs/promotions/storage-service.md` | 2026-06-27 | Remove service scaffold/governance entries; no runtime rollback | High |
| Configuration Service | `services/configuration/` | ARK env/config loaders, Foundry runtime config, Jarvis ingress env | `docs/promotions/configuration-service.md` | 2026-06-27 | Remove service scaffold/governance entries; no runtime rollback | Medium-High |
| Policy Service | `services/policy/` | ARK policy engines/rules and Foundry policy gates | `docs/promotions/policy-service.md` | 2026-06-27 | Remove service scaffold/governance entries; no runtime rollback | High |

## Phase 4 Service Implementation Proofs

| Name | Current Owner | Previous Owner | Proof | Date | Rollback | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Identity Implementation | `services/identity/` | ARK truth-spine entity model and request ID middleware | `docs/promotions/identity-implementation.md` | 2026-06-27 | Remove implementation files/governance entries; no engine rollback | Medium-High |

