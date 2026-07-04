# Cross-Oracle Language Specification

Every Oracle should emit or enable enough source text and provenance for
Canonical Language to rebuild source-agnostic language artifacts.

## Oracle Requirements

Each Observation Source should provide:

- artifact classification
- raw content or raw content reference
- source path/span when available
- parser name and version
- source hash
- timestamp when present
- author/role when present
- structural metadata without interpretation

## Source Mapping

| Source | Canonical Language input | Oracle-specific behavior |
| --- | --- | --- |
| ChatGPT | Conversation, message, attachment metadata, transcript document. | Shard parsing, role preservation, attachment references. |
| Markdown | Document, heading blocks, paragraphs, lists, tables, code blocks. | Markdown block parser and frontmatter handling. |
| PDF | Document pages, text blocks, tables when deterministic extraction exists. | Page coordinate provenance and OCR confidence when needed. |
| Email | Thread, message, headers, quoted text, attachments. | MIME parsing, quote boundary preservation, thread IDs. |
| Calendar | Event fields, descriptions, attendees, recurrence text. | Time zone and recurrence preservation without inference. |
| Filesystem | Paths, file names, metadata, text documents. | Path normalization, symlink policy, permission failures. |
| OCR | Regions, lines, text, confidence, coordinates. | Confidence and bounding box provenance. |
| Speech | Transcript turns, speaker labels, timestamps, confidence. | Turn segmentation and time spans. |
| Home Assistant | Entity events and state text fields. | Entity IDs and event/state boundaries. |
| Build Bible | Specifications, requirements, decisions, examples. | Specification sections and requirement IDs. |

## Downstream Contract

The Knowledge Compiler should consume Canonical Statements, not source-specific
conversation/message/document structures.

The compiler may still reference original observations through provenance.
