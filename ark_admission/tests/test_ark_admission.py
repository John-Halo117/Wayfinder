from dataclasses import replace

import pytest

from ark_admission import AdmissionCandidate, create_admission_candidate
from artifact_promotion import CandidateArtifact, PromotionDecision, review_candidate
from provenance import noncanonical_external_output


def _provenance(canonical: bool = False):
    provenance = noncanonical_external_output(
        source_system="odysseus",
        source_adapter="external.odysseus.workspace",
        source_session_id="session-1",
        request_id="req-1",
        timestamp=1,
        trace_id="trace-1",
    )
    if canonical:
        return replace(provenance, canonical=True)
    return provenance


def _candidate(provenance=None) -> CandidateArtifact:
    return CandidateArtifact(
        artifact_id="candidate:odysseus:workspace_note:req-1",
        artifact_type="workspace_note",
        content="workspace output",
        provenance=_provenance() if provenance is None else provenance,
        status="candidate",
    )


def test_accepted_reviewed_candidate_becomes_admission_candidate():
    candidate = _candidate()
    decision = review_candidate(candidate, "accepted", reviewer="tester", reason="ready")

    admission = create_admission_candidate(candidate, decision)

    assert isinstance(admission, AdmissionCandidate)
    assert admission.status == "ready_for_observation"
    assert admission.artifact_id == candidate.artifact_id
    assert admission.request_id == "req-1"
    assert admission.trace_id == "trace-1"
    assert admission.provenance.canonical is False


def test_rejected_decision_cannot_become_admission_candidate():
    candidate = _candidate()
    decision = review_candidate(candidate, "rejected", reviewer="tester", reason="no")

    with pytest.raises(ValueError, match="must be accepted"):
        create_admission_candidate(candidate, decision)


def test_missing_provenance_is_rejected():
    candidate = _candidate(provenance=None)
    decision = PromotionDecision(
        artifact_id=candidate.artifact_id,
        status="accepted",
        reason="ready",
        reviewer="tester",
        provenance=None,  # type: ignore[arg-type]
    )

    with pytest.raises(ValueError, match="provenance is required"):
        create_admission_candidate(candidate, decision)


def test_canonical_provenance_is_rejected():
    candidate = _candidate(provenance=_provenance(canonical=True))
    decision = PromotionDecision(
        artifact_id=candidate.artifact_id,
        status="accepted",
        reason="ready",
        reviewer="tester",
        provenance=candidate.provenance,
    )

    with pytest.raises(ValueError, match="canonical"):
        create_admission_candidate(candidate, decision)


def test_no_ark_write_occurs(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("ARK admission contract must not write to ARK")

    monkeypatch.setattr("builtins.open", fail_if_called)
    candidate = _candidate()
    decision = review_candidate(candidate, "accepted", reviewer="tester", reason="ready")

    admission = create_admission_candidate(candidate, decision)

    assert admission.status == "ready_for_observation"
    assert not hasattr(admission, "observation")
