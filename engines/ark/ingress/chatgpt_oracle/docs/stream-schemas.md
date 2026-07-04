# Observation, Provenance, And Relationship Schemas

These are implementation-local schemas for the Phase 2 Oracle streams. They are
not global Wayfinder contracts.

## Observation Schema

| Field | Meaning |
| --- | --- |
| `observation_id` | Deterministic observation identifier. |
| `timestamp` | Source timestamp when present. |
| `source` | `ChatGPT Export`. |
| `artifact_type` | Classified artifact type. |
| `original_location` | File path or JSON pointer-like source location. |
| `conversation_reference` | Source conversation ID when present. |
| `message_reference` | Source message ID when present. |
| `author` | Source author/name/role when present. |
| `role` | Source role when present. |
| `raw_content` | Uninterpreted source content. |
| `attachments` | Attachment artifact IDs referenced by the observation. |
| `metadata` | Uninterpreted source metadata and parser metadata. |
| `provenance` | Provenance record. |
| `parsing_status` | `parsed`, `preserved`, `unsupported`, or `corrupt`. |
| `confidence` | Parser confidence in structural preservation only. |

## Provenance Schema

| Field | Meaning |
| --- | --- |
| `original_file` | File containing the observation. |
| `source_file` | Canonical source file field; additive alias of `original_file`. |
| `original_path` | Exact source location. |
| `byte_offset` | Byte offset when available; currently `null`. |
| `conversation_id` | Source conversation ID when present. |
| `message_id` | Source message ID when present. |
| `attachment_id` | Source attachment ID when present. |
| `parser_name` | Parser identity. |
| `parser_version` | Parser version. |
| `import_timestamp` | Explicit or default deterministic import timestamp. |
| `source_hash` | Canonical source hash field; additive alias of `hash`. |
| `hash` | Source file or export hash. |

## Relationship Schema

| Field | Meaning |
| --- | --- |
| `relationship_id` | Deterministic relationship identifier. |
| `relationship_type` | Non-inferential relationship type. |
| `source_id` | Source observation or artifact ID. |
| `target_id` | Target observation or artifact ID. |
| `provenance` | Provenance for the relationship source. |
| `metadata` | Uninterpreted relationship metadata. |

## Relationship Types

- `artifact_originated_from_export`
- `conversation_originated_from_artifact`
- `conversation_contains_message`
- `message_replies_to_message`
- `message_references_attachment`
- `conversation_belongs_to_project`
