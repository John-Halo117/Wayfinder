"""Typed Host Groundskeeper public interfaces.

Contract:
- Inputs: explicit dataclasses, primitive strings, and bounded mappings.
- Outputs: immutable records or structured failures.
- Runtime constraint: operations are O(plugin_count + subscription_count), bounded
  by HostGroundskeeperConfig(max_plugins, max_subscriptions, max_log_entries).
- Memory assumption: O(plugin_count + subscription_count + log_entries), bounded
  by configuration caps.
- Failure cases: invalid configuration, duplicate plugins, exhausted registry,
  subscription failure, lifecycle misuse, logging bounds, and invalid health input.
- Determinism: all behavior is deterministic when dependencies are deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping, Protocol

MAX_NAME_LENGTH = 128
MAX_DESCRIPTION_LENGTH = 512
MAX_ROUTE_LENGTH = 256
MAX_CONTEXT_KEYS = 32
MAX_CONTEXT_VALUE_LENGTH = 512
DEFAULT_MAX_PLUGINS = 32
DEFAULT_MAX_SUBSCRIPTIONS = 32
DEFAULT_MAX_LOG_ENTRIES = 256
DEFAULT_MAX_METRICS = 64
DEFAULT_MAX_OBSERVATIONS = 512
DEFAULT_COALESCE_WINDOW_SECONDS = 5
MAX_OBSERVATION_TYPE_LENGTH = 128
MAX_SOURCE_LENGTH = 128
MAX_FIELD_COUNT = 64
DEFAULT_MAX_RECOMMENDATIONS = 64
MAX_RECOMMENDATION_ID_LENGTH = 160
MAX_EXPLANATION_LENGTH = 1024
MAX_SUPPORTING_OBSERVATIONS = 16


@dataclass(frozen=True)
class Failure:
    """Standard structured failure object.

    Runtime: O(context key count), bounded by MAX_CONTEXT_KEYS.
    Memory: O(context key count).
    Failure: raises ValueError for oversized context.
    Deterministic: yes.
    """

    status: str
    error_code: str
    reason: str
    context: Mapping[str, object]
    recoverable: bool

    @classmethod
    def build(
        cls,
        error_code: str,
        reason: str,
        context: Mapping[str, object] | None = None,
        recoverable: bool = True,
    ) -> "Failure":
        normalized = dict(context or {})
        if len(normalized) > MAX_CONTEXT_KEYS:
            raise ValueError("failure context exceeds maximum key count")
        return cls(
            status="error",
            error_code=_normalize_text(error_code, field="error_code", max_length=MAX_NAME_LENGTH),
            reason=_normalize_text(reason, field="reason", max_length=MAX_DESCRIPTION_LENGTH),
            context=MappingProxyType(normalized),
            recoverable=recoverable,
        )


@dataclass(frozen=True)
class HostGroundskeeperConfig:
    """Runtime caps and identity for the Host Groundskeeper module.

    Runtime: O(1). Memory: O(1). Failure: invalid caps or empty module identity.
    Deterministic: yes.
    """

    module_name: str = "host-groundskeeper"
    enabled: bool = True
    max_plugins: int = DEFAULT_MAX_PLUGINS
    max_subscriptions: int = DEFAULT_MAX_SUBSCRIPTIONS
    max_log_entries: int = DEFAULT_MAX_LOG_ENTRIES
    max_metrics: int = DEFAULT_MAX_METRICS


@dataclass(frozen=True)
class PluginDescriptor:
    """Metadata-only plugin registration record.

    Runtime: O(1). Memory: O(1). Failure: invalid fields during registry insert.
    Deterministic: yes.
    """

    plugin_id: str
    version: str
    description: str
    enabled: bool = True


@dataclass(frozen=True)
class SubscriptionDescriptor:
    """Event subscription requested by the module.

    Runtime: O(1). Memory: O(1). Failure: invalid route during subscription setup.
    Deterministic: yes.
    """

    route_pattern: str
    purpose: str


@dataclass(frozen=True)
class ModuleRegistration:
    """Observable result of registering the Host Groundskeeper module."""

    status: str
    module_name: str
    plugins: tuple[PluginDescriptor, ...]
    subscriptions: tuple[SubscriptionDescriptor, ...]
    failure: Failure | None = None


@dataclass(frozen=True)
class LifecycleResult:
    """Structured lifecycle transition result."""

    status: str
    state: str
    failure: Failure | None = None


@dataclass(frozen=True)
class LogEntry:
    """Structured log entry emitted through the injected logger."""

    level: str
    message: str
    context: Mapping[str, object]


@dataclass(frozen=True)
class MetricsSnapshot:
    """Bounded metric snapshot emitted by the metrics interface."""

    status: str
    counters: Mapping[str, int]
    gauges: Mapping[str, int]
    failure: Failure | None = None


@dataclass(frozen=True)
class ObservationThresholds:
    """Material-change thresholds for host observations.

    Runtime: O(1). Memory: O(1). Failure: invalid negative thresholds are
    rejected by observation engine construction. Deterministic: yes.
    """

    cpu_utilization_percent: float = 2.0
    cpu_frequency_mhz: float = 100.0
    cpu_temperature_celsius: float = 2.0
    gpu_utilization_percent: float = 2.0
    gpu_vram_megabytes: float = 128.0
    gpu_temperature_celsius: float = 2.0
    memory_megabytes: float = 256.0
    storage_utilization_percent: float = 2.0
    storage_free_megabytes: float = 1024.0
    generic_numeric: float = 1.0


@dataclass(frozen=True)
class HostObservation:
    """Canonical host observation event.

    Runtime: O(field count), bounded by MAX_FIELD_COUNT. Memory: O(field count).
    Failure: invalid fields are rejected by the observer. Deterministic: yes.
    """

    timestamp: int
    observation: str
    source: str
    confidence: float
    values: Mapping[str, object]
    delta: Mapping[str, object]


@dataclass(frozen=True)
class ObservationPublishResult:
    """Result of processing and publishing one candidate observation."""

    status: str
    published: bool
    observation: HostObservation | None = None
    failure: Failure | None = None


@dataclass(frozen=True)
class RecommendationThresholds:
    """Advisory recommendation thresholds.

    Runtime: O(1). Memory: O(1). Failure: negative thresholds are rejected by the
    recommendation engine. Deterministic: yes.
    """

    idle_cpu_percent: float = 8.0
    idle_memory_available_percent: float = 25.0
    high_cpu_package_power_watts: float = 45.0
    high_cpu_temperature_celsius: float = 85.0
    gpu_active_percent: float = 15.0
    thermal_trend_celsius: float = 5.0


@dataclass(frozen=True)
class HostRecommendation:
    """Advisory-only recommendation derived from host observations.

    Runtime: O(supporting observation count), bounded by
    MAX_SUPPORTING_OBSERVATIONS. Memory: O(supporting observation count). Failure:
    invalid fields are rejected by the recommendation engine. Deterministic: yes.
    """

    recommendation_id: str
    confidence: float
    estimated_benefit: str
    estimated_cost: str
    supporting_observations: tuple[str, ...]
    expected_capability_impact: str
    explanation: str


@dataclass(frozen=True)
class RecommendationResult:
    """Result of evaluating host observations for advisory recommendations."""

    status: str
    recommendations: tuple[HostRecommendation, ...]
    failure: Failure | None = None


@dataclass(frozen=True)
class HealthResponse:
    """Framework-neutral health endpoint response."""

    status: str
    module_name: str
    lifecycle_state: str
    plugins_registered: int
    subscriptions_registered: int
    metrics: MetricsSnapshot
    failure: Failure | None = None


class EventBusPort(Protocol):
    """Strict event bus dependency expected by ingress subscription wiring."""

    def subscribe(self, route_pattern: str) -> object:
        """Subscribe to a route pattern and return an object with a status field."""


class LoggerPort(Protocol):
    """Structured logging dependency for Host Groundskeeper."""

    def write(self, entry: LogEntry) -> None:
        """Persist or forward a bounded structured log entry."""


class ObservationPublisherPort(Protocol):
    """Strict telemetry publication dependency for host observations."""

    def publish(self, observation: HostObservation) -> object:
        """Publish an observation and return an object with a status field."""


@dataclass(frozen=True)
class HostGroundskeeperDependencies:
    """Explicit dependency injection boundary for the module.

    Runtime: O(1). Memory: O(1). Failure: missing dependency is rejected by module
    construction. Deterministic: depends on injected ports.
    """

    event_bus: EventBusPort
    logger: LoggerPort


def _normalize_text(value: str, *, field: str, max_length: int) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field} is required")
    if len(normalized) > max_length:
        raise ValueError(f"{field} exceeds maximum length")
    return normalized
