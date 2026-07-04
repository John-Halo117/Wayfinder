# Relationship Architecture

Canonical Language relationships are derived edges. They do not replace Source
Relationships or WEAVE topology.

## Ownership

| Relationship | Owner | Rebuildable |
| --- | --- | --- |
| Observation contains language occurrence | Canonical Language | Yes |
| Statement occurrence has content statement | Canonical Language | Yes |
| Chunk contains statement occurrence | Canonical Language | Yes |
| Statement contains phrase occurrence | Canonical Language | Yes |
| Phrase contains word occurrence | Canonical Language | Yes |
| Previous/next statement | Canonical Language | Yes |
| Source Relationship | ARK preservation | Preserved reality evidence |
| Durable topology | WEAVE | Derived/promoted later |
| Knowledge candidate supports statement | Knowledge Compiler | Yes until promoted |
| Promoted knowledge cites statement | Knowledge Governance | Durable promoted record |

## Rebuild Rules

Canonical Language relationships rebuild from:

- ARK preserved observations
- source spans
- Canonical Language algorithm versions
- Import Profile

If any input changes, derived relationships are regenerated. They are not
manually edited.

## Relationship Types

- `observation_contains_block`
- `block_contains_paragraph`
- `paragraph_contains_statement`
- `statement_has_phrase`
- `phrase_has_word`
- `chunk_contains_statement`
- `statement_next_statement`
- `statement_occurrence_of`
- `chunk_occurrence_of`
- `statement_traced_to_observation`

These are structural relationships only.

## Knowledge Boundary

Canonical Language relationships do not assert meaning. For example,
`statement_next_statement` says two statements were adjacent in the source; it
does not say the second follows logically from the first.
