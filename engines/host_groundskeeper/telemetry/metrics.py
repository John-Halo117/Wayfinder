"""Metrics collection interface for Host Groundskeeper."""

from __future__ import annotations

from types import MappingProxyType

from ..contracts.interfaces import Failure, MetricsSnapshot, _normalize_text


class MetricsCollector:
    """Bounded in-memory metrics collector.

    Inputs: counter/gauge names and integer values. Outputs: MetricsSnapshot.
    Runtime: O(metric_count), bounded by max_metrics. Memory: O(max_metrics).
    Failure: returns structured failure in snapshots when limits are exceeded by
    direct invalid calls. Deterministic: yes.
    """

    def __init__(self, *, max_metrics: int) -> None:
        if max_metrics <= 0:
            raise ValueError("max_metrics must be positive")
        self._max_metrics = max_metrics
        self._counters: dict[str, int] = {}
        self._gauges: dict[str, int] = {}
        self._failure: Failure | None = None

    def increment(self, name: str, amount: int = 1) -> None:
        metric = self._normalize_metric(name)
        if amount <= 0:
            self._failure = Failure.build("HOST_METRIC_INVALID", "counter increment must be positive")
            return
        if metric not in self._counters and self._metric_count() >= self._max_metrics:
            self._failure = Failure.build("HOST_METRIC_LIMIT", "metric count exceeds configured maximum")
            return
        self._counters[metric] = self._counters.get(metric, 0) + amount

    def gauge(self, name: str, value: int) -> None:
        metric = self._normalize_metric(name)
        if metric not in self._gauges and self._metric_count() >= self._max_metrics:
            self._failure = Failure.build("HOST_METRIC_LIMIT", "metric count exceeds configured maximum")
            return
        self._gauges[metric] = int(value)

    def snapshot(self) -> MetricsSnapshot:
        status = "error" if self._failure is not None else "ok"
        return MetricsSnapshot(
            status=status,
            counters=MappingProxyType(dict(self._counters)),
            gauges=MappingProxyType(dict(self._gauges)),
            failure=self._failure,
        )

    def _metric_count(self) -> int:
        return len(set(self._counters) | set(self._gauges))

    @staticmethod
    def _normalize_metric(name: str) -> str:
        metric = _normalize_text(name, field="metric", max_length=128).lower()
        allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_.-")
        if any(ch not in allowed for ch in metric):
            raise ValueError("metric contains invalid characters")
        return metric
