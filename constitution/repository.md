# Repository Responsibilities

Wayfinder is organized by responsibility, not by execution order.

Each top-level directory is a constitutional ownership home. Concepts should be placed by what they are, not by where they were historically implemented.

## Top-Level Directories

| Directory | Purpose | Owns | Does Not Own |
| --- | --- | --- | --- |
| `constitution/` | Immutable architectural doctrine. | Laws, CivPhys, repository rules, execution semantics, naming doctrine, architectural invariants. | Runtime implementation or engine behavior. |
| `contracts/` | Shared implementation-free language. | Schemas, vocabularies, interface language, cross-engine nouns. | Runtime behavior or infrastructure. |
| `capabilities/` | Stable architectural verbs and capability grammar. | Outcome-level verbs and capability classification. | Specific implementation or provider behavior. |
| `services/` | Reusable infrastructure. | Shared implementation primitives such as identity, storage, event bus, configuration, and policy. | Unique engine responsibility. |
| `engines/` | Unique architectural responsibilities composed from services and contracts. | Engine behavior, engine lifecycle, responsibility-specific durable logic. | Shared infrastructure or domain orchestration. |
| `domains/` | Real-world orchestration. | Domain compositions of engines, services, external systems, and objectives. | Platform infrastructure. |
| `internal/` | Wayfinder-owned application surfaces. | API, CLI, desktop, web, workers, automation owned by Wayfinder. | Engine concepts or shared services. |
| `external/` | Replaceable outside systems and integrations. | Third-party system boundaries and adapters. | Canonical Wayfinder concepts. |
| `operations/` | Runtime operations and maintenance. | Deployment, monitoring, backup, recovery, migrations, runtime workflows. | Product behavior or constitutional doctrine. |
| `tooling/` | Developer tooling. | Scaffolding, linters, code generation, migration tools, benchmarks, formatters. | Runtime platform behavior. |
| `docs/` | Governance, reports, migration evidence, and explanatory documentation. | Census, scorecards, dashboards, debt registers, promotion reports. | Canonical concept ownership when another directory owns the concept. |
| `tests/` | Cross-cutting repository tests and validation evidence. | Repo-level verification scaffolds. | Engine-specific canonical behavior. |
| `canon/` | Semantic kernel and naming registry. | Canonical glossary, aliases, deprecated terms, naming rules. | Runtime behavior, contracts, or engine responsibilities. |

## Ownership Rules

- Every concept has exactly one canonical home.
- Other directories may reference a concept, but they must not redefine it.
- If a concept is shared language, it belongs in `contracts/`.
- If a concept is reusable infrastructure, it belongs in `services/`.
- If a concept is a unique responsibility, it belongs in `engines/`.
- If a concept is domain orchestration, it belongs in `domains/`.
- If a concept is an outside system, it belongs in `external/`.
- If a concept is runtime maintenance, it belongs in `operations/`.
- If a concept is developer support, it belongs in `tooling/`.
- If a concept is semantic naming guidance, it belongs in `canon/`.
- If ownership is ambiguous, record the ambiguity in governance evidence before implementation.

## Dependency Rule

Dependencies point toward more foundational concepts.

A higher responsibility may reference lower responsibility language. A lower responsibility must not depend on a higher responsibility. When a dependency would point upward, reclassify the concept or express the boundary as a contract.

## Repository Topology And Execution

Repository topology is independent from execution flow.

The repository says where a concept lives. It does not say when a concept executes. Execution semantics are defined in `constitution/execution.md`.

## Private Validation Artifacts

Local validation payloads are not repository knowledge.

Generated observations, preserved source artifacts, replay outputs, temporary
indexes, import payloads, validation workspaces, and other source-derived local
artifacts must remain outside Git history unless explicitly promoted through a
privacy-safe report. The repository ignores `.wayfinder-validation/` for this
reason.

Validation reports committed to `docs/` must summarize aggregate evidence and
must not include raw private source content, generated observation payloads, or
preserved source artifacts.

## Filesystem Operation Discipline

Filesystem operations follow progressive discovery. They must complete a
bounded inventory before reorganization, classify items before choosing
destinations, and route unknown or low-confidence items to review instead of
guessing.

Canonical filesystem flow:

```text
Observe
  -> Inventory
  -> Classify
  -> Build Canonical Destinations
  -> Simulate
  -> Execute
  -> Verify
  -> Report
```

Every move must be reversible, logged, and verified. Recommendations that
affect file placement must include a confidence assessment.
