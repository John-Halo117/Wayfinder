# Reality Identity (RID) Model

Date: 2026-06-27

This document completes `RID-M-003 RID Model` as implementation planning. It does not implement RID, change runtime behavior, or refactor ARK.

## Purpose

The RID model defines how Wayfinder plans to represent stable reality identity across assets, observations, evidence, provenance, representations, relationships, events, and future ingestion.

RID is the universal continuity anchor. It identifies an Asset or reality-backed constitutional referent, not a file, row, event, view, chunk, embedding, summary, or other representation.

## Evidence Basis

| Evidence | Finding |
| --- | --- |
| `constitution/assets.md` | RID is stable identity for an asset or reality-backed entity. |
| `contracts/identities/README.md` | RID language belongs to Identity contracts and reusable implementation belongs to Identity Service. |
| `services/identity/docs/implementation-proof.md` | Identity Service has bounded alias, namespace, lookup, merge, and health primitives. |
| `docs/reality-identity-program.md` | RID must precede Universal Asset Ingestion and full ARK implementation. |
| `engines/ark/README.md` | ARK consumes Identity Service and preserves reality; it does not own shared identity. |

## Ownership

| Concept | Owner | Rule |
| --- | --- | --- |
| RID constitutional meaning | `constitution/assets.md` | Defines what RID means. |
| RID vocabulary | `contracts/identities/` | Defines boundary language and invariants. |
| RID implementation capability | `services/identity/` | Implements reusable identity mechanics. |
| Durable identity evidence | ARK consumes Identity and preserves evidence/provenance | ARK does not own universal RID semantics. |
| Asset identity | `constitution/assets.md`, `contracts/assets/` | Asset identity remains distinct from representations. |

## RID Shape

The RID model is intentionally implementation-independent. Future encoding must preserve these logical parts:

| Part | Purpose |
| --- | --- |
| Identifier family | Distinguishes asset identity from observation, evidence, representation, relationship, event, or policy identifiers. |
| Namespace | Establishes the bounded identity domain. |
| Local key | Stable key within the namespace. |
| Optional version or lifecycle reference | Refers to identity lifecycle metadata without changing the RID's core identity. |
| Optional checksum or content reference | May support integrity but must not replace RID identity. |

The RID shape must support validation, resolution, aliases, merge, split, provenance, and future migration.

## Identifier Families

`RID-M-004 Domain Identifiers` will specify exact families. `RID-M-003` establishes the planning classification:

| Family | Meaning | Canonical Owner |
| --- | --- | --- |
| RID | Stable reality identity for an Asset or constitutional referent. | Identity Service / Identity Contracts, grounded in Asset Model |
| AST | Asset reference family. | Asset Contracts |
| OBS | Observation reference family. | Observation Contracts / ARK behavior |
| ENT | Entity candidate or extracted entity reference. | Identity/Evidence boundary until promoted |
| REL | Relationship reference family. | Relationship Contracts / WEAVE behavior |
| EVD | Evidence reference family. | Evidence Contracts / ARK proofs |
| PRV | Provenance reference family. | Provenance Contracts / ARK behavior |
| REP | Representation reference family. | Representation Contracts / Views behavior |
| EVT | Event reference family. | Event Contracts / Event Bus Service |
| CAP | Capability reference family. | Capability grammar and Capability Contracts |
| POL | Policy reference family. | Policy Contracts / Policy Service |
| PERM | Permission reference family. | Permission Contracts / Policy Service |

Only RID identifies the asset itself. Other families may refer to records, claims, observations, transformations, or boundary artifacts.

## Stability Rules

- A RID remains stable across representation changes.
- A RID remains stable across storage backends, file paths, database rows, URLs, and deployment topology.
- A RID may survive lifecycle changes such as active, deprecated, merged, retired, or unknown.
- A RID must not encode transient context as core identity.
- A RID must not encode secrets.
- A RID must not depend on a content hash alone. Content hashes can support evidence and integrity, but content is not identity.
- A RID must be resolvable through Identity Service boundaries when implementation exists.

## Merge Semantics

Two RIDs may be merged only when proof establishes that they identify the same asset.

Merge planning requirements:

- Preserve both prior RIDs as aliases or provenance references.
- Record evidence supporting the merge.
- Record confidence and uncertainty.
- Preserve rollback or split evidence.
- Do not mutate observations to pretend the merged identity always existed.

## Split Semantics

A RID may be split when proof establishes that it was over-broad or conflated multiple assets.

Split planning requirements:

- Preserve the original RID as historical evidence.
- Create or identify distinct successor RIDs.
- Attach observations, evidence, and representations to successor identities only through proof.
- Record uncertainty when evidence does not fully assign prior claims.

## Relationships To Core Concepts

| Concept | RID Relationship |
| --- | --- |
| Asset | RID identifies the Asset or constitutional referent. |
| Asset in Context | Context changes interpretation, not RID identity. |
| Observation | Observation may reference a RID but does not create durable identity without proof. |
| Evidence | Evidence supports claims about a RID. |
| Provenance | Provenance explains how Wayfinder knows claims about a RID. |
| Representation | Representation describes a RID-identified asset but is not the asset. |
| Relationship | Relationship connects RIDs without merging identity. |
| Event | Event may carry RID references but does not own identity. |
| Capability | A capability may be treated as an asset with a RID when it becomes a continuity-bearing object. |
| Capsule | Capsule may preserve continuity context around one or more RIDs. |

## Validation Requirements

Future RID implementation must validate:

- identifier family is known;
- namespace is non-empty, bounded, and allowed;
- local key is non-empty and bounded;
- RID is representation-independent;
- aliases do not collide silently;
- merge candidates have proof paths;
- split candidates preserve provenance;
- lifecycle state is explicit;
- failures return structured, testable errors.

## Failure Modes

| Failure | Meaning | Recoverable |
| --- | --- | --- |
| Unknown RID | RID cannot be resolved. | Yes |
| Invalid RID | RID shape or namespace is invalid. | Yes |
| Alias collision | Alias maps to multiple identities. | Yes |
| Merge conflict | Merge candidates conflict by type, evidence, or provenance. | Usually |
| Split uncertainty | Prior observations cannot be confidently assigned. | Yes |
| Representation confusion | A representation ID is treated as asset RID. | Yes, but must be corrected before promotion |
| Provenance gap | Identity claim lacks sufficient source or derivation evidence. | Yes |

## ARK Consumption Rules

ARK consumes RID for reality preservation. ARK must not own universal RID semantics.

ARK integration must preserve:

- observations as append-only records;
- evidence as support for RID claims;
- provenance as source and derivation trace;
- promotion as proof-gated durability;
- legacy behavior until compatibility proof exists.

## Success Criteria

`RID-M-003` is complete when:

- RID shape is planned without implementation binding.
- Identifier families are classified for `RID-M-004`.
- Stability, merge, and split semantics are explicit.
- Core concept relationships are documented.
- Validation and failure modes are documented.
- RID remains before Universal Asset Ingestion and ARK in dependency order.
- Identity ownership remains singular.
- No implementation files change.

## Next Milestone

`UAI-M-001 Pipeline Contracts` is now unblocked for planning. `RID-M-004 Domain Identifiers` remains the next deeper RID-specific milestone.
