"""Odysseus Host Shell provider."""

from __future__ import annotations

from external.odysseus import OdysseusPromptRequest, OdysseusWorkspaceAdapter

from ..interfaces import (
    Failure,
    HostShellHealth,
    HostShellRequest,
    HostShellResponse,
    validate_host_shell_request,
)


class OdysseusHostShellProvider:
    """Host Shell provider backed by the reversible Odysseus adapter."""

    provider_name = "odysseus"

    def __init__(self, adapter: OdysseusWorkspaceAdapter) -> None:
        """Construct provider with an explicit adapter dependency.

        Inputs: OdysseusWorkspaceAdapter.
        Outputs: provider instance.
        Runtime: O(1). Memory: O(1).
        Failure: none.
        Deterministic: yes.
        """

        self._adapter = adapter

    def health(self) -> HostShellHealth:
        """Map Odysseus adapter health into Host Shell health.

        Inputs: adapter configuration.
        Outputs: HostShellHealth.
        Runtime: bounded by wrapped adapter timeout.
        Memory: bounded by wrapped adapter response cap.
        Failure: adapter failures are mapped to Host Shell failures.
        Deterministic: validation deterministic; adapter may perform network.
        """

        health = self._adapter.health()
        failure = None
        if health.failure is not None:
            failure = _map_failure(health.failure.error_code, health.failure.reason, dict(health.failure.context))
        return HostShellHealth(
            status=health.status,
            provider=self.provider_name,
            enabled=health.enabled,
            available=health.available,
            canonical=False,
            failure=failure,
        )

    def send(self, request: HostShellRequest) -> HostShellResponse:
        """Delegate one Host Shell request to Odysseus safely.

        Inputs: HostShellRequest.
        Outputs: HostShellResponse.
        Runtime: bounded by wrapped adapter timeout and caps.
        Memory: bounded by request and wrapped adapter response caps.
        Failure: invalid request or adapter failure is returned structurally.
        Deterministic: validation deterministic; adapter may perform network.
        """

        validation_failure = validate_host_shell_request(request)
        if validation_failure is not None:
            return HostShellResponse(
                status="error",
                provider=self.provider_name,
                content=None,
                provenance=None,
                canonical=False,
                failure=validation_failure,
            )
        result = self._adapter.send_prompt(
            OdysseusPromptRequest(
                prompt=request.prompt.strip(),
                session_id=request.session_id.strip(),
                include_provenance=request.include_provenance,
                request_id=request.request_id,
                trace_id=request.trace_id,
                timestamp=request.timestamp,
            )
        )
        if result.failure is not None:
            return HostShellResponse(
                status="error",
                provider=self.provider_name,
                content=None,
                provenance=None,
                canonical=False,
                failure=_map_failure(
                    result.failure.error_code,
                    result.failure.reason,
                    dict(result.failure.context),
                    result.failure.recoverable,
                ),
            )
        return HostShellResponse(
            status=result.status,
            provider=self.provider_name,
            content=result.response,
            provenance=result.provenance,
            canonical=False,
        )


def _map_failure(
    error_code: str,
    reason: str,
    context: dict[str, object] | None = None,
    recoverable: bool = True,
) -> Failure:
    return Failure.build(error_code, reason, context, recoverable)
