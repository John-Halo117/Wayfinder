from artifact_promotion import CandidateArtifact
from external.odysseus import HttpResponse, OdysseusPromptRequest, OdysseusWorkspaceAdapter
from external.odysseus.config import load_odysseus_config
from host_shell import HostShellRequest, build_host_shell_provider
from host_shell.providers.odysseus import OdysseusHostShellProvider
from provenance import noncanonical_external_output


class FakeTransport:
    def __init__(self, responses: tuple[HttpResponse, ...] = ()) -> None:
        self.responses = responses
        self.calls: list[tuple[str, str, object, float, int]] = []

    def request_json(self, method: str, url: str, payload: object, timeout_seconds: float, max_response_bytes: int):
        self.calls.append((method, url, payload, timeout_seconds, max_response_bytes))
        if not self.responses:
            raise OSError("no fake response configured")
        return self.responses[min(len(self.calls) - 1, len(self.responses) - 1)]


class FakeOdysseusAdapter:
    def __init__(self) -> None:
        self.requests: list[OdysseusPromptRequest] = []

    def health(self):
        return type(
            "Health",
            (),
            {
                "status": "ok",
                "enabled": True,
                "available": True,
                "failure": None,
            },
        )()

    def send_prompt(self, request: OdysseusPromptRequest):
        self.requests.append(request)
        provenance = noncanonical_external_output(
            source_system="odysseus",
            source_adapter="external.odysseus.workspace",
            source_session_id=request.session_id,
            request_id=request.request_id or f"odysseus:{request.session_id}",
            timestamp=request.timestamp,
            trace_id=request.trace_id or f"odysseus:{request.session_id}",
        )
        return type(
            "Result",
            (),
            {
                "status": "ok",
                "response": "delegated response",
                "provenance": provenance,
                "failure": None,
            },
        )()


def test_registry_disabled_mode_returns_noop_provider_without_network():
    provider = build_host_shell_provider({"HOST_SHELL": "none"})

    health = provider.health()
    response = provider.send(HostShellRequest(prompt="hello", session_id="session-1"))

    assert health.status == "disabled"
    assert health.available is False
    assert health.canonical is False
    assert response.status == "error"
    assert response.failure is not None
    assert response.failure.error_code == "HOST_SHELL_DISABLED"


def test_registry_odysseus_mode_builds_provider_without_health_probe():
    values = {
        "HOST_SHELL": "odysseus",
        "ODYSSEUS_ENABLED": "true",
        "ODYSSEUS_BASE_URL": "http://127.0.0.1:7000",
        "ODYSSEUS_TIMEOUT_SECONDS": "2",
    }

    provider = build_host_shell_provider(values)

    assert isinstance(provider, OdysseusHostShellProvider)
    assert provider.provider_name == "odysseus"


def test_registry_odysseus_mode_has_no_network_side_effects(monkeypatch):
    def fail_urlopen(*args, **kwargs):
        raise AssertionError("registry construction must not open network connections")

    monkeypatch.setattr("external.odysseus.adapter.urlopen", fail_urlopen)

    provider = build_host_shell_provider(
        {
            "HOST_SHELL": "odysseus",
            "ODYSSEUS_ENABLED": "true",
            "ODYSSEUS_BASE_URL": "http://127.0.0.1:7000",
        }
    )

    assert provider.provider_name == "odysseus"


def test_odysseus_provider_delegates_safely():
    adapter = FakeOdysseusAdapter()
    provider = OdysseusHostShellProvider(adapter)  # type: ignore[arg-type]

    response = provider.send(HostShellRequest(prompt="  hello  ", session_id=" session-1 "))

    assert response.status == "ok"
    assert response.content == "delegated response"
    assert response.provider == "odysseus"
    assert adapter.requests == [OdysseusPromptRequest(prompt="hello", session_id="session-1", include_provenance=True)]


def test_host_shell_response_remains_noncanonical_with_real_adapter_mock():
    config = load_odysseus_config(
        {
            "ODYSSEUS_ENABLED": "true",
            "ODYSSEUS_BASE_URL": "http://127.0.0.1:7000",
            "ODYSSEUS_TIMEOUT_SECONDS": "2",
        }
    )
    transport = FakeTransport((HttpResponse(200, b'{"response":"Workspace reply"}'),))
    provider = OdysseusHostShellProvider(OdysseusWorkspaceAdapter(config, transport))

    response = provider.send(HostShellRequest(prompt="hello", session_id="session-1"))

    assert response.status == "ok"
    assert response.canonical is False
    assert response.provenance is not None
    assert response.provenance.canonical is False
    assert response.provenance.source_adapter == "external.odysseus.workspace"
    assert transport.calls[0][0] == "POST"


def test_host_shell_response_is_not_candidate_artifact_or_observation():
    adapter = FakeOdysseusAdapter()
    provider = OdysseusHostShellProvider(adapter)  # type: ignore[arg-type]

    response = provider.send(HostShellRequest(prompt="hello", session_id="session-1"))

    assert not isinstance(response, CandidateArtifact)
    assert not hasattr(response, "observation")
    assert not hasattr(response, "artifact_id")
