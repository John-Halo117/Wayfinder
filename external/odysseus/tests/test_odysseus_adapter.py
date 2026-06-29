from types import MappingProxyType
from typing import Mapping

from external.odysseus import (
    HttpResponse,
    OdysseusPromptRequest,
    OdysseusWorkspaceAdapter,
    register_odysseus_workspace_capability,
)
from external.odysseus.config import load_odysseus_config


class FakeTransport:
    def __init__(self, responses: tuple[HttpResponse, ...] = (), timeout: bool = False) -> None:
        self.responses = responses
        self.timeout = timeout
        self.calls: list[tuple[str, str, Mapping[str, object] | None, float, int]] = []

    def request_json(
        self,
        method: str,
        url: str,
        payload: Mapping[str, object] | None,
        timeout_seconds: float,
        max_response_bytes: int,
    ) -> HttpResponse:
        self.calls.append((method, url, payload, timeout_seconds, max_response_bytes))
        if self.timeout:
            raise TimeoutError("timed out")
        if not self.responses:
            raise OSError("no fake response configured")
        return self.responses[min(len(self.calls) - 1, len(self.responses) - 1)]


def test_disabled_adapter_health_does_not_call_transport():
    config = load_odysseus_config({"ODYSSEUS_ENABLED": "false"})
    transport = FakeTransport()
    adapter = OdysseusWorkspaceAdapter(config, transport)

    health = adapter.health()

    assert health.status == "disabled"
    assert health.available is False
    assert transport.calls == []


def test_health_reports_available_with_mock_response():
    config = load_odysseus_config(
        {
            "ODYSSEUS_ENABLED": "true",
            "ODYSSEUS_BASE_URL": "http://127.0.0.1:7000",
            "ODYSSEUS_TIMEOUT_SECONDS": "2",
        }
    )
    transport = FakeTransport((HttpResponse(200, b'{"status":"healthy"}', MappingProxyType({})),))
    adapter = OdysseusWorkspaceAdapter(config, transport)

    health = adapter.health()

    assert health.status == "ok"
    assert health.available is True
    assert transport.calls[0][0] == "GET"
    assert transport.calls[0][1] == "http://127.0.0.1:7000/api/health"


def test_send_prompt_returns_response_with_noncanonical_provenance():
    config = load_odysseus_config(
        {
            "ODYSSEUS_ENABLED": "true",
            "ODYSSEUS_BASE_URL": "http://127.0.0.1:7000",
            "ODYSSEUS_TIMEOUT_SECONDS": "2",
        }
    )
    transport = FakeTransport((HttpResponse(200, b'{"response":"Workspace reply"}', MappingProxyType({})),))
    adapter = OdysseusWorkspaceAdapter(config, transport)

    result = adapter.send_prompt(OdysseusPromptRequest(prompt="  hello  ", session_id="session-1"))

    assert result.status == "ok"
    assert result.response == "Workspace reply"
    assert result.provenance is not None
    assert result.provenance.canonical is False
    assert result.provenance.source_system == "odysseus"
    assert result.provenance.source_adapter == "external.odysseus.workspace"
    assert result.provenance.source_session_id == "session-1"
    assert transport.calls[0][0] == "POST"
    assert transport.calls[0][2] == {
        "message": "hello",
        "session": "session-1",
        "use_web": False,
        "use_research": False,
    }


def test_send_prompt_rejects_empty_prompt_without_network_call():
    config = load_odysseus_config(
        {
            "ODYSSEUS_ENABLED": "true",
            "ODYSSEUS_BASE_URL": "http://127.0.0.1:7000",
        }
    )
    transport = FakeTransport()
    adapter = OdysseusWorkspaceAdapter(config, transport)

    result = adapter.send_prompt(OdysseusPromptRequest(prompt=" ", session_id="session-1"))

    assert result.status == "error"
    assert result.failure is not None
    assert result.failure.error_code == "ODYSSEUS_PROMPT_INVALID"
    assert transport.calls == []


def test_send_prompt_maps_http_error_to_structured_failure():
    config = load_odysseus_config(
        {
            "ODYSSEUS_ENABLED": "true",
            "ODYSSEUS_BASE_URL": "http://127.0.0.1:7000",
        }
    )
    transport = FakeTransport((HttpResponse(503, b'{"detail":"down"}', MappingProxyType({})),))
    adapter = OdysseusWorkspaceAdapter(config, transport)

    result = adapter.send_prompt(OdysseusPromptRequest(prompt="hello", session_id="session-1"))

    assert result.status == "error"
    assert result.failure is not None
    assert result.failure.error_code == "ODYSSEUS_HTTP_ERROR"
    assert result.failure.context["status_code"] == 503


def test_capability_registration_is_minimal_and_noncanonical():
    registration = register_odysseus_workspace_capability()

    assert registration.status == "ok"
    assert registration.capability_id == "external.odysseus.workspace"
    assert registration.display_name == "Odysseus Workspace"
    assert registration.owns_canonical_state is False
    assert registration.allowed_calls == ("health", "send_prompt", "receive_response")
