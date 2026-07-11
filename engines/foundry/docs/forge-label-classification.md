# Forge Label Classification

## Summary

Foundry is the canonical Wayfinder owner for engineering workflows. Forge is
historical ARK terminology and a compatibility label for preserved source,
launchers, tests, docs, and migration evidence.

This report classifies repo-local Forge labels as either code-bearing surfaces
or idea-bearing architectural references. Duplicated ARK/Foundry legacy code is
classified as preserved historical code, not as two canonical owners.

## Code-Labeled Forge

| Path | Kind | Canonical owner | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `engines/ark/legacy/ark-core/forge/` | Runtime package | Foundry, preserved under ARK legacy | Contains Forge context, control, core loop, exec, MCP, memory, models, runtime, transform, UI, and verify modules. | High |
| `engines/foundry/legacy/ark-core/forge/` | Runtime package copy | Foundry | Preserved Forge-origin package under Foundry fold. | High |
| `engines/ark/legacy/forge`, `forge-app`, `forge.cmd`, `forge.ps1`, `Forge App.*` | Legacy launchers | Foundry compatibility | Executable/script entrypoints for historical Forge app/runtime. | High |
| `engines/foundry/legacy/forge`, `forge-app`, `forge.cmd`, `forge.ps1`, `Forge App.*` | Legacy launchers | Foundry compatibility | Preserved launchers under Foundry fold. | High |
| `engines/ark/legacy/ark-core/scripts/ai/forge.py` | Python launcher/script | Foundry compatibility | Repo-root Forge launcher for ark-core legacy flow. | High |
| `engines/foundry/legacy/ark-core/scripts/ai/forge.py` | Python launcher/script | Foundry compatibility | Preserved Foundry-folded ark-core Forge launcher. | High |
| `engines/ark/legacy/scripts/ai/forge.py` | Python launcher/script | Foundry compatibility | Legacy Forge launcher in ARK scripts. | High |
| `engines/foundry/legacy/scripts/ai/forge.py` | Python launcher/script | Foundry compatibility | Preserved Foundry-folded Forge launcher. | High |
| `engines/ark/legacy/ark-core/tests/test_forge_*.py` | Tests | Foundry compatibility | Forge-specific test suite for launcher, browser, MCP, security, session, UI, proposals, and related behavior. | High |
| `engines/ark/legacy/agents/forge_native/` | Agent compatibility package | Foundry compatibility | Legacy Forge-native agent wrapper. | High |
| `engines/foundry/legacy/agents/forge_native/` | Agent compatibility package | Foundry compatibility | Preserved Foundry-folded Forge-native agent wrapper. | High |
| `engines/ark/legacy/ark/forge_planner.py` | Planner facade | Foundry compatibility | Forge planner facade for legacy ARK. | High |
| `engines/foundry/legacy/ark/forge_planner.py` | Planner facade | Foundry compatibility | Preserved Foundry-folded planner facade. | High |
| `engines/ark/legacy/install-forge-arch.sh` | Installer script | Foundry compatibility | Legacy install script for Forge app commands. | High |
| `engines/foundry/legacy/install-forge-arch.sh` | Installer script | Foundry compatibility | Preserved Foundry-folded installer. | High |
| `engines/ark/legacy/packaging/linux/forge-app.desktop.in` | Packaging asset | Foundry compatibility | Linux desktop integration for Forge app. | High |
| `engines/ark/legacy/packaging/linux/forge-app.svg` | Packaging asset | Foundry compatibility | Linux icon asset for Forge app. | High |
| `engines/ark/legacy/agents/*/agent.py` references to Forge-native profiles | Runtime adapter references | Foundry compatibility | Legacy agents route capabilities through Forge-compatible local planning. | Medium |
| `engines/ark/legacy/ark/sd_trisca.py` | Runtime support reference | Foundry compatibility | Mentions Forge-style planners as users of TRISCA support logic. | Medium |

## Idea-Labeled Forge

