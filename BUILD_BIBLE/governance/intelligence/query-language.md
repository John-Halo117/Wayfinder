# Build Bible Query Language

The Build Bible query language is a conceptual language for future tooling. It
is documented here; it is not implemented in P3.

## Query Shape

```text
FIND <document-class>
WHERE <relationship-or-field> <operator> <value>
RETURN <fields-or-related-documents>
```

## Example Queries

```text
FIND pattern
WHERE composes CONTAINS wet-area
RETURN title, path, contracts
```

```text
FIND doctrine
WHERE references CONTAINS drainage
RETURN title, defined_in
```

```text
FIND pattern
WHERE implements = universal-scope
RETURN title, inheritance, composition
```

```text
FIND dependency
WHERE status = unresolved
RETURN subject, depends_on, criticality
```

```text
FIND reliability-record
WHERE failure_resource = water
RETURN failure, detection, isolation, recovery
```

```text
FIND document
WHERE depends_on = room-spine
RETURN title, path, relationship_type
```

```text
FIND generated-artifact
WHERE generated_from = <pattern-id>
RETURN artifact_type, path, generator
```

## Supported Query Concepts

- document class
- layer
- path
- relationship type
- contract
- schema
- pattern
- capability
- resource
- reliability class
- verification state
- generated artifact target

## Rule

Queries operate on canonical metadata and typed relationships. They must not
infer hidden design intent from prose when explicit metadata is absent.

Queries follow Progressive Discovery. They should answer from indexes,
metadata, relationship records, and scoped summaries before opening full
documents. If metadata is absent or confidence is low, the result is a review
item rather than an inferred fact.

## Relationships

- Relationship model: [Knowledge Graph Relationship Model](knowledge-graph-relationship-model.md)
- Metadata: [Document Metadata Standard](document-metadata-standard.md)
- Validation: [Repository Validation Standard](../validation/repository-validation-standard.md)
- Wayfinder retrieval: [Canonical Language Retrieval Strategy](../../../docs/canonical-language/retrieval-strategy.md)
