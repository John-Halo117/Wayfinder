# Prompt Refactor Report

## Scope

Reviewed prompt-bearing Foundry and Codex surfaces:

- `engines/foundry/legacy/ark-core/forge/models/prompts.py`
- `engines/ark/legacy/ark-core/forge/models/prompts.py`
- `engines/foundry/legacy/ark-core/scripts/ai/codex_prompt.txt`
- `engines/ark/legacy/ark-core/scripts/ai/codex_prompt.txt`
- `engines/ark/legacy/ark-core/docs/CODEX_ARK_SYSTEM_PROMPT.md`
- `engines/foundry/legacy/scripts/ai/autonomous_repair.py`
- `engines/ark/legacy/scripts/ai/autonomous_repair.py`
- `engines/foundry/legacy/scripts/ai/local_codegen_loop.py`
- `engines/ark/legacy/scripts/ai/local_codegen_loop.py`

## Changes

- Added the canonical Prompt Architecture Standard.
- Refactored Forge plan, diff, and attack prompt builders to emit the standard
  ten sections.
- Converted the ARK Codex system prompt from restated architecture into an
  inheritance-oriented compiler pass.
- Refactored inline autonomous repair and local codegen prompts to the standard
  structure.
- Added an explicit cycle cap to the local codegen queue worker.
- Kept phase intent unchanged: plan prompts still plan, diff prompts still emit
  diffs, attack prompts still red-team a candidate patch.

## Token Savings Estimate

| Surface | Before | After | Estimated Reduction |
| --- | ---: | ---: | ---: |
| ARK Codex System Prompt | High repetition of laws and flow diagrams | References inherited artifacts | 35-45% |
| Forge Diff Prompt | Mixed identity/context/rules | Standard sections | 5-10% |
| Forge Plan Prompt | Ad hoc structure | Standard sections | Neutral |
| Forge Attack Prompt | Ad hoc structure | Standard sections | Neutral |

## Duplicate Content Removed

- Direct restatement of ARK system laws in the Codex prompt.
- Direct restatement of truth-spine flow in the Codex prompt.
- Repeated local/deterministic/proof posture across prompt surfaces.

## Shared Artifacts Introduced

- `prompt-architecture-standard.md`
- `prompt-dependency-graph.md`
- `prompt-refactor-report.md`

## Redundancy Report

| Redundancy | Resolution |
| --- | --- |
| Constitutional behavior repeated in prompt text. | Replaced with inherited artifact references. |
| Runtime posture repeated across prompts. | Kept only pass-local rules in each prompt. |
| Output expectations embedded in prose. | Moved to explicit `Outputs` and `Validation` sections. |

## Recommendations

- Add new prompts only through the Prompt Architecture Standard.
- Store shared rules in constitution, contracts, engine docs, or configs.
- Require each new prompt to declare exactly one responsibility and one success
  question.
- Treat prompt outputs as durable phase artifacts when they feed later prompts.