| Path | Concept | Canonical owner | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `canon/glossary.md` | Forge alias/deprecated term | Canon and Foundry | Defines Forge as the former name for Foundry engineering support. | High |
| `docs/adrs/0010-legacy-forge-consolidation-with-compatibility-aliases.md` | Compatibility decision | Foundry | Decides Forge legacy consolidation through compatibility aliases. | High |
| `docs/adrs/README.md` | ADR index reference | Architecture decisions | Links ADR-0010. | High |
| `docs/architecture/20-repository-map.md` | Repository ownership mapping | Foundry | Maps Foundry and Foundry legacy as the canonical Forge fold. | High |
| `docs/constitutional-census.md` | Capability and responsibility analysis | Foundry | Classifies Engineering Workflow, Forge Compatibility, model adapters, MCP tooling, UI, memory, and artifacts. | High |
| `docs/architectural-analysis-2026-07-05.md` | Architecture analysis | Foundry and governance | Describes duplicate Forge-origin preserved legacy body and consolidation questions. | High |
| `docs/architectural-debt.md` | Compatibility debt | Foundry | Records Forge-origin executable names preserved under Foundry. | High |
| `docs/migration-dashboard.md` | Migration status | Foundry | Tracks Foundry inventory and Forge normalization status. | High |
| `docs/promotion-registry.md` | Promotion evidence | Foundry | Records Foundry canonical owner and Forge-origin source. | High |
| `docs/ownership-matrix.md` | Ownership matrix | Foundry | Maps Forge Legacy Compatibility to Foundry. | High |
| `docs/implementation-backlog.md` | Roadmap/backlog item | Foundry | Tracks Foundry stage and Forge normalization evidence. | Medium |
| `docs/first-contact/evidence-assimilation.md` | Evidence assimilation reference | Foundry / generated evidence | Mentions Forge within first-contact evidence context. | Medium |
| `docs/governance/repository-timeline.md` | Governance timeline | Foundry | References ADR-0010. | High |
| `docs/governance/capability-dashboard.md` | Capability dashboard phrase | Capability Registry / Foundry | Mentions Forge publishing a capability call. | Medium |
| `docs/governance/candidate-pages.md` | Generated governance candidate references | Governance evidence | Repeats ADR-0010 and related Forge candidate references. | Medium |
| `docs/governance/architecture-doctor.json` | Generated governance index | Governance evidence | Contains generated references to Forge docs, code, tests, and duplicate paths. | Medium |
| `engines/ark/docs/dependency-graph.md`, `duplicate-concepts.md`, `inventory.md`, `migration-plan.md` | ARK extraction/migration documentation | ARK / Foundry boundary | Documents Forge-origin duplication and migration context. | Medium |
| `engines/foundry/README.md` | Foundry ownership statement | Foundry | States Forge is historical ARK terminology and Foundry is canonical owner. | High |
| `engines/foundry/docs/ark-forge-normalization.md` | Forge normalization record | Foundry | Records Forge-origin source preserved under Foundry. | High |
| `engines/foundry/docs/p0-*`, `p1-*`, `p2-*`, `p3-*`, `p4-*` references | Foundry phase artifacts | Foundry | Treat Forge as legacy alias or compatibility/history evidence. | High |
| `services/configuration/docs/inventory.md`, `services/policy/docs/inventory.md` | Service extraction inventory | Configuration / Policy service | References Forge config/policy files as source evidence for service boundaries. | Medium |

## Ambiguous Or Excluded

| Path or label | Classification | Reason |
| --- | --- | --- |
| `docs/wayfinder-infra-program.md` Forgejo references | Excluded | Forgejo is a Git forge product, not the historical Forge/Foundry engineering engine. |
| `docs/governance/architecture-doctor.json` | Ambiguous generated evidence | Generated index mixes code paths, docs, duplicate groups, and candidate references. Use as evidence, not canonical classification. |
| `docs/governance/candidate-pages.md` | Ambiguous generated evidence | Generated candidate pages repeat source references and should not be treated as canonical ownership. |
| `engines/ark/legacy/ARK_SPEC_PACK_V1.md`, `DEPLOYMENT_GUIDE_v1.0.md`, `PRODUCTION_RELEASE_v1.0.md`, `README.md`, `VERIFICATION_v1.0.md` | Idea/reference inside legacy docs | These are historical ARK docs that mention Forge behavior; they are not the canonical Foundry architecture. |
| `engines/ark/legacy/policy/import_registry.json` | Ambiguous legacy config | Contains Forge-related legacy import/config evidence; classify as historical config until extracted. |
| `engines/ark/legacy/scripts/deploy.sh` | Ambiguous legacy operations script | Mentions Forge in deployment context; classify under historical operations until extracted. |
| `BUILD_BIBLE/` | Excluded | Currently untracked and outside this classification unless explicitly requested. |
| `BUILD_OPERATIONS/` | Excluded | Currently untracked and outside this classification unless explicitly requested. |

## Verification

Scans used:

```bash
rg -l -i "\\bforge\\b|forge-|-forge|Forge" . \
  -g '!BUILD_BIBLE/**' \
  -g '!BUILD_OPERATIONS/**' \
  -g '!.git/**' \
  -g '!Knowledge/**' \
  -g '!.wayfinder-validation/**' \
  -g '!**/__pycache__/**'
```

```bash
find . \
  -path './.git' -prune -o \
  -path './Knowledge' -prune -o \
  -path './.wayfinder-validation' -prune -o \
  -path './BUILD_BIBLE' -prune -o \
  -path './BUILD_OPERATIONS' -prune -o \
  -iname '*forge*' -print
```

Every matched surface is classified as Code, Ideas, Ambiguous, or Excluded.

