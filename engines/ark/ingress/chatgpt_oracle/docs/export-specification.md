# ChatGPT Export Specification

## Input Forms

The Oracle accepts:

- A ChatGPT export directory.
- A ChatGPT export zip file.
- A single export file for parser-level validation.

## Discovery Contract

The Oracle discovers every file before parsing. Discovery is bounded by
`OracleLimits.max_files` and `OracleLimits.max_file_bytes`.

Every discovered file produces a `SourceFile` entry with:

- `original_path`
- `size_bytes`
- `sha256`
- `media_type`
- `artifact_type`

Unknown files remain in the export inventory and artifact inventory. They are
reported in `unknown_artifacts.json` and preserved in `preserved_artifacts/`.

## Supported Top-Level Files

| Pattern | Artifact Type | Parser Behavior |
| --- | --- | --- |
| `conversations.json` | Conversation | Parse conversations, messages, attachments, and structural relationships. |
| `*memory*.json` | Memory | Preserve parsed JSON as raw observation. |
| `*project*.json` | Project | Preserve parsed JSON and explicit project IDs. |
| `*prompt*.json` | Prompt | Preserve parsed JSON as raw observation. |
| `user.json`, `account.json`, `*metadata*.json` | Metadata | Preserve parsed JSON as raw observation. |
| `*setting*.json`, `*config*.json` | Configuration | Preserve parsed JSON as raw observation. |
| image extensions | Image | Preserve artifact and file-level observation. |
| document extensions | Document | Preserve artifact and file-level observation. |
| `attachments/*`, `files/*` | Attachment | Preserve artifact and file-level observation. |
| anything else | Unknown | Preserve and report. |

## Non-Goals

The export specification does not define embeddings, summaries, semantic search,
reasoning, recommendations, or navigation.
