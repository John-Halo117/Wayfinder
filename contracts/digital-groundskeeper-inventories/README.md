# Digital Groundskeeper Inventory Contract

## Purpose

Defines the observe-only inventory artifact produced by Digital Groundskeeper when digital objects are brought under Wayfinder attention as Assets in Context.

The inventory reduces uncertainty before interpretation, recommendation, approval, or execution. It records what exists, what changed, what evidence supports the record, what capability may be affected, and what remains unknown.

## Producer

Digital Groundskeeper

Exactly one program produces this contract across Digital Groundskeeper boundaries.

## Consumers

Digital Groundskeeper Observation Reports, Operators, Operations workflows, ARK observation ingestion, Storage maintenance planning, Policy review, Universal Asset Ingestion, domains, and internal applications.

## Inputs

Reality, Observation, Asset in Context, unresolved digital object reference, RID or identity uncertainty, Context, Evidence, Provenance, Capability, Storage reference, Policy boundary, Event reference, metadata, relationships, dependencies, timestamps, usage signals, integrity signals, size or capacity signals, location signals, and access signals.

## Outputs

Digital asset inventory, inventory item, evidence reference, provenance reference, context reference, identity status, representation reference, relationship candidate, dependency candidate, capability support statement, continuity risk note, pressure note, unknowns, and next-observation proposal.

## Inventory Item Fields

| Field | Purpose |
| --- | --- |
| Observed object | Names the digital object under observation without treating its name as proof. |
| Asset context | States the conditions under which the object is being assessed. |
| Identity status | Records known RID, candidate RID, alias, unresolved identity, or merge/split uncertainty. |
| Representation status | Distinguishes the asset from representations, metadata, summaries, indexes, previews, caches, and backups. |
| Evidence | Cites observations, metadata, timestamps, relationships, dependency signals, or other support. |
| Provenance | Records how the inventory fact was observed or derived. |
| Relationships | Records owns, depends on, located in, enables, constrains, consumes, produces, represents, or other canonical relationships when supported. |
| Dependencies | Records known or suspected dependency relationships and the evidence behind them. |
| Capability support | States which user capability may be supported, degraded, blocked, or put at risk. |
| Continuity impact | States whether the object affects recovery, re-entry, audit trail, rollback, or long-term continuity. |
| Pressure | Records demand, risk, scarcity, entropy, storage pressure, attention burden, or operational pressure. |
| Classification | Uses Safe, Probably Safe, Needs Review, or Critical with evidence. |
| Unknowns | Records unresolved questions and the highest-value next observation. |

## Digital Asset Examples

Inventory may describe these objects as Assets in Context when evidence supports them:

- Files.
- Directories.
- Applications.
- Containers.
- Virtual machines.
- Git repositories.
- Game installations.
- Mod collections.
- AI models.
- Documents.
- Photos.
- Configuration files.
- Backups.
- Databases.
- Logs.
- Caches.
- Generated artifacts.
- Service exports.

Examples do not create domain-specific base classes. The universal model remains Asset in Context.

## Invariants

- Inventory is observe-only by default.
- Inventory precedes interpretation and recommendation.
- A digital object's name is evidence only when corroborated; it is not proof by itself.
- Large does not mean unnecessary.
- Old does not mean obsolete.
- Duplicate does not mean safe to delete.
- Caches, previews, indexes, and generated artifacts may support capability and require context.
- Representations are not the asset itself.
- Identity remains unresolved until sufficient evidence supports a RID or identity relationship.
- Inventory does not promote facts into durable truth by assertion.
- Inventory never authorizes destructive action.

## Classification Language

| Classification | Meaning |
| --- | --- |
| Safe | Evidence indicates low risk and clear benefit for continued observation or non-destructive handling. |
| Probably Safe | Evidence supports a low-risk interpretation, but uncertainty remains. |
| Needs Review | Human judgment or more evidence is required before recommendation or action. |
| Critical | Capability, continuity, recovery, security, or data-loss risk may be high. |

Classification is about current inventory risk and uncertainty, not permission to act.

## Does Not Own

- Identity generation.
- Storage persistence.
- ARK reality preservation.
- Policy definition.
- Permission decisions.
- Event transport.
- Cleanup execution.
- Deletion decisions.
- Recommendation production.
- Approval records.
- Runtime implementation.

## Dependencies

- [Asset Model](../../constitution/assets.md)
- [Execution Semantics](../../constitution/execution.md)
- [Digital Groundskeeper Observation Report Contract](../digital-groundskeeper-observation-reports/README.md)
- [Observation Contract](../observations/README.md)
- [Evidence Contract](../evidence/README.md)
- [Provenance Contract](../provenance/README.md)
- [Identity Contract](../identities/README.md)
- [Relationship Contract](../relationships/README.md)
- [Capability Contract](../capabilities/README.md)
- [Policy Contract](../policies/README.md)
- [Storage Contract](../storage/README.md)
- [Universal Asset Ingestion Pipeline](../ingestion/README.md)

## Failure Conditions

Insufficient access, missing metadata, ambiguous identity, unsupported object type, stale or conflicting timestamps, unresolved dependency, unverified relationship, unclear capability support, unclear continuity impact, missing provenance, inaccessible storage boundary, policy uncertainty, or evidence that depends only on naming remain explicit unknowns.

Failure conditions produce next-observation proposals. They do not justify cleanup, deletion, merge, quarantine, or promotion by themselves.

## Promotion Rules

Inventory artifacts remain planning evidence until ARK or another canonical owner promotes supported observations, evidence, provenance, relationships, identities, or decisions through proof.

An inventory item may support later recommendations, approval requests, quarantine plans, archive plans, or ARK ingestion, but it does not perform those actions.

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- System scanning logic.
- Cleanup execution.
- Deletion policy.
- Recommendation generation by itself.
- Engine refactoring.
