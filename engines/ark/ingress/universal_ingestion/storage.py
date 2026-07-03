"""Append-only local storage for universal ingestion outputs.

Contract:
- Inputs: immutable ingestion records and a local storage root.
- Outputs: JSONL records, manifests, artifact copies, and query results.
- Runtime constraint: O(record_count + stored_record_count) for writes and reads,
  bounded by IngestionConfig caps.
- Memory assumption: O(stored_record_count) for query operations, bounded by config.
- Failure cases: invalid root, existing manifest collision, malformed stored JSON,
  non-writable storage, and query cap exhaustion.
- Determinism: file paths and ordering are deterministic.
"""

from __future__ import annotations

from json import dumps, loads
from pathlib import Path
from tempfile import NamedTemporaryFile
from types import MappingProxyType
from typing import Iterable
from zipfile import ZipFile

from .models import ArtifactRecord, Failure, HealthStatus, ImportManifest, IngestionConfig, ObservationRecord, SearchResult, TimelineResult, freeze_mapping, to_plain, validate_query
from .chatgpt import PARSER_VERSION

IMPORTS_DIR = "imports"
OBSERVATIONS_DIR = "observations"
ARTIFACTS_DIR = "artifacts"
PROVENANCE_DIR = "provenance"
OBSERVATIONS_FILE = "observations.jsonl"
PROVENANCE_FILE = "provenance.jsonl"
INDEX_FILE = "search_index.jsonl"
ARTIFACT_REGISTRY_FILE = "artifacts.jsonl"
MANIFEST_FILE = "manifest.json"
OBJECTS_DIR = "objects"
COPY_CHUNK_BYTES = 1024 * 1024


