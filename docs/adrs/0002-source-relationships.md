# ADR-0002: Preserve Source Relationships Before Topology

Status: Accepted

Date: 2026-07-03

## Context

First Contact preserved 217,994 explicit relationships from source structure.
WEAVE remains the future owner of durable relationship topology.

## Decision

Source Relationships are explicit relationships present in source data. ARK may
preserve Source Relationships as evidence. WEAVE owns later durable
relationship topology.

## Consequences

- ARK can preserve containment, reply, reference, origin, membership, and
  attachment edges without making topology claims.
- WEAVE consumes preserved evidence when topology is implemented later.
- Documentation must avoid calling ARK-preserved source edges a Knowledge Graph.

## Evidence

- First Contact relationship count: 217,994.
- `docs/first-contact/evidence-assimilation.md`.

## Rollback

Rollback by removing Source Relationship language only if WEAVE is implemented
and proves that preserving explicit source relationships elsewhere is safer.
