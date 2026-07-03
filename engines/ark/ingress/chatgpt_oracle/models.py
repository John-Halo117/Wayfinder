"""Data contracts for the deterministic ChatGPT export Oracle.

These dataclasses are implementation-local representations of canonical
observation, provenance, and relationship streams. They intentionally avoid
summary, embedding, search, reasoning, or navigation fields.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

ParserStatus = Literal["parsed", "unsupported", "corrupt", "preserved"]
ValidationSeverity = Literal["info", "warning", "error"]


@dataclass(frozen=True)
class SourceFile:
    """Discovered export file with deterministic integrity metadata."""

    original_path: str
    size_bytes: int
    sha256: str
    media_type: str
    artifact_type: str


@dataclass(frozen=True)
class ExportInventory:
    """Complete export file inventory."""

    source: str
    source_kind: str
    export_hash: str
    files: tuple[SourceFile, ...]


@dataclass(frozen=True)
class ArtifactRecord:
    """Classified artifact record for every discovered file or nested artifact."""

    artifact_id: str
    artifact_type: str
    original_location: str
    source_file: str
    hash: str
    size_bytes: int | None
    parser_name: str
    parser_version: str
    parsing_status: ParserStatus
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProvenanceRecord:
    """Traceability fields attached to each observation."""

    original_file: str
    original_path: str
    byte_offset: int | None
    conversation_id: str | None
    message_id: str | None
    attachment_id: str | None
    parser_name: str
    parser_version: str
    import_timestamp: str
    hash: str


@dataclass(frozen=True)
class ObservationRecord:
    """Canonical observation emitted by the Oracle."""

    observation_id: str
    timestamp: str | None
    source: str
    artifact_type: str
    original_location: str
    conversation_reference: str | None
    message_reference: str | None
    author: str | None
    role: str | None
    raw_content: Any
    attachments: tuple[str, ...]
    metadata: dict[str, Any]
    provenance: ProvenanceRecord
    parsing_status: ParserStatus
    confidence: float


@dataclass(frozen=True)
class RelationshipRecord:
    """Non-inferential relationship preserved from export structure."""

    relationship_id: str
    relationship_type: str
    source_id: str
    target_id: str
    provenance: ProvenanceRecord
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ParserRecord:
    """Parser registration and responsibility inventory."""

    parser_name: str
    parser_version: str
    supported_artifact_types: tuple[str, ...]
    supported_locations: tuple[str, ...]
    deterministic: bool
    emits_observations: bool


@dataclass(frozen=True)
class ValidationIssue:
    """Structured import validation issue."""

    issue_id: str
    severity: ValidationSeverity
    error_code: str
    reason: str
    context: dict[str, Any]
    recoverable: bool


@dataclass(frozen=True)
class ImportReport:
    """Deterministic import summary."""

    source: str
    source_kind: str
    export_hash: str
    import_timestamp: str
    parser_version: str
    file_count: int
    artifact_count: int
    observation_count: int
    relationship_count: int
    validation_issue_count: int
    unknown_artifact_count: int


@dataclass(frozen=True)
class ImportResult:
    """Complete Oracle output streams."""

    export_inventory: ExportInventory
    artifact_inventory: tuple[ArtifactRecord, ...]
    parser_inventory: tuple[ParserRecord, ...]
    observations: tuple[ObservationRecord, ...]
    relationships: tuple[RelationshipRecord, ...]
    import_report: ImportReport
    validation_report: tuple[ValidationIssue, ...]
    unknown_artifacts: tuple[ArtifactRecord, ...]


def to_plain(value: Any) -> Any:
    """Convert nested dataclasses and tuples into JSON-ready values."""

    if hasattr(value, "__dataclass_fields__"):
        return to_plain(asdict(value))
    if isinstance(value, tuple):
        return [to_plain(item) for item in value]
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    if isinstance(value, dict):
        return {str(key): to_plain(item) for key, item in value.items()}
    return value
