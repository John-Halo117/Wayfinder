from __future__ import annotations

import json
from pathlib import Path

from tooling.export_mining.mine_wayfinder_export import (
    MiningLimits,
    WayfinderExportMiner,
    write_knowledge_base,
)
from tooling.export_mining.compile_knowledge import compile_knowledge_base


def test_export_miner_reconstructs_order_and_deduplicates(tmp_path: Path) -> None:
    shard = tmp_path / "conversations-000.json"
    shard.write_text(
        json.dumps(
            [
                {
                    "id": "conv-1",
                    "conversation_id": "conv-1",
                    "title": "Architecture",
                    "mapping": {
                        "root": {"id": "root", "parent": None, "message": None},
                        "b": {
                            "id": "b",
                            "parent": "a",
                            "message": {
                                "id": "msg-b",
                                "create_time": 2,
                                "author": {"role": "assistant"},
                                "content": {
                                    "parts": [
                                        "Wayfinder must preserve provenance for every Observation.",
                                    ]
                                },
                            },
                        },
                        "a": {
                            "id": "a",
                            "parent": "root",
                            "message": {
                                "id": "msg-a",
                                "create_time": 1,
                                "author": {"role": "user"},
                                "content": {
                                    "parts": [
                                        "Wayfinder must preserve provenance for every Observation.",
                                    ]
                                },
                            },
                        },
                    },
                }
            ]
        ),
        encoding="utf-8",
    )

    result = WayfinderExportMiner(limits=MiningLimits(max_files=4)).mine_paths((shard,))

    matching = [
        fact
        for fact in result.facts
        if fact.category == "requirement" and "preserve provenance" in fact.normalized_statement
    ]
    assert len(matching) == 1
    assert [item.message_id for item in matching[0].evidence] == ["msg-a", "msg-b"]
    assert result.conversation_count == 1
    assert result.message_count == 2


def test_export_miner_writes_deterministic_knowledge_outputs(tmp_path: Path) -> None:
    shard = tmp_path / "conversations-000.json"
    shard.write_text(
        json.dumps(
            [
                {
                    "id": "conv-1",
                    "conversation_id": "conv-1",
                    "title": "Ontology",
                    "mapping": {
                        "root": {"id": "root", "parent": None, "message": None},
                        "msg": {
                            "id": "msg",
                            "parent": "root",
                            "message": {
                                "id": "msg-1",
                                "create_time": 1,
                                "author": {"role": "assistant"},
                                "content": {
                                    "parts": [
                                        "Oracle is the canonical term for an observation source in Wayfinder.",
                                    ]
                                },
                            },
                        },
                    },
                }
            ]
        ),
        encoding="utf-8",
    )
    output = tmp_path / "Knowledge"

    result = WayfinderExportMiner().mine_paths((shard,))
    write_knowledge_base(result, output)

    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    sources = json.loads((output / "Graph" / "sources.json").read_text(encoding="utf-8"))
    facts_index = json.loads((output / "Graph" / "facts" / "index.json").read_text(encoding="utf-8"))
    facts = json.loads((output / "Graph" / facts_index["chunks"][0]["path"]).read_text(encoding="utf-8"))
    assert manifest["privacy"]["raw_export_copied"] is False
    assert "path" not in manifest["source_files"][0]
    assert "path" not in sources[0]
    assert facts
    assert (output / "Glossary" / "README.md").exists()


def test_export_miner_accepts_path_manifest(tmp_path: Path) -> None:
    shard = tmp_path / "conversations-000.json"
    shard.write_text("[]", encoding="utf-8")
    manifest = tmp_path / "inputs.txt"
    manifest.write_text(f"# source list\n{shard}\n", encoding="utf-8")
    output = tmp_path / "Knowledge"

    from tooling.export_mining.mine_wayfinder_export import main

    assert main(["--input-manifest", str(manifest), "--output", str(output)]) == 0
    generated = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert generated["source_files"][0]["name"] == "conversations-000.json"


def test_export_miner_redacts_local_paths(tmp_path: Path) -> None:
    shard = tmp_path / "conversations-000.json"
    shard.write_text(
        json.dumps(
            [
                {
                    "id": "conv-1",
                    "conversation_id": "conv-1",
                    "title": "Wayfinder Repository",
                    "mapping": {
                        "root": {"id": "root", "parent": None, "message": None},
                        "msg": {
                            "id": "msg",
                            "parent": "root",
                            "message": {
                                "id": "msg-1",
                                "create_time": 1,
                                "author": {"role": "assistant"},
                                "content": {
                                    "parts": [
                                        "Wayfinder decision: use [docs](%USERPROFILE%/OneDrive/Documents/Wayfinder/docs/example.md) and never expose %USERPROFILE%/Desktop/private.txt.",
                                    ]
                                },
                            },
                        },
                    },
                }
            ]
        ),
        encoding="utf-8",
    )

    result = WayfinderExportMiner().mine_paths((shard,))

    assert result.facts
    statements = "\n".join(fact.statement for fact in result.facts)
    assert "C:/Users" not in statements
    assert "docs/example.md" in statements
    assert "[local-path]" in statements


def test_knowledge_compiler_builds_graph_search_and_reports(tmp_path: Path) -> None:
    shard = tmp_path / "conversations-000.json"
    shard.write_text(
        json.dumps(
            [
                {
                    "id": "conv-1",
                    "conversation_id": "conv-1",
                    "title": "Wayfinder Pipeline",
                    "mapping": {
                        "root": {"id": "root", "parent": None, "message": None},
                        "msg": {
                            "id": "msg",
                            "parent": "root",
                            "message": {
                                "id": "msg-1",
                                "create_time": 1,
                                "author": {"role": "assistant"},
                                "content": {
                                    "parts": [
                                        "Wayfinder must preserve provenance for every Pipeline requirement.",
                                    ]
                                },
                            },
                        },
                    },
                }
            ]
        ),
        encoding="utf-8",
    )
    output = tmp_path / "Knowledge"
    result = WayfinderExportMiner().mine_paths((shard,))
    write_knowledge_base(result, output)

    compiled = compile_knowledge_base(output)

    assert compiled.status == "ok"
    assert (output / "graph" / "nodes.jsonl").exists()
    assert (output / "graph" / "edges.jsonl").exists()
    assert (output / "graph" / "provenance.jsonl").exists()
    assert (output / "search" / "sqlite.db").exists()
    assert (output / "search" / "fts5.db").exists()
    assert (output / "reports" / "quality_gates.json").exists()
    assert compiled.quality_gates["provenance_missing_count"] == 0
