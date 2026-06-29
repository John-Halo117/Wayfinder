"""Minimal Odysseus Workspace capability registration."""

from __future__ import annotations

from .interfaces import CAPABILITY_ID, OdysseusCapabilityRegistration


def register_odysseus_workspace_capability() -> OdysseusCapabilityRegistration:
    """Return the safe, non-canonical Odysseus Workspace capability descriptor.

    Inputs: none.
    Outputs: OdysseusCapabilityRegistration.
    Runtime: O(allowed call count), bounded to a fixed tuple of three calls.
    Memory: O(1).
    Failure: none.
    Deterministic: yes.
    """

    return OdysseusCapabilityRegistration(
        status="ok",
        capability_id=CAPABILITY_ID,
        display_name="Odysseus Workspace",
        provider="odysseus",
        boundary="optional UI/agent workspace adapter; not source of truth",
        allowed_calls=(
            "health",
            "send_prompt",
            "receive_response",
        ),
        owns_canonical_state=False,
    )
