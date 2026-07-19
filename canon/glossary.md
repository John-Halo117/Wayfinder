# Canonical Glossary

This glossary is the semantic kernel of Wayfinder. It preserves One Concept, One Home by defining canonical names, ownership boundaries, aliases, deprecated terms, and cross-references.

Use this file for semantic orientation before creating new contracts, services, engines, domains, or migrations. If a concept has a more specific canonical owner, this glossary summarizes the term and points to that owner.

## Entry Template

```markdown
## Term

Status:
Canonical | Proposed | Deprecated | Alias | Engine | Capability | Contract | Service

Definition:
One or two precise sentences.

Purpose:
Why this concept exists.

Owns:
Responsibilities.

Does Not Own:
Explicit non-responsibilities.

Inputs:
Optional.

Outputs:
Optional.

Relationships:
Related canonical terms.

Examples:
Very short examples.

See Also:
Canonical owning document.
```

# Canonical Naming Rules

- One concept has one home.
- One concept has one canonical name.
- Aliases exist only for discoverability.
- Deprecated names always resolve to exactly one canonical replacement.
- No alias may point to another alias.
- Engine names are stable.
- Capability names describe outcomes rather than implementations.
- Prefer universal terminology over domain-specific terminology.
- If ownership is ambiguous, record the ambiguity instead of creating a duplicate concept.

# Glossary Entries

## Reality First

Status:
Canonical

Definition:
Reality precedes representation. Observation and evidence must exist before interpretation or durable conclusions.

Purpose:
Prevents interpretation from overwriting source truth.

Owns:
Observation order; append-only reality boundary; evidence-before-conclusion doctrine.

Does Not Own:
Derived views; policy decisions; mutable projections.

Relationships:
Observation, Evidence, Reality, Representation.

See Also:
constitution/laws.md

## Capability First

Status:
Canonical

Definition:
Capabilities are stable architectural verbs; implementations are replaceable.

Purpose:
Keeps architecture independent from temporary tooling.

Owns:
Capability names; capability ownership boundary; outcome vocabulary.

Does Not Own:
Specific implementations or vendors.

Relationships:
Capability, Service, Engine.

See Also:
constitution/laws.md

## Law of Theseus

Status:
Canonical

Definition:
Preserve capability, continuity, and objectives while replacing implementations freely.

Purpose:
Allows migration without identity loss.

Owns:
Continuity standard for replacement work.

Does Not Own:
Freezing historical implementations.

Relationships:
Continuity, Promotion, Proof.

See Also:
constitution/laws.md

## One Concept, One Home

Status:
Canonical

Definition:
Every concept has exactly one canonical owner. Other locations reference that owner.

Purpose:
Prevents semantic drift and duplicated authority.

Owns:
Canonical ownership rule; alias resolution rule.

Does Not Own:
Multiple competing definitions.

Relationships:
Canonical Naming Rules, Contract, Service, Engine.

See Also:
constitution/laws.md

## Closed Under Extension

Status:
Canonical

Definition:
Prefer extension and composition over modifying stable architectural cores.

Purpose:
Lets Wayfinder grow without destabilizing foundations.

Owns:
Extension posture; composition preference.

Does Not Own:
Unbounded abstraction or speculative layers.

Relationships:
Service, Engine, Domain.

See Also:
constitution/laws.md

## Ephemeral First

Status:
Canonical

Definition:
Default execution state is disposable unless intentionally promoted.

Purpose:
Protects durable knowledge from unproven computation.

Owns:
Working state; temporary projections; disposable caches.

Does Not Own:
Durable knowledge.

Relationships:
Ephemeral State, Proof Before Promotion, Durable Knowledge.

See Also:
constitution/laws.md

## Progressive Discovery

Status:
Canonical

Definition:
Progressive Discovery retrieves the smallest sufficient representation for the
current objective and escalates depth only when confidence is insufficient.

Purpose:
Minimizes tokens, I/O, latency, storage access, privacy exposure, and
unnecessary computation.

Owns:
Retrieval progression; bounded traversal posture; preference for indexes,
metadata, summaries, relationships, deltas, hashes, and references before full
content.

Does Not Own:
Source truth, durable knowledge, domain-specific classification rules, or a
new engine/service implementation.

Relationships:
Reality First, Ephemeral First, Proof Before Promotion, Representation,
Retrieval, Focus.

See Also:
constitution/laws.md; constitution/execution.md; docs/canonical-language/retrieval-strategy.md

## Proof Before Promotion

Status:
Canonical

Definition:
Nothing becomes durable without passing through an ephemeral proof.

Purpose:
Keeps durable knowledge evidence-backed.

Owns:
Promotion gate; proof requirement.

Does Not Own:
The promoted durable record itself.

Relationships:
Proof, Promotion, Evidence.

See Also:
constitution/laws.md

## Reality

Status:
Canonical

Definition:
Append-only canonical observations and evidence. Reality is not interpretation.

Purpose:
Provides the source boundary for preserving what happened.

Owns:
Observations; canonical evidence references; immutable record boundary.

Does Not Own:
Views, projections, recommendations, policies.

Relationships:
Observation, Evidence, Provenance.

See Also:
contracts/observations/README.md

## Observation

Status:
Contract

Definition:
A recorded encounter with reality before interpretation.

Purpose:
Captures what was seen, received, measured, or asserted.

Owns:
Observation language; observation identity; observation metadata.

Does Not Own:
Conclusion, projection, policy decision.

