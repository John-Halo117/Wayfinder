# Chunk Architecture

## Purpose

Chunks are bounded windows of ordered Statements used for retrieval, context
expansion, and future AI consumption.

Chunks are not the primary unit of meaning. Statements are.

## Boundary Rules

Prefer natural boundaries in order:

1. Message
2. Section
3. Paragraph
4. Table row group
5. Transcript turn
6. Fixed statement window fallback

Never cross source artifact boundaries. Avoid crossing author/role boundaries
unless a profile explicitly allows dialogue-pair chunks.

## Size

Recommended defaults:

- minimum: 1 Statement
- target: 8 to 20 Statements
- maximum: 40 Statements or 3,000 normalized characters
- overlap: 1 to 3 Statements when using fixed windows

Profiles may tune these values for OCR, speech, email threads, or technical
documents.

## Chunk Types

- message_chunk
- section_chunk
- paragraph_chunk
- table_chunk
- transcript_chunk
- fixed_window_chunk
- metadata_chunk

## Stable Numbering

Each chunk occurrence has:

- source artifact ID
- parent observation ID
- chunk profile ID
- ordinal within parent
- ordered statement occurrence IDs

Chunk ordinal is stable only within a chunk profile version. Content ID remains
content-addressed.

## Lifecycle

```text
statements emitted
  -> chunk profile selected
  -> natural boundaries applied
  -> fallback windows created
  -> chunk IDs assigned
  -> validation issues emitted
  -> chunk indexes rebuilt
```

## Validation

Report:

- oversized chunks
- empty chunks
- broken statement references
- unstable ordinal replay
- overlap exceeding profile bounds
- cross-artifact chunk attempts
- cross-author chunks when forbidden
