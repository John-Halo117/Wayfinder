# Domains

Domains hold canonical physical-world source documents grouped by primary
responsibility.

Each domain should define its own scopes, spines, interfaces, capabilities,
constraints, capacity, service paths, inspection paths, upgrade paths,
replacement paths, and maintenance obligations.

Shared infrastructure is referenced through interfaces instead of duplicated.

## Purpose

Define reusable physical architecture for land, structures, spaces, utilities,
materials, equipment, agriculture, construction, maintenance, and future
expansion.

## Contents

- [Site](site/README.md)
- [Buildings](buildings/README.md)
- [Spaces](spaces/README.md)
- [Utilities](utilities/README.md)
- [Drainage](drainage/README.md)
- [Roads](roads/README.md)
- [Expansion](expansion/README.md)
- [Materials](materials/README.md)
- [Maintenance](maintenance/README.md)

## Relationships

Domains implement [doctrine](../doctrine/README.md), conform to
[contracts](../contracts/README.md), may be validated by
[schemas](../schemas/README.md), and are instantiated by
[reality records](../reality/README.md).

## Lifecycle

Domain patterns evolve through decision records. Property-specific facts belong
in instantiated physical scope records, not reusable pattern documents.

## Generation Targets

Domain records feed CAD, BIM, diagrams, bills of materials, maintenance
schedules, automation configs, network configs, and documentation.
