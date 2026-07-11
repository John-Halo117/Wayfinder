# Wayfinder Implementation Readiness Report

Status: Not ready - halted pending RFC  
Repository: Wayfinder  
Phase: Skeleton validation  

## Summary

Wayfinder is not implementation-ready. The target path
`repositories/wayfinder/` already contains an existing implementation-bearing
nested repository. This conflicts with the requested skeleton-only lifecycle
and prevents certification.

## Outstanding RFCs

Required:

- RFC-0001 Wayfinder Existing Repository Collision and Migration Decision

## Outstanding ADRs

Potential ADRs after RFC disposition:

- Wayfinder existing repository preservation and migration plan.
- Harvest/move/retain decision for existing implementation-bearing content.
- Ownership reassignment decisions for any content that belongs to ARK,
  Foundry, Aurora, Observatory, AMOS, Odysseus, Jarvis, Atlas, Basecamp,
  Groundskeeper, Commons, or Polaris.
- Compatibility and rollback plan for existing Wayfinder users or workflows.

## Remaining Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Existing implementation becomes accidental Wayfinder authority | Critical | Halt and resolve through RFC/ADR. |
| History-preserving policy is violated by cleanup | Critical | Do not move/delete content without approved migration plan. |
| Ownership duplication | Critical | Audit existing services, engines, contracts, and docs against Foundation v2 owners. |
| Skeleton certification becomes meaningless | High | Keep validation failed until target path is resolved. |

## Implementation Assumptions

No implementation assumptions are approved while this stop condition is open.

## Known Unknowns

- Which existing Wayfinder materials are canonical semantic assets.
- Which existing materials are implementation or legacy artifacts.
- Which materials belong in future repositories.
- Whether the constitutional skeleton should be created in a new clean path or
  layered into the existing repository after migration.
- Whether existing nested Git history must be preserved as the Wayfinder child
  repository history.

## Recommended Resolution Order

1. Review and decide RFC-0001.
2. If accepted, produce required ADR(s) for migration/history/ownership.
3. Audit existing Wayfinder contents against Foundation v2 ownership.
4. Decide whether to preserve, archive, migrate, or leave existing materials.
5. Re-run skeleton generation only after the target path is constitutionally
   clear.

## Certification Status

| Certification | Status | Evidence |
| --- | --- | --- |
| Skeleton Certified | Fail | Existing implementation-bearing repository present. |
| Interface Certified | Fail | Existing surfaces require audit before certification. |
| Documentation Certified | Blocked | New placeholders coexist with unaudited historical docs. |
| Governance Certified | Blocked | RFC/ADR decision required. |
| Implementation Ready | Fail | Stop condition active. |

## Readiness Decision

Not ready.

## Approval Requested

Do not proceed to AMOS. Review the RFC candidate and decide how to handle the
existing Wayfinder repository collision.

