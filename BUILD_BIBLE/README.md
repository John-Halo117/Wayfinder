# Build Bible

The Build Bible is the canonical source tree for physical reality: land,
buildings, utilities, fixtures, infrastructure, equipment, agriculture,
maintenance, and future expansion.

It is compiler input for the physical world. Humans edit intent and verified
reality here. Software may consume this tree to generate CAD, BIM, diagrams,
bills of materials, automation configs, inspection checklists, and maintenance
plans.

Wayfinder software is outside this scope. Wayfinder may consume this tree, but
the Build Bible governs physical systems only.

## Canonical Rule

Canonical information lives in exactly one human-edited document. Other
documents reference that owner instead of duplicating its content.

Generated artifacts are never canonical. Generated files must identify their
source scope, source revision, generator, and generation time.

Repository intelligence and future tooling should use Progressive Discovery:
indexes, metadata, relationships, and scoped summaries before full-document
retrieval, with low-confidence findings routed to review.

## Editing Model

- One concept per document.
- Every physical scope has identity, boundaries, interfaces, capabilities,
  constraints, capacity, service paths, inspection paths, upgrade paths,
  replacement paths, maintenance procedures, history, and growth options.
- Every critical capability must be serviceable without destructive access.
- Unknown future technologies are handled by preserved interfaces, spare
  capacity, access paths, and published expansion locations.
- Reality claims require evidence or an explicit verification state.

## Start Here

- [INDEX.md](INDEX.md) explains the repository hierarchy.
- [indexes/constitutional-index.md](indexes/constitutional-index.md) is the
  primary navigation document for long-lived principles.
- [governance/scope-boundary.md](governance/scope-boundary.md) defines what
  belongs in the Build Bible.
- [governance/canonicality.md](governance/canonicality.md) defines canonical
  ownership and reference rules.
- [doctrine/fractal-spines.md](doctrine/fractal-spines.md) defines the recursive
  spine model.
- [contracts/physical-scope-contract.md](contracts/physical-scope-contract.md)
  defines the minimum required structure for any physical scope.
- [contracts/universal-scope-contract.md](contracts/universal-scope-contract.md)
  defines the root abstraction for all physical entities.

## Canonical Pattern Entry Points

- [Property Pattern](domains/site/property-pattern.md)
- [Building Patterns](domains/buildings/patterns/README.md)
- [Utility Standards](domains/utilities/standards/README.md)
- [Spatial Bundle Standard](domains/spaces/spatial-bundle-standard.md)
- [Universal Room Pattern](domains/spaces/universal-room-pattern.md)
- [Universal Wet Area Pattern](domains/spaces/universal-wet-area-pattern.md)
- [Universal Mechanical Pattern](domains/spaces/universal-mechanical-pattern.md)
- [Universal Expansion Pattern](domains/expansion/universal-expansion-pattern.md)
- [Material Standards](domains/materials/material-standards.md)
- [Reusable Maintenance Procedures](domains/maintenance/reusable-maintenance-procedures.md)
- [Resource Flow Ontology](registries/ontologies/resource-flow-ontology.md)
- [Dependency Ontology](registries/ontologies/dependency-ontology.md)
- [Reliability](lifecycle/reliability/README.md)
- [Metrics Rubrics](governance/reviews/metrics-rubrics.md)
- [Anti-Pattern Library](governance/reviews/anti-pattern-library.md)
- [Repository Intelligence](governance/intelligence/README.md)
- [Repository Validation](governance/validation/README.md)
- [Pattern Composition Catalog](registries/composition/pattern-composition-catalog.md)
- [Digital Twin Readiness Standard](digital-twin/readiness-standard.md)
- [Indexes](indexes/README.md)
- [BUILD_OPERATIONS](../BUILD_OPERATIONS/README.md)
