"""Configuration loading for Host Groundskeeper."""

from __future__ import annotations

from typing import Mapping

from ..contracts.interfaces import Failure, HostGroundskeeperConfig, MAX_NAME_LENGTH


def load_config(values: Mapping[str, object] | None = None) -> HostGroundskeeperConfig:
    """Load and validate Host Groundskeeper configuration from a mapping.

    Inputs: mapping with optional module_name, enabled, max_plugins,
    max_subscriptions, max_log_entries, and max_metrics keys.
    Outputs: HostGroundskeeperConfig.
    Runtime: O(known_key_count), bounded to six known keys. Memory: O(1).
    Failure: raises ValueError for invalid caps or malformed values.
    Deterministic: yes.
    """

    raw = dict(values or {})
    module_name = str(raw.get("module_name", HostGroundskeeperConfig.module_name)).strip()
    if not module_name:
        raise ValueError("module_name is required")
    if len(module_name) > MAX_NAME_LENGTH:
        raise ValueError("module_name exceeds maximum length")
    return HostGroundskeeperConfig(
        module_name=module_name,
        enabled=_coerce_bool(raw.get("enabled", True)),
        max_plugins=_positive_int(raw.get("max_plugins", HostGroundskeeperConfig.max_plugins), "max_plugins"),
        max_subscriptions=_positive_int(
            raw.get("max_subscriptions", HostGroundskeeperConfig.max_subscriptions),
            "max_subscriptions",
        ),
        max_log_entries=_positive_int(
            raw.get("max_log_entries", HostGroundskeeperConfig.max_log_entries),
            "max_log_entries",
        ),
        max_metrics=_positive_int(raw.get("max_metrics", HostGroundskeeperConfig.max_metrics), "max_metrics"),
    )


def config_failure(error: ValueError) -> Failure:
    """Convert configuration exceptions to the standard failure model.

    Inputs: ValueError. Outputs: Failure. Runtime: O(1). Memory: O(1).
    Failure: none. Deterministic: yes.
    """

    return Failure.build("HOST_CONFIG_INVALID", str(error), recoverable=True)


def _positive_int(value: object, field: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be an integer")
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be an integer") from exc
    if number <= 0:
        raise ValueError(f"{field} must be positive")
    return number


def _coerce_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    raise ValueError("enabled must be boolean-like")
