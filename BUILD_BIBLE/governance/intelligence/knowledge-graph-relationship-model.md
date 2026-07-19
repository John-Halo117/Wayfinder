# Knowledge Graph Relationship Model

The Build Bible knowledge graph treats every document as a node and explicit
links as typed relationships.

## Relationship Types

- `implements`
- `depends_on`
- `composes`
- `extends`
- `specializes`
- `references`
- `supersedes`
- `requires`
- `provides`
- `generated_from`
- `verified_by`
- `reviewed_by`
- `related_to`

## Relationship Rules

- `implements` means a document satisfies a contract, doctrine, or pattern.
- `depends_on` means a document cannot be interpreted safely without another
  document.
- `composes` means a pattern is assembled from peer patterns or standards.
- `extends` means a child inherits questions and obligations from a parent.
- `specializes` means a document narrows a general rule for a domain.
- `references` means navigational or explanatory linkage.
- `supersedes` means the source replaces an earlier canonical record.
- `requires` means a capability, resource, or dependency is necessary.
- `provides` means a scope or pattern exposes a capability.
- `generated_from` points from output to canonical source.
- `verified_by` points to evidence, observation, inspection, or acceptance.
- `reviewed_by` points to review records or review standards.
- `related_to` is a weak relationship used only when no stronger type applies.

## Direction Rule

Use relationship direction consistently. A generated artifact is
`generated_from` source; source is not generated from the artifact.

## Relationships

- Query model: [Build Bible Query Language](query-language.md)
- Validation: [Repository Validation Standard](../validation/repository-validation-standard.md)
- Traceability: [Traceability Standard](../reviews/traceability-standard.md)
- Generated artifacts: knowledge graph exports, relationship indexes,
  traceability maps

