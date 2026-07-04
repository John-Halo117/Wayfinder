# Canon

The `canon/` directory contains Wayfinder's semantic kernel: stable names,
ontology entries, glossary entries, aliases, deprecated terms, and naming
rules.

Use [ontology.md](ontology.md) to inspect concept relationships and
[glossary.md](glossary.md) before adding or migrating terms. If a term already
has a canonical owner elsewhere, canon summarizes it and links to that owner
instead of duplicating doctrine.

## Responsibilities

- Preserve One Concept, One Home at the language level.
- Record canonical concept relationships.
- Provide canonical names for humans and coding agents.
- Record aliases and deprecated terms for discoverability.
- Identify ambiguous ownership instead of creating duplicate concepts.

## Non-Responsibilities

- Runtime implementation.
- Service or engine behavior.
- Domain-specific definitions that belong in domains.
- Contract schemas that already belong under `contracts/`.

## Core Semantic Anchors

- [Asset in Context](../constitution/assets.md) is the universal object model every engine can operate on.
- [Ontology](ontology.md) records canonical relationships between concepts.
- [Glossary](glossary.md) records names, aliases, deprecated terms, and acronym
  expansions.
