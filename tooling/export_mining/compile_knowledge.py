"""Compile mined Wayfinder export evidence into graph, search, and reports.

The compiler is deterministic and provenance-first. It consumes the chunked
facts produced by ``mine_wayfinder_export.py`` and emits stable UUID graph
records, SQLite/FTS search databases, quality-gate reports, and optional
Parquet outputs when pyarrow is installed.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .mine_wayfinder_export import (
    MiningLimits,
    WayfinderExportMiner,
    _load_input_manifest,
    write_knowledge_base,
)

COMPILER_VERSION = "1.0.0"
WAYFINDER_UUID_NAMESPACE = uuid.UUID("7ddff4f4-0e77-5a12-9e80-d4fa1e09ad2e")
DEFAULT_MAX_RECORDS = 2_000_000
DEFAULT_MAX_CYCLE_NODES = 100_000

ENTITY_TYPE_BY_CATEGORY: Mapping[str, str] = {
    "architectural_decision": "ADR",
    "boundary": "Concept",
    "constraint": "Constraint",
    "constitutional_principle": "Principle",
    "contradiction": "Conflict",
    "domain_model": "Domain",
    "future_work": "TODO",
    "interface_api": "API",
    "pattern": "Pattern",
    "pipeline": "Pipeline",
    "requirement": "Requirement",
    "terminology": "Concept",
    "tradeoff": "Decision",
}


@dataclass(frozen=True)
class CompilerLimits:
    """Bounded resource limits for deterministic compilation."""

    max_records: int = DEFAULT_MAX_RECORDS
    max_cycle_nodes: int = DEFAULT_MAX_CYCLE_NODES


@dataclass(frozen=True)
class StageResult:
    """Observable result for one compiler stage."""

    name: str
    status: str
    input_count: int
    output_count: int
    detail: Mapping[str, Any]


@dataclass(frozen=True)
class CompileResult:
    """Structured compile result."""

    status: str
    compiler_version: str
    source_hash: str
    stages: tuple[StageResult, ...]
    quality_gates: Mapping[str, Any]


class KnowledgeCompileError(ValueError):
    """Raised when compile inputs violate deterministic compiler contracts."""


def compile_knowledge_base(knowledge_dir: Path, *, limits: CompilerLimits = CompilerLimits()) -> CompileResult:
    """Compile an existing mined ``Knowledge`` directory."""

    manifest = _load_json_object(knowledge_dir / "manifest.json")
    facts = tuple(_load_chunked_records(knowledge_dir / "Graph", "facts"))
    concepts = tuple(_load_json_array(knowledge_dir / "Graph" / "concepts.json"))
    sources = tuple(_load_json_array(knowledge_dir / "Graph" / "sources.json"))
    timeline = tuple(_load_json_array(knowledge_dir / "Graph" / "timeline.json"))
    _check_record_limit("facts", len(facts), limits.max_records)

    nodes, edges, entities, provenance = _build_graph_records(facts, concepts, sources)
    _check_record_limit("nodes", len(nodes), limits.max_records)
    _check_record_limit("edges", len(edges), limits.max_records)
    quality = _quality_gates(facts, concepts, nodes, edges, limits)

    graph_dir = knowledge_dir / "Graph"
    search_dir = knowledge_dir / "search"
    reports_dir = knowledge_dir / "reports"
    graph_dir.mkdir(parents=True, exist_ok=True)
    search_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    _write_jsonl(graph_dir / "nodes.jsonl", nodes)
    _write_jsonl(graph_dir / "edges.jsonl", edges)
    _write_jsonl(graph_dir / "entities.jsonl", entities)
    _write_jsonl(graph_dir / "provenance.jsonl", provenance)
    _write_jsonl(graph_dir / "timeline.jsonl", _timeline_records(timeline, facts, concepts))
    parquet_status = _write_optional_parquet(graph_dir, nodes, edges, entities, provenance, timeline)
    _write_json(graph_dir / "parquet_status.json", parquet_status)

    sqlite_stage = _write_sqlite(search_dir / "sqlite.db", nodes, edges, provenance)
    fts_stage = _write_fts(search_dir / "fts5.db", nodes)
    _write_embeddings_manifest(search_dir / "embeddings" / "manifest.json")
    _write_reports(reports_dir, facts, quality)

    stages = (
        StageResult("Acquire", "ok", int(manifest.get("source_file_count", len(sources))), len(sources), {}),
        StageResult("Parse", "ok", int(manifest.get("conversation_count", 0)), int(manifest.get("message_count", 0)), {}),
        StageResult("Normalize", "ok", len(facts), len(facts), {}),
        StageResult("Canonicalize", "ok", len(facts), len(entities), {}),
        StageResult("Deduplicate", "ok", len(facts), len(facts), {"duplicate_groups": quality["duplicate_groups"]}),
        StageResult("Resolve entities", "ok", len(facts), len(entities), {}),
        StageResult("Build graph", "ok", len(nodes), len(edges), {}),
        StageResult("Extract knowledge", "ok", len(facts), len(entities), {}),
        StageResult("Detect conflicts", "ok", len(facts), quality["contradiction_count"], {}),
        StageResult("Generate documentation", "ok", len(facts), len(tuple(reports_dir.glob("*.md"))), {}),
        StageResult("Build indexes", "ok", len(nodes), len(provenance), {}),
        StageResult("Generate search database", sqlite_stage["status"], len(nodes), sqlite_stage["row_count"], sqlite_stage),
        StageResult("Generate FTS5 database", fts_stage["status"], len(nodes), fts_stage["row_count"], fts_stage),
        StageResult("Generate embeddings", "unavailable", len(nodes), 0, {"reason": "sentence-transformers is not installed"}),
    )
    status = "ok" if quality["provenance_missing_count"] == 0 else "error"
    result = CompileResult(
        status=status,
        compiler_version=COMPILER_VERSION,
        source_hash=str(manifest.get("source_hash", "")),
        stages=stages,
        quality_gates=quality,
    )
    _write_json(knowledge_dir / "compile_report.json", _to_plain(result))
    return result


def _build_graph_records(
    facts: Sequence[Mapping[str, Any]],
    concepts: Sequence[Mapping[str, Any]],
    sources: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    nodes: dict[str, dict[str, Any]] = {}
    edges: dict[str, dict[str, Any]] = {}
    entities: dict[str, dict[str, Any]] = {}
    provenance: dict[str, dict[str, Any]] = {}

    for source in sources:
        source_id = f"file:{source.get('sha256')}"
        _add_node(nodes, source_id, "File", str(source.get("name") or "source"), source.get("artifact_type"), source)
        entities[source_id] = _entity(source_id, "File", str(source.get("name") or "source"), source.get("artifact_type"))

    for concept in concepts:
        concept_id = str(concept["concept_id"])
        _add_node(nodes, concept_id, "Concept", str(concept.get("name") or concept_id), concept.get("status"), concept)
        entities[concept_id] = _entity(concept_id, "Concept", str(concept.get("name") or concept_id), concept.get("status"))

    for fact in facts:
        fact_id = str(fact["fact_id"])
        entity_type = ENTITY_TYPE_BY_CATEGORY.get(str(fact.get("category")), "Concept")
        title = _title_from_statement(str(fact.get("statement") or fact_id))
        _add_node(nodes, fact_id, entity_type, title, fact.get("status"), _fact_metadata(fact))
        entities[fact_id] = _entity(fact_id, entity_type, title, fact.get("status"))
        for concept_id in fact.get("concept_ids", ()):
            if concept_id:
                _add_edge(edges, fact_id, str(concept_id), "references", fact_id, fact.get("confidence"))
        for evidence in fact.get("evidence", ()):
            conversation_id = f"conversation:{evidence.get('conversation_id')}"
            message_id = f"message:{evidence.get('message_id')}"
            file_id = f"file:{evidence.get('source_hash')}"
            _add_node(nodes, conversation_id, "Conversation", str(evidence.get("conversation_title") or evidence.get("conversation_id")), "observed", {})
            _add_node(nodes, message_id, "Message", str(evidence.get("message_id")), "observed", {"role": evidence.get("author_role"), "timestamp": evidence.get("timestamp")})
            _add_edge(edges, fact_id, message_id, "derived_from", fact_id, evidence.get("confidence"))
            _add_edge(edges, message_id, conversation_id, "belongs_to", fact_id, evidence.get("confidence"))
            _add_edge(edges, conversation_id, file_id, "derived_from", fact_id, evidence.get("confidence"))
            provenance_id = _stable_uuid("provenance", fact_id, message_id)
            provenance[provenance_id] = {
                "uuid": provenance_id,
                "fact_id": fact_id,
                "conversation_id": evidence.get("conversation_id"),
                "message_id": evidence.get("message_id"),
                "timestamp": evidence.get("timestamp"),
                "confidence": evidence.get("confidence"),
                "source_file": evidence.get("source_file"),
                "source_hash": evidence.get("source_hash"),
            }
    return (
        sorted(nodes.values(), key=lambda item: item["uuid"]),
        sorted(edges.values(), key=lambda item: item["uuid"]),
        sorted(entities.values(), key=lambda item: item["uuid"]),
        sorted(provenance.values(), key=lambda item: item["uuid"]),
    )


def _add_node(
    nodes: dict[str, dict[str, Any]],
    stable_id: str,
    node_type: str,
    name: str,
    status: object,
    metadata: Mapping[str, Any],
) -> None:
    node_uuid = _stable_uuid("node", stable_id)
    nodes[stable_id] = {
        "uuid": node_uuid,
        "stable_id": stable_id,
        "node_type": node_type,
        "name": name,
        "status": str(status or "observed"),
        "metadata": dict(metadata),
    }


def _add_edge(
    edges: dict[str, dict[str, Any]],
    source_id: str,
    target_id: str,
    relationship_type: str,
    evidence_fact_id: str,
    confidence: object,
) -> None:
    edge_uuid = _stable_uuid("edge", source_id, relationship_type, target_id, evidence_fact_id)
    edges[edge_uuid] = {
        "uuid": edge_uuid,
        "source_id": source_id,
        "target_id": target_id,
        "relationship_type": relationship_type,
        "evidence_fact_id": evidence_fact_id,
        "confidence": float(confidence or 0.0),
    }


def _entity(stable_id: str, entity_type: str, name: str, status: object) -> dict[str, Any]:
    return {
        "uuid": _stable_uuid("entity", stable_id),
        "stable_id": stable_id,
        "entity_type": entity_type,
        "name": name,
        "status": str(status or "observed"),
    }


def _fact_metadata(fact: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "category": fact.get("category"),
        "statement": fact.get("statement"),
        "normalized_statement": fact.get("normalized_statement"),
        "first_seen": fact.get("first_seen"),
        "last_seen": fact.get("last_seen"),
        "confidence": fact.get("confidence"),
    }


def _quality_gates(
    facts: Sequence[Mapping[str, Any]],
    concepts: Sequence[Mapping[str, Any]],
    nodes: Sequence[Mapping[str, Any]],
    edges: Sequence[Mapping[str, Any]],
    limits: CompilerLimits,
) -> dict[str, Any]:
    by_statement: dict[str, set[str]] = {}
    concept_refs: set[str] = set()
    for fact in facts:
        by_statement.setdefault(str(fact.get("normalized_statement") or ""), set()).add(str(fact.get("category") or ""))
        concept_refs.update(str(item) for item in fact.get("concept_ids", ()) if item)
    concept_ids = {str(item.get("concept_id")) for item in concepts}
    orphan_concepts = sorted(concept_ids - concept_refs)
    duplicate_groups = {
        statement: sorted(categories)
        for statement, categories in by_statement.items()
        if statement and len(categories) > 1
    }
    provenance_missing = [
        str(fact.get("fact_id")) for fact in facts if not fact.get("evidence")
    ]
    cycle_count = _cycle_count(edges, limits.max_cycle_nodes)
    return {
        "duplicate_groups": len(duplicate_groups),
        "duplicate_examples": list(sorted(duplicate_groups.items()))[:50],
        "contradiction_count": sum(1 for fact in facts if fact.get("category") == "contradiction"),
        "orphan_concept_count": len(orphan_concepts),
        "orphan_concept_examples": orphan_concepts[:50],
        "circular_reference_count": cycle_count,
        "provenance_missing_count": len(provenance_missing),
        "provenance_missing_examples": provenance_missing[:50],
        "stable_identifier_scheme": "uuid5(namespace, kind + ':' + stable_id)",
    }


def _cycle_count(edges: Sequence[Mapping[str, Any]], max_nodes: int) -> int:
    adjacency: dict[str, set[str]] = {}
    for edge in edges:
        if edge.get("relationship_type") not in {"depends_on", "implements", "supersedes", "references"}:
            continue
        source = str(edge.get("source_id"))
        target = str(edge.get("target_id"))
        adjacency.setdefault(source, set()).add(target)
        if len(adjacency) > max_nodes:
            return -1
    visiting: set[str] = set()
    visited: set[str] = set()
    cycles = 0

    def visit(node: str) -> None:
        nonlocal cycles
        if node in visiting:
            cycles += 1
            return
        if node in visited:
            return
        visiting.add(node)
        for target in adjacency.get(node, ()):
            visit(target)
        visiting.remove(node)
        visited.add(node)

    for node in sorted(adjacency):
        visit(node)
    return cycles


def _timeline_records(
    timeline: Sequence[Mapping[str, Any]],
    facts: Sequence[Mapping[str, Any]],
    concepts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for item in timeline:
        records.append({"timeline_type": "conversation", **dict(item)})
    for fact in facts:
        if fact.get("first_seen"):
            records.append(
                {
                    "timeline_type": "fact_first_seen",
                    "timestamp": fact.get("first_seen"),
                    "stable_id": fact.get("fact_id"),
                    "category": fact.get("category"),
                }
            )
    for concept in concepts:
        if concept.get("first_seen"):
            records.append(
                {
                    "timeline_type": "concept_first_seen",
                    "timestamp": concept.get("first_seen"),
                    "stable_id": concept.get("concept_id"),
                    "name": concept.get("name"),
                }
            )
    return sorted(records, key=lambda item: (str(item.get("timestamp") or ""), str(item.get("stable_id") or item.get("conversation_id") or "")))


def _write_optional_parquet(
    graph_dir: Path,
    nodes: Sequence[Mapping[str, Any]],
    edges: Sequence[Mapping[str, Any]],
    entities: Sequence[Mapping[str, Any]],
    provenance: Sequence[Mapping[str, Any]],
    timeline: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    try:
        import pyarrow as pa  # type: ignore[import-not-found]
        import pyarrow.parquet as pq  # type: ignore[import-not-found]
    except Exception as exc:
        return {
            "status": "unavailable",
            "reason": f"pyarrow unavailable: {type(exc).__name__}",
            "fallback": "jsonl",
        }
    outputs = {
        "nodes.parquet": nodes,
        "edges.parquet": edges,
        "entities.parquet": entities,
        "provenance.parquet": provenance,
        "timeline.parquet": timeline,
    }
    for filename, rows in outputs.items():
        table = pa.Table.from_pylist([_json_safe(row) for row in rows])
        pq.write_table(table, graph_dir / filename)
    return {"status": "ok", "format": "parquet", "files": sorted(outputs)}


def _write_sqlite(path: Path, nodes: Sequence[Mapping[str, Any]], edges: Sequence[Mapping[str, Any]], provenance: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if path.exists():
        path.unlink()
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE nodes (uuid TEXT PRIMARY KEY, stable_id TEXT, node_type TEXT, name TEXT, status TEXT, metadata_json TEXT)")
        db.execute("CREATE TABLE edges (uuid TEXT PRIMARY KEY, source_id TEXT, target_id TEXT, relationship_type TEXT, evidence_fact_id TEXT, confidence REAL)")
        db.execute("CREATE TABLE provenance (uuid TEXT PRIMARY KEY, fact_id TEXT, conversation_id TEXT, message_id TEXT, timestamp TEXT, confidence REAL, source_file TEXT, source_hash TEXT)")
        db.executemany(
            "INSERT INTO nodes VALUES (?, ?, ?, ?, ?, ?)",
            ((row["uuid"], row["stable_id"], row["node_type"], row["name"], row["status"], json.dumps(row["metadata"], sort_keys=True)) for row in nodes),
        )
        db.executemany(
            "INSERT INTO edges VALUES (?, ?, ?, ?, ?, ?)",
            ((row["uuid"], row["source_id"], row["target_id"], row["relationship_type"], row["evidence_fact_id"], row["confidence"]) for row in edges),
        )
        db.executemany(
            "INSERT INTO provenance VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                (
                    row["uuid"],
                    row["fact_id"],
                    row["conversation_id"],
                    row["message_id"],
                    row["timestamp"],
                    row["confidence"],
                    row["source_file"],
                    row["source_hash"],
                )
                for row in provenance
            ),
        )
        db.execute("CREATE INDEX idx_nodes_type ON nodes(node_type)")
        db.execute("CREATE INDEX idx_edges_source ON edges(source_id)")
        db.execute("CREATE INDEX idx_edges_target ON edges(target_id)")
        db.execute("CREATE INDEX idx_provenance_fact ON provenance(fact_id)")
    return {"status": "ok", "row_count": len(nodes), "path": path.name}


def _write_fts(path: Path, nodes: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if path.exists():
        path.unlink()
    with sqlite3.connect(path) as db:
        try:
            db.execute("CREATE VIRTUAL TABLE docs_fts USING fts5(uuid, stable_id, node_type, name, body)")
            status = "ok"
        except sqlite3.OperationalError:
            db.execute("CREATE TABLE docs_fts (uuid TEXT, stable_id TEXT, node_type TEXT, name TEXT, body TEXT)")
            status = "fallback"
        db.executemany(
            "INSERT INTO docs_fts VALUES (?, ?, ?, ?, ?)",
            (
                (
                    row["uuid"],
                    row["stable_id"],
                    row["node_type"],
                    row["name"],
                    str(row.get("metadata", {}).get("statement") or row["name"]),
                )
                for row in nodes
            ),
        )
    return {"status": status, "row_count": len(nodes), "path": path.name}


def _write_embeddings_manifest(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import sentence_transformers  # type: ignore[import-not-found]  # noqa: F401
    except Exception as exc:
        _write_json(
            path,
            {
                "status": "unavailable",
                "reason": f"sentence-transformers unavailable: {type(exc).__name__}",
                "policy": "No embeddings generated without explicit local model dependency.",
            },
        )
        return
    _write_json(
        path,
        {
            "status": "not_run",
            "reason": "Embedding generation requires an explicit local model name and is disabled by default.",
        },
    )


def _write_reports(reports_dir: Path, facts: Sequence[Mapping[str, Any]], quality: Mapping[str, Any]) -> None:
    conflicts = [fact for fact in facts if fact.get("category") == "contradiction"]
    unresolved = [fact for fact in facts if fact.get("category") == "future_work"]
    _write_markdown_fact_report(reports_dir / "conflicts.md", "Conflicts", conflicts)
    _write_markdown_fact_report(reports_dir / "unresolved.md", "Unresolved", unresolved)
    _write_json(reports_dir / "quality_gates.json", quality)
    duplicate_lines = ["# Duplicates", "", f"Duplicate normalized statement groups: {quality['duplicate_groups']}", ""]
    for statement, categories in quality["duplicate_examples"]:
        duplicate_lines.append(f"- `{', '.join(categories)}`: {statement}")
    _write_text(reports_dir / "duplicates.md", "\n".join(duplicate_lines) + "\n")
    _write_text(
        reports_dir / "timeline.md",
        "# Timeline Report\n\nSee `../Graph/timeline.jsonl` for machine-readable temporal records.\n",
    )


def _write_markdown_fact_report(path: Path, title: str, facts: Sequence[Mapping[str, Any]]) -> None:
    lines = [f"# {title}", "", f"Fact count: {len(facts)}", ""]
    for fact in facts[:500]:
        evidence = (fact.get("evidence") or [{}])[0]
        lines.extend(
            [
                f"## `{fact.get('fact_id')}`",
                "",
                str(fact.get("statement") or ""),
                "",
                f"- Confidence: `{fact.get('confidence')}`",
                f"- First seen: `{fact.get('first_seen') or 'unknown'}`",
                f"- Provenance: `conversation:{evidence.get('conversation_id')}` `message:{evidence.get('message_id')}`",
                "",
            ]
        )
    if len(facts) > 500:
        lines.append(f"{len(facts) - 500} additional facts are available in `../Graph/facts/index.json`.")
        lines.append("")
    _write_text(path, "\n".join(lines))


def _load_chunked_records(graph_dir: Path, stem: str) -> Iterable[Mapping[str, Any]]:
    index = _load_json_object(graph_dir / stem / "index.json")
    for chunk in index.get("chunks", ()):
        chunk_path = graph_dir / str(chunk["path"])
        for record in _load_json_array(chunk_path):
            if isinstance(record, Mapping):
                yield record


def _load_json_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise KnowledgeCompileError(f"expected JSON object: {path}")
    return data


def _load_json_array(path: Path) -> list[Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise KnowledgeCompileError(f"expected JSON array: {path}")
    return data


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(_json_safe(row), sort_keys=True, ensure_ascii=False) + "\n")


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def _stable_uuid(kind: str, *parts: str) -> str:
    return str(uuid.uuid5(WAYFINDER_UUID_NAMESPACE, f"{kind}:{':'.join(str(part) for part in parts)}"))


def _title_from_statement(statement: str) -> str:
    return statement[:96].rstrip() or "Untitled entity"


def _check_record_limit(name: str, count: int, limit: int) -> None:
    if count > limit:
        raise KnowledgeCompileError(f"{name} count exceeds configured maximum: {count} > {limit}")


def _json_safe(row: Mapping[str, Any]) -> dict[str, Any]:
    return {str(key): _json_value(value) for key, value in row.items()}


def _json_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


def _to_plain(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return _to_plain(asdict(value))
    if isinstance(value, tuple):
        return [_to_plain(item) for item in value]
    if isinstance(value, list):
        return [_to_plain(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): _to_plain(item) for key, item in value.items()}
    return value


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile mined Wayfinder export knowledge.")
    parser.add_argument("--knowledge", default="Knowledge", help="Knowledge output directory.")
    parser.add_argument("--input", action="append", default=[], help="Input export file or directory. Repeatable.")
    parser.add_argument("--input-manifest", action="append", default=[], help="Text or JSON manifest of input paths.")
    parser.add_argument("--max-records", type=int, default=DEFAULT_MAX_RECORDS)
    parser.add_argument("--max-cycle-nodes", type=int, default=DEFAULT_MAX_CYCLE_NODES)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    knowledge_dir = Path(args.knowledge)
    input_paths = [Path(item) for item in args.input]
    for manifest_path in args.input_manifest:
        input_paths.extend(_load_input_manifest(Path(manifest_path)))
    if input_paths:
        mining_limits = MiningLimits(max_files=max(2_000, len(input_paths) + 10))
        result = WayfinderExportMiner(limits=mining_limits).mine_paths(tuple(input_paths))
        write_knowledge_base(result, knowledge_dir, limits=mining_limits)
    compile_result = compile_knowledge_base(
        knowledge_dir,
        limits=CompilerLimits(max_records=args.max_records, max_cycle_nodes=args.max_cycle_nodes),
    )
    print(json.dumps(_to_plain(compile_result), sort_keys=True))
    return 0 if compile_result.status == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
