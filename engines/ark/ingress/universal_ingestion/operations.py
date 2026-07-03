"""Persistent queue, watcher, history, and event operations for living ingestion.

Contract:
- Inputs: explicit paths, queue IDs, watcher IDs, import results, and config caps.
- Outputs: append-only JSONL transition records and bounded query snapshots.
- Runtime constraint: O(max_history_records + max_folder_files) for snapshots/scans.
- Memory assumption: O(max_history_records + max_folder_files).
- Failure cases: invalid queue ID, invalid watcher path, cancelled queue item, and
  filesystem errors.
- Determinism: IDs derive from cSHAKE256 over canonical inputs.
"""

from __future__ import annotations

from dataclasses import asdict
from json import dumps, loads
from pathlib import Path

from .models import Failure, ImportHistoryRecord, IngestionConfig, QueueRecord, StatisticsRecord, WatcherRecord, to_plain
from .rid import cshake256_rid

QUEUE_DIR = "queue"
QUEUE_FILE = "import_queue.jsonl"
HISTORY_FILE = "import_history.jsonl"
WATCHERS_FILE = "watchers.jsonl"
EVENTS_FILE = "events.jsonl"
STATE_QUEUED = "Queued"
STATE_RUNNING = "Running"
STATE_COMPLETED = "Completed"
STATE_FAILED = "Failed"
STATE_CANCELLED = "Cancelled"


def canonical_bytes(value: object) -> bytes:
    return dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def append_jsonl(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(dumps(to_plain(value), sort_keys=True, ensure_ascii=False) + "\n")


def read_jsonl(path: Path, max_records: int) -> tuple[dict[str, object], ...]:
    if not path.exists():
        return ()
    records: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for _ in range(max_records):
            line = handle.readline()
            if not line:
                break
            value = loads(line)
            if isinstance(value, dict):
                records.append(value)
    return tuple(records)


class LivingIngestionStore:
    """Append-only operational store for continuous ingestion."""

    def __init__(self, root: Path, config: IngestionConfig) -> None:
        self.root = root.expanduser().resolve()
        self.config = config.validate()
        self.queue_root = self.root / QUEUE_DIR

    def queue_path(self) -> Path:
        return self.queue_root / QUEUE_FILE

    def history_path(self) -> Path:
        return self.queue_root / HISTORY_FILE

    def watchers_path(self) -> Path:
        return self.queue_root / WATCHERS_FILE

    def events_path(self) -> Path:
        return self.queue_root / EVENTS_FILE

    def enqueue(self, source: Path, substrate: str, now: str) -> QueueRecord:
        normalized = str(source.expanduser().resolve())
        queue_id = cshake256_rid("WF:ImportQueue", canonical_bytes({"source": normalized, "substrate": substrate}))
        existing = self.queue_latest().get(queue_id)
        if existing is not None and str(existing.get("state")) in {STATE_QUEUED, STATE_RUNNING, STATE_COMPLETED}:
            state = str(existing.get("state"))
            record = QueueRecord(queue_id, normalized, substrate, state, str(existing.get("created_at", now)), now, int(existing.get("attempts", 0)), str(existing.get("last_error")) if existing.get("last_error") else None)
            return record
        record = QueueRecord(queue_id, normalized, substrate, STATE_QUEUED, now, now, 0)
        append_jsonl(self.queue_path(), record)
        return record

    def transition(self, record: QueueRecord, state: str, now: str, *, error: str | None = None) -> QueueRecord:
        updated = QueueRecord(record.queue_id, record.source, record.substrate, state, record.created_at, now, record.attempts + (1 if state == STATE_RUNNING else 0), error)
        append_jsonl(self.queue_path(), updated)
        return updated

    def queue_latest(self) -> dict[str, dict[str, object]]:
        latest: dict[str, dict[str, object]] = {}
        for record in read_jsonl(self.queue_path(), self.config.max_history_records):
            latest[str(record.get("queue_id", ""))] = record
        return latest

    def queue(self) -> tuple[dict[str, object], ...]:
        return tuple(sorted(self.queue_latest().values(), key=lambda item: str(item.get("updated_at", ""))))

    def append_history(self, record: ImportHistoryRecord) -> None:
        append_jsonl(self.history_path(), record)

    def history(self, *, limit: int = 100, state: str | None = None) -> tuple[dict[str, object], ...]:
        bounded = min(limit, self.config.max_history_records)
        records = read_jsonl(self.history_path(), self.config.max_history_records)
        if state is not None:
            records = tuple(item for item in records if item.get("state") == state)
        return tuple(records[-bounded:])

    def watch(self, path: Path, now: str) -> WatcherRecord:
        normalized = str(path.expanduser().resolve())
        watcher_id = cshake256_rid("WF:Watcher", canonical_bytes({"path": normalized}))
        record = WatcherRecord(watcher_id, normalized, True, now, now)
        append_jsonl(self.watchers_path(), record)
        return record

    def unwatch(self, path: Path, now: str) -> WatcherRecord | Failure:
        normalized = str(path.expanduser().resolve())
        watcher_id = cshake256_rid("WF:Watcher", canonical_bytes({"path": normalized}))
        current = self.watchers_latest().get(watcher_id)
        if current is None:
            return Failure.build("WATCHER_NOT_FOUND", "No watcher exists for path.", {"path": normalized})
        record = WatcherRecord(watcher_id, normalized, False, str(current.get("created_at", now)), now)
        append_jsonl(self.watchers_path(), record)
        return record

    def watchers_latest(self) -> dict[str, dict[str, object]]:
        latest: dict[str, dict[str, object]] = {}
        for record in read_jsonl(self.watchers_path(), self.config.max_history_records):
            latest[str(record.get("watcher_id", ""))] = record
        return latest

    def watchers(self) -> tuple[dict[str, object], ...]:
        return tuple(sorted(self.watchers_latest().values(), key=lambda item: str(item.get("path", ""))))

    def append_event(self, event_type: str, payload: dict[str, object], now: str) -> str:
        event_id = cshake256_rid("WF:Observation", canonical_bytes({"type": event_type, "payload": payload, "timestamp": now}))
        append_jsonl(self.events_path(), {"event_id": event_id, "event_type": event_type, "timestamp": now, "payload": payload})
        return event_id

    def events(self, *, limit: int = 100) -> tuple[dict[str, object], ...]:
        return read_jsonl(self.events_path(), min(limit, self.config.max_history_records))

    def statistics(self, artifact_count: int, storage_bytes: int) -> StatisticsRecord:
        queue = self.queue()
        history = self.history(limit=self.config.max_history_records)
        return StatisticsRecord(
            queue_depth=sum(1 for item in queue if item.get("state") == STATE_QUEUED),
            active_imports=sum(1 for item in queue if item.get("state") == STATE_RUNNING),
            completed_imports=sum(1 for item in history if item.get("state") == STATE_COMPLETED),
            failed_imports=sum(1 for item in history if item.get("state") == STATE_FAILED),
            duplicate_imports=sum(1 for item in history if item.get("duplicate") is True),
            imported_bytes=sum(int(item.get("imported_bytes", 0)) for item in history),
            imported_observations=sum(int(item.get("imported_observations", 0)) for item in history),
            imported_artifacts=sum(int(item.get("imported_artifacts", 0)) for item in history),
            artifact_count=artifact_count,
            storage_bytes=storage_bytes,
        )
