"""Bounded metadata-only plugin registry."""

from __future__ import annotations

from dataclasses import dataclass

from ..contracts.interfaces import Failure, PluginDescriptor, _normalize_text


@dataclass(frozen=True)
class PluginRegistryResult:
    """Result of plugin registry mutation."""

    status: str
    plugins: tuple[PluginDescriptor, ...]
    failure: Failure | None = None


class PluginRegistry:
    """Local bounded plugin descriptor registry.

    Inputs: PluginDescriptor values. Outputs: PluginRegistryResult and immutable
    plugin tuples. Runtime: O(plugin_count), bounded by max_plugins. Memory:
    O(max_plugins). Failure: duplicate IDs, invalid descriptors, or capacity
    exhaustion return structured failures. Deterministic: yes.
    """

    def __init__(self, *, max_plugins: int) -> None:
        if max_plugins <= 0:
            raise ValueError("max_plugins must be positive")
        self._max_plugins = max_plugins
        self._plugins: tuple[PluginDescriptor, ...] = ()

    def register_many(self, plugins: tuple[PluginDescriptor, ...]) -> PluginRegistryResult:
        if len(plugins) > self._max_plugins:
            return PluginRegistryResult(
                status="error",
                plugins=self._plugins,
                failure=Failure.build("HOST_PLUGIN_LIMIT", "plugin count exceeds configured maximum"),
            )
        for index, plugin in enumerate(plugins):
            if index >= self._max_plugins:
                return PluginRegistryResult(
                    status="error",
                    plugins=self._plugins,
                    failure=Failure.build("HOST_PLUGIN_LIMIT", "plugin iteration exceeded configured maximum"),
                )
            result = self.register(plugin)
            if result.failure is not None:
                return result
        return PluginRegistryResult(status="ok", plugins=self._plugins)

    def register(self, plugin: PluginDescriptor) -> PluginRegistryResult:
        if len(self._plugins) >= self._max_plugins:
            return PluginRegistryResult(
                status="error",
                plugins=self._plugins,
                failure=Failure.build("HOST_PLUGIN_LIMIT", "plugin registry is full"),
            )
        try:
            normalized = PluginDescriptor(
                plugin_id=_normalize_text(plugin.plugin_id, field="plugin_id", max_length=128),
                version=_normalize_text(plugin.version, field="version", max_length=128),
                description=_normalize_text(plugin.description, field="description", max_length=512),
                enabled=plugin.enabled,
            )
        except ValueError as exc:
            return PluginRegistryResult(
                status="error",
                plugins=self._plugins,
                failure=Failure.build("HOST_PLUGIN_INVALID", str(exc)),
            )
        for existing in self._plugins:
            if existing.plugin_id == normalized.plugin_id:
                return PluginRegistryResult(
                    status="error",
                    plugins=self._plugins,
                    failure=Failure.build(
                        "HOST_PLUGIN_DUPLICATE",
                        "plugin_id already registered",
                        {"plugin_id": normalized.plugin_id},
                        recoverable=False,
                    ),
                )
        self._plugins = (*self._plugins, normalized)
        return PluginRegistryResult(status="ok", plugins=self._plugins)

    def plugins(self) -> tuple[PluginDescriptor, ...]:
        return self._plugins
