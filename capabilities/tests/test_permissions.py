from capabilities.permissions import (
    TOOL_EXECUTION_CAPABILITY,
    WORKSPACE_PROMPT_CAPABILITY,
    check_execution_permission,
)
from execution.interfaces import ExecutionRequest, freeze_mapping


def _request(capability_id: str, intent: str, constraints=None) -> ExecutionRequest:
    return ExecutionRequest(
        request_id="req-1",
        actor="jarvis",
        intent=intent,
        capability_id=capability_id,
        payload=freeze_mapping({}),
        constraints=freeze_mapping(constraints or {}),
    )


def test_allowed_workspace_prompt_passes():
    decision = check_execution_permission(_request(WORKSPACE_PROMPT_CAPABILITY, "workspace.prompt.read"))

    assert decision.allowed is True
    assert decision.status == "allowed"


def test_unknown_capability_denied():
    decision = check_execution_permission(_request("unknown.capability", "workspace.prompt.read"))

    assert decision.allowed is False
    assert decision.status == "denied"
    assert decision.reason == "unknown capability_id"


def test_mutation_intent_denied():
    decision = check_execution_permission(_request(WORKSPACE_PROMPT_CAPABILITY, "workspace.prompt.write"))

    assert decision.allowed is False
    assert decision.status == "denied"
    assert "mutation" in decision.reason


def test_tool_execution_requires_confirmation():
    decision = check_execution_permission(_request(TOOL_EXECUTION_CAPABILITY, "tool.execute"))

    assert decision.allowed is False
    assert decision.status == "requires_confirmation"
    assert decision.requires_confirmation is True


def test_tool_execution_with_confirmation_allowed():
    decision = check_execution_permission(
        _request(TOOL_EXECUTION_CAPABILITY, "tool.execute", {"explicit_confirmation": True})
    )

    assert decision.allowed is True
    assert decision.status == "allowed"
