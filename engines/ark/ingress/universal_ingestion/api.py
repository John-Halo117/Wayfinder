"""Frontend-independent universal ingestion API.

Contract:
- Inputs: explicit paths, optional substrate selectors, query strings, and
  IngestionConfig caps.
- Outputs: typed result dataclasses and structured failures.
- Runtime constraint: ingest is O(detection + adapter parse + append storage);
  search and timeline are O(stored observations), all bounded by config.
- Memory assumption: bounded by IngestionConfig.
- Failure cases: invalid source, unsupported substrate, storage collision, invalid
  query, malformed folder entries, and filesystem errors.
- Determinism: identical imports produce identical RIDs and stored records.
"""

from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter
from json import dumps, loads
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from .chatgpt import ChatGPTZipAdapter, PARSER_VERSION as CHATGPT_PARSER_VERSION, _hash_file_bounded
from .detection import detect_source
from .generic_file import GenericFileAdapter, PARSER_VERSION as GENERIC_FILE_PARSER_VERSION
from .models import Failure, ImportHistoryRecord, ImportManifest, IngestionConfig, IngestionResult, QueueRecord, SearchResult, TimelineResult, to_plain
from .rid import cshake256_rid
from .operations import LivingIngestionStore, STATE_CANCELLED, STATE_COMPLETED, STATE_FAILED, STATE_QUEUED, STATE_RUNNING
from .storage import AppendOnlyObservationStore
from .substrates.interface import SubstrateParseResult

FOLDER_PARSER_VERSION = "folder_substrate_v1"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical_manifest_payload(source_sha256: str, parser_version: str, source_kind: str) -> bytes:
    value = {"source_sha256": source_sha256, "parser_version": parser_version, "source_kind": source_kind}
    return dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _bounded_dirs(path: Path, max_items: int) -> tuple[Path, ...]:
    if max_items <= 0 or not path.exists():
        return ()
    collected: list[Path] = []
    iterator = path.iterdir()
    for _ in range(max_items):
        try:
            candidate = next(iterator)
        except StopIteration:
            break
        if candidate.is_dir():
            collected.append(candidate)
    return tuple(sorted(collected))


def _bounded_directory_entries(path: Path, max_entries: int) -> tuple[Path, ...]:
    if max_entries <= 0:
        return ()
    entries: list[Path] = []
    iterator = path.iterdir()
    for _ in range(max_entries + 1):
        try:
            entry = next(iterator)
        except StopIteration:
            break
        entries.append(entry)
        if len(entries) > max_entries:
            raise ValueError("directory entry count exceeds maximum")
    return tuple(sorted(entries))


def _bounded_folder_files(root: Path, config: IngestionConfig) -> tuple[Path, ...]:
    if not root.exists() or not root.is_dir():
        raise ValueError("folder source does not exist")
    files: list[Path] = []
    stack: list[tuple[Path, int]] = [(root, 0)]
    max_steps = config.max_folder_files + config.max_folder_depth + 1
    for _ in range(max_steps):
        if not stack:
            break
        directory, depth = stack.pop()
        if depth > config.max_folder_depth:
            raise ValueError("folder depth exceeds maximum")
        entries = _bounded_directory_entries(directory, config.max_zip_entries)
        for entry in entries:
            if entry.is_dir():
                stack.append((entry, depth + 1))
            elif entry.is_file():
                files.append(entry)
                if len(files) > config.max_folder_files:
                    raise ValueError("folder file count exceeds maximum")
    if stack:
        raise ValueError("folder traversal exceeded bounded iteration limit")
    return tuple(sorted(files))


