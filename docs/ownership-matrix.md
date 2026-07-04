# Ownership Matrix

Every concept has exactly one canonical owner.

## Canonical Concepts

| Concept | Canonical Owner |
| --- | --- |
| Observation | Observation Contracts |
| Observation Source | Observation Contracts |
| Source Relationship | Relationship Contracts |
| Import Profile | Execution Semantics |
| Candidate Page | Knowledge Governance |
| Opaque Attachment | Asset Contracts and source-specific Oracle docs |
| Evidence | Evidence Contracts |
| Evidence Bundle | Evidence Contracts |
| Provenance | Provenance Contracts |
| Provenance Edge | Provenance Contracts |
| RID | Identity Contracts |
| Canonical Identity | Identity Contracts |
| Alias | Identity Contracts |
| Namespace | Identity Contracts |
| Identity Lifecycle | Identity Contracts |
| Identity Lookup | Identity Contracts |
| Identity Merge | Identity Contracts |
| Asset | Asset Contracts |
| Asset Metadata | Asset Contracts |
| Asset Lifecycle | Asset Contracts |
| Event | Event Contracts |
| Event Envelope | Event Contracts |
| Event Metadata | Event Contracts |
| Event Route | Event Contracts |
| Correlation ID | Event Contracts |
| Causation ID | Event Contracts |
| Replay Cursor | Event Contracts |
| Policy | Policy Contracts |
| Policy Rule | Policy Contracts |
| Policy Decision | Policy Contracts |
| Permission | Permission Contracts |
| Permission Scope | Permission Contracts |
| Capability | Capabilities |
| Capability Grammar | Capabilities |
| Capability Availability | Capability Contracts |
| Capability Route Language | Capability Contracts |
| Bearing | Bearing Contracts |
| Route Target | Bearing Contracts |
| View | View Contracts |
| Projection Language | View Contracts |
| Capsule | Capsule Contracts |
| Continuity Boundary | Capsule Contracts |
| Promotion | Promotion Contracts |
| Promotion Criteria | Promotion Contracts |
| Rollback Reference | Promotion Contracts |
| Health | Health Contracts |
| Readiness Status | Health Contracts |
| Dependency Status | Health Contracts |
| Schema Identifier | Schema Contracts |
| Schema Version | Schema Contracts |
| Validation Result | Schema Contracts |
| Structured Failure Model | Schema Contracts |
| Persistence | Storage |
| Storage Interface | Storage |
| Storage Backend | Storage |
| Object Storage | Storage |
| Object Metadata | Storage |
| Versioning Hook | Storage |
| Engineering Workflow | Foundry |
| Code-Change Proposal | Foundry |
| Patch Application | Foundry |
| Verification Gate | Foundry |
| Red-Team Engineering Check | Foundry |
| Engineering Artifact | Foundry |
| Forge Legacy Compatibility | Foundry |

## Boundary Rules

Contracts own language only. They do not own implementation, runtime behavior,
service adapters, engine algorithms, domain workflows, or external integration
logic.

Identity Contracts own identity language. Identity Service owns reusable identity implementation. Event Bus owns subject routing and event route semantics.

Event Contracts own event language. Event Bus owns future event transport and
routing implementation.

Storage Contracts own persistence language. Storage Service owns persistence abstraction and storage implementation boundaries.

Observation Sources own source discovery and canonical observation-shaped record
production.

ARK owns reality-preservation behavior that consumes Observation, Source
Relationship, Evidence, Provenance, Promotion, Health, Event, Identity, Asset,
Policy, Permission, Capability, View, Capsule, and Schema language.

WEAVE owns durable relationship topology. ARK-preserved Source Relationships
remain evidence until WEAVE consumes and promotes topology.

Jarvis owns navigation behavior that consumes Bearing and Capability language.

Foundry owns engineering workflow behavior that consumes Policy, Permission,
Capability, Health, View, Capsule, Event, Asset, and Schema language.

## Wave 2 Service Ownership

| Concept | Canonical Owner |
| --- | --- |
| RID Generation | Identity Service |
| Alias Resolution | Identity Service |
| Namespace Handling | Identity Service |
| Identity Lookup | Identity Service |
| Identity Merge Semantics | Identity Service |
| Publish | Event Bus |
| Subscribe | Event Bus |
| Event Routing | Event Bus |
| Correlation ID Handling | Event Bus |
| Event Replay Boundary | Event Bus |
| Persistence Abstraction | Storage Service |
| Storage Backend Boundary | Storage Service |
| Object Storage | Storage Service |
| Object Metadata | Storage Service |
| Transaction Boundary | Storage Service |
| Versioning Hooks | Storage Service |
| Configuration Loading | Configuration Service |
| Layered Configuration | Configuration Service |
| Environment Abstraction | Configuration Service |
| Configuration Defaults | Configuration Service |
| Configuration Validation | Configuration Service |
| Runtime Configuration Access | Configuration Service |
| Policy Evaluation | Policy Service |
| Rule Execution | Policy Service |
| Authorization Policy Evaluation | Policy Service |
| Promotion Policy Evaluation | Policy Service |
| Architectural Policy Evaluation | Policy Service |

## Phase 4 Implementation Ownership

| Concept | Canonical Owner |
| --- | --- |
| IdentityRecord Implementation | Identity Service |
| Alias Resolver Implementation | Identity Service |
| Identity Namespace Validator | Identity Service |
| Identity Merge Decision Implementation | Identity Service |
| Request Identity Generator | Identity Service |
| Identity Health Signal | Identity Service |
## M-002 Event Bus Implementation Ownership

| Concept | Canonical Owner |
| --- | --- |
| EventEnvelope Implementation | Event Bus Service |
| Route Pattern Matcher | Event Bus Service |
| Publish Result Implementation | Event Bus Service |
| Subscription Registry Implementation | Event Bus Service |
| Replay Cursor Implementation | Event Bus Service |
| Event Bus Health Signal | Event Bus Service |
