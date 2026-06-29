"""Capability execution permission checks.

Contract:
- Inputs: explicit ExecutionRequest records.
- Outputs: immutable permission decisions.
- Runtime constraint: O(intent length + capability length), bounded by request
  field caps enforced by callers.
- Memory assumption: O(1).
- Failure cases: unknown capability, mutation intent, and unconfirmed tool
  execution are denied structurally.
- Determinism: policy decisions are deterministic for explicit request inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from execution.interfaces import ExecutionRequest

PermissionStatus = Literal["allowed", "denied", "requires_confirmation"]
WORKSPACE_PROMPT_CAPABILITY = "host_shell.workspace_prompt"
TOOL_EXECUTION_CAPABILITY = "host_shell.tool_execution"
KNOWN_CAPABILITIES = (WORKSPACE_PROMPT_CAPABILITY, TOOL_EXECUTION_CAPABILITY)
MUTATION_INTENT_TOKENS = ("mutate", "write", "delete", "update", "create", "persist", "promote")


@dataclass(frozen=True)
class CapabilityPermission:
    """Static permission rule descriptor."""

    capability_id: str
    allowed_read_only: bool
    mutation_allowed: bool
    tool_execution_requires_confirmation: bool


@dataclass(frozen=True)
class PermissionDecision:
    """Structured permission decision."""

    status: PermissionStatus
    allowed: bool
    capability_id: str
    intent: str
    reason: str
    requires_confirmation: bool = False


def check_execution_permission(request: ExecutionRequest) -> PermissionDecision:
    """Check whether an execution request may proceed.

    Inputs: ExecutionRequest.
    Outputs: PermissionDecision.
    Runtime: O(intent token count), bounded by MUTATION_INTENT_TOKENS.
    Memory: O(1).
    Failure: none; denied requests return PermissionDecision.
    Deterministic: yes.
    """

    capability_id = request.capability_id.strip()
    intent = request.intent.strip().lower()
    if capability_id not in KNOWN_CAPABILITIES:
        return PermissionDecision(
            status="denied",
            allowed=False,
            capability_id=capability_id,
            intent=intent,
            reason="unknown capability_id",
        )
    if _is_mutation_intent(intent):
        return PermissionDecision(
            status="denied",
            allowed=False,
            capability_id=capability_id,
            intent=intent,
            reason="mutation intents are denied by default",
        )
    if capability_id == TOOL_EXECUTION_CAPABILITY or intent.startswith("tool."):
        if bool(request.constraints.get("explicit_confirmation")):
            return PermissionDecision(
                status="allowed",
                allowed=True,
                capability_id=capability_id,
                intent=intent,
                reason="tool execution explicitly confirmed",
            )
        return PermissionDecision(
            status="requires_confirmation",
            allowed=False,
            capability_id=capability_id,
            intent=intent,
            reason="tool execution requires explicit confirmation",
            requires_confirmation=True,
        )
    if capability_id == WORKSPACE_PROMPT_CAPABILITY and _is_read_only_workspace_prompt(intent):
        return PermissionDecision(
            status="allowed",
            allowed=True,
            capability_id=capability_id,
            intent=intent,
            reason="read-only workspace prompt allowed",
        )
    return PermissionDecision(
        status="denied",
        allowed=False,
        capability_id=capability_id,
        intent=intent,
        reason="intent is not allowed for capability",
    )


def _is_read_only_workspace_prompt(intent: str) -> bool:
    return intent in {"workspace.prompt.read", "read.workspace_prompt", "workspace.read"}


def _is_mutation_intent(intent: str) -> bool:
    for token in MUTATION_INTENT_TOKENS:
        if token in intent:
            return True
    return False