def _combine_digest(parts: tuple[str, ...]) -> str:
    payload = dumps(parts, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return cshake256_rid("WF:Import", payload)


class IngestionAPI:
    """Core ingestion API usable by future CLI, GUI, or service frontends."""

    def __init__(self, storage_root: Path, config: IngestionConfig | None = None) -> None:
        self._config = (config or IngestionConfig()).validate()
        self._store = AppendOnlyObservationStore(storage_root, self._config)
        self._living = LivingIngestionStore(storage_root, self._config)

    def health(self):
        return self._store.health()

    def detect(self, source: Path):
        return detect_source(source, self._config)

    def ingest(self, substrate_or_source: str | Path, source: Path | None = None) -> IngestionResult:
        """Ingest one source while preserving legacy and auto-detect APIs.

        Supported calls:
        - ingest("chatgpt", Path("export.zip"))
        - ingest("folder", Path("~/Downloads"))
        - ingest(Path("export.zip"))
        - ingest("export.zip")
        """

        if source is None:
            return self.ingest_auto(Path(substrate_or_source))
        normalized = str(substrate_or_source).strip().lower()
        if normalized == "folder":
            return self.ingest_folder(source)
        if normalized == "chatgpt":
            return self._ingest_chatgpt(source)
        detection = detect_source(source, self._config)
        if normalized in {detection.substrate, detection.adapter}:
            return self._ingest_detected(source, detection)
        return IngestionResult(status="error", import_manifest=None, observations=(), artifacts=(), failure=Failure.build("SUBSTRATE_UNSUPPORTED", "No adapter is registered for requested substrate.", {"substrate": str(substrate_or_source)}))

    def ingest_auto(self, source: Path) -> IngestionResult:
        try:
            detection = detect_source(source, self._config)
            if detection.status == "error":
                return IngestionResult(status="error", import_manifest=None, observations=(), artifacts=(), failure=Failure.build("SOURCE_DETECTION_FAILED", detection.reason, {"source": str(source)}))
            if detection.adapter == "folder":
                return self.ingest_folder(source)
            return self._ingest_detected(source, detection)
        except (OSError, ValueError) as exc:
            return IngestionResult(status="error", import_manifest=None, observations=(), artifacts=(), failure=Failure.build("INGEST_FAILED", str(exc)))

    def ingest_folder(self, folder: Path) -> IngestionResult:
        started = perf_counter()
        started_at = _now_iso()
        try:
            root = folder.expanduser().resolve()
            files = _bounded_folder_files(root, self._config)
            parsed_results: list[SubstrateParseResult] = []
            errors: list[Failure] = []
            digest_parts: list[str] = [str(root)]
            for file_path in files:
                detection = detect_source(file_path, self._config)
                if detection.status == "error":
                    errors.append(Failure.build("SOURCE_DETECTION_FAILED", detection.reason, {"source": str(file_path)}))
                    continue
                file_hash = _hash_file_bounded(file_path, max_bytes=self._config.max_artifact_bytes)
                digest_parts.append(f"{file_path.relative_to(root)}:{file_hash}:{detection.substrate}:{detection.adapter}")
            folder_digest = _combine_digest(tuple(sorted(digest_parts)))
            import_id = cshake256_rid("WF:Import", _canonical_manifest_payload(folder_digest, FOLDER_PARSER_VERSION, "folder"))
            for file_path in files:
                detection = detect_source(file_path, self._config)
                if detection.status == "error":
                    continue
                try:
                    parsed_results.append(self._parse_detected(file_path, detection, import_id=import_id))
                except (OSError, ValueError) as exc:
                    errors.append(Failure.build("FOLDER_ITEM_INGEST_FAILED", str(exc), {"source": str(file_path)}))
            observations = tuple(item for parsed in parsed_results for item in parsed.observations)
            artifacts = tuple(item for parsed in parsed_results for item in parsed.artifacts)
            all_errors = tuple(errors + [error for parsed in parsed_results for error in parsed.errors])
            manifest = ImportManifest(import_id=import_id, timestamp=_now_iso(), source=str(root), parser_version=FOLDER_PARSER_VERSION, checksums={"folder_digest": folder_digest}, imported_objects=tuple(item.rid for item in observations), statistics={"observations": len(observations), "artifacts": len(artifacts), "errors": len(all_errors), "files": len(files)}, errors=all_errors)
            failure = self._store.append_import(manifest, observations, artifacts, root)
            if failure is not None:
                result = IngestionResult(status="error", import_manifest=manifest, observations=observations, artifacts=artifacts, failure=failure)
                self._history_from_result(result, source=root, queue_id=None, started=started, started_at=started_at)
                return result
            result = IngestionResult(status="ok", import_manifest=manifest, observations=observations, artifacts=artifacts)
            self._history_from_result(result, source=root, queue_id=None, started=started, started_at=started_at)
            return result
        except (OSError, ValueError) as exc:
            result = IngestionResult(status="error", import_manifest=None, observations=(), artifacts=(), failure=Failure.build("INGEST_FAILED", str(exc)))
            self._history_from_result(result, source=folder, queue_id=None, started=started, started_at=started_at)
            return result

    def _ingest_detected(self, source: Path, detection) -> IngestionResult:
        started = perf_counter()
        started_at = _now_iso()
        if detection.adapter == "chatgpt":
            return self._ingest_chatgpt(source)
        try:
            source_path = source.expanduser().resolve()
            source_hash = _hash_file_bounded(source_path, max_bytes=self._config.max_artifact_bytes)
            import_id = cshake256_rid("WF:Import", _canonical_manifest_payload(source_hash, GENERIC_FILE_PARSER_VERSION, detection.substrate))
            parsed = self._parse_detected(source_path, detection, import_id=import_id)
            manifest = ImportManifest(import_id=import_id, timestamp=_now_iso(), source=str(source_path), parser_version=GENERIC_FILE_PARSER_VERSION, checksums={"sha256": parsed.source_sha256}, imported_objects=tuple(item.rid for item in parsed.observations), statistics={"observations": len(parsed.observations), "artifacts": len(parsed.artifacts), "errors": len(parsed.errors)}, errors=parsed.errors)
            failure = self._store.append_import(manifest, parsed.observations, parsed.artifacts, source_path)
            if failure is not None:
                result = IngestionResult(status="error", import_manifest=manifest, observations=parsed.observations, artifacts=parsed.artifacts, failure=failure)
                self._history_from_result(result, source=source, queue_id=None, started=started, started_at=started_at)
                return result
            result = IngestionResult(status="ok", import_manifest=manifest, observations=parsed.observations, artifacts=parsed.artifacts)
            self._history_from_result(result, source=source, queue_id=None, started=started, started_at=started_at)
            return result
        except (OSError, ValueError) as exc:
            result = IngestionResult(status="error", import_manifest=None, observations=(), artifacts=(), failure=Failure.build("INGEST_FAILED", str(exc)))
            self._history_from_result(result, source=source, queue_id=None, started=started, started_at=started_at)
            return result

    def _ingest_chatgpt(self, source: Path) -> IngestionResult:
        started = perf_counter()
        started_at = _now_iso()
        try:
            source_path = source.expanduser().resolve()
            if not source_path.exists() or not source_path.is_file():
                raise ValueError("source file does not exist")
            source_hash = _hash_file_bounded(source_path, max_bytes=self._config.max_artifact_bytes)
            import_id = cshake256_rid("WF:Import", _canonical_manifest_payload(source_hash, CHATGPT_PARSER_VERSION, "conversation"))
            parsed = ChatGPTZipAdapter(self._config).parse(source_path, import_id=import_id)
            manifest = ImportManifest(import_id=import_id, timestamp=_now_iso(), source=str(source_path), parser_version=CHATGPT_PARSER_VERSION, checksums={"sha256": parsed.source_sha256}, imported_objects=tuple(item.rid for item in parsed.observations), statistics={"observations": len(parsed.observations), "artifacts": len(parsed.artifacts), "errors": len(parsed.errors)}, errors=parsed.errors)
            failure = self._store.append_import(manifest, parsed.observations, parsed.artifacts, source_path)
            if failure is not None:
                result = IngestionResult(status="error", import_manifest=manifest, observations=parsed.observations, artifacts=parsed.artifacts, failure=failure)
                self._history_from_result(result, source=source, queue_id=None, started=started, started_at=started_at)
                return result
            result = IngestionResult(status="ok", import_manifest=manifest, observations=parsed.observations, artifacts=parsed.artifacts)
            self._history_from_result(result, source=source, queue_id=None, started=started, started_at=started_at)
            return result
        except (OSError, ValueError) as exc:
            result = IngestionResult(status="error", import_manifest=None, observations=(), artifacts=(), failure=Failure.build("INGEST_FAILED", str(exc)))
            self._history_from_result(result, source=source, queue_id=None, started=started, started_at=started_at)
            return result

    def _parse_detected(self, source: Path, detection, *, import_id: str) -> SubstrateParseResult:
        if detection.adapter == "chatgpt":
            parsed = ChatGPTZipAdapter(self._config).parse(source, import_id=import_id)
            return SubstrateParseResult(parsed.source_sha256, parsed.observations, parsed.artifacts, parsed.errors)
        if detection.adapter == "generic_file":
            return GenericFileAdapter(self._config).parse(source, import_id=import_id)
        raise ValueError(f"unsupported adapter: {detection.adapter}")


    def watch(self, path: Path):
        return self._living.watch(path, _now_iso())

    def unwatch(self, path: Path):
        return self._living.unwatch(path, _now_iso())

    def watchers(self):
        return self._living.watchers()

    def queue(self):
        return self._living.queue()

    def import_history(self, *, limit: int = 100, state: str | None = None):
        return self._living.history(limit=limit, state=state)

    def cancel(self, queue_id: str):
        latest = self._living.queue_latest().get(queue_id)
        if latest is None:
            return Failure.build("QUEUE_ITEM_NOT_FOUND", "No queued import exists for ID.", {"queue_id": queue_id})
        record = QueueRecord(str(latest.get("queue_id")), str(latest.get("source")), str(latest.get("substrate")), str(latest.get("state")), str(latest.get("created_at")), str(latest.get("updated_at")), int(latest.get("attempts", 0)), str(latest.get("last_error")) if latest.get("last_error") else None)
        return self._living.transition(record, STATE_CANCELLED, _now_iso(), error="cancelled by operator")

    def retry(self, import_id: str):
        history = self._living.history(limit=self._config.max_history_records)
        for item in reversed(history):
            if str(item.get("import_id")) == import_id:
                source = Path(str(item.get("source")))
                return self.enqueue(source)
        return Failure.build("IMPORT_HISTORY_NOT_FOUND", "No import history exists for ID.", {"import_id": import_id})

    def enqueue(self, source: Path, substrate: str = "auto"):
        return self._living.enqueue(source, substrate, _now_iso())

    def process_queue(self, *, limit: int | None = None) -> tuple[IngestionResult, ...]:
        queue_items = self._living.queue()
        max_items = min(limit or self._config.max_import_concurrency, self._config.max_import_concurrency, len(queue_items))
        results: list[IngestionResult] = []
        processed = 0
        for item in queue_items:
            if processed >= max_items:
                break
            if item.get("state") != STATE_QUEUED:
                continue
            record = QueueRecord(str(item.get("queue_id")), str(item.get("source")), str(item.get("substrate")), str(item.get("state")), str(item.get("created_at")), str(item.get("updated_at")), int(item.get("attempts", 0)), str(item.get("last_error")) if item.get("last_error") else None)
            running = self._living.transition(record, STATE_RUNNING, _now_iso())
            self._living.append_event("Import started", {"queue_id": running.queue_id, "source": running.source}, _now_iso())
            result = self.ingest(Path(running.source)) if running.substrate == "auto" else self.ingest(running.substrate, Path(running.source))
            state = STATE_COMPLETED if result.status == "ok" else STATE_FAILED
            error = result.failure.error_code if result.failure else None
            self._living.transition(running, state, _now_iso(), error=error)
            self._living.append_event("Import completed" if result.status == "ok" else "Import failed", {"queue_id": running.queue_id, "source": running.source, "error": error}, _now_iso())
            results.append(result)
            processed += 1
        return tuple(results)

    def scan_watchers(self, *, process: bool = True) -> tuple[QueueRecord, ...]:
        queued: list[QueueRecord] = []
        watchers = self._living.watchers()
        max_watchers = min(len(watchers), self._config.max_history_records)
        for index in range(max_watchers):
            watcher = watchers[index]
            if watcher.get("active") is not True:
                continue
            path = Path(str(watcher.get("path")))
            try:
                files = _bounded_folder_files(path, self._config)
            except (OSError, ValueError) as exc:
                self._living.append_event("Import failed", {"watcher": str(path), "error": str(exc)}, _now_iso())
                continue
            for file_path in files:
                detection = detect_source(file_path, self._config)
                if detection.status == "error":
                    self._living.append_event("Unsupported substrate" if "invalid" not in detection.reason.lower() else "Corrupt archive", {"source": str(file_path), "reason": detection.reason}, _now_iso())
                    continue
                queued.append(self._living.enqueue(file_path, "auto", _now_iso()))
                if len(queued) >= self._config.max_folder_files:
                    break
        if process:
            self.process_queue(limit=self._config.max_import_concurrency)
        return tuple(queued)

    def statistics(self):
        return self._living.statistics(artifact_count=len(self.artifacts()), storage_bytes=self._store.storage_bytes())

    def events(self, *, limit: int = 100):
        return self._living.events(limit=limit)


    def _history_from_result(self, result: IngestionResult, *, source: Path, queue_id: str | None, started: float, started_at: str) -> None:
        completed_at = _now_iso()
        duration_ms = int((perf_counter() - started) * 1000)
        manifest = result.import_manifest
        duplicate = result.failure is not None and result.failure.error_code == "IMPORT_ALREADY_EXISTS"
        imported_bytes = 0
        try:
            imported_bytes = source.stat().st_size if source.is_file() else 0
        except OSError:
            imported_bytes = 0
        record = ImportHistoryRecord(
            import_id=manifest.import_id if manifest else cshake256_rid("WF:Import", _canonical_manifest_payload(str(source), "failed", "unknown")),
            queue_id=queue_id,
            source=str(source),
            state=STATE_COMPLETED if result.status == "ok" else STATE_FAILED,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            imported_bytes=imported_bytes,
            imported_observations=len(result.observations),
            imported_artifacts=len(result.artifacts),
            duplicate=duplicate,
            error_code=result.failure.error_code if result.failure else None,
            reason=result.failure.reason if result.failure else None,
        )
        self._living.append_history(record)
        if result.failure is not None:
            event_type = "Duplicate detected" if duplicate else "Import failed"
            if result.failure.error_code == "SUBSTRATE_UNSUPPORTED":
                event_type = "Unsupported substrate"
            if result.failure.error_code == "SOURCE_DETECTION_FAILED":
                event_type = "Corrupt archive"
            self._living.append_event(event_type, {"source": str(source), "error_code": result.failure.error_code, "reason": result.failure.reason}, completed_at)
        else:
            self._living.append_event("Import completed", {"source": str(source), "import_id": record.import_id}, completed_at)

    def search(self, query: str) -> SearchResult:
        return self._store.search(query)

    def timeline(self, query: str | None = None) -> TimelineResult:
        return self._store.timeline(query)

    def observations(self, *, limit: int | None = None):
        return self._store.observations(limit=limit)

    def imports(self) -> tuple[dict[str, object], ...]:
        imports_root = self._store.root / "imports"
        if not imports_root.exists():
            return ()
        manifests: list[dict[str, object]] = []
        import_dirs = _bounded_dirs(imports_root, self._config.max_conversations)
        for import_dir in import_dirs:
            manifest_path = import_dir / "manifest.json"
            if manifest_path.exists():
                manifests.append(loads(manifest_path.read_text(encoding="utf-8")))
        return tuple(manifests)

    def provenance(self, rid: str):
        for observation in self.observations(limit=self._config.max_messages):
            if observation.rid == rid:
                return to_plain(observation.provenance)
        artifact = self.artifact_by_rid(rid)
        if isinstance(artifact, dict):
            return {"import_id": artifact.get("import_id"), "source_path": artifact.get("source_path"), "sha256": artifact.get("sha256"), "metadata": artifact.get("metadata", {})}
        return Failure.build("PROVENANCE_NOT_FOUND", "No provenance was found for RID.", {"rid": rid})

    def artifacts(self):
        return self._store._artifact_records()

    def artifact_by_rid(self, rid: str):
        return self._store.artifact_by_rid(rid)

    def artifacts_by_checksum(self, sha256: str):
        return self._store.artifacts_by_checksum(sha256)
