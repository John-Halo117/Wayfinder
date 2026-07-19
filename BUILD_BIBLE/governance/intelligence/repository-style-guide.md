# Repository Style Guide

The repository style guide defines how Build Bible documents are written so
they remain composable and machine-readable over time.

## Markdown Structure

Use short canonical documents with one concept per document. Prefer these
sections when applicable:

- Purpose
- Scope
- Required Fields
- Rules
- Relationships
- Lifecycle
- Generation Targets

## Metadata Requirements

Major documents should expose relationships to doctrine, contracts, schemas,
patterns, reliability, verification, generated targets, and future reality
records when applicable.

## Cross-Reference Style

Use relative Markdown links to canonical owners. Do not duplicate facts that
belong to another owner.

## Terminology

Use terms from registries and ontologies. Introduce new terms only when no
existing term is accurate.

## SHALL, SHOULD, MAY

- `SHALL`: mandatory for validity.
- `SHOULD`: expected default unless an Engineering Decision Record accepts a
  tradeoff.
- `MAY`: allowed option.

## Examples

Examples must remain generic unless placed in a specification or reality
record. Do not use examples to smuggle property-specific facts into doctrine.

## Versioning

Prefer additive evolution. Supersede documents explicitly rather than silently
rewriting history.

## File Organization

Place concepts in the narrowest existing owner. Add a new directory only when
the concept has multiple related documents and no existing directory owns the
group.

When reorganizing files, inventory before moving, classify before choosing
destinations, simulate before execution, and route low-confidence items to
review. Moves must be reversible, logged, verified, and reported with
confidence.

## Section Ordering

Use stable ordering so future tools can parse repeated document shapes.

## Relationships

- Metadata: [Document Metadata Standard](document-metadata-standard.md)
- Naming: [Naming Standard](../naming-standard.md)
- Canonicality: [Canonicality](../canonicality.md)
