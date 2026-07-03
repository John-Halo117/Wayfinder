"""Execution Runtime provider registry."""

from __future__ import annotations

import os
from typing import Mapping

from external.odysseus import OdysseusWorkspaceAdapter
from external.odysseus.config import load_odysseus_config

from .interfaces import (
    ExecutionRuntimeHealth,
    ExecutionRuntimeProvider,
    ExecutionRuntimeRequest,
    ExecutionRuntimeResponse,
    Failure,
)
from .providers.odysseus import OdysseusExecutionRuntime

EXECUTION_RUNTIME_ENV = "EXECUTION_RUNTIME"
LEGACY_HOST_SHELL_ENV = "HOST_SHELL"
EXECUTION_RUNTIME_NONE = "none"
EXECUTION_RUNTIME_ODYSSEUS = "odysseus"


class DisabledExecutionRuntimeProvider:
    """No-op Execution Runtime provider for EXECUTION_RUNTIME=none."""

    provider_name = EXECUTION_RUNTIME_NONE

    def health(self) -> ExecutionRuntimeHealth:
        """Return disabled Execution Runtime health without network calls.

        Inputs: none. Outputs: ExecutionRuntimeHealth.
        Runtime: O(1). Memory: O(1).
        Failure: none. Deterministic: yes.
        """

        return ExecutionRuntimeHealth(
            status="disabled",
            provider=self.provider_name,
            enabled=False,
            available=False,
            canonical=False,
        )

    def send(self, request: ExecutionRuntimeRequest) -> ExecutionRuntimeResponse:
        """Reject Execution Runtime requests while disabled.

        Inputs: ExecutionRuntimeRequest. Outputs: ExecutionRuntimeResponse.
        Runtime: O(1). Memory: O(1).
        Failure: always returns EXECUTION_RUNTIME_DISABLED.
        Deterministic: yes.
        """

        return ExecutionRuntimeResponse(
            status="error",
            provider=self.provider_name,
            content=None,
            provenance=None,
            canonical=False,
            failure=Failure.build("EXECUTION_RUNTIME_DISABLED", "Execution Runtime provider is disabled"),
        )


def build_execution_runtime_provider(values: Mapping[str, object] | None = None) -> ExecutionRuntimeProvider:
    """Build an Execution Runtime provider from runtime selection.

    Inputs: optional mapping with EXECUTION_RUNTIME and provider-specific values.
    Outputs: ExecutionRuntimeProvider.
    Runtime: O(known provider count), bounded to two provider options.
    Memory: O(1).
    Failure: raises ValueError for unknown runtime or invalid provider config.
    Deterministic: yes for explicit mappings; environment-dependent otherwise.
    """

    raw = values or os.environ
    selected = str(
        raw.get(EXECUTION_RUNTIME_ENV, raw.get(LEGACY_HOST_SHELL_ENV, EXECUTION_RUNTIME_NONE))
    ).strip().lower()
    if selected == EXECUTION_RUNTIME_NONE:
        return DisabledExecutionRuntimeProvider()
    if selected == EXECUTION_RUNTIME_ODYSSEUS:
        return OdysseusExecutionRuntime(OdysseusWorkspaceAdapter(load_odysseus_config(raw)))
    raise ValueError("EXECUTION_RUNTIME must be one of: none, odysseus")

