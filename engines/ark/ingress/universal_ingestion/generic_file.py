"""Generic substrate adapter for arbitrary local files.

Contract:
- Inputs: one local file and detected substrate information.
- Outputs: one observation candidate plus one first-class artifact record.
- Runtime constraint: O(file bytes), bounded by max_artifact_bytes.
- Memory assumption: O(1) plus bounded path metadata; file hashing is streaming.
- Failure cases: missing file, oversized file, unreadable file.
- Determinism: identical source bytes and detected substrate produce identical RIDs.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from json import dumps
from mimetypes import guess_type
from pathlib import Path

from .chatgpt import _hash_file_bounded
from .detection import detect_source
from .models import ArtifactRecord, Failure, IngestionConfig, ObservationRecord, ProvenanceRecord, freeze_mapping
from .rid import cshake256_rid
from .substrates.interface import SubstrateParseResult

PARSER_VERSION = "generic_file_v1"


def _canonical_bytes(value: dict[str, object]) -> bytes:
    return dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _mtime_iso(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class GenericFileAdapter:
    """Adapter for non-specialized file substrates."""

    config: IngestionConfig

    def parse(self, source: Path, *, import_id: str) -> SubstrateParseResult:
        source_path = source.expanduser().resolve()
        if not source_path.exists() or not source_path.is_file():
            raise ValueError("source file does not exist")
        digest = _hash_file_bounded(source_path, max_bytes=self.config.max_artifact_bytes)
        detection = detect_source(source_path, self.config)
        timestamp = _mtime_iso(source_path)
        media_type = guess_type(str(source_path))[0] or "application/octet-stream"
        artifact_payload = {"path": str(source_path), "sha256": digest, "size": source_path.stat().st_size}
        artifact_rid = cshake256_rid("WF:Artifact", _canonical_bytes(artifact_payload))
        observation_payload = {
            "type": "file",
            "substrate": detection.substrate,
            "adapter": detection.adapter,
            "path": str(source_path),
            "sha256": digest,
            "timestamp": timestamp,
        }
        observation_rid = cshake256_rid("WF:Observation", _canonical_bytes(observation_payload))
        provenance = ProvenanceRecord(import_id=import_id, source_uri=str(source_path), source_sha256=digest, parser="generic_file", parser_version=PARSER_VERSION, source_path=str(source_path), source_record_id=str(source_path))
        metadata = freeze_mapping({"substrate": detection.substrate, "adapter": detection.adapter, "source_kind": detection.source_kind, "mime_type": media_type, "file_name": source_path.name, "file_suffix": source_path.suffix.lower(), "record_type": "file"})
        observation = ObservationRecord(rid=observation_rid, timestamp=timestamp, actor="filesystem", source=detection.substrate, provenance=provenance, content=source_path.name, metadata=metadata, relationships=(artifact_rid,))
        artifact = ArtifactRecord(rid=artifact_rid, import_id=import_id, source_path=str(source_path), artifact_path=source_path.name, sha256=digest, size_bytes=source_path.stat().st_size, media_type=media_type, metadata=freeze_mapping({"container": "filesystem", "substrate": detection.substrate, "adapter": detection.adapter, "provenance_import_id": import_id}))
        return SubstrateParseResult(source_sha256=digest, observations=(observation,), artifacts=(artifact,), errors=())
