"""Configuration loading for the Odysseus workspace adapter."""

from __future__ import annotations

import os
from typing import Mapping

from .interfaces import (
    DEFAULT_CHAT_PATH,
    DEFAULT_HEALTH_PATH,
    DEFAULT_TIMEOUT_SECONDS,
    Failure,
    MAX_PATH_LENGTH,
    MAX_PROMPT_CHARS,
    MAX_RESPONSE_BYTES,
    MAX_TIMEOUT_SECONDS,
    MAX_URL_LENGTH,
    MIN_TIMEOUT_SECONDS,
    OdysseusConfig,
)


def load_odysseus_config(values: Mapping[str, object] | None = None) -> OdysseusConfig:
    """Load and validate Odysseus configuration from a mapping or environment.

    Inputs: optional mapping with ODYSSEUS_BASE_URL, ODYSSEUS_ENABLED,
    ODYSSEUS_TIMEOUT_SECONDS, ODYSSEUS_CHAT_PATH, and ODYSSEUS_HEALTH_PATH.
    Outputs: OdysseusConfig.
    Runtime: O(known_key_count), bounded to five known keys. Memory: O(1).
    Failure: raises ValueError for invalid booleans, URLs, paths, or timeouts.
    Deterministic: yes for explicit mappings; environment-dependent otherwise.
    """

    raw = values or os.environ
    enabled = _coerce_bool(raw.get("ODYSSEUS_ENABLED", "false"))
    base_url = str(raw.get("ODYSSEUS_BASE_URL", "")).strip().rstrip("/")
    timeout_seconds = _coerce_timeout(raw.get("ODYSSEUS_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS))
    chat_path = _coerce_path(raw.get("ODYSSEUS_CHAT_PATH", DEFAULT_CHAT_PATH), "ODYSSEUS_CHAT_PATH")
    health_path = _coerce_path(raw.get("ODYSSEUS_HEALTH_PATH", DEFAULT_HEALTH_PATH), "ODYSSEUS_HEALTH_PATH")
    if enabled and not base_url:
        raise ValueError("ODYSSEUS_BASE_URL is required when ODYSSEUS_ENABLED is true")
    if base_url:
        _validate_base_url(base_url)
    return OdysseusConfig(
        enabled=enabled,
        base_url=base_url,
        timeout_seconds=timeout_seconds,
        chat_path=chat_path,
        health_path=health_path,
        max_prompt_chars=MAX_PROMPT_CHARS,
        max_response_bytes=MAX_RESPONSE_BYTES,
    )


def config_failure(error: ValueError) -> Failure:
    """Convert configuration exceptions to the standard failure model.

    Inputs: ValueError. Outputs: Failure. Runtime: O(1). Memory: O(1).
    Failure: none. Deterministic: yes.
    """

    return Failure.build("ODYSSEUS_CONFIG_INVALID", str(error), recoverable=True)


def _coerce_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    raise ValueError("ODYSSEUS_ENABLED must be boolean-like")


def _coerce_timeout(value: object) -> float:
    if isinstance(value, bool):
        raise ValueError("ODYSSEUS_TIMEOUT_SECONDS must be numeric")
    try:
        timeout = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("ODYSSEUS_TIMEOUT_SECONDS must be numeric") from exc
    if timeout < MIN_TIMEOUT_SECONDS or timeout > MAX_TIMEOUT_SECONDS:
        raise ValueError("ODYSSEUS_TIMEOUT_SECONDS is outside supported bounds")
    return timeout


def _coerce_path(value: object, field: str) -> str:
    path = str(value).strip()
    if not path:
        raise ValueError(f"{field} is required")
    if len(path) > MAX_PATH_LENGTH:
        raise ValueError(f"{field} exceeds maximum length")
    if not path.startswith("/"):
        raise ValueError(f"{field} must start with /")
    if any(ch.isspace() for ch in path):
        raise ValueError(f"{field} must not contain whitespace")
    return path


def _validate_base_url(base_url: str) -> None:
    if len(base_url) > MAX_URL_LENGTH:
        raise ValueError("ODYSSEUS_BASE_URL exceeds maximum length")
    if not (base_url.startswith("http://") or base_url.startswith("https://")):
        raise ValueError("ODYSSEUS_BASE_URL must use http or https")
    if any(ch.isspace() for ch in base_url):
        raise ValueError("ODYSSEUS_BASE_URL must not contain whitespace")
