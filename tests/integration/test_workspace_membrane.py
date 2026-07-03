from __future__ import annotations

import builtins
import sys
from dataclasses import replace
from secrets import token_hex
from typing import Callable

import pytest

from ark_admission import AdmissionCandidate, create_admission_candidate
from artifact_promotion import CandidateArtifact, create_candidate_from_runtime_response, review_candidate
from execution_runtime.interfaces import ExecutionRuntimeRequest, ExecutionRuntimeResponse
from jarvis import JarvisExecutionBridge
from provenance import ProvenanceRecord, noncanonical_external_output


class MockOdysseusExecutionRuntime:
    """Registry-instantiated Odysseus provider mock with bounded call capture."""

    provider_name = "odysseus"
    instances: list["MockOdysseusExecutionRuntime"] = []
    response_factory: Callable[[ExecutionRuntimeRequest], ExecutionRuntimeResponse]

    def __init__(self, adapter: object) -> None:
        self.adapter = adapter
        self.requests: list[ExecutionRuntimeRequest] = []
        self.responses: list[ExecutionRuntimeResponse] = []
        self.__class__.instances.append(self)

    def send(self, request: ExecutionRuntimeRequest) -> ExecutionRuntimeResponse:
        self.requests.append(request)
        response = self.__class__.response_factory(request)
        self.responses.append(response)
        return response


@pytest.fixture
def side_effect_guards(monkeypatch):
    before_ark_modules = {name for name in sys.modules if name.startswith("engines.ark")}

    def fail_open(*args, **kwargs):
        raise AssertionError("workspace membrane test must not persist data")

    def fail_urlopen(*args, **kwargs):
        raise AssertionError("workspace membrane test must not make network calls")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr("external.odysseus.adapter.urlopen", fail_urlopen)
    yield
    after_ark_modules = {name for name in sys.modules if name.startswith("engines.ark")}
    assert after_ark_modules == before_ark_modules


@pytest.fixture
def mocked_registry(monkeypatch):
    MockOdysseusExecutionRuntime.instances = []
    monkeypatch.setattr("execution_runtime.registry.OdysseusExecutionRuntime", MockOdysseusExecutionRuntime)
    return MockOdysseusExecutionRuntime


def _bridge() -> JarvisExecutionBridge:
    return JarvisExecutionBridge(
        {
            "EXECUTION_RUNTIME": "odysseus",
            "ODYSSEUS_ENABLED": "true",
            "ODYSSEUS_BASE_URL": "http://127.0.0.1:7000",
            "ODYSSEUS_TIMEOUT_SECONDS": "2",
        }
    )


def _provenance(request: ExecutionRuntimeRequest, *, canonical: bool = False) -> ProvenanceRecord:
    record = noncanonical_external_output(
        source_system="odysseus",
        source_adapter="execution_runtime.providers.odysseus",
        source_session_id=request.session_id,
        request_id=request.request_id or "req-fixed",
        timestamp=request.timestamp,
        trace_id=request.trace_id or "trace-fixed",
    )
    if canonical:
        return replace(record, canonical=True)
    return record


_DEFAULT_PROVENANCE = object()


def _response(
    request: ExecutionRuntimeRequest,
    *,
    content: str = "workspace synthesis",
    provenance: ProvenanceRecord | None | object = _DEFAULT_PROVENANCE,
    canonical: bool = False,
) -> ExecutionRuntimeResponse:
    return ExecutionRuntimeResponse(
        status="ok",
        provider="odysseus",
        content=content,
        provenance=_provenance(request, canonical=canonical) if provenance is _DEFAULT_PROVENANCE else provenance,
        canonical=canonical,
    )


def _last_runtime_response(provider_class: type[MockOdysseusExecutionRuntime]) -> ExecutionRuntimeResponse:
    assert len(provider_class.instances) == 1
    provider = provider_class.instances[0]
    assert len(provider.responses) == 1
    return provider.responses[0]


