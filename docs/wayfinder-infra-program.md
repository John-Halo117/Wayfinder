# Wayfinder Infra Implementation Program

Date: 2026-06-27

This document creates the first-class implementation program for the future `wayfinder-infra` repository. It is planning evidence only. It does not create Docker infrastructure, compose files, containers, application services, or platform implementation.

## Objective

`wayfinder-infra` implements deployment of the Wayfinder platform. It is not the platform and it is not constitutional architecture.

Infrastructure is replaceable. The Wayfinder platform is not. Docker Compose is one possible implementation detail; it must never become the architecture.

## Repository Relationship

| Repository | Owns | Does Not Own |
| --- | --- | --- |
| `wayfinder` | Constitution, Canon, Contracts, Capabilities, Services, Engines, Runtime, Tests, Documentation | Host deployment topology, Docker Compose implementation, backup scripts, machine-specific environment layout |
| `wayfinder-infra` | Deployment, Docker Compose, container orchestration, host directory layout, operations, monitoring, backups, recovery, environment configuration | Constitution, contracts, application logic, engine behavior, service implementations, domain logic |

`wayfinder` implements the platform. `wayfinder-infra` implements deployment of the platform.

## Infrastructure Principles

| Principle | Meaning |
| --- | --- |
| Local First | The deployment should work on local hardware before depending on remote infrastructure. |
| Repairable | A human operator should be able to inspect, repair, and rebuild the system with ordinary tools. |
| Observable | Health, logs, ports, volumes, and backup state should be visible. |
| Version Controlled | Infrastructure definitions, scripts, docs, and conventions should be tracked. |
| Replaceable | Docker Compose, host paths, and selected tools may be replaced without redefining Wayfinder. |
| Declarative | Desired infrastructure state should be described clearly instead of hidden in manual steps. |
| Safe by Default | Defaults should avoid exposing secrets, deleting data, or binding unsafe services. |
| Non-Destructive | Install, update, backup, restore, and doctor flows must preserve data unless destruction is explicit and confirmed. |

Infrastructure should preserve data and remain easy to rebuild.

## Execution Program

Infrastructure follows the standard Wayfinder execution grammar:

```text
Constitution
  -> Program
  -> Roadmap
  -> Milestones
  -> Backlog
  -> Implementation
  -> Verification
  -> Proof
  -> Promotion
  -> Reality
```

For `wayfinder-infra`, Constitution remains in `wayfinder`. Program, roadmap, milestones, and backlog are planned here first, then implemented in the separate infrastructure repository.

## Repository Maturity Model

| Stage | Meaning | Evidence Required |
| --- | --- | --- |
| Stage 0 | Program | Repository purpose, boundaries, and principles are documented. |
| Stage 1 | Scaffold | README, roadmap, backlog, docs structure, compose skeleton path, scripts path, and services path are present without running containers. |
| Stage 2 | Shared Infrastructure | Network, environment, directory, compose, and healthcheck conventions are documented and verified. |
| Stage 3 | Service Groups | Planned service groups have compose definitions and operations docs. |
| Stage 4 | Operational | Install, update, backup, restore, doctor, and healthcheck flows are verified. |
| Stage 5 | Mature | Recovery is proven, monitoring is routine, and ARK ingress evidence is reliable. |

## Platform Progress

| Component | Stage | Status |
| --- | :---: | --- |
| Repository Program | 0 | ✅ |
| Repository Scaffold | 0 | 🔄 Next |
| Shared Infrastructure | 0 | ⏳ |
| Core Repositories | 0 | ⏳ |
| Operations | 0 | ⏳ |
| ARK Ingress Preparation | 0 | ⏳ |

## Ownership Table

| Area | Canonical Repository | Notes |
| --- | --- | --- |
| Constitution | `wayfinder` | Must not be duplicated in `wayfinder-infra`. |
| Contracts | `wayfinder` | Infra may reference contracts but does not own them. |
| Platform services | `wayfinder` | Infra deploys services; it does not implement application logic. |
| Engine behavior | `wayfinder` | Infra may expose logs or endpoints; it does not own behavior. |
| Compose implementation | `wayfinder-infra` | Replaceable deployment detail. |
| Host directory layout | `wayfinder-infra` | Operational deployment concern. |
| Environment configuration | `wayfinder-infra` | Runtime configuration for deployment, not constitutional config ownership. |
| Backups and recovery | `wayfinder-infra` | Operational responsibility. |
| Monitoring deployment | `wayfinder-infra` | Observability implementation, not VALOR ownership. |
| ARK ingress paths | `wayfinder-infra` documents locations; `wayfinder` owns ARK behavior | No ARK integration is implemented in this program. |

## Infrastructure Roadmap

| Milestone | Stage Target | Status | Depends On |
| --- | :---: | --- | --- |
| M-001 Repository Scaffold | 1 | 🔄 Next | Program approval |
| M-002 Shared Infrastructure | 2 | ⏳ | M-001 |
| M-003 Core Repositories | 3 | ⏳ | M-002 |
| M-004 Inventory | 3 | ⏳ | M-002 |
| M-005 Media | 3 | ⏳ | M-002 |
| M-006 ARR Stack | 3 | ⏳ | M-002 |
| M-007 Platform Services | 3 | ⏳ | M-002 |
| M-008 Observation | 3 | ⏳ | M-002 |
| M-009 Monitoring | 3 | ⏳ | M-002 |
| M-010 Operations | 4 | ⏳ | M-003 through M-009 |
| M-011 Documentation | 4 | ⏳ | M-001 through M-010 |

## Milestone Dependency Graph

