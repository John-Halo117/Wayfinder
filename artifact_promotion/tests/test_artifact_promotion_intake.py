from dataclasses import replace

import pytest

from artifact_promotion import CandidateArtifact, create_candidate_from_host_response, review_candidate
from host_shell.interfaces import HostShellResponse
from provenance import noncanonical_external_output
from provenance.interfaces import ProvenanceRecord


def _provenance(canonical: bool = False) -> ProvenanceRecord:
    base = noncanonical_external_output(
        source_system="odysseus",
        source_adapter="external.odysseus.workspace",
        source_session_id="session-1",
        request_id="req-1",
        timestamp=1,
        trace_id="trace-1",
    )
    if canonical:
        return replace(base, canonical=True)
    return base


_DEFAULT_PROVENANCE = object()


def _host_response(provenance: ProvenanceRecord | None | object = _DEFAULT_PROVENANCE) -> HostShellResponse:
    return HostShellResponse(
        status="ok",
        provider="odysseus",
        content="workspace output",
        provenance=_provenance() if provenance is _DEFAULT_PROVENANCE else provenance,
        canonical=False,
    )


def test_noncanonical_host_shell_response_can_become_candidate_artifact():
    candidate = create_candidate_from_host_response(_host_response(), "workspace_note", summary="review this")

    assert isinstance(candidate, CandidateArtifact)
    assert candidate.status == "candidate"
    assert candidate.artifact_type == "workspace_note"
    assert candidate.content == "workspace output"
    assert candidate.provenance.canonical is False
    assert candidate.metadata["summary"] == "review this"


def test_canonical_response_is_rejected_by_intake():
    response = _host_response(_provenance(canonical=True))

    with pytest.raises(ValueError, match="canonical provenance"):
        create_candidate_from_host_response(response, "workspace_note")


def test_missing_provenance_is_rejected_by_intake():
    response = _host_response(provenance=None)

    with pytest.raises(ValueError, match="provenance is required"):
        create_candidate_from_host_response(response, "workspace_note")


def test_accepted_decision_still_does_not_write_to_ark(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("artifact review must not write to ARK")

    monkeypatch.setattr("builtins.open", fail_if_called)
    candidate = create_candidate_from_host_response(_host_response(), "workspace_note")

    decision = review_candidate(candidate, "accepted", reviewer="tester", reason="looks useful")

    assert decision.status == "accepted"
    assert decision.artifact_id == candidate.artifact_id
    assert decision.reason == "looks useful"
    assert decision.provenance == candidate.provenance


def test_rejected_decision_preserves_provenance():
    candidate = create_candidate_from_host_response(_host_response(), "workspace_note")

    decision = review_candidate(candidate, "rejected", reviewer="tester", reason="not relevant")

    assert decision.status == "rejected"
    assert decision.provenance == candidate.provenance
    assert decision.provenance.canonical is False
