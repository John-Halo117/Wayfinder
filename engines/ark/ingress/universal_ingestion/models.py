"""Typed schemas for universal ingestion.

Contract:
- Inputs: primitive values and bounded mappings/sequences.
- Outputs: frozen dataclasses with explicit status fields.
- Runtime constraint: validation is O(field_count + metadata_count), bounded by
  IngestionConfig caps.
- Memory assumption: O(field_count + metadata_count).
- Failure cases: invalid config, malformed records, oversized metadata, and missing
  required fields.
- Determinism: normalization preserves source values except for stable ordering of
  dictionaries where required by RID generation.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from types import MappingProxyType
from typing import Mapping

DEFAULT_MAX_ZIP_ENTRIES = 2_000
DEFAULT_MAX_JSON_BYTES = 64 * 1024 * 1024
DEFAULT_MAX_CONVERSATIONS = 100_000
DEFAULT_MAX_MESSAGES = 1_000_000
DEFAULT_MAX_ARTIFACTS = 100_000
DEFAULT_MAX_ARTIFACT_BYTES = 512 * 1024 * 1024
DEFAULT_MAX_SEARCH_RESULTS = 100
DEFAULT_MAX_FOLDER_FILES = 10_000
DEFAULT_MAX_FOLDER_DEPTH = 32
DEFAULT_MAX_ARCHIVE_DEPTH = 4
DEFAULT_MAX_IMPORT_CONCURRENCY = 1
DEFAULT_MAX_HISTORY_RECORDS = 10_000
DEFAULT_MAX_STORAGE_BYTES = 10 * 1024 * 1024 * 1024
MAX_QUERY_LENGTH = 512
MAX_RID_LENGTH = 160
MAX_ACTOR_LENGTH = 256
MAX_SOURCE_LENGTH = 512
MAX_CONTENT_LENGTH = 2_000_000
MAX_METADATA_KEYS = 128
MAX_METADATA_VALUE_LENGTH = 8_192
MAX_RELATIONSHIPS = 512


@dataclass(frozen=True)
class Failure:
    """Structured failure object for non-throwing ingestion operations."""

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
        return cls(
            status="error",
            error_code=error_code,
            reason=reason,
            context=MappingProxyType(dict(context or {})),
            recoverable=recoverable,
        )


@dataclass(frozen=True)
class IngestionConfig:
    """Resource caps for one ingestion run.

    Runtime: O(1) validation.
    Memory: O(1).
    Failure: raises ValueError when any cap is non-positive.
    Deterministic: yes.
    """

    max_zip_entries: int = DEFAULT_MAX_ZIP_ENTRIES
    max_json_bytes: int = DEFAULT_MAX_JSON_BYTES
    max_conversations: int = DEFAULT_MAX_CONVERSATIONS
    max_messages: int = DEFAULT_MAX_MESSAGES
    max_artifacts: int = DEFAULT_MAX_ARTIFACTS
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES
    max_search_results: int = DEFAULT_MAX_SEARCH_RESULTS
    max_folder_files: int = DEFAULT_MAX_FOLDER_FILES
    max_folder_depth: int = DEFAULT_MAX_FOLDER_DEPTH
    max_archive_depth: int = DEFAULT_MAX_ARCHIVE_DEPTH
    max_import_concurrency: int = DEFAULT_MAX_IMPORT_CONCURRENCY
    max_history_records: int = DEFAULT_MAX_HISTORY_RECORDS
    max_storage_bytes: int = DEFAULT_MAX_STORAGE_BYTES
    ignored_extensions: tuple[str, ...] = ()
    ignored_folders: tuple[str, ...] = ()

    def validate(self) -> "IngestionConfig":
        for field_name, value in self.__dict__.items():
            if isinstance(value, int) and value <= 0:
                raise ValueError(f"{field_name} must be positive")
            if field_name in {"ignored_extensions", "ignored_folders"} and not isinstance(value, tuple):
                raise ValueError(f"{field_name} must be a tuple")
        return self


@dataclass(frozen=True)
class SubstrateDetection:
    """Detected substrate and adapter for a source.

    Runtime: O(1) for extension checks, O(zip entry cap) for archive probing.
    Memory: O(zip entry cap).
    Failure: source-level detection failures are represented as unknown results.
    Deterministic: yes.
    """

    status: str
    substrate: str
    adapter: str
    source_kind: str
    confidence: float
    reason: str


@dataclass(frozen=True)
class SubstrateObject:
    """Canonical substrate object passed into the universal pipeline.

    Runtime: construction is O(metadata keys), bounded by MAX_METADATA_KEYS.
    Memory: O(content + metadata), bounded by adapter/config caps.
    Failure: adapter construction raises explicit validation errors.
    Deterministic: yes.
    """

    substrate: str
    adapter: str
    object_id: str
    timestamp: str
    actor: str
    source: str
    content: str
    metadata: Mapping[str, object]
    relationships: tuple[str, ...]


@dataclass(frozen=True)
class ProvenanceRecord:
    """Source and custody trace for an import-derived record."""

    import_id: str
    source_uri: str
    source_sha256: str
    parser: str
    parser_version: str
    source_path: str
    source_record_id: str


@dataclass(frozen=True)
class ObservationRecord:
    """Canonical Wayfinder observation candidate produced by ingestion."""

    rid: str
    timestamp: str
    actor: str
    source: str
    provenance: ProvenanceRecord
    content: str
    metadata: Mapping[str, object]
    relationships: tuple[str, ...]


@dataclass(frozen=True)
class ArtifactRecord:
    """Preserved binary artifact reference extracted from an import."""

    rid: str
    import_id: str
    source_path: str
    artifact_path: str
    sha256: str
    size_bytes: int
    media_type: str
    metadata: Mapping[str, object]


@dataclass(frozen=True)
class ImportManifest:
    """Append-only manifest for one ingestion run."""

    import_id: str
    timestamp: str
    source: str
    parser_version: str
    checksums: Mapping[str, str]
    imported_objects: tuple[str, ...]
    statistics: Mapping[str, int]
    errors: tuple[Failure, ...]


@dataclass(frozen=True)
class IngestionResult:
    """Structured result for ingest operations."""

    status: str
    import_manifest: ImportManifest | None
    observations: tuple[ObservationRecord, ...]
    artifacts: tuple[ArtifactRecord, ...]
    failure: Failure | None = None


@dataclass(frozen=True)
class SearchResult:
    """Search result over stored observations."""

    status: str
    query: str
    observations: tuple[ObservationRecord, ...]
    failure: Failure | None = None


@dataclass(frozen=True)
class TimelineResult:
    """Timeline result over stored observations."""

    status: str
    query: str | None
    observations: tuple[ObservationRecord, ...]
    failure: Failure | None = None


@dataclass(frozen=True)
class QueueRecord:
    """Persistent import queue transition record."""

    queue_id: str
    source: str
    substrate: str
    state: str
    created_at: str
    updated_at: str
    attempts: int
    last_error: str | None = None


@dataclass(frozen=True)
class ImportHistoryRecord:
    """Completed import history snapshot."""

    import_id: str
    queue_id: str | None
    source: str
    state: str
    started_at: str
    completed_at: str
    duration_ms: int
    imported_bytes: int
    imported_observations: int
    imported_artifacts: int
    duplicate: bool
    error_code: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class WatcherRecord:
    """Persistent folder watcher record."""

    watcher_id: str
    path: str
    active: bool
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class StatisticsRecord:
    """Operational ingestion statistics."""

    queue_depth: int
    active_imports: int
    completed_imports: int
    failed_imports: int
    duplicate_imports: int
    imported_bytes: int
    imported_observations: int
    imported_artifacts: int
    artifact_count: int
    storage_bytes: int


@dataclass(frozen=True)
class HealthStatus:
    """Bounded health signal for the universal ingestion module."""

    status: str
    storage_root: str
    writable: bool
    parser_version: str
    max_zip_entries: int
    max_json_bytes: int
    max_conversations: int
    max_messages: int
    max_artifacts: int


def freeze_mapping(values: Mapping[str, object]) -> Mapping[str, object]:
    """Return a shallow immutable mapping after bounded validation.

    Runtime: O(metadata_count), capped at MAX_METADATA_KEYS.
    Memory: O(metadata_count).
    Failure: raises ValueError for oversized keys or values.
    Deterministic: preserves insertion order supplied by caller.
    """

    if len(values) > MAX_METADATA_KEYS:
        raise ValueError("metadata key count exceeds maximum")
    normalized: dict[str, object] = {}
    for key, value in values.items():
        key_text = str(key).strip()
        if not key_text:
            raise ValueError("metadata key is required")
        if len(str(value)) > MAX_METADATA_VALUE_LENGTH:
            raise ValueError("metadata value exceeds maximum length")
        normalized[key_text] = value
    return MappingProxyType(normalized)


def validate_query(query: str) -> str:
    """Normalize a user query for search or timeline filtering."""

    normalized = query.strip()
    if not normalized:
        raise ValueError("query is required")
    if len(normalized) > MAX_QUERY_LENGTH:
        raise ValueError("query exceeds maximum length")
    return normalized

def to_plain(value: object) -> object:
    """Convert ingestion dataclasses to JSON-safe immutable snapshots.

    Runtime: O(total field count + nested item count), bounded by config caps.
    Memory: O(total field count + nested item count).
    Failure: no expected failures for supported schema values.
    Deterministic: preserves tuple/list order and mapping key/value content.
    """

    if is_dataclass(value):
        return {field.name: to_plain(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Mapping):
        return {str(key): to_plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [to_plain(item) for item in value]
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    return value
