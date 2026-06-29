"""Reusable provenance interfaces.

Contract:
- Inputs: explicit source, adapter, session, request, timestamp, and trace
  fields.
- Outputs: immutable provenance records.
- Runtime constraint: O(total field length), bounded by field caps.
- Memory assumption: O(total field length), bounded by field caps.
- Failure cases: missing or oversized required fields.
- Determinism: helper output is deterministic for explicit inputs.
"""

from __future__ import annotations

from dataclasses import dataclass

MAX_SOURCE_LENGTH = 128
MAX_ADAPTER_LENGTH = 160
MAX_SESSION_ID_LENGTH = 128
MAX_REQUEST_ID_LENGTH = 128
MAX_TRACE_ID_LENGTH = 128


@dataclass(frozen=True)
class ProvenanceRecord:
    """Reusable provenance record for runtime and adapter outputs."""

    canonical: bool
    source_system: str
    source_adapter: str
    source_session_id: str
    request_id: str
    timestamp: int
    trace_id: str


def noncanonical_external_output(
    *,
    source_system: str,
    source_adapter: str,
    source_session_id: str,
    request_id: str,
    timestamp: int,
    trace_id: str,
) -> ProvenanceRecord:
    """Build provenance for noncanonical external/runtime output.

    Inputs: source system, adapter, source session, request id, timestamp, trace id.
    Outputs: ProvenanceRecord with canonical=False.
    Runtime: O(total field length), bounded by caps.
    Memory: O(total field length).
    Failure: raises ValueError for invalid fields.
    Deterministic: yes.
    """

    return ProvenanceRecord(
        canonical=False,
        source_system=_normalize(source_system, "source_system", MAX_SOURCE_LENGTH),
        source_adapter=_normalize(source_adapter, "source_adapter", MAX_ADAPTER_LENGTH),
        source_session_id=_normalize(source_session_id, "source_session_id", MAX_SESSION_ID_LENGTH),
        request_id=_normalize(request_id, "request_id", MAX_REQUEST_ID_LENGTH),
        timestamp=_normalize_timestamp(timestamp),
        trace_id=_normalize(trace_id, "trace_id", MAX_TRACE_ID_LENGTH),
    )


def _normalize(value: str, field: str, max_length: int) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field} is required")
    if len(normalized) > max_length:
        raise ValueError(f"{field} exceeds maximum length")
    return normalized


def _normalize_timestamp(value: int) -> int:
    if isinstance(value, bool):
        raise ValueError("timestamp must be an integer")
    timestamp = int(value)
    if timestamp < 0:
        raise ValueError("timestamp must be non-negative")
    return timestamp
