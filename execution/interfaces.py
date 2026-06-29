"""Execution boundary interfaces.

Contract:
- Inputs: explicit request id, actor, intent, capability id, payload,
  constraints, and optional parent provenance.
- Outputs: immutable execution request/response records.
- Runtime constraint: O(payload keys + constraint keys), bounded by local caps.
- Memory assumption: O(payload + constraints), bounded by local caps.
- Failure cases: invalid fields are rejected by construction helpers.
- Determinism: records are deterministic value objects.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from provenance import ProvenanceRecord


@dataclass(frozen=True)
class ExecutionRequest:
    """Explicit execution request boundary record."""

    request_id: str
    actor: str
    intent: str
    capability_id: str
    payload: Mapping[str, object]
    constraints: Mapping[str, object]
    provenance_parent: ProvenanceRecord | None = None


@dataclass(frozen=True)
class ExecutionResponse:
    """Explicit execution response boundary record."""

    status: str
    request_id: str
    actor: str
    capability_id: str
    result: Mapping[str, object]
    provenance: ProvenanceRecord | None = None
    error_code: str | None = None
    reason: str | None = None


def freeze_mapping(value: Mapping[str, object] | None = None) -> Mapping[str, object]:
    """Return an immutable shallow mapping.

    Inputs: optional mapping. Outputs: MappingProxyType.
    Runtime: O(key count), bounded by caller caps. Memory: O(key count).
    Failure: none. Deterministic: yes.
    """

    return MappingProxyType(dict(value or {}))
