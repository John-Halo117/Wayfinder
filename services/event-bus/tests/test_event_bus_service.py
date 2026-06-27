import importlib.util
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "event_bus_service.py"
spec = importlib.util.spec_from_file_location("event_bus_service", MODULE_PATH)
event_bus_service = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = event_bus_service
spec.loader.exec_module(event_bus_service)

EventBusService = event_bus_service.EventBusService
route_matches = event_bus_service.route_matches
normalize_route = event_bus_service.normalize_route


def test_normalize_route_is_lowercase_and_strict():
    assert normalize_route(" ARK.Event.State.Change ") == "ark.event.state.change"


def test_route_matches_ark_subject_wildcards():
    assert route_matches("ark.event.*.change", "ark.event.state.change") is True
    assert route_matches("ark.call.opencode.>", "ark.call.opencode.code.analyze") is True
    assert route_matches("ark.event.*.change", "ark.event.state.sensor") is False


def test_subscribe_and_publish_delivers_to_matching_routes():
    bus = EventBusService(max_events=5, max_subscribers=3)
    first = bus.subscribe("ark.event.state.*")
    second = bus.subscribe("ark.metrics.>")
    envelope = bus.build_envelope(
        event_type="state",
        source="emitter.homeassistant",
        route="ark.event.state.change",
        payload={"entity_id": "sensor.kitchen"},
        correlation_id="req-1",
        causation_id="obs-1",
        metadata={"schema": "ark/contracts/event_v1"},
    )

    result = bus.publish(envelope)

    assert first.status == "ok"
    assert second.status == "ok"
    assert result.status == "ok"
    assert result.envelope is not None
    assert result.envelope.sequence == 1
    assert result.envelope.event_id == "evt-1"
    assert result.envelope.correlation_id == "req-1"
    assert result.delivered_to == (first.subscription.subscription_id,)


def test_replay_returns_ordered_events_after_cursor_with_limit():
    bus = EventBusService(max_events=5, max_replay_limit=2)
    for idx in range(3):
        bus.publish(
            bus.build_envelope(
                event_type="metric",
                source="system",
                route="ark.metrics.temperature",
                payload={"idx": idx},
            )
        )

    replay = bus.replay(after_sequence=1, limit=2)

    assert replay.status == "ok"
    assert [event.sequence for event in replay.events] == [2, 3]
    assert replay.next_cursor == 3


def test_publish_rejects_duplicate_event_id_with_structured_failure():
    bus = EventBusService(max_events=5)
    envelope = bus.build_envelope(
        event_id="event-1",
        event_type="state",
        source="system",
        route="ark.event.state.change",
        payload={},
    )

    first = bus.publish(envelope)
    second = bus.publish(envelope)

    assert first.status == "ok"
    assert second.status == "error"
    assert second.failure is not None
    assert second.failure.error_code == "EVENT_DUPLICATE_ID"
    assert second.failure.recoverable is False


def test_publish_rejects_oversized_payload_without_mutating_log():
    bus = EventBusService(max_events=5, max_payload_bytes=10)
    envelope = bus.build_envelope(
        event_type="state",
        source="system",
        route="ark.event.state.change",
        payload={"large": "x" * 20},
    )

    result = bus.publish(envelope)
    health = bus.health()

    assert result.status == "error"
    assert result.failure is not None
    assert result.failure.error_code == "EVENT_INVALID"
    assert health.events == 0


def test_subscribe_rejects_exhausted_capacity():
    bus = EventBusService(max_subscribers=1)

    first = bus.subscribe("ark.event.>")
    second = bus.subscribe("ark.metrics.>")

    assert first.status == "ok"
    assert second.status == "error"
    assert second.failure is not None
    assert second.failure.error_code == "EVENT_SUBSCRIBER_LIMIT"


def test_health_reports_bounds():
    bus = EventBusService(max_events=7, max_subscribers=4, max_payload_bytes=128, max_replay_limit=3)
    bus.subscribe("ark.event.>")
    bus.publish(bus.build_envelope(event_type="status", source="system", route="ark.event.status", payload={}))

    health = bus.health()

    assert health.status == "ok"
    assert health.events == 1
    assert health.subscribers == 1
    assert health.next_sequence == 2
    assert health.max_events == 7
    assert health.max_subscribers == 4
    assert health.max_payload_bytes == 128
    assert health.max_replay_limit == 3
