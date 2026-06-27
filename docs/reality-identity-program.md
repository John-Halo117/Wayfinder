# Reality Identity (RID) Implementation Program

Date: 2026-06-27

This program adds first-class planning for Wayfinder's constitutional Reality Identifier architecture. It is planning evidence only. It does not implement RID, refactor ARK, or change runtime behavior.

## Evidence Summary

| Evidence | Finding |
| --- | --- |
| `constitution/assets.md` | RID is the stable identity reference for an asset or reality-backed entity; it identifies the asset, not a representation. |
| `contracts/identities/README.md` | Identity language includes RID, aliases, namespaces, lifecycle, lookup, canonical identity, and merge semantics. |
| `services/identity/README.md` | Identity Service owns reusable identity infrastructure and consumes identity contracts. |
| `services/identity/docs/implementation-proof.md` | Minimal Identity implementation exists for identity records, aliases, namespace validation, merge decisions, and request identity generation. |
| `constitution/execution.md` | Durable knowledge requires proof and promotion into canonical owners. |
| `docs/implementation-backlog.md` | Identity is Stage 2; ARK implementation depends on platform substrate maturity. |
| `docs/migration-dashboard.md` | ARK remains folded and not yet rewired to platform services. |
| `docs/promotion-registry.md` | Identity Contract, Identity Service, and Identity Implementation promotions are recorded. |

## Objective

Implement the constitutional identity model used throughout Wayfinder.

RID is the universal continuity anchor for Wayfinder. The Constitution defines RID semantics. The Identity Service implements reusable identity capability. ARK consumes RID when preserving observations, evidence, provenance, assets, and reality graph knowledge.

## Ownership

| Concept | Canonical Owner | Notes |
| --- | --- | --- |
| RID constitutional meaning | `constitution/assets.md` | RID identifies assets or reality-backed entities, not representations. |
| RID and identity language | `contracts/identities/` | Defines shared vocabulary and invariants. |
| Reusable identity implementation | `services/identity/` | Implements identity capability without owning ARK behavior. |
| Asset model | `constitution/assets.md`, `contracts/assets/` | Universal asset semantics remain constitutional. |
| Reality preservation behavior | `engines/ark/` | ARK consumes RID; it does not own universal identity. |

## Maturity Model

| Stage | Meaning | Evidence Required |
| --- | --- | --- |
| Stage 0 | Constitutional Definition | RID semantics and ownership are documented. |
| Stage 1 | Contract Language | Identity contract defines RID language, invariants, failure modes, and promotion rules. |
| Stage 2 | Service Capability | Identity Service provides bounded reusable identity primitives. |
| Stage 3 | RID Model | Domain identifier families and encoding rules are planned and specified. |
| Stage 4 | ARK Integration Proof | ARK consumes RID through service boundaries without behavior drift. |
| Stage 5 | Migration Verified | Legacy identity references are migrated or adapted with proof and rollback. |

## RID Program Progress

| Component | Stage | Status |
| --- | :---: | --- |
| Identity Contracts | 1 | ✅ |
| Identity Service | 2 | ✅ |
| RID Model | 2 | 🔄 Next |
| Domain Identifiers | 1 | ⏳ |
| Identity Encoding | 1 | ⏳ |
| Identity Resolution | 2 | ⏳ |
| Provenance Integration | 1 | ⏳ |
| ARK Integration | 1 | ⏳ |
| Migration | 0 | ⏳ |
| Verification | 0 | ⏳ |

## Dependency Order

```text
Identity Service
  -> Reality ID (RID)
  -> Universal Asset Ingestion
  -> Runtime Kernel
  -> ARK
```

RID becomes a prerequisite for full ARK implementation. ARK may continue to preserve legacy behavior until a proof-backed integration consumes RID through the Identity Service.

## Milestone Roadmap

| Milestone | Target Stage | Status | Depends On |
| --- | :---: | --- | --- |
| RID-M-001 Identity Contracts | 1 | ✅ Complete | Constitution v1 |
| RID-M-002 Identity Service | 2 | ✅ Complete | RID-M-001 |
| RID-M-003 RID Model | 3 | 🔄 Next | RID-M-002 |
| RID-M-004 Domain Identifiers | 3 | ⏳ | RID-M-003 |
| RID-M-005 Identity Encoding | 3 | ⏳ | RID-M-004 |
| RID-M-006 Identity Resolution | 3 | ⏳ | RID-M-005 |
| RID-M-007 Provenance Integration | 4 | ⏳ | RID-M-006 |
| RID-M-008 ARK Integration | 4 | ⏳ | RID-M-007 |
| RID-M-009 Migration | 5 | ⏳ | RID-M-008 |
| RID-M-010 Verification | 5 | ⏳ | RID-M-009 |

