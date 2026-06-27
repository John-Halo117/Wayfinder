# Wayfinder Portfolio

Date: 2026-06-27

This portfolio tracks the family of Wayfinder repositories. It is planning evidence, not constitutional doctrine. The `wayfinder` repository remains the canonical source for Constitution, Canon, Contracts, Capabilities, Services, Engines, Runtime, Tests, and platform documentation.

## Portfolio Status

| Repository | Status |
| --- | --- |
| `wayfinder` | Active |
| `wayfinder-infra` | Planned |
| `wayfinder-home` | Planned |
| `wayfinder-build-bible` | Planned |
| `wayfinder-living-map` | Planned |
| `wayfinder-family` | Planned |
| `wayfinder-homestead` | Planned |
| `wayfinder-cookbook` | Planned |

## Portfolio Ownership Rules

- `wayfinder` owns the platform and constitutional architecture.
- Other repositories may implement deployments, domains, applications, datasets, or operating practices.
- No portfolio repository duplicates constitutional doctrine.
- Domain repositories consume Wayfinder contracts and services; they do not redefine them.
- Infrastructure remains replaceable and does not become the architecture.
- Portfolio roadmaps must reduce ambiguity, not create competing homes for concepts.

## Repository Dependency Graph

```text
wayfinder
  -> wayfinder-infra
  -> wayfinder-home
  -> wayfinder-build-bible
  -> wayfinder-living-map
  -> wayfinder-family
  -> wayfinder-homestead
  -> wayfinder-cookbook
```

`wayfinder` is the platform dependency for every other repository. Domain repositories may later depend on `wayfinder-infra` for local deployment evidence, but they must continue to treat deployment as replaceable.

## Portfolio Roadmap

| Order | Repository | Current Maturity | Next Milestone | Status |
| ---: | --- | --- | --- | --- |
| 1 | `wayfinder` | Stage 2 platform substrate in progress | M-003 Storage Minimal Implementation Proof | Active |
| 2 | `wayfinder-infra` | Stage 0 Program | M-001 Repository Scaffold | Planned |
| 3 | `wayfinder-home` | Stage 0 Planned | M-001 Repository Program | Planned |
| 4 | `wayfinder-build-bible` | Stage 0 Planned | M-001 Repository Program | Planned |
| 5 | `wayfinder-living-map` | Stage 0 Planned | M-001 Repository Program | Planned |
| 6 | `wayfinder-family` | Stage 0 Planned | M-001 Repository Program | Planned |
| 7 | `wayfinder-homestead` | Stage 0 Planned | M-001 Repository Program | Planned |
| 8 | `wayfinder-cookbook` | Stage 0 Planned | M-001 Repository Program | Planned |

## Repository Maturity Model

| Stage | Meaning | Evidence Required |
| --- | --- | --- |
| Stage 0 | Planned / Program | Purpose, owner, dependencies, next milestone, roadmap, and backlog are documented. |
| Stage 1 | Scaffold | Repository exists with README, roadmap, backlog, docs structure, and no duplicated constitutional doctrine. |
| Stage 2 | Minimal Implementation | The first bounded implementation proof exists with tests or verification evidence. |
| Stage 3 | Vertical Slice | One useful end-to-end workflow is proven through Wayfinder contracts or deployment conventions. |
| Stage 4 | Operational | Maintenance, health, backup, restore, and routine operation are documented and verified. |
| Stage 5 | Mature | Multiple workflows are stable, debt is visible, and recovery or continuity proof exists. |

## `wayfinder`

### Purpose

Canonical Wayfinder platform repository. Owns constitutional architecture, canon, contracts, capabilities, services, engines, runtime implementation, tests, and platform documentation.

### Owner

Wayfinder Platform.

### Dependencies

None above it in the portfolio. It depends internally on its Constitution, Canon, Contracts, and governance evidence.

### Current Maturity

Stage 2 for platform substrate implementation. Identity and Event Bus have minimal implementation proofs. Storage, Configuration, and Policy remain Stage 1.

### Next Milestone

M-003 Storage Minimal Implementation Proof.

### Roadmap

