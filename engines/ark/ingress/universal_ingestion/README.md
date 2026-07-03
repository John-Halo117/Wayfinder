# Universal Ingestion MVP

This module implements the first bounded ARK ingress slice for Wayfinder
Universal Asset Ingestion.

## Contract

Inputs:

- Local ChatGPT export ZIP files containing `conversations.json`
- Explicit `IngestionConfig` resource caps
- Local append-only storage root

Outputs:

- Import manifests
- Observation records
- Provenance records
- Preserved artifact records
- Search and timeline query results

Constraints:

- Runtime: O(zip entries + conversations + messages + artifacts), bounded by
  `IngestionConfig`.
- Memory: bounded by `max_json_bytes`, `max_messages`, and artifact byte caps.
- Environment: local filesystem only; no network access.
- State: append-only local state under the configured ARK storage root.

Edge cases:

- Duplicate imports return `IMPORT_ALREADY_EXISTS` and do not overwrite prior
  manifests.
- Unsupported substrates return `SUBSTRATE_UNSUPPORTED`.
- Oversized ZIPs, messages, JSON payloads, and artifacts fail fast.
- Malformed conversation entries are recorded as structured import errors when
  recoverable.

Invariants:

- Reality source artifacts are preserved separately from observations.
- Observations retain provenance back to the import and source record.
- RIDs are deterministic and domain-separated.
- Relationship discovery is limited to source-contained parent conversation
  links in this MVP; WEAVE remains the owner of broader relationship discovery.
- No embeddings, AI summarization, knowledge graph, ADR extraction, constitution
  generation, or Jarvis integration is implemented.

## ARK Check

- Loop bounds defined? yes
- Resource caps defined? yes
- State localized? yes
- Interfaces strict? yes
- Failure paths explicit? yes

## API

- `IngestionAPI.ingest("chatgpt", Path("export.zip"))`
- `IngestionAPI.search("Ambient Certainty")`
- `IngestionAPI.timeline("Living Reality Map")`
- `IngestionAPI.observations()`
- `IngestionAPI.imports()`
- `IngestionAPI.provenance(rid)`
- `IngestionAPI.artifacts()`

## CLI

```bash
python3 internal/cli/wf.py ingest chatgpt export.zip
python3 internal/cli/wf.py search "Ambient Certainty"
python3 internal/cli/wf.py timeline "Living Reality Map"
python3 internal/cli/wf.py imports
```

## Desktop

```bash
python3 internal/desktop/ingestion_workbench.py
```

## Failure Modes

```json
{
  "status": "error",
  "error_code": "INGEST_FAILED",
  "reason": "STRING",
  "context": {},
  "recoverable": true
}
```

```json
{
  "status": "error",
  "error_code": "IMPORT_ALREADY_EXISTS",
  "reason": "Import manifest already exists.",
  "context": {"import_id": "STRING"},
  "recoverable": false
}
```

## Complexity

- Ingest: O(zip entries + conversations + messages + artifacts).
- Search: O(stored observations), capped by `max_messages` and
  `max_search_results`.
- Timeline: O(stored observations log stored observations) for timestamp sort,
  capped by `max_messages`.
- Space: O(max JSON bytes + bounded observations + bounded artifacts).


## Phase 2 Substrate Architecture

Universal ingestion now accepts sources through a substrate front end before they
enter the unchanged append-only pipeline. The pipeline stores observations,
provenance, manifests, and artifacts exactly as before.

```text
Reality
  -> Substrate Detection
  -> Adapter
  -> Universal Ingestion Pipeline
  -> ARK
```

Current substrate interfaces live under `substrates/`:

- `conversation/` with a ChatGPT ZIP adapter
- `document/`
- `filesystem/`
- `media/`
- `geometry/`
- `archive/`

The non-conversation substrates currently use the generic file adapter. Future
adapters can replace that per substrate without changing the pipeline or ARK
storage code.

## Detection

`IngestionAPI.detect(path)` returns a `SubstrateDetection` record. Detection is
extension-based for ordinary files and bounded ZIP probing for archives. ChatGPT
exports are recognized by `conversations.json`.

Supported examples:

- `export.zip` with `conversations.json`: conversation / ChatGPT
- `house.stl`, `house.sh3d`: geometry
- `notes.pdf`, `notes.md`: document
- unknown files: filesystem artifact

## Folder Import

`IngestionAPI.ingest("folder", Path("~/Downloads"))` walks recursively with
`max_folder_files`, `max_folder_depth`, and per-directory entry caps. It detects
each file, dispatches to the matching adapter, and writes one import manifest.

## Artifact Registry

Artifacts are first-class append-only records in `ARK/artifacts/artifacts.jsonl`.
Lookup APIs:

- `artifact_by_rid(rid)`
- `artifacts_by_checksum(sha256)`
- `artifacts()`

## CLI

Legacy explicit substrate form remains valid:

```bash
python3 internal/cli/wf.py ingest chatgpt export.zip
```

New auto-detect and folder forms:

```bash
python3 internal/cli/wf.py ingest export.zip
python3 internal/cli/wf.py ingest folder ~/Downloads
python3 internal/cli/wf.py search "Guest House"
python3 internal/cli/wf.py timeline
```
