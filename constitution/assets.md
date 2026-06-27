# Constitutional Asset Model

The Asset model is Wayfinder's universal object model.

Everything Wayfinder operates on should be representable as an Asset in Context: a person, organization, household, property, tool, device, document, recipe, project, capability, trust, infrastructure system, geographic region, continuity basin, or observation source.

This is a constitutional model, not an implementation model. It defines identity, context, relationship, evidence, lifecycle, CivPhys, and capability boundaries without prescribing storage, serialization, runtime behavior, or domain-specific base classes.

## Asset

An Asset is a persistent, referenceable thing under Wayfinder attention.

An Asset is not merely a file, record, document, representation, or stored row. It is the constitutional identity that may be observed, represented, related, reasoned about, transformed, governed, or acted upon.

An Asset has:

- Identity: a stable reference through a Reality Identifier.
- Persistence: continuity across observations and representations.
- Continuity: the ability to remain the same asset through change.
- Ownership: an accountable or governing relationship, when known.
- Lifecycle: existence, observation, representation, interpretation, promotion, retirement, and other state changes.

An Asset may be physical, digital, social, legal, conceptual, operational, geographic, or organizational.

## Asset In Context

An Asset in Context is an Asset interpreted under a specific set of conditions.

Context changes meaning, relevance, affordance, risk, and capability without changing the asset's identity.

Example:

- Land.
- Land inside a family trust.
- Land during a drought.
- Land under construction.

These are the same Asset under different contexts. The RID remains stable unless identity evidence proves that the asset was incorrectly identified or must be merged with another identity.

## RID

A Reality Identifier, or RID, is the stable identity reference for an asset or reality-backed entity.

A RID identifies the asset, not any particular representation of the asset. Multiple representations, observations, evidence bundles, views, or summaries may refer to the same RID.

RID semantics:

- Stable identity: a RID persists across representations and lifecycle changes.
- Evidence-bound knowledge: claims about the RID require evidence and provenance.
- Representation independence: changing a representation does not change the RID.
- Merge semantics: two RIDs may be merged only when proof establishes that they identify the same asset.
- Split semantics: if a RID was over-broad, later proof may distinguish separate assets while preserving provenance.

The Identity Service owns reusable RID implementation. The constitutional meaning of asset identity is defined here and in Identity contracts.

## Representation

A Representation describes, encodes, summarizes, renders, or projects an Asset.

Representations are not the Asset itself.

Examples of representations include:

- OCR.
- Markdown.
- Images.
- Embeddings.
- Metadata.
- Summaries.
- Projections.
- Views.

A representation may be deleted, regenerated, replaced, compressed, translated, or transformed without destroying the asset. An asset may outlive every representation of it.

## Evidence

Evidence is observation-backed support for claims about an Asset.

Evidence connects an asset claim to observation, provenance, proof, and uncertainty. Evidence does not become the asset. Evidence supports knowledge about the asset.

Relationships:

- Provenance records where evidence came from and how it was produced.
- Proof evaluates whether evidence is sufficient for promotion.
- Uncertainty records limits in confidence, completeness, or stability.
- ARK preserves evidence and reality references without turning interpretation into observation.

## Context

Context is the set of conditions under which an Asset is interpreted.

Context may include:

- Time.
- Location.
- Objective.
- Actor.
- Capability.
- Constraints.
- Policy.
- Relationship.
- Environmental conditions.
- CivPhys state.

Context changes meaning and affordance. It does not automatically change identity.

## Relationships

Relationships connect assets without merging their identities.

Canonical relationship vocabulary should remain minimal. Use existing relationship types before adding new ones.

Common constitutional relationships:

- owns.
- depends on.
- transforms into.
- located in.
- governs.
- enables.
- constrains.
- consumes.
- produces.
- represents.

Relationships may have evidence, provenance, confidence, context, and lifecycle. A relationship is not proof by itself.

## CivPhys Profile

Every Asset may expose a CivPhys profile.

A CivPhys profile describes the asset in terms of:

- Potential: what capability, reserve, or possibility the asset stores.
- Pressure: what demand, risk, incentive, constraint, or force acts on it.
- Flow: what moves through, from, to, or within it.
- Membrane: what boundaries regulate, constrain, permit, or transform flows.

Derived mechanics such as value, cost, resilience, fragility, entropy, slack, trust, or control should not be stored as primary constitutional state. They are derived from the CivPhys profile, evidence, context, and objectives.

## Capability Profile

Every Asset may expose a Capability profile.

A Capability profile may identify:

- Capabilities the asset enables.
- Capabilities the asset requires.
- Capabilities the asset constrains.
- Capabilities the asset transforms.

Capability profiles attach uniformly to all assets. A tool, person, document, trust, power system, recipe, or continuity basin can all enable, require, constrain, or transform capabilities.

## Provenance

Asset identity never depends upon provenance.

