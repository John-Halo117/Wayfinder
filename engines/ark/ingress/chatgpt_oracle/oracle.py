"""Deterministic ChatGPT export Oracle.

The Oracle preserves source artifacts, parses supported ChatGPT export files,
and emits canonical observations plus non-inferential relationships. It does
not summarize, embed, infer, search, reason, navigate, or repair source data.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from json import JSONDecodeError, dumps, loads
from mimetypes import guess_type
from pathlib import Path
from re import fullmatch
from shutil import copyfileobj
from typing import Any, Iterable, Mapping
from zipfile import BadZipFile, ZipFile

from .models import (
    ArtifactRecord,
    ExportInventory,
    ImportReport,
    ImportResult,
    ObservationRecord,
    ParserRecord,
    ProvenanceRecord,
    RelationshipRecord,
    SourceFile,
    ValidationIssue,
    to_plain,
)

PARSER_NAME = "chatgpt-export-oracle"
PARSER_VERSION = "1.0.0"
DEFAULT_IMPORT_TIMESTAMP = "1970-01-01T00:00:00Z"
TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".csv",
    ".json",
    ".html",
    ".htm",
    ".yaml",
    ".yml",
}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff"}
DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".rtf", ".odt"}


@dataclass(frozen=True)
class OracleLimits:
    """Bounded resource limits for import."""

    max_files: int = 100_000
    max_file_bytes: int = 512 * 1024 * 1024
    max_json_bytes: int = 512 * 1024 * 1024
    max_relationships_per_message: int = 10_000


@dataclass(frozen=True)
class _LoadedFile:
    original_path: str
    data: bytes


class ChatGPTExportOracle:
    """Read a ChatGPT export and emit deterministic observation streams."""

    def __init__(
        self,
        *,
        limits: OracleLimits = OracleLimits(),
        import_timestamp: str = DEFAULT_IMPORT_TIMESTAMP,
    ) -> None:
        self._limits = limits
        self._import_timestamp = _normalize_timestamp(import_timestamp)

    def import_path(self, export_path: str | Path) -> ImportResult:
        """Import a directory or zip export."""

        path = Path(export_path)
        loaded, source_kind, source_label = self._load_source(path)
        loaded = tuple(sorted(loaded, key=lambda item: item.original_path))
        export_hash = _hash_export(loaded)
        source_files = tuple(self._build_source_file(item) for item in loaded)
        export_inventory = ExportInventory(
            source=source_label,
            source_kind=source_kind,
            export_hash=export_hash,
            files=source_files,
        )

        artifacts: list[ArtifactRecord] = []
        observations: list[ObservationRecord] = []
        relationships: list[RelationshipRecord] = []
        issues: list[ValidationIssue] = []
        explicit_project_artifacts: dict[str, str] = {}

        export_artifact_id = _stable_id("artifact", "export", export_hash)
        artifacts.append(
            ArtifactRecord(
                artifact_id=export_artifact_id,
                artifact_type="Export",
                original_location=source_label,
                source_file=source_label,
                hash=export_hash,
                size_bytes=sum(item.size_bytes for item in source_files),
                parser_name=PARSER_NAME,
                parser_version=PARSER_VERSION,
                parsing_status="preserved",
                metadata={"source_kind": source_kind, "file_count": len(source_files)},
            )
        )
        export_provenance = self._provenance(
            original_file=source_label,
            original_path=source_label,
            source_hash=export_hash,
            conversation_id=None,
            message_id=None,
            attachment_id=None,
        )

        for source_file, loaded_file in zip(source_files, loaded, strict=True):
            file_artifact = self._artifact_for_file(source_file)
            artifacts.append(file_artifact)
            relationships.append(
                self._relationship(
                    "artifact_originated_from_export",
                    file_artifact.artifact_id,
                    export_artifact_id,
                    export_provenance,
                    {"source_file": source_file.original_path},
                )
            )

            if source_file.artifact_type == "Conversation":
                self._parse_conversations_json(
                    loaded_file,
                    file_artifact,
                    observations,
                    relationships,
                    artifacts,
                    issues,
                )
                continue
            if source_file.artifact_type in {"Memory", "Project", "Prompt", "Metadata", "Configuration"}:
                parsed_artifact = self._parse_json_artifact(loaded_file, file_artifact, observations, issues)
                if source_file.artifact_type == "Project" and parsed_artifact is not _JSON_FAILED:
                    self._collect_project_artifacts(parsed_artifact, file_artifact, explicit_project_artifacts)
                continue
            if source_file.artifact_type in {"Image", "Document", "Attachment"}:
                observations.append(self._file_observation(loaded_file, file_artifact, raw_content=None))
                continue
            issues.append(
                self._issue(
                    "UNKNOWN_ARTIFACT",
                    "Artifact type is not supported by a parser and was preserved only.",
                    {"path": source_file.original_path, "artifact_type": source_file.artifact_type},
                    severity="warning",
                    recoverable=True,
                )
            )

        self._validate_duplicate_observations(observations, issues)
        self._link_conversations_to_projects(observations, relationships, explicit_project_artifacts, issues)
        self._validate_relationship_targets(observations, artifacts, relationships, issues)

        artifacts_sorted = tuple(sorted(artifacts, key=lambda item: item.artifact_id))
        observations_sorted = tuple(sorted(observations, key=lambda item: item.observation_id))
        relationships_sorted = tuple(sorted(relationships, key=lambda item: item.relationship_id))
        issues_sorted = tuple(sorted(issues, key=lambda item: item.issue_id))
        unknowns = tuple(item for item in artifacts_sorted if item.artifact_type == "Unknown")
        report = ImportReport(
            source=source_label,
            source_kind=source_kind,
            export_hash=export_hash,
            import_timestamp=self._import_timestamp,
            parser_version=PARSER_VERSION,
            file_count=len(source_files),
            artifact_count=len(artifacts_sorted),
            observation_count=len(observations_sorted),
            relationship_count=len(relationships_sorted),
            validation_issue_count=len(issues_sorted),
            unknown_artifact_count=len(unknowns),
        )
        return ImportResult(
            export_inventory=export_inventory,
            artifact_inventory=artifacts_sorted,
            parser_inventory=parser_inventory(),
            observations=observations_sorted,
            relationships=relationships_sorted,
            import_report=report,
            validation_report=issues_sorted,
            unknown_artifacts=unknowns,
        )

    def _load_source(self, path: Path) -> tuple[tuple[_LoadedFile, ...], str, str]:
        if not path.exists():
            raise FileNotFoundError(f"export path does not exist: {path}")
        if path.is_dir():
            return self._load_directory(path), "directory", str(path)
        if path.is_file() and path.suffix.lower() == ".zip":
            return self._load_zip(path), "zip", str(path)
        if path.is_file():
            return (self._load_file(path, path.name),), "file", str(path)
        raise ValueError(f"unsupported export path: {path}")

    def _load_directory(self, path: Path) -> tuple[_LoadedFile, ...]:
        files = [item for item in path.rglob("*") if item.is_file()]
        if len(files) > self._limits.max_files:
            raise ValueError("export file count exceeds configured maximum")
        loaded: list[_LoadedFile] = []
        for item in sorted(files):
            loaded.append(self._load_file(item, item.relative_to(path).as_posix()))
        return tuple(loaded)

    def _load_zip(self, path: Path) -> tuple[_LoadedFile, ...]:
        try:
            with ZipFile(path) as archive:
                infos = [info for info in archive.infolist() if not info.is_dir()]
                if len(infos) > self._limits.max_files:
                    raise ValueError("export file count exceeds configured maximum")
                loaded: list[_LoadedFile] = []
                for info in sorted(infos, key=lambda item: item.filename):
                    if info.file_size > self._limits.max_file_bytes:
                        raise ValueError(f"file exceeds configured maximum: {info.filename}")
                    loaded.append(_LoadedFile(_normalize_path(info.filename), archive.read(info)))
                return tuple(loaded)
        except BadZipFile as exc:
            raise ValueError(f"corrupt zip export: {path}") from exc

    def _load_file(self, path: Path, original_path: str) -> _LoadedFile:
        size = path.stat().st_size
        if size > self._limits.max_file_bytes:
            raise ValueError(f"file exceeds configured maximum: {original_path}")
        return _LoadedFile(_normalize_path(original_path), path.read_bytes())

    def _build_source_file(self, item: _LoadedFile) -> SourceFile:
        media_type = guess_type(item.original_path)[0] or "application/octet-stream"
        return SourceFile(
            original_path=item.original_path,
            size_bytes=len(item.data),
            sha256=sha256(item.data).hexdigest(),
            media_type=media_type,
            artifact_type=classify_artifact(item.original_path, item.data),
        )

    def _artifact_for_file(self, source_file: SourceFile) -> ArtifactRecord:
        status = "parsed"
        if source_file.artifact_type in {"Image", "Document", "Attachment"}:
            status = "preserved"
        if source_file.artifact_type == "Unknown":
            status = "unsupported"
        return ArtifactRecord(
            artifact_id=_stable_id("artifact", source_file.original_path, source_file.sha256),
            artifact_type=source_file.artifact_type,
            original_location=source_file.original_path,
            source_file=source_file.original_path,
            hash=source_file.sha256,
            size_bytes=source_file.size_bytes,
            parser_name=PARSER_NAME,
            parser_version=PARSER_VERSION,
            parsing_status=status,  # type: ignore[arg-type]
            metadata={"media_type": source_file.media_type},
        )

    def _parse_json_artifact(
        self,
        loaded_file: _LoadedFile,
        artifact: ArtifactRecord,
        observations: list[ObservationRecord],
        issues: list[ValidationIssue],
    ) -> Any:
        parsed = self._load_json(loaded_file, artifact, issues)
        if parsed is _JSON_FAILED:
            observations.append(self._file_observation(loaded_file, artifact, raw_content=None, status="corrupt"))
            return _JSON_FAILED
        observations.append(self._file_observation(loaded_file, artifact, raw_content=parsed))
        return parsed

    def _collect_project_artifacts(
        self,
        parsed: Any,
        artifact: ArtifactRecord,
        explicit_project_artifacts: dict[str, str],
    ) -> None:
        for project_id in _extract_project_ids(parsed):
            explicit_project_artifacts.setdefault(project_id, artifact.artifact_id)

    def _parse_conversations_json(
        self,
        loaded_file: _LoadedFile,
        artifact: ArtifactRecord,
        observations: list[ObservationRecord],
        relationships: list[RelationshipRecord],
        artifacts: list[ArtifactRecord],
        issues: list[ValidationIssue],
    ) -> None:
        parsed = self._load_json(loaded_file, artifact, issues)
        if parsed is _JSON_FAILED:
            observations.append(self._file_observation(loaded_file, artifact, raw_content=None, status="corrupt"))
            return
        if not isinstance(parsed, list):
            issues.append(
                self._issue(
                    "UNKNOWN_CONVERSATIONS_SCHEMA",
                    "conversations.json was not a list.",
                    {"path": loaded_file.original_path, "type": type(parsed).__name__},
                    severity="error",
                    recoverable=True,
                )
            )
            observations.append(self._file_observation(loaded_file, artifact, raw_content=parsed))
            return

        file_observation = self._file_observation(loaded_file, artifact, raw_content=None)
        observations.append(file_observation)
        for index, conversation in enumerate(parsed):
            if not isinstance(conversation, Mapping):
                issues.append(
                    self._issue(
                        "UNKNOWN_CONVERSATION_SCHEMA",
                        "Conversation entry was not an object.",
                        {"path": loaded_file.original_path, "index": index},
                        severity="error",
                        recoverable=True,
                    )
                )
                continue
            self._parse_conversation(
                loaded_file,
                artifact,
                conversation,
                index,
                file_observation,
                observations,
                relationships,
                artifacts,
                issues,
            )

    def _parse_conversation(
        self,
        loaded_file: _LoadedFile,
        file_artifact: ArtifactRecord,
        conversation: Mapping[str, Any],
        index: int,
        file_observation: ObservationRecord,
        observations: list[ObservationRecord],
        relationships: list[RelationshipRecord],
        artifacts: list[ArtifactRecord],
        issues: list[ValidationIssue],
    ) -> None:
        conversation_id = _string_or_none(conversation.get("id")) or f"conversation-index-{index}"
        conversation_hash = _hash_json(conversation)
        conversation_artifact = ArtifactRecord(
            artifact_id=_stable_id("artifact", loaded_file.original_path, conversation_id, conversation_hash),
            artifact_type="Conversation",
            original_location=f"{loaded_file.original_path}#/conversations/{index}",
            source_file=loaded_file.original_path,
            hash=conversation_hash,
            size_bytes=None,
            parser_name=PARSER_NAME,
            parser_version=PARSER_VERSION,
            parsing_status="parsed",
            metadata={"title": conversation.get("title")},
        )
        artifacts.append(conversation_artifact)
        conversation_observation = self._observation(
            artifact_type="Conversation",
            original_location=conversation_artifact.original_location,
            source_file=loaded_file.original_path,
            source_hash=file_artifact.hash,
            timestamp=_timestamp_from_export(conversation.get("create_time")),
            conversation_id=conversation_id,
            message_id=None,
            attachment_id=None,
            author=None,
            role=None,
            raw_content={
                "id": conversation.get("id"),
                "title": conversation.get("title"),
                "create_time": conversation.get("create_time"),
                "update_time": conversation.get("update_time"),
                "project_id": _project_reference(conversation),
                "metadata": conversation.get("metadata", {}),
            },
            attachments=(),
            metadata={
                "current_node": conversation.get("current_node"),
                "conversation_template_id": conversation.get("conversation_template_id"),
                "project_id": _project_reference(conversation),
            },
        )
        observations.append(conversation_observation)
        relationships.append(
            self._relationship(
                "conversation_originated_from_artifact",
                conversation_observation.observation_id,
                file_observation.observation_id,
                conversation_observation.provenance,
                {"conversation_id": conversation_id},
            )
        )

        mapping = conversation.get("mapping")
        if not isinstance(mapping, Mapping):
            issues.append(
                self._issue(
                    "CONVERSATION_MAPPING_MISSING",
                    "Conversation mapping is missing or not an object.",
                    {"conversation_id": conversation_id},
                    severity="error",
                    recoverable=True,
                )
            )
            return
        message_observation_ids: dict[str, str] = {}
        parent_by_message: dict[str, str | None] = {}
        for node_key in sorted(mapping):
            node = mapping[node_key]
            if not isinstance(node, Mapping):
                issues.append(
                    self._issue(
                        "CONVERSATION_NODE_INVALID",
                        "Conversation node is not an object.",
                        {"conversation_id": conversation_id, "node": str(node_key)},
                        severity="error",
                        recoverable=True,
                    )
                )
                continue
            message = node.get("message")
            if not isinstance(message, Mapping):
                continue
            message_observation = self._parse_message(
                loaded_file,
                file_artifact,
                conversation_id,
                str(node_key),
                node,
                message,
                observations,
                relationships,
                artifacts,
                issues,
            )
            if message_observation is not None:
                message_id = message_observation.message_reference or str(node_key)
                message_observation_ids[message_id] = message_observation.observation_id
                parent_by_message[message_id] = _string_or_none(node.get("parent"))
                relationships.append(
                    self._relationship(
                        "conversation_contains_message",
                        conversation_observation.observation_id,
                        message_observation.observation_id,
                        message_observation.provenance,
                        {"conversation_id": conversation_id, "message_id": message_id},
                    )
                )
                _validate_message_timestamps(conversation, message, conversation_id, message_id, issues, self._issue)

        for message_id, parent_id in sorted(parent_by_message.items()):
            if not parent_id:
                continue
            child_observation = message_observation_ids.get(message_id)
            parent_observation = message_observation_ids.get(parent_id)
            if child_observation and parent_observation:
                child = next(item for item in observations if item.observation_id == child_observation)
                relationships.append(
                    self._relationship(
                        "message_replies_to_message",
                        child_observation,
                        parent_observation,
                        child.provenance,
                        {"conversation_id": conversation_id, "message_id": message_id, "parent_id": parent_id},
                    )
                )
            else:
                issues.append(
                    self._issue(
                        "BROKEN_MESSAGE_REFERENCE",
                        "Message parent reference does not resolve to a parsed message.",
                        {"conversation_id": conversation_id, "message_id": message_id, "parent_id": parent_id},
                        severity="warning",
                        recoverable=True,
                    )
                )

    def _parse_message(
        self,
        loaded_file: _LoadedFile,
        file_artifact: ArtifactRecord,
        conversation_id: str,
        node_key: str,
        node: Mapping[str, Any],
        message: Mapping[str, Any],
        observations: list[ObservationRecord],
        relationships: list[RelationshipRecord],
        artifacts: list[ArtifactRecord],
        issues: list[ValidationIssue],
    ) -> ObservationRecord | None:
        message_id = _string_or_none(message.get("id")) or node_key
        content = message.get("content")
        metadata = message.get("metadata")
        if metadata is None:
            metadata = {}
        if not isinstance(metadata, Mapping):
            metadata = {"raw_metadata": metadata}
        author_value = message.get("author")
        author, role = _author_and_role(author_value)
        attachments = _extract_attachments(message)
        attachment_ids: list[str] = []
        for attachment_index, attachment in enumerate(attachments):
            attachment_hash = _hash_json(attachment)
            attachment_id = (
                _string_or_none(attachment.get("id"))
                or _string_or_none(attachment.get("file_id"))
                or _string_or_none(attachment.get("name"))
                or f"{message_id}-attachment-{attachment_index}"
            )
            attachment_artifact = ArtifactRecord(
                artifact_id=_stable_id(
                    "artifact",
                    loaded_file.original_path,
                    conversation_id,
                    message_id,
                    attachment_id,
                    attachment_hash,
                ),
                artifact_type="Attachment",
                original_location=(
                    f"{loaded_file.original_path}#/conversations/{conversation_id}"
                    f"/messages/{message_id}/attachments/{attachment_index}"
                ),
                source_file=loaded_file.original_path,
                hash=attachment_hash,
                size_bytes=None,
                parser_name=PARSER_NAME,
                parser_version=PARSER_VERSION,
                parsing_status="parsed",
                metadata=dict(attachment),
            )
            artifacts.append(attachment_artifact)
            attachment_ids.append(attachment_artifact.artifact_id)

        observation = self._observation(
            artifact_type="Message",
            original_location=f"{loaded_file.original_path}#/conversations/{conversation_id}/messages/{message_id}",
            source_file=loaded_file.original_path,
            source_hash=file_artifact.hash,
            timestamp=_timestamp_from_export(message.get("create_time")),
            conversation_id=conversation_id,
            message_id=message_id,
            attachment_id=None,
            author=author,
            role=role,
            raw_content=content,
            attachments=tuple(attachment_ids),
            metadata={
                "node": node_key,
                "parent": node.get("parent"),
                "children": node.get("children", ()),
                "status": message.get("status"),
                "end_turn": message.get("end_turn"),
                "weight": message.get("weight"),
                "metadata": metadata,
                "recipient": message.get("recipient"),
            },
        )
        observations.append(observation)
        for artifact_id in attachment_ids:
            relationships.append(
                self._relationship(
                    "message_references_attachment",
                    observation.observation_id,
                    artifact_id,
                    observation.provenance,
                    {"conversation_id": conversation_id, "message_id": message_id},
                )
            )
        if len(attachment_ids) > self._limits.max_relationships_per_message:
            issues.append(
                self._issue(
                    "MESSAGE_RELATIONSHIP_LIMIT",
                    "Message exceeded relationship cap.",
                    {"conversation_id": conversation_id, "message_id": message_id},
                    severity="error",
                    recoverable=True,
                )
            )
        return observation

    def _load_json(
        self,
        loaded_file: _LoadedFile,
        artifact: ArtifactRecord,
        issues: list[ValidationIssue],
    ) -> Any:
        if len(loaded_file.data) > self._limits.max_json_bytes:
            issues.append(
                self._issue(
                    "JSON_FILE_LIMIT",
                    "JSON file exceeds configured parse maximum.",
                    {"path": loaded_file.original_path, "max_json_bytes": self._limits.max_json_bytes},
                    severity="error",
                    recoverable=True,
                )
            )
            return _JSON_FAILED
        try:
            return loads(loaded_file.data.decode("utf-8-sig"))
        except UnicodeDecodeError as exc:
            issues.append(
                self._issue(
                    "JSON_DECODE_FAILED",
                    "JSON file is not valid UTF-8.",
                    {"path": loaded_file.original_path, "error": str(exc), "artifact_id": artifact.artifact_id},
                    severity="error",
                    recoverable=True,
                )
            )
            return _JSON_FAILED
        except JSONDecodeError as exc:
            issues.append(
                self._issue(
                    "JSON_PARSE_FAILED",
                    "JSON file could not be parsed.",
                    {
                        "path": loaded_file.original_path,
                        "line": exc.lineno,
                        "column": exc.colno,
                        "artifact_id": artifact.artifact_id,
                    },
                    severity="error",
                    recoverable=True,
                )
            )
            return _JSON_FAILED

    def _file_observation(
        self,
        loaded_file: _LoadedFile,
        artifact: ArtifactRecord,
        *,
        raw_content: Any,
        status: str = "parsed",
    ) -> ObservationRecord:
        return self._observation(
            artifact_type=artifact.artifact_type,
            original_location=artifact.original_location,
            source_file=loaded_file.original_path,
            source_hash=artifact.hash,
            timestamp=None,
            conversation_id=None,
            message_id=None,
            attachment_id=None,
            author=None,
            role=None,
            raw_content=raw_content,
            attachments=(),
            metadata={"size_bytes": len(loaded_file.data), "media_type": artifact.metadata.get("media_type")},
            status=status,
        )

    def _observation(
        self,
        *,
        artifact_type: str,
        original_location: str,
        source_file: str,
        source_hash: str,
        timestamp: str | None,
        conversation_id: str | None,
        message_id: str | None,
        attachment_id: str | None,
        author: str | None,
        role: str | None,
        raw_content: Any,
        attachments: tuple[str, ...],
        metadata: dict[str, Any],
        status: str = "parsed",
    ) -> ObservationRecord:
        raw_hash = _hash_json(
            {
                "artifact_type": artifact_type,
                "original_location": original_location,
                "conversation_id": conversation_id,
                "message_id": message_id,
                "attachment_id": attachment_id,
                "raw_content": raw_content,
                "metadata": metadata,
            }
        )
        provenance = self._provenance(
            original_file=source_file,
            original_path=original_location,
            source_hash=source_hash,
            conversation_id=conversation_id,
            message_id=message_id,
            attachment_id=attachment_id,
        )
        observation_id = _stable_id("obs", artifact_type, original_location, raw_hash)
        return ObservationRecord(
            observation_id=observation_id,
            timestamp=timestamp,
            source="ChatGPT Export",
            artifact_type=artifact_type,
            original_location=original_location,
            conversation_reference=conversation_id,
            message_reference=message_id,
            author=author,
            role=role,
            raw_content=raw_content,
            attachments=attachments,
            metadata=metadata,
            provenance=provenance,
            parsing_status=status,  # type: ignore[arg-type]
            confidence=1.0 if status == "parsed" else 0.0,
        )

    def _relationship(
        self,
        relationship_type: str,
        source_id: str,
        target_id: str,
        provenance: ProvenanceRecord,
        metadata: dict[str, Any],
    ) -> RelationshipRecord:
        return RelationshipRecord(
            relationship_id=_stable_id("rel", relationship_type, source_id, target_id, metadata),
            relationship_type=relationship_type,
            source_id=source_id,
            target_id=target_id,
            provenance=provenance,
            metadata=metadata,
        )

    def _provenance(
        self,
        *,
        original_file: str,
        original_path: str,
        source_hash: str,
        conversation_id: str | None,
        message_id: str | None,
        attachment_id: str | None,
    ) -> ProvenanceRecord:
        return ProvenanceRecord(
            original_file=original_file,
            original_path=original_path,
            byte_offset=None,
            conversation_id=conversation_id,
            message_id=message_id,
            attachment_id=attachment_id,
            parser_name=PARSER_NAME,
            parser_version=PARSER_VERSION,
            import_timestamp=self._import_timestamp,
            hash=source_hash,
        )

    def _issue(
        self,
        error_code: str,
        reason: str,
        context: dict[str, Any],
        *,
        severity: str,
        recoverable: bool,
    ) -> ValidationIssue:
        return ValidationIssue(
            issue_id=_stable_id("issue", error_code, reason, context),
            severity=severity,  # type: ignore[arg-type]
            error_code=error_code,
            reason=reason,
            context=context,
            recoverable=recoverable,
        )

    def _validate_duplicate_observations(
        self,
        observations: Iterable[ObservationRecord],
        issues: list[ValidationIssue],
    ) -> None:
        seen: set[str] = set()
        for observation in observations:
            if observation.observation_id in seen:
                issues.append(
                    self._issue(
                        "DUPLICATE_OBSERVATION",
                        "Duplicate observation ID emitted.",
                        {"observation_id": observation.observation_id},
                        severity="error",
                        recoverable=False,
                    )
                )
            seen.add(observation.observation_id)

    def _validate_relationship_targets(
        self,
        observations: Iterable[ObservationRecord],
        artifacts: Iterable[ArtifactRecord],
        relationships: Iterable[RelationshipRecord],
        issues: list[ValidationIssue],
    ) -> None:
        known = {item.observation_id for item in observations}
        known.update(item.artifact_id for item in artifacts)
        for relationship in relationships:
            if relationship.source_id not in known:
                issues.append(
                    self._issue(
                        "BROKEN_RELATIONSHIP_SOURCE",
                        "Relationship source is unknown.",
                        {"relationship_id": relationship.relationship_id, "source_id": relationship.source_id},
                        severity="warning",
                        recoverable=True,
                    )
                )
            if relationship.target_id not in known:
                issues.append(
                    self._issue(
                        "BROKEN_RELATIONSHIP_TARGET",
                        "Relationship target is unknown.",
                        {"relationship_id": relationship.relationship_id, "target_id": relationship.target_id},
                        severity="warning",
                        recoverable=True,
                    )
                )

    def _link_conversations_to_projects(
        self,
        observations: Iterable[ObservationRecord],
        relationships: list[RelationshipRecord],
        explicit_project_artifacts: Mapping[str, str],
        issues: list[ValidationIssue],
    ) -> None:
        for observation in observations:
            if observation.artifact_type != "Conversation":
                continue
            project_id = _project_reference(observation.raw_content)
            if project_id is None:
                continue
            project_artifact_id = explicit_project_artifacts.get(project_id)
            if project_artifact_id is None:
                issues.append(
                    self._issue(
                        "BROKEN_PROJECT_REFERENCE",
                        "Conversation references a project that was not found as a parsed project artifact.",
                        {"conversation_id": observation.conversation_reference, "project_id": project_id},
                        severity="warning",
                        recoverable=True,
                    )
                )
                continue
            relationships.append(
                self._relationship(
                    "conversation_belongs_to_project",
                    observation.observation_id,
                    project_artifact_id,
                    observation.provenance,
                    {"conversation_id": observation.conversation_reference, "project_id": project_id},
                )
            )


class _JsonFailed:
    pass


_JSON_FAILED = _JsonFailed()


def parser_inventory() -> tuple[ParserRecord, ...]:
    """Return deterministic parser inventory."""

    return (
        ParserRecord(
            parser_name=PARSER_NAME,
            parser_version=PARSER_VERSION,
            supported_artifact_types=(
                "Export",
                "Conversation",
                "Message",
                "Attachment",
                "Image",
                "Document",
                "Prompt",
                "Project",
                "Memory",
                "Metadata",
                "Configuration",
                "Unknown",
            ),
            supported_locations=(
                "conversations.json",
                "memory*.json",
                "project*.json",
                "prompt*.json",
                "user.json",
                "settings*.json",
                "metadata*.json",
                "images/*",
                "attachments/*",
            ),
            deterministic=True,
            emits_observations=True,
        ),
    )


def classify_artifact(original_path: str, data: bytes) -> str:
    """Classify a file without dropping unknowns."""

    path = _normalize_path(original_path)
    name = Path(path).name.lower()
    suffix = Path(name).suffix.lower()
    path_lower = path.lower()
    if name == "conversations.json" or fullmatch(r"conversations-\d+\.json", name):
        return "Conversation"
    if "memory" in name and suffix == ".json":
        return "Memory"
    if "project" in name and suffix == ".json":
        return "Project"
    if "prompt" in name and suffix == ".json":
        return "Prompt"
    if name in {"user.json", "account.json"} or "metadata" in name:
        return "Metadata"
    if "setting" in name or "config" in name:
        return "Configuration"
    if suffix in IMAGE_EXTENSIONS or path_lower.startswith("images/"):
        return "Image"
    if name == "chat.html" or suffix in DOCUMENT_EXTENSIONS:
        return "Document"
    if path_lower.startswith("attachments/") or path_lower.startswith("files/"):
        return "Attachment"
    if suffix == ".dat" and (name.startswith("file_") or name.startswith("file-")):
        return "Attachment"
    if suffix in TEXT_EXTENSIONS:
        return "Metadata"
    return "Unknown"


def import_export(
    export_path: str | Path,
    *,
    limits: OracleLimits = OracleLimits(),
    import_timestamp: str = DEFAULT_IMPORT_TIMESTAMP,
) -> ImportResult:
    """Import a ChatGPT export with a one-call API."""

    return ChatGPTExportOracle(limits=limits, import_timestamp=import_timestamp).import_path(export_path)


def write_import_outputs(result: ImportResult, export_path: str | Path, output_dir: str | Path) -> None:
    """Write required import outputs and preserve source artifacts by hash."""

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    _write_json(output / "export_inventory.json", result.export_inventory)
    _write_json(output / "artifact_inventory.json", result.artifact_inventory)
    _write_json(output / "parser_inventory.json", result.parser_inventory)
    _write_jsonl(output / "observations.jsonl", result.observations)
    _write_jsonl(output / "relationships.jsonl", result.relationships)
    _write_json(output / "import_report.json", result.import_report)
    _write_json(output / "validation_report.json", result.validation_report)
    _write_json(output / "unknown_artifacts.json", result.unknown_artifacts)
    _preserve_artifacts(export_path, output / "preserved_artifacts")


def _preserve_artifacts(export_path: str | Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = Path(export_path)
    if path.is_dir():
        files = sorted(item for item in path.rglob("*") if item.is_file())
        for item in files:
            digest = sha256(item.read_bytes()).hexdigest()
            target = output_dir / digest
            if not target.exists():
                target.write_bytes(item.read_bytes())
        return
    if path.is_file() and path.suffix.lower() == ".zip":
        with ZipFile(path) as archive:
            for info in sorted((item for item in archive.infolist() if not item.is_dir()), key=lambda item: item.filename):
                with archive.open(info) as source:
                    data_hash = sha256()
                    target_temp = output_dir / f".{Path(info.filename).name}.tmp"
                    with target_temp.open("wb") as target_handle:
                        while True:
                            chunk = source.read(1024 * 1024)
                            if not chunk:
                                break
                            data_hash.update(chunk)
                            target_handle.write(chunk)
                    target = output_dir / data_hash.hexdigest()
                    if target.exists():
                        target_temp.unlink()
                    else:
                        target_temp.replace(target)
        return
    if path.is_file():
        digest = sha256(path.read_bytes()).hexdigest()
        target = output_dir / digest
        if not target.exists():
            with path.open("rb") as source, target.open("wb") as target_handle:
                copyfileobj(source, target_handle)


def _write_json(path: Path, value: Any) -> None:
    path.write_text(dumps(to_plain(value), ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, values: Iterable[Any]) -> None:
    lines = [dumps(to_plain(value), ensure_ascii=False, sort_keys=True) for value in values]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def _stable_id(prefix: str, *parts: Any) -> str:
    return f"{prefix}_{sha256(_canonical_bytes(parts)).hexdigest()[:32]}"


def _hash_json(value: Any) -> str:
    return sha256(_canonical_bytes(value)).hexdigest()


def _hash_export(files: Iterable[_LoadedFile]) -> str:
    digest = sha256()
    for item in files:
        digest.update(item.original_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256(item.data).hexdigest().encode("ascii"))
        digest.update(b"\0")
        digest.update(str(len(item.data)).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _canonical_bytes(value: Any) -> bytes:
    return dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def _normalize_path(value: str) -> str:
    return value.replace("\\", "/").lstrip("/")


def _normalize_timestamp(value: str) -> str:
    if value == DEFAULT_IMPORT_TIMESTAMP:
        return value
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _timestamp_from_export(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        numeric = float(value)
        for candidate in (numeric, numeric / 1000.0):
            try:
                return datetime.fromtimestamp(candidate, tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
            except (OverflowError, OSError, ValueError):
                continue
        return str(value)
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            return _normalize_timestamp(stripped)
        except ValueError:
            return stripped
    return str(value)


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _author_and_role(author: Any) -> tuple[str | None, str | None]:
    if not isinstance(author, Mapping):
        return None, None
    role = _string_or_none(author.get("role"))
    name = _string_or_none(author.get("name"))
    return name or role, role


def _extract_attachments(message: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    attachments: list[Mapping[str, Any]] = []
    metadata = message.get("metadata")
    if isinstance(metadata, Mapping):
        metadata_attachments = metadata.get("attachments")
        if isinstance(metadata_attachments, list):
            attachments.extend(item for item in metadata_attachments if isinstance(item, Mapping))
        aggregate = metadata.get("aggregate_result")
        if isinstance(aggregate, Mapping):
            files = aggregate.get("files")
            if isinstance(files, list):
                attachments.extend(item for item in files if isinstance(item, Mapping))
    content = message.get("content")
    if isinstance(content, Mapping):
        parts = content.get("parts")
        if isinstance(parts, list):
            for part in parts:
                if isinstance(part, Mapping) and any(key in part for key in ("asset_pointer", "file_id", "url", "name")):
                    attachments.append(part)
    return tuple(attachments)


def _extract_project_ids(value: Any) -> tuple[str, ...]:
    ids: list[str] = []
    if isinstance(value, Mapping):
        direct_id = _string_or_none(value.get("id"))
        if direct_id is not None:
            ids.append(direct_id)
        candidate = _project_reference(value)
        if candidate is not None:
            ids.append(candidate)
        for item in value.values():
            ids.extend(_extract_project_ids(item))
    elif isinstance(value, list):
        for item in value:
            ids.extend(_extract_project_ids(item))
    return tuple(dict.fromkeys(ids))


def _project_reference(value: Any) -> str | None:
    if not isinstance(value, Mapping):
        return None
    for key in ("project_id", "projectId", "project_uuid", "projectUuid"):
        project_id = _string_or_none(value.get(key))
        if project_id is not None:
            return project_id
    metadata = value.get("metadata")
    if isinstance(metadata, Mapping):
        for key in ("project_id", "projectId", "project_uuid", "projectUuid"):
            project_id = _string_or_none(metadata.get(key))
            if project_id is not None:
                return project_id
        project = metadata.get("project")
        if isinstance(project, Mapping):
            return _project_reference(project)
    project = value.get("project")
    if isinstance(project, Mapping):
        return _project_reference(project)
    return None


def _validate_message_timestamps(
    conversation: Mapping[str, Any],
    message: Mapping[str, Any],
    conversation_id: str,
    message_id: str,
    issues: list[ValidationIssue],
    issue_builder: Any,
) -> None:
    conversation_create = _numeric_time(conversation.get("create_time"))
    message_create = _numeric_time(message.get("create_time"))
    message_update = _numeric_time(message.get("update_time"))
    if conversation_create is not None and message_create is not None and message_create < conversation_create:
        issues.append(
            issue_builder(
                "TIMESTAMP_INCONSISTENCY",
                "Message create_time is earlier than conversation create_time.",
                {"conversation_id": conversation_id, "message_id": message_id},
                severity="warning",
                recoverable=True,
            )
        )
    if message_create is not None and message_update is not None and message_update < message_create:
        issues.append(
            issue_builder(
                "TIMESTAMP_INCONSISTENCY",
                "Message update_time is earlier than message create_time.",
                {"conversation_id": conversation_id, "message_id": message_id},
                severity="warning",
                recoverable=True,
            )
        )


def _numeric_time(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None
