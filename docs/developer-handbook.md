# Wayfinder Developer Handbook

This handbook orients contributors to Wayfinder Constitution v1. It explains how to add to the repository without breaking constitutional continuity.

## What Is Wayfinder?

Wayfinder is a constitutional continuity platform for preserving reality, reasoning under uncertainty, navigating capabilities, and maintaining long-term continuity. It is organized by responsibility so implementations can change while capabilities, objectives, and continuity survive.

Wayfinder is not a single engine, application, database, or interface. It is a constitutional architecture that keeps durable knowledge, reusable services, engine boundaries, and domain composition in their proper homes.

## Constitutional Philosophy

### Reality First

Reality precedes representation. Observation precedes interpretation. Evidence precedes conclusions. Durable reality is append-only and must not be overwritten by later interpretations.

### Capability First

Capabilities are stable architectural verbs. Implementations, providers, tools, and integrations may change. The capability grammar remains durable.

### Law of Theseus

Preserve capabilities, continuity, and objectives while replacing implementations freely. Identity depends on preserved constitutional invariants, not preserved material or code.

### One Concept, One Home

Every concept has exactly one canonical owner. Other layers reference that owner instead of duplicating definitions.

### CivPhys

CivPhys is Wayfinder's constitutional mechanics layer. Its irreducible primitives are Potential, Pressure, Flow, and Membrane. Time is a dimension, not a primitive. Derived mechanics must derive from those four primitives.

### Proof Before Promotion

Nothing becomes durable without proof. Ephemeral evidence, validation, confidence, and promotion criteria must justify durable knowledge.

### Ephemeral First

Working state is disposable by default. Caches, projections, summaries, simulations, indexes, and temporary recognition remain ephemeral unless intentionally promoted.

## Repository Overview

| Directory | Purpose |
| --- | --- |
| `canon/` | Canonical glossary and concise reference language. |
| `constitution/` | Immutable architectural doctrine: principles, CivPhys, execution, repository model, assets, and constitutional rules. |
| `contracts/` | Stable boundary language between engines and services. Contracts contain no implementation. |
| `capabilities/` | Canonical architectural verbs and capability grammar. |
| `services/` | Reusable infrastructure consumed by engines. Services may depend on contracts but not engines. |
| `engines/` | Unique responsibility owners that compose contracts and services into architectural behavior. |
| `domains/` | Real-world compositions of engines into domain solutions. |
| `internal/` | Applications owned by Wayfinder, such as CLI, API, workers, desktop, mobile, or web surfaces. |
| `external/` | Replaceable third-party integrations and adapters. |
| `operations/` | Deployment, monitoring, maintenance, recovery, migrations, and runtime operations. |
| `tooling/` | Developer tooling, scaffolding, linters, code generation, benchmarks, and migration tools. |
| `docs/` | Governance, audits, scorecards, dashboards, reports, and contributor guidance. |
| `tests/` | Verification assets that validate constitutional and implementation behavior. |

Repository topology is independent of execution flow. Execution flows through Reality, Observation, Ephemeral Computation, Proof, Promotion, Durable Knowledge, Navigation, and Action.

First Contact refined that flow: Observation Sources produce
observation-shaped records, ARK preserves them, and WEAVE owns later durable
relationship topology.

## Engine Model

### Engine

An engine owns one unique architectural responsibility. It consumes contracts and services, produces its own constitutional outputs, and does not compete to become the platform.

### Service

A service owns reusable infrastructure. Services are generic, engine-independent, and consume contracts rather than engine internals.

### Capability

A capability is a stable architectural verb describing an outcome. Implementations, providers, and availability live elsewhere.

### Contract

A contract defines what crosses boundaries. It names producers, consumers, inputs, outputs, invariants, failure modes, and promotion rules without defining implementation APIs.

For observations, the producer role is Observation Source. ARK is the
preservation authority that consumes observation-shaped records.

### Domain

A domain composes engines into real-world solutions. Domains own orchestration, not shared infrastructure.

### View

A view is a projection or perspective over knowledge. Views present and reveal; they do not own the underlying reality, asset, or reasoning.

## Adding New Concepts

Before adding a concept, answer these questions in order:

1. Does this concept already exist under another name?
2. Can it be derived from an existing constitutional concept?
3. Who owns it today?
4. Who should be the canonical owner?
5. Does it belong in `constitution/`, `contracts/`, `capabilities/`, `services/`, `engines/`, or `domains/`?
6. What depends on it?
7. What consumes it?
8. What proof would justify making it durable?
9. Does adding it reduce ambiguity, or does it duplicate an existing home?

If ownership is unclear, do not implement. Record the ambiguity as architectural evidence first.

## Adding New Engines

A new engine must satisfy this checklist:

- One purpose.
- One owner.
- Defined boundaries.
- Contracts first.
- No duplicated concepts.
- Clear inputs and outputs.
- Clear dependencies.
- Clear consumers.
- No ownership of shared infrastructure.
- No capability grammar ownership.

Create a constitutional stub before implementation. The stub must define Purpose, Owns, Does Not Own, Inputs, Outputs, Dependencies, and Consumers.

Placeholder engine folders and lifecycle templates are not implementations.
Mark planned engines clearly as pending until there is proof-backed behavior.

## Adding New Services

A new service must satisfy this checklist:

- Infrastructure only.
- Reusable across engines.
- No engine dependencies.
- One responsibility.
- Contract-backed language.
- Replaceable implementation.
- Explicit failure model.
- No domain-specific behavior.

Services may depend on Constitution and Contracts. Services must not depend on Engines, Domains, Internal applications, External integrations, or Operations.

## Adding Capabilities

Capabilities are added to the grammar only when the verb is stable, reusable, and not an implementation detail. Ask:

1. Is this an outcome rather than a tool?
2. Is the verb stable across providers?
3. Does an existing capability already cover it?
4. Is availability a NOMAD discovery concern rather than a new grammar term?
5. Is routing a Jarvis concern rather than a new grammar term?

Implementations belong in services, engines, domains, internal applications, external integrations, or operations. They do not belong in `capabilities/`.

## Constitutional Change Process

```text
Proposal
  ↓
Review
  ↓
Proof
  ↓
Promotion
  ↓
Canonical Adoption
```

A constitutional change starts as a proposal with evidence. Review tests it against One Concept, One Home, dependency direction, CivPhys, the Asset model, contracts, and engine boundaries. Proof demonstrates that the change reduces ambiguity or debt without breaking continuity. Promotion records the canonical owner, rollback path, date, and confidence. Canonical adoption updates the relevant constitution, contract, ownership, debt, census, and dashboard documents.

## Local Validation Outputs

Validation payloads, generated observations, replay outputs, temporary indexes,
import artifacts, and preserved source artifacts are local by default. The
repository ignores `.wayfinder-validation/`; do not commit files from that
directory. Commit privacy-safe aggregate reports under `docs/` instead.

## First Contact Follow-Up Rules

- Add Import Profiles before larger private imports.
- Use Candidate Pages or equivalent bounded intake before storing real
  export-scale compiler output in governance.
- Keep streamable event publication as a future improvement before larger
  import volumes.
- Do not add embeddings, Knowledge Graph behavior, Jarvis, Reasoning, or new
  Oracles until the First Contact consolidation items are reviewed.

## Contributor Rule Of Thumb

When in doubt, preserve behavior, reduce duplication, clarify ownership, and make evidence visible before making anything durable.