Knowledge about an asset always does.

An asset can exist even when provenance is incomplete. Wayfinder's confidence about that asset, its claims, its representations, and its relationships depends on provenance and evidence.

Provenance answers how Wayfinder knows. It does not decide what exists.

## Lifecycle

Asset lifecycle separates existence from observation and representation.

Lifecycle dimensions:

- Existence: the asset exists or existed in reality or as a constitutional object of attention.
- Observation: Wayfinder records an encounter with the asset.
- Representation: Wayfinder creates or receives a description, projection, or encoding of the asset.
- Interpretation: Wayfinder proposes meaning for observations or representations.
- Reasoning: Wayfinder evaluates claims about the asset under uncertainty.
- Promotion: Wayfinder makes proven knowledge about the asset durable.
- Deletion of representations: Wayfinder may remove a representation without deleting the asset.
- Retirement: Wayfinder may mark an asset as no longer active while preserving identity and provenance.

An asset may outlive every representation. A representation lifecycle is not the same as an asset lifecycle.

## Law Of Theseus

Assets preserve identity despite replacement of components, representations, implementations, or subsystems when constitutional invariants remain continuous.

Identity depends upon preserved constitutional invariants rather than preserved material alone.

Examples:

- A tool repaired with new parts may remain the same asset.
- A repository migrated to a new host may remain the same asset.
- A recipe rewritten in a clearer format may remain the same asset.
- A household with changing members may preserve household identity if continuity evidence supports it.

When continuity is ambiguous, Wayfinder records evidence and proof before merging or splitting identity.

## Universal Examples

| Example | Asset | Context | RID | CivPhys Profile | Capability Profile |
| --- | --- | --- | --- | --- | --- |
| Person | A human person under Wayfinder attention. | Family role, legal role, health context, project context. | Stable person RID. | Potential: skills/trust/attention; Pressure: needs/obligations; Flow: communication/care/work; Membrane: privacy/roles/consent. | Enables care, decision, communication; requires trust and attention; constrains access. |
| Recipe | A reusable preparation pattern. | Dietary goal, available ingredients, kitchen tools, family preference. | Stable recipe RID. | Potential: meal pattern; Pressure: hunger/time/diet; Flow: ingredients/process; Membrane: instructions/constraints. | Enables cooking and planning; requires ingredients/tools; transforms raw materials. |
| Homestead | A household/property system. | Season, occupancy, maintenance state, local conditions. | Stable homestead RID. | Potential: shelter/land/tools; Pressure: weather/cost/maintenance; Flow: energy/water/labor; Membrane: property boundary/routines. | Enables living, storage, production; requires upkeep; constrains access. |
| Software Repository | A continuity-bearing code/specification asset. | Project objective, branch state, review state, release state. | Stable repository RID. | Potential: code/specs/tests; Pressure: bugs/features/risk; Flow: changes/reviews/knowledge; Membrane: governance/ownership. | Enables build, change, verification; requires policy and proof; transforms requirements. |
| Family Trust | A legal and relational asset. | Beneficiaries, obligations, jurisdiction, asset holdings. | Stable trust RID. | Potential: protected assets/authority; Pressure: taxes/duties/needs; Flow: distributions/information; Membrane: trust instrument/fiduciary rules. | Enables stewardship and transfer; requires governance; constrains use. |
| Power System | An energy infrastructure asset. | Load, weather, maintenance, resilience objective. | Stable power-system RID. | Potential: stored/generated energy; Pressure: demand/outage risk; Flow: electricity/control signals; Membrane: breakers/inverters/rules. | Enables power delivery; requires monitoring; constrains dependent systems. |
| Capability | A stable outcome Wayfinder can pursue. | Provider, objective, constraints, policy, readiness. | Stable capability RID when treated as an asset. | Potential: outcome possibility; Pressure: demand/objective; Flow: invocation/result; Membrane: contracts/policy. | Enables dependent capabilities; may require services; transforms assets. |
| Continuity Basin | A preserved field of context and re-entry potential. | Project, family, property, organization, or long-term objective. | Stable basin RID. | Potential: memory/context/trust; Pressure: entropy/interruption; Flow: attention/updates; Membrane: capsules/governance/rituals. | Enables re-entry, preservation, coordination; requires evidence and maintenance. |

## Ownership

This document defines the constitutional Asset model.

Related canonical owners:

- Asset contract language: `contracts/assets/`.
- Identity and RID language: `contracts/identities/`.
- Reusable identity implementation: `services/identity/`.
- Evidence language: `contracts/evidence/`.
- Provenance language: `contracts/provenance/`.
- Capability language: `contracts/capabilities/`.
- CivPhys mechanics: `constitution/civphys.md`.
- Reality preservation behavior: `engines/ark/`.

No engine owns the universal Asset model. Engines operate on Assets in Context through their own constitutional responsibilities.
