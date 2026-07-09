# ADR-0011: Adopt Progressive Discovery And Minimal Retrieval

Status: Accepted

## Context

Wayfinder operates over large source exports, generated indexes, repository
trees, physical-domain records, future containers, OSINT inputs, home systems,
and conversation memory. Loading full content by default increases tokens,
I/O, latency, privacy exposure, and unnecessary computation.

Existing architecture already prefers Reality First, Ephemeral First,
bounded import profiles, derived indexes, review queues, and reproducible
retrieval. The missing decision is a single canonical retrieval discipline
that applies across domains without creating a new engine or duplicating
domain ownership.

Referenced architecture sections:

- [00 Overview](../architecture/00-overview.md)
- [02 Perception](../architecture/02-perception.md)
- [05 Representations](../architecture/05-representations.md)
- [18 Cross-Cutting Systems](../architecture/18-cross-cutting.md)
- [20 Repository Map](../architecture/20-repository-map.md)
- [Canonical Language Retrieval Strategy](../canonical-language/retrieval-strategy.md)

## Decision

Adopt Progressive Discovery as a constitutional retrieval invariant.

Canonical progression:

```text
Reality -> Root Inventory -> Metadata -> Structure -> Summary -> Relationships -> Candidate Selection -> Targeted Retrieval -> Full Content
```

Full content retrieval is the final escalation step and is used only when
smaller representations cannot satisfy the current objective with adequate
confidence.

Filesystem operations use:

```text
Observe -> Inventory -> Classify -> Build Canonical Destinations -> Simulate -> Execute -> Verify -> Report
```

Unknown or low-confidence items go to review instead of being guessed. Moves
must be reversible, logged, verified, and reported with confidence.

## Consequences

- Retrieval, indexing, imports, repository operations, Build Bible
  intelligence, ARK consumers, conversation memory, containers, OSINT, home
  systems, and future domains share one shallow-to-deep discipline.
- Domain owners remain responsible for domain semantics and stricter limits.
- Generated indexes and metadata become preferred access surfaces, but remain
  derived and rebuildable.
- Implementations should expose status sufficient to explain retrieval depth,
  confidence, and stop conditions.

## Evidence

- Canonical Language already has deterministic retrieval units and rebuildable
  indexes.
- Knowledge Retrieval and generated Knowledge artifacts are documented as
  derived representations.
- Import Profiles already require bounded large imports.
- Candidate Page ADRs already move large review surfaces toward bounded
  intake.

## Rollback

Rollback by reverting this ADR and associated documentation language. No
runtime behavior, schemas, or file placement changes are introduced by this
decision.