Relationships:
Reality, Evidence, Provenance.

See Also:
contracts/observations/README.md

## Representation

Status:
Canonical

Definition:
A model, view, projection, or encoding of reality. It is downstream from observation.

Purpose:
Makes reality usable without replacing it.

Owns:
Represented form; mapping to source evidence.

Does Not Own:
Source truth.

Relationships:
Reality, View, Projection.

See Also:
contracts/views/README.md

## Evidence

Status:
Contract

Definition:
Support used to justify a claim, proof, or promotion.

Purpose:
Connects conclusions to observations and sources.

Owns:
Evidence vocabulary; support references; confidence support.

Does Not Own:
The promoted conclusion.

Relationships:
Observation, Proof, Promotion.

See Also:
contracts/evidence/README.md

## Provenance

Status:
Contract

Definition:
Lineage that records where something came from and how it was produced.

Purpose:
Maintains traceability across transformations and promotions.

Owns:
Source, method, lineage, derivation language.

Does Not Own:
Validation outcome.

Relationships:
Evidence, Asset, Promotion.

See Also:
contracts/provenance/README.md

## RID

Status:
Contract

Definition:
Reality Identifier: a canonical identifier for a Wayfinder identity or reality-backed entity.

Purpose:
Provides stable reference across engines and services.

Owns:
Identifier language; canonical identity reference.

Does Not Own:
Identity storage implementation.

Relationships:
Identity, Asset, Observation.

See Also:
contracts/identities/README.md

## Asset

Status:
Contract

Definition:
A durable or referenceable thing under Wayfinder attention.

Purpose:
Lets systems refer to entities consistently.

Owns:
Asset language; asset identity; asset metadata boundary.

Does Not Own:
Domain-specific behavior of the asset.

Relationships:
RID, Asset in Context, Context.

See Also:
contracts/assets/README.md

## Asset in Context

Status:
Proposed

Definition:
An asset considered within a specific situational frame.

Purpose:
Preserves that usefulness depends on context.

Owns:
Relationship between asset, context, constraints, and affordances.

Does Not Own:
The asset globally.

Relationships:
Asset, Context, Affordance.

See Also:
contracts/assets/README.md

## Context

Status:
Canonical

Definition:
The bounded situation in which an asset, observation, decision, or route is evaluated.

Purpose:
Prevents universal claims from hiding local assumptions.

Owns:
Situational frame; relevant constraints and relationships.

Does Not Own:
Reality itself.

Relationships:
Constraint, Bearing, Asset in Context.

See Also:
docs/classification.md

## Constraint

Status:
Canonical

Definition:
A boundary that limits possible actions, interpretations, or transformations.

Purpose:
Makes planning and reasoning explicit.

Owns:
Limits; requirements; disallowed moves.

Does Not Own:
Policy evaluation unless formalized as Policy.

Relationships:
Policy, Tradeoff Surface, Route.

See Also:
contracts/policies/README.md

## Affordance

Status:
Canonical

Definition:
An available action or transformation made possible by an asset in context.

Purpose:
Supports capability navigation and transformation planning.

Owns:
Action possibility vocabulary.

Does Not Own:
Executing the action.

Relationships:
Capability, Transformation Opportunity, Asset in Context.

See Also:
contracts/capabilities/README.md

## Capability

Status:
Capability

Definition:
A stable architectural verb describing an outcome Wayfinder can pursue.

Purpose:
Separates what can be done from how it is implemented.

Owns:
Outcome language; capability grammar.

Does Not Own:
Implementation, runtime infrastructure.

Relationships:
Capability First, Service, Engine.

See Also:
contracts/capabilities/README.md

## Continuity

Status:
Canonical

Definition:
Preservation of identity, objective, and usable history across change.

Purpose:
Allows systems and work to survive replacement.

Owns:
Continuity standard; long-term thread preservation.

Does Not Own:
Exact implementation preservation.

Relationships:
Law of Theseus, Capsule, Durable Knowledge.

See Also:
WAYFINDER.md

## Attention

Status:
Capability

Definition:
A cross-cutting capability for selecting what deserves limited cognitive or operational focus.

Purpose:
Protects scarce focus and prioritizes action.

Owns:
Focus allocation language.

Does Not Own:
Owning all navigation or planning.

Relationships:
Bearing, Capability, Jarvis.

See Also:
contracts/capabilities/README.md

## Maneuverability

Status:
Canonical

Definition:
The ability to preserve useful options under uncertainty and constraint.

Purpose:
Keeps Wayfinder capable of changing course.

Owns:
Option preservation; route flexibility.

Does Not Own:
Guaranteeing success.

Relationships:
Navigation, Tradeoff Surface, Uncertainty.

See Also:
WAYFINDER.md

## Uncertainty

Status:
Canonical

Definition:
Known or unknown lack of confidence, completeness, or stability.

Purpose:
Keeps reasoning honest under incomplete reality.

Owns:
Uncertainty vocabulary; confidence boundary.

Does Not Own:
Evidence or proof by itself.

Relationships:
Proof, Evidence, Expected Uncertainty Reduction.

See Also:
contracts/evidence/README.md

## Proof

Status:
Canonical

Definition:
A validation artifact that justifies promotion from ephemeral to durable state.

Purpose:
Prevents unvalidated durability.

Owns:
Validation result; confidence; criteria satisfaction.

Does Not Own:
The durable promoted object.

Relationships:
Promotion, Evidence, Ephemeral State.

See Also:
contracts/promotion/README.md

