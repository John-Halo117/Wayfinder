# Canonical Language Architecture

## Purpose

Canonical Language normalizes source language into reusable, deterministic,
traceable language artifacts. It reduces duplication and provides consistent
compiler/retrieval inputs across Oracles without turning language into reality
or knowledge.

## Placement

```text
Reality
  -> Observation Sources
  -> ARK Preservation
  -> Canonical Language
  -> Knowledge Compiler
  -> Knowledge Governance
  -> Durable Knowledge
  -> Retrieval / Views
```

Canonical Language is downstream of ARK and upstream of interpretation. It is
derived and rebuildable. ARK remains the source of preserved reality.

## Primary Unit

The primary reusable unit is the Statement.

A Statement is the smallest deterministic language unit that can carry a
claim-like, instruction-like, question-like, list-item-like, or utterance-like
surface form while preserving source provenance. A Statement is not a truth
claim by itself. It is language prepared for later interpretation.

## Canonical Hierarchy

```text
Corpus
  -> Source Artifact
  -> Container
  -> Section
  -> Block
  -> Paragraph
  -> Statement
  -> Phrase
  -> Word
  -> Token
  -> Character span
```

Recommended hierarchy for common conversational inputs:

```text
Conversation
  -> Message
  -> Block
  -> Paragraph
  -> Statement
  -> Phrase
  -> Word
  -> Token
```

Recommended hierarchy for document inputs:

```text
Document
  -> Section
  -> Block
  -> Paragraph
  -> Statement
  -> Phrase
  -> Word
  -> Token
```

## Level Justification

| Level | Role | Stable ID | Justification |
| --- | --- | --- | --- |
| Character span | Offset reference | No shared ID | Needed for provenance and replay, too granular for reuse. |
| Token | Parser output | No global ID | Technical boundary for punctuation, code, symbols, and words. |
| Word | Dictionary entry | Yes | Supports language reuse, frequency, and compression. |
| Phrase | Dictionary entry | Yes | Captures recurring multi-word surfaces without implying meaning. |
| Statement | Primary reusable unit | Yes | Best compiler input; smaller than chunks, more meaningful than phrases. |
| Paragraph | Occurrence/container | Occurrence ID | Preserves author formatting and grouping. |
| Chunk | Retrieval/window unit | Yes | Bounded context window for retrieval and later AI. |
| Block | Structural occurrence | Occurrence ID | Handles code blocks, quotes, tables, lists, OCR regions. |
| Section | Structural occurrence | Occurrence ID | Document navigation and rebuild boundary. |
| Message | Source container | Source/Observation ID | Conversational source boundary. |
| Conversation/Document | Source container | Source/Artifact ID | Oracle-preserved aggregate boundary. |

## Stable Identity

Canonical Language separates reusable content identity from source occurrence
identity.

| Layer | Content ID | Occurrence ID | Notes |
| --- | --- | --- | --- |
| Word | `clw:v1:<hash>` | optional | Hash of Canonical English word form plus language version. |
| Phrase | `clp:v1:<hash>` | optional | Hash of ordered word IDs and normalized surface. |
| Statement | `cls:v1:<hash>` | `clso:v1:<hash>` | Content ID deduplicates language; occurrence ID preserves source span. |
| Paragraph | no shared content ID by default | `clpo:v1:<hash>` | Formatting and source grouping matter more than reuse. |
| Chunk | `clc:v1:<hash>` | `clco:v1:<hash>` | Content ID identifies deterministic statement window; occurrence preserves source context. |

Hash input must include:

- artifact type prefix
- canonical language algorithm version
- Canonical English version
- normalized content or ordered child IDs
- optional structural type when it changes meaning

Occurrence hash input must include:

- content ID
- ARK observation ID or artifact ID
- source span or structural path
- parser version

## Lifecycle

```text
ARK-preserved observation
  -> language extraction
  -> block segmentation
  -> paragraph segmentation
  -> statement segmentation
  -> Canonical English normalization
  -> dictionary lookup / append
  -> chunking
  -> validation report
  -> derived language artifact streams
```

Canonical Language artifacts are rebuildable. A rebuild with the same input,
algorithm version, and Import Profile must produce identical IDs and streams.

## Versioning

Version every deterministic algorithm boundary:

- extraction version
- segmentation version
- Canonical English version
- dictionary version
- chunking version

Breaking changes create a new version namespace. Old derived artifacts may be
rebuilt, migrated, or discarded because raw reality remains preserved by ARK.

## Canonical English

Canonical English is the deterministic normalized surface used for language
deduplication. It is not a translation, summary, or interpretation.

Rules:

- Preserve original raw text by reference; never replace it.
- Normalize Unicode compatibility forms deterministically.
- Normalize whitespace outside code blocks.
- Preserve punctuation that changes meaning.
- Normalize quotation mark variants to canonical ASCII quote characters outside
  code spans when meaning is unchanged.
- Preserve contractions as written; do not expand them.
- Lowercase dictionary words for word IDs, but preserve statement display form.
- Preserve list item boundaries as statement boundaries.
- Preserve Markdown headings, code blocks, tables, and quotes as block types.
- Preserve table row/cell boundaries before statement segmentation.
- Preserve units with numeric values.
- Normalize dates only when source format is unambiguous; otherwise preserve
  source surface and record an ambiguity issue.
- Normalize numbers only for dictionary indexing; preserve source surface in
  statement display text.

## Deterministic Versus AI Stages

Deterministic now:

- source text extraction when parser-supported
- block/paragraph/statement segmentation
- Canonical English normalization
- word and phrase dictionary construction
- statement and chunk IDs
- relationship creation between language artifacts and observations

Possible AI later:

- ambiguous OCR correction proposals
- speech transcript confidence review
- semantic clustering
- paraphrase detection
- statement-to-claim interpretation

AI must consume Canonical Statements. AI must never own normalization.

## Non-Goals

- Summarization.
- Embeddings as canonical output.
- Knowledge graph construction.
- Claim truth evaluation.
- Durable knowledge promotion.
- Source parsing that belongs inside Oracles.
