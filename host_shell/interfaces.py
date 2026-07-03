"""Compatibility aliases for the renamed Execution Runtime interfaces."""

from execution_runtime.interfaces import (
    ExecutionRuntimeHealth,
    ExecutionRuntimeProvider,
    ExecutionRuntimeRequest,
    ExecutionRuntimeResponse,
    Failure,
    validate_execution_runtime_request,
)

HostShellHealth = ExecutionRuntimeHealth
HostShellProvider = ExecutionRuntimeProvider
HostShellRequest = ExecutionRuntimeRequest
HostShellResponse = ExecutionRuntimeResponse


def validate_host_shell_request(request: HostShellRequest) -> Failure | None:
    """Compatibility wrapper for validate_execution_runtime_request."""

    return validate_execution_runtime_request(request)