## Promotion

Status:
Contract

Definition:
The act of making proven information durable in its canonical owner.

Purpose:
Controls durable knowledge creation.

Owns:
Promotion language; proof reference; rollback language.

Does Not Own:
Discovery or extraction by itself.

Relationships:
Proof, Durable Knowledge, Service.

See Also:
contracts/promotion/README.md

## Ephemeral State

Status:
Canonical

Definition:
Disposable working state used for computation, recognition, simulation, or projection.

Purpose:
Keeps unproven work from becoming durable accidentally.

Owns:
Temporary state; derived caches; simulations.

Does Not Own:
Canonical knowledge.

Relationships:
Ephemeral First, Proof, Projection.

See Also:
constitution/laws.md

## Durable Knowledge

Status:
Canonical

Definition:
Knowledge intentionally promoted into a canonical owner after proof.

Purpose:
Provides reliable continuity.

Owns:
Promoted records; durable ownership.

Does Not Own:
Unvalidated working memory.

Relationships:
Promotion, Proof, One Concept One Home.

See Also:
docs/promotion-registry.md

## Bearing

Status:
Contract

Definition:
A navigational orientation that indicates direction, confidence, and action relevance.

Purpose:
Supports choice under uncertainty.

Owns:
Bearing language; route orientation.

Does Not Own:
Executing plans.

Relationships:
Navigation, Route, Jarvis.

See Also:
contracts/bearings/README.md

## Operational Band

Status:
Proposed

Definition:
The action-oriented layer of navigation concerned with feasible execution.

Purpose:
Separates doing from knowing.

Owns:
Operational constraints and choices.

Does Not Own:
Epistemic confidence model.

Relationships:
Epistemic Band, Route.

See Also:
contracts/bearings/README.md

## Epistemic Band

Status:
Proposed

Definition:
The knowledge-oriented layer of navigation concerned with confidence and uncertainty.

Purpose:
Separates knowing from doing.

Owns:
Uncertainty and evidence posture.

Does Not Own:
Execution implementation.

Relationships:
Operational Band, Expected Uncertainty Reduction.

See Also:
contracts/evidence/README.md

## Bearings Economy

Status:
Proposed

Definition:
The trade space of maintaining useful bearings under attention limits.

Purpose:
Makes orientation maintenance cost visible.

Owns:
Bearing value and cost vocabulary.

Does Not Own:
Planning engine implementation.

Relationships:
Bearing Maintenance Cost, Attention.

See Also:
contracts/bearings/README.md

## Bearing Maintenance Cost

Status:
Proposed

Definition:
The ongoing cost of keeping a bearing accurate and useful.

Purpose:
Prevents stale orientation from appearing free.

Owns:
Maintenance cost vocabulary.

Does Not Own:
The bearing itself.

Relationships:
Bearings Economy, Ambient Certainty.

See Also:
contracts/bearings/README.md

## Ambient Certainty

Status:
Proposed

Definition:
Background confidence available without active investigation.

Purpose:
Models passive navigational confidence.

Owns:
Passive certainty language.

Does Not Own:
Proof.

Relationships:
Expected Uncertainty Reduction, Attention.

See Also:
contracts/evidence/README.md

## Expected Uncertainty Reduction

Status:
Proposed

Definition:
The anticipated decrease in uncertainty from an observation, action, or route.

Purpose:
Supports attention and navigation choices.

Owns:
Expected value of information.

Does Not Own:
Actual proof outcome.

Relationships:
Uncertainty, Attention, Route.

See Also:
contracts/evidence/README.md

## Navigation

Status:
Engine

Definition:
The responsibility of orienting through options, bearings, routes, and tradeoffs.

Purpose:
Helps Wayfinder choose direction under uncertainty.

Owns:
Route selection vocabulary; bearing use.

Does Not Own:
Reality preservation or reasoning implementation.

Relationships:
Jarvis, Bearing, Route.

See Also:
engines/jarvis/README.md

## Route

Status:
Proposed

Definition:
A candidate path through actions, constraints, and expected outcomes.

Purpose:
Makes navigation actionable.

Owns:
Path vocabulary; step sequence reference.

Does Not Own:
Commitment by itself.

Relationships:
Recommendation, Tradeoff Surface.

See Also:
contracts/bearings/README.md

## Recommendation

Status:
Proposed

Definition:
A proposed route or action with supporting rationale and uncertainty.

Purpose:
Provides advisory output without claiming obligation.

Owns:
Recommendation language; rationale.

Does Not Own:
Commitment or execution.

Relationships:
Route, MICE, Jarvis.

See Also:
contracts/bearings/README.md

## Tradeoff Surface

Status:
Proposed

Definition:
The visible set of competing costs, risks, benefits, and constraints.

Purpose:
Makes navigation choices comparable.

Owns:
Tradeoff vocabulary.

Does Not Own:
Decision authority.

Relationships:
Route, Constraint, Maneuverability.

See Also:
contracts/bearings/README.md

## ZWLib

Status:
Engine

Definition:
The transformation and affordance engine.

Purpose:
Owns reusable transformation reasoning.

Owns:
Transformation paths; affordance topology; universal transformation graph.

Does Not Own:
Reality preservation or navigation.

Relationships:
Transformation, Affordance.

See Also:
engines/README.md

## Transformation

Status:
Capability

Definition:
A change from one state, form, or asset arrangement to another.

Purpose:
Makes change reasoned and reusable.

Owns:
Transformation language.

