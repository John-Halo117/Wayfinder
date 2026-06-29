"""Odysseus workspace adapter package."""

from .adapter import HttpOdysseusTransport, OdysseusWorkspaceAdapter
from .capability import register_odysseus_workspace_capability
from .interfaces import (
    Failure,
    HttpResponse,
    OdysseusCapabilityRegistration,
    OdysseusConfig,
    OdysseusHealthStatus,
    OdysseusPromptRequest,
    OdysseusPromptResult,
    ProvenanceTag,
)

__all__ = (
    "Failure",
    "HttpOdysseusTransport",
    "HttpResponse",
    "OdysseusCapabilityRegistration",
    "OdysseusConfig",
    "OdysseusHealthStatus",
    "OdysseusPromptRequest",
    "OdysseusPromptResult",
    "OdysseusWorkspaceAdapter",
    "ProvenanceTag",
    "register_odysseus_workspace_capability",
)