def _copy_zip_member_bounded(zip_file: ZipFile, source_path: str, target_path: Path, *, size_bytes: int) -> None:
    max_chunks = (size_bytes // COPY_CHUNK_BYTES) + 1
    with zip_file.open(source_path) as source_handle:
        with NamedTemporaryFile("wb", delete=False, dir=target_path.parent) as temp_handle:
            temp_path = Path(temp_handle.name)
            remaining = size_bytes
            for _ in range(max_chunks):
                if remaining <= 0:
                    break
                chunk = source_handle.read(min(COPY_CHUNK_BYTES, remaining))
                if not chunk:
                    break
                temp_handle.write(chunk)
                remaining -= len(chunk)
    if remaining != 0:
        temp_path.unlink(missing_ok=True)
        raise ValueError("artifact copy ended before expected byte count")
    temp_path.replace(target_path)


def _copy_file_bounded(source_path: Path, target_path: Path, *, size_bytes: int) -> None:
    max_chunks = (size_bytes // COPY_CHUNK_BYTES) + 1
    with source_path.open("rb") as source_handle:
        with NamedTemporaryFile("wb", delete=False, dir=target_path.parent) as temp_handle:
            temp_path = Path(temp_handle.name)
            remaining = size_bytes
            for _ in range(max_chunks):
                if remaining <= 0:
                    break
                chunk = source_handle.read(min(COPY_CHUNK_BYTES, remaining))
                if not chunk:
                    break
                temp_handle.write(chunk)
                remaining -= len(chunk)
    if remaining != 0:
        temp_path.unlink(missing_ok=True)
        raise ValueError("file artifact copy ended before expected byte count")
    temp_path.replace(target_path)


def _json_default(value: object) -> object:
    if isinstance(value, MappingProxyType):
        return dict(value)
    return value


def _to_json_line(value: object) -> str:
    return dumps(to_plain(value), sort_keys=True, ensure_ascii=False, default=_json_default) + "\n"


def _observation_from_dict(value: dict[str, object]) -> ObservationRecord:
    from .models import ProvenanceRecord

    provenance_value = value.get("provenance")
    if not isinstance(provenance_value, dict):
        raise ValueError("stored observation provenance is invalid")
    metadata_value = value.get("metadata")
    if not isinstance(metadata_value, dict):
        raise ValueError("stored observation metadata is invalid")
    relationships_value = value.get("relationships", ())
    if not isinstance(relationships_value, list):
        raise ValueError("stored observation relationships are invalid")
    provenance = ProvenanceRecord(
        import_id=str(provenance_value.get("import_id", "")),
        source_uri=str(provenance_value.get("source_uri", "")),
        source_sha256=str(provenance_value.get("source_sha256", "")),
        parser=str(provenance_value.get("parser", "")),
        parser_version=str(provenance_value.get("parser_version", "")),
        source_path=str(provenance_value.get("source_path", "")),
        source_record_id=str(provenance_value.get("source_record_id", "")),
    )
    return ObservationRecord(
        rid=str(value.get("rid", "")),
        timestamp=str(value.get("timestamp", "")),
        actor=str(value.get("actor", "")),
        source=str(value.get("source", "")),
        provenance=provenance,
        content=str(value.get("content", "")),
        metadata=freeze_mapping(metadata_value),
        relationships=tuple(str(item) for item in relationships_value),
    )


class AppendOnlyObservationStore:
    """Local append-only store for import manifests and observations."""

    def __init__(self, root: Path, config: IngestionConfig) -> None:
        self._root = root.expanduser().resolve()
        self._config = config.validate()

    @property
    def root(self) -> Path:
        return self._root

    def initialize(self) -> None:
        """Create append-only storage directories.

        Runtime: O(1) over fixed directory set.
        Memory: O(1).
        Failure: raises OSError for filesystem errors.
        Deterministic: yes.
        """

        for relative in (IMPORTS_DIR, OBSERVATIONS_DIR, ARTIFACTS_DIR, PROVENANCE_DIR):
            (self._root / relative).mkdir(parents=True, exist_ok=True)

    def health(self) -> HealthStatus:
        self.initialize()
        probe = self._root / ".healthcheck"
        writable = False
        try:
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            writable = True
        except OSError:
            writable = False
        return HealthStatus(status="ok" if writable else "error", storage_root=str(self._root), writable=writable, parser_version=PARSER_VERSION, max_zip_entries=self._config.max_zip_entries, max_json_bytes=self._config.max_json_bytes, max_conversations=self._config.max_conversations, max_messages=self._config.max_messages, max_artifacts=self._config.max_artifacts)

    def append_import(self, manifest: ImportManifest, observations: tuple[ObservationRecord, ...], artifacts: tuple[ArtifactRecord, ...], source_zip: Path) -> Failure | None:
        """Append one import without overwriting existing records."""

        self.initialize()
        import_dir = self._root / IMPORTS_DIR / manifest.import_id.replace(":", "_")
        if import_dir.exists():
            return Failure.build("IMPORT_ALREADY_EXISTS", "Import manifest already exists.", {"import_id": manifest.import_id}, recoverable=False)
        import_dir.mkdir(parents=False)
        (import_dir / MANIFEST_FILE).write_text(dumps(to_plain(manifest), sort_keys=True, ensure_ascii=False, default=_json_default, indent=2), encoding="utf-8")
        self._append_lines(self._root / OBSERVATIONS_DIR / OBSERVATIONS_FILE, (_to_json_line(item) for item in observations))
        self._append_lines(self._root / PROVENANCE_DIR / PROVENANCE_FILE, (_to_json_line(item.provenance) for item in observations))
        self._append_lines(self._root / OBSERVATIONS_DIR / INDEX_FILE, (self._index_line(item) for item in observations))
        self._append_lines(self._root / ARTIFACTS_DIR / ARTIFACT_REGISTRY_FILE, (_to_json_line(item) for item in artifacts))
        self._preserve_artifacts(artifacts, source_path=source_zip, import_dir=import_dir)
        return None


    def storage_bytes(self) -> int:
        total = 0
        stack: list[Path] = [self._root]
        max_steps = self._config.max_folder_files + self._config.max_artifacts + self._config.max_conversations
        for _ in range(max_steps):
            if not stack:
                break
            current = stack.pop()
            if current.is_file():
                total += current.stat().st_size
            elif current.is_dir():
                iterator = current.iterdir()
                for _ in range(self._config.max_zip_entries):
                    try:
                        child = next(iterator)
                    except StopIteration:
                        break
                    stack.append(child)
        return total

    def observations(self, *, limit: int | None = None) -> tuple[ObservationRecord, ...]:
        max_items = self._config.max_messages if limit is None else min(limit, self._config.max_messages)
        path = self._root / OBSERVATIONS_DIR / OBSERVATIONS_FILE
        if not path.exists():
            return ()
        records: list[ObservationRecord] = []
        with path.open("r", encoding="utf-8") as handle:
            for _ in range(max_items):
                line = handle.readline()
                if not line:
                    break
                records.append(_observation_from_dict(loads(line)))
        return tuple(records)

    def search(self, query: str) -> SearchResult:
        try:
            normalized = validate_query(query).lower()
        except ValueError as exc:
            return SearchResult(status="error", query=query, observations=(), failure=Failure.build("SEARCH_QUERY_INVALID", str(exc)))
        matches: list[ObservationRecord] = []
        for observation in self.observations(limit=self._config.max_messages):
            haystack = " ".join((observation.content, observation.actor, observation.source, str(dict(observation.metadata)))).lower()
            if normalized in haystack:
                matches.append(observation)
                if len(matches) >= self._config.max_search_results:
                    break
        return SearchResult(status="ok", query=query, observations=tuple(matches))

    def timeline(self, query: str | None = None) -> TimelineResult:
        observations = self.observations(limit=self._config.max_messages)
        if query is not None and query.strip():
            search_result = self.search(query)
            if search_result.status == "error":
                return TimelineResult(status="error", query=query, observations=(), failure=search_result.failure)
            observations = search_result.observations
        ordered = tuple(sorted(observations, key=lambda item: (item.timestamp, item.rid)))
        return TimelineResult(status="ok", query=query, observations=ordered)


    def artifact_by_rid(self, rid: str) -> dict[str, object] | Failure:
        for artifact in self._artifact_records():
            if str(artifact.get("rid", "")) == rid:
                return artifact
        return Failure.build("ARTIFACT_NOT_FOUND", "No artifact was found for RID.", {"rid": rid})

    def artifacts_by_checksum(self, sha256: str) -> tuple[dict[str, object], ...]:
        checksum = sha256.strip().lower()
        if not checksum:
            return ()
        matches: list[dict[str, object]] = []
        for artifact in self._artifact_records():
            if str(artifact.get("sha256", "")).lower() == checksum:
                matches.append(artifact)
                if len(matches) >= self._config.max_artifacts:
                    break
        return tuple(matches)

    def _artifact_records(self) -> tuple[dict[str, object], ...]:
        path = self._root / ARTIFACTS_DIR / ARTIFACT_REGISTRY_FILE
        if not path.exists():
            return ()
        records: list[dict[str, object]] = []
        with path.open("r", encoding="utf-8") as handle:
            for _ in range(self._config.max_artifacts):
                line = handle.readline()
                if not line:
                    break
                value = loads(line)
                if isinstance(value, dict):
                    records.append(value)
        return tuple(records)

    def _append_lines(self, path: Path, lines: Iterable[str]) -> None:
        with path.open("a", encoding="utf-8") as handle:
            for line in lines:
                handle.write(line)

    def _index_line(self, observation: ObservationRecord) -> str:
        value = {
            "rid": observation.rid,
            "timestamp": observation.timestamp,
            "text": " ".join((observation.content, observation.actor, observation.source, str(dict(observation.metadata)))).lower(),
        }
        return dumps(value, sort_keys=True, ensure_ascii=False) + "\n"

    def _preserve_artifacts(self, artifacts: tuple[ArtifactRecord, ...], *, source_path: Path, import_dir: Path) -> None:
        if not artifacts:
            return
        artifact_root = import_dir / ARTIFACTS_DIR
        artifact_root.mkdir(parents=False, exist_ok=False)
        zip_file: ZipFile | None = None
        try:
            for artifact in artifacts:
                target = artifact_root / artifact.rid.replace(":", "_")
                target.mkdir(parents=False, exist_ok=False)
                object_dir = self._root / ARTIFACTS_DIR / OBJECTS_DIR / artifact.sha256
                object_dir.mkdir(parents=True, exist_ok=True)
                final_path = object_dir / Path(artifact.artifact_path).name
                if not final_path.exists():
                    if dict(artifact.metadata).get("container") == "zip":
                        if zip_file is None:
                            zip_file = ZipFile(Path(str(dict(artifact.metadata).get("container_path") or source_path)))
                        _copy_zip_member_bounded(zip_file, artifact.source_path, final_path, size_bytes=artifact.size_bytes)
                    else:
                        _copy_file_bounded(Path(artifact.source_path), final_path, size_bytes=artifact.size_bytes)
                pointer = dict(to_plain(artifact))
                pointer["content_address"] = str(final_path)
                (target / "artifact.json").write_text(dumps(pointer, sort_keys=True, ensure_ascii=False, default=_json_default, indent=2), encoding="utf-8")
        finally:
            if zip_file is not None:
                zip_file.close()
