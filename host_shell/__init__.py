"""Compatibility aliases for the renamed Execution Runtime boundary."""

from execution_runtime import (
    ExecutionRuntimeHealth,
    ExecutionRuntimeProvider,
    ExecutionRuntimeRequest,
    ExecutionRuntimeResponse,
    build_execution_runtime_provider,
)

HostShellHealth = ExecutionRuntimeHealth
HostShellProvider = ExecutionRuntimeProvider
HostShellRequest = ExecutionRuntimeRequest
HostShellResponse = ExecutionRuntimeResponse


def build_host_shell_provider(values=None):
    """Compatibility wrapper for build_execution_runtime_provider."""

    return build_execution_runtime_provider(values)

__all__ = (
    "HostShellHealth",
    "HostShellProvider",
    "HostShellRequest",
    "HostShellResponse",
    "build_host_shell_provider",
)
