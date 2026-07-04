# Engines

Engines are compositions of services implementing unique architectural responsibilities.

Every engine owns one major responsibility. Modules never compete to become the platform.

Repository organization is independent of execution order. Engine folders are ownership homes, not steps in a pipeline.

## Canonical Engine Structure

```text
engine/
  README.md
  contracts/
  ingress/
  reality/
  ephemeral/
  proofs/
  core/
  egress/
  docs/
  tests/
  examples/
```

The structure gives each engine a common constitutional shape. It does not imply that repository topology is the execution flow.

## Constitutional Engine Index

| Engine | Purpose | Owns | Does Not Own | Inputs | Outputs |
| --- | --- | --- | --- | --- | --- |
| [ARK](ark/README.md) | Preserves reality by maintaining append-only observations, explicit Source Relationships, evidence, provenance, replay, and LVR. | Preservation, provenance, append-only reality, replay, Last Verified Reality, and source relationship preservation. | Observation discovery, parsing, storage, identity, event bus, policy, telemetry, topology, navigation, reasoning, views, or domain orchestration. | Observation-shaped records, Source Relationships, evidence, source references, proof criteria, contract language, and supporting services. | Durable reality records, provenance references, evidence records, preserved source relationships, replay outputs, and LVR. |
| [WEAVE](weave/README.md) | Maintains relationship topology among durable entities, observations, assets, and concepts. | Relationship topology, adjacency, relationship context, and connection structure. | Reality preservation, Source Relationship preservation, interpretation, reasoning, navigation decisions, or storage infrastructure. | Durable reality, identity references, evidence references, preserved Source Relationships, asset references, and context. | Relationship topology and relationship surfaces for interpretation, reasoning, views, and navigation. |
| [Capsules](capsules/README.md) | Preserves continuity packages for future re-entry. | Capsules, re-entry context, continuity bundles, capsule maturity, handoff boundaries. | Generic storage, reality preservation, navigation, or commitment ownership. | Durable knowledge, context references, state references, evidence references, objectives, and owner references. | Continuity capsules, re-entry context, handoff packages, and capsule maturity signals. |
| [Interpretation](interpretation/README.md) | Produces meaning candidates from observations, representations, and relationships. | Interpretive hypotheses, semantic candidates, ambiguity surfaces, and candidate meanings. | Reality preservation, final inference, navigation, commitments, or views. | Observations, representations, relationship topology, evidence, context, and schemas. | Interpretation candidates with uncertainty and evidence references. |
| [Reasoning](reasoning/README.md) | Evaluates interpretations and evidence to infer conclusions under uncertainty. | Inference, argument structure, contradiction handling, confidence posture, and reasoned conclusions. | Observation storage, view presentation, commitments, route choice, or action execution. | Evidence, interpretations, objectives, constraints, policies, and durable knowledge. | Reasoned conclusions, uncertainty assessments, open questions, and proof inputs. |
| [Views](views/README.md) | Presents derived representations without owning source truth. | Views, projections, read models, presentation-ready representations, and derived inspection surfaces. | Reality preservation, reasoning, interpretation, or storage backend behavior. | Durable knowledge, relationship topology, reasoned conclusions, projections, and context. | Consumable representations, projections, and read models. |
| [Jarvis](jarvis/README.md) | Navigates capabilities and routes under uncertainty. | Bearings, routes, recommendations, navigation posture, route tradeoffs, and capability navigation behavior. | Discovery registry ownership, reasoning, commitments, reality preservation, or task execution. | Objectives, capabilities, views, reasoning outputs, constraints, policies, and context. | Bearings, routes, recommendations, navigation decisions, and route proof requirements. |
| [ZWLib](zwlib/README.md) | Owns transformation and affordance reasoning. | Transformation paths, affordances, transformation opportunities, byproducts, and universal transformation graph language. | Navigation choice, action execution, storage infrastructure, or reality preservation. | Assets in context, constraints, capabilities, relationships, objectives, and evidence. | Transformation options, transformation paths, affordance maps, and opportunity surfaces. |
| [Foundry](foundry/README.md) | Owns engineering workflows with proof. | Engineering change proposals, verification gates, patch/workflow artifacts, rollback evidence, and proof-backed engineering change. | Canonical specifications, reality preservation, navigation, reusable services, or external provider ownership. | Objectives, specifications, repository context, policies, route recommendations, and capsules. | Proven engineering changes, verification artifacts, rollback evidence, and engineering outputs. |
| [Build Bible](build-bible/README.md) | Owns canonical specifications. | Canonical build specifications, promoted implementation requirements, specification continuity, and specification references. | Engineering execution, verification workflow, or runtime operation. | Promoted specifications, architectural decisions, proof references, and Foundry outputs. | Canonical specifications and build doctrine. |
| [Sandbox](sandbox/README.md) | Owns simulation and bounded experimentation. | Simulated worlds, counterfactuals, ephemeral trials, and safe exploratory scenarios. | Durable reality, commitments, production action, or promoted knowledge. | Hypotheses, constraints, context, transformation paths, and reasoned uncertainty. | Simulation results, counterfactual evidence, and proof candidates. |
| [NOMAD](nomad/README.md) | Owns discovery. | Discovered options, providers, resources, opportunities, and discovery evidence. | Navigation decisions, route selection, external system ownership, or capability language. | Capabilities, context, constraints, external references, and objectives. | Discovery candidates, provider options, and opportunity inventories. |
| [MIDAS](midas/README.md) | Owns measurement and insight sidecars. | Measurement frames, derived metrics, indicators, insight sidecars, and measurement evidence. | Telemetry infrastructure, policy decisions, reality preservation, or value judgment. | Observations, evidence, relationships, assets, and CivPhys-derived mechanics. | Measurements, indicators, sidecars, and measurement-backed evidence. |
| [MICE](mice/README.md) | Owns commitment, consensus, coordination, and accountability. | Commitments, agreements, consensus, delegation, accountability, negotiation, and human-agent coordination. | Planning, navigation, reality preservation, reasoning, or task execution. | Recommendations, identities, policies, parties, objectives, and reasoned conclusions. | Commitments, agreements, delegation records, accountability records, and consensus outcomes. |
| [VALOR](valor/README.md) | Owns value and risk evaluation. | Value assessments, risk posture, tradeoff evaluation, and objective-relative significance. | Policy enforcement, navigation, commitments, measurement, or reality preservation. | Evidence, measurements, objectives, constraints, reasoning outputs, and policies. | Value/risk assessments, tradeoff surfaces, and evaluation findings. |
| [Blackwall](blackwall/README.md) | Owns protection boundary behavior. | Threat posture, protection decisions, boundary hardening recommendations, and protection constraints. | Permission vocabulary, cryptography service behavior, operations, or policy ownership. | Assets, policies, permissions, value/risk assessments, network findings, and context. | Protection findings, protection constraints, and boundary recommendations. |
| [NetWatch](netwatch/README.md) | Owns network-specific observation and response behavior. | Network state interpretation, network findings, network response recommendations, and network watch posture. | Generic telemetry, external integration ownership, operations, or protection policy. | Network observations, health signals, external network references, and policies. | Network findings, network posture, and network response recommendations. |

