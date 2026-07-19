# Artifact Classification

## Artifact Types

| Type | Meaning |
| --- | --- |
| Export | The import source as a whole. |
| Conversation | ChatGPT conversation container or conversation file. |
| Message | Message node inside a conversation mapping. |
| Attachment | File or message attachment reference. |
| Image | Image file artifact. |
| Document | Document file artifact. |
| Prompt | Prompt JSON artifact. |
| Project | Project JSON artifact. |
| Memory | Memory JSON artifact. |
| Metadata | Account/user/metadata JSON artifact. |
| Configuration | Settings/configuration JSON artifact. |
| Unknown | Preserved artifact without supported parser. |

## Classification Rule

Classification uses original path and extension only. It does not infer semantic
meaning from file content beyond supported JSON parser entry points.

Observed ChatGPT export path conventions are classified as follows:

- `conversations.json` and `conversations-000.json` style shards:
  `Conversation`
- `chat.html`: `Document`
- `file_*.dat` and `file-*.dat`: `Attachment`

## Preservation Rule

Every file is preserved regardless of classification.
