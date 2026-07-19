# Phase 8B Evidence Assimilation

Date: 2026-07-03
Evidence baseline: `v0.1-foundation` plus First Contact commits on
`validation/chatgpt-export-first-contact`

This report assimilates what the first real-world ChatGPT export taught
Wayfinder. It is deliberately conservative: every finding below is grounded in
the First Contact import, repository files, existing constitutional documents,
or tracked implementation behavior. It does not propose new engines, Jarvis,
reasoning, or multi-oracle implementation.

## Evidence Sources

- First Contact audit: `docs/first-contact/chatgpt-export-validation.md`
- Local aggregate reports under `.wayfinder-validation/first-contact/reports/`
- Oracle inventories under `.wayfinder-validation/first-contact/oracle/`
- Parser and ARK fixes committed after First Contact
- Constitution, canonical glossary, contracts, services, engines, and debt docs
- Tracked repository inventory

Raw private export content, preserved artifacts, observation streams, and
relationship streams were not copied into this report.

## Repository Archaeology Report

Tracked repository shape:

| Area | Evidence |
| --- | ---: |
| Tracked files | 788 |
| Legacy or folded source files | 496 |
| Active non-legacy files | 292 |
| Exact duplicate-content groups | 67 |
| Legacy/source payload size | about 2.5 MB |

Major active subsystems:

- Constitution and canonical glossary.
- Contract set for observations, evidence, provenance, relationships, identity,
  storage, events, views, promotion, and related language.
- ARK ChatGPT Oracle and ARK reality ingestion.
- Identity and Event Bus implementation proofs.
- Knowledge Compiler, Knowledge Governance, Knowledge Retrieval, and Knowledge
  Views implementation proofs.
- Service scaffolds for storage, policy, and configuration.
- Engine scaffolds for future systems such as WEAVE, Capsules, Reasoning,
  Jarvis, NOMAD, MIDAS, VALOR, NetWatch, ZWLib, and Sandbox.

Confirmed repository debt:

- `engines/ark/legacy/` remains the largest historical source quarantine.
- `engines/foundry/legacy/` duplicates much of the Forge-origin source already
  preserved under ARK legacy.
- Many engine lifecycle subdirectories are placeholder readmes.
- The compact `constitution/glossary.md` lags the richer
  `canon/glossary.md`.
- Several contract producer tables still say ARK produces the Observation
  Contract, while the implemented pipeline and First Contact prove that Oracles
  produce observation-shaped records and ARK preserves them.

Deletion candidates, recommended only after a reviewable compatibility commit:

1. Delete exact duplicate Forge/Foundry files from `engines/ark/legacy/` once
   the Foundry copy and historical Git commit are accepted as the preservation
   source. Keep a manifest pointer in ARK legacy.
2. Collapse empty engine lifecycle readmes that contain no engine-specific
   evidence into a smaller scaffold convention, or move them to the template.
3. Remove `engines/jarvis/docs/source/` if its contents are only folded source
   metadata already preserved elsewhere.
4. Keep service scaffolds for storage, policy, and configuration, but mark them
   explicitly as pending consumer migration rather than active implementation.

No deletion should happen in Phase 8B. The recommendation is to prepare a later
repository-simplification branch with file-by-file preservation evidence.

## First Contact Lessons Learned

Confirmed assumptions:

- Reality-first architecture worked: the Oracle preserved every discovered file
  and ARK preserved all accepted observations and explicit relationships.
- Unknown artifacts should be classified, not ignored. After evidence-backed
  parser fixes, unknown artifacts fell from 250 to 0.
- Append-only preservation and deterministic IDs were sufficient for replay.
- Identity can remain external to ARK; First Contact preserved observations
  with unresolved identity rather than inventing identity.
- Retrieval indexes and Views can remain disposable downstream projections.
- Human governance correctly blocked unreviewed promotion from private export
  data.

Disproven assumptions:

- A single `conversations.json` filename is not a sufficient ChatGPT export
  assumption. Real exports may use `conversations-000.json` shards.