| Order | Milestone | Status |
| ---: | --- | --- |
| 1 | Constitution v1 Finalization | Complete |
| 2 | Identity Minimal Implementation Proof | Complete |
| 3 | Event Bus Minimal Implementation Proof | Complete |
| 4 | Storage Minimal Implementation Proof | Next |
| 5 | Configuration Minimal Implementation Proof | Planned |
| 6 | Policy Minimal Implementation Proof | Planned |
| 7 | Identity Vertical Slice | Planned |

### Backlog

- Complete Storage Stage 2 proof.
- Complete Configuration Stage 2 proof.
- Complete Policy Stage 2 proof.
- Select the first platform vertical slice.
- Preserve dependency direction and update governance after each milestone.

## `wayfinder-infra`

### Purpose

Deployment repository for Wayfinder. Owns Docker Compose implementation, host directory layout, operations, monitoring deployment, backups, recovery, and environment configuration.

### Owner

Wayfinder Operations / Infrastructure.

### Dependencies

Depends on `wayfinder` for platform boundaries and ARK ingress expectations. Does not own platform logic.

### Current Maturity

Stage 0 Program. Planning exists in `docs/wayfinder-infra-program.md`; repository scaffold is not yet created.

### Next Milestone

M-001 Repository Scaffold.

### Roadmap

| Order | Milestone | Status |
| ---: | --- | --- |
| 1 | Repository Scaffold | Next |
| 2 | Shared Infrastructure | Planned |
| 3 | Core Repositories | Planned |
| 4 | Monitoring | Planned |
| 5 | Operations | Planned |
| 6 | Inventory, Media, ARR, Platform Services, Observation | Planned |
| 7 | Documentation | Planned |

### Backlog

- Create README, ROADMAP, backlog, docs structure, compose skeleton path, scripts path, and services path.
- Do not create containers during scaffold milestone.
- Document shared network, environment, directory, and healthcheck conventions.
- Preserve Docker as an implementation detail.

## `wayfinder-home`

### Purpose

Home operations repository for household systems, routines, devices, automations, maintenance records, and home-specific workflows that consume Wayfinder platform concepts.

### Owner

Home Domain.

### Dependencies

Depends on `wayfinder` for contracts, assets, observations, capabilities, policies, and ARK/Jarvis boundaries. May later depend on `wayfinder-infra` deployment conventions for local services.

### Current Maturity

Stage 0 Planned.

### Next Milestone

M-001 Repository Program.

### Roadmap

| Order | Milestone | Status |
| ---: | --- | --- |
| 1 | Repository Program | Next |
| 2 | Domain Boundary | Planned |
| 3 | Asset Inventory Model | Planned |
| 4 | Home Observation Sources | Planned |
| 5 | First Home Workflow Slice | Planned |

### Backlog

- Define repository boundary without duplicating `domains/` doctrine.
- Identify home asset categories and observation sources.
- Document integrations that remain external or infra-owned.
- Define first workflow candidate after platform Storage and Policy mature.

## `wayfinder-build-bible`

### Purpose

Repository for canonical build specifications, project requirements, acceptance criteria, and specification artifacts that may be consumed by Foundry and domains.

### Owner

Build Bible / Specification Domain.

### Dependencies

Depends on `wayfinder` contracts for specifications, schemas, proofs, promotion, assets, and evidence. May later consume Foundry outputs from `wayfinder`.

### Current Maturity

Stage 0 Planned.

### Next Milestone

M-001 Repository Program.

### Roadmap

| Order | Milestone | Status |
| ---: | --- | --- |
| 1 | Repository Program | Next |
| 2 | Specification Taxonomy | Planned |
| 3 | Acceptance Criteria Templates | Planned |
| 4 | Foundry Consumption Boundary | Planned |
| 5 | First Specification Slice | Planned |

### Backlog

- Define what specifications live here versus in `wayfinder/contracts/`.
- Document non-ownership of constitutional schemas.
- Create initial spec categories and promotion rules.
- Identify first build artifact to prove the repository boundary.

## `wayfinder-living-map`

### Purpose

Repository for living map knowledge: places, regions, routes, property context, environmental context, and spatial continuity artifacts.

### Owner

Living Map Domain.

### Dependencies

Depends on `wayfinder` asset, context, relationship, bearing, observation, and evidence contracts. May later consume deployment evidence from `wayfinder-infra` for map services.

### Current Maturity

Stage 0 Planned.

### Next Milestone

M-001 Repository Program.

### Roadmap

