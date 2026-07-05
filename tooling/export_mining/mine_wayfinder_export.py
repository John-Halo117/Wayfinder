"""Mine ChatGPT export shards into a provenance-backed Wayfinder knowledge base.

This tool is intentionally deterministic and non-AI. It reads historical
ChatGPT export JSON files as evidence, extracts architecture-relevant facts
with explicit rule markers, preserves provenance for every emitted fact, and
generates concise canonical documentation plus machine-readable graph files.
It does not copy raw export files into the repository.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

MINER_VERSION = "1.0.0"
DEFAULT_SOURCE_KIND = "chatgpt-export"
DEFAULT_MAX_FILES = 2_000
DEFAULT_MAX_FILE_BYTES = 768 * 1024 * 1024
DEFAULT_MAX_CONVERSATIONS = 100_000
DEFAULT_MAX_MESSAGES = 1_000_000
DEFAULT_MAX_FACTS = 250_000
DEFAULT_MAX_TEXT_CHARS = 200_000
DEFAULT_MAX_UNIT_CHARS = 1_600
DEFAULT_MAX_MARKDOWN_FACTS_PER_DOC = 500
DEFAULT_GRAPH_CHUNK_SIZE = 5_000


CANONICAL_TERMS: tuple[str, ...] = (
    "Reality",
    "Observation",
    "Evidence",
    "Provenance",
    "Representation",
    "Asset",
    "RID",
    "ARK",
    "Oracle",
    "ChatGPT Oracle",
    "Perception",
    "Propagation",
    "Capsule",
    "Specialist",
    "Twin",
    "Mission",
    "Mission Band",
    "Capability",
    "Capability Registry",
    "Provider",
    "Plugin",
    "Knowledge Vault",
    "Jarvis",
    "Attention Filter",
    "Affordance Field",
    "Opportunity Bundle",
    "Knowledge Graph",
    "Knowledge Compiler",
    "Knowledge Governance",
    "Knowledge Retrieval",
    "Knowledge Views",
    "Constitution",
    "Glossary",
    "Ontology",
    "ADR",
    "Pipeline",
    "Parser",
    "Import",
    "Replay",
    "Validation",
    "Boundary",
    "Interface",
    "Contract",
)

RELEVANCE_TERMS: tuple[str, ...] = tuple(
    sorted(
        {
            "wayfinder",
            "constitutional",
            "constitution",
            "ontology",
            "glossary",
            "oracle",
            "chatgpt oracle",
            "ark",
            "first contact",
            "canonical language",
            "canonical term",
            "canonical vocabulary",
            "knowledge",
            "knowledge compiler",
            "knowledge governance",
            "knowledge retrieval",
            "knowledge views",
            "knowledge vault",
            "provenance",
            "observation",
            "reality precedes",
            "preserve reality",
            "capability registry",
            "capsule",
            "jarvis",
            "mission",
            "mission band",
            "affordance field",
            "opportunity bundle",
            "rid",
            "replay",
            "adr",
        }
    )
)

BROAD_ARCHITECTURE_TERMS: tuple[str, ...] = (
    "architecture",
    "architectural",
    "boundary",
    "capability",
    "contract",
    "domain",
    "engine",
    "graph",
    "identity",
    "index",
    "interface",
    "lifecycle",
    "module",
    "parser",
    "pipeline",
    "plugin",
    "provider",
    "registry",
    "relationship",
    "repository",
    "schema",
    "service",
    "validation",
)

PROJECT_TITLE_TERMS: tuple[str, ...] = (
    "wayfinder",
    "ark",
    "jarvis",
    "first contact",
    "chatgpt export",
    "gpt export",
    "oracle",
    "ontology",
    "constitution",
    "canonical language",
    "knowledge compiler",
    "knowledge governance",
    "knowledge retrieval",
    "knowledge views",
    "repository",
)

CATEGORY_RULES: Mapping[str, tuple[str, ...]] = {
    "constitutional_principle": (
        "always",
        "never",
        "prefer",
        "principle",
        "constitutional principle",
        "reality precedes",
        "observation precedes",
        "preserve before",
        "observe before",
        "local-first",
        "privacy-first",
        "must preserve",
    ),
    "architectural_decision": (
        "decision",
        "decide",
        "decided",
        "accepted",
        "canonical",
        "promoted",
        "established",
        "chosen",
        "adr",
    ),
    "requirement": (
        "requirement",
        "requirements",
        "shall",
        "must",
        "should",
        "success criteria",
        "responsible for",
        "not responsible for",
    ),
    "constraint": (
        "constraint",
        "do not",
        "cannot",
        "must not",
        "bounded",
        "resource cap",
        "idempotent",
        "deterministic",
        "append-only",
        "privacy",
        "local-first",
    ),
    "boundary": (
        "boundary",
        "owns",
        "owner",
        "responsibility",
        "non-responsibility",
        "separation",
        "belongs to",
        "leak",
    ),
    "domain_model": (
        "domain",
        "schema",
        "artifact",
        "observation",
        "relationship",
        "provenance",
        "asset",
        "rid",
    ),
    "pattern": (
        "pattern",
        "practice",
        "workflow",
        "strategy",
        "migration",
        "preserve",
        "extract",
        "consolidate",
        "replaceable",
    ),
    "pipeline": (
        "pipeline",
        "ingest",
        "import",
        "parse",
        "compiler",
        "governance",
        "retrieval",
        "views",
        "promotion",
        "replay",
    ),
    "interface_api": (
        "interface",
        "api",
        "contract",
        "provider",
        "registry",
        "schema",
        "service",
        "implements",
    ),
    "terminology": (
        "term",
        "glossary",
        "ontology",
        "canonical term",
        "alias",
        "rename",
        "renamed",
        "deprecated",
        "definition",
    ),
    "tradeoff": (
        "tradeoff",
        "risk",
        "cost",
        "benefit",
        "rationale",
        "instead",
    ),
    "future_work": (
        "todo",
        "future work",
        "open question",
        "later phase",
        "phase 9",
        "missing",
        "incomplete",
        "needs validation",
        "next step",
    ),
    "contradiction": (
        "contradiction",
        "conflict",
        "conflicts",
        "versus",
        " vs ",
        "disproven",
        "replaced by",
        "superseded",
    ),
}

DIRECTORY_FOR_CATEGORY: Mapping[str, str] = {
    "constitutional_principle": "Constitution",
    "architectural_decision": "Decisions",
    "requirement": "Requirements",
    "constraint": "Requirements",
    "boundary": "Architecture",
    "domain_model": "Domains",
    "pattern": "Patterns",
    "pipeline": "Pipelines",
    "interface_api": "Architecture",
    "terminology": "Glossary",
    "tradeoff": "Research",
    "future_work": "OpenQuestions",
    "contradiction": "Research",
}


@dataclass(frozen=True)
class MiningLimits:
    """Bounded resource limits for export mining."""

    max_files: int = DEFAULT_MAX_FILES
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES
    max_conversations: int = DEFAULT_MAX_CONVERSATIONS
    max_messages: int = DEFAULT_MAX_MESSAGES
    max_facts: int = DEFAULT_MAX_FACTS
    max_text_chars: int = DEFAULT_MAX_TEXT_CHARS
    max_unit_chars: int = DEFAULT_MAX_UNIT_CHARS
    max_markdown_facts_per_doc: int = DEFAULT_MAX_MARKDOWN_FACTS_PER_DOC
    graph_chunk_size: int = DEFAULT_GRAPH_CHUNK_SIZE


@dataclass(frozen=True)
class SourceFile:
    """Source export file metadata without raw content."""

    path: str
    name: str
    size_bytes: int
    sha256: str
    artifact_type: str


@dataclass(frozen=True)
class EvidenceRef:
    """Traceable evidence for an extracted fact."""

    conversation_id: str
    conversation_title: str | None
    message_id: str
    author_role: str | None
    timestamp: str | None
    source_file: str
    source_hash: str
    confidence: float


@dataclass
class ExtractedFact:
    """Architecture-relevant fact extracted from historical evidence."""

    fact_id: str
    category: str
    statement: str
    normalized_statement: str
    concept_ids: set[str]
    evidence: list[EvidenceRef] = field(default_factory=list)
    first_seen: str | None = None
    last_seen: str | None = None
    confidence: float = 0.0
    status: str = "observed"
    evolution: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class GraphConcept:
    """Stable concept node."""

    concept_id: str
    name: str
    slug: str
    status: str
    categories: tuple[str, ...]
    first_seen: str | None
    last_seen: str | None
    evidence_count: int


@dataclass(frozen=True)
class GraphRelationship:
    """Evidence-backed graph relationship."""

    relationship_id: str
    relationship_type: str
    source_id: str
    target_id: str
    evidence_fact_id: str
    confidence: float


@dataclass(frozen=True)
class MiningResult:
    """Complete deterministic mining output."""

    source_kind: str
    source_hash: str
    source_files: tuple[SourceFile, ...]
    conversation_count: int
    message_count: int
    fact_count: int
    concept_count: int
    relationship_count: int
    facts: tuple[ExtractedFact, ...]
    concepts: tuple[GraphConcept, ...]
    relationships: tuple[GraphRelationship, ...]
    contradictions: tuple[ExtractedFact, ...]
    timeline: tuple[dict[str, Any], ...]


class ExportMiningError(ValueError):
    """Structured mining failure."""


class WayfinderExportMiner:
    """Deterministically mine architecture facts from ChatGPT export shards."""

    def __init__(self, *, limits: MiningLimits = MiningLimits()) -> None:
        self._limits = limits

    def mine_paths(self, inputs: Sequence[Path]) -> MiningResult:
        source_files = tuple(self._discover_sources(inputs))
        _check_count("files", len(source_files), self._limits.max_files)
        source_hash = _stable_hash([item.sha256 for item in source_files])
        facts_by_key: dict[tuple[str, str], ExtractedFact] = {}
        conversation_count = 0
        message_count = 0
        timeline_events: list[dict[str, Any]] = []

        for source in source_files:
            if not _is_conversation_file(source.name):
                continue
            data = _load_json_array(Path(source.path), self._limits.max_file_bytes)
            conversation_count += len(data)
            _check_count("conversations", conversation_count, self._limits.max_conversations)
            for conversation in data:
                if not isinstance(conversation, Mapping):
                    continue
                ordered_messages = tuple(_ordered_messages(conversation))
                message_count += len(ordered_messages)
                _check_count("messages", message_count, self._limits.max_messages)
                for message in ordered_messages:
                    self._extract_from_message(conversation, message, source, facts_by_key)
                if ordered_messages:
                    first_ts = _iso_timestamp(_message_timestamp(ordered_messages[0]))
                    title = _clean_inline(str(conversation.get("title") or "Untitled conversation"))
                    timeline_events.append(
                        {
                            "timestamp": first_ts,
                            "conversation_id": str(conversation.get("conversation_id") or conversation.get("id") or ""),
                            "title": title,
                            "source_file": source.name,
                            "message_count": len(ordered_messages),
                        }
                    )

        facts = tuple(sorted(facts_by_key.values(), key=lambda item: item.fact_id))
        _check_count("facts", len(facts), self._limits.max_facts)
        concepts = tuple(sorted(_build_concepts(facts), key=lambda item: item.concept_id))
        relationships = tuple(sorted(_build_relationships(facts), key=lambda item: item.relationship_id))
        contradictions = tuple(item for item in facts if item.category == "contradiction")
        timeline = tuple(sorted(timeline_events, key=lambda item: ((item.get("timestamp") or ""), item["conversation_id"])))
        return MiningResult(
            source_kind=DEFAULT_SOURCE_KIND,
            source_hash=source_hash,
            source_files=source_files,
            conversation_count=conversation_count,
            message_count=message_count,
            fact_count=len(facts),
            concept_count=len(concepts),
            relationship_count=len(relationships),
            facts=facts,
            concepts=concepts,
            relationships=relationships,
            contradictions=contradictions,
            timeline=timeline,
        )

    def _discover_sources(self, inputs: Sequence[Path]) -> list[SourceFile]:
        paths: list[Path] = []
        for item in inputs:
            if item.is_dir():
                paths.extend(path for path in item.rglob("*.json") if path.is_file())
            elif item.is_file():
                paths.append(item)
            else:
                raise ExportMiningError(f"input path does not exist: {item}")
        deduped = sorted({path.resolve() for path in paths}, key=lambda path: path.as_posix())
        sources: list[SourceFile] = []
        for path in deduped:
            size = path.stat().st_size
            if size > self._limits.max_file_bytes:
                raise ExportMiningError(f"source file exceeds configured maximum: {path}")
            digest = _file_sha256(path)
            sources.append(
                SourceFile(
                    path=str(path),
                    name=path.name,
                    size_bytes=size,
                    sha256=digest,
                    artifact_type=_classify_source_file(path.name),
                )
            )
        return sources

    def _extract_from_message(
        self,
        conversation: Mapping[str, Any],
        message_node: Mapping[str, Any],
        source: SourceFile,
        facts_by_key: dict[tuple[str, str], ExtractedFact],
    ) -> None:
        message = message_node.get("message")
        if not isinstance(message, Mapping):
            return
        text = _message_text(message, self._limits.max_text_chars)
        if not text:
            return
        conversation_id = str(conversation.get("conversation_id") or conversation.get("id") or "")
        message_id = str(message.get("id") or message_node.get("id") or "")
        if not conversation_id or not message_id:
            return
        timestamp = _iso_timestamp(_message_timestamp(message_node))
        role = _author_role(message)
        evidence = EvidenceRef(
            conversation_id=conversation_id,
            conversation_title=_clean_inline(str(conversation.get("title") or "")) or None,
            message_id=message_id,
            author_role=role,
            timestamp=timestamp,
            source_file=source.name,
            source_hash=source.sha256,
            confidence=0.0,
        )
        title = str(conversation.get("title") or "")
        for unit in _extract_units(text, self._limits.max_unit_chars):
            context = f"{title}\n{unit}"
            if not _unit_has_architecture_signal(unit, title):
                continue
            categories = _categories_for_unit(unit)
            if not categories:
                continue
            concept_ids = _concept_ids_for_unit(context)
            if not concept_ids and not _unit_has_architecture_signal(unit, title):
                continue
            normalized = _normalize_statement(unit)
            if not normalized:
                continue
            for category, base_confidence in categories:
                key = (category, normalized)
                confidence = _confidence_for_unit(context, category, base_confidence)
                fact = facts_by_key.get(key)
                if fact is None:
                    fact_id = _stable_id("fact", category, normalized)
                    fact = ExtractedFact(
                        fact_id=fact_id,
                        category=category,
                        statement=_clean_statement(unit),
                        normalized_statement=normalized,
                        concept_ids=set(concept_ids),
                        confidence=confidence,
                        status=_status_for_unit(unit),
                    )
                    facts_by_key[key] = fact
                fact.concept_ids.update(concept_ids)
                fact.confidence = max(fact.confidence, confidence)
                fact.evidence.append(evidence_with_confidence(evidence, confidence))
                fact.first_seen, fact.last_seen = _seen_range(fact.first_seen, fact.last_seen, timestamp)
                evolution = _evolution_marker(unit)
                if evolution and evolution not in fact.evolution:
                    fact.evolution.append(evolution)


def evidence_with_confidence(evidence: EvidenceRef, confidence: float) -> EvidenceRef:
    return EvidenceRef(
        conversation_id=evidence.conversation_id,
        conversation_title=evidence.conversation_title,
        message_id=evidence.message_id,
        author_role=evidence.author_role,
        timestamp=evidence.timestamp,
        source_file=evidence.source_file,
        source_hash=evidence.source_hash,
        confidence=confidence,
    )


def write_knowledge_base(result: MiningResult, output_dir: Path, *, limits: MiningLimits = MiningLimits()) -> None:
    """Write deterministic graph data and Markdown knowledge docs."""

    output_dir.mkdir(parents=True, exist_ok=True)
    for directory in (
        "Constitution",
        "Architecture",
        "Domains",
        "Pipelines",
        "Glossary",
        "ADR",
        "Requirements",
        "Patterns",
        "Decisions",
        "Research",
        "Historical",
        "OpenQuestions",
        "Graph",
        "Indexes",
    ):
        (output_dir / directory).mkdir(parents=True, exist_ok=True)

    _write_json(output_dir / "manifest.json", _manifest(result))
    _write_json(output_dir / "Graph" / "concepts.json", [asdict(item) for item in result.concepts])
    _write_chunked_json(output_dir / "Graph", "relationships", [asdict(item) for item in result.relationships], limits.graph_chunk_size)
    _write_chunked_json(output_dir / "Graph", "facts", [_fact_to_plain(item) for item in result.facts], limits.graph_chunk_size)
    _write_chunked_json(
        output_dir / "Graph",
        "contradictions",
        [_fact_to_plain(item) for item in result.contradictions],
        limits.graph_chunk_size,
    )
    _write_json(output_dir / "Graph" / "sources.json", [_source_to_public(item) for item in result.source_files])
    _write_json(output_dir / "Graph" / "timeline.json", list(result.timeline))

    _write_text(output_dir / "README.md", _render_root_readme(result))
    _write_text(output_dir / "Historical" / "timeline.md", _render_timeline(result))
    _write_text(output_dir / "Indexes" / "concepts.md", _render_concept_index(result))
    _write_text(output_dir / "Indexes" / "sources.md", _render_source_index(result))
    _write_text(output_dir / "Indexes" / "provenance.md", _render_provenance_index(result))
    _write_text(output_dir / "ADR" / "README.md", _render_adr_index(result, limits))

    by_directory: dict[str, list[ExtractedFact]] = {}
    for fact in result.facts:
        by_directory.setdefault(DIRECTORY_FOR_CATEGORY.get(fact.category, "Research"), []).append(fact)
    for directory in (
        "Constitution",
        "Architecture",
        "Domains",
        "Pipelines",
        "Glossary",
        "Requirements",
        "Patterns",
        "Decisions",
        "Research",
        "Historical",
        "OpenQuestions",
    ):
        facts = tuple(sorted(by_directory.get(directory, ()), key=lambda item: (item.category, item.statement)))
        _write_text(output_dir / directory / "README.md", _render_category_doc(directory, facts, result, limits))


def _manifest(result: MiningResult) -> dict[str, Any]:
    return {
        "schema": "wayfinder.export_mining.manifest.v1",
        "miner_version": MINER_VERSION,
        "source_kind": result.source_kind,
        "source_hash": result.source_hash,
        "generated_at": "deterministic-from-source",
        "conversation_count": result.conversation_count,
        "message_count": result.message_count,
        "fact_count": result.fact_count,
        "concept_count": result.concept_count,
        "relationship_count": result.relationship_count,
        "source_files": [_source_to_public(item) for item in result.source_files],
        "privacy": {
            "raw_export_copied": False,
            "provenance_uses_ids_and_hashes": True,
            "extraction_method": "deterministic marker rules; no AI summarization",
        },
    }


def _render_root_readme(result: MiningResult) -> str:
    return "\n".join(
        [
            "# Wayfinder Knowledge Base",
            "",
            "This directory is generated from historical ChatGPT export evidence.",
            "It contains derived architecture facts, graph data, and provenance indexes.",
            "Raw export conversations are not copied into this repository.",
            "",
            "## Invariants",
            "",
            "- Historical conversations are evidence, not canonical documentation.",
            "- Every extracted fact has source conversation and message provenance.",
            "- Generation is deterministic and uses no AI summarization.",
            "- Reruns use stable source hashes, fact IDs, concept IDs, and relationship IDs.",
            "",
            "## Inventory",
            "",
            f"- Source hash: `{result.source_hash}`",
            f"- Source files: {len(result.source_files)}",
            f"- Conversations: {result.conversation_count}",
            f"- Messages inspected: {result.message_count}",
            f"- Extracted facts: {result.fact_count}",
            f"- Concepts: {result.concept_count}",
            f"- Relationships: {result.relationship_count}",
            "",
            "## Primary Outputs",
            "",
            "- `Graph/facts/index.json`: machine-readable extracted facts with provenance, chunked for reviewability.",
            "- `Graph/concepts.json`: stable concept nodes.",
            "- `Graph/relationships/index.json`: evidence-backed graph edges, chunked for reviewability.",
            "- `Historical/timeline.md`: chronological project history index.",
            "- `Indexes/provenance.md`: provenance and source evidence index.",
            "",
        ]
    )


def _render_category_doc(
    title: str,
    facts: Sequence[ExtractedFact],
    result: MiningResult,
    limits: MiningLimits,
) -> str:
    lines = [
        f"# {title}",
        "",
        "Generated from historical export evidence. Entries are extracted facts, not conversation summaries.",
        "",
        f"Source hash: `{result.source_hash}`",
        f"Fact count in this section: {len(facts)}",
        "",
    ]
    if not facts:
        lines.extend(["No evidence-backed facts were extracted for this section.", ""])
        return "\n".join(lines)
    shown = facts[: limits.max_markdown_facts_per_doc]
    current_category = None
    for fact in shown:
        if fact.category != current_category:
            current_category = fact.category
            lines.extend([f"## {_title_from_slug(current_category)}", ""])
        evidence = fact.evidence[0] if fact.evidence else None
        provenance = _provenance_label(evidence)
        concepts = ", ".join(f"`{item}`" for item in sorted(fact.concept_ids)[:8]) or "`unclassified`"
        lines.extend(
            [
                f"### `{fact.fact_id}`",
                "",
                fact.statement,
                "",
                f"- Status: `{fact.status}`",
                f"- Confidence: `{fact.confidence:.2f}`",
                f"- Concepts: {concepts}",
                f"- First seen: `{fact.first_seen or 'unknown'}`",
                f"- Last seen: `{fact.last_seen or 'unknown'}`",
                f"- Provenance: {provenance}",
                "",
            ]
        )
    remaining = len(facts) - len(shown)
    if remaining > 0:
        lines.extend(
            [
                f"{remaining} additional facts are available in `../Graph/facts/index.json`.",
                "",
            ]
        )
    return "\n".join(lines)


def _render_adr_index(result: MiningResult, limits: MiningLimits) -> str:
    facts = tuple(
        sorted(
            (fact for fact in result.facts if fact.category in {"architectural_decision", "tradeoff", "contradiction"}),
            key=lambda item: (item.first_seen or "", item.fact_id),
        )
    )
    lines = [
        "# ADR Candidates",
        "",
        "This index lists evidence-backed decision material suitable for human-authored ADRs.",
        "It does not promote extracted material into accepted decisions by itself.",
        "",
    ]
    for index, fact in enumerate(facts[: limits.max_markdown_facts_per_doc], start=1):
        lines.extend(
            [
                f"## ADR-CANDIDATE-{index:04d}",
                "",
                f"- Fact: `{fact.fact_id}`",
                f"- Category: `{fact.category}`",
                f"- Status: `{fact.status}`",
                f"- Confidence: `{fact.confidence:.2f}`",
                f"- First seen: `{fact.first_seen or 'unknown'}`",
                f"- Evidence: {_provenance_label(fact.evidence[0] if fact.evidence else None)}",
                "",
                fact.statement,
                "",
            ]
        )
    if len(facts) > limits.max_markdown_facts_per_doc:
        lines.append(f"{len(facts) - limits.max_markdown_facts_per_doc} additional candidates are in `../Graph/facts/index.json`.")
        lines.append("")
    return "\n".join(lines)


def _render_timeline(result: MiningResult) -> str:
    lines = [
        "# Historical Timeline",
        "",
        "Chronological index of conversations in the provided export shards.",
        "",
    ]
    for event in result.timeline:
        lines.append(
            f"- `{event.get('timestamp') or 'unknown'}` `{event['conversation_id']}` "
            f"{event['title']} ({event['message_count']} messages; {event['source_file']})"
        )
    lines.append("")
    return "\n".join(lines)


def _render_concept_index(result: MiningResult) -> str:
    lines = ["# Concept Index", "", "Stable concept IDs extracted from historical evidence.", ""]
    for concept in result.concepts:
        lines.extend(
            [
                f"## `{concept.concept_id}`",
                "",
                f"- Name: {concept.name}",
                f"- Status: `{concept.status}`",
                f"- Categories: {', '.join(f'`{item}`' for item in concept.categories)}",
                f"- Evidence count: {concept.evidence_count}",
                f"- First seen: `{concept.first_seen or 'unknown'}`",
                f"- Last seen: `{concept.last_seen or 'unknown'}`",
                "",
            ]
        )
    return "\n".join(lines)


def _render_source_index(result: MiningResult) -> str:
    lines = ["# Source Index", "", "Source files used as evidence. Raw content is not copied.", ""]
    for source in result.source_files:
        lines.extend(
            [
                f"## `{source.name}`",
                "",
                f"- Artifact type: `{source.artifact_type}`",
                f"- Size bytes: {source.size_bytes}",
                f"- SHA-256: `{source.sha256}`",
                "",
            ]
        )
    return "\n".join(lines)


def _render_provenance_index(result: MiningResult) -> str:
    by_conversation: dict[str, set[str]] = {}
    for fact in result.facts:
        for evidence in fact.evidence:
            by_conversation.setdefault(evidence.conversation_id, set()).add(fact.fact_id)
    lines = [
        "# Provenance Index",
        "",
        "Maps source conversations to derived fact IDs. Message-level provenance is in `../Graph/facts/index.json`.",
        "",
    ]
    for conversation_id in sorted(by_conversation):
        fact_ids = sorted(by_conversation[conversation_id])
        lines.append(f"- `{conversation_id}`: {len(fact_ids)} facts")
    lines.append("")
    return "\n".join(lines)


def _fact_to_plain(fact: ExtractedFact) -> dict[str, Any]:
    return {
        "fact_id": fact.fact_id,
        "category": fact.category,
        "statement": fact.statement,
        "normalized_statement": fact.normalized_statement,
        "concept_ids": sorted(fact.concept_ids),
        "first_seen": fact.first_seen,
        "last_seen": fact.last_seen,
        "confidence": fact.confidence,
        "status": fact.status,
        "evolution": sorted(fact.evolution),
        "evidence": [asdict(item) for item in sorted(fact.evidence, key=lambda ev: (ev.timestamp or "", ev.conversation_id, ev.message_id))],
    }


def _source_to_public(source: SourceFile) -> dict[str, Any]:
    return {
        "name": source.name,
        "size_bytes": source.size_bytes,
        "sha256": source.sha256,
        "artifact_type": source.artifact_type,
    }


def _write_chunked_json(parent: Path, stem: str, records: Sequence[Any], chunk_size: int) -> None:
    if chunk_size <= 0:
        raise ExportMiningError("graph chunk size must be greater than zero")
    chunk_dir = parent / stem
    if chunk_dir.exists():
        shutil.rmtree(chunk_dir)
    legacy_file = parent / f"{stem}.json"
    if legacy_file.exists():
        legacy_file.unlink()
    chunk_dir.mkdir(parents=True, exist_ok=True)
    chunks: list[dict[str, Any]] = []
    for index, start in enumerate(range(0, len(records), chunk_size)):
        chunk = records[start : start + chunk_size]
        path = chunk_dir / f"part-{index:04d}.json"
        _write_json(path, chunk)
        chunks.append(
            {
                "path": path.relative_to(parent).as_posix(),
                "record_count": len(chunk),
                "sha256": _file_sha256(path),
            }
        )
    if not records:
        path = chunk_dir / "part-0000.json"
        _write_json(path, [])
        chunks.append({"path": path.relative_to(parent).as_posix(), "record_count": 0, "sha256": _file_sha256(path)})
    _write_json(
        chunk_dir / "index.json",
        {
            "schema": f"wayfinder.export_mining.{stem}.chunks.v1",
            "record_count": len(records),
            "chunk_size": chunk_size,
            "chunk_count": len(chunks),
            "chunks": chunks,
        },
    )


def _build_concepts(facts: Sequence[ExtractedFact]) -> list[GraphConcept]:
    grouped: dict[str, list[ExtractedFact]] = {}
    for fact in facts:
        for concept_id in fact.concept_ids:
            grouped.setdefault(concept_id, []).append(fact)
    concepts: list[GraphConcept] = []
    for concept_id, concept_facts in grouped.items():
        timestamps = [item for fact in concept_facts for item in (fact.first_seen, fact.last_seen) if item]
        categories = tuple(sorted({fact.category for fact in concept_facts}))
        concepts.append(
            GraphConcept(
                concept_id=concept_id,
                name=_name_from_concept_id(concept_id),
                slug=concept_id.removeprefix("concept:"),
                status=_concept_status(concept_facts),
                categories=categories,
                first_seen=min(timestamps) if timestamps else None,
                last_seen=max(timestamps) if timestamps else None,
                evidence_count=sum(len(fact.evidence) for fact in concept_facts),
            )
        )
    return concepts


def _build_relationships(facts: Sequence[ExtractedFact]) -> list[GraphRelationship]:
    relationships: dict[str, GraphRelationship] = {}
    for fact in facts:
        for concept_id in sorted(fact.concept_ids):
            _add_relationship(relationships, "references", fact.fact_id, concept_id, fact.fact_id, fact.confidence)
        for evidence in fact.evidence:
            evidence_id = _stable_id("evidence", evidence.conversation_id, evidence.message_id)
            _add_relationship(relationships, "derived-from", fact.fact_id, evidence_id, fact.fact_id, evidence.confidence)
        if fact.status in {"deprecated", "superseded"}:
            for concept_id in sorted(fact.concept_ids):
                _add_relationship(relationships, "supersedes-or-deprecates", fact.fact_id, concept_id, fact.fact_id, fact.confidence)
        if fact.category == "boundary":
            for concept_id in sorted(fact.concept_ids):
                _add_relationship(relationships, "defines-boundary-for", fact.fact_id, concept_id, fact.fact_id, fact.confidence)
    return list(relationships.values())


def _add_relationship(
    relationships: dict[str, GraphRelationship],
    relationship_type: str,
    source_id: str,
    target_id: str,
    evidence_fact_id: str,
    confidence: float,
) -> None:
    relationship_id = _stable_id("relationship", relationship_type, source_id, target_id, evidence_fact_id)
    relationships[relationship_id] = GraphRelationship(
        relationship_id=relationship_id,
        relationship_type=relationship_type,
        source_id=source_id,
        target_id=target_id,
        evidence_fact_id=evidence_fact_id,
        confidence=confidence,
    )


def _ordered_messages(conversation: Mapping[str, Any]) -> Iterable[Mapping[str, Any]]:
    mapping = conversation.get("mapping")
    if not isinstance(mapping, Mapping):
        return ()
    nodes = {str(key): value for key, value in mapping.items() if isinstance(value, Mapping)}
    children: dict[str | None, list[str]] = {}
    for node_id, node in nodes.items():
        parent = node.get("parent")
        parent_id = str(parent) if parent else None
        children.setdefault(parent_id, []).append(node_id)
    for child_ids in children.values():
        child_ids.sort(key=lambda item: (_message_sort_key(nodes.get(item, {})), item))
    roots = children.get(None, [])
    ordered: list[Mapping[str, Any]] = []
    seen: set[str] = set()
    stack = list(reversed(roots))
    while stack:
        node_id = stack.pop()
        if node_id in seen:
            continue
        seen.add(node_id)
        node = nodes[node_id]
        if isinstance(node.get("message"), Mapping):
            ordered.append(node)
        for child_id in reversed(children.get(node_id, [])):
            stack.append(child_id)
    for node_id, node in sorted(nodes.items(), key=lambda item: (_message_sort_key(item[1]), item[0])):
        if node_id in seen:
            continue
        if isinstance(node.get("message"), Mapping):
            ordered.append(node)
    return tuple(ordered)


def _message_sort_key(node: Mapping[str, Any]) -> tuple[float, str]:
    ts = _message_timestamp(node)
    return (ts if ts is not None else math.inf, str(node.get("id") or ""))


def _message_timestamp(node: Mapping[str, Any]) -> float | None:
    message = node.get("message") if isinstance(node.get("message"), Mapping) else node
    if not isinstance(message, Mapping):
        return None
    for key in ("create_time", "update_time"):
        value = message.get(key)
        if isinstance(value, (int, float)) and math.isfinite(value):
            return float(value)
    return None


def _message_text(message: Mapping[str, Any], max_chars: int) -> str:
    content = message.get("content")
    fragments: list[str] = []
    if isinstance(content, Mapping):
        parts = content.get("parts")
        if isinstance(parts, list):
            for part in parts:
                fragments.extend(_text_fragments(part))
        for key in ("text", "result"):
            value = content.get(key)
            if isinstance(value, str):
                fragments.append(value)
    elif isinstance(content, str):
        fragments.append(content)
    text = "\n".join(fragment.strip() for fragment in fragments if fragment and fragment.strip())
    return text[:max_chars]


def _text_fragments(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, Mapping):
        fragments: list[str] = []
        for key in ("text", "name", "content"):
            inner = value.get(key)
            if isinstance(inner, str):
                fragments.append(inner)
        return fragments
    return []


def _author_role(message: Mapping[str, Any]) -> str | None:
    author = message.get("author")
    if isinstance(author, Mapping):
        role = author.get("role")
        if isinstance(role, str):
            return role
    return None


def _extract_units(text: str, max_unit_chars: int) -> Iterable[str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    raw_units = re.split(r"(?<=[.!?])\s+|\n+", normalized)
    for raw in raw_units:
        unit = _clean_statement(raw)
        if len(unit) < 18:
            continue
        if len(unit) > max_unit_chars:
            unit = unit[:max_unit_chars].rstrip()
        yield unit


def _categories_for_unit(unit: str) -> list[tuple[str, float]]:
    lower = f" {_normalize_space(unit).lower()} "
    categories: list[tuple[str, float]] = []
    for category, markers in CATEGORY_RULES.items():
        for marker in markers:
            needle = marker.lower()
            if needle in lower:
                categories.append((category, 0.68))
                break
    return categories


def _confidence_for_unit(unit: str, category: str, base: float) -> float:
    confidence = base
    if _contains_term(unit, "wayfinder"):
        confidence += 0.12
    if _contains_any_term(unit, CANONICAL_TERMS):
        confidence += 0.10
    if category in {"constitutional_principle", "architectural_decision"}:
        confidence += 0.05
    if len(_concept_ids_for_unit(unit)) >= 2:
        confidence += 0.05
    return min(confidence, 0.98)


def _is_architecture_relevant(unit: str) -> bool:
    return _contains_any_term(unit, RELEVANCE_TERMS)


def _unit_has_architecture_signal(unit: str, title: str) -> bool:
    if _is_architecture_relevant(unit):
        return True
    if _contains_any_term(title, PROJECT_TITLE_TERMS) and _contains_any_term(unit, BROAD_ARCHITECTURE_TERMS):
        return True
    return False


def _concept_ids_for_unit(unit: str) -> set[str]:
    concept_ids: set[str] = set()
    for term in CANONICAL_TERMS:
        if _contains_term(unit, term):
            concept_ids.add(_concept_id(term))
    for match in re.finditer(r"\b[A-Z][A-Za-z0-9]*(?:\s+[A-Z][A-Za-z0-9]*){0,3}\b", unit):
        term = match.group(0).strip()
        if len(term) >= 3 and term.lower() in RELEVANCE_TERMS:
            concept_ids.add(_concept_id(term))
    return concept_ids


def _contains_any_term(value: str, terms: Iterable[str]) -> bool:
    return any(_contains_term(value, term) for term in terms)


def _contains_term(value: str, term: str) -> bool:
    return _term_pattern(term).search(value) is not None


@lru_cache(maxsize=1024)
def _term_pattern(term: str) -> re.Pattern[str]:
    pieces = [re.escape(piece) for piece in _normalize_space(term).lower().split()]
    if not pieces:
        return re.compile(r"a\A")
    pattern = r"\b" + r"\s+".join(pieces) + r"\b"
    return re.compile(pattern, re.IGNORECASE)


def _concept_id(term: str) -> str:
    return f"concept:{_slug(term)}"


def _status_for_unit(unit: str) -> str:
    lower = unit.lower()
    if "deprecated" in lower or "obsolete" in lower:
        return "deprecated"
    if "superseded" in lower or "replaced by" in lower:
        return "superseded"
    if "accepted" in lower or "canonical" in lower or "promoted" in lower:
        return "accepted"
    if "open question" in lower or "todo" in lower or "future work" in lower:
        return "open"
    return "observed"


def _evolution_marker(unit: str) -> str | None:
    lower = unit.lower()
    for marker in ("renamed", "rename", "deprecated", "superseded", "replaced by", "merged", "split"):
        if marker in lower:
            return marker
    return None


def _concept_status(facts: Sequence[ExtractedFact]) -> str:
    statuses = {fact.status for fact in facts}
    if "accepted" in statuses:
        return "accepted"
    if "deprecated" in statuses:
        return "deprecated"
    if "superseded" in statuses:
        return "superseded"
    return "observed"


def _seen_range(first_seen: str | None, last_seen: str | None, timestamp: str | None) -> tuple[str | None, str | None]:
    if not timestamp:
        return first_seen, last_seen
    new_first = timestamp if not first_seen else min(first_seen, timestamp)
    new_last = timestamp if not last_seen else max(last_seen, timestamp)
    return new_first, new_last


def _classify_source_file(name: str) -> str:
    lower = name.lower()
    if _is_conversation_file(name):
        return "ConversationShard"
    if "library_files" in lower:
        return "LibraryFiles"
    if "message_feedback" in lower:
        return "MessageFeedback"
    if "shared_conversations" in lower:
        return "SharedConversationIndex"
    if re.match(r"user\s*\(", lower) or lower == "user.json":
        return "UserProfile"
    if "user_settings" in lower:
        return "UserSettings"
    if lower.endswith(".dat"):
        return "ConversationAssetBlob"
    if "manifest" in lower:
        return "ExportManifest"
    if "asset" in lower:
        return "AssetIndex"
    return "JsonArtifact"


def _is_conversation_file(name: str) -> bool:
    return bool(re.match(r"conversations-\d+.*\.json$", name.lower()))


def _load_json_array(path: Path, max_file_bytes: int) -> list[Any]:
    if path.stat().st_size > max_file_bytes:
        raise ExportMiningError(f"JSON file exceeds configured maximum: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ExportMiningError(f"invalid JSON: {path}") from exc
    if not isinstance(data, list):
        raise ExportMiningError(f"expected JSON array: {path}")
    return data


def _file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stable_hash(parts: Iterable[str]) -> str:
    digest = sha256()
    for part in sorted(parts):
        digest.update(part.encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def _stable_id(prefix: str, *parts: str) -> str:
    digest = sha256()
    for part in parts:
        digest.update(str(part).encode("utf-8"))
        digest.update(b"\0")
    return f"{prefix}:{digest.hexdigest()[:24]}"


def _normalize_statement(value: str) -> str:
    return _normalize_space(_clean_statement(value)).lower()


def _clean_statement(value: str) -> str:
    cleaned = re.sub(r"^[-*•\d.)\s]+", "", value.strip())
    cleaned = cleaned.replace("\u2014", "-").replace("\u2013", "-").replace("\u2019", "'")
    cleaned = _redact_local_paths(cleaned)
    return _normalize_space(cleaned)


def _clean_inline(value: str) -> str:
    return _normalize_space(_redact_local_paths(value).replace("|", "/"))


def _redact_local_paths(value: str) -> str:
    redacted = re.sub(
        r"/mnt/c/Users/<user>/\s)]+/OneDrive/Documents/Wayfinder/",
        "",
        value,
        flags=re.IGNORECASE,
    )
    redacted = re.sub(
        r"C:[/\\]Users[/\\][^/\\\s)]+[/\\]OneDrive[/\\]Documents[/\\]Wayfinder[/\\]",
        "",
        redacted,
        flags=re.IGNORECASE,
    )
    redacted = re.sub(r"/mnt/c/Users/<user>", "[local-path]", redacted, flags=re.IGNORECASE)
    redacted = re.sub(r"%USERPROFILE%\s,;:`]+", "[local-path]", redacted, flags=re.IGNORECASE)
    redacted = re.sub(r"%USERPROFILE%\s,;:`]+", "[local-path]", redacted, flags=re.IGNORECASE)
    return redacted


def _normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "unknown"


def _name_from_concept_id(concept_id: str) -> str:
    return _title_from_slug(concept_id.removeprefix("concept:"))


def _title_from_slug(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").title()


def _iso_timestamp(value: float | None) -> str | None:
    if value is None:
        return None
    timestamp = value / 1000 if value > 100_000_000_000 else value
    try:
        return datetime.fromtimestamp(timestamp, tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    except (OverflowError, OSError, ValueError):
        return None


def _provenance_label(evidence: EvidenceRef | None) -> str:
    if evidence is None:
        return "`unknown`"
    return (
        f"`conversation:{evidence.conversation_id}` "
        f"`message:{evidence.message_id}` "
        f"`timestamp:{evidence.timestamp or 'unknown'}` "
        f"`file:{evidence.source_file}`"
    )


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_text(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8")


def _check_count(name: str, value: int, limit: int) -> None:
    if value > limit:
        raise ExportMiningError(f"{name} exceeds configured maximum: {value} > {limit}")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mine Wayfinder architecture knowledge from ChatGPT export JSON.")
    parser.add_argument("--input", action="append", default=(), help="Input JSON file or directory. Repeatable.")
    parser.add_argument("--output", required=True, help="Knowledge output directory.")
    parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES)
    parser.add_argument("--max-file-bytes", type=int, default=DEFAULT_MAX_FILE_BYTES)
    parser.add_argument("--max-conversations", type=int, default=DEFAULT_MAX_CONVERSATIONS)
    parser.add_argument("--max-messages", type=int, default=DEFAULT_MAX_MESSAGES)
    parser.add_argument("--max-facts", type=int, default=DEFAULT_MAX_FACTS)
    parser.add_argument("--max-text-chars", type=int, default=DEFAULT_MAX_TEXT_CHARS)
    parser.add_argument("--max-unit-chars", type=int, default=DEFAULT_MAX_UNIT_CHARS)
    parser.add_argument("--max-markdown-facts-per-doc", type=int, default=DEFAULT_MAX_MARKDOWN_FACTS_PER_DOC)
    parser.add_argument("--graph-chunk-size", type=int, default=DEFAULT_GRAPH_CHUNK_SIZE)
    parser.add_argument(
        "--input-manifest",
        action="append",
        default=[],
        help="Text or JSON file containing input paths. Repeatable. Lines beginning with # are ignored.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    limits = MiningLimits(
        max_files=args.max_files,
        max_file_bytes=args.max_file_bytes,
        max_conversations=args.max_conversations,
        max_messages=args.max_messages,
        max_facts=args.max_facts,
        max_text_chars=args.max_text_chars,
        max_unit_chars=args.max_unit_chars,
        max_markdown_facts_per_doc=args.max_markdown_facts_per_doc,
        graph_chunk_size=args.graph_chunk_size,
    )
    miner = WayfinderExportMiner(limits=limits)
    input_paths = [Path(item) for item in args.input]
    for manifest_path in args.input_manifest:
        input_paths.extend(_load_input_manifest(Path(manifest_path)))
    if not input_paths:
        raise ExportMiningError("at least one --input or --input-manifest path is required")
    result = miner.mine_paths(tuple(input_paths))
    write_knowledge_base(result, Path(args.output), limits=limits)
    print(
        json.dumps(
            {
                "status": "ok",
                "source_hash": result.source_hash,
                "conversations": result.conversation_count,
                "messages": result.message_count,
                "facts": result.fact_count,
                "concepts": result.concept_count,
                "relationships": result.relationship_count,
                "output": str(Path(args.output)),
            },
            sort_keys=True,
        )
    )
    return 0


def _load_input_manifest(path: Path) -> list[Path]:
    if not path.exists():
        raise ExportMiningError(f"input manifest does not exist: {path}")
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if stripped.startswith("["):
        data = json.loads(text)
        if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
            raise ExportMiningError(f"input manifest must be a JSON array of paths: {path}")
        return [Path(item) for item in data]
    paths: list[Path] = []
    for line in text.splitlines():
        item = line.strip()
        if not item or item.startswith("#"):
            continue
        paths.append(Path(item))
    return paths


if __name__ == "__main__":
    raise SystemExit(main())