- File extension alone is not sufficient for all ChatGPT artifacts. Real
  exported attachments appeared as `.dat` blobs.
- Numeric timestamps cannot be assumed to be seconds; millisecond values occur.
- The default ARK observation cap of 100,000 is not enough for a single
  medium-large personal export.
- In-memory tuple rebuilding is not acceptable for append-heavy ingestion at
  110,619 observations and 217,994 relationships.
- A batch-only candidate review path is not enough for real export-scale
  compiler output.

Missing concepts demonstrated by evidence:

- `Observation Source` should be an explicit constitutional producer role.
- `Source Relationship` or equivalent wording is needed to distinguish explicit
  source-provided relationships from WEAVE-owned durable topology.
- `Import Profile` is needed as a bounded configuration concept for real-world
  local imports.
- `Candidate Page` or `Review Page` is needed for bounded governance intake.
- `Opaque Attachment` is needed as an artifact state for preserved binary blobs
  without a specialized parser.

Unnecessary concepts not supported by First Contact:

- Jarvis, Reasoning, Mission, Affordance Field, Opportunity Bundle, and
  Attention Filter were not exercised and should not be implemented before
  durable promoted knowledge exists.
- A Knowledge Graph was not required to preserve, replay, validate, compile, or
  review the export. Relationship topology can remain deferred to WEAVE.
- Embeddings were not required; deterministic lexical retrieval over promoted
  knowledge remains enough for the current proof stage.

Implementation bugs exposed:

- ChatGPT shard classification missed `conversations-\d+.json`.
- `chat.html` was incorrectly routed toward JSON metadata parsing.
- `.dat` exported blobs were unknown artifacts.
- Timestamp normalization treated large numeric values only as seconds.
- In-memory storage append complexity was quadratic.

Constitutional gaps exposed:

- Contracts do not clearly distinguish observation production from observation
  preservation.
- Relationship ownership language does not clearly separate explicit source
  relationship preservation from durable relationship topology ownership.
- The Constitution does not yet require import profiles for large private
  exports.
- Governance documentation does not yet require paginated or streamed review
  intake when candidate volume exceeds repository caps.

## Constitutional Evolution Report

Recommended constitutional changes:

| Change | Evidence | Affected documents | Migration impact |
| --- | --- | --- | --- |
| Define `Observation Source` as the producer of canonical observation-shaped records. | ChatGPT Oracle emitted 110,619 observations before ARK preservation. | `constitution/architecture.md`, `contracts/observations/README.md`, `contracts/ownership-matrix.md`, `contracts/README.md`, `canon/glossary.md` | Documentation and contract-language update only; no code change required. |
| Define ARK as the preservation authority, not the only possible observation producer. | `engines/ark/ingress/reality_ingestion/README.md` already states Observation Sources produce observations and ARK accepts them. | Same as above plus `engines/ark/README.md` | Aligns docs with implementation. |
| Add source relationship preservation rule. | ARK preserved 217,994 explicit relationships; WEAVE was not implemented. | `contracts/relationships/README.md`, `docs/system-architecture-v1.md`, `canon/glossary.md` | Clarifies that ARK may preserve source relationships without owning topology. |
| Add bounded import profile concept. | Default ARK limits blocked real export until explicit caps were supplied. | `constitution/execution.md`, ARK docs, Oracle docs | Documentation first; later config profile can be implemented. |
| Add governance intake pagination requirement. | Compiler hit 250,000 candidates; governance repository cap blocked storage at 100,000. | Governance docs, compiler docs, `docs/system-architecture-v1.md` | Future implementation change, but constitutional boundary can be documented now. |
| Add private validation artifact rule. | First Contact generated large private outputs under `.wayfinder-validation/`. | `constitution/repository.md`, `docs/developer-handbook.md` | Documentation only; `.gitignore` already protects local outputs. |

Changes not justified:

- No new engine.
- No Knowledge Graph promotion.
- No embedding requirement.
- No Jarvis or Reasoning implementation.
- No universal parser framework beyond the existing Oracle-local pattern.

## Ontology Updates

