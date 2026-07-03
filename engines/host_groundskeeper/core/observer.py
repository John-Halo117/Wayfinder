"""Delta-first host observation engine.

Contract:
- Inputs: typed HostObservation candidates and process names.
- Outputs: ObservationPublishResult values and bounded cached state.
- Runtime constraint: O(field_count) per observation, bounded by max_fields.
- Memory assumption: O(observation_type_count * field_count), bounded by
  max_observation_types and max_fields.
- Failure cases: invalid observation, invalid thresholds, publication failure,
  duplicate/coalesced event, and resource-bound violations.
- Determinism: all decisions are deterministic for identical inputs and publisher
  responses.
"""

from __future__ import annotations

from dataclasses import replace
from types import MappingProxyType
from typing import Mapping

from ..contracts.interfaces import (
    Failure,
    HostObservation,
    MAX_FIELD_COUNT,
    MAX_OBSERVATION_TYPE_LENGTH,
    MAX_SOURCE_LENGTH,
    ObservationPublisherPort,
    ObservationPublishResult,
    ObservationThresholds,
    _normalize_text,
)

DEFAULT_MAX_OBSERVATION_TYPES = 64
KNOWN_CODING_PROCESSES = frozenset(
    {
        "code",
        "code-insiders",
        "devenv",
        "idea64",
        "idea",
        "pycharm64",
        "pycharm",
        "webstorm64",
        "webstorm",
        "rider64",
        "rider",
        "clion64",
        "clion",
        "goland64",
        "goland",
    }
)
KNOWN_GAME_PROCESSES = frozenset(
    {
        "steam",
        "steamwebhelper",
        "cyberpunk2077",
        "witcher3",
        "eldenring",
        "starfield",
        "bg3",
        "helldivers2",
        "gamebar",
    }
)


class HostObservationEngine:
    """Stateful, bounded delta suppressor and telemetry publisher.

    Inputs: ObservationPublisherPort, thresholds, max observation types, max fields,
    and coalescing window. Outputs: ObservationPublishResult.
    Runtime: O(field_count), bounded by max_fields. Memory: bounded by
    max_observation_types * max_fields. Failure: returns structured failures for
    invalid observations or publish failures. Deterministic: yes when publisher is.
    """

    def __init__(
        self,
        publisher: ObservationPublisherPort,
        *,
        thresholds: ObservationThresholds | None = None,
        max_observation_types: int = DEFAULT_MAX_OBSERVATION_TYPES,
        max_fields: int = MAX_FIELD_COUNT,
        coalesce_window_seconds: int = 5,
    ) -> None:
        if max_observation_types <= 0:
            raise ValueError("max_observation_types must be positive")
        if max_fields <= 0 or max_fields > MAX_FIELD_COUNT:
            raise ValueError("max_fields must be positive and within MAX_FIELD_COUNT")
        if coalesce_window_seconds < 0:
            raise ValueError("coalesce_window_seconds must be non-negative")
        self._thresholds = thresholds or ObservationThresholds()
        self._validate_thresholds(self._thresholds)
        self._publisher = publisher
        self._max_observation_types = max_observation_types
        self._max_fields = max_fields
        self._coalesce_window_seconds = coalesce_window_seconds
        self._last_by_type: dict[str, HostObservation] = {}

    def process(self, observation: HostObservation) -> ObservationPublishResult:
        """Publish only materially changed observations.

        Inputs: HostObservation candidate. Outputs: ObservationPublishResult.
        Runtime: O(field_count), bounded by max_fields. Memory: O(field_count).
        Failure: returns structured failure for invalid input or publisher failure.
        Deterministic: yes when publisher is deterministic.
        """

        try:
            candidate = self._normalize_observation(observation)
        except ValueError as exc:
            return ObservationPublishResult(
                status="error",
                published=False,
                failure=Failure.build("HOST_OBSERVATION_INVALID", str(exc)),
            )
        previous = self._last_by_type.get(candidate.observation)
        if previous is None:
            if len(self._last_by_type) >= self._max_observation_types:
                return ObservationPublishResult(
                    status="error",
                    published=False,
                    failure=Failure.build("HOST_OBSERVATION_LIMIT", "observation type count exceeds maximum"),
                )
            return self._publish(candidate)
        delta = calculate_delta(previous.values, candidate.values, thresholds=self._thresholds)
        if not delta:
            return ObservationPublishResult(status="ok", published=False)
        if candidate.timestamp - previous.timestamp < self._coalesce_window_seconds:
            return ObservationPublishResult(status="ok", published=False)
        return self._publish(replace(candidate, delta=MappingProxyType(delta)))

    def cached(self) -> tuple[HostObservation, ...]:
        """Return cached last observations.

        Inputs: none. Outputs: immutable observation tuple. Runtime:
        O(observation_type_count), bounded by max_observation_types. Memory:
        O(observation_type_count). Failure: none. Deterministic: yes.
        """

        return tuple(self._last_by_type.values())

    def _publish(self, observation: HostObservation) -> ObservationPublishResult:
        result = self._publisher.publish(observation)
        if getattr(result, "status", None) != "ok":
            return ObservationPublishResult(
                status="error",
                published=False,
                failure=Failure.build(
                    "HOST_OBSERVATION_PUBLISH_FAILED",
                    "telemetry publisher rejected observation",
                    {"observation": observation.observation},
                ),
            )
        self._last_by_type[observation.observation] = observation
        return ObservationPublishResult(status="ok", published=True, observation=observation)

    def _normalize_observation(self, observation: HostObservation) -> HostObservation:
        if observation.timestamp < 0:
            raise ValueError("timestamp must be non-negative")
        if observation.confidence < 0.0 or observation.confidence > 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if len(observation.values) > self._max_fields:
            raise ValueError("observation field count exceeds maximum")
        normalized_values = dict(observation.values)
        normalized_delta = dict(observation.delta)
        return HostObservation(
            timestamp=observation.timestamp,
            observation=_normalize_text(
                observation.observation,
                field="observation",
                max_length=MAX_OBSERVATION_TYPE_LENGTH,
            ),
            source=_normalize_text(observation.source, field="source", max_length=MAX_SOURCE_LENGTH),
            confidence=observation.confidence,
            values=MappingProxyType(normalized_values),
            delta=MappingProxyType(normalized_delta),
        )

    @staticmethod
    def _validate_thresholds(thresholds: ObservationThresholds) -> None:
        values = (
            thresholds.cpu_utilization_percent,
            thresholds.cpu_frequency_mhz,
            thresholds.cpu_temperature_celsius,
            thresholds.gpu_utilization_percent,
            thresholds.gpu_vram_megabytes,
            thresholds.gpu_temperature_celsius,
            thresholds.memory_megabytes,
            thresholds.storage_utilization_percent,
            thresholds.storage_free_megabytes,
            thresholds.generic_numeric,
        )
        for index, value in enumerate(values):
            if value < 0:
                raise ValueError(f"threshold at index {index} must be non-negative")


