import importlib.util
import json
import sys
from pathlib import Path
from zipfile import ZipFile


PACKAGE_DIR = Path(__file__).resolve().parents[1] / "ingress" / "chatgpt_oracle"


def _load_oracle_module():
    package_name = "chatgpt_oracle"
    init_spec = importlib.util.spec_from_file_location(
        package_name,
        PACKAGE_DIR / "__init__.py",
        submodule_search_locations=[str(PACKAGE_DIR)],
    )
    package = importlib.util.module_from_spec(init_spec)
    assert init_spec.loader is not None
    sys.modules[package_name] = package
    init_spec.loader.exec_module(package)
    return package


chatgpt_oracle = _load_oracle_module()
import_export = chatgpt_oracle.import_export
write_import_outputs = chatgpt_oracle.write_import_outputs


def _write_sample_export(root: Path) -> None:
    conversations = [
        {
            "id": "conv-1",
            "title": "Reality first",
            "create_time": 1700000000,
            "update_time": 1700000020,
            "current_node": "msg-2",
            "metadata": {"project_id": "proj-1"},
            "mapping": {
                "msg-1": {
                    "id": "msg-1",
                    "parent": None,
                    "children": ["msg-2"],
                    "message": {
                        "id": "msg-1",
                        "author": {"role": "user", "name": None},
                        "create_time": 1700000001,
                        "content": {"content_type": "text", "parts": ["Preserve this."]},
                        "metadata": {
                            "attachments": [
                                {"id": "att-1", "name": "note.txt", "mime_type": "text/plain"}
                            ]
                        },
                    },
                },
                "msg-2": {
                    "id": "msg-2",
                    "parent": "msg-1",
                    "children": [],
                    "message": {
                        "id": "msg-2",
                        "author": {"role": "assistant", "name": None},
                        "create_time": 1700000002,
                        "content": {"content_type": "text", "parts": ["Observed, not summarized."]},
                        "metadata": {},
                    },
                },
            },
        }
    ]
    (root / "conversations.json").write_text(json.dumps(conversations), encoding="utf-8")
    (root / "projects.json").write_text(
        json.dumps({"projects": [{"id": "proj-1", "name": "Preservation Project"}]}),
        encoding="utf-8",
    )
    (root / "user.json").write_text(json.dumps({"email": "redacted@example.invalid"}), encoding="utf-8")
    (root / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (root / "unknown.bin").write_bytes(b"\x00\x01unknown")


def test_import_is_deterministic_and_preserves_relationships(tmp_path):
    export = tmp_path / "export"
    export.mkdir()
    _write_sample_export(export)

    first = import_export(export)
    second = import_export(export)

    first_observations = [item.observation_id for item in first.observations]
    second_observations = [item.observation_id for item in second.observations]
    first_relationships = [(item.relationship_type, item.source_id, item.target_id) for item in first.relationships]
    second_relationships = [(item.relationship_type, item.source_id, item.target_id) for item in second.relationships]

    assert first.import_report.file_count == 5
    assert first.import_report.unknown_artifact_count == 1
    assert first_observations == second_observations
    assert first_relationships == second_relationships
    assert any(item.artifact_type == "Message" for item in first.observations)
    assert any(item.relationship_type == "conversation_contains_message" for item in first.relationships)
    assert any(item.relationship_type == "message_replies_to_message" for item in first.relationships)
    assert any(item.relationship_type == "message_references_attachment" for item in first.relationships)
    assert any(item.relationship_type == "conversation_belongs_to_project" for item in first.relationships)
    assert first.observations[0].provenance.source_file == first.observations[0].provenance.original_file
    assert first.observations[0].provenance.source_hash == first.observations[0].provenance.hash


def test_unknown_and_corrupt_artifacts_are_reported_without_silent_repair(tmp_path):
    export = tmp_path / "export"
    export.mkdir()
    (export / "conversations.json").write_text("{not-json", encoding="utf-8")
    (export / "mystery.bin").write_bytes(b"mystery")

    result = import_export(export)

    error_codes = {issue.error_code for issue in result.validation_report}
    assert "JSON_PARSE_FAILED" in error_codes
    assert "UNKNOWN_ARTIFACT" in error_codes
    assert len(result.unknown_artifacts) == 1
    assert any(item.parsing_status == "corrupt" for item in result.observations)


def test_output_writer_emits_required_files_and_preserves_artifacts(tmp_path):
    export = tmp_path / "export"
    output = tmp_path / "output"
    export.mkdir()
    _write_sample_export(export)

    result = import_export(export)
    write_import_outputs(result, export, output)

    expected = {
        "export_inventory.json",
        "artifact_inventory.json",
        "parser_inventory.json",
        "observations.jsonl",
        "relationships.jsonl",
        "import_report.json",
        "validation_report.json",
        "unknown_artifacts.json",
    }
    assert expected.issubset({item.name for item in output.iterdir()})
    preserved = output / "preserved_artifacts"
    assert preserved.is_dir()
    assert len(list(preserved.iterdir())) == result.import_report.file_count


def test_zip_export_matches_directory_export(tmp_path):
    export = tmp_path / "export"
    export.mkdir()
    _write_sample_export(export)
    archive_path = tmp_path / "export.zip"
    with ZipFile(archive_path, "w") as archive:
        for item in sorted(export.rglob("*")):
            if item.is_file():
                archive.write(item, item.relative_to(export).as_posix())

    directory_result = import_export(export)
    zip_result = import_export(archive_path)

    assert [item.original_path for item in directory_result.export_inventory.files] == [
        item.original_path for item in zip_result.export_inventory.files
    ]
    assert [item.observation_id for item in directory_result.observations] == [
        item.observation_id for item in zip_result.observations
    ]
    assert [(item.relationship_type, item.source_id, item.target_id) for item in directory_result.relationships] == [
        (item.relationship_type, item.source_id, item.target_id) for item in zip_result.relationships
    ]


def test_real_export_artifact_shapes_are_classified_without_json_repair(tmp_path):
    export = tmp_path / "export"
    export.mkdir()
    (export / "conversations-000.json").write_text("[]", encoding="utf-8")
    (export / "chat.html").write_text("<html><body>export transcript</body></html>", encoding="utf-8")
    (export / "file_0000000000cc722fbd172561674a1b74.dat").write_bytes(b"attachment")

    result = import_export(export)

    by_path = {item.original_path: item.artifact_type for item in result.export_inventory.files}
    assert by_path["conversations-000.json"] == "Conversation"
    assert by_path["chat.html"] == "Document"
    assert by_path["file_0000000000cc722fbd172561674a1b74.dat"] == "Attachment"
    assert "JSON_PARSE_FAILED" not in {issue.error_code for issue in result.validation_report}


def test_numeric_millisecond_timestamps_do_not_abort_import(tmp_path):
    export = tmp_path / "export"
    export.mkdir()
    conversations = [
        {
            "id": "conv-ms",
            "create_time": 1700000000000,
            "mapping": {
                "msg-ms": {
                    "id": "msg-ms",
                    "parent": None,
                    "children": [],
                    "message": {
                        "id": "msg-ms",
                        "author": {"role": "user"},
                        "create_time": 1700000000000,
                        "content": {"content_type": "text", "parts": ["millisecond timestamp"]},
                        "metadata": {},
                    },
                }
            },
        }
    ]
    (export / "conversations-000.json").write_text(json.dumps(conversations), encoding="utf-8")

    result = import_export(export)
    timestamps = {item.timestamp for item in result.observations if item.message_reference == "msg-ms"}

    assert "2023-11-14T22:13:20Z" in timestamps
