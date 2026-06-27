# Canon

The `canon/` directory contains Wayfinder's semantic kernel: stable names, glossary entries, aliases, deprecated terms, and naming rules.

Use [glossary.md](glossary.md) before adding or migrating concepts. If a term already has a canonical owner elsewhere, the glossary summarizes it and links to that owner instead of duplicating doctrine.

## Responsibilities

- Preserve One Concept, One Home at the language level.
- Provide canonical names for humans and coding agents.
- Record aliases and deprecated terms for discoverability.
- Identify ambiguous ownership instead of creating duplicate concepts.

## Non-Responsibilities

- Runtime implementation.
- Service or engine behavior.
- Domain-specific definitions that belong in domains.
- Contract schemas that already belong under `contracts/`.
