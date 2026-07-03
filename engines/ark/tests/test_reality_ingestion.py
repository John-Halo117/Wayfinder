import importlib.util
import json
import sys
from pathlib import Path

from engines.ark.ingress.reality_ingestion import (
    EventBusEventSink,
    InMemoryRealityStorage,
    RealityIngestionPipeline,
)
from services.identity import IdentityService


CHATGPT_ORACLE_DIR = Path(__file__).resolve().parents[1] / "ingress" / "chatgpt_oracle"
EVENT_BUS_FILE = Path(__file__).resolve().parents[3] / "services" / "event-bus" / "event_bus_service.py"


def _load_chatgpt_oracle():
    package_name = "phase3_chatgpt_oracle"
    init_spec = importlib.util.spec_from_file_location(
        package_name,
        CHATGPT_ORACLE_DIR / "__init__.py",
        submodule_search_locations=[str(CHATGPT_ORACLE_DIR)],
    )
    package = importlib.util.module_from_spec(init_spec)
    assert init_spec.loader is not None
    sys.modules[package_name] = package
    init_spec.loader.exec_module(package)
    return package


def _load_event_bus_module():
    spec = importlib.util.spec_from_file_location("phase3_event_bus_service", EVENT_BUS_FILE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["phase3_event_bus_service"] = module
    spec.loader.exec_module(module)
    return module


def _write_sample_export(root: Path) -> None:
    conversations = [
        {
            "id": "conv-1",
            "title": "Reality first",
            "create_time": 1700000000,
            "update_time": 1700000020,
            "mapping": {
                "msg-1": {
                    "id": "msg-1",
                    "parent": None,
                    "children": ["msg-2"],
                    "message": {
                        "id": "msg-1",
                        "author": {"role": "user"},
                        "create_time": 1700000001,
                        "content": {"content_type": "text", "parts": ["Preserve this."]},
                        "metadata": {},
                    },
                },
                "msg-2": {
                    "id": "msg-2",
                    "parent": "msg-1",
                    "children": [],
                    "message": {
                        "id": "msg-2",
                        "author": {"role": "assistant"},
                        "create_time": 1700000002,
                        "content": {"content_type": "text", "parts": ["Observed."]},
                        "metadata": {},
                    },
                },
            },
        }
    ]
    (root / "conversations.json").write_text(json.dumps(conversations), encoding="utf-8")


def _observation(observation_id: str, *, timestamp: str | None = "2026-01-01T00:00:00Z"):
    return {
        "observation_id": observation_id,
        "timestamp": timestamp,
        "source": "unit-test-oracle",
        "artifact_type": "Message",
        "original_location": "fixture/conversations.json#msg-1",
        "conversation_reference": "conv-1",
        "message_reference": "msg-1",
        "author": "Tester",
        "role": "user",
        "raw_content": {"content_type": "text", "parts": ["raw"]},
        "attachments": (),
        "metadata": {},
        "provenance": {
            "original_file": "conversations.json",
            "original_path": "conversations.json",
            "byte_offset": None,
            "conversation_id": "conv-1",
            "message_id": "msg-1",
            "attachment_id": None,
            "parser_name": "unit-test-oracle",
            "parser_version": "1.0.0",
            "import_timestamp": "2026-01-01T00:00:00Z",
            "hash": "hash-1",
        },
        "parsing_status": "parsed",
        "confidence": 1.0,
    }


def test_ark_ingests_chatgpt_oracle_output_without_chatgpt_coupling(tmp_path):
    oracle = _load_chatgpt_oracle()
    export = tmp_path / "export"
    export.mkdir()
    _write_sample_export(export)
    oracle_result = oracle.import_export(export)

    pipeline = RealityIngestionPipeline()
    result = pipeline.ingest(
        observations=oracle_result.observations,
        relationships=oracle_result.relationships,
        artifacts=oracle_result.artifact_inventory,
        source="chatgpt-export-oracle",
    )

    assert result.status == "ok"
    assert len(result.preserved_observations) == len(oracle_result.observations)
    assert len(result.preserved_relationships) == len(oracle_result.relationships)
    assert result.last_verified_reality.sequence == len(oracle_result.observations)
    assert RealityIngestionPipeline.__module__.startswith("engines.ark.ingress.reality_ingestion")


def test_identity_and_event_bus_integrations_are_contract_boundaries():
    event_bus_module = _load_event_bus_module()
    event_bus = event_bus_module.EventBusService(max_events=50)
    event_sink = EventBusEventSink(
        event_bus,
        envelope_builder=event_bus_module.EventBusService.build_envelope,
    )
    identity = IdentityService(
        [
            IdentityService.build_record(
                namespace="observation",
                key="canonical-1",
                identity_type="message",
                aliases=("obs-1", "msg-1", "conv-1"),
                canonical_label="Canonical message",
                confidence=1.0,
            )
        ]
    )
    pipeline = RealityIngestionPipeline(identity_service=identity, event_sink=event_sink)

    result = pipeline.ingest(observations=(_observation("obs-1"),), source="unit-test-oracle")
    replay = event_bus.replay(after_sequence=0, limit=20)

    assert result.status == "ok"
    assert result.identity_resolutions[0].canonical_rid == "observation:canonical-1"
    assert any(event.event_type == "IdentityResolved" for event in replay.events)
    assert any(event.event_type == "ObservationPreserved" for event in replay.events)


def test_validation_rejects_missing_provenance_and_broken_relationships():
    observation = dict(_observation("obs-1"))
    del observation["provenance"]
    relationship = {
        "relationship_id": "rel-1",
        "relationship_type": "message_replies_to_message",
        "source_id": "obs-1",
        "target_id": "missing-observation",
        "provenance": {
            "original_file": "conversations.json",
            "original_path": "conversations.json",
            "parser_version": "1.0.0",
            "import_timestamp": "2026-01-01T00:00:00Z",
            "hash": "hash-1",
        },
    }
    pipeline = RealityIngestionPipeline()

    result = pipeline.ingest(observations=(observation,), relationships=(relationship,))

    error_codes = {issue.error_code for issue in result.validation_report}
    assert result.status == "error"
    assert "PROVENANCE_MISSING" in error_codes
    assert "RELATIONSHIP_REFERENCE_BROKEN" in error_codes
    assert result.preserved_observations == ()
    assert result.preserved_relationships == ()


def test_storage_idempotency_lvr_and_replay_are_deterministic():
    storage = InMemoryRealityStorage()
    pipeline = RealityIngestionPipeline(storage=storage)
    observation = _observation("obs-1")

    first = pipeline.ingest(observations=(observation,), source="unit-test-oracle")
    second = pipeline.ingest(observations=(observation,), source="unit-test-oracle")
    replay = pipeline.replay(after_observation_sequence=0, after_relationship_sequence=0, limit=10)

    assert first.status == "ok"
    assert second.status == "ok"
    assert first.last_verified_reality == second.last_verified_reality
    assert len(replay.observations) == 1
    assert replay.observations[0].observation_id == "obs-1"
    assert replay.next_observation_sequence == 1


def test_relationships_can_reference_prior_preserved_reality():
    storage = InMemoryRealityStorage()
    pipeline = RealityIngestionPipeline(storage=storage)
    first_observation = _observation("obs-1")
    second_observation = _observation("obs-2")
    relationship = {
        "relationship_id": "rel-1",
        "relationship_type": "message_replies_to_message",
        "source_id": "obs-2",
        "target_id": "obs-1",
        "provenance": {
            "original_file": "conversations.json",
            "original_path": "conversations.json",
            "parser_version": "1.0.0",
            "import_timestamp": "2026-01-01T00:00:00Z",
            "hash": "hash-1",
        },
    }

    first = pipeline.ingest(observations=(first_observation,), source="unit-test-oracle")
    second = pipeline.ingest(
        observations=(second_observation,),
        relationships=(relationship,),
        source="unit-test-oracle",
    )

    assert first.status == "ok"
    assert second.status == "ok"
    assert len(second.preserved_relationships) == 1
    assert second.preserved_relationships[0].target_id == "obs-1"