Does Not Own:
Specific engine implementation unless owned by ZWLib.

Relationships:
Transformation Path, Byproduct.

See Also:
contracts/capabilities/README.md

## Transformation Path

Status:
Proposed

Definition:
A sequence of transformations from source state to target state.

Purpose:
Supports planning and reuse of change routes.

Owns:
Transformation sequence vocabulary.

Does Not Own:
Execution.

Relationships:
Transformation, Route.

See Also:
engines/README.md

## Byproduct

Status:
Proposed

Definition:
A secondary output of a transformation.

Purpose:
Prevents useful leftovers from being invisible.

Owns:
Secondary output language.

Does Not Own:
Waste classification by itself.

Relationships:
Waste, Transformation Opportunity.

See Also:
engines/README.md

## Waste

Status:
Alias

Definition:
Deprecated as final classification; resolve to Transformation Opportunity when useful potential exists.

Purpose:
Preserves possible value in discarded material or state.

Owns:
Alias discoverability.

Does Not Own:
Canonical ownership.

Relationships:
Transformation Opportunity, Byproduct.

See Also:
canon/glossary.md

## Transformation Opportunity

Status:
Proposed

Definition:
A possible useful transformation discovered in an asset, byproduct, or context.

Purpose:
Turns latent usefulness into navigable possibility.

Owns:
Opportunity language.

Does Not Own:
Execution or guarantee of value.

Relationships:
Affordance, ZWLib.

See Also:
engines/README.md

## Universal Transformation Graph

Status:
Proposed

Definition:
A graph of assets, states, affordances, and transformation paths.

Purpose:
Supports cross-domain transformation reasoning.

Owns:
Transformation topology language.

Does Not Own:
Runtime storage backend.

Relationships:
ZWLib, Transformation Path.

See Also:
engines/README.md

## Capsule

Status:
Contract

Definition:
A continuity package that preserves context for later re-entry.

Purpose:
Maintains long-term continuity across time and interruption.

Owns:
Capsule vocabulary; continuity package language.

Does Not Own:
Generic storage or memory service.

Relationships:
Continuity, Re-entry Capability.

See Also:
contracts/capsules/README.md

## Sedimentary Capsule

Status:
Proposed

Definition:
A capsule built by accumulated layers over time.

Purpose:
Represents continuity formed through repeated deposits.

Owns:
Layered capsule language.

Does Not Own:
Temporal scheduling.

Relationships:
Capsule, Capsule Maturity.

See Also:
contracts/capsules/README.md

## Temporal Capsule

Status:
Proposed

Definition:
A capsule organized around a time boundary or re-entry moment.

Purpose:
Preserves continuity across temporal gaps.

Owns:
Time-bound capsule language.

Does Not Own:
Calendar integration.

Relationships:
Capsule, Re-entry Capability.

See Also:
contracts/capsules/README.md

## Capsule Density

Status:
Proposed

Definition:
The concentration of useful continuity information within a capsule.

Purpose:
Helps judge capsule usefulness.

Owns:
Density vocabulary.

Does Not Own:
Proof by itself.

Relationships:
Capsule Maturity, Re-entry Capability.

See Also:
contracts/capsules/README.md

## Capsule Maturity

Status:
Proposed

Definition:
The readiness of a capsule for durable reuse or re-entry.

Purpose:
Distinguishes rough continuity from reliable continuity.

Owns:
Maturity vocabulary.

Does Not Own:
Promotion decision alone.

Relationships:
Proof, Capsule Density.

See Also:
contracts/capsules/README.md

## Re-entry Capability

Status:
Capability

Definition:
The ability to resume context from a capsule with minimal loss.

Purpose:
Makes continuity operational.

Owns:
Re-entry language.

Does Not Own:
The capsule artifact itself.

Relationships:
Capsule, Continuity.

See Also:
contracts/capsules/README.md

## Repository Stack

Status:
Canonical

Definition:
The ordered Wayfinder responsibility stack from Reality through Operations.

Purpose:
Controls dependency direction.

Owns:
Layer order; placement boundary.

Does Not Own:
Runtime call graph.

Relationships:
Contract, Service, Engine.

See Also:
WAYFINDER.md

## Runtime Continuity Loop

Status:
Proposed

Definition:
The recurring runtime cycle that preserves continuity through observation, proof, promotion, and egress.

Purpose:
Connects execution to constitutional continuity.

Owns:
Loop vocabulary.

Does Not Own:
A specific engine pipeline.

Relationships:
Engine Lifecycle, Promotion.

See Also:
WAYFINDER.md

## Engine Lifecycle

Status:
Canonical

Definition:
Ingress, Reality, Ephemeral, Proof, Promotion, Core, Egress.

Purpose:
Normalizes engine execution shape.

Owns:
Lifecycle stages; engine structure.

Does Not Own:
Service implementation internals.

Relationships:
Ingress, Reality, Core, Egress.

See Also:
engines/README.md

## Contract

Status:
Contract

Definition:
Shared implementation-free language.

Purpose:
Lets services and engines communicate without duplicating concepts.

Owns:
Vocabulary; schemas; interface language.

Does Not Own:
Runtime logic.

Relationships:
Service, Engine.

See Also:
contracts/README.md

## Service

Status:
Service

Definition:
Reusable infrastructure consumed by engines and other platform components.

Purpose:
Centralizes shared implementation.

Owns:
Generic infrastructure implementation.

Does Not Own:
Unique engine responsibility.

