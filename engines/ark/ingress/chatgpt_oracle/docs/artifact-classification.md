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

## Preservation Rule

Every file is preserved regardless of classification.
