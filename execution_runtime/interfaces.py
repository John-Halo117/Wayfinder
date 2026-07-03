"""Typed Execution Runtime provider interfaces.

Contract:
- Inputs: explicit dataclasses and primitive strings.
- Outputs: immutable records or structured failures.
- Runtime constraint: O(prompt bytes + response bytes), bounded by the selected
  runtime provider's caps and timeout.
- Memory assumption: O(prompt bytes + response bytes), bounded by provider caps.
- Failure cases: disabled provider, invalid request, unavailable provider,
  delegated adapter failure, and invalid runtime selection.
- Determinism: validation and provider selection are deterministic for explicit
  inputs. Network behavior is isolated behind provider method calls.
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
MAX_SESSION_ID_LENGTH = 128
MAX_PROMPT_CHARS = 50_000


@dataclass(frozen=True)
class Failure:
    """Standard structured failure object."""

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
        """Build a bounded structured failure.

        Inputs: error code, reason, optional context, recoverability.
        Outputs: Failure.
        Runtime: O(context key count), bounded by MAX_CONTEXT_KEYS.
        Memory: O(context key count).
        Failure: raises ValueError for oversized context.
        Deterministic: yes.
        """

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
class ExecutionRuntimeHealth:
    """Provider health signal for Execution Runtime."""

    status: str
    provider: str
    enabled: bool
    available: bool
    canonical: bool
    failure: Failure | None = None


@dataclass(frozen=True)
class ExecutionRuntimeRequest:
    """Bounded Execution Runtime interaction request."""

    prompt: str
    session_id: str
    include_provenance: bool = True
    request_id: str = ""
    trace_id: str = ""
    timestamp: int = 0


@dataclass(frozen=True)
class ExecutionRuntimeResponse:
    """Bounded Execution Runtime interaction response."""

    status: str
    provider: str
    content: str | None
    provenance: ProvenanceRecord | None
    canonical: bool
    failure: Failure | None = None


class ExecutionRuntimeProvider(Protocol):
    """Explicit provider contract for bounded execution runtimes."""

    provider_name: str

    def health(self) -> ExecutionRuntimeHealth:
        """Return provider availability.

        Inputs: provider configuration. Outputs: ExecutionRuntimeHealth.
        Runtime: bounded by provider timeout. Memory: bounded by provider caps.
        Failure: represented by ExecutionRuntimeHealth.failure.
        Deterministic: validation deterministic; network depends on provider.
        """

    def send(self, request: ExecutionRuntimeRequest) -> ExecutionRuntimeResponse:
        """Send one Execution Runtime interaction request.

        Inputs: ExecutionRuntimeRequest. Outputs: ExecutionRuntimeResponse.
        Runtime: bounded by provider timeout and response caps.
        Memory: bounded by request and response caps.
        Failure: represented by ExecutionRuntimeResponse.failure.
        Deterministic: validation deterministic; network depends on provider.
        """


def validate_execution_runtime_request(request: ExecutionRuntimeRequest) -> Failure | None:
    """Validate Execution Runtime request shape without calling a provider.

    Inputs: ExecutionRuntimeRequest. Outputs: optional Failure.
    Runtime: O(prompt + session length), bounded by MAX_PROMPT_CHARS and
    MAX_SESSION_ID_LENGTH. Memory: O(1).
    Failure: none; invalid input returns Failure.
    Deterministic: yes.
    """

    prompt = request.prompt.strip()
    if not prompt:
        return Failure.build("EXECUTION_RUNTIME_PROMPT_INVALID", "prompt is required")
    if len(prompt) > MAX_PROMPT_CHARS:
        return Failure.build("EXECUTION_RUNTIME_PROMPT_TOO_LARGE", "prompt exceeds maximum length")
    session_id = request.session_id.strip()
    if not session_id:
        return Failure.build("EXECUTION_RUNTIME_SESSION_INVALID", "session_id is required")
    if len(session_id) > MAX_SESSION_ID_LENGTH:
        return Failure.build("EXECUTION_RUNTIME_SESSION_INVALID", "session_id exceeds maximum length")
    return None


def _normalize_text(value: str, *, field: str, max_length: int) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field} is required")
    if len(normalized) > max_length:
        raise ValueError(f"{field} exceeds maximum length")
    return normalized

