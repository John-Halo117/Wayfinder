from __future__ import annotations

from engines.host_groundskeeper.contracts import HostObservation, ObservationThresholds
from engines.host_groundskeeper.core.observer import HostObservationEngine, build_process_change_observations, calculate_delta, classify_process
from engines.host_groundskeeper.telemetry.publisher import InMemoryObservationPublisher


def _observation(timestamp: int, values: dict[str, object], observation: str = "HostCpuChanged") -> HostObservation:
    return HostObservation(
        timestamp=timestamp,
        observation=observation,
        source="test",
        confidence=1.0,
        values=values,
        delta=values,
    )


def test_delta_suppression_does_not_publish_duplicate_events():
    publisher = InMemoryObservationPublisher(max_events=4)
    engine = HostObservationEngine(publisher, coalesce_window_seconds=0)

    first = engine.process(_observation(1, {"cpu_utilization_percent": 20}))
    second = engine.process(_observation(2, {"cpu_utilization_percent": 20}))

    assert first.published is True
    assert second.status == "ok"
    assert second.published is False
    assert len(publisher.events()) == 1


def test_threshold_behavior_publishes_only_material_changes():
    publisher = InMemoryObservationPublisher(max_events=4)
    thresholds = ObservationThresholds(cpu_utilization_percent=5.0)
    engine = HostObservationEngine(publisher, thresholds=thresholds, coalesce_window_seconds=0)

    engine.process(_observation(1, {"cpu_utilization_percent": 20}))
    small = engine.process(_observation(2, {"cpu_utilization_percent": 24}))
    large = engine.process(_observation(3, {"cpu_utilization_percent": 25}))

    assert small.published is False
    assert large.published is True
    assert large.observation is not None
    assert large.observation.delta["cpu_utilization_percent"] == 25
    assert len(publisher.events()) == 2


def test_event_coalescing_suppresses_rapid_changes():
    publisher = InMemoryObservationPublisher(max_events=4)
    thresholds = ObservationThresholds(cpu_utilization_percent=1.0)
    engine = HostObservationEngine(publisher, thresholds=thresholds, coalesce_window_seconds=5)

    engine.process(_observation(10, {"cpu_utilization_percent": 20}))
    rapid = engine.process(_observation(12, {"cpu_utilization_percent": 30}))
    later = engine.process(_observation(16, {"cpu_utilization_percent": 31}))

    assert rapid.published is False
    assert later.published is True
    assert len(publisher.events()) == 2


def test_process_detection_classifies_known_coding_and_game_processes():
    assert classify_process("Code.exe") == "coding"
    assert classify_process("pycharm64") == "coding"
    assert classify_process("Cyberpunk2077.exe") == "game"
    assert classify_process("steam") == "game"
    assert classify_process("notepad.exe") == "other"


def test_event_publication_reports_publisher_failures():
    publisher = InMemoryObservationPublisher(max_events=1)
    engine = HostObservationEngine(publisher, coalesce_window_seconds=0)

    first = engine.process(_observation(1, {"available_memory_megabytes": 4000}, "MemoryChanged"))
    second = engine.process(_observation(2, {"available_memory_megabytes": 3000}, "MemoryChanged"))

    assert first.published is True
    assert second.status == "error"
    assert second.failure is not None
    assert second.failure.error_code == "HOST_OBSERVATION_PUBLISH_FAILED"


def test_calculate_delta_handles_state_changes_and_new_fields():
    delta = calculate_delta(
        {"foreground_application": "Code", "available_memory_megabytes": 4000},
        {"foreground_application": "rider64", "available_memory_megabytes": 3900, "active_power_plan": "Balanced"},
        thresholds=ObservationThresholds(memory_megabytes=256),
    )

    assert delta["foreground_application"] == "rider64"
    assert delta["active_power_plan"] == "Balanced"
    assert "available_memory_megabytes" not in delta


def test_process_start_and_exit_observations_are_bounded_and_classified():
    observations = build_process_change_observations(
        previous_processes=("Code:1", "notepad:2"),
        current_processes=("Code:1", "Cyberpunk2077:3"),
        timestamp=10,
        max_events=4,
    )

    assert [item.observation for item in observations] == ["ProcessStarted", "ProcessExited"]
    assert observations[0].values["classification"] == "game"
    assert observations[1].values["classification"] == "other"
