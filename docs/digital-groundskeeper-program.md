# Digital Groundskeeper Implementation Program

Date: 2026-06-28

Digital Groundskeeper is a planned execution-agent program for preserving and improving the health, continuity, maneuverability, and navigability of digital systems.

It executes work inside Wayfinder boundaries. It does not define policy, own constitutional doctrine, or optimize computers for their own sake.

## Purpose

Observe digital reality, reduce uncertainty, preserve continuity, recover capability, and reduce attention cost for digital systems.

Digital Groundskeeper treats files, directories, applications, containers, virtual machines, git repositories, games, mod collections, AI models, documents, photos, configuration files, backups, and databases as Assets in Context.

## Scope

- Digital system observation.
- Inventory and evidence collection.
- Capability-centered assessment.
- Cleanup, repair, quarantine, archive, and recovery planning.
- Approval-gated execution.
- Verification and updated reality reporting.
- Audit trails for reversible maintenance actions.

## Non-Goals

- Defining policy.
- Replacing ARK reality preservation.
- Replacing Storage, Identity, Event Bus, Policy, or Configuration services.
- Performing destructive actions without explicit human approval.
- Treating disk space or performance as the sole optimization target.
- Inferring meaning from file names alone.

## Operating Grammar

```text
Reality
  -> Observation
  -> Inventory
  -> Interpretation
  -> Assessment
  -> Recommendations
  -> Execution Plan
  -> Approval
  -> Execution
  -> Verification
  -> Updated Reality
```

Default behavior is observe-only. Unless explicitly instructed otherwise, the agent generates a report and waits for approval before modifying the system.

## Constitutional Principles

- Observation before interpretation.
- Interpretation before action.
- Planning before execution.
- Verification after execution.
- Evidence over assumptions.
- Reversible actions over destructive actions.
- Quarantine over deletion.
- Human approval over irreversible change.

## Optimization Order

1. Capability
2. Continuity
3. Attention
4. Maneuverability

Disk space and performance matter only when they support these objectives.

## Capability Model

A capability is something the user can reliably accomplish, such as booting Windows, playing a game, developing software, recovering files, running Docker, hosting Home Assistant, performing backups, editing photos, or running AI models.

Digital assets support capabilities. Recommendations must explain which capability is supported, protected, recovered, or put at risk.

## Assessment Framework

Every observation should answer:

- What exists?
- What changed?
- Why does it matter?
- What capability does it support?
- What pressure exists?
- What uncertainty remains?

## Classification

| Classification | Meaning |
| --- | --- |
| Safe | Evidence indicates low risk and clear benefit. |
| Probably Safe | Evidence supports action, but uncertainty remains. |
| Needs Review | Human judgment is required before action. |
| Critical | Capability, continuity, or recovery risk is high. |

Every classification must explain why.

## Recommendation Contract

Every recommendation must include:

- Observation
- Evidence
- Interpretation
- Confidence
- Alternative explanations
- Recommendation
- Expected benefit
- Potential downside
- Expected outcome
- Risks
- Rollback procedure
- Verification procedure

## Execution Rules

- Never perform destructive actions without explicit approval.
- Prefer quarantine, archiving, versioning, snapshotting, and logging.
- Report uncertainty instead of inventing confidence.
- Preserve continuity when evidence is incomplete.
- Treat reducing uncertainty as valid progress.

## Dependencies

- Asset Model
- RID and Identity Service
- Universal Asset Ingestion
- Storage Service
- Policy Service
- ARK
- Event Bus
- Configuration Service
- Operations documentation

## Downstream Consumers

- Operators
- Operations workflows
- ARK observation ingestion
- Storage maintenance
- Domain repositories
- Internal applications

## Roadmap

| Milestone | Stage | Status | Purpose |
| --- | :---: | --- | --- |
| DG-M-001 Program Charter | 0 | ✅ | Record purpose, scope, grammar, boundaries, and safety posture. |
| DG-M-002 Observation Report Contract | 1 | ✅ | Define evidence-based report structure for observe-only runs. |
| DG-M-003 Inventory Contract | 1 | ✅ | Define digital asset inventory language using Asset in Context. |
| DG-M-004 Recommendation Contract | 1 | ✅ | Define recommendation fields, confidence, alternatives, risks, rollback, and verification. |
| DG-M-005 Approval Boundary | 1 | 🔄 Next | Define what requires explicit approval and how approval is recorded. |
| DG-M-006 Quarantine and Archive Plan | 1 | ⏳ | Define reversible maintenance actions without destructive cleanup. |
| DG-M-007 First Observe-Only Slice | 2 | ⏳ | Produce a bounded report without modifying the system. |
| DG-M-008 Approval-Gated Maintenance Slice | 3 | ⏳ | Execute one reversible approved maintenance action with verification. |
| DG-M-009 ARK Observation Integration Plan | 3 | ⏳ | Plan how digital-system observations can become ARK-ingress evidence. |
| DG-M-010 Operational Runbook | 4 | ⏳ | Document recurring use, rollback, verification, and audit trail practice. |

## Backlog

### DG-M-002 Observation Report Contract

Status: Complete 2026-06-28.

- Define Facts, Interpretations, Recommendations, and Unknowns sections.
- Require evidence for every interpretation.
- Require confidence and next observation for unknowns.
- Keep the contract implementation-free.
- Evidence: `contracts/digital-groundskeeper-observation-reports/README.md`.

### DG-M-003 Inventory Contract

Status: Complete 2026-06-28.

- Define files, directories, applications, containers, virtual machines, repositories, models, documents, backups, and databases as digital Assets in Context.
- Require metadata, relationships, dependencies, timestamps, usage, and evidence.
- Prohibit reasoning from names alone.
- Evidence: `contracts/digital-groundskeeper-inventories/README.md`.

### DG-M-004 Recommendation Contract

Status: Complete 2026-06-28.

- Define expected outcome, risks, rollback, verification, benefit, downside, alternatives, and confidence.
- Require capability, continuity, attention, and maneuverability assessment.
- Evidence: `contracts/digital-groundskeeper-recommendations/README.md`.

### DG-M-005 Approval Boundary

- Define destructive, reversible, quarantine, archive, snapshot, and logging boundaries.
- Require explicit approval for irreversible change.

## Success Criteria

- Uncertainty is reduced.
- User capability increases or is preserved.
- Continuity is protected.
- Maintenance burden is lowered.
- Maneuverability improves.
- Audit trail is clear.
- Changes are reversible where possible.
- User control is preserved.

## Recommended Next Milestone

DG-M-005 Approval Boundary.

Reason: observation, inventory, and recommendation language are now defined. The next basic contract is the explicit approval boundary before quarantine, archive, or execution planning.
