# 04 ARK

ARK is the reality preservation engine. It preserves observations, explicit
Source Relationships, evidence, provenance, replay records, and Last Verified
Reality.

## Owns

- Append-only preservation.
- Provenance preservation.
- Replay.
- LVR.
- Preservation of explicit Source Relationships as evidence.

## Does Not Own

- Source discovery or parsing.
- Identity service implementation.
- Storage backend implementation.
- Event transport implementation.
- Durable relationship topology.
- Interpretation, reasoning, navigation, views, or actions.

## Current Implementations

- `engines/ark/ingress/reality_ingestion/`
- `engines/ark/ingress/chatgpt_oracle/`
- `engines/ark/legacy/` as preserved historical source.

## Health

Active Python dependency scan found no service-to-engine violations. ARK
ingestion consumes Identity Service and Event Bus through explicit protocols or
boundaries.

## Gaps

- Storage remains local/in-memory in active proof and duplicated in legacy.
- Source Relationships are preserved, but WEAVE topology is not implemented.
- Import Profiles are documented but not yet a shared configuration service.