Recommended additions:

| Concept | Status | Definition | Responsibility | Non-responsibility |
| --- | --- | --- | --- | --- |
| Observation Source | Canonical | A boundary that observes external reality and emits canonical observation-shaped records. | Discovery, classification, parsing, provenance, observation emission. | Reality preservation, identity ownership, topology ownership, interpretation. |
| Source Relationship | Proposed | A relationship explicitly present in source structure and preserved before interpretation. | Preserve source-provided containment, reference, reply, origin, or membership edges. | Inferring topology, resolving conceptual meaning, building a knowledge graph. |
| Import Profile | Proposed | A bounded set of resource caps and validation expectations for one import class. | Declare file, observation, relationship, artifact, payload, and runtime caps. | Special-case source semantics or repair invalid source data. |
| Candidate Page | Proposed | A bounded slice of compiler candidates for governance review. | Preserve reviewability when candidate volume exceeds one repository batch. | Changing candidate meaning or promoting automatically. |
| Opaque Attachment | Proposed | A preserved attachment artifact whose bytes are retained but not parsed. | Preserve binary/blob source artifacts with provenance. | Interpretation, OCR, transcription, embedding, or file-type inference beyond safe classification. |

Recommended clarifications:

- `Relationship` remains the durable topology concept owned by WEAVE.
- `Source Relationship` is not a WEAVE substitute; it is ARK-preserved source
  evidence that WEAVE may later consume.
- `Observation` should remain source-neutral. ChatGPT-specific terms such as
  conversation shard and `.dat` blob belong in the ChatGPT Oracle docs.
- `Export` should be treated as an artifact aggregate, not a new engine or
  domain concept.

## Glossary Updates

Add or update:

- `Observation Source`: canonical role; aliases: Oracle, Integration when used
  as a producer.
- `Oracle`: an Observation Source with deterministic source-specific discovery
  and parsing behavior.
- `Source Relationship`: explicit relationship from source structure, preserved
  by ARK before topology interpretation.
- `Import Profile`: bounded import configuration and validation posture.
- `Candidate Page`: bounded governance input unit.
- `Opaque Attachment`: preserved unparsed attachment.
- `Conversation Shard`: ChatGPT Oracle-specific artifact, not constitutional.
- `Export Transcript`: ChatGPT Oracle-specific document artifact for
  `chat.html`.

Deprecate or constrain:

- Use `Knowledge Graph` only for future WEAVE topology outputs, not for Oracle
  or ARK preservation.
- Avoid using `relationship graph` to describe ARK source relationship
  preservation.
- Avoid using `parser framework` until at least a second Oracle proves repeated
  infrastructure need.

## Contract Updates

Observation Contract:

- Change producer language from `ARK` to `Observation Sources`.
- Define ARK as the canonical preservation consumer and durable reality
  producer.
- Preserve the invariant that observation precedes interpretation.

Relationship Contract:

- Keep WEAVE as producer of durable relationship topology.
- Add a clarification that ARK may preserve explicit source relationships as
  reality evidence without producing topology.
- Add `Source Relationship` as a non-topological input to future WEAVE.

Provenance Contract:

- Add `parser_name`, `parser_version`, `source_file`, `original_path`,
  `import_timestamp`, and `source_hash` as first-contact-proven provenance
  fields.
- Keep byte offset optional because the current parser could not provide it for
  JSON objects without unsafe custom parsing.

Promotion and Governance Contracts:

- Require candidate review intake to remain bounded and replayable.
- Add pagination/streaming as a contract expectation for large candidate sets.

Repository Contract:

- State that local validation outputs containing source artifacts must be
  ignored by Git and summarized only through privacy-safe aggregate reports.

## Parser Lessons

General improvements:

- Deterministic classification must include known export naming conventions, not
  just generic extensions.
- Numeric timestamp normalization should tolerate seconds and milliseconds.
- Unknown artifacts should be reported and preserved; classification fixes
  should reduce unknowns without dropping data.
- Parser docs should record observed source conventions immediately after real
  contact.

