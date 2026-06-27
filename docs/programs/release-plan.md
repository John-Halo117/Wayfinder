# Release Plan

Date: 2026-06-27

This release plan maps implementation programs to target releases. Targets are planning anchors, not promises. A release may only include milestones that preserve constitutional ownership, pass verification, and update governance evidence.

## Release Map

| Release | Theme | Included Milestones | Exit Criteria |
| --- | --- | --- | --- |
| v0.1.0 | Wayfinder Constitution v1 | Constitution, contracts, governance, engine boundaries, asset model, program planning baseline | No Critical or Major constitutional issues remain. |
| v0.2.0 | Platform Substrate Proofs | Identity Service Stage 2, Event Bus Stage 2, Storage Stage 2, Configuration Stage 2, Policy Stage 2 | Foundational services have minimal implementation proofs and tests. |
| v0.3.0 | Reality Identity and Ingestion Planning | RID-M-003 through RID-M-006, UAI-M-001 through UAI-M-006 | RID model and universal ingestion pipeline contracts are specified. |
| v0.4.0 | Ingestion and ARK Integration Planning | UAI-M-007 through UAI-M-010, Runtime Kernel Program, ARK integration plan | ARK can be implemented against RID/UAI/runtime boundaries without media-specific ownership. |
| v0.5.0 | ARK Minimal Implementation | ARK consumes platform services, RID, and universal ingestion in one bounded slice | Reality preservation slice passes compatibility and behavior-preservation proofs. |
| v0.6.0 | Relationship and Interpretation Chain | WEAVE, Interpretation, Reasoning, Views planning and first slices | Derived knowledge remains evidence-backed and contract-bound. |
| v0.7.0 | Navigation and Continuity | Jarvis, Capsules, ZWLib, Foundry slices | Navigation and continuity consume proven upstream outputs. |
| v0.8.0 | Coordination, Valuation, Protection | NOMAD, MIDAS, MICE, VALOR, Blackwall, NetWatch planning and slices | Coordination and safety engines preserve upstream ownership. |
| v0.9.0 | Portfolio and Infrastructure Readiness | `wayfinder-infra` scaffold and operations proof; first domain repo program | Deployment remains replaceable and domain repos do not duplicate constitution. |
| v1.0.0 | Operational Wayfinder | End-to-end reality -> navigation -> action loop with proof and recovery | Core loop is usable, observable, recoverable, and governance-backed. |

## Current Release Position

| Area | Current State |
| --- | --- |
| Last recommended tag | v0.1.0 Wayfinder Constitution v1 |
| Current implementation track | v0.2.0 Platform Substrate Proofs |
| Active planning gate | RID-M-003 RID Model |
| Next planning gate | UAI-M-001 Pipeline Contracts |
| Next implementation proof | Storage Minimal Implementation Proof |

## Release Rules

- A release cannot include a milestone that lacks proof or verification evidence.
- A release cannot move ARK ahead of RID and Universal Asset Ingestion planning.
- A release cannot turn Docker, media pipelines, or domain repos into architecture.
- A release must update the program index, dashboard, dependency graph, roadmap, backlog, and promotion registry when relevant.
