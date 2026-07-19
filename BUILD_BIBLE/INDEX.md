# Build Bible Repository Index

This index explains why each directory exists, what belongs inside it, and
which information is canonical.

## Top-Level Map

```text
BUILD_BIBLE/
  governance/
  doctrine/
  contracts/
  schemas/
  registries/
  indexes/
  reality/
  digital-twin/
  domains/
  lifecycle/
  templates/
  generation/
```

## Directory Responsibilities

### governance/

Owns rules for editing the Build Bible itself: scope boundaries, canonicality,
identity, change control, verification, and generated-artifact boundaries.

Canonical: yes, for repository operating rules.

### doctrine/

Owns durable physical-world principles: platform-not-product, fractal spines,
serviceability, reserve capacity, optionality, and evolution.

Canonical: yes, for design philosophy and invariants.

### contracts/

Owns human-readable contracts for recurring document types such as physical
scopes, spines, interfaces, capabilities, capacity, and maintenance.

Canonical: yes, for document semantics.

### schemas/

Owns machine-readable validation schemas for structured scope records,
interfaces, capabilities, spines, and maintenance procedures.

Canonical: yes, for machine validation.

### registries/

Owns stable identifiers, namespaces, catalogs, and controlled vocabularies used
by physical scopes.

Canonical: yes, for names and reusable terms.

Ontologies live under `registries/ontologies/` because they define reusable
classification and relationship vocabularies rather than property-specific
records.

Composition catalogs live under `registries/composition/` because they define
reusable pattern assemblies and relationship vocabularies.

### indexes/

Owns navigation indexes that point to canonical owners without duplicating
canonical facts.

Canonical: yes, for repository navigation.

### reality/

Owns verified observations, evidence, surveys, inspections, measurements, and
source material that preserve what physically exists.

Canonical: yes, for observed reality when records include evidence and
verification state.

### digital-twin/

Owns the digital representation model for physical scopes: spatial addresses,
state, capacity, service history, maintenance, observations, and last verified
reality.

Canonical: yes, for digital-twin semantics. Generated twin exports belong in
`generation/`.

### domains/

Owns physical domain source files: land, site, buildings, utilities, water,
electrical, low voltage, HVAC, roads, agriculture, equipment, construction, and
maintenance.

Canonical: yes, for domain-specific intent and verified physical systems.

### lifecycle/

Owns decisions, changes, service records, and maintenance schedules across time.

Canonical: yes, for historical record and planned lifecycle obligations.

Reliability lives under lifecycle because degradation, failure, inspection,
verification, recovery, and resilience are long-term obligations across the
life of physical systems.

### templates/

Owns reusable document starters for creating new canonical records consistently.

Canonical: no for any copied instance until the instance is filled, verified,
and placed in its owning directory. The template definitions themselves are
canonical as authoring aids.

### generation/

Owns generated output boundaries and output folders for CAD, BIM, diagrams,
bills of materials, configs, schedules, and documentation.

Canonical: no. This directory contains outputs derived from canonical source
documents.

## Operations Boundary

`BUILD_OPERATIONS/` is a separate top-level physical operations manual layer.
It contains property-specific operating procedures, seasonal routines, active
checklists, operating modes, and emergency actions. It references Build Bible
source records but does not own canonical design intent or maintenance history.

## Reference Rules

Documents reference owners by relative Markdown links and by stable IDs from
the relevant registry. Summaries may be repeated for orientation, but numeric
capacity, physical location, interface definitions, maintenance obligations,
and verification state must link to the canonical owner.

## Physical Scope Placement

A physical scope belongs in the narrowest domain directory that owns its primary
purpose. Shared infrastructure is modeled through interfaces and spines rather
than copied into every consumer.

## Canonical Pattern Layer

The initial reusable physical architecture is organized as classes that future
reality records instantiate:

- Property class: [domains/site/property-pattern.md](domains/site/property-pattern.md)
- Building classes: [domains/buildings/patterns/README.md](domains/buildings/patterns/README.md)
- Utility classes: [domains/utilities/standards/README.md](domains/utilities/standards/README.md)
- Spatial classes: [domains/spaces/spatial-bundle-standard.md](domains/spaces/spatial-bundle-standard.md)
- Spine classes: [doctrine/spines/README.md](doctrine/spines/README.md)
- Expansion class: [domains/expansion/universal-expansion-pattern.md](domains/expansion/universal-expansion-pattern.md)
- Material class: [domains/materials/material-standards.md](domains/materials/material-standards.md)
- Maintenance class: [domains/maintenance/reusable-maintenance-procedures.md](domains/maintenance/reusable-maintenance-procedures.md)
- Universal scope class: [contracts/universal-scope-contract.md](contracts/universal-scope-contract.md)
- Resource-flow ontology: [registries/ontologies/resource-flow-ontology.md](registries/ontologies/resource-flow-ontology.md)
- Dependency ontology: [registries/ontologies/dependency-ontology.md](registries/ontologies/dependency-ontology.md)
- Reliability architecture: [lifecycle/reliability/README.md](lifecycle/reliability/README.md)
- Composition catalog: [registries/composition/pattern-composition-catalog.md](registries/composition/pattern-composition-catalog.md)
- Repository intelligence: [governance/intelligence/README.md](governance/intelligence/README.md)
- Repository validation: [governance/validation/README.md](governance/validation/README.md)
- Constitutional index: [indexes/constitutional-index.md](indexes/constitutional-index.md)

These patterns are canonical source. Property-specific observations, surveys,
installations, and service records are objects instantiated from these classes.
Generated files remain compiled outputs under `generation/`.
