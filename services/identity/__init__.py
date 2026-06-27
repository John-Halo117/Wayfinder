"""Wayfinder Identity Service.

Canonical reusable identity infrastructure harvested from folded legacy engines.
"""

from .identity_service import (
    AliasResolution,
    Failure,
    HealthStatus,
    IdentityRecord,
    IdentityService,
    MergeDecision,
    RequestIdentity,
    generate_request_id,
    normalize_namespace,
)

__all__ = [
    "AliasResolution",
    "Failure",
    "HealthStatus",
    "IdentityRecord",
    "IdentityService",
    "MergeDecision",
    "RequestIdentity",
    "generate_request_id",
    "normalize_namespace",
]