def calculate_delta(
    previous: Mapping[str, object],
    current: Mapping[str, object],
    *,
    thresholds: ObservationThresholds,
) -> Mapping[str, object]:
    """Return fields that changed beyond configured thresholds.

    Inputs: previous/current value mappings and thresholds. Outputs: mapping of
    changed fields to current values. Runtime: O(field_count), bounded by
    MAX_FIELD_COUNT by caller. Memory: O(field_count). Failure: none.
    Deterministic: yes.
    """

    delta: dict[str, object] = {}
    keys = tuple(current.keys())
    for index, key in enumerate(keys):
        if index >= MAX_FIELD_COUNT:
            break
        current_value = current[key]
        if key not in previous:
            delta[key] = current_value
            continue
        previous_value = previous[key]
        if _materially_changed(key, previous_value, current_value, thresholds):
            delta[key] = current_value
    return MappingProxyType(delta)


def classify_process(process_name: str) -> str:
    """Classify a process name without inspecting process contents.

    Inputs: executable/process name. Outputs: one of coding, game, or other.
    Runtime: O(len(process_name)), bounded by process name length supplied by OS.
    Memory: O(len(process_name)). Failure: raises ValueError for empty names.
    Deterministic: yes.
    """

    normalized = process_name.strip().lower()
    if not normalized:
        raise ValueError("process_name is required")
    if normalized.endswith(".exe"):
        normalized = normalized[:-4]
    if normalized in KNOWN_CODING_PROCESSES:
        return "coding"
    if normalized in KNOWN_GAME_PROCESSES:
        return "game"
    return "other"


def _materially_changed(
    key: str,
    previous: object,
    current: object,
    thresholds: ObservationThresholds,
) -> bool:
    if isinstance(previous, (int, float)) and isinstance(current, (int, float)):
        return abs(float(current) - float(previous)) >= _threshold_for_key(key, thresholds)
    return previous != current


def _threshold_for_key(key: str, thresholds: ObservationThresholds) -> float:
    normalized = key.lower()
    if "cpu" in normalized and "utilization" in normalized:
        return thresholds.cpu_utilization_percent
    if "frequency" in normalized:
        return thresholds.cpu_frequency_mhz
    if "cpu" in normalized and "temperature" in normalized:
        return thresholds.cpu_temperature_celsius
    if "gpu" in normalized and "utilization" in normalized:
        return thresholds.gpu_utilization_percent
    if "vram" in normalized:
        return thresholds.gpu_vram_megabytes
    if "gpu" in normalized and "temperature" in normalized:
        return thresholds.gpu_temperature_celsius
    if "memory" in normalized or "committed" in normalized or "available" in normalized:
        return thresholds.memory_megabytes
    if "disk" in normalized and "utilization" in normalized:
        return thresholds.storage_utilization_percent
    if "free" in normalized:
        return thresholds.storage_free_megabytes
    return thresholds.generic_numeric


def build_process_change_observations(
    *,
    previous_processes: tuple[str, ...],
    current_processes: tuple[str, ...],
    timestamp: int,
    source: str = "windows.process",
    max_events: int = 128,
) -> tuple[HostObservation, ...]:
    """Build ProcessStarted and ProcessExited observations from process snapshots.

    Inputs: previous/current process identity tuples, timestamp, source, and event
    cap. Outputs: HostObservation tuple. Runtime: O(process_count + max_events),
    bounded by caller-supplied snapshots and max_events. Memory: O(max_events).
    Failure: raises ValueError for invalid caps or timestamp. Deterministic: yes.
    """

    if max_events <= 0:
        raise ValueError("max_events must be positive")
    if timestamp < 0:
        raise ValueError("timestamp must be non-negative")
    previous = frozenset(previous_processes)
    current = frozenset(current_processes)
    observations: list[HostObservation] = []
    started = tuple(sorted(current - previous))
    exited = tuple(sorted(previous - current))
    for process_name in started:
        if len(observations) >= max_events:
            break
        observations.append(_process_event("ProcessStarted", process_name, timestamp, source))
    for process_name in exited:
        if len(observations) >= max_events:
            break
        observations.append(_process_event("ProcessExited", process_name, timestamp, source))
    return tuple(observations)


def _process_event(observation: str, process_name: str, timestamp: int, source: str) -> HostObservation:
    values = MappingProxyType({"process": process_name, "classification": classify_process(process_name.split(":", 1)[0])})
    return HostObservation(
        timestamp=timestamp,
        observation=observation,
        source=source,
        confidence=0.9,
        values=values,
        delta=values,
    )
