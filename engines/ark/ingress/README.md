# ARK Ingress

This directory is reserved for the normalized ARK ingress layer after Phase 1 classification and proof-backed extraction.

## Universal Ingestion MVP

`universal_ingestion/` contains the Stage 2 ARK ingress implementation for the
Universal Asset Ingestion program. It implements the requested ChatGPT ZIP
ingestion slice as substrate-oriented ingestion behavior while preserving the
current Wayfinder boundary: ARK owns reality-preservation ingress, and Foundry
remains the engineering workflow engine.

Supported MVP surface:

- ChatGPT ZIP ingestion through `ChatGPTZipAdapter`
- Conversation and message normalization into observation candidates
- Deterministic cSHAKE256 RIDs with Wayfinder domain separation
- Append-only local storage under `ARK/imports`, `ARK/observations`,
  `ARK/artifacts`, and `ARK/provenance`
- Search and timeline queries over stored observations
- Frontend-independent `IngestionAPI` consumed by internal CLI and desktop
  wrappers

Compatibility note: the attached implementation request used the name Foundry
for universal ingestion. In this repository, Foundry is already canonicalized as
the engineering engine. The ingestion behavior is therefore implemented here and
linked to the Universal Asset Ingestion contracts instead of redefining Foundry.

Phase 2 adds substrate detection and folder ingestion in front of the same
append-only pipeline. The pipeline does not branch on vendor names; vendor
logic is isolated in substrate adapters such as the Conversation/ChatGPT ZIP
adapter.
