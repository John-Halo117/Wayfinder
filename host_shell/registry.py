"""Host Shell provider registry."""

from __future__ import annotations

import os
from typing import Mapping

from external.odysseus import OdysseusWorkspaceAdapter
from external.odysseus.config import load_odysseus_config

from .interfaces import Failure, HostShellHealth, HostShellProvider, HostShellRequest, HostShellResponse
from .providers.odysseus import OdysseusHostShellProvider

HOST_SHELL_ENV = "HOST_SHELL"
HOST_SHELL_NONE = "none"
HOST_SHELL_ODYSSEUS = "odysseus"


class DisabledHostShellProvider:
    """No-op Host Shell provider for HOST_SHELL=none."""

    provider_name = HOST_SHELL_NONE

    def health(self) -> HostShellHealth:
        """Return disabled Host Shell health without network calls.

        Inputs: none. Outputs: HostShellHealth.
        Runtime: O(1). Memory: O(1).
        Failure: none. Deterministic: yes.
        """

        return HostShellHealth(
            status="disabled",
            provider=self.provider_name,
            enabled=False,
            available=False,
            canonical=False,
        )

    def send(self, request: HostShellRequest) -> HostShellResponse:
        """Reject Host Shell requests while disabled.

        Inputs: HostShellRequest. Outputs: HostShellResponse.
        Runtime: O(1). Memory: O(1).
        Failure: always returns HOST_SHELL_DISABLED.
        Deterministic: yes.
        """

        return HostShellResponse(
            status="error",
            provider=self.provider_name,
            content=None,
            provenance=None,
            canonical=False,
            failure=Failure.build("HOST_SHELL_DISABLED", "Host Shell provider is disabled"),
        )


def build_host_shell_provider(values: Mapping[str, object] | None = None) -> HostShellProvider:
    """Build a Host Shell provider from HOST_SHELL selection.

    Inputs: optional mapping with HOST_SHELL and provider-specific variables.
    Outputs: HostShellProvider.
    Runtime: O(known provider count), bounded to two provider options.
    Memory: O(1).
    Failure: raises ValueError for unknown HOST_SHELL or invalid provider config.
    Deterministic: yes for explicit mappings; environment-dependent otherwise.
    """

    raw = values or os.environ
    selected = str(raw.get(HOST_SHELL_ENV, HOST_SHELL_NONE)).strip().lower()
    if selected == HOST_SHELL_NONE:
        return DisabledHostShellProvider()
    if selected == HOST_SHELL_ODYSSEUS:
        return OdysseusHostShellProvider(OdysseusWorkspaceAdapter(load_odysseus_config(raw)))
    raise ValueError("HOST_SHELL must be one of: none, odysseus")