## Milestone Dependency Graph

```text
RID-M-001 Identity Contracts
  -> RID-M-002 Identity Service
      -> RID-M-003 RID Model
          -> RID-M-004 Domain Identifiers
              -> RID-M-005 Identity Encoding
                  -> RID-M-006 Identity Resolution
                      -> RID-M-007 Provenance Integration
                          -> RID-M-008 ARK Integration
                              -> RID-M-009 Migration
                                  -> RID-M-010 Verification
```

## Implementation Backlog

### RID-M-001 Identity Contracts

Status: Complete.

Acceptance Criteria:

- Identity contract defines RID language.
- RID identifies assets or constitutional referents, not representations.
- Merge and split semantics preserve provenance and uncertainty.

Evidence:

- `contracts/identities/README.md`
- `constitution/assets.md`

### RID-M-002 Identity Service

Status: Complete for minimal service capability.

Acceptance Criteria:

- Identity Service owns reusable identity implementation.
- Service does not import engines, domains, internal apps, external integrations, or operations.
- Focused tests and implementation proof exist.

Evidence:

- `services/identity/identity_service.py`
- `services/identity/tests/test_identity_service.py`
- `services/identity/docs/implementation-proof.md`

### RID-M-003 RID Model

Status: Next.

Tasks:

- Define the RID model without implementing code.
- Clarify constitutional RID shape, namespace families, stability rules, and merge/split semantics.
- Define how RIDs relate to Assets, Observations, Evidence, Provenance, Representations, Relationships, and Events.
- Identify validation requirements and failure modes for later implementation.

Acceptance Criteria:

- RID model is documented as implementation planning, not new constitutional doctrine.
- Identity ownership remains singular.
- ARK remains a consumer, not owner, of RID.
- No implementation files change.

### RID-M-004 Domain Identifiers

Status: Planned.

Scope:

- RID
- AST
- OBS
- ENT
- REL
- EVD
- PRV
- REP
- EVT
- CAP
- POL
- PERM

Acceptance Criteria:

- Identifier families are classified by canonical owner.
- Identifier families do not create duplicate concepts.
- Identifier names align with existing contracts.

### RID-M-005 Identity Encoding

Status: Planned.

Tasks:

- Specify encoding rules for identifier families.
- Preserve readability, stability, and validation boundaries.
- Avoid binding RID semantics to any storage format or database.

Acceptance Criteria:

- Encoding remains implementation-independent until proof.
- Encodings do not expose secrets or unstable representation details.

### RID-M-006 Identity Resolution

Status: Planned.

Tasks:

- Plan lookup, alias resolution, namespace handling, and merge/split behavior.
- Align with existing Identity Service primitives.

Acceptance Criteria:

- Identity resolution remains owned by Identity Service.
- Failure modes are explicit and structured.

### RID-M-007 Provenance Integration

Status: Planned.

Tasks:

- Define how RID claims connect to Evidence and Provenance.
- Identify proof requirements for durable RID claims, merges, and splits.

Acceptance Criteria:

- RID knowledge remains evidence-bound.
- Provenance supports knowledge about identity without defining identity itself.

### RID-M-008 ARK Integration

Status: Planned.

Tasks:

- Plan how ARK consumes RID in observations, evidence, provenance, assets, and reality graph behavior.
- Do not refactor ARK until compatibility proof exists.

Acceptance Criteria:

- ARK consumes RID through service and contract boundaries.
- ARK behavior remains unchanged until proof-backed migration.

### RID-M-009 Migration

Status: Planned.

Tasks:

- Inventory legacy identifiers.
- Define adapters and rollback paths.
- Plan migration without destructive rewrite.

Acceptance Criteria:

- Existing behavior is preserved.
- Migration is reversible or compatibility-preserving.

### RID-M-010 Verification

Status: Planned.

Tasks:

- Verify dependency order.
- Verify acyclic graph.
- Verify Identity ownership singularity.
- Verify ARK consumes rather than owns RID.
- Verify no representation IDs are confused with asset RIDs.

Acceptance Criteria:

- Dependency graph remains acyclic.
- RID precedes full ARK implementation.
- Tests or verification reports prove compatibility.

## Recommended Next Milestone

RID-M-003 RID Model.

Reason: Identity contracts and the minimal Identity Service proof already exist. The next gap is the explicit RID model and identifier-family plan needed before Universal Asset Ingestion and full ARK implementation.

## Validation

| Check | Result |
| --- | --- |
| Dependency graph remains acyclic | Pass |
| RID precedes full ARK implementation | Pass |
| Identity ownership remains singular | Pass |
| ARK remains RID consumer, not owner | Pass |
| No implementation files changed by this planning task | Pass |
