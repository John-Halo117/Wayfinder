# First Contact ChatGPT Export Validation

Date: 2026-07-03
Branch: `validation/chatgpt-export-first-contact`
Foundation baseline: `v0.1-foundation`

This report records aggregate validation evidence from the first real-world
ChatGPT export import. It intentionally excludes raw conversation content,
preserved artifacts, observation payloads, and generated relationship streams.

## Source Evidence

- Export: `GPT Export.zip`
- Export SHA-256:
  `268acb20680a067a0950a4c62ea0fe6047f8fddba9386b65db4231b27c7b95fa`
- Compressed size: about 260 MB
- Expanded size: about 795 MB
- Discovered source files: 275

## Baseline Oracle Result

The foundation Oracle preserved the export but misclassified several observed
ChatGPT export conventions.

| Metric | Count |
| --- | ---: |
| Files | 275 |
| Artifacts | 276 |
| Observations | 25 |
| Relationships | 275 |
| Unknown artifacts | 250 |
| Validation issues | 251 |

Evidence-backed gaps:

- `conversations-000.json` style shards were not classified as conversations.
- `chat.html` was treated as metadata and attempted as JSON.
- `file_*.dat` and `file-*.dat` exported blobs were unknown artifacts.
- Millisecond numeric timestamps could exceed platform timestamp range when
  interpreted only as seconds.

## Implemented Minimal Corrections

- Classify `conversations-\d+.json` files as `Conversation`.
- Classify `chat.html` as `Document`.
- Classify `file_*.dat` and `file-*.dat` files as `Attachment`.
- Normalize numeric timestamps as seconds first, then milliseconds, preserving
  unrepresentable values as source strings.
- Change in-memory ARK reality storage append behavior from tuple rebuilding to
  list append while preserving tuple-returning read APIs.

The storage change was required by real export scale: ARK ingestion timed out
after 15 minutes when each append rebuilt the full preserved record tuple.

## Corrected Oracle Result

| Metric | Count |
| --- | ---: |
| Files | 275 |
| Artifacts | 2,382 |
| Observations | 110,619 |
| Relationships | 217,994 |
| Unknown artifacts | 0 |
| Validation issues | 4,560 |

Source artifact classification:

| Artifact type | Count |
| --- | ---: |
| Attachment | 250 |
| Conversation | 17 |
| Metadata | 6 |
| Document | 1 |
| Configuration | 1 |

Normalized artifact inventory:

| Artifact type | Count |
| --- | ---: |
| Conversation | 1,673 |
| Attachment | 700 |
| Metadata | 6 |
| Export | 1 |
| Configuration | 1 |
| Document | 1 |

Validation issues after correction:

| Issue | Count |
| --- | ---: |
| `TIMESTAMP_INCONSISTENCY` | 2,797 |
| `BROKEN_MESSAGE_REFERENCE` | 1,763 |

These issues are reported source-structure observations, not silent repairs.

## ARK Reality Ingestion Result

The default ARK import cap of 100,000 observations was lower than the export's
110,619 observations. First-contact validation used an explicit validation
profile with larger bounded caps:

- `max_observations`: 150,000
- `max_relationships`: 300,000
- `max_artifacts`: 10,000

| Metric | Count |
| --- | ---: |
| Input observations | 110,619 |
| Input relationships | 217,994 |
| Input artifacts | 2,382 |
| Preserved observations | 110,619 |
| Preserved relationships | 217,994 |
| Identity resolutions | 110,619 |
| Event publications | 328,614 |
| ARK validation issues | 275 |
| LVR sequence | 110,619 |

Runtime evidence:

- Load time: 23.167 seconds
- Ingestion time after storage correction: 85.893 seconds
- Maximum resident set size: 3,416,344 KB
- Replay sample: passed

ARK validation issues:

| Issue | Count |
| --- | ---: |
| `OBSERVATION_TIMESTAMP_MISSING` | 275 |

## Full Pipeline Aggregate Result

The pipeline was exercised only through constitutional boundaries. No AI
summary, embedding generation, semantic search, navigation, or human promotion
was performed.

| Stage | Status | Evidence |
| --- | --- | --- |
| Oracle | ok | 110,619 observations, 0 unknown artifacts |
| ARK | ok | All observations and relationships preserved |
| Knowledge Compiler | error | Candidate cap reached at 250,000 |
| Knowledge Governance | error | Repository candidate cap reached at 100,000 |
| Retrieval | ok | Empty durable index rebuilt and verified |
| Views | ok | Empty projections produced |

Compiler candidate counts before cap:

| Candidate type | Count |
| --- | ---: |
| adr | 912 |
| amendment | 3,138 |
| capsule | 3,406 |
| concept | 45,131 |
| contradiction | 44,596 |
| decision | 12,767 |
| duplicate | 76,162 |
| glossary | 3,192 |
| novelty | 44,887 |
| principle | 10,975 |
| todo | 4,834 |

Compiler validation issues:

| Issue | Count |
| --- | ---: |
| `CANDIDATE_LIMIT_EXCEEDED` | 1 |
| `LOW_CONFIDENCE_CANDIDATE` | 34,910 |
| `OBSERVATION_TEXT_TRUNCATED_FOR_COMPILATION` | 1 |

No governance promotions were created because no human reviewer approved real
export-derived candidates during first-contact validation.

## Constitutional Findings

- Reality was preserved before interpretation.
- Unknown export artifacts were eliminated by classification, not by dropping
  data.
- Provenance-bearing observations and relationships were emitted
  deterministically.
- ARK preserved observations and relationships without promoting knowledge.
- The Knowledge Compiler remained proposal-only and stopped at configured caps.
- Governance did not promote unreviewed export-derived knowledge.
- Retrieval and Views remained downstream projections over durable knowledge.

## Architectural Gaps Exposed

1. The default ARK observation cap is too low for this real export.
2. The Knowledge Compiler can generate too many low-confidence candidates from
   large personal exports.
3. Knowledge Governance currently expects an in-memory bounded candidate batch
   rather than paginated or streamed review input.
4. `chat.html` is preserved as a document but is not parsed into transcript
   observations.
5. Exported attachment blobs are classified and preserved, but additional
   source metadata could improve attachment-to-message traceability.

## Recommended Follow-Up

1. Add an explicit first-contact import profile for large local exports.
2. Add bounded compiler candidate pagination or grouping before governance.
3. Add a governance review queue import path that accepts candidate pages.
4. Add an optional parser for ChatGPT attachment metadata files when present.
5. Consider an optional `chat.html` transcript parser only if it provides source
   relationships not already available in conversation shards.

## Suggested ADRs

- Support sharded ChatGPT conversation exports.
- Treat exported `.dat` blobs as attachment artifacts.
- Define first-contact validation profiles for large private exports.
- Require candidate pagination between compiler and governance boundaries.

## Validation Commands

Executed successfully:

```bash
python3 -m pytest -s engines/ark/tests/test_chatgpt_oracle.py
python3 -m compileall engines/ark/ingress/chatgpt_oracle engines/ark/tests/test_chatgpt_oracle.py
python3 -m pytest -s engines/ark/tests/test_reality_ingestion.py engines/interpretation/tests/test_knowledge_compiler.py engines/interpretation/tests/test_knowledge_governance.py engines/views/tests/test_knowledge_retrieval.py engines/views/tests/test_knowledge_views.py
python3 -m compileall engines/ark/ingress/reality_ingestion engines/ark/tests/test_reality_ingestion.py
```
