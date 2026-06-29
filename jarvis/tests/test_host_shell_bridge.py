import jarvis.host_shell_bridge as bridge_module
from host_shell.interfaces import HostShellResponse
from jarvis import JarvisHostShellBridge
from provenance import noncanonical_external_output


class FakeProvider:
    provider_name = "odysseus"

    def __init__(self) -> None:
        self.requests = []

    def send(self, request):
        self.requests.append(request)
        return HostShellResponse(
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


def test_bridge_fails_gracefully_when_host_shell_none():
    bridge = JarvisHostShellBridge({"HOST_SHELL": "none"})

    result = bridge.send_workspace_prompt("session-1", "hello")

    assert result.status == "error"
    assert result.provider == "none"
    assert result.canonical is False
    assert result.failure is not None
    assert result.failure.error_code == "HOST_SHELL_DISABLED"


def test_bridge_uses_registry_and_mocked_odysseus_provider(monkeypatch):
    fake_provider = FakeProvider()

    def fake_build_provider(values=None):
        assert values == {"HOST_SHELL": "odysseus"}
        return fake_provider

    monkeypatch.setattr(bridge_module.host_shell_registry, "build_host_shell_provider", fake_build_provider)
    bridge = JarvisHostShellBridge({"HOST_SHELL": "odysseus"})

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


def test_denied_permission_never_reaches_host_shell(monkeypatch):
    def deny_request(_request):
        return type(
            "Decision",
            (),
            {
                "allowed": False,
                "status": "denied",
                "capability_id": "host_shell.workspace_prompt",
                "intent": "workspace.prompt.write",
                "reason": "mutation intents are denied by default",
                "requires_confirmation": False,
            },
        )()

    def fail_build_provider(values=None):
        raise AssertionError("denied requests must not reach Host Shell registry")

    monkeypatch.setattr(bridge_module, "check_execution_permission", deny_request)
    monkeypatch.setattr(bridge_module.host_shell_registry, "build_host_shell_provider", fail_build_provider)

    result = JarvisHostShellBridge({"HOST_SHELL": "odysseus"}).send_workspace_prompt("session-1", "hello")

    assert result.status == "error"
    assert result.failure is not None
    assert result.failure.error_code == "JARVIS_HOST_SHELL_PERMISSION_DENIED"