Relationships:
Contract, Engine.

See Also:
services/README.md

## Engine

Status:
Engine

Definition:
A composition of services implementing one unique architectural responsibility.

Purpose:
Owns differentiated behavior.

Owns:
Unique responsibility; engine lifecycle.

Does Not Own:
Shared infrastructure.

Relationships:
Service, Domain.

See Also:
engines/README.md

## Domain

Status:
Canonical

Definition:
A real-world composition of engines and services.

Purpose:
Applies platform capability to practical contexts.

Owns:
Orchestration for a domain.

Does Not Own:
Infrastructure ownership.

Relationships:
Engine, External Integration.

See Also:
domains/README.md

## Internal Application

Status:
Canonical

Definition:
A Wayfinder-owned application surface.

Purpose:
Provides user or automation access to platform capabilities.

Owns:
App boundary; API/CLI/UI/workers.

Does Not Own:
Core engine responsibility.

Relationships:
Internal, Service.

See Also:
internal/README.md

## External Integration

Status:
Canonical

Definition:
An adapter boundary to a third-party or outside system.

Purpose:
Keeps replaceable systems outside core ownership.

Owns:
Integration boundary.

Does Not Own:
Canonical platform concepts.

Relationships:
External, Domain.

See Also:
external/README.md

## Operation

Status:
Canonical

Definition:
Runtime infrastructure and maintenance concern.

Purpose:
Keeps deployment and reliability separate from product behavior.

Owns:
Deployment; monitoring; backup; migration.

Does Not Own:
Engine logic.

Relationships:
Operations, Service.

See Also:
operations/README.md

## Tooling

Status:
Canonical

Definition:
Developer tooling for scaffolding, validation, migration, and maintenance.

Purpose:
Improves development without owning runtime behavior.

Owns:
Developer automation.

Does Not Own:
Platform runtime behavior.

Relationships:
Constitutional Linter.

See Also:
tooling/README.md

## Ingress

Status:
Canonical

Definition:
The engine lifecycle stage that accepts inputs.

Purpose:
Defines controlled entry into an engine.

Owns:
Input boundary.

Does Not Own:
Interpretation or durable storage.

Relationships:
Engine Lifecycle, Egress.

See Also:
engines/_template/ingress/README.md

## Egress

Status:
Canonical

Definition:
The engine lifecycle stage that emits outputs.

Purpose:
Defines controlled exit from an engine.

Owns:
Output boundary.

Does Not Own:
Internal state ownership.

Relationships:
Ingress, Engine Lifecycle.

See Also:
engines/_template/egress/README.md

## Core

Status:
Canonical

Definition:
Durable engine logic after proof and promotion.

Purpose:
Contains the engine-specific durable responsibility.

Owns:
Algorithms, workflows, state machines owned by engine.

Does Not Own:
Shared infrastructure.

Relationships:
Engine, Service.

See Also:
engines/_template/core/README.md

## View

Status:
Contract

Definition:
A representation optimized for consumption.

Purpose:
Lets users and systems inspect reality without mutating it.

Owns:
View language.

Does Not Own:
Source reality.

Relationships:
Projection, Read Model.

See Also:
contracts/views/README.md

## Projection

Status:
Canonical

Definition:
A derived representation computed from source data.

Purpose:
Makes source material queryable or inspectable.

Owns:
Derived view logic boundary.

Does Not Own:
Source observation.

Relationships:
View, Read Model.

See Also:
contracts/views/README.md

## Read Model

Status:
Canonical

Definition:
A query-oriented representation derived from canonical sources.

Purpose:
Supports efficient access without owning truth.

Owns:
Query representation.

Does Not Own:
Canonical write model or source reality.

Relationships:
Projection, View.

See Also:
contracts/views/README.md

## ARK

Status:
Engine

Definition:
The Reality Preservation engine.

Purpose:
Preserves observations, evidence, provenance, and reality graph behavior.

Owns:
Observation; evidence; provenance; reality graph; promotion logic.

Does Not Own:
Generic storage, identity, event bus, policy, or configuration services.

Relationships:
Reality, Observation, Evidence.

See Also:
engines/ark/README.md

## WEAVE

Status:
Engine

Definition:
The relationship topology engine.

Purpose:
Owns relationship structure and topology.

Owns:
Relationship topology.

Does Not Own:
Reality preservation.

Relationships:
Engine, Graph.

See Also:
engines/README.md

# First Contact Terms

## Observation Source

Status:
Canonical

Acronym:
OS (Observation Source)

Expanded Name:
Observation Source

Definition:
A source-specific producer of canonical observation-shaped records before ARK
preservation.

Purpose:
Separates source discovery and parsing from append-only reality preservation.

Owns:
Discovery, artifact classification, source-specific parsing, source validation,
provenance capture, observation emission, and explicit Source Relationship
emission.

Does Not Own:
Reality preservation, identity, topology, interpretation, reasoning,
navigation, summaries, embeddings, search, or durable knowledge.

Relationships:
Oracle, Observation, Source Relationship, ARK, Import Profile.

Aliases:
Oracle when source-specific and deterministic; integration producer when the
source is an integration boundary.

Deprecated Aliases:
Importer as source-of-truth; parser as preservation owner.

Evidence:
First Contact ChatGPT Oracle emitted 110,619 observations before ARK
preservation.

See Also:
contracts/observations/README.md

## Oracle

Status:
Alias

Acronym:
None

Expanded Name:
Oracle

