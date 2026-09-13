# RFC-0001 — Wayfinder Existing Repository Collision and Migration Decision

Status: Accepted
Decision date: 2026-09-12
Scope: Wayfinder repository identity, history, and migration posture

## Decision

The existing `John-Halo117/Wayfinder` repository is the canonical Wayfinder child repository and its Git history is preserved in place.

The constitutional skeleton is layered into this repository additively. Existing content is not moved, deleted, rewritten, or made authoritative merely by presence. Canonical authority continues to derive from Foundation v2, approved Wayfinder specifications, and governed ownership decisions.

Any historical material whose ownership is uncertain remains non-authoritative until audited. Content that belongs to another canonical owner may be referenced or later migrated through a separate, history-preserving ADR; it must not be silently reclassified.

## Context

The skeleton-readiness pass identified an implementation-bearing Wayfinder repository at the same target where a clean skeleton had been expected. Treating that collision as grounds for destructive cleanup would risk historical loss and accidental semantic reassignment.

The requirement is to make Wayfinder governable without discarding useful history or creating a second competing Wayfinder authority.

## RFC Questions

1. **Does this concept already exist?** Yes. The existing Wayfinder repository and its history already exist and are in active use.
2. **Who canonically owns it?** Wayfinder owns Wayfinder semantic history and specifications. Presence alone does not grant semantic authority to historical artifacts.
3. **Can it be harvested?** Yes. Existing semantic assets may be harvested after ownership audit; implementation artifacts remain owned by their proper implementation repositories.
4. **Can it be generalized?** Yes. The resolution establishes a general rule: preserve repository history and reconcile authority additively rather than replacing repositories destructively.
5. **Can an existing abstraction satisfy the requirement?** Yes. Foundation v2 canonical ownership plus normal Git history and governed ADR migration are sufficient.
6. **Does introducing this concept create semantic duplication?** No new Wayfinder authority is created.
7. **Does it preserve constitutional laws?** Yes: one canonical owner, backward continuity, evidence/history preservation, and explicit migration.
8. **Does it improve architectural clarity?** Yes. Repository identity and semantic authority are explicitly separated.

## Alternatives Considered

### Replace the existing repository with a clean skeleton
Rejected. It is destructive, loses history or requires unnecessary archival choreography, and creates needless migration risk.

### Create a second clean Wayfinder repository/path
Rejected. It creates competing authority and a long-lived reconciliation burden.

### Preserve the existing repository but freeze all further work indefinitely
Rejected. It avoids immediate risk but prevents governed convergence.

## Ownership Impact

No canonical ownership changes. Wayfinder remains the semantic authority defined by Foundation v2. Runtime, persistence, presentation, contract packaging, and other implementation responsibilities remain with their existing owners.

## Compatibility Impact

Backward compatible. Existing paths and history remain valid. New constitutional material is additive.

## Migration Expectations

- Preserve all existing Git history.
- Do not bulk move or delete historical content.
- Audit uncertain content before assigning authority.
- Migrate material only through explicit owner-qualified ADRs when migration has positive value.
- Prefer aliases/references over destructive relocation when either preserves compatibility.

## Rollback

No destructive action is required. If later evidence changes the preferred repository organization, this decision can be superseded by another RFC/ADR while retaining the existing history.

## Review Outcome

Accepted by repository owner direction to proceed with the governed implementation path. The collision stop condition is resolved by preservation-in-place; this RFC does not authorize unrelated runtime implementation inside Wayfinder.
