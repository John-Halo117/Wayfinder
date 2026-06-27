# Wayfinder

Wayfinder is the constitutional continuity platform for preserving reality,
reasoning under uncertainty, navigating capabilities, and maintaining long-term
continuity.

The repository is organized as a master monorepo. Existing and future projects
are folded into the architecture by responsibility, not by implementation
history or convenience.

## Constitutional Priority

Wayfinder optimizes for:

- Capability
- Continuity
- Attention
- Maneuverability

Architectural integrity takes precedence over short-term convenience.

## Repository Map

```text
wayfinder/
  canon/
  constitution/
  contracts/
  capabilities/
  services/
  engines/
  domains/
  internal/
  external/
  operations/
  tooling/
  docs/
  tests/
```

Dependencies point downward through the stack. Concepts have one canonical
home, and all other locations reference that home.

## Getting Oriented

- Start with [WAYFINDER.md](WAYFINDER.md) for the constitutional foundation.
- Use [canon/glossary.md](canon/glossary.md) for canonical terms, aliases, deprecated names, and ownership boundaries.
- Use [docs/repository-folding.md](docs/repository-folding.md) when moving an
  existing repository into the monorepo.
- Use [docs/classification.md](docs/classification.md) before adding any new
  concept.
- Use [engines/README.md](engines/README.md) before creating or modifying an
  engine.

