"""Artifact promotion intake membrane.

This module converts noncanonical Execution Runtime output into review candidates only.
It does not create observations, persist artifacts, or write to ARK.
"""

from __future__ import annotations

from execution_runtime.interfaces import ExecutionRuntimeResponse

from .interfaces import CandidateArtifact, freeze_metadata, normalize_artifact_type


def create_candidate_from_runtime_response(
    response: ExecutionRuntimeResponse,
    artifact_type: str,
    summary: str | None = None,
) -> CandidateArtifact:
    """Create a candidate artifact from noncanonical Execution Runtime output.

    Inputs: ExecutionRuntimeResponse, artifact type, optional summary.
    Outputs: CandidateArtifact with status="candidate".
    Runtime: O(content length + summary length), bounded by upstream Execution Runtime
    caps and metadata caps.
    Memory: O(content length + metadata keys).
    Failure: raises ValueError for failed response, missing content, missing
    provenance, canonical provenance, or invalid artifact type.
    Deterministic: yes.
    """

    if response.status != "ok":
        raise ValueError("host response must be successful")
    if response.content is None or not response.content.strip():
        raise ValueError("host response content is required")
    if response.provenance is None:
        raise ValueError("host response provenance is required")
    if response.provenance.canonical:
        raise ValueError("canonical provenance cannot enter artifact intake")
    normalized_type = normalize_artifact_type(artifact_type)
    artifact_id = _candidate_id(response.provider, normalized_type, response.provenance.request_id)
    metadata = {
        "source_provider": response.provider,
        "source_session_id": response.provenance.source_session_id,
    }
    if summary is not None and summary.strip():
        metadata["summary"] = summary.strip()
    return CandidateArtifact(
        artifact_id=artifact_id,
        artifact_type=normalized_type,
        content=response.content,
        provenance=response.provenance,
        status="candidate",
        metadata=freeze_metadata(metadata),
    )


def create_candidate_from_host_response(
    response: ExecutionRuntimeResponse,
    artifact_type: str,
    summary: str | None = None,
) -> CandidateArtifact:
    """Compatibility wrapper for create_candidate_from_runtime_response."""

    return create_candidate_from_runtime_response(response, artifact_type, summary)


def _candidate_id(provider: str, artifact_type: str, request_id: str) -> str:
    return f"candidate:{provider.strip().lower()}:{artifact_type}:{request_id.strip()}"