Definition:
An Observation Source with deterministic, source-specific discovery,
classification, parsing, and provenance behavior.

Purpose:
Names source-specific observation producers without making them preservation
owners.

Owns:
Source-specific parser behavior and artifact handling.

Does Not Own:
ARK preservation, identity, WEAVE topology, interpretation, or navigation.

Relationships:
Observation Source, Import Profile, Provenance.

Aliases:
Observation Source.

Deprecated Aliases:
Knowledge source when used to imply promoted truth.

Evidence:
The ChatGPT Export Oracle imported a real export with zero unknown artifacts
after First Contact fixes.

See Also:
engines/ark/ingress/chatgpt_oracle/README.md

## Source Relationship

Status:
Canonical

Acronym:
SR (Source Relationship)

Expanded Name:
Source Relationship

Definition:
An explicit relationship present in source data and preserved before
interpretation.

Purpose:
Keeps source-provided structure separate from durable topology.

Owns:
Explicit source edges such as containment, reply, reference, origin,
membership, and attachment links.

Does Not Own:
Inferred topology, conceptual relationship meaning, knowledge graph behavior,
or WEAVE promotion.

Relationships:
Relationship, Observation Source, ARK, WEAVE, Provenance.

Aliases:
Explicit source edge; preserved source edge.

Deprecated Aliases:
Relationship graph; inferred relationship.

Evidence:
First Contact preserved 217,994 explicit relationships while WEAVE remained a
future topology owner.

See Also:
contracts/relationships/README.md

## Import Profile

Status:
Canonical

Acronym:
IP (Import Profile)

Expanded Name:
Import Profile

Definition:
A bounded configuration posture for one import class.

Purpose:
Keeps large imports deterministic, capped, replayable, and reviewable.

Owns:
Limits, validation posture, runtime expectations, replay expectations, and
reporting requirements.

Does Not Own:
Source repair, source semantics, storage backend selection, or observation
content.

Relationships:
Observation Source, ARK, Validation, Replay.

Aliases:
Validation profile; import limits profile.

Deprecated Aliases:
Unbounded import mode.

Evidence:
First Contact required explicit caps above the default ARK observation limit.

See Also:
constitution/execution.md

## Candidate Page

Status:
Proposed

Acronym:
CP (Candidate Page)

Expanded Name:
Candidate Page

Definition:
A bounded slice of compiler candidates prepared for governance review.

Purpose:
Preserves reviewability when candidate volume exceeds one governance batch.

Owns:
Candidate intake bounds, deterministic page identity, candidate provenance
retention, and review queue handoff.

Does Not Own:
Candidate meaning, promotion, human approval, or durable knowledge.

Relationships:
Knowledge Compiler, Knowledge Governance, Knowledge Views.

Aliases:
Review page; candidate batch page.

Deprecated Aliases:
Unbounded review batch.

Evidence:
First Contact hit 250,000 compiler candidates and a 100,000 governance
repository cap.

See Also:
engines/interpretation/knowledge_governance/README.md

## Opaque Attachment

Status:
Canonical

Acronym:
OA (Opaque Attachment)

Expanded Name:
Opaque Attachment

Definition:
A preserved attachment artifact whose bytes are retained with provenance but
not parsed by the current Observation Source.

Purpose:
Preserves attachments without pretending to understand unsupported content.

Owns:
Attachment classification, source location, hash, byte preservation, and
provenance.

Does Not Own:
OCR, transcription, embeddings, semantic extraction, or file-type inference
beyond safe source classification.

Relationships:
Asset, Artifact, Observation, Source Relationship, Provenance.

Aliases:
Preserved blob; unparsed attachment.

Deprecated Aliases:
Unknown artifact when source evidence identifies it as an attachment.

Evidence:
First Contact classified 250 `.dat` source files as attachments and normalized
700 attachment artifacts.

See Also:
engines/ark/ingress/chatgpt_oracle/docs/artifact-classification.md

## Conversation Shard

Status:
Oracle-specific

Acronym:
CS (Conversation Shard)

Expanded Name:
Conversation Shard

Definition:
A ChatGPT export conversation file using a numbered shard name such as
`conversations-000.json`.

Purpose:
Records a real ChatGPT export convention without making it universal
architecture.

Owns:
ChatGPT Oracle classification evidence.

Does Not Own:
Generic conversation ontology or non-ChatGPT parsers.

Relationships:
Oracle, Observation Source, Conversation, Export.

Aliases:
Sharded conversation export file.

Deprecated Aliases:
Metadata file when the source path matches ChatGPT conversation shard evidence.

Evidence:
First Contact observed 17 conversation shard source files.

See Also:
engines/ark/ingress/chatgpt_oracle/docs/artifact-classification.md

## Export Transcript

Status:
Oracle-specific

Acronym:
ET (Export Transcript)

Expanded Name:
Export Transcript

Definition:
A ChatGPT export transcript document such as `chat.html`.

Purpose:
Preserves transcript artifacts without forcing JSON parsing or interpretation.

Owns:
ChatGPT Oracle document classification evidence.

Does Not Own:
Conversation reconstruction, summarization, or source truth.

Relationships:
Document, Oracle, Opaque Attachment, Export.

Aliases:
Transcript document.

Deprecated Aliases:
JSON metadata when the file is `chat.html`.

Evidence:
First Contact observed `chat.html` and corrected it from JSON metadata parsing
to document preservation.

See Also:
engines/ark/ingress/chatgpt_oracle/docs/artifact-classification.md