## Boundary Rules

- ARK preserves what is.
- Observation Sources observe what is.
- ARK preserves what was observed.
- WEAVE relates what has been preserved.
- Interpretation proposes what it may mean.
- Reasoning evaluates what follows.
- Views present what can be seen.
- Jarvis chooses where to go.
- MICE commits who is accountable.
- Foundry changes systems with proof.
- Build Bible preserves canonical specifications.
- ZWLib maps how things can transform.
- NOMAD discovers available options.
- MIDAS measures.
- VALOR evaluates value and risk.
- Blackwall protects.
- NetWatch watches networks.
- Capsules preserve re-entry continuity.
- Sandbox explores safely.

## Dependency Rules

- Engines depend on Constitution, Contracts, Capabilities, Services, and lower or peer engine outputs expressed through contracts.
- Engines must not own shared infrastructure.
- Engines must not duplicate another engine's unique responsibility.
- Engines expose durable outputs and capabilities, not private internal state.
- If an engine boundary becomes ambiguous, record the ambiguity in governance before implementation.

## Implementation Status

Several engine folders are constitutional placeholders or legacy quarantines.
They are not implemented merely because a folder exists. First Contact
exercised ARK, Knowledge Compiler, Knowledge Governance, Knowledge Retrieval,
Knowledge Views, Identity Service, and Event Bus proofs only.
