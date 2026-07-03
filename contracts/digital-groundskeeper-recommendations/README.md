# Digital Groundskeeper Recommendation Contract

## Purpose

Defines the evidence-backed maintenance recommendation artifact produced by Digital Groundskeeper after observation and inventory, before approval or execution.

A Digital Groundskeeper recommendation proposes a digital maintenance next step while preserving uncertainty, user control, rollback awareness, and verification requirements. It is not a Jarvis navigation recommendation, not a MICE commitment, and not approval to act.

## Producer

Digital Groundskeeper

Exactly one program produces this contract across Digital Groundskeeper boundaries.

## Consumers

Operators, Approval Boundary, Operations workflows, Policy review, ARK observation ingestion, Storage maintenance planning, Digital Groundskeeper execution planning, domains, and internal applications.

## Inputs

Digital Groundskeeper Observation Report, Digital Groundskeeper Inventory, Observation, Evidence, Provenance, Asset in Context, RID or unresolved identity reference, Context, Capability, Policy boundary, Storage reference, classification, unknowns, pressure, continuity impact, and operator objective.

## Outputs

Digital maintenance recommendation, recommendation classification, confidence statement, alternative explanations, expected benefit, potential downside, required approval, expected outcome, risk statement, rollback procedure, verification procedure, next-observation proposal, and execution-plan readiness status.

## Recommendation Fields

| Field | Purpose |
| --- | --- |
| Observation | States the observed condition that motivates the recommendation. |
| Evidence | Cites the inventory, report, metadata, provenance, relationships, or other support. |
| Interpretation | Explains what the evidence may mean without presenting it as fact. |
| Confidence | States confidence and why that confidence is limited or sufficient. |
| Alternative explanations | Records plausible interpretations that may change the recommendation. |
| Capability impact | States which capability is preserved, recovered, improved, or protected. |
| Continuity impact | States continuity, recovery, audit trail, or re-entry implications. |
| Recommendation | Proposes the next step. |
| Expected benefit | Explains expected improvement in capability, continuity, attention, or maneuverability. |
| Potential downside | Explains what could get worse or become less maneuverable. |
| Required approval | States whether human approval is required before action. |
| Expected outcome | Defines what should be true after approved execution. |
| Risks | Identifies data loss, capability loss, dependency breakage, security, recovery, or trust risks. |
| Rollback procedure | Defines how to reverse or recover from the proposed action when possible. |
| Verification procedure | Defines how success or failure will be checked after action. |
| Unknowns | Records remaining uncertainty and the highest-value next observation. |

## Recommendation Types

| Type | Meaning |
| --- | --- |
| Observe More | Reduce uncertainty before planning an action. |
| No Action | Preserve current state because action would not improve objectives or evidence is insufficient. |
| Quarantine | Isolate without deletion when risk exists but continuity should be preserved. |
| Archive | Move or package for lower attention cost while preserving recovery. |
| Snapshot | Capture recoverable state before a future action. |
| Repair | Restore or improve a capability with an explicit rollback path. |
| Reorganize | Improve navigability or attention cost without destroying assets. |
| Escalate | Require human review, policy review, or specialist attention. |

Recommendation types are planning language only. They do not execute work.

## Invariants

- Recommendation follows observation and inventory.
- Recommendation is not approval.
- Recommendation is not execution.
- Recommendation is not a MICE commitment.
- Recommendation does not replace Jarvis route recommendation ownership.
- Destructive action must require explicit approval.
- Quarantine, archive, snapshot, and rollback are preferred over deletion when uncertainty exists.
- Recommendations must optimize in order: capability, continuity, attention, maneuverability.
- Disk space or performance alone is not sufficient justification.
- Unknowns must be recorded rather than hidden.

## Classification Language

| Classification | Meaning |
| --- | --- |
| Safe | Evidence indicates low risk and clear benefit, and the proposed next step is non-destructive or observe-only. |
| Probably Safe | Evidence supports the recommendation, but uncertainty or reversible risk remains. |
| Needs Review | Human judgment is required before action. |
| Critical | Capability, continuity, recovery, security, or data-loss risk is high and timely review is needed. |

Classification does not authorize execution.

## Does Not Own

- Jarvis route recommendations.
- MICE commitments.
- Policy definition.
- Permission decisions.
- Approval records.
- Execution plans.
- Runtime maintenance logic.
- Storage persistence.
- Identity generation.
- ARK reality preservation.
- Cleanup or deletion.

## Dependencies

- [Asset Model](../../constitution/assets.md)
- [Execution Semantics](../../constitution/execution.md)
- [Digital Groundskeeper Observation Report Contract](../digital-groundskeeper-observation-reports/README.md)
- [Digital Groundskeeper Inventory Contract](../digital-groundskeeper-inventories/README.md)
- [Recommendation Contract](../recommendations/README.md)
- [Observation Contract](../observations/README.md)
- [Evidence Contract](../evidence/README.md)
- [Provenance Contract](../provenance/README.md)
- [Capability Contract](../capabilities/README.md)
- [Policy Contract](../policies/README.md)
- [Permission Contract](../permissions/README.md)
- [Storage Contract](../storage/README.md)

## Failure Conditions

Missing evidence, missing inventory, ambiguous identity, unclear capability impact, unresolved policy boundary, missing approval requirement, missing rollback procedure, missing verification procedure, destructive recommendation without explicit approval requirement, insufficient confidence, unrecorded alternatives, or recommendation based only on size, age, name, or apparent duplication remain explicit gaps.

Failure conditions produce Needs Review, Observe More, No Action, or Critical review recommendations. They do not authorize execution.

## Promotion Rules

Digital Groundskeeper recommendations remain planning evidence unless accepted, recorded as decision evidence, transformed into an approval record, or consumed by a later execution plan through proof.

Accepted recommendations may support MICE commitments or ARK-preserved decision evidence, but this contract does not perform that promotion.

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- System modification.
- Approval capture.
- Execution planning by itself.
- Commitments.
- Cleanup execution.
- Engine refactoring.