## Capsules

Status:
Engine

Definition:
The continuity capsule engine.

Purpose:
Owns capsule behavior and continuity packages.

Owns:
Capsule creation, maturity, re-entry behavior.

Does Not Own:
Generic storage.

Relationships:
Capsule, Continuity.

See Also:
contracts/capsules/README.md

## Interpretation

Status:
Engine

Definition:
The engine responsible for turning representations into meaning candidates.

Purpose:
Separates interpretation from observation.

Owns:
Interpretive hypotheses.

Does Not Own:
Reality preservation.

Relationships:
Observation, Representation.

See Also:
engines/README.md

## Reasoning

Status:
Engine

Definition:
The engine responsible for structured inference under uncertainty.

Purpose:
Keeps reasoning distinct from reality and navigation.

Owns:
Inference; argument structure; uncertainty reasoning.

Does Not Own:
Observation storage or navigation UI.

Relationships:
Uncertainty, Proof.

See Also:
engines/README.md

## Views

Status:
Engine

Definition:
The engine responsible for user-facing and system-facing views.

Purpose:
Owns view composition without owning reality.

Owns:
View behavior; projection presentation.

Does Not Own:
Reality source records.

Relationships:
View, Projection.

See Also:
contracts/views/README.md

## Jarvis

Status:
Engine

Definition:
The Navigation engine.

Purpose:
Owns bearings, routes, and navigation behavior.

Owns:
Navigation; bearings; route recommendations.

Does Not Own:
Generic eventing, telemetry, permissions, policy, or integrations.

Relationships:
Navigation, Bearing.

See Also:
engines/jarvis/README.md

## Foundry

Status:
Engine

Definition:
The engineering and transformation support engine formerly called Forge.

Purpose:
Owns engineering workflows and implementation-generation support.

Owns:
Patch orchestration; verification gates; artifacts.

Does Not Own:
Shared identity, storage, event bus, policy, configuration.

Relationships:
Forge, Build Bible.

See Also:
engines/foundry/README.md

## Build Bible

Status:
Engine

Definition:
The canonical specification engine.

Purpose:
Owns build and specification canon where promoted.

Owns:
Canonical build specifications.

Does Not Own:
General engineering workflow.

Relationships:
Foundry.

See Also:
engines/README.md

## Sandbox

Status:
Engine

Definition:
The simulation and bounded experimentation engine.

Purpose:
Owns disposable test worlds and simulations.

Owns:
Simulation; bounded experiments.

Does Not Own:
Durable reality.

Relationships:
Ephemeral State, Proof.

See Also:
engines/README.md

## NOMAD

Status:
Engine

Definition:
The discovery engine.

Purpose:
Owns discovery behavior where not navigation-specific.

Owns:
Discovery workflows.

Does Not Own:
Navigation decisions.

Relationships:
Capability, Jarvis.

See Also:
engines/README.md

## MIDAS

Status:
Engine

Definition:
The measurement and insight sidecar engine discovered in ARK legacy.

Purpose:
Owns its unique measurement/sidecar behavior after proof.

Owns:
Measurement sidecars; primitive extraction evidence.

Does Not Own:
Generic storage or identity.

Relationships:
Measure, Engine.

See Also:
engines/README.md

## MICE

Status:
Engine

Definition:
The commitment, consensus, coordination, and accountability engine.

Purpose:
Coordinates people and agents around commitments and agreements.

Owns:
Commitments; agreements; consensus; delegation; accountability; negotiation; coordination between people and agents.

Does Not Own:
Reality preservation; planning implementation; reasoning; navigation.

Relationships:
Commitment, Recommendation, Route.

See Also:
engines/README.md

## VALOR

Status:
Engine

Definition:
The value/risk-oriented engine discovered in ARK legacy.

Purpose:
Owns VALOR-specific evaluation behavior after proof.

Owns:
VALOR core behavior.

Does Not Own:
Generic policy or measurement services.

Relationships:
Policy, Engine.

See Also:
engines/README.md

## Blackwall

Status:
Engine

Definition:
The protection/security boundary engine.

Purpose:
Owns defensive boundary behavior where promoted.

Owns:
Protection boundary behavior.

Does Not Own:
Generic permissions or cryptography services.

Relationships:
Protect, Permission.

See Also:
engines/README.md

## NetWatch

Status:
Engine

Definition:
The network observation/control engine discovered in ARK legacy.

Purpose:
Owns network-specific monitoring and response behavior.

Owns:
Network watch behavior.

Does Not Own:
Generic telemetry or event bus.

Relationships:
External Integration, Operation.

See Also:
engines/README.md

# Canonical Language Terms

## Canonical Language

Status:
Proposed

Acronym:
CL (Canonical Language)

Expanded Name:
Canonical Language

Definition:
A deterministic, rebuildable, source-agnostic language normalization and
compression substrate derived from ARK-preserved reality.

Purpose:
Gives every Oracle a shared language substrate before interpretation.

Owns:
Canonical English, Statements, Chunks, language dictionaries, structural
language relationships, and rebuild validation.

Does Not Own:
Reality, raw artifacts, durable knowledge, reasoning, navigation,
summarization, embeddings, or truth evaluation.

Relationships:
ARK, Observation, Statement, Chunk, Knowledge Compiler, Retrieval.

Aliases:
CL; language substrate.

Deprecated Aliases:
Knowledge; reality; summary layer.

Evidence:
Phase 8D Canonical Language Architecture.

