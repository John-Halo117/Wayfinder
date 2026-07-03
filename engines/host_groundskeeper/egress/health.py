"""Framework-neutral health endpoint."""

from __future__ import annotations

from ..contracts.interfaces import HealthResponse, MetricsSnapshot, _normalize_text


def build_health_response(
    *,
    module_name: str,
    lifecycle_state: str,
    plugins_registered: int,
    subscriptions_registered: int,
    metrics: MetricsSnapshot,
) -> HealthResponse:
    """Build a health response without choosing an HTTP framework.

    Inputs: module identity, lifecycle state, counts, and metrics snapshot.
    Outputs: HealthResponse. Runtime: O(1). Memory: O(1). Failure: raises
    ValueError for invalid counts or empty fields. Deterministic: yes.
    """

    if plugins_registered < 0:
        raise ValueError("plugins_registered must be non-negative")
    if subscriptions_registered < 0:
        raise ValueError("subscriptions_registered must be non-negative")
    status = "ok" if lifecycle_state in {"initialized", "running", "stopped"} and metrics.status == "ok" else "error"
    return HealthResponse(
        status=status,
        module_name=_normalize_text(module_name, field="module_name", max_length=128),
        lifecycle_state=_normalize_text(lifecycle_state, field="lifecycle_state", max_length=64),
        plugins_registered=plugins_registered,
        subscriptions_registered=subscriptions_registered,
        metrics=metrics,
        failure=metrics.failure,
    )
