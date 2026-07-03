from __future__ import annotations

from json import dumps
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from engines.ark.ingress.universal_ingestion import IngestionAPI, IngestionConfig, cshake256_rid


def _write_chatgpt_export(path: Path) -> None:
    conversations = [
        {
            "id": "conv-1",
            "title": "Living Reality Map",
            "create_time": 1,
            "mapping": {
                "node-user": {
                    "message": {
                        "id": "msg-1",
                        "author": {"role": "user"},
                        "create_time": 2,
                        "content": {"content_type": "text", "parts": ["Ambient Certainty"]},
                    }
                },
                "node-assistant": {
                    "message": {
                        "id": "msg-2",
                        "author": {"role": "assistant"},
                        "create_time": 3,
                        "content": {"content_type": "text", "parts": ["Preserve reality exactly once."]},
                    }
                },
            },
        }
    ]
    with ZipFile(path, "w", ZIP_DEFLATED) as zip_file:
        zip_file.writestr("conversations.json", dumps(conversations))
        zip_file.writestr("attachments/example.txt", "artifact bytes")


def test_cshake256_rid_is_deterministic_and_domain_separated():
    left = cshake256_rid("WF:Observation", b"payload")
    right = cshake256_rid("WF:Observation", b"payload")
    other = cshake256_rid("WF:Artifact", b"payload")

    assert left == right
    assert left != other
    assert left.startswith("rid:WF:Observation:")


def test_chatgpt_ingest_generates_observations_artifacts_search_and_timeline(tmp_path):
    export = tmp_path / "export.zip"
    storage = tmp_path / "ARK"
    _write_chatgpt_export(export)
    api = IngestionAPI(storage, IngestionConfig(max_conversations=10, max_messages=10, max_artifacts=10))

    result = api.ingest("chatgpt", export)

    assert result.status == "ok"
    assert result.import_manifest is not None
    assert result.import_manifest.statistics["observations"] == 3
    assert len(result.artifacts) == 1
    assert (storage / "imports").exists()
    assert (storage / "observations" / "observations.jsonl").exists()

    search = api.search("Ambient Certainty")
    assert search.status == "ok"
    assert len(search.observations) == 1
    assert search.observations[0].actor == "user"

    timeline = api.timeline("Living Reality Map")
    assert timeline.status == "ok"
    assert len(timeline.observations) == 1
    assert timeline.observations[0].metadata["record_type"] == "conversation"

    imports = api.imports()
    assert len(imports) == 1
    assert imports[0]["statistics"]["artifacts"] == 1


def test_ingest_rejects_duplicate_import_without_overwrite(tmp_path):
    export = tmp_path / "export.zip"
    storage = tmp_path / "ARK"
    _write_chatgpt_export(export)
    api = IngestionAPI(storage, IngestionConfig(max_conversations=10, max_messages=10, max_artifacts=10))

    first = api.ingest("chatgpt", export)
    second = api.ingest("chatgpt", export)

    assert first.status == "ok"
    assert second.status == "error"
    assert second.failure is not None
    assert second.failure.error_code == "IMPORT_ALREADY_EXISTS"


def test_ingest_enforces_message_cap(tmp_path):
    export = tmp_path / "export.zip"
    _write_chatgpt_export(export)
    api = IngestionAPI(tmp_path / "ARK", IngestionConfig(max_conversations=10, max_messages=1, max_artifacts=10))

    result = api.ingest("chatgpt", export)

    assert result.status == "error"
    assert result.failure is not None
    assert result.failure.error_code == "INGEST_FAILED"


def test_unsupported_substrate_returns_structured_failure(tmp_path):
    api = IngestionAPI(tmp_path / "ARK")

    result = api.ingest("claude", tmp_path / "missing.zip")

    assert result.status == "error"
    assert result.failure is not None
    assert result.failure.error_code == "SUBSTRATE_UNSUPPORTED"

