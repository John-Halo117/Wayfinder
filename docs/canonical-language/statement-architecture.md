# Statement Architecture

## Definition

A Statement is a deterministic language unit derived from source text. It is
small enough to be reused and mined, and large enough to be useful for
compiler, retrieval, and future AI inputs.

A Statement may be:

- a sentence
- a heading
- a bullet item
- a table cell or row summary surface
- a code-adjacent comment
- a short transcript utterance
- a calendar event text field
- a structured field rendered into canonical language

A Statement is not a truth claim. It is language awaiting interpretation.

## Identity

Statement content ID:

```text
cls:v1:<sha256(canonical_english_statement + statement_type + algorithm_version)>
```

Statement occurrence ID:

```text
clso:v1:<sha256(statement_id + observation_id + source_span + parser_version)>
```

Content identity enables reuse. Occurrence identity preserves provenance.

## Statement Types

- declarative
- question
- imperative
- heading
- list_item
- table_cell
- table_row
- code_comment
- transcript_utterance
- metadata_field
- unknown

Type is structural, not semantic truth.

## Relationships

Statements relate to:

- parent observation
- source artifact
- block/paragraph
- previous/next statement
- phrase occurrences
- word occurrences
- chunk membership
- compiler candidates derived later

## Versioning

Statement segmentation and Canonical English normalization are versioned
separately. A change to either can create a new statement ID namespace.

## Compiler Inputs

The Knowledge Compiler should eventually consume Canonical Statements instead
of raw conversation/message text. This preserves deterministic preprocessing
and prevents compiler rules from becoming source-specific.

## Mining

Statements support deterministic mining for:

- recurring decisions
- repeated principles
- glossary-like definitions
- TODOs
- contradictions
- duplicate concepts
- ADR-like rationale

Mining outputs remain candidates until governance review.
