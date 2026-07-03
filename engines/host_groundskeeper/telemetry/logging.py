"""Structured logging adapter boundary."""

from __future__ import annotations

from ..contracts.interfaces import LogEntry, LoggerPort, _normalize_text


class InMemoryLogSink:
    """Bounded test/log sink implementing LoggerPort.

    Inputs: LogEntry values. Outputs: immutable entry tuple. Runtime: O(1) per
    write. Memory: O(max_entries). Failure: raises ValueError if capacity is
    exhausted. Deterministic: yes.
    """

    def __init__(self, *, max_entries: int) -> None:
        if max_entries <= 0:
            raise ValueError("max_entries must be positive")
        self._max_entries = max_entries
        self._entries: tuple[LogEntry, ...] = ()

    def write(self, entry: LogEntry) -> None:
        if len(self._entries) >= self._max_entries:
            raise ValueError("log sink is full")
        self._entries = (*self._entries, entry)

    def entries(self) -> tuple[LogEntry, ...]:
        return self._entries


class StructuredLogger:
    """Structured logger with bounded context forwarding.

    Inputs: level, message, context mapping. Outputs: delegated LogEntry.
    Runtime: O(context key count), bounded by MAX_CONTEXT_KEYS. Memory: O(context
    key count). Failure: sink errors are explicit exceptions. Deterministic: yes
    when sink is deterministic.
    """

    def __init__(self, sink: LoggerPort, *, max_entries: int) -> None:
        if max_entries <= 0:
            raise ValueError("max_entries must be positive")
        self._sink = sink
        self._max_entries = max_entries
        self._written = 0

    def info(self, message: str, context: dict[str, object] | None = None) -> None:
        self._write("info", message, context or {})

    def error(self, message: str, context: dict[str, object] | None = None) -> None:
        self._write("error", message, context or {})

    def _write(self, level: str, message: str, context: dict[str, object]) -> None:
        if self._written >= self._max_entries:
            raise ValueError("logger exceeded configured maximum entries")
        entry = LogEntry(
            level=_normalize_text(level, field="level", max_length=32),
            message=_normalize_text(message, field="message", max_length=512),
            context=dict(context),
        )
        self._sink.write(entry)
        self._written += 1
