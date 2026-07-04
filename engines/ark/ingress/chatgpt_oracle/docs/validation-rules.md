# Validation Rules

The Oracle reports validation issues. It does not silently repair source data.

## Rules

| Error Code | Severity | Meaning |
| --- | --- | --- |
| `UNKNOWN_ARTIFACT` | warning | File has no supported parser. |
| `JSON_FILE_LIMIT` | error | JSON file exceeds parse cap. |
| `JSON_DECODE_FAILED` | error | JSON file is not valid UTF-8. |
| `JSON_PARSE_FAILED` | error | JSON parser failed. |
| `UNKNOWN_CONVERSATIONS_SCHEMA` | error | `conversations.json` is not a list. |
| `UNKNOWN_CONVERSATION_SCHEMA` | error | Conversation entry is not an object. |
| `CONVERSATION_MAPPING_MISSING` | error | Conversation mapping is missing or invalid. |
| `CONVERSATION_NODE_INVALID` | error | Conversation node is invalid. |
| `BROKEN_MESSAGE_REFERENCE` | warning | Message parent does not resolve. |
| `BROKEN_PROJECT_REFERENCE` | warning | Conversation project ID has no parsed project artifact. |
| `BROKEN_RELATIONSHIP_SOURCE` | warning | Relationship source ID is unknown. |
| `BROKEN_RELATIONSHIP_TARGET` | warning | Relationship target ID is unknown. |
| `DUPLICATE_OBSERVATION` | error | Duplicate observation ID emitted. |
| `TIMESTAMP_INCONSISTENCY` | warning | Source timestamp order is inconsistent. |
| `MESSAGE_RELATIONSHIP_LIMIT` | error | Message relationship count exceeds configured cap. |

Numeric timestamps are normalized from seconds or milliseconds when possible.
Unrepresentable timestamp values are preserved as their original value.

## Missing Files

The Oracle cannot know which optional export files should exist for a given
account. It reports discovered files exhaustively and treats absent optional
files as absent reality, not errors.