```text
M-001 Repository Scaffold
  -> M-002 Shared Infrastructure
      -> M-003 Core Repositories
      -> M-004 Inventory
      -> M-005 Media
      -> M-006 ARR Stack
      -> M-007 Platform Services
      -> M-008 Observation
      -> M-009 Monitoring
          -> M-010 Operations
              -> M-011 Documentation
```

Service-group milestones may be planned in parallel after M-002, but implementation should remain small, verifiable, and non-destructive.

## Initial Implementation Order

| Order | Milestone | Reason |
| ---: | --- | --- |
| 1 | M-001 Repository Scaffold | Creates the repo shell and planning structure without containers. |
| 2 | M-002 Shared Infrastructure | Establishes conventions before individual services duplicate patterns. |
| 3 | M-003 Core Repositories | Nextcloud, Immich, and Paperless are high-value durable user data systems. |
| 4 | M-009 Monitoring | Basic visibility should arrive before the stack grows too large. |
| 5 | M-010 Operations | Backup, restore, doctor, and healthcheck need early proof. |
| 6 | M-004 Inventory | Grocy and InvenTree depend on shared conventions and backup policy. |
| 7 | M-005 Media | Jellyfin and Navidrome are less foundational than durable repositories. |
| 8 | M-006 ARR Stack | ARR services should follow media and shared network conventions. |
| 9 | M-007 Platform Services | Forgejo and Ollama should be deployed after operational practices are proven. |
| 10 | M-008 Observation | Home Assistant and Frigate become ARK observation producers after ingress paths are documented. |
| 11 | M-011 Documentation | Finalizes ports, volumes, operations, backups, and ARK ingress docs after plans stabilize. |

## Implementation Backlog

### M-001 Repository Scaffold

Create in the future `wayfinder-infra` repository:

- `README.md`
- `ROADMAP.md`
- implementation backlog
- documentation structure
- compose skeleton directory
- scripts directory
- services directory

No containers. No compose service definitions. No application logic.

Definition of Done:

- Repository exists.
- Planning complete.
- No containers are started.
- No platform code is copied from `wayfinder`.

### M-002 Shared Infrastructure

Plan:

- shared network
- environment management
- directory layout
- common compose conventions
- shared healthcheck conventions

Definition of Done:

- Conventions are documented.
- No service-specific compose implementation is required.
- Secrets, host paths, and destructive operations have safe defaults.

### M-003 Core Repositories

Plan deployment for:

- Nextcloud
- Immich
- Paperless

Definition of Done:

- Ports, volumes, backup expectations, restore expectations, and ARK observation surfaces are planned.
- No containers are implemented by this planning milestone.

### M-004 Inventory

Plan deployment for:

- Grocy
- InvenTree

Definition of Done:

- Data ownership, backups, ports, and observation surfaces are planned.

### M-005 Media

Plan deployment for:

- Jellyfin
- Navidrome

Definition of Done:

- Media paths, ports, backup expectations, and observation surfaces are planned.

### M-006 ARR Stack

Plan deployment for:

- Prowlarr
- Sonarr
- Radarr
- Readarr

Definition of Done:

- Network boundaries, data paths, dependency order, and observation surfaces are planned.

### M-007 Platform Services

Plan deployment for:

- Forgejo
- Ollama

Definition of Done:

- Data paths, model/storage expectations, access patterns, and observation surfaces are planned.

### M-008 Observation

Plan deployment for:

- Home Assistant
- Frigate

Definition of Done:

- Device/network assumptions, media paths, event surfaces, and ARK ingress expectations are planned.

### M-009 Monitoring

Plan deployment for:

- Uptime Kuma
- Dozzle

Definition of Done:

- Healthcheck patterns, log access, alert surfaces, and operator visibility are planned.

### M-010 Operations

Plan:

- install
- update
- backup
- restore
- doctor
- healthcheck

Definition of Done:

- Operations are non-destructive by default.
- Restore is treated as a first-class proof, not an afterthought.
- Doctor and healthcheck flows report structured evidence.

### M-011 Documentation

Plan:

- ports
- volumes
- operations
- backups
- ARK ingress

Definition of Done:

- Operators can understand what runs, where data lives, how to recover it, and how observations may later reach ARK.

## ARK Preparation

Every infrastructure service is a future producer of observations for ARK. This program does not implement ARK integration.

Expected ingress locations and access patterns should be documented for each service group:

| Service Group | Future Observation Examples | Expected Access Pattern |
| --- | --- | --- |
| Core Repositories | file changes, document ingestion, photo/media indexing, sync health | service APIs, exported logs, backup manifests, filesystem metadata |
| Inventory | stock changes, item updates, consumption records, purchase needs | service APIs, scheduled exports, backup manifests |
| Media | playback events, library scans, metadata updates | service APIs, logs, filesystem metadata |
| ARR Stack | queue state, download/import events, indexer health | service APIs, logs, health endpoints |
| Platform Services | repository events, model availability, job status | service APIs, logs, health endpoints |
| Observation | device states, camera detections, automation events | event exports, APIs, media paths, logs |
| Monitoring | uptime events, container logs, alert state | monitoring APIs, log streams, health endpoints |

ARK ingress docs should identify where observations can be read later. They must not make ARK responsible for infrastructure deployment.

## Validation

| Check | Result |
| --- | --- |
| Infrastructure responsibilities separated from platform repository | Pass |
| No application code planned for `wayfinder-infra` | Pass |
| No constitutional documents duplicated | Pass |
| Docker remains an implementation detail | Pass |
| Infrastructure remains replaceable | Pass |
| No Docker infrastructure created by this task | Pass |
| No compose files created by this task | Pass |
| No services implemented by this task | Pass |

## Recommended First Implementation Milestone

M-001 Repository Scaffold.

Reason: It creates the future `wayfinder-infra` repository shell and planning structure without running containers or encoding Docker as architecture.