def test_detects_chatgpt_zip_geometry_document_and_unknown_file(tmp_path):
    export = tmp_path / "export.zip"
    _write_chatgpt_export(export)
    stl = tmp_path / "house.stl"
    stl.write_text("solid house", encoding="utf-8")
    pdf = tmp_path / "notes.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    unknown = tmp_path / "raw.bin"
    unknown.write_bytes(b"raw")
    api = IngestionAPI(tmp_path / "ARK")

    assert api.detect(export).adapter == "chatgpt"
    assert api.detect(stl).substrate == "geometry"
    assert api.detect(pdf).substrate == "document"
    assert api.detect(unknown).substrate == "filesystem"


def test_auto_ingest_chatgpt_zip_preserves_legacy_behavior(tmp_path):
    export = tmp_path / "export.zip"
    _write_chatgpt_export(export)
    api = IngestionAPI(tmp_path / "ARK", IngestionConfig(max_conversations=10, max_messages=10, max_artifacts=10))

    result = api.ingest(export)

    assert result.status == "ok"
    assert result.import_manifest is not None
    assert result.import_manifest.statistics["observations"] == 3


def test_folder_ingestion_recurses_and_searches_across_substrates(tmp_path):
    downloads = tmp_path / "Downloads"
    nested = downloads / "nested"
    nested.mkdir(parents=True)
    (downloads / "Guest House.stl").write_text("solid guest_house", encoding="utf-8")
    (nested / "notes.pdf").write_bytes(b"%PDF-1.4 guest house")
    export = nested / "export.zip"
    _write_chatgpt_export(export)
    api = IngestionAPI(tmp_path / "ARK", IngestionConfig(max_conversations=10, max_messages=20, max_artifacts=20, max_folder_files=10, max_folder_depth=4))

    result = api.ingest("folder", downloads)

    assert result.status == "ok"
    assert result.import_manifest is not None
    assert result.import_manifest.statistics["files"] == 3
    assert result.import_manifest.statistics["artifacts"] >= 3

    search = api.search("Guest House")
    assert search.status == "ok"
    assert any(item.metadata["substrate"] == "geometry" for item in search.observations)

    timeline = api.timeline()
    assert timeline.status == "ok"
    assert len(timeline.observations) >= 5


def test_artifact_registry_lookup_by_rid_and_checksum(tmp_path):
    artifact_file = tmp_path / "house.sh3d"
    artifact_file.write_bytes(b"sweet home 3d")
    api = IngestionAPI(tmp_path / "ARK", IngestionConfig(max_artifacts=10))

    result = api.ingest(artifact_file)

    assert result.status == "ok"
    artifact = result.artifacts[0]
    by_rid = api.artifact_by_rid(artifact.rid)
    by_checksum = api.artifacts_by_checksum(artifact.sha256)

    assert isinstance(by_rid, dict)
    assert by_rid["rid"] == artifact.rid
    assert len(by_checksum) == 1
    assert by_checksum[0]["sha256"] == artifact.sha256


def test_deterministic_import_identity_survives_reimport_from_copy(tmp_path):
    left = tmp_path / "left.pdf"
    right = tmp_path / "right.pdf"
    left.write_bytes(b"same bytes")
    right.write_bytes(b"same bytes")
    api = IngestionAPI(tmp_path / "ARK")

    first = api.ingest(left)
    second = api.ingest(right)

    assert first.status == "ok"
    assert second.status == "error"
    assert second.failure is not None
    assert second.failure.error_code == "IMPORT_ALREADY_EXISTS"


def test_malformed_zip_returns_detection_failure(tmp_path):
    bad_zip = tmp_path / "bad.zip"
    bad_zip.write_bytes(b"not a zip")
    api = IngestionAPI(tmp_path / "ARK")

    result = api.ingest(bad_zip)

    assert result.status == "error"
    assert result.failure is not None
    assert result.failure.error_code == "SOURCE_DETECTION_FAILED"
