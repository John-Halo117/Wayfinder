# ADR 0007: Promote Storage Service Proof Before Runtime Kernel Extraction

Status: Proposed

Date: 2026-07-05

## Architecture Sections

- [04 ARK](../architecture/04-ark.md)
- [18 Cross-Cutting Systems](../architecture/18-cross-cutting.md)
- [21 Roadmap](../architecture/21-roadmap.md)

## Context

Wayfinder already identifies shared infrastructure as service-owned.
`services/storage/` is the canonical owner for storage language, but it has no
runtime implementation proof. Persistence behavior exists in several places:
ARK reality ingestion storage, governance repositories, retrieval indexes,
export compiler SQLite outputs, and legacy ARK DuckDB/Redis/state files.

The implementation backlog also identifies Storage as the next platform
milestone after Identity and Event Bus.

## Decision

Prioritize a minimal backend-neutral Storage service proof before introducing a
broader Runtime Kernel.

The proof should define small primitives for content-addressed objects,
metadata, append-only writes, bounded reads, transaction boundaries, and health.
It must not select DuckDB, Redis, SQLite, S3, or any concrete backend as
architecture.

## Alternatives Considered

- Extract a Runtime Kernel first. Rejected for now because it would risk
  becoming a broad abstraction before the highest-pressure service boundary is
  proven.
- Rewire ARK directly to a concrete database. Rejected because it would violate
  replaceability and service-first architecture.
- Leave all storage local. Rejected because duplication is already visible and
  high-impact.

## Tradeoffs

Storage-first reduces duplication and prepares later services, but it may leave
smaller utility duplication, such as `to_plain` helpers and limit validation,
in place a little longer. That is acceptable because those utilities are lower
risk than persistence semantics.

## Migration Plan

1. Inventory storage behavior in active modules and legacy evidence.
2. Define the smallest service-owned storage contract.
3. Implement in-memory proof with focused tests.
4. Document compatibility expectations for ARK, Governance, Retrieval, Event
   Bus, Identity, and tooling.
5. Rewire one consumer only after parity evidence exists.