| Order | Milestone | Status |
| ---: | --- | --- |
| 1 | Repository Program | Next |
| 2 | Spatial Asset Boundary | Planned |
| 3 | Context and Relationship Model | Planned |
| 4 | Observation Source Plan | Planned |
| 5 | First Map Slice | Planned |

### Backlog

- Define repository scope for spatial knowledge without creating new base classes.
- Identify assets, contexts, relationships, and observation sources.
- Document dependencies on ARK, WEAVE, Views, and Jarvis outputs.
- Select first bounded map workflow.

## `wayfinder-family`

### Purpose

Repository for family continuity, commitments, routines, shared knowledge, agreements, documents, and household coordination artifacts.

### Owner

Family Domain.

### Dependencies

Depends on `wayfinder` identity, asset, evidence, capsule, commitment, policy, permission, and MICE boundaries. May later depend on infra for deployed family applications.

### Current Maturity

Stage 0 Planned.

### Next Milestone

M-001 Repository Program.

### Roadmap

| Order | Milestone | Status |
| ---: | --- | --- |
| 1 | Repository Program | Next |
| 2 | Family Asset and Identity Boundary | Planned |
| 3 | Commitment and Agreement Model | Planned |
| 4 | Capsule Continuity Plan | Planned |
| 5 | First Family Workflow Slice | Planned |

### Backlog

- Define privacy and permission boundaries.
- Identify durable family assets, records, commitments, and capsules.
- Document what remains in `wayfinder` contracts and engines.
- Select first workflow after Policy and Permission service maturity improves.

## `wayfinder-homestead`

### Purpose

Repository for homestead planning and operations: land, structures, water, power, gardens, animals if applicable, maintenance, projects, and environmental resilience.

### Owner

Homestead Domain.

### Dependencies

Depends on `wayfinder` asset, context, CivPhys, capability, evidence, relationship, health, and bearing contracts. May later consume observations from Home Assistant, Frigate, weather, and inventory systems through infra and ARK.

### Current Maturity

Stage 0 Planned.

### Next Milestone

M-001 Repository Program.

### Roadmap

| Order | Milestone | Status |
| ---: | --- | --- |
| 1 | Repository Program | Next |
| 2 | Homestead Asset Map | Planned |
| 3 | Resource Flow Model | Planned |
| 4 | Observation Source Plan | Planned |
| 5 | First Homestead Workflow Slice | Planned |

### Backlog

- Define homestead assets in context without domain-specific base classes.
- Map potential, pressure, flow, and membrane examples to homestead operations.
- Identify infrastructure and observation sources.
- Select the first maintenance or resilience workflow.

## `wayfinder-cookbook`

### Purpose

Repository for recipes, meal planning, pantry context, preparation workflows, nutrition preferences, and cooking knowledge as assets in context.

### Owner

Cooking Domain.

### Dependencies

Depends on `wayfinder` asset, representation, evidence, capability, transformation, context, and inventory-related contracts. May later consume Grocy or inventory observations through infra and ARK.

### Current Maturity

Stage 0 Planned.

### Next Milestone

M-001 Repository Program.

### Roadmap

| Order | Milestone | Status |
| ---: | --- | --- |
| 1 | Repository Program | Next |
| 2 | Recipe Asset Boundary | Planned |
| 3 | Pantry and Inventory Relationship Plan | Planned |
| 4 | Transformation Workflow Plan | Planned |
| 5 | First Meal Planning Slice | Planned |

### Backlog

- Define recipes as assets in context, not just files or text.
- Identify representations such as images, OCR, Markdown, tags, nutrition, and summaries.
- Document relationship to Grocy/InvenTree observations and ZWLib transformations.
- Select first bounded recipe or meal-planning workflow.

## Portfolio Validation

| Check | Result |
| --- | --- |
| Platform ownership remains in `wayfinder` | Pass |
| Planned repositories do not duplicate Constitution | Pass |
| Infrastructure remains replaceable | Pass |
| Domain repositories consume contracts rather than redefining them | Pass |
| Every planned repository has purpose, owner, dependencies, maturity, next milestone, roadmap, and backlog | Pass |

## Recommended Next Portfolio Milestone

Create the `wayfinder-infra` repository scaffold.

Reason: infrastructure deployment is the first non-platform repository dependency, and its scaffold can be created without Docker implementation or application logic.
