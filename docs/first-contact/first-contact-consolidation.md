# Phase 8C First Contact Consolidation Report

Date: 2026-07-03
Milestone: `v0.2-first-contact`

## Objective

Align Wayfinder's Constitution, ontology, glossary, contracts, documentation,
validation posture, and existing implementation with First Contact evidence.

## Implemented Consolidation

1. Updated constitutional language for Observation Sources, ARK preservation,
   Source Relationships, Import Profiles, and private validation artifacts.
2. Added canonical ontology entries for Observation Source, Source
   Relationship, Import Profile, Candidate Page, and Opaque Attachment.
3. Updated the canonical glossary with requested terms, acronyms, aliases,
   deprecated aliases, owners, relationships, and evidence.
4. Updated contracts and ownership tables so Observation Sources produce
   observations, ARK preserves observations, and WEAVE owns durable topology.
5. Added additive provenance fields `source_file` and `source_hash` to the
   ChatGPT Oracle stream while preserving `original_file` and `hash`.
6. Updated architecture diagrams, developer guidance, repository docs, engine
   status language, and service scaffold language.
7. Documented candidate paging, candidate grouping, streaming governance intake,
   streamable event publication, and import profiles as future improvements.
8. Added First Contact debt entries with priority, owner, dependencies, and
   migration paths.
9. Added ADRs for Observation Sources, Source Relationships, Import Profiles,
   private validation outputs, and candidate paging/governance intake.
10. Produced a validation report and constitutional change log.

## Multi-Oracle Readiness

| Source | Already generalizes | Remains source-specific | Keep local |
| --- | --- | --- | --- |
| Filesystem | Observation Source role, artifact inventory, hashing, provenance, Import Profile. | Symlink policy, permission failures, incremental import semantics. | File walking and platform-specific path handling until repeated. |
| Markdown | Document preservation, provenance, source relationships for links. | Frontmatter and repository-root semantics. | Markdown parser rules until a Markdown Oracle exists. |
| PDF | Document preservation and opaque attachment posture. | Text extraction, page offsets, OCR, embedded attachments. | PDF parser and OCR policy. |
| Gmail | Observation Source, timestamps, attachments, source relationships. | API pagination, custody, scopes, thread semantics. | Provider API adapter and privacy scopes. |
| Calendar | Observation Source, time fields, source relationships. | Recurrence, time zones, attendee identity. | Calendar recurrence parser. |
| Immich | Asset and attachment preservation, provenance, hashes. | Media metadata extraction, thumbnail policy. | Media parser and preview generation. |
| Home Assistant | Observation Source boundary, event volumes, identity references. | Entity identity mapping and state-event semantics. | HA adapter rules. |
| Grocy | Structured artifact preservation. | Inventory lifecycle and domain schema mapping. | Grocy schema adapter. |
| InvenTree | Structured artifact preservation and source relationships. | Part identity, stock movements, API pagination. | InvenTree adapter rules. |
| Nextcloud | Filesystem-like document preservation. | Version history, remote custody, sharing metadata. | Remote sync adapter. |
| Build Bible | Specification and promoted knowledge contracts. | Specification extraction and promotion workflow. | Build Bible parser rules. |

## What Should Remain Local

- Source-specific naming conventions.
- Provider API pagination and authentication behavior.
- Parser heuristics that have only one source of evidence.
- Temporary validation outputs and generated observation payloads.
- Opaque attachment handling until a parser is justified.

## What Is Now Universal

- Observation Source as producer role.
- ARK as preservation authority.
- Source Relationship as explicit source evidence.
- Import Profile as bounded import posture.
- Candidate Page as bounded governance intake concept.
- Private validation artifacts remain local.

## Deferred Work

- Implement reusable Import Profiles.
- Implement Candidate Pages and grouped governance intake.
- Add streamable event publication or bounded event reporting.
- Prepare a repository simplification branch for duplicate legacy material.
- Begin Phase 9 only after review.
