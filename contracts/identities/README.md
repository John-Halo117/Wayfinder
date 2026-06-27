# Identity Contract

## Purpose

Defines shared language for stable identity: RIDs, aliases, namespaces, lifecycle, lookup, canonical identity, and merge semantics.

## Producer

Identity Service

Exactly one service produces identity boundary language. Engines consume identity references; they do not redefine identity vocabulary.

## Consumers

ARK, Event Bus, Storage, Jarvis, Foundry, Capsules, MICE, Domains, Internal applications, Operations

## Inputs

Identity claim, RID reference, alias, namespace, lifecycle signal, evidence reference, provenance reference, policy reference, merge candidate, context.

## Outputs

RID, canonical identity reference, alias reference, namespace reference, lookup result, lifecycle reference, merge decision reference.

## Invariants

- RID identifies an asset or constitutional referent, not a representation.
- Aliases never replace canonical identity.
- Merge and split decisions preserve provenance and uncertainty.
- Identity implementation belongs to Identity Service, while asset meaning remains constitutional.

## Failure Modes

Unknown identity, namespace conflict, alias collision, ambiguous merge, stale lifecycle state, or insufficient evidence remain explicit uncertainty.

## Promotion Rules

Identity claims become durable only when sufficient evidence and provenance support promotion. Temporary lookup results and candidate merges remain ephemeral until proven.

## Constitutional Basis

- [Asset Model](../../constitution/assets.md)
- [Execution Semantics](../../constitution/execution.md)
- [Repository Responsibilities](../../constitution/repository.md)
- [Engine Boundaries](../../engines/README.md)

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Domain-specific schemas.
- Engine internals.
