"""Typed Odysseus workspace adapter interfaces.

Contract:
- Inputs: explicit dataclasses and primitive strings.
- Outputs: immutable records or structured failures.
- Runtime constraint: O(prompt bytes + response bytes), bounded by
  OdysseusConfig(max_prompt_chars, max_response_bytes, timeout_seconds).
- Memory assumption: O(max_prompt_chars + max_response_bytes), bounded by
  configuration caps.
- Failure cases: disabled adapter, invalid configuration, invalid prompt,
  missing session, HTTP timeout/error, malformed JSON, and oversized response.
- Determinism: validation and result shaping are deterministic when the injected
  transport is deterministic. Network behavior is isolated behind the adapter.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Protocol

from provenance import ProvenanceRecord

MAX_CONTEXT_KEYS = 32
MAX_CONTEXT_VALUE_LENGTH = 512
MAX_ERROR_CODE_LENGTH = 128
MAX_REASON_LENGTH = 512
MAX_URL_LENGTH = 512
MAX_PATH_LENGTH = 128
MAX_SESSION_ID_LENGTH = 128
MAX_PROMPT_CHARS = 50_000
MAX_RESPONSE_BYTES = 1_048_576
MAX_RESPONSE_CHARS = 200_000
DEFAULT_TIMEOUT_SECONDS = 5.0
MIN_TIMEOUT_SECONDS = 0.1
MAX_TIMEOUT_SECONDS = 30.0
DEFAULT_CHAT_PATH = "/api/chat"
DEFAULT_HEALTH_PATH = "/api/health"
CAPABILITY_ID = "external.odysseus.workspace"


@dataclass(frozen=True)
class Failure:
    """Standard structured failure object.

    Runtime: O(context key count), bounded by MAX_CONTEXT_KEYS.
    Memory: O(context key count).
    Failure: raises ValueError for oversized context.
    Deterministic: yes.
    """

    status: str
    error_code: str
    reason: str
    context: Mapping[str, object]
    recoverable: bool

    @classmethod
    def build(
        cls,
        error_code: str,
        reason: str,
        context: Mapping[str, object] | None = None,
        recoverable: bool = True,
    ) -> "Failure":
        normalized = dict(context or {})
        if len(normalized) > MAX_CONTEXT_KEYS:
            raise ValueError("failure context exceeds maximum key count")
        checked_context: dict[str, object] = {}
        for key, value in normalized.items():
            key_text = _normalize_text(str(key), field="context key", max_length=MAX_ERROR_CODE_LENGTH)
            if len(str(value)) > MAX_CONTEXT_VALUE_LENGTH:
                raise ValueError("failure context value exceeds maximum length")
            checked_context[key_text] = value
        return cls(
            status="error",
            error_code=_normalize_text(error_code, field="error_code", max_length=MAX_ERROR_CODE_LENGTH),
            reason=_normalize_text(reason, field="reason", max_length=MAX_REASON_LENGTH),
            context=MappingProxyType(checked_context),
            recoverable=recoverable,
        )


@dataclass(frozen=True)
class OdysseusConfig:
    """Explicit Odysseus adapter configuration.

    Runtime: O(1). Memory: O(1). Failure: invalid fields are rejected by config
    loading before adapter construction. Deterministic: yes.
    """

    enabled: bool
    base_url: str
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    chat_path: str = DEFAULT_CHAT_PATH
    health_path: str = DEFAULT_HEALTH_PATH
    max_prompt_chars: int = MAX_PROMPT_CHARS
    max_response_bytes: int = MAX_RESPONSE_BYTES


ProvenanceTag = ProvenanceRecord


@dataclass(frozen=True)
class OdysseusPromptRequest:
    """Safe prompt request for the Odysseus workspace.

    Runtime: O(prompt length), bounded by max_prompt_chars. Memory: O(prompt).
    Failure: empty or oversized prompt/session is rejected. Deterministic: yes.
    """

    prompt: str
    session_id: str
    include_provenance: bool = True
    request_id: str = ""
    trace_id: str = ""
    timestamp: int = 0


@dataclass(frozen=True)
class OdysseusPromptResult:
    """Structured response from an Odysseus prompt call.

    Runtime: O(response length), bounded by max_response_bytes. Memory:
    O(response length). Failure: represented by Failure. Deterministic: yes.
    """

    status: str
    response: str | None
    provenance: ProvenanceTag | None = None
    failure: Failure | None = None


@dataclass(frozen=True)
class OdysseusHealthStatus:
    """Bounded availability signal for the Odysseus adapter.

    Runtime: O(1) plus configured HTTP timeout. Memory: O(1) plus capped
    response bytes. Failure: represented by Failure. Deterministic validation.
    """

    status: str
    enabled: bool
    available: bool
    base_url: str
    timeout_seconds: float
    failure: Failure | None = None


@dataclass(frozen=True)
class OdysseusCapabilityRegistration:
    """Minimal capability provider descriptor for Odysseus Workspace.

    Runtime: O(allowed calls count), bounded to this module's fixed safe-call
    tuple. Memory: O(1). Failure: none. Deterministic: yes.
    """

    status: str
    capability_id: str
    display_name: str
    provider: str
    boundary: str
    allowed_calls: tuple[str, ...]
    owns_canonical_state: bool
    failure: Failure | None = None


@dataclass(frozen=True)
class HttpResponse:
    """HTTP response returned by an injected transport."""

    status_code: int
    body: bytes
    headers: Mapping[str, str] = MappingProxyType({})


class OdysseusTransport(Protocol):
    """Explicit transport dependency for testable network isolation."""

    def request_json(
        self,
        method: str,
        url: str,
        payload: Mapping[str, object] | None,
        timeout_seconds: float,
        max_response_bytes: int,
    ) -> HttpResponse:
        """Send one bounded JSON request.

        Runtime: bounded by timeout_seconds and max_response_bytes.
        Memory: O(max_response_bytes).
        Failure: raises TimeoutError, OSError, or ValueError.
        Deterministic: depends on implementation.
        """


def _normalize_text(value: str, *, field: str, max_length: int) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field} is required")
    if len(normalized) > max_length:
        raise ValueError(f"{field} exceeds maximum length")
    return normalized
