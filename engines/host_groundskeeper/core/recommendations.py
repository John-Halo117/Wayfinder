"""Advisory-only Host Groundskeeper recommendation engine.

Contract:
- Inputs: bounded HostObservation sequences.
- Outputs: RecommendationResult with advisory HostRecommendation records.
- Runtime constraint: O(observation_count + recommendation_count), bounded by
  max_observations and max_recommendations.
- Memory assumption: O(observation_count + recommendation_count), bounded by
  constructor caps.
- Failure cases: invalid thresholds, too many observations, invalid observation
  shape, or recommendation cap exhaustion.
- Determinism: identical observations and thresholds produce identical
  recommendations in stable order.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from ..contracts.interfaces import (
    DEFAULT_MAX_OBSERVATIONS,
    DEFAULT_MAX_RECOMMENDATIONS,
    Failure,
    HostObservation,
    HostRecommendation,
    MAX_EXPLANATION_LENGTH,
    MAX_RECOMMENDATION_ID_LENGTH,
    MAX_SUPPORTING_OBSERVATIONS,
    RecommendationResult,
    RecommendationThresholds,
    _normalize_text,
)
from .observer import classify_process


@dataclass(frozen=True)
class _ObservationState:
    foreground_application: str | None = None
    foreground_classification: str | None = None
    cpu_utilization_percent: float | None = None
    cpu_package_power_watts: float | None = None
    cpu_temperature_celsius: float | None = None
    previous_cpu_temperature_celsius: float | None = None
    gpu_utilization_percent: float | None = None
    gpu_temperature_celsius: float | None = None
    available_memory_percent: float | None = None
    active_power_plan: str | None = None
    process_started: tuple[str, ...] = ()


class HostRecommendationEngine:
    """Bounded advisory recommendation evaluator.

    Inputs: HostObservation sequences. Outputs: RecommendationResult. Runtime:
    O(max_observations + max_recommendations). Memory: O(max_observations +
    max_recommendations). Failure: returns structured failures for invalid inputs
    or cap exhaustion. Deterministic: yes.
    """

    def __init__(
        self,
        *,
        thresholds: RecommendationThresholds | None = None,
        max_observations: int = DEFAULT_MAX_OBSERVATIONS,
        max_recommendations: int = DEFAULT_MAX_RECOMMENDATIONS,
    ) -> None:
        if max_observations <= 0:
            raise ValueError("max_observations must be positive")
        if max_recommendations <= 0:
            raise ValueError("max_recommendations must be positive")
        self._thresholds = thresholds or RecommendationThresholds()
        self._validate_thresholds(self._thresholds)
        self._max_observations = max_observations
        self._max_recommendations = max_recommendations
        self._last_recommendation_ids: tuple[str, ...] = ()

    def evaluate(self, observations: tuple[HostObservation, ...]) -> RecommendationResult:
        """Evaluate observations and emit advisory-only recommendations.

        Inputs: HostObservation tuple. Outputs: RecommendationResult. Runtime:
        O(observation_count + recommendation_count), bounded by constructor caps.
        Memory: O(recommendation_count). Failure: structured failures for invalid
        input or cap exhaustion. Deterministic: yes.
        """

        if len(observations) > self._max_observations:
            return RecommendationResult(
                status="error",
                recommendations=(),
                failure=Failure.build("HOST_RECOMMENDATION_OBSERVATION_LIMIT", "observation count exceeds maximum"),
            )
        try:
            state = self._build_state(observations)
            recommendations = self._build_recommendations(state)
        except ValueError as exc:
            return RecommendationResult(
                status="error",
                recommendations=(),
                failure=Failure.build("HOST_RECOMMENDATION_INVALID", str(exc)),
            )
        recommendation_ids = tuple(item.recommendation_id for item in recommendations)
        if recommendation_ids == self._last_recommendation_ids:
            return RecommendationResult(status="ok", recommendations=())
        self._last_recommendation_ids = recommendation_ids
        return RecommendationResult(status="ok", recommendations=recommendations)

    def _build_state(self, observations: tuple[HostObservation, ...]) -> _ObservationState:
        state = _ObservationState()
        cpu_temperatures: list[float] = []
        started: list[str] = []
        for index, observation in enumerate(observations):
            if index >= self._max_observations:
                raise ValueError("observation iteration exceeded maximum")
            values = observation.values
            if observation.observation == "ForegroundApplicationChanged":
                foreground = _string_value(values, "foreground_application")
                classification = _string_value(values, "classification") or (classify_process(foreground) if foreground else None)
                state = _replace_state(state, foreground_application=foreground, foreground_classification=classification)
            elif observation.observation == "ProcessStarted":
                process = _string_value(values, "process")
                if process and len(started) < MAX_SUPPORTING_OBSERVATIONS:
                    started.append(process)
            elif observation.observation == "HostCpuChanged":
                cpu_util = _number_value(values, "cpu_utilization_percent")
                cpu_power = _first_number(values, ("package_power_watts", "cpu_package_power_watts"))
                cpu_temp = _first_number(values, ("package_temperature_celsius", "cpu_temperature_celsius"))
                if cpu_temp is not None:
                    cpu_temperatures.append(cpu_temp)
                state = _replace_state(
                    state,
                    cpu_utilization_percent=cpu_util if cpu_util is not None else state.cpu_utilization_percent,
                    cpu_package_power_watts=cpu_power if cpu_power is not None else state.cpu_package_power_watts,
                    cpu_temperature_celsius=cpu_temp if cpu_temp is not None else state.cpu_temperature_celsius,
                )
            elif observation.observation == "HostGpuChanged":
                gpu_util = _number_value(values, "gpu_utilization_percent")
                gpu_temp = _first_number(values, ("gpu_temperature_celsius", "temperature_celsius"))
                state = _replace_state(
                    state,
                    gpu_utilization_percent=gpu_util if gpu_util is not None else state.gpu_utilization_percent,
                    gpu_temperature_celsius=gpu_temp if gpu_temp is not None else state.gpu_temperature_celsius,
                )
            elif observation.observation == "MemoryChanged":
                available = _number_value(values, "available_megabytes") or _number_value(values, "available_memory_megabytes")
                total = _number_value(values, "total_megabytes") or _number_value(values, "total_memory_megabytes")
                if available is not None and total and total > 0:
                    state = _replace_state(state, available_memory_percent=(available / total) * 100.0)
            elif observation.observation == "PowerPlanChanged":
                state = _replace_state(state, active_power_plan=_string_value(values, "active_power_plan"))
        if len(cpu_temperatures) >= 2:
            state = _replace_state(
                state,
                previous_cpu_temperature_celsius=cpu_temperatures[-2],
                cpu_temperature_celsius=cpu_temperatures[-1],
            )
        return _replace_state(state, process_started=tuple(started))

    def _build_recommendations(self, state: _ObservationState) -> tuple[HostRecommendation, ...]:
        recommendations: list[HostRecommendation] = []
        self._maybe_append(recommendations, self._coding_profile(state))
        self._maybe_append(recommendations, self._gaming_profile(state))
        self._maybe_append(recommendations, self._eco_mode(state))
        self._maybe_append(recommendations, self._background_process(state))
        self._maybe_append(recommendations, self._cpu_power_high(state))
        self._maybe_append(recommendations, self._gpu_unmatched(state))
        self._maybe_append(recommendations, self._thermal_trend(state))
        self._maybe_append(recommendations, self._idle_opportunity(state))
        return tuple(recommendations)

    def _maybe_append(self, recommendations: list[HostRecommendation], recommendation: HostRecommendation | None) -> None:
        if recommendation is None:
            return
        if len(recommendations) >= self._max_recommendations:
            raise ValueError("recommendation count exceeds maximum")
        recommendations.append(recommendation)

    def _coding_profile(self, state: _ObservationState) -> HostRecommendation | None:
        if state.foreground_classification != "coding":
            return None
        if _contains_text(state.active_power_plan, "coding"):
            return None
        return _recommendation(
            recommendation_id="host.profile.coding",
            confidence=0.86,
            estimated_benefit="Lower latency and steadier compile/editor responsiveness.",
            estimated_cost="Potentially higher power draw than Eco mode.",
            supporting_observations=("ForegroundApplicationChanged", "PowerPlanChanged"),
            expected_capability_impact="Coding responsiveness may improve; no automatic action is taken.",
            explanation="A known coding IDE is foreground while the active power plan is not already identified as Coding.",
        )

    def _gaming_profile(self, state: _ObservationState) -> HostRecommendation | None:
        if state.foreground_classification != "game":
            return None
        if _contains_text(state.active_power_plan, "gaming"):
            return None
        return _recommendation(
            recommendation_id="host.profile.gaming",
            confidence=0.88,
            estimated_benefit="Improved frame pacing and reduced foreground game latency.",
            estimated_cost="Higher energy use and thermal load are likely.",
            supporting_observations=("ForegroundApplicationChanged", "PowerPlanChanged"),
            expected_capability_impact="Foreground game performance may improve; no automatic action is taken.",
            explanation="A known game is foreground while the active power plan is not already identified as Gaming.",
        )

    def _eco_mode(self, state: _ObservationState) -> HostRecommendation | None:
        if not _is_idle(state, self._thresholds):
            return None
        if _contains_text(state.active_power_plan, "eco"):
            return None
        return _recommendation(
            recommendation_id="host.profile.eco",
            confidence=0.8,
            estimated_benefit="Reduced idle power consumption and lower fan activity.",
            estimated_cost="Background tasks may complete more slowly.",
            supporting_observations=("HostCpuChanged", "MemoryChanged", "ForegroundApplicationChanged", "PowerPlanChanged"),
            expected_capability_impact="Interactive performance should remain acceptable for idle/light use; no automatic action is taken.",
            explanation="CPU appears idle, memory headroom is available, and no coding or gaming foreground workload is active.",
        )

    def _background_process(self, state: _ObservationState) -> HostRecommendation | None:
        candidates = tuple(process for process in state.process_started if classify_process(process.split(":", 1)[0]) == "other")
        if not candidates:
            return None
        return _recommendation(
            recommendation_id="host.process.background-review",
            confidence=0.62,
            estimated_benefit="May reduce background CPU, memory, or disk contention if the process is truly unnecessary.",
            estimated_cost="User review time; stopping the wrong process could interrupt work.",
            supporting_observations=("ProcessStarted",),
            expected_capability_impact="No capability changes occur unless a human acts later.",
            explanation=f"A non-coding, non-game process started and may be worth reviewing: {candidates[0]}.",
        )

    def _cpu_power_high(self, state: _ObservationState) -> HostRecommendation | None:
        if state.cpu_package_power_watts is None:
            return None
        if state.cpu_package_power_watts < self._thresholds.high_cpu_package_power_watts:
            return None
        return _recommendation(
            recommendation_id="host.cpu.package-power-high",
            confidence=0.74,
            estimated_benefit="Identifying sustained high CPU power can guide manual workload or thermal review.",
            estimated_cost="No execution cost; advisory review only.",
            supporting_observations=("HostCpuChanged",),
            expected_capability_impact="No immediate capability impact; no automatic action is taken.",
            explanation="CPU package power is above the configured advisory threshold.",
        )

    def _gpu_unmatched(self, state: _ObservationState) -> HostRecommendation | None:
        if state.gpu_utilization_percent is None or state.gpu_utilization_percent < self._thresholds.gpu_active_percent:
            return None
        if state.foreground_classification == "game":
            return None
        return _recommendation(
            recommendation_id="host.gpu.active-without-foreground-workload",
            confidence=0.72,
            estimated_benefit="May reveal avoidable GPU power use or a hidden accelerated workload.",
            estimated_cost="Review effort only; no automatic GPU changes are made.",
            supporting_observations=("HostGpuChanged", "ForegroundApplicationChanged"),
            expected_capability_impact="No capability impact unless a human later changes the workload.",
            explanation="GPU activity is above threshold while no known foreground GPU-heavy workload is active.",
        )

    def _thermal_trend(self, state: _ObservationState) -> HostRecommendation | None:
        if state.previous_cpu_temperature_celsius is None or state.cpu_temperature_celsius is None:
            return None
        increase = state.cpu_temperature_celsius - state.previous_cpu_temperature_celsius
        if increase < self._thresholds.thermal_trend_celsius:
            return None
        return _recommendation(
            recommendation_id="host.thermal.trend-increasing",
            confidence=0.7,
            estimated_benefit="Early thermal awareness can prevent sustained fan noise or throttling.",
            estimated_cost="Review effort only.",
            supporting_observations=("HostCpuChanged",),
            expected_capability_impact="No immediate capability impact; no automatic action is taken.",
            explanation="CPU package temperature increased beyond the configured thermal trend threshold.",
        )

    def _idle_opportunity(self, state: _ObservationState) -> HostRecommendation | None:
        if not _is_idle(state, self._thresholds):
            return None
        return _recommendation(
            recommendation_id="host.idle.opportunity",
            confidence=0.76,
            estimated_benefit="Potential energy savings if the user chooses an idle-friendly profile or pauses background work.",
            estimated_cost="May defer noninteractive background throughput if acted upon.",
            supporting_observations=("HostCpuChanged", "MemoryChanged", "ForegroundApplicationChanged"),
            expected_capability_impact="No current impact; this is an advisory idle signal only.",
            explanation="Observed host state indicates low CPU use, available memory headroom, and no active coding or game foreground workload.",
        )

    @staticmethod
    def _validate_thresholds(thresholds: RecommendationThresholds) -> None:
        values = (
            thresholds.idle_cpu_percent,
            thresholds.idle_memory_available_percent,
            thresholds.high_cpu_package_power_watts,
            thresholds.high_cpu_temperature_celsius,
            thresholds.gpu_active_percent,
            thresholds.thermal_trend_celsius,
        )
        for index, value in enumerate(values):
            if value < 0:
                raise ValueError(f"recommendation threshold at index {index} must be non-negative")


def _recommendation(
    *,
    recommendation_id: str,
    confidence: float,
    estimated_benefit: str,
    estimated_cost: str,
    supporting_observations: tuple[str, ...],
    expected_capability_impact: str,
    explanation: str,
) -> HostRecommendation:
    if confidence < 0.0 or confidence > 1.0:
        raise ValueError("confidence must be between 0 and 1")
    if len(supporting_observations) > MAX_SUPPORTING_OBSERVATIONS:
        raise ValueError("supporting observation count exceeds maximum")
    return HostRecommendation(
        recommendation_id=_normalize_text(
            recommendation_id,
            field="recommendation_id",
            max_length=MAX_RECOMMENDATION_ID_LENGTH,
        ),
        confidence=confidence,
        estimated_benefit=_normalize_text(estimated_benefit, field="estimated_benefit", max_length=MAX_EXPLANATION_LENGTH),
        estimated_cost=_normalize_text(estimated_cost, field="estimated_cost", max_length=MAX_EXPLANATION_LENGTH),
        supporting_observations=tuple(
            _normalize_text(item, field="supporting_observation", max_length=MAX_RECOMMENDATION_ID_LENGTH)
            for item in supporting_observations
        ),
        expected_capability_impact=_normalize_text(
            expected_capability_impact,
            field="expected_capability_impact",
            max_length=MAX_EXPLANATION_LENGTH,
        ),
        explanation=_normalize_text(explanation, field="explanation", max_length=MAX_EXPLANATION_LENGTH),
    )


def _replace_state(state: _ObservationState, **changes: object) -> _ObservationState:
    values = {
        "foreground_application": state.foreground_application,
        "foreground_classification": state.foreground_classification,
        "cpu_utilization_percent": state.cpu_utilization_percent,
        "cpu_package_power_watts": state.cpu_package_power_watts,
        "cpu_temperature_celsius": state.cpu_temperature_celsius,
        "previous_cpu_temperature_celsius": state.previous_cpu_temperature_celsius,
        "gpu_utilization_percent": state.gpu_utilization_percent,
        "gpu_temperature_celsius": state.gpu_temperature_celsius,
        "available_memory_percent": state.available_memory_percent,
        "active_power_plan": state.active_power_plan,
        "process_started": state.process_started,
    }
    values.update(changes)
    return _ObservationState(**values)


def _is_idle(state: _ObservationState, thresholds: RecommendationThresholds) -> bool:
    if state.cpu_utilization_percent is None or state.cpu_utilization_percent > thresholds.idle_cpu_percent:
        return False
    if state.available_memory_percent is not None and state.available_memory_percent < thresholds.idle_memory_available_percent:
        return False
    return state.foreground_classification not in {"coding", "game"}


def _contains_text(value: str | None, expected: str) -> bool:
    return value is not None and expected.lower() in value.lower()


def _number_value(values: MappingProxyType[str, object] | dict[str, object], key: str) -> float | None:
    value = values.get(key)
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _first_number(values: MappingProxyType[str, object] | dict[str, object], keys: tuple[str, ...]) -> float | None:
    for index, key in enumerate(keys):
        if index >= len(keys):
            break
        value = _number_value(values, key)
        if value is not None:
            return value
    return None


def _string_value(values: MappingProxyType[str, object] | dict[str, object], key: str) -> str | None:
    value = values.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None
