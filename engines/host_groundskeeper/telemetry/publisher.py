"""Bounded in-memory observation publisher used by tests and adapters."""

from __future__ import annotations

from dataclasses import dataclass

from ..contracts.interfaces import Failure, HostObservation


@dataclass(frozen=True)
class PublishAck:
    """Telemetry publication acknowledgement."""

    status: str
    failure: Failure | None = None


class InMemoryObservationPublisher:
    """Local publisher compatible with ObservationPublisherPort.

    Inputs: HostObservation values. Outputs: PublishAck and immutable event tuple.
    Runtime: O(1) per publish. Memory: O(max_events). Failure: capacity exhaustion
    returns structured failure. Deterministic: yes.
    """

    def __init__(self, *, max_events: int) -> None:
        if max_events <= 0:
            raise ValueError("max_events must be positive")
        self._max_events = max_events
        self._events: tuple[HostObservation, ...] = ()

    def publish(self, observation: HostObservation) -> PublishAck:
        if len(self._events) >= self._max_events:
            return PublishAck(
                status="error",
                failure=Failure.build("HOST_TELEMETRY_LIMIT", "observation publisher is full"),
            )
        self._events = (*self._events, observation)
        return PublishAck(status="ok")

    def events(self) -> tuple[HostObservation, ...]:
        return self._events
