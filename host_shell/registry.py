"""Compatibility registry for the renamed Execution Runtime registry."""

from execution_runtime.registry import (
    DisabledExecutionRuntimeProvider,
    build_execution_runtime_provider,
)

DisabledHostShellProvider = DisabledExecutionRuntimeProvider


def build_host_shell_provider(values=None):
    """Compatibility wrapper for build_execution_runtime_provider."""

    return build_execution_runtime_provider(values)
