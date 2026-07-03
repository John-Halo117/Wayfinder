"""Lifecycle management for Host Groundskeeper."""

from __future__ import annotations

from ..contracts.interfaces import Failure, LifecycleResult


class LifecycleController:
    """Explicit lifecycle state machine.

    Inputs: enabled flag and start/stop calls. Outputs: LifecycleResult.
    Runtime: O(1). Memory: O(1). Failure: disabled or invalid transitions return
    structured failures. Deterministic: yes.
    """

    def __init__(self) -> None:
        self._state = "initialized"

    @property
    def state(self) -> str:
        return self._state

    def start(self, *, enabled: bool) -> LifecycleResult:
        if not enabled:
            self._state = "disabled"
            return LifecycleResult(
                status="error",
                state=self._state,
                failure=Failure.build("HOST_DISABLED", "host groundskeeper is disabled"),
            )
        if self._state == "running":
            return LifecycleResult(status="ok", state=self._state)
        if self._state not in {"initialized", "stopped"}:
            return LifecycleResult(
                status="error",
                state=self._state,
                failure=Failure.build("HOST_LIFECYCLE_INVALID", "cannot start from current state"),
            )
        self._state = "running"
        return LifecycleResult(status="ok", state=self._state)

    def stop(self) -> LifecycleResult:
        if self._state in {"initialized", "stopped", "disabled"}:
            self._state = "stopped"
            return LifecycleResult(status="ok", state=self._state)
        if self._state != "running":
            return LifecycleResult(
                status="error",
                state=self._state,
                failure=Failure.build("HOST_LIFECYCLE_INVALID", "cannot stop from current state"),
            )
        self._state = "stopped"
        return LifecycleResult(status="ok", state=self._state)