ChatGPT-specific logic to keep inside the Oracle:

- `conversations-\d+.json` shard recognition.
- `chat.html` treatment as a document artifact.
- `file_*.dat` and `file-*.dat` attachment classification.
- Conversation/message/project metadata traversal.

Oracle-independent logic not yet justified for extraction:

- Parser registry abstraction. Only one Oracle exists.
- Shared attachment parser. Only ChatGPT `.dat` blobs were tested.
- Shared timestamp module. The current normalization is small and local; extract
  only after a second Oracle repeats the need.

## ARK Lessons

Verified:

- Reality preservation remains append-only.
- Identity remains external and optional during preservation.
- Relationship topology remains external; ARK preserves explicit relationships
  without interpreting them.
- Storage remains replaceable behind `RealityStorage`.
- Replay remains deterministic for sampled preserved records.
- LVR advances only on observation preservation.

Boundary risks:

- ARK currently materializes complete input tuples before validation. This is
  bounded but memory-heavy for large imports.
- Event publication records are accumulated in memory. First Contact produced
  328,614 event records, which is acceptable for proof but should become
  streamable before larger imports.
- Default import limits are conservative but not realistic for medium personal
  exports.

No First Contact fix violated constitutional boundaries. The storage change
preserved the public read API and changed only append complexity.

## Knowledge Pipeline Review

Knowledge Compiler:

- Confirmed as proposal-only.
- Candidate rules are too broad for large private exports: 250,000 candidates
  were emitted before the configured cap.
- Duplicate, novelty, contradiction, and concept candidates dominate output and
  should be grouped or paginated before governance.
- The compiler should expose candidate pages or grouped summaries before any
  governance repository write.

Knowledge Governance:

- Correctly refused unreviewed promotion.
- Current repository intake is batch-bound and failed at the 100,000 candidate
  cap.
- Review views returning zero items after intake failure is predictable but not
  useful; future intake should preserve a partial bounded page with validation
  status.

Knowledge Retrieval:

- Correctly rebuilt an empty index from zero promoted knowledge.
- No evidence justifies embeddings or semantic search yet.
- The deterministic vector index remains a proof mechanism, not a requirement
  for raw import.

Knowledge Views:

- Correctly produced empty projections when no durable knowledge existed.
- Review queue views need paged candidate input before they can handle real
  export-scale compiler output.

Simplification recommendations:

1. Reduce compiler candidate noise before adding any new knowledge stages.
2. Treat retrieval and views as inactive until governance has promoted durable
   knowledge.
3. Keep deterministic lexical retrieval; do not add external embedding models.
4. Prefer candidate grouping and paging over new review engines.

## Multi-Oracle Readiness Assessment

Readiness categories:

| Source | Readiness | What generalizes | What remains missing |
| --- | --- | --- | --- |
| Filesystem | Medium | File discovery, artifact inventory, hashing, preservation, provenance. | Directory change semantics, permission errors, symlink policy, incremental import profile. |
| PDF | Medium-Low | Document artifact preservation and provenance. | Deterministic PDF parser/OCR policy; page offsets; text extraction validation. |
| Markdown | Medium | Text/document preservation; timestamp/profile concepts. | Frontmatter parsing, link relationships, repository-root provenance. |
| Gmail | Low-Medium | Observation Source contract, attachments, timestamps, relationships. | API custody, pagination, message/thread source relationships, privacy scopes. |
| Calendar | Low-Medium | Observation Source contract, event timestamps, source relationships. | Recurrence semantics, time zones, attendee identity resolution. |
| Immich | Low-Medium | Asset/attachment preservation, metadata, provenance. | Media metadata extraction, binary storage profile, privacy-safe thumbnails. |
| Home Assistant | Medium | Legacy ARK emitter evidence plus observation source boundary. | State-event import profile, entity identity mapping, event volume controls. |
| Grocy | Low | Structured artifact preservation. | Domain schema mapping, identity and inventory lifecycle semantics. |
| InvenTree | Low | Structured artifact preservation. | Inventory identity, relationship semantics, API pagination. |
| Nextcloud | Medium-Low | Filesystem-like document preservation. | Remote custody, version history, sharing metadata, incremental sync. |

