from __future__ import annotations

from engines.host_groundskeeper.contracts import HostObservation, RecommendationThresholds
from engines.host_groundskeeper.core.recommendations import HostRecommendationEngine


def _obs(observation: str, values: dict[str, object], timestamp: int = 1) -> HostObservation:
    return HostObservation(
        timestamp=timestamp,
        observation=observation,
        source="test",
        confidence=1.0,
        values=values,
        delta=values,
    )


def _ids(result) -> tuple[str, ...]:
    return tuple(item.recommendation_id for item in result.recommendations)


def test_recommends_coding_profile_for_foreground_ide_without_changing_power_plan():
    engine = HostRecommendationEngine()

    result = engine.evaluate(
        (
            _obs("ForegroundApplicationChanged", {"foreground_application": "Code.exe"}),
            _obs("PowerPlanChanged", {"active_power_plan": "Balanced"}),
        )
    )

    assert result.status == "ok"
    assert _ids(result) == ("host.profile.coding",)
    recommendation = result.recommendations[0]
    assert recommendation.confidence > 0.8
    assert "no automatic action" in recommendation.expected_capability_impact.lower()
    assert recommendation.supporting_observations == ("ForegroundApplicationChanged", "PowerPlanChanged")


def test_recommends_gaming_profile_for_known_game():
    engine = HostRecommendationEngine()

    result = engine.evaluate(
        (
            _obs("ForegroundApplicationChanged", {"foreground_application": "Cyberpunk2077.exe"}),
            _obs("PowerPlanChanged", {"active_power_plan": "Balanced"}),
        )
    )

    assert "host.profile.gaming" in _ids(result)
    assert result.recommendations[0].estimated_cost
    assert result.recommendations[0].estimated_benefit


def test_recommends_eco_and_idle_opportunity_for_idle_host():
    engine = HostRecommendationEngine(
        thresholds=RecommendationThresholds(idle_cpu_percent=10.0, idle_memory_available_percent=20.0)
    )

    result = engine.evaluate(
        (
            _obs("ForegroundApplicationChanged", {"foreground_application": "notepad.exe"}),
            _obs("HostCpuChanged", {"cpu_utilization_percent": 3}),
            _obs("MemoryChanged", {"available_megabytes": 6000, "total_megabytes": 16000}),
            _obs("PowerPlanChanged", {"active_power_plan": "Balanced"}),
        )
    )

    assert "host.profile.eco" in _ids(result)
    assert "host.idle.opportunity" in _ids(result)


def test_recommends_background_process_review_for_other_process_start():
    engine = HostRecommendationEngine()

    result = engine.evaluate((_obs("ProcessStarted", {"process": "updater:44"}),))

    assert _ids(result) == ("host.process.background-review",)
    assert "updater:44" in result.recommendations[0].explanation


def test_recommends_high_cpu_power_when_observed_above_threshold():
    engine = HostRecommendationEngine(thresholds=RecommendationThresholds(high_cpu_package_power_watts=35.0))

    result = engine.evaluate((_obs("HostCpuChanged", {"cpu_package_power_watts": 42.0}),))

    assert _ids(result) == ("host.cpu.package-power-high",)
    assert result.recommendations[0].supporting_observations == ("HostCpuChanged",)


def test_recommends_gpu_review_when_gpu_active_without_foreground_game():
    engine = HostRecommendationEngine(thresholds=RecommendationThresholds(gpu_active_percent=10.0))

    result = engine.evaluate(
        (
            _obs("ForegroundApplicationChanged", {"foreground_application": "Code.exe"}),
            _obs("HostGpuChanged", {"gpu_utilization_percent": 30}),
        )
    )

    assert "host.gpu.active-without-foreground-workload" in _ids(result)


def test_recommends_thermal_trend_when_temperature_increases():
    engine = HostRecommendationEngine(thresholds=RecommendationThresholds(thermal_trend_celsius=4.0))

    result = engine.evaluate(
        (
            _obs("HostCpuChanged", {"package_temperature_celsius": 60.0}, timestamp=1),
            _obs("HostCpuChanged", {"package_temperature_celsius": 65.0}, timestamp=2),
        )
    )

    assert _ids(result) == ("host.thermal.trend-increasing",)


def test_suppresses_duplicate_recommendation_batches():
    engine = HostRecommendationEngine()
    observations = (
        _obs("ForegroundApplicationChanged", {"foreground_application": "Code.exe"}),
        _obs("PowerPlanChanged", {"active_power_plan": "Balanced"}),
    )

    first = engine.evaluate(observations)
    second = engine.evaluate(observations)

    assert _ids(first) == ("host.profile.coding",)
    assert second.status == "ok"
    assert second.recommendations == ()


def test_rejects_excess_observations_with_structured_failure():
    engine = HostRecommendationEngine(max_observations=1)

    result = engine.evaluate(
        (
            _obs("HostCpuChanged", {"cpu_utilization_percent": 1}),
            _obs("MemoryChanged", {"available_megabytes": 1, "total_megabytes": 2}),
        )
    )

    assert result.status == "error"
    assert result.failure is not None
    assert result.failure.error_code == "HOST_RECOMMENDATION_OBSERVATION_LIMIT"


def test_recommendation_schema_contains_required_advisory_fields():
    engine = HostRecommendationEngine()

    result = engine.evaluate((_obs("HostCpuChanged", {"cpu_package_power_watts": 90.0}),))
    recommendation = result.recommendations[0]

    assert recommendation.recommendation_id
    assert 0.0 <= recommendation.confidence <= 1.0
    assert recommendation.estimated_benefit
    assert recommendation.estimated_cost
    assert recommendation.supporting_observations
    assert recommendation.expected_capability_impact
    assert recommendation.explanation