See Also:
docs/canonical-language/README.md

## Canonical English

Status:
Proposed

Acronym:
CE (Canonical English)

Expanded Name:
Canonical English

Definition:
The deterministic normalized English surface used for language deduplication
and content-addressed IDs.

Purpose:
Normalizes language without losing raw source traceability.

Owns:
Whitespace normalization, safe punctuation normalization, source-preserving
case/display rules, and structural text normalization.

Does Not Own:
Translation, meaning repair, summarization, or AI correction.

Relationships:
Canonical Language, Statement, Phrase, Word.

Aliases:
Normalized English surface.

Deprecated Aliases:
Cleaned truth; summary text.

Evidence:
Phase 8D requires AI never to own normalization.

See Also:
docs/canonical-language/architecture.md

## Statement

Status:
Proposed

Acronym:
STMT (Statement)

Expanded Name:
Statement

Definition:
The primary reusable language unit: a deterministic source-derived surface unit
prepared for compiler, retrieval, and future AI consumption.

Purpose:
Provides a unit more useful than a Phrase and more precise than a Chunk.

Owns:
Statement content identity, occurrence identity, structural type, normalized
surface, and provenance links.

Does Not Own:
Truth, claim validation, promotion, or interpretation.

Relationships:
Canonical Language, Chunk, Phrase, Word, Observation.

Aliases:
Canonical Statement.

Deprecated Aliases:
Claim when truth has not been evaluated.

Evidence:
Phase 8D selected Statement as the primary reusable unit.

See Also:
docs/canonical-language/statement-architecture.md

## Chunk

Status:
Proposed

Acronym:
CHK (Chunk)

Expanded Name:
Chunk

Definition:
A bounded ordered window of Statements used for retrieval, context expansion,
and future AI input.

Purpose:
Carries enough context around Statements without becoming the primary language
identity.

Owns:
Chunk profile, ordered Statement membership, stable ordinal under profile,
content ID, occurrence ID, and retrieval context.

Does Not Own:
Raw source, truth, summary, or durable knowledge.

Relationships:
Statement, Paragraph, Message, Section, Retrieval.

Aliases:
Context window.

Deprecated Aliases:
Summary chunk.

Evidence:
Phase 8D chunk architecture.

See Also:
docs/canonical-language/chunk-architecture.md

## Canonical Dictionary

Status:
Proposed

Acronym:
CD (Canonical Dictionary)

Expanded Name:
Canonical Dictionary

Definition:
A versioned, content-addressed dictionary for canonical Words, Phrases,
Statements, and Chunks.

Purpose:
Deduplicates language and supports compression, frequency, and retrieval.

Owns:
Dictionary entry identity, occurrence references, versioning, and rebuildable
frequency indexes.

Does Not Own:
Raw source, mutable content IDs, or knowledge promotion.

Relationships:
Word Dictionary, Phrase Dictionary, Statement Dictionary, Chunk Dictionary.

Aliases:
Language dictionary.

Deprecated Aliases:
Memory store; knowledge base.

Evidence:
Phase 8D dictionary architecture.

See Also:
docs/canonical-language/dictionary-architecture.md

# Aliases and Deprecated Terms

## Forge

Status:
Alias

Definition:
Legacy name for Foundry.

Purpose:
Preserves discoverability for folded ARK/Forge source.

Owns:
Alias resolution to Foundry.

Does Not Own:
A separate engine identity.

Relationships:
Foundry.

See Also:
engines/foundry/README.md

## Digital Twin

Status:
Deprecated

Definition:
Use Representation plus Views plus domain projections.

Purpose:
Avoids importing ambiguous domain terminology as a platform concept.

Owns:
Deprecated-name resolution.

Does Not Own:
A canonical Wayfinder engine.

Relationships:
Representation, View, Projection, Domain.

See Also:
contracts/views/README.md

## Automation

Status:
Alias

Definition:
An implementation of a capability.

Purpose:
Keeps outcome language separate from execution mechanism.

Owns:
Alias discoverability.

Does Not Own:
Capability identity.

Relationships:
Capability, Internal Application, Operation.

See Also:
contracts/capabilities/README.md

## Thing

Status:
Deprecated

Definition:
Use Asset or RID-backed entity depending on context.

Purpose:
Avoids vague ownership.

Owns:
Deprecated-name resolution.

Does Not Own:
A canonical concept.

Relationships:
Asset, RID.

See Also:
contracts/assets/README.md

## Task

Status:
Deprecated

Definition:
Use Plan Step for execution sequence work or Commitment when accountability is involved.

Purpose:
Prevents one word from hiding two ownership domains.

Owns:
Ambiguity warning.

Does Not Own:
Planning or commitment behavior.

Relationships:
Route, MICE, Commitment.

See Also:
engines/README.md

## Smart Home

Status:
Deprecated

Definition:
Use External systems plus domain orchestration plus capabilities.

Purpose:
Keeps vendor/integration framing out of platform canon.

Owns:
Deprecated-name resolution.

Does Not Own:
A Wayfinder domain by itself.

Relationships:
External Integration, Domain, Capability.

See Also:
external/README.md

## Assistant

Status:
Deprecated

Definition:
An interface role, not Jarvis itself.

Purpose:
Prevents UI/persona language from owning navigation architecture.

Owns:
Interface naming warning.

Does Not Own:
Jarvis, navigation, or reasoning.

Relationships:
Internal Application, Jarvis, Navigation.

See Also:
engines/jarvis/README.md