Constitutional changes required before expansion:

- Observation Source producer language.
- Source Relationship clarification.
- Import Profile concept.
- Private validation output rule.

No additional Oracle implementation should start until those documentation
changes are accepted.

## Simplification Report

Simplify now by documentation:

- Mark `Observation Source` as the producer role and ARK as preservation role.
- Make source relationships explicit so WEAVE is not accidentally pulled into
  ARK ingestion.
- Add the First Contact lessons to the architectural debt register.

Simplify later by deletion:

- Remove exact duplicate Forge/Foundry files from one legacy location after
  review.
- Collapse placeholder lifecycle readmes with no unique evidence.
- Move historical engine candidates from active-looking folders to clear
  backlog status unless they have implementation proofs.

Do not simplify by merging:

- Do not merge Oracle and ARK. First Contact confirmed the boundary.
- Do not merge Compiler and Governance. First Contact confirmed that proposal
  and promotion must remain separate.
- Do not merge Retrieval and Views. Retrieval owns indexes; Views own
  projections.
- Do not merge Source Relationship and WEAVE Relationship. One preserves source
  evidence; the other owns topology.

## Technical Debt Register

| ID | Type | Evidence | Impact | Recommended repayment |
| --- | --- | --- | --- | --- |
| FC-DEBT-001 | Contract language drift | Observation contract names ARK as producer; implementation names Observation Sources as producers. | Medium | Update contract producer language. |
| FC-DEBT-002 | Relationship boundary ambiguity | ARK preserved 217,994 relationships while WEAVE owns topology. | Medium | Add source relationship clarification. |
| FC-DEBT-003 | Import cap mismatch | Default ARK cap blocked 110,619-observation export. | Medium | Add first-contact import profile. |
| FC-DEBT-004 | Compiler candidate explosion | 250,000 candidate cap reached; 34,910 low-confidence warnings. | High | Add candidate grouping/paging before governance. |
| FC-DEBT-005 | Governance batch limit | Repository rejected 250,000 candidates at 100,000 cap. | High | Add bounded candidate page intake. |
| FC-DEBT-006 | Event accumulation memory | 328,614 event publication records accumulated. | Medium | Add streamable event sink/reporting before larger imports. |
| FC-DEBT-007 | Legacy duplication | 67 exact duplicate-content groups, mostly ARK/Foundry legacy. | Medium | Delete duplicate mirror with manifest pointer after review. |
| FC-DEBT-008 | Placeholder scaffolds | Many 3-7 line lifecycle readmes with no local evidence. | Low-Medium | Collapse or template-only after architecture review. |
| FC-DEBT-009 | Glossary split | `constitution/glossary.md` is much thinner than `canon/glossary.md`. | Medium | Make one canonical glossary home and link the other. |
| FC-DEBT-010 | Opaque attachment metadata | 250 `.dat` blobs preserved; 700 attachment artifacts normalized. | Low-Medium | Parse attachment metadata files only if needed for traceability. |

## Prioritized Next Steps

1. Update constitutional and contract language for Observation Source,
   preservation, source relationships, import profiles, and private validation
   outputs.
2. Update the canonical glossary with First Contact terms and deprecations.
3. Add candidate paging/grouping design to compiler and governance docs.
4. Add First Contact debt entries to the architectural debt register.
5. Prepare a repository-simplification branch for duplicate legacy file removal,
   starting with exact Forge/Foundry duplicates.
6. Add a first-contact import profile before running another private export.
7. Only after these are reviewed, begin Phase 9 Multi-Oracle Expansion.

## Decision Summary

Reality validated the main architecture: observe, preserve, compile candidates,
govern promotion, then rebuild retrieval and views. The weakest point is not
the number of layers; it is bounded intake between compiler and governance and
language drift around who produces observations versus who preserves reality.

The strongest constitutional amendment is small: Oracles observe, ARK
preserves, Governance promotes, and relationship topology remains downstream.
