"""Prompt builders for optional Ollama-backed Forge components.

All prompts follow the Wayfinder Prompt Architecture Standard:
Mission, Inheritance, Inputs, Objectives, Tasks, Rules, Validation, Outputs,
Prohibited, and Success Criteria.
"""

from __future__ import annotations

import json

from ..types import ContextBundle


def build_diff_prompt(context: ContextBundle) -> str:
    """Request a bounded unified diff only.

    Runtime: O(excerpt count + constraint count), bounded by ContextBundle.
    Memory: O(rendered prompt size), bounded by caller context limits.
    Failure cases: malformed context is surfaced by normal Python exceptions.
    Deterministic behavior: same ContextBundle produces same prompt.
    """

    files = "\n".join(f"- {path}" for path in context.excerpts) or "- none"
    excerpts = "\n\n".join(
        f"FILE {path}\n{body}" for path, body in context.excerpts.items()
    )
    constraints = list(context.task.constraints)
    constraints.extend(
        str(item) for item in list((context.plan or {}).get("constraints", []))
    )
    rendered_constraints = (
        "\n".join(f"- {item}" for item in constraints)
        or "- preserve behavior unless tests demand change"
    )
    plan = json.dumps(context.plan or {}, indent=2, sort_keys=True)
    return f"""Mission
Produce the smallest bounded unified diff for the requested engineering task.

Inheritance
- Prompt Architecture Standard.
- Wayfinder constitutional and repository rules already loaded by caller.
- ContextBundle source excerpts and optional plan.

Inputs
- Summary: {context.task.summary}
- Scope: {context.task.scope}
- Todo: {context.task.todo}
- Known hot regions: {list(context.ban_hotspots)}
- Target files:
{files}
- Constraints:
{rendered_constraints}
- Plan:
{plan}
- Repository excerpts:
{excerpts}

Objectives
- Implement only the requested change.
- Preserve behavior unless tests or task constraints require change.
- Touch only files required by the task.

Tasks
1. Inspect inherited context.
2. Choose the minimal patch surface.
3. Emit a unified diff.

Rules
- Output a diff only.
- Start with "diff --git" whenever possible.
- Do not use markdown fences.
- Do not invent files outside the target/problem area unless necessary for tests.

Validation
- Diff applies cleanly.
- Diff is limited to task-relevant files.
- Diff preserves stated constraints.

Outputs
- Unified diff only.

Prohibited
- Explanations.
- Markdown.
- Architectural rewrites.
- Unrequested refactors.

Success Criteria
Does the diff implement the requested task with the smallest bounded patch?
"""


def build_plan_prompt(context: ContextBundle) -> str:
    """Ask the planner for bounded structured guidance.

    Runtime: O(excerpt count), bounded by ContextBundle.
    Memory: O(rendered prompt size), bounded by caller context limits.
    Failure cases: malformed context is surfaced by normal Python exceptions.
    Deterministic behavior: same ContextBundle produces same prompt.
    """

    files = "\n".join(f"- {path}" for path in context.excerpts) or "- none"
    return f"""Mission
Produce bounded implementation guidance for one coding task.

Inheritance
- Prompt Architecture Standard.
- Wayfinder constitutional and repository rules already loaded by caller.
- ContextBundle task and file candidates.

Inputs
- Summary: {context.task.summary}
- Scope: {context.task.scope}
- Todo: {context.task.todo}
- Known hot regions: {list(context.ban_hotspots)}
- Current candidate files:
{files}

Objectives
- Identify likely target files.
- Identify implementation strategies.
- Identify risks and constraints.

Tasks
1. Read the task and candidate files.
2. Select bounded target files.
3. Return structured plan JSON.

Rules
- Plan only.
- Do not emit code.
- Do not restate inherited architecture.

Validation
- JSON is parseable.
- JSON contains all required keys.
- Plan is bounded to the task scope.

Outputs
- JSON with keys: target_files, strategies, risk_map, constraints.

Prohibited
- Patches.
- Prose outside JSON.
- New architecture.

Success Criteria
Does the plan provide enough bounded guidance for the diff pass?
"""


def build_attack_prompt(context: ContextBundle, delta: str, mode: str) -> str:
    """Ask for a structured adversarial critique.

    Runtime: O(diff size), bounded by caller context limits.
    Memory: O(rendered prompt size), bounded by caller context limits.
    Failure cases: malformed context is surfaced by normal Python exceptions.
    Deterministic behavior: same ContextBundle, delta, and mode produce same prompt.
    """

    return f"""Mission
Critique one candidate diff for engineering risk.

Inheritance
- Prompt Architecture Standard.
- Wayfinder constitutional and repository rules already loaded by caller.
- Candidate diff from the diff pass.

Inputs
- Mode: {mode}
- Task: {context.task.summary}
- Diff:
{delta}

Objectives
- Identify logic breaks.
- Identify edge cases and regressions.
- Identify exploitability and minimal repro inputs.

Tasks
1. Inspect the candidate diff.
2. Model plausible failure paths.
3. Return structured red-team JSON.

Rules
- Critique only.
- Prefer concrete repro inputs.
- Preserve task intent.

Validation
- JSON is parseable.
- Findings are tied to the supplied diff.
- Risk is calibrated to observable behavior.

Outputs
- JSON with keys: risk, findings, attacker, repro_inputs, counterfactuals.

Prohibited
- Patches.
- Architectural rewrites.
- Prose outside JSON.

Success Criteria
Does the critique expose the most important risk in the candidate diff?
"""
