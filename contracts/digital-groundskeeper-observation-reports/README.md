# Digital Groundskeeper Observation Report Contract

## Purpose

Defines the observe-only report produced by Digital Groundskeeper before any maintenance action is planned or executed.

The report reduces uncertainty about digital systems while preserving user control. It separates facts from interpretations, recommendations, and unknowns so that assumptions are never presented as reality.

## Producer

Digital Groundskeeper

Exactly one program produces this contract across Digital Groundskeeper boundaries.

## Consumers

Operators, Operations workflows, ARK observation ingestion, Storage maintenance planning, Policy review, Universal Asset Ingestion, domains, and internal applications.

## Inputs

Reality, Observation, Asset in Context, RID or unresolved identity reference, Context, Evidence, Provenance, Capability, Policy boundary, Storage reference, Event reference, system metadata, timestamps, relationships, dependencies, usage signals, and uncertainty notes.

## Outputs

Observation report, facts section, interpretations section, recommendations section, unknowns section, capability impact summary, classification, evidence references, confidence statements, next-observation proposal, and approval boundary statement.

## Required Sections

| Section | Purpose |
| --- | --- |
| Facts | Records observed reality and evidence without interpretation. |
| Interpretations | Explains what facts may mean, with confidence and alternative explanations. |
| Recommendations | Proposes observe-only next steps, reversible actions, or approval-gated plans. |
| Unknowns | Records missing information, uncertainty, and the highest-value next observation. |
| Capability Impact | States which user capabilities are supported, degraded, blocked, or at risk. |
| Continuity Impact | States continuity risk, recovery risk, rollback implications, and audit trail needs. |
| Approval Boundary | States whether any proposed next step requires explicit human approval. |

## Invariants

- Observation precedes interpretation.
- Interpretation precedes action.
- Report production is observe-only by default.
- Facts must cite evidence or be marked unknown.
- Interpretations must cite facts and confidence.
- Recommendations must include expected benefit, downside, risk, rollback, and verification when they propose future action.
- Unknowns are first-class outputs, not failures to hide.
- Large, old, duplicate, or unfamiliar assets are not assumed unnecessary.
- Destructive actions require explicit approval and cannot be performed by this contract.

## Classification Language

| Classification | Meaning |
| --- | --- |
| Safe | Evidence indicates low risk and clear benefit. |
| Probably Safe | Evidence supports action, but uncertainty remains. |
| Needs Review | Human judgment is required before action. |
| Critical | Capability, continuity, recovery, or safety risk is high. |

Every classification must include evidence and reasoning.

## Recommendation Fields

Every recommendation in an observation report must include:

- Observation.
- Evidence.
- Interpretation.
- Confidence.
- Alternative explanations.
- Recommendation.
- Expected benefit.
- Potential downside.
- Required approval.
- Expected outcome.
- Risks.
- Rollback procedure.
- Verification procedure.

## Does Not Own

- Policy definition.
- Identity generation.
- Storage persistence.
- ARK reality preservation.
- Event transport.
- Configuration management.
- Media ingestion.
- Execution approval.
- Destructive cleanup.
- Runtime implementation.

## Dependencies

- [Asset Model](../../constitution/assets.md)
- [Execution Semantics](../../constitution/execution.md)
- [Observation Contract](../observations/README.md)
- [Evidence Contract](../evidence/README.md)
- [Provenance Contract](../provenance/README.md)
- [Identity Contract](../identities/README.md)
- [Policy Contract](../policies/README.md)
- [Storage Contract](../storage/README.md)
- [Universal Asset Ingestion Pipeline](../ingestion/README.md)

## Failure Conditions

Missing evidence, insufficient access, ambiguous asset identity, unclear capability impact, unresolved policy boundary, conflicting metadata, stale timestamps, unknown dependency, unverified relationship, missing rollback path, missing verification path, or destructive recommendation without approval remain explicit report gaps.

These conditions do not justify action. They produce unknowns and next-observation recommendations.

## Promotion Rules

Observation reports remain planning evidence until ARK or another canonical owner promotes specific observations, evidence, provenance, or decisions through proof. The report itself does not make facts durable by assertion.

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- System modification.
- Cleanup execution.
- Policy creation.
- Engine refactoring.
