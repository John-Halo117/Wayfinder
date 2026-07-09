# Prompt Dependency Graph

## Bootstrap-Centric Pipeline

```text
bootstrap/bootstrap.yaml
  -> Bootstrap
      -> P0
          -> P1
              -> P2
                  -> P2.5
                      -> P3
                          -> P4
                              -> P5
                                  -> ...
```

Every phase declares bootstrap as a prerequisite, inherits bootstrap artifacts,
and inherits every prior phase artifact. No phase rediscovers information
already represented by inherited artifacts.

## Bootstrap Contract

| Contract | Source |
| --- | --- |
| Boot policy | `engines/foundry/bootstrap/bootstrap.yaml` |
| Document order | `engines/foundry/bootstrap/bootstrap.yaml` |
| Required documents | `engines/foundry/bootstrap/bootstrap.yaml` |
| Produced artifacts | `engines/foundry/bootstrap/bootstrap.yaml` |
| Cache and invalidation snapshot | `engines/foundry/bootstrap/bootstrap.lock` |

## Legacy Forge Prompt Lineage

```text
Constitution
  -> ARK Truth Spine
  -> Mission-Grade Rules
  -> Operating Rules
  -> System Invariants
  -> Codex ARK System Prompt
      -> AI Codex Loader Prompt
      -> Forge Plan Prompt
          -> Forge Diff Prompt
              -> Forge Attack Prompt
```

## Artifact Flow

```text
Bootstrap artifacts
  -> Repository Model
  -> Knowledge Graph
  -> Architectural Intelligence
  -> Opportunity Catalog
  -> Bundle Catalog
  -> Priority Plan
  -> Implementation Plan
  -> Implementation
  -> Verification
```

## Prompt Pipeline

| Prompt | Responsibility | Inputs | Outputs |
| --- | --- | --- | --- |
| Codex ARK System Prompt | Bind agent behavior to inherited ARK artifacts. | Task request, loaded ARK artifacts. | Bounded local execution posture. |
| AI Codex Loader Prompt | Load canonical ARK behavior artifacts. | ARK docs and configs. | Agent instruction preload. |
| Forge Plan Prompt | Produce bounded implementation guidance. | `ContextBundle`. | Plan JSON. |
| Forge Diff Prompt | Produce patch only. | `ContextBundle`, optional plan. | Unified diff. |
| Forge Attack Prompt | Critique one candidate patch. | `ContextBundle`, diff, mode. | Red-team JSON. |

## Refactored Foundry Phase Prompts

| Prompt | Responsibility | Inheritance | Outputs |
| --- | --- | --- | --- |
| `prompts/P0.md` | Validate bootstrap completion and expose foundation artifacts. | Bootstrap artifacts. | P0 foundation artifact index. |
| `prompts/P1.md` | Construct repository model from bootstrapped worldview. | Bootstrap artifacts, P0. | Repository discovery artifacts. |
| `prompts/P2.md` | Construct canonical knowledge graph artifacts. | Bootstrap artifacts, P0, P1. | Knowledge acquisition artifacts. |
| `prompts/P2.5.md` | Validate knowledge integrity and classify uncertainty. | Bootstrap artifacts, P0, P1, P2. | P3 readiness artifacts. |
| `prompts/P3.md` | Discover evidence-backed architectural opportunities. | Bootstrap artifacts, P0, P1, P2, P2.5. | Architectural intelligence artifacts. |
| `prompts/P4.md` | Compose opportunities into coherent bundles. | Bootstrap artifacts, P0-P3. | Bundle composition artifacts. |
