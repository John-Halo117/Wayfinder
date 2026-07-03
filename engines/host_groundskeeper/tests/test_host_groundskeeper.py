from __future__ import annotations

from dataclasses import dataclass

from engines.host_groundskeeper import (
    HostGroundskeeperDependencies,
    register_host_groundskeeper,
)
from engines.host_groundskeeper.contracts import PluginDescriptor, SubscriptionDescriptor
from engines.host_groundskeeper.core.config import load_config
from engines.host_groundskeeper.core.module import HostGroundskeeperModule
from engines.host_groundskeeper.plugins.registry import PluginRegistry
from engines.host_groundskeeper.telemetry.logging import InMemoryLogSink
from engines.host_groundskeeper.telemetry.metrics import MetricsCollector


@dataclass(frozen=True)
class _SubscribeOk:
    status: str = "ok"


class _EventBus:
    def __init__(self) -> None:
        self.routes: tuple[str, ...] = ()

    def subscribe(self, route_pattern: str) -> _SubscribeOk:
        self.routes = (*self.routes, route_pattern)
        return _SubscribeOk()


def _dependencies() -> tuple[HostGroundskeeperDependencies, _EventBus, InMemoryLogSink]:
    bus = _EventBus()
    sink = InMemoryLogSink(max_entries=16)
    return HostGroundskeeperDependencies(event_bus=bus, logger=sink), bus, sink


def test_load_config_normalizes_and_enforces_caps():
    config = load_config(
        {
            "module_name": " host-groundskeeper ",
            "enabled": "true",
            "max_plugins": "4",
            "max_subscriptions": 3,
            "max_log_entries": 8,
            "max_metrics": 6,
        }
    )

    assert config.module_name == "host-groundskeeper"
    assert config.enabled is True
    assert config.max_plugins == 4
    assert config.max_subscriptions == 3
    assert config.max_log_entries == 8
    assert config.max_metrics == 6


def test_plugin_registry_rejects_duplicate_plugins_with_structured_failure():
    registry = PluginRegistry(max_plugins=2)
    plugin = PluginDescriptor("host.lifecycle", "1.0.0", "Lifecycle foundation.")

    first = registry.register(plugin)
    second = registry.register(plugin)

    assert first.status == "ok"
    assert second.status == "error"
    assert second.failure is not None
    assert second.failure.error_code == "HOST_PLUGIN_DUPLICATE"
    assert second.failure.recoverable is False


def test_default_registration_registers_plugin_and_event_subscriptions():
    dependencies, bus, sink = _dependencies()
    config = load_config({"max_plugins": 2, "max_subscriptions": 3, "max_log_entries": 8, "max_metrics": 8})

    module, registration = register_host_groundskeeper(config, dependencies)

    assert isinstance(module, HostGroundskeeperModule)
    assert registration.status == "ok"
    assert [plugin.plugin_id for plugin in registration.plugins] == ["host.lifecycle"]
    assert bus.routes == ("wayfinder.host.lifecycle.*", "wayfinder.host.health.*")
    assert sink.entries()[0].level == "info"


def test_registration_rejects_subscription_cap_without_mutating_subscriptions():
    dependencies, bus, _sink = _dependencies()
    config = load_config({"max_plugins": 2, "max_subscriptions": 1, "max_log_entries": 8, "max_metrics": 8})
    module = HostGroundskeeperModule.build(config, dependencies)

    registration = module.register(
        plugins=(PluginDescriptor("host.lifecycle", "1.0.0", "Lifecycle foundation."),),
        subscriptions=(
            SubscriptionDescriptor("wayfinder.host.lifecycle.*", "Lifecycle events."),
            SubscriptionDescriptor("wayfinder.host.health.*", "Health events."),
        ),
    )

    assert registration.status == "error"
    assert registration.failure is not None
    assert registration.failure.error_code == "HOST_SUBSCRIPTION_LIMIT"
    assert module.subscriptions == ()
    assert bus.routes == ()


def test_lifecycle_start_stop_and_health_are_observable():
    dependencies, _bus, _sink = _dependencies()
    config = load_config({"max_plugins": 2, "max_subscriptions": 3, "max_log_entries": 8, "max_metrics": 8})
    module, registration = register_host_groundskeeper(config, dependencies)

    start = module.start()
    health = module.health()
    stop = module.stop()

    assert registration.status == "ok"
    assert start.status == "ok"
    assert start.state == "running"
    assert health.status == "ok"
    assert health.lifecycle_state == "running"
    assert health.plugins_registered == 1
    assert health.subscriptions_registered == 2
    assert stop.status == "ok"
    assert stop.state == "stopped"


def test_disabled_lifecycle_returns_failure_and_health_error():
    dependencies, _bus, _sink = _dependencies()
    config = load_config({"enabled": False, "max_plugins": 2, "max_subscriptions": 3, "max_metrics": 8})
    module, registration = register_host_groundskeeper(config, dependencies)

    start = module.start()
    health = module.health()

    assert registration.status == "ok"
    assert start.status == "error"
    assert start.failure is not None
    assert start.failure.error_code == "HOST_DISABLED"
    assert health.status == "error"
    assert health.lifecycle_state == "disabled"


def test_metrics_interface_reports_limit_failures_without_throwing():
    metrics = MetricsCollector(max_metrics=1)

    metrics.increment("host.registration.ok")
    metrics.gauge("host.extra", 1)
    snapshot = metrics.snapshot()

    assert snapshot.status == "error"
    assert snapshot.failure is not None
    assert snapshot.failure.error_code == "HOST_METRIC_LIMIT"
    assert snapshot.counters["host.registration.ok"] == 1
