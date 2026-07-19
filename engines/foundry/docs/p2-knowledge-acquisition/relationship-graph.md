# Relationship Graph

## Canonical Files

- `Knowledge/Graph/edges.jsonl`
- `Knowledge/Graph/relationships/index.json`
- `Knowledge/Graph/relationships/part-*.json`
- `Knowledge/Graph/provenance.jsonl`

## Relationship Classes

P2 recognizes these relationship classes:

- Concept to concept.
- Concept to alias.
- Artifact to source.
- Decision to source.
- Requirement to project.
- Capability to implementation.
- Implementation to repository owner.
- Observation to provenance.
- Historical artifact to successor or canonical owner.

## Validation Contract

Every relationship must reference valid objects or be recorded as unresolved.
Duplicate concepts are linked rather than duplicated. Relationship conflicts are
review artifacts until promoted with evidence.
