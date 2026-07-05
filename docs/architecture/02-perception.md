# 02 Perception

Perception is the boundary where external source material is noticed,
discovered, classified, and prepared for observation emission.

## Owns

- Source discovery.
- Source-specific classification.
- Safe handling of unknown artifacts.
- Parser selection and import profile selection.

## Does Not Own

- ARK preservation.
- Identity ownership.
- Relationship topology.
- Reasoning, navigation, summaries, embeddings, or knowledge promotion.

## Current Implementations

- ChatGPT Export Oracle under `engines/ark/ingress/chatgpt_oracle/`.
- Export source manifest tooling under `tooling/export_mining/`.

## Oracle Audit

| Oracle / Source | Status | Coverage | Gaps |
| --- | --- | --- | --- |
| ChatGPT Export Oracle | Active proof | conversations, metadata, attachments, relationships, unknown artifacts | richer attachment metadata and future export variants |
| Filesystem | Not implemented | planned by universal asset ingestion | acquisition and content-addressing contracts |
| Markdown/PDF | Not implemented | planned | parsers and representation boundaries |
| Gmail/Calendar | Not implemented | planned | privacy and import profiles |
| Home Assistant/Grocy/InvenTree/Nextcloud/Immich | Legacy or planned | external integration evidence exists in legacy/docs | Compatibility Layer adapters |

## Migration Path

Keep source-specific behavior in Observation Sources. Extract shared discovery,
limits, status, and adapter classification only after at least two sources need
the same behavior.