def test_happy_path_noncanonical_workspace_membrane(mocked_registry, side_effect_guards):
    request_id = "req-happy"
    trace_id = "trace-happy"

    def response_factory(request: ExecutionRuntimeRequest) -> ExecutionRuntimeResponse:
        return _response(
            replace(request, request_id=request_id, trace_id=trace_id, timestamp=7),
            content="reviewable workspace output",
        )

    mocked_registry.response_factory = response_factory

    jarvis_result = _bridge().send_workspace_prompt("session-1", "summarize workspace")
    runtime_response = _last_runtime_response(mocked_registry)
    candidate = create_candidate_from_runtime_response(runtime_response, "workspace_summary", summary="membrane test")
    decision = review_candidate(candidate, "accepted", reviewer="integration-test", reason="ready")
    admission = create_admission_candidate(candidate, decision)

    assert jarvis_result.status == "ok"
    assert runtime_response.status == "ok"
    assert candidate.status == "candidate"
    assert decision.status == "accepted"
    assert admission.status == "ready_for_observation"
    assert jarvis_result.canonical is False
    assert runtime_response.canonical is False
    assert candidate.provenance.canonical is False
    assert decision.provenance.canonical is False
    assert admission.provenance.canonical is False
    assert admission.trace_id == trace_id
    assert admission.request_id == request_id
    assert candidate.provenance.trace_id == trace_id
    assert decision.provenance.trace_id == trace_id
    assert candidate.provenance.request_id == request_id
    assert decision.provenance.request_id == request_id
    assert candidate.provenance == decision.provenance == admission.provenance
    assert decision.artifact_id == candidate.artifact_id
    assert admission.artifact_id == candidate.artifact_id
    assert not hasattr(runtime_response, "observation")
    assert not hasattr(candidate, "observation")
    assert not hasattr(decision, "observation")
    assert not hasattr(admission, "observation")


def test_missing_provenance_stops_before_candidate_and_admission(mocked_registry, side_effect_guards):
    mocked_registry.response_factory = lambda request: _response(request, provenance=None)

    jarvis_result = _bridge().send_workspace_prompt("session-1", "summarize workspace")
    runtime_response = _last_runtime_response(mocked_registry)
    candidate = None
    admission = None

    assert jarvis_result.status == "ok"
    assert runtime_response.provenance is None
    with pytest.raises(ValueError, match="provenance is required"):
        candidate = create_candidate_from_runtime_response(runtime_response, "workspace_summary")

    assert candidate is None
    assert admission is None


def test_canonical_response_is_rejected_before_promotion(mocked_registry, side_effect_guards):
    mocked_registry.response_factory = lambda request: _response(request, canonical=True)

    _bridge().send_workspace_prompt("session-1", "summarize workspace")
    runtime_response = _last_runtime_response(mocked_registry)
    candidate = None
    decision = None
    admission = None

    assert runtime_response.provenance is not None
    assert runtime_response.provenance.canonical is True
    with pytest.raises(ValueError, match="canonical provenance"):
        candidate = create_candidate_from_runtime_response(runtime_response, "workspace_summary")

    assert candidate is None
    assert decision is None
    assert admission is None


def test_rejected_review_cannot_enter_admission(mocked_registry, side_effect_guards):
    mocked_registry.response_factory = lambda request: _response(request)

    _bridge().send_workspace_prompt("session-1", "summarize workspace")
    runtime_response = _last_runtime_response(mocked_registry)
    candidate = create_candidate_from_runtime_response(runtime_response, "workspace_summary")
    decision = review_candidate(candidate, "rejected", reviewer="integration-test", reason="not useful")
    admission = None

    with pytest.raises(ValueError, match="must be accepted"):
        admission = create_admission_candidate(candidate, decision)

    assert admission is None
    assert decision.provenance == candidate.provenance
    assert decision.provenance.canonical is False


def test_trace_integrity_preserves_random_ids(mocked_registry, side_effect_guards):
    request_id = f"req-{token_hex(8)}"
    trace_id = f"trace-{token_hex(8)}"

    def response_factory(request: ExecutionRuntimeRequest) -> ExecutionRuntimeResponse:
        return _response(replace(request, request_id=request_id, trace_id=trace_id, timestamp=11))

    mocked_registry.response_factory = response_factory

    _bridge().send_workspace_prompt("session-1", "summarize workspace")
    runtime_response = _last_runtime_response(mocked_registry)
    candidate = create_candidate_from_runtime_response(runtime_response, "workspace_summary")
    decision = review_candidate(candidate, "accepted", reviewer="integration-test")
    admission = create_admission_candidate(candidate, decision)

    assert runtime_response.provenance is not None
    assert runtime_response.provenance.request_id == request_id
    assert runtime_response.provenance.trace_id == trace_id
    assert candidate.provenance.request_id == request_id
    assert candidate.provenance.trace_id == trace_id
    assert decision.provenance.request_id == request_id
    assert decision.provenance.trace_id == trace_id
    assert admission.request_id == request_id
    assert admission.trace_id == trace_id


def test_registry_disabled_stops_pipeline(side_effect_guards):
    bridge = JarvisExecutionBridge({"EXECUTION_RUNTIME": "none"})

    result = bridge.send_workspace_prompt("session-1", "summarize workspace")
    candidate = None

    assert result.status == "error"
    assert result.failure is not None
    assert result.failure.error_code == "EXECUTION_RUNTIME_DISABLED"
    assert result.canonical is False
    assert candidate is None
