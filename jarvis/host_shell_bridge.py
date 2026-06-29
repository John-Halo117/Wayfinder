"""Minimal Jarvis bridge to the Host Shell provider registry.

Contract:
- Inputs: explicit session id, prompt, optional bounded context, and optional
  provider configuration mapping.
- Outputs: immutable structured success or failure result.
- Runtime constraint: O(prompt bytes + context bytes + provider response bytes),
  bounded by local context caps and Host Shell provider caps.
- Memory assumption: O(prompt bytes + context bytes + provider response bytes),
  bounded by local caps and provider caps.
- Failure cases: invalid input, invalid context, disabled Host Shell, invalid
  provider configuration, and delegated provider failure.
- Determinism: validation and context formatting are deterministic. Network
  behavior is isolated behind the explicit Host Shell provider send call.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

import host_shell.registry as host_shell_registry
from capabilities.permissions import WORKSPACE_PROMPT_CAPABILITY, check_execution_permission
from execution.interfaces import ExecutionRequest, freeze_mapping
from host_shell import HostShellRequest
from host_shell.interfaces import Failure
from provenance import ProvenanceRecord

MAX_CONTEXT_KEYS = 16
MAX_CONTEXT_KEY_LENGTH = 64
MAX_CONTEXT_VALUE_LENGTH = 512
MAX_SESSION_ID_LENGTH = 128
MAX_PROMPT_CHARS = 50_000
MAX_COMPOSED_PROMPT_CHARS = 55_000
WORKSPACE_PROMPT_INTENT = "workspace.prompt.read"


@dataclass(frozen=True)
class JarvisHostShellResult:
    """Structured result returned by the Jarvis Host Shell bridge."""

    status: str
    provider: str
    content: str | None
    provenance: ProvenanceRecord | None
    canonical: bool
    failure: Failure | None = None


class JarvisHostShellBridge:
    """Bridge Jarvis explicit workspace prompts into Host Shell."""

    def __init__(self, config: Mapping[str, object] | None = None) -> None:
        """Construct the bridge with optional explicit provider config.

        Inputs: optional mapping containing HOST_SHELL and provider env values.
        Outputs: bridge instance.
        Runtime: O(1). Memory: O(1).
        Failure: none; provider configuration errors are surfaced by send.
        Deterministic: yes for explicit mappings; environment-dependent
        provider resolution occurs during send when config is omitted.
        """

        self._config = MappingProxyType(dict(config)) if config is not None else None

    def send_workspace_prompt(
        self,
        session_id: str,
        prompt: str,
        context: Mapping[str, object] | None = None,
    ) -> JarvisHostShellResult:
        """Send an explicit workspace prompt through the configured Host Shell.

        Inputs: session_id, prompt, optional context mapping.
        Outputs: JarvisHostShellResult.
        Runtime: O(prompt bytes + context key count + provider response bytes),
        bounded by MAX_CONTEXT_KEYS, MAX_COMPOSED_PROMPT_CHARS, and provider
        caps.
        Memory: O(prompt bytes + context bytes + provider response bytes).
        Failure: invalid input, invalid config, disabled provider, or delegated
        provider failure.
        Deterministic: validation and formatting deterministic; provider may
        perform network only through its explicit send call.
        """

        validation_failure = _validate_inputs(session_id, prompt)
        if validation_failure is not None:
            return _failure_result("unknown", validation_failure)
        try:
            composed_prompt = _compose_prompt(prompt, context)
        except ValueError as exc:
            return _failure_result(
                "unknown",
                Failure.build("JARVIS_HOST_SHELL_CONTEXT_INVALID", str(exc), recoverable=True),
            )
        execution_request = _build_execution_request(session_id.strip(), composed_prompt, context)
        permission = check_execution_permission(execution_request)
        if not permission.allowed:
            return _failure_result(
                "unknown",
                Failure.build(
                    "JARVIS_HOST_SHELL_PERMISSION_DENIED",
                    permission.reason,
                    {
                        "capability_id": permission.capability_id,
                        "intent": permission.intent,
                        "permission_status": permission.status,
                        "requires_confirmation": permission.requires_confirmation,
                    },
                    recoverable=permission.requires_confirmation,
                ),
            )
        try:
            provider = host_shell_registry.build_host_shell_provider(self._config)
        except ValueError as exc:
            return _failure_result(
                "unknown",
                Failure.build("JARVIS_HOST_SHELL_CONFIG_INVALID", str(exc), recoverable=True),
            )
        try:
            response = provider.send(
                HostShellRequest(
                    prompt=composed_prompt,
                    session_id=session_id.strip(),
                    include_provenance=True,
                )
            )
        except Exception as exc:
            return _failure_result(
                getattr(provider, "provider_name", "unknown"),
                Failure.build("JARVIS_HOST_SHELL_SEND_FAILED", str(exc), recoverable=True),
            )
        if response.failure is not None:
            return JarvisHostShellResult(
                status="error",
                provider=response.provider,
                content=None,
                provenance=response.provenance,
                canonical=False,
                failure=response.failure,
            )
        return JarvisHostShellResult(
            status=response.status,
            provider=response.provider,
            content=response.content,
            provenance=response.provenance,
            canonical=False,
        )


def _validate_inputs(session_id: str, prompt: str) -> Failure | None:
    session = session_id.strip()
    if not session:
        return Failure.build("JARVIS_HOST_SHELL_SESSION_INVALID", "session_id is required")
    if len(session) > MAX_SESSION_ID_LENGTH:
        return Failure.build("JARVIS_HOST_SHELL_SESSION_INVALID", "session_id exceeds maximum length")
    normalized_prompt = prompt.strip()
    if not normalized_prompt:
        return Failure.build("JARVIS_HOST_SHELL_PROMPT_INVALID", "prompt is required")
    if len(normalized_prompt) > MAX_PROMPT_CHARS:
        return Failure.build("JARVIS_HOST_SHELL_PROMPT_TOO_LARGE", "prompt exceeds maximum length")
    return None


def _compose_prompt(prompt: str, context: Mapping[str, object] | None) -> str:
    base_prompt = prompt.strip()
    if context is None:
        return base_prompt
    if not isinstance(context, Mapping):
        raise ValueError("context must be a mapping")
    if len(context) > MAX_CONTEXT_KEYS:
        raise ValueError("context exceeds maximum key count")
    lines = [base_prompt, "", "Context:"]
    for key in sorted(context):
        key_text = str(key).strip()
        if not key_text:
            raise ValueError("context key is required")
        if len(key_text) > MAX_CONTEXT_KEY_LENGTH:
            raise ValueError("context key exceeds maximum length")
        value_text = str(context[key]).strip()
        if len(value_text) > MAX_CONTEXT_VALUE_LENGTH:
            raise ValueError("context value exceeds maximum length")
        lines.append(f"- {key_text}: {value_text}")
    composed = "\n".join(lines)
    if len(composed) > MAX_COMPOSED_PROMPT_CHARS:
        raise ValueError("composed prompt exceeds maximum length")
    return composed


def _build_execution_request(
    session_id: str,
    composed_prompt: str,
    context: Mapping[str, object] | None,
) -> ExecutionRequest:
    return ExecutionRequest(
        request_id=f"jarvis-host-shell:{session_id}",
        actor="jarvis",
        intent=WORKSPACE_PROMPT_INTENT,
        capability_id=WORKSPACE_PROMPT_CAPABILITY,
        payload=freeze_mapping(
            {
                "session_id": session_id,
                "prompt": composed_prompt,
                "context_keys": tuple(sorted(str(key) for key in (context or {}).keys())),
            }
        ),
        constraints=freeze_mapping({"read_only": True}),
    )


def _failure_result(provider: str, failure: Failure) -> JarvisHostShellResult:
    return JarvisHostShellResult(
        status="error",
        provider=provider,
        content=None,
        provenance=None,
        canonical=False,
        failure=failure,
    )
