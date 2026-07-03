import jarvis.execution_bridge as bridge_module
from execution_runtime.interfaces import ExecutionRuntimeResponse
from jarvis import JarvisExecutionBridge
from provenance import noncanonical_external_output


class FakeProvider:
    provider_name = "odysseus"

    def __init__(self) -> None:
        self.requests = []

    def send(self, request):
        self.requests.append(request)
        return ExecutionRuntimeResponse(
            status="ok",
            provider="odysseus",
            content="workspace reply",
            provenance=noncanonical_external_output(
                source_system="odysseus",
                source_adapter="external.odysseus.workspace",
                source_session_id=request.session_id,
                request_id="req-1",
                timestamp=0,
                trace_id="trace-1",
            ),
            canonical=False,
        )


def test_bridge_fails_gracefully_when_execution_runtime_none():
    bridge = JarvisExecutionBridge({"EXECUTION_RUNTIME": "none"})

    result = bridge.send_workspace_prompt("session-1", "hello")

    assert result.status == "error"
    assert result.provider == "none"
    assert result.canonical is False
    assert result.failure is not None
    assert result.failure.error_code == "EXECUTION_RUNTIME_DISABLED"


def test_bridge_uses_registry_and_mocked_odysseus_provider(monkeypatch):
    fake_provider = FakeProvider()

    def fake_build_provider(values=None):
        assert values == {"EXECUTION_RUNTIME": "odysseus"}
        return fake_provider

    monkeypatch.setattr(bridge_module.execution_runtime_registry, "build_execution_runtime_provider", fake_build_provider)
    bridge = JarvisExecutionBridge({"EXECUTION_RUNTIME": "odysseus"})

    result = bridge.send_workspace_prompt(" session-1 ", "hello", context={"route": "workspace"})

    assert result.status == "ok"
    assert result.provider == "odysseus"
    assert result.content == "workspace reply"
    assert result.canonical is False
    assert result.provenance is not None
    assert result.provenance.canonical is False
    assert result.provenance.source_adapter == "external.odysseus.workspace"
    assert len(fake_provider.requests) == 1
    assert fake_provider.requests[0].session_id == "session-1"
    assert fake_provider.requests[0].prompt == "hello\n\nContext:\n- route: workspace"


def test_denied_permission_never_reaches_execution_runtime(monkeypatch):
    def deny_request(_request):
        return type(
            "Decision",
            (),
            {
                "allowed": False,
                "status": "denied",
                "capability_id": "execution_runtime.workspace_prompt",
                "intent": "workspace.prompt.write",
                "reason": "mutation intents are denied by default",
                "requires_confirmation": False,
            },
        )()

    def fail_build_provider(values=None):
        raise AssertionError("denied requests must not reach Execution Runtime registry")

    monkeypatch.setattr(bridge_module, "check_execution_permission", deny_request)
    monkeypatch.setattr(bridge_module.execution_runtime_registry, "build_execution_runtime_provider", fail_build_provider)

    result = JarvisExecutionBridge({"EXECUTION_RUNTIME": "odysseus"}).send_workspace_prompt("session-1", "hello")

    assert result.status == "error"
    assert result.failure is not None
    assert result.failure.error_code == "JARVIS_EXECUTION_PERMISSION_DENIED"
