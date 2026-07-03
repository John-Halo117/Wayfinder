"""Host Groundskeeper composition root."""

from __future__ import annotations

from dataclasses import dataclass

from ..contracts.interfaces import (
    Failure,
    HealthResponse,
    HostGroundskeeperConfig,
    HostGroundskeeperDependencies,
    LifecycleResult,
    ModuleRegistration,
    PluginDescriptor,
    SubscriptionDescriptor,
)
from ..egress.health import build_health_response
from ..ingress.subscriptions import subscribe_to_events
from ..plugins.registry import PluginRegistry
from ..scheduler.lifecycle import LifecycleController
from ..telemetry.logging import StructuredLogger
from ..telemetry.metrics import MetricsCollector


@dataclass
class HostGroundskeeperModule:
    """Dependency-injected module facade.

    Inputs: HostGroundskeeperConfig and HostGroundskeeperDependencies.
    Outputs: registration, lifecycle, metrics, and health records.
    Runtime: O(max_plugins + max_subscriptions + max_log_entries) for registration;
    lifecycle and health are O(metric_count), bounded by max_metrics.
    Memory: O(max_plugins + max_subscriptions + max_log_entries + max_metrics).
    Failure: construction rejects missing dependencies, operations return structured
    failures. Deterministic: yes when injected dependencies are deterministic.
    """

    config: HostGroundskeeperConfig
    dependencies: HostGroundskeeperDependencies
    registry: PluginRegistry
    lifecycle: LifecycleController
    metrics: MetricsCollector
    logger: StructuredLogger
    subscriptions: tuple[SubscriptionDescriptor, ...] = ()

    @classmethod
    def build(
        cls,
        config: HostGroundskeeperConfig,
        dependencies: HostGroundskeeperDependencies,
    ) -> "HostGroundskeeperModule":
        if dependencies.event_bus is None:
            raise ValueError("event_bus dependency is required")
        if dependencies.logger is None:
            raise ValueError("logger dependency is required")
        return cls(
            config=config,
            dependencies=dependencies,
            registry=PluginRegistry(max_plugins=config.max_plugins),
            lifecycle=LifecycleController(),
            metrics=MetricsCollector(max_metrics=config.max_metrics),
            logger=StructuredLogger(dependencies.logger, max_entries=config.max_log_entries),
        )

    def register(
        self,
        plugins: tuple[PluginDescriptor, ...],
        subscriptions: tuple[SubscriptionDescriptor, ...],
    ) -> ModuleRegistration:
        """Register plugins and event subscriptions.

        Inputs: bounded plugin and subscription descriptors.
        Outputs: ModuleRegistration.
        Runtime: O(plugin_count + subscription_count), bounded by config caps.
        Memory: O(plugin_count + subscription_count), bounded by config caps.
        Failure: returns structured failures for caps, duplicates, or subscription
        failure. Deterministic: yes when event bus is deterministic.
        """

        if len(plugins) > self.config.max_plugins:
            return self._registration_failure("HOST_PLUGIN_LIMIT", "plugin count exceeds configured maximum")
        if len(subscriptions) > self.config.max_subscriptions:
            return self._registration_failure(
                "HOST_SUBSCRIPTION_LIMIT",
                "subscription count exceeds configured maximum",
            )
        plugin_result = self.registry.register_many(plugins)
        if plugin_result.failure is not None:
            return self._registration_failure(plugin_result.failure.error_code, plugin_result.failure.reason)
        subscription_result = subscribe_to_events(
            self.dependencies.event_bus,
            subscriptions,
            max_subscriptions=self.config.max_subscriptions,
        )
        if subscription_result.failure is not None:
            return self._registration_failure(
                subscription_result.failure.error_code,
                subscription_result.failure.reason,
            )
        self.subscriptions = subscriptions
        self.metrics.increment("host.registration.ok")
        self.logger.info("host groundskeeper registered", {"module": self.config.module_name})
        return ModuleRegistration(
            status="ok",
            module_name=self.config.module_name,
            plugins=self.registry.plugins(),
            subscriptions=self.subscriptions,
        )

    def start(self) -> LifecycleResult:
        """Start the module lifecycle.

        Inputs: none. Outputs: LifecycleResult. Runtime: O(1). Memory: O(1).
        Failure: invalid transition returns structured failure. Deterministic: yes.
        """

        result = self.lifecycle.start(enabled=self.config.enabled)
        self.metrics.increment(f"host.lifecycle.{result.status}")
        self.logger.info("host groundskeeper lifecycle transition", {"state": result.state})
        return result

    def stop(self) -> LifecycleResult:
        """Stop the module lifecycle.

        Inputs: none. Outputs: LifecycleResult. Runtime: O(1). Memory: O(1).
        Failure: invalid transition returns structured failure. Deterministic: yes.
        """

        result = self.lifecycle.stop()
        self.metrics.increment(f"host.lifecycle.{result.status}")
        self.logger.info("host groundskeeper lifecycle transition", {"state": result.state})
        return result

    def health(self) -> HealthResponse:
        """Return a framework-neutral health endpoint response.

        Inputs: none. Outputs: HealthResponse. Runtime: O(metric_count), bounded by
        max_metrics. Memory: O(metric_count). Failure: none. Deterministic: yes.
        """

        return build_health_response(
            module_name=self.config.module_name,
            lifecycle_state=self.lifecycle.state,
            plugins_registered=len(self.registry.plugins()),
            subscriptions_registered=len(self.subscriptions),
            metrics=self.metrics.snapshot(),
        )

    def _registration_failure(self, error_code: str, reason: str) -> ModuleRegistration:
        failure = Failure.build(error_code, reason, {"module": self.config.module_name})
        self.metrics.increment("host.registration.error")
        self.logger.error("host groundskeeper registration failed", {"error_code": failure.error_code})
        return ModuleRegistration(
            status="error",
            module_name=self.config.module_name,
            plugins=(),
            subscriptions=(),
            failure=failure,
        )


def register_host_groundskeeper(
    config: HostGroundskeeperConfig,
    dependencies: HostGroundskeeperDependencies,
) -> tuple[HostGroundskeeperModule, ModuleRegistration]:
    """Build and register the default Host Groundskeeper foundation.

    Inputs: strict config and injected dependencies.
    Outputs: module plus ModuleRegistration.
    Runtime: O(1) because default foundation has one plugin and two subscriptions.
    Memory: O(1). Failure: construction raises ValueError for missing dependencies;
    registration returns structured failures. Deterministic: yes when dependencies
    are deterministic.
    """

    module = HostGroundskeeperModule.build(config, dependencies)
    registration = module.register(
        plugins=(
            PluginDescriptor(
                plugin_id="host.lifecycle",
                version="1.0.0",
                description="Lifecycle and health foundation for host groundskeeping.",
            ),
        ),
        subscriptions=(
            SubscriptionDescriptor(
                route_pattern="wayfinder.host.lifecycle.*",
                purpose="Observe host lifecycle events.",
            ),
            SubscriptionDescriptor(
                route_pattern="wayfinder.host.health.*",
                purpose="Observe host health probe events.",
            ),
        ),
    )
    return module, registration
