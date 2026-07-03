"""ChatGPT ZIP adapter for universal ingestion.

Contract:
- Inputs: local ChatGPT export ZIP files containing `conversations.json`.
- Outputs: normalized conversation/message observations and preserved artifacts.
- Runtime constraint: O(zip_entries + conversations + messages + artifact_bytes),
  bounded by IngestionConfig caps.
- Memory assumption: O(max_json_bytes + max_messages), bounded by config.
- Failure cases: missing export file, invalid ZIP, missing conversations JSON,
  unsupported JSON shape, invalid message content, and resource cap exhaustion.
- Determinism: observation order follows export order plus stable mapping order.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from json import dumps, loads
from pathlib import Path
from typing import Mapping, Sequence
from zipfile import BadZipFile, ZipFile

from .models import ArtifactRecord, Failure, IngestionConfig, ObservationRecord, ProvenanceRecord, freeze_mapping
from .rid import cshake256_rid

PARSER_VERSION = "chatgpt_zip_v1"
CONVERSATIONS_JSON = "conversations.json"
MAX_CONTENT_PARTS = 1_024
MAX_MAPPING_NODES_PER_CONVERSATION = 20_000
ARTIFACT_PREFIXES = ("attachments/", "images/", "files/")
HASH_CHUNK_BYTES = 1024 * 1024


@dataclass(frozen=True)
class ParsedChatGPTExport:
    """Normalized adapter output before append-only storage."""

    source_sha256: str
    observations: tuple[ObservationRecord, ...]
    artifacts: tuple[ArtifactRecord, ...]
    errors: tuple[Failure, ...]


def _hash_file_bounded(path: Path, *, max_bytes: int) -> str:
    size = path.stat().st_size
    if size > max_bytes:
        raise ValueError("source ZIP exceeds maximum bytes")
    digest = sha256()
    max_chunks = (size // HASH_CHUNK_BYTES) + 1
    with path.open("rb") as handle:
        for _ in range(max_chunks):
            chunk = handle.read(HASH_CHUNK_BYTES)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _hash_zip_member_bounded(zip_file: ZipFile, name: str, *, size_bytes: int) -> str:
    digest = sha256()
    max_chunks = (size_bytes // HASH_CHUNK_BYTES) + 1
    remaining = size_bytes
    with zip_file.open(name) as handle:
        for _ in range(max_chunks):
            if remaining <= 0:
                break
            chunk = handle.read(min(HASH_CHUNK_BYTES, remaining))
            if not chunk:
                break
            digest.update(chunk)
            remaining -= len(chunk)
    if remaining != 0:
        raise ValueError("ZIP artifact ended before expected byte count")
    return digest.hexdigest()


def _timestamp_from_value(value: object) -> str:
    if isinstance(value, (int, float)) and value > 0:
        return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return datetime.fromtimestamp(0, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical_bytes(value: Mapping[str, object]) -> bytes:
    return dumps(dict(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _read_zip_member(zip_file: ZipFile, name: str, *, max_bytes: int) -> bytes:
    info = zip_file.getinfo(name)
    if info.file_size > max_bytes:
        raise ValueError(f"{name} exceeds maximum size")
    return zip_file.read(name)


def _extract_content(message: Mapping[str, object]) -> str:
    content = message.get("content")
    if not isinstance(content, Mapping):
        return ""
    parts = content.get("parts", ())
    if isinstance(parts, str):
        return parts
    if not isinstance(parts, Sequence):
        return ""
    if len(parts) > MAX_CONTENT_PARTS:
        raise ValueError("message content part count exceeds maximum")
    rendered: list[str] = []
    for part in parts:
        if isinstance(part, str):
            rendered.append(part)
        elif isinstance(part, Mapping):
            rendered.append(dumps(dict(part), sort_keys=True, ensure_ascii=False))
        elif part is not None:
            rendered.append(str(part))
    return "\n".join(rendered)


def _extract_actor(message: Mapping[str, object]) -> str:
    author = message.get("author")
    if isinstance(author, Mapping):
        role = author.get("role")
        if isinstance(role, str) and role.strip():
            return role.strip()
    return "unknown"


def _iter_messages(conversation: Mapping[str, object], *, max_nodes: int) -> tuple[tuple[str, Mapping[str, object]], ...]:
    mapping = conversation.get("mapping")
    if not isinstance(mapping, Mapping):
        return ()
    if len(mapping) > max_nodes:
        raise ValueError("conversation mapping exceeds maximum nodes")
    messages: list[tuple[str, Mapping[str, object]]] = []
    for node_id, node in mapping.items():
        if not isinstance(node, Mapping):
            continue
        message = node.get("message")
        if isinstance(message, Mapping):
            messages.append((str(node_id), message))
    messages.sort(key=lambda item: (_timestamp_from_value(item[1].get("create_time")), item[0]))
    return tuple(messages)


class ChatGPTZipAdapter:
    """Adapter from ChatGPT export ZIP to Wayfinder observation candidates."""

    def __init__(self, config: IngestionConfig) -> None:
        self._config = config.validate()

    def parse(self, source_zip: Path, *, import_id: str) -> ParsedChatGPTExport:
        """Parse one bounded ChatGPT ZIP export.

        Runtime: O(zip_entries + conversations + messages + artifact_bytes).
        Memory: O(max_json_bytes + max_messages).
        Failure: returns ParsedChatGPTExport with errors for recoverable record
        failures; raises ValueError for invalid source-level input.
        Deterministic: yes.
        """

        source_path = source_zip.expanduser().resolve()
        if not source_path.exists() or not source_path.is_file():
            raise ValueError("source ZIP does not exist")
        source_sha256 = _hash_file_bounded(source_path, max_bytes=self._config.max_artifact_bytes)
        try:
            with ZipFile(source_path) as zip_file:
                names = tuple(info.filename for info in zip_file.infolist())
                if len(names) > self._config.max_zip_entries:
                    raise ValueError("ZIP entry count exceeds maximum")
                if CONVERSATIONS_JSON not in names:
                    raise ValueError("conversations.json is required")
                raw = _read_zip_member(zip_file, CONVERSATIONS_JSON, max_bytes=self._config.max_json_bytes)
                conversations_value = loads(raw.decode("utf-8"))
                artifacts = self._extract_artifacts(zip_file, names, import_id=import_id, source_path=source_path)
        except BadZipFile as exc:
            raise ValueError("source is not a valid ZIP file") from exc
        if not isinstance(conversations_value, Sequence) or isinstance(conversations_value, (str, bytes)):
            raise ValueError("conversations.json must contain a list")
        if len(conversations_value) > self._config.max_conversations:
            raise ValueError("conversation count exceeds maximum")
        observations: list[ObservationRecord] = []
        errors: list[Failure] = []
        message_count = 0
        for index, conversation in enumerate(conversations_value):
            if not isinstance(conversation, Mapping):
                errors.append(Failure.build("CHATGPT_CONVERSATION_INVALID", "Conversation entry is not an object.", {"index": index}))
                continue
            conversation_observation = self._conversation_observation(conversation, index=index, import_id=import_id, source_uri=str(source_path), source_sha256=source_sha256)
            observations.append(conversation_observation)
            messages = _iter_messages(conversation, max_nodes=MAX_MAPPING_NODES_PER_CONVERSATION)
            if message_count + len(messages) > self._config.max_messages:
                raise ValueError("message count exceeds maximum")
            for node_id, message in messages:
                try:
                    observations.append(self._message_observation(conversation, message, node_id=node_id, import_id=import_id, source_uri=str(source_path), source_sha256=source_sha256, parent_rid=conversation_observation.rid))
                    message_count += 1
                except ValueError as exc:
                    errors.append(Failure.build("CHATGPT_MESSAGE_INVALID", str(exc), {"node_id": node_id}))
        return ParsedChatGPTExport(source_sha256=source_sha256, observations=tuple(observations), artifacts=artifacts, errors=tuple(errors))

    def _conversation_observation(self, conversation: Mapping[str, object], *, index: int, import_id: str, source_uri: str, source_sha256: str) -> ObservationRecord:
        conversation_id = str(conversation.get("id") or conversation.get("conversation_id") or index)
        title = str(conversation.get("title") or "Untitled conversation")
        timestamp = _timestamp_from_value(conversation.get("create_time") or conversation.get("update_time"))
        payload = {
            "type": "conversation",
            "source": "chatgpt",
            "conversation_id": conversation_id,
            "title": title,
            "timestamp": timestamp,
        }
        rid = cshake256_rid("WF:Conversation", _canonical_bytes(payload))
        provenance = ProvenanceRecord(import_id=import_id, source_uri=source_uri, source_sha256=source_sha256, parser="chatgpt_zip", parser_version=PARSER_VERSION, source_path=CONVERSATIONS_JSON, source_record_id=conversation_id)
        metadata = freeze_mapping({"substrate": "conversation", "source_system": "chatgpt", "conversation_id": conversation_id, "title": title, "record_type": "conversation"})
        return ObservationRecord(rid=rid, timestamp=timestamp, actor="system", source="chatgpt", provenance=provenance, content=title, metadata=metadata, relationships=())

    def _message_observation(self, conversation: Mapping[str, object], message: Mapping[str, object], *, node_id: str, import_id: str, source_uri: str, source_sha256: str, parent_rid: str) -> ObservationRecord:
        conversation_id = str(conversation.get("id") or conversation.get("conversation_id") or "unknown")
        timestamp = _timestamp_from_value(message.get("create_time"))
        actor = _extract_actor(message)
        content = _extract_content(message)
        message_id = str(message.get("id") or node_id)
        payload = {
            "type": "message",
            "source": "chatgpt",
            "conversation_id": conversation_id,
            "message_id": message_id,
            "actor": actor,
            "timestamp": timestamp,
            "content": content,
        }
        rid = cshake256_rid("WF:Observation", _canonical_bytes(payload))
        provenance = ProvenanceRecord(import_id=import_id, source_uri=source_uri, source_sha256=source_sha256, parser="chatgpt_zip", parser_version=PARSER_VERSION, source_path=CONVERSATIONS_JSON, source_record_id=message_id)
        content_value = message.get("content")
        content_type = content_value.get("content_type") if isinstance(content_value, Mapping) else "unknown"
        metadata = freeze_mapping({"substrate": "conversation", "source_system": "chatgpt", "conversation_id": conversation_id, "message_id": message_id, "node_id": node_id, "content_type": str(content_type), "record_type": "message"})
        return ObservationRecord(rid=rid, timestamp=timestamp, actor=actor, source="chatgpt", provenance=provenance, content=content, metadata=metadata, relationships=(parent_rid,))

    def _extract_artifacts(self, zip_file: ZipFile, names: tuple[str, ...], *, import_id: str, source_path: Path) -> tuple[ArtifactRecord, ...]:
        artifact_names = tuple(name for name in names if name.startswith(ARTIFACT_PREFIXES) and not name.endswith("/"))
        if len(artifact_names) > self._config.max_artifacts:
            raise ValueError("artifact count exceeds maximum")
        artifacts: list[ArtifactRecord] = []
        for name in artifact_names:
            info = zip_file.getinfo(name)
            if info.file_size > self._config.max_artifact_bytes:
                raise ValueError("artifact exceeds maximum size")
            digest = _hash_zip_member_bounded(zip_file, name, size_bytes=info.file_size)
            rid = cshake256_rid("WF:Artifact", _canonical_bytes({"path": name, "sha256": digest, "size": info.file_size}))
            artifacts.append(ArtifactRecord(rid=rid, import_id=import_id, source_path=name, artifact_path=name, sha256=digest, size_bytes=info.file_size, media_type="application/octet-stream", metadata=freeze_mapping({"source_system": "chatgpt", "container": "zip", "container_path": str(source_path)})))
        return tuple(artifacts)
