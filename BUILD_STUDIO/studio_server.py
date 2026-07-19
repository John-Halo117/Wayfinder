#!/usr/bin/env python3
"""Build Bible Studio local server.

This server owns no canonical data. It builds bounded in-memory indexes from
BUILD_BIBLE and BUILD_OPERATIONS on demand.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import posixpath
import re
import subprocess
import sys
import time
import traceback
from dataclasses import asdict, dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from typing import Any, Callable
from urllib.parse import parse_qs, unquote, urlparse

import aurora_core

REPO_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = Path(__file__).resolve().parent
STATIC_ROOT = APP_ROOT / "static"
TEXT_SUFFIXES = {".md", ".json", ".txt", ".yaml", ".yml"}
DEFAULT_SOURCE_ROOTS = ("BUILD_BIBLE", "BUILD_OPERATIONS")
DEFAULT_MAX_FILES = 2500
DEFAULT_MAX_FILE_BYTES = 750_000
DEFAULT_MAX_SEARCH_RESULTS = 80
DEFAULT_MAX_GRAPH_NODES = 180
DEFAULT_CACHE_TTL_SECONDS = 2.0


@dataclass(frozen=True)
class StudioConfig:
    repo_root: Path = REPO_ROOT
    static_root: Path = STATIC_ROOT
    source_roots: tuple[str, ...] = DEFAULT_SOURCE_ROOTS
    max_files: int = DEFAULT_MAX_FILES
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES
    max_search_results: int = DEFAULT_MAX_SEARCH_RESULTS
    max_graph_nodes: int = DEFAULT_MAX_GRAPH_NODES
    cache_ttl_seconds: float = DEFAULT_CACHE_TTL_SECONDS
    git_timeout_seconds: float = 15.0
    debug: bool = False

    def validate(self) -> None:
        if self.max_files < 1:
            raise ValueError("max_files must be positive")
        if self.max_file_bytes < 1024:
            raise ValueError("max_file_bytes must be at least 1024")
        if self.max_search_results < 1:
            raise ValueError("max_search_results must be positive")
        if self.max_graph_nodes < 1:
            raise ValueError("max_graph_nodes must be positive")
        if self.cache_ttl_seconds < 0:
            raise ValueError("cache_ttl_seconds cannot be negative")


@dataclass
class IndexCache:
    value: dict[str, Any] | None = None
    created_at: float = 0.0
    signature: str = ""


@dataclass
class StudioState:
    config: StudioConfig
    cache: IndexCache = field(default_factory=IndexCache)


STATE = StudioState(config=StudioConfig())
sys.modules.setdefault("studio_server", sys.modules[__name__])


@dataclass(frozen=True)
class ClientError(Exception):
    status: int
    code: str
    reason: str
    context: dict[str, Any]
    recoverable: bool


@dataclass(frozen=True)
class Document:
    id: str
    path: str
    root: str
    layer: str
    title: str
    suffix: str
    size: int
    modified: float
    headings: list[str]
    links: list[dict[str, str]]
    text: str


@dataclass(frozen=True)
class RepositoryRecord:
    id: str
    name: str
    path: str
    kind: str
    exists: bool
    health: str
    relationships: list[str]
    dependencies: list[str]
    compatibility: str
    recent: bool


@dataclass(frozen=True)
class WorkspaceRecord:
    id: str
    name: str
    repositories: list[str]
    layout: dict[str, Any]
    preferences: dict[str, Any]


@dataclass(frozen=True)
class EventRecord:
    id: str
    type: str
    timestamp: float
    source: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class EngineeringObject:
    id: str
    kind: str
    title: str
    path: str
    source_pattern: str
    fields: dict[str, Any]


def safe_relative(path: Path) -> str:
    return path.relative_to(STATE.config.repo_root).as_posix()


def is_allowed_source_path(candidate: Path) -> bool:
    for root_name in STATE.config.source_roots:
        root = (STATE.config.repo_root / root_name).resolve()
        try:
            candidate.relative_to(root)
            return True
        except ValueError:
            continue
    return False


def doc_id(path: str) -> str:
    return "doc:" + path.lower().replace("/", ":").replace(".", "-")


def layer_for(path: str) -> str:
    parts = path.split("/")
    if len(parts) < 2:
        return "root"
    if parts[0] == "BUILD_OPERATIONS":
        return "operations"
    if parts[0] != "BUILD_BIBLE":
        return "external"
    if len(parts) == 2:
        return "root"
    return parts[1]


def read_text(path: Path) -> str:
    data = path.read_bytes()[:STATE.config.max_file_bytes]
    return data.decode("utf-8", errors="replace")


def markdown_links(text: str) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for match in pattern.finditer(text):
        label = match.group(1).strip()
        target = match.group(2).split("#", 1)[0].strip()
        if target and "://" not in target and not target.startswith("mailto:"):
            links.append({"label": label, "target": target})
    return links


def parse_document(path: Path) -> Document | None:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return None
    stat = path.stat()
    if stat.st_size > STATE.config.max_file_bytes:
        return None
    rel = safe_relative(path)
    text = read_text(path)
    headings = [
        line.lstrip("#").strip()
        for line in text.splitlines()
        if line.startswith("#")
    ]
    title = headings[0] if headings else path.name
    return Document(
        id=doc_id(rel),
        path=rel,
        root=rel.split("/", 1)[0],
        layer=layer_for(rel),
        title=title,
        suffix=path.suffix.lower(),
        size=stat.st_size,
        modified=stat.st_mtime,
        headings=headings[:40],
        links=markdown_links(text),
        text=text,
    )


def source_files() -> list[Path]:
    files: list[Path] = []
    for root_name in STATE.config.source_roots:
        root = STATE.config.repo_root / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if len(files) >= STATE.config.max_files:
                return files
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                files.append(path)
    return sorted(files)


def build_index() -> dict[str, Any]:
    docs = load_documents()
    by_path = {doc.path: doc for doc in docs}
    tree = build_tree(docs)
    graph = build_graph(docs, by_path)
    validation = validate_repository(docs, by_path)
    layers: dict[str, int] = {}
    for doc in docs:
        layers[doc.layer] = layers.get(doc.layer, 0) + 1
    return {
        "summary": {
            "documents": len(docs),
            "roots": list(STATE.config.source_roots),
            "layers": layers,
            "maxFiles": STATE.config.max_files,
            "maxFileBytes": STATE.config.max_file_bytes,
            "cacheTtlSeconds": STATE.config.cache_ttl_seconds,
            "generatedAt": time.time(),
        },
        "documents": [document_payload(doc) for doc in docs],
        "tree": tree,
        "graph": graph,
        "validation": validation,
        "compiler": compiler_status(docs),
        "reports": report_status(docs, validation),
        "git": git_status(),
        "extensions": extension_surfaces(),
        "platform": platform_summary(),
    }


def repository_signature() -> str:
    digest = hashlib.sha256()
    for path in source_files():
        try:
            stat = path.stat()
        except OSError:
            continue
        digest.update(safe_relative(path).encode("utf-8"))
        digest.update(str(stat.st_mtime_ns).encode("ascii"))
        digest.update(str(stat.st_size).encode("ascii"))
    return digest.hexdigest()


def get_index(force: bool = False) -> dict[str, Any]:
    now = time.time()
    signature = repository_signature()
    cache = STATE.cache
    is_fresh = (
        cache.value is not None
        and cache.signature == signature
        and (now - cache.created_at) <= STATE.config.cache_ttl_seconds
    )
    if not force and is_fresh:
        return cache.value
    value = build_index()
    cache.value = value
    cache.created_at = now
    cache.signature = signature
    return value


def load_documents() -> list[Document]:
    return [doc for path in source_files() if (doc := parse_document(path))]


def document_payload(doc: Document) -> dict[str, Any]:
    payload = asdict(doc)
    payload["excerpt"] = excerpt(doc.text)
    payload.pop("text")
    return payload


def excerpt(text: str) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    return clean[:260]


def build_tree(docs: list[Document]) -> dict[str, Any]:
    root: dict[str, Any] = {"name": "workspace", "path": "", "children": {}}
    for doc in docs:
        node = root
        parts = doc.path.split("/")
        for part in parts:
            children = node.setdefault("children", {})
            node = children.setdefault(part, {"name": part, "path": "", "children": {}})
        node["path"] = doc.path
        node["id"] = doc.id
        node["layer"] = doc.layer
        node["title"] = doc.title
    return compact_tree(root)


def compact_tree(node: dict[str, Any]) -> dict[str, Any]:
    children = node.get("children", {})
    return {
        key: value
        for key, value in {
            "name": node.get("name"),
            "path": node.get("path", ""),
            "id": node.get("id"),
            "layer": node.get("layer"),
            "title": node.get("title"),
            "children": [compact_tree(child) for child in children.values()],
        }.items()
        if value not in (None, "", [])
    }


def resolve_link(source_path: str, target: str) -> str:
    if not target or target.startswith("/") or "://" in target:
        return ""
    source_dir = posixpath.dirname(source_path)
    normalized = posixpath.normpath(posixpath.join(source_dir, target))
    if normalized == "." or normalized.startswith("../") or normalized == "..":
        return ""
    return normalized


def infer_relationship(label: str, source_text: str, target: str) -> str:
    probe = f"{label} {target} {source_text}".lower()
    rules = [
        ("implements", "implement"),
        ("depends_on", "depend"),
        ("composes", "compos"),
        ("extends", "extend"),
        ("specializes", "special"),
        ("supersedes", "supersed"),
        ("requires", "requir"),
        ("provides", "provid"),
        ("generated_from", "generated"),
        ("verified_by", "verif"),
        ("reviewed_by", "review"),
    ]
    for rel, marker in rules:
        if marker in probe:
            return rel
    return "references"


def build_graph(docs: list[Document], by_path: dict[str, Document]) -> dict[str, Any]:
    nodes = [
        {"id": doc.id, "path": doc.path, "title": doc.title, "layer": doc.layer}
        for doc in docs[:STATE.config.max_graph_nodes]
    ]
    allowed = {node["id"] for node in nodes}
    edges: list[dict[str, str]] = []
    for doc in docs:
        if doc.id not in allowed:
            continue
        for link in doc.links:
            target_path = resolve_link(doc.path, link["target"])
            target_doc = by_path.get(target_path)
            if not target_doc or target_doc.id not in allowed:
                continue
            edges.append({
                "source": doc.id,
                "target": target_doc.id,
                "type": infer_relationship(link["label"], doc.text[:500], link["target"]),
                "label": link["label"],
            })
            if len(edges) >= STATE.config.max_graph_nodes * 3:
                break
    return {"nodes": nodes, "edges": edges}


def validate_repository(docs: list[Document], by_path: dict[str, Document]) -> dict[str, Any]:
    diagnostics: list[dict[str, str]] = []
    for doc in docs:
        for link in doc.links:
            target = resolve_link(doc.path, link["target"])
            if not target or target not in by_path:
                diagnostics.append(diag("BBREF-001", "error", doc.path, f"Broken local reference: {link['target']}"))
        if doc.suffix == ".json":
            try:
                json.loads(doc.text)
            except json.JSONDecodeError as exc:
                diagnostics.append(diag("BBSCHEMA-001", "error", doc.path, f"Invalid JSON: {exc.msg}"))
        if doc.layer == "doctrine" and re.search(r"\b(my house|my property|sq ft|moat)\b", doc.text, re.I):
            diagnostics.append(diag("BBLAYER-001", "error", doc.path, "Property-specific fact appears in doctrine."))
        if doc.path.startswith("BUILD_BIBLE/generation/") and "Canonical: yes" in doc.text:
            diagnostics.append(diag("BBGEN-001", "error", doc.path, "Generated artifact treated as canonical."))
    for root_name in STATE.config.source_roots:
        root = STATE.config.repo_root / root_name
        if not root.exists():
            diagnostics.append(diag("BBROOT-001", "warning", root_name, "Source root does not exist."))
            continue
        for directory, _, _ in os.walk(root):
            readme = Path(directory) / "README.md"
            if not readme.exists():
                diagnostics.append(diag("BBREADME-001", "warning", safe_relative(Path(directory)), "Directory has no README.md."))
    counts: dict[str, int] = {}
    for item in diagnostics:
        counts[item["severity"]] = counts.get(item["severity"], 0) + 1
    return {"diagnostics": diagnostics[:300], "counts": counts, "status": "passed" if not counts.get("error") else "failed"}


def diag(rule: str, severity: str, path: str, message: str) -> dict[str, str]:
    return {"rule": rule, "severity": severity, "path": path, "message": message}


def compiler_status(docs: list[Document]) -> dict[str, Any]:
    pipeline = CompilerService().pipeline()
    return {
        "status": pipeline["status"],
        "message": "Compiler pipeline interfaces are ready; artifact backends are explicit extension slots.",
        "targets": pipeline["stages"],
        "documentCount": len(docs),
    }


def report_status(docs: list[Document], validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "repositoryHealth": validation["status"],
        "documentCount": len(docs),
        "validationDiagnostics": len(validation["diagnostics"]),
        "coverage": {
            "doctrine": count_layer(docs, "doctrine"),
            "contracts": count_layer(docs, "contracts"),
            "schemas": count_layer(docs, "schemas"),
            "patterns": len([doc for doc in docs if "pattern" in doc.path.lower()]),
            "operations": count_layer(docs, "operations"),
        },
    }


def count_layer(docs: list[Document], layer: str) -> int:
    return sum(1 for doc in docs if doc.layer == layer)


def git_status() -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=STATE.config.repo_root,
            check=False,
            text=True,
            capture_output=True,
            timeout=STATE.config.git_timeout_seconds,
        )
    except Exception as exc:  # noqa: BLE001
        return {"available": False, "error": str(exc), "entries": []}
    entries = [line for line in result.stdout.splitlines() if line.strip()]
    return {"available": result.returncode == 0, "entries": entries[:200]}


def extension_surfaces() -> dict[str, Any]:
    return {
        "pluginManager": [slot["name"] for slot in PluginService().manifest()["availableSlots"]],
        "aiGateway": [provider["name"] for provider in AIService().providers()["providers"]],
        "jarvisInterface": JarvisService().interface()["capabilities"],
    }


def platform_summary() -> dict[str, Any]:
    return {
        "services": service_catalog()["services"],
        "workspace": WorkspaceService().current_workspace(),
        "repositories": RepositoryService().registry()["repositories"],
        "property": PropertyService().model(),
        "events": EVENT_BUS.recent(12),
    }


def search_documents(docs: list[Document], query: str) -> list[dict[str, Any]]:
    terms = expand_query(query)
    if not terms:
        return [document_payload(doc) for doc in docs[:STATE.config.max_search_results]]
    scored: list[tuple[int, Document]] = []
    for doc in docs:
        doc_text = document_text_for_search(doc)
        score = 0
        for term in terms:
            if term in doc_text:
                score += 1
            if term in doc.title.lower():
                score += 3
            if term in doc.path.lower():
                score += 2
        if score:
            scored.append((score, doc))
    scored.sort(key=lambda item: (-item[0], item[1].path))
    return [document_payload(doc) | {"score": score} for score, doc in scored[:STATE.config.max_search_results]]


def health_payload() -> dict[str, Any]:
    roots = [
        {"name": root, "exists": (STATE.config.repo_root / root).exists()}
        for root in STATE.config.source_roots
    ]
    return {
        "status": "ok" if all(root["exists"] for root in roots) else "degraded",
        "service": "Build Bible Studio",
        "version": "0.3.0",
        "roots": roots,
        "limits": {
            "maxFiles": STATE.config.max_files,
            "maxFileBytes": STATE.config.max_file_bytes,
            "maxSearchResults": STATE.config.max_search_results,
            "maxGraphNodes": STATE.config.max_graph_nodes,
        },
    }


def expand_query(query: str) -> list[str]:
    base = [term for term in re.split(r"[^a-z0-9-]+", query.lower()) if term]
    expansions = {
        "wet": ["wet", "wet-area", "bathroom", "laundry", "mudroom", "greenhouse", "waterproof"],
        "room": ["room", "space", "spine"],
        "drainage": ["drainage", "stormwater", "rainwater", "water movement"],
        "potable": ["potable", "water"],
        "water": ["water", "rainwater", "greywater", "drainage"],
        "compile": ["compiler", "generation", "generated"],
    }
    terms = list(base)
    for term in base:
        terms.extend(expansions.get(term, []))
    return sorted(set(terms))


def document_text_for_search(doc: Document) -> str:
    return " ".join([
        doc.title,
        doc.path,
        doc.layer,
        " ".join(doc.headings),
        doc.text,
    ]).lower()


class EventBus:
    def __init__(self) -> None:
        self._events: list[EventRecord] = []
        self._next_id = 1
        self._lock = Lock()

    def publish(self, event_type: str, source: str, payload: dict[str, Any]) -> EventRecord:
        with self._lock:
            event = EventRecord(
                id=f"event-{self._next_id}",
                type=event_type,
                timestamp=time.time(),
                source=source,
                payload=payload,
            )
            self._next_id += 1
            self._events.append(event)
            self._events = self._events[-200:]
            return event

    def recent(self, limit: int = 50) -> list[dict[str, Any]]:
        bounded_limit = max(0, min(limit, 200))
        with self._lock:
            return [asdict(event) for event in self._events[-bounded_limit:]]


EVENT_BUS = EventBus()


class RepositoryService:
    def registry(self) -> dict[str, Any]:
        records: list[RepositoryRecord] = []
        known = [
            ("wayfinder", "Wayfinder", ".", "platform"),
            ("build-bible", "Build Bible", "BUILD_BIBLE", "canonical-source"),
            ("build-operations", "Build Operations", "BUILD_OPERATIONS", "operations"),
            ("build-studio", "Aurora Studio", "BUILD_STUDIO", "engineering-ide"),
            ("ark", "ARK", "engines/ark", "engine"),
            ("foundry", "Foundry", "engines/foundry", "engine"),
        ]
        for repo_id, name, rel_path, kind in known:
            path = STATE.config.repo_root / rel_path
            exists = path.exists()
            records.append(RepositoryRecord(
                id=repo_id,
                name=name,
                path=rel_path,
                kind=kind,
                exists=exists,
                health="ok" if exists else "missing",
                relationships=self.relationships_for(repo_id),
                dependencies=self.dependencies_for(repo_id),
                compatibility="p6-service-api",
                recent=exists and rel_path in STATE.config.source_roots,
            ))
        EVENT_BUS.publish("RepositoryRegistryRead", "RepositoryService", {"count": len(records)})
        return {"repositories": [asdict(record) for record in records]}

    @staticmethod
    def relationships_for(repo_id: str) -> list[str]:
        relationships = {
            "wayfinder": ["hosts-build-bible", "hosts-build-studio"],
            "build-bible": ["canonical-source-for-property", "consumed-by-studio"],
            "build-operations": ["operates-property", "references-build-bible"],
            "build-studio": ["indexes-build-bible", "front-end-for-compiler"],
            "ark": ["future-validation-engine"],
            "foundry": ["future-knowledge-workflow"],
        }
        return relationships.get(repo_id, [])

    @staticmethod
    def dependencies_for(repo_id: str) -> list[str]:
        dependencies = {
            "build-operations": ["build-bible"],
            "build-studio": ["build-bible", "build-operations"],
            "ark": ["wayfinder"],
            "foundry": ["wayfinder"],
        }
        return dependencies.get(repo_id, [])


class WorkspaceService:
    def current_workspace(self) -> dict[str, Any]:
        registry = RepositoryService().registry()["repositories"]
        repositories = [repo["id"] for repo in registry if repo["exists"]]
        workspace = WorkspaceRecord(
            id="workspace-local",
            name="Local Aurora Workspace",
            repositories=repositories,
            layout={
                "primary": "BUILD_BIBLE",
                "secondary": "BUILD_OPERATIONS",
                "tool": "BUILD_STUDIO",
                "panes": ["explorer", "search", "graph", "validation", "compiler", "git"],
            },
            preferences={
                "localFirst": True,
                "hiddenCanonicalState": False,
                "offlineCapable": True,
            },
        )
        EVENT_BUS.publish("WorkspaceLoaded", "WorkspaceService", {"id": workspace.id, "repositories": len(repositories)})
        return asdict(workspace)


class CompilerService:
    def pipeline(self) -> dict[str, Any]:
        stages = [
            "Validation",
            "Relationship Resolution",
            "Composition",
            "Dependency Analysis",
            "Generation Planning",
            "CAD",
            "BIM",
            "BOM",
            "Inspection Packages",
            "Maintenance Packages",
            "Digital Twin",
        ]
        EVENT_BUS.publish("CompilerPipelineRead", "CompilerService", {"stages": len(stages)})
        return {
            "status": "architecture-ready",
            "replaceableBackends": True,
            "stages": [
                {"name": stage, "state": "interface-ready" if index < 5 else "backend-slot"}
                for index, stage in enumerate(stages)
            ],
        }

    def plan_compile(self, target: str = "Digital Twin") -> dict[str, Any]:
        pipeline = self.pipeline()
        EVENT_BUS.publish("CompilerPlanCreated", "CompilerService", {"target": target, "state": "planned"})
        return {
            "target": target,
            "status": "planned",
            "pipeline": pipeline,
            "artifacts": [],
            "message": "Compiler orchestration is ready; backend artifact generation is available through extension slots.",
        }


class PluginService:
    def manifest(self) -> dict[str, Any]:
        plugins = [
            "CAD",
            "BIM",
            "GIS",
            "Scheduling",
            "Simulation",
            "Rendering",
            "Cost Estimation",
            "Weather",
            "Home Assistant",
            "ESPHome",
            "Networking",
            "Digital Twin Visualization",
            "Inspection",
            "Reporting",
        ]
        return {
            "apiVersion": "p6-service-api",
            "loaded": [],
            "availableSlots": [{"name": plugin, "state": "extension-slot"} for plugin in plugins],
            "contract": "Plugins communicate through stable service APIs and receive no privileged repository access.",
        }


class AIService:
    def providers(self) -> dict[str, Any]:
        return {
            "contract": "Provider-independent engineering interface",
            "activeProvider": None,
            "providers": [
                {"name": "OpenAI", "state": "provider-slot"},
                {"name": "Ollama", "state": "provider-slot"},
                {"name": "Local Models", "state": "provider-slot"},
                {"name": "Wayfinder Specialists", "state": "future-provider"},
                {"name": "Jarvis", "state": "future-client"},
            ],
            "operations": ["search", "review", "validate", "compile", "navigate"],
        }


class JarvisService:
    def interface(self) -> dict[str, Any]:
        return {
            "implemented": False,
            "access": "unprivileged-engineering-client",
            "capabilities": [
                "search_repositories",
                "instantiate_patterns",
                "validate_changes",
                "run_architectural_reviews",
                "generate_reports",
                "compile_artifacts",
                "navigate_dependencies",
                "review_git_changes",
                "open_engineering_decision_records",
            ],
            "security": "Jarvis uses the same public Studio APIs as other clients.",
        }


class PropertyService:
    def model(self) -> dict[str, Any]:
        object_types = [
            "Property",
            "Building",
            "Room",
            "Utility",
            "Equipment",
            "Infrastructure",
            "Asset",
            "Land",
            "Agriculture",
            "Vehicle",
            "Reality Record",
            "Generated Artifact",
        ]
        return {
            "status": "interface-ready",
            "repositorySupport": "Property repositories instantiate Build Bible patterns.",
            "objectTypes": object_types,
            "objectContract": [
                "identity",
                "purpose",
                "capabilities",
                "interfaces",
                "dependencies",
                "resources",
                "reliability",
                "maintenance",
                "lifecycle",
                "verification",
                "history",
                "digitalTwin",
            ],
        }

    def navigator(self, object_id: str | None = None) -> dict[str, Any]:
        return {
            "objectId": object_id,
            "panels": [
                "documentation",
                "dependencies",
                "composition",
                "relationships",
                "validation",
                "metrics",
                "failures",
                "maintenance",
                "generatedArtifacts",
                "gitHistory",
                "digitalTwin",
                "relatedEDRs",
            ],
        }


class DigitalTwinService:
    def interface(self) -> dict[str, Any]:
        return {
            "status": "interface-ready",
            "ownsReality": False,
            "canonicalSources": ["BUILD_BIBLE", "BUILD_OPERATIONS", "property repositories"],
            "records": [
                "identity",
                "spatialAddress",
                "capabilities",
                "constraints",
                "interfaces",
                "resourceFlows",
                "dependencies",
                "health",
                "maintenance",
                "serviceHistory",
                "lastVerifiedReality",
            ],
            "exports": ["graph", "inspection model", "asset register", "maintenance schedule"],
        }


class InstantiationService:
    def workflow(self) -> dict[str, Any]:
        steps = [
            "select_pattern",
            "select_property_repository",
            "configure_parameters",
            "generate_specification",
            "validate",
            "review",
            "commit",
        ]
        return {
            "status": "workflow-designed",
            "writesCanonicalData": False,
            "steps": steps,
            "traceability": ["pattern", "doctrine", "contracts", "schemas", "EDRs", "verification"],
        }

    def preview(self, pattern_path: str, property_repo: str) -> dict[str, Any]:
        pattern = normalized_param(pattern_path, "pattern", 240)
        property_id = normalized_param(property_repo, "property", 120)
        if not pattern.startswith("BUILD_BIBLE/"):
            raise ClientError(400, "INVALID_PATTERN_PATH", "Pattern path must be inside BUILD_BIBLE.", {"patternPath": pattern}, True)
        if not re.fullmatch(r"[A-Za-z0-9_.\-/]+", property_id):
            raise ClientError(400, "INVALID_PROPERTY_REPOSITORY", "Property repository id contains unsupported characters.", {"propertyRepository": property_id}, True)
        pattern_file = (STATE.config.repo_root / pattern).resolve()
        build_bible_root = (STATE.config.repo_root / "BUILD_BIBLE").resolve()
        try:
            pattern_file.relative_to(build_bible_root)
        except ValueError:
            raise ClientError(400, "INVALID_PATTERN_PATH", "Pattern path must remain inside BUILD_BIBLE.", {"patternPath": pattern}, True)
        if not pattern_file.exists() or pattern_file.suffix.lower() not in TEXT_SUFFIXES:
            raise ClientError(404, "PATTERN_NOT_FOUND", "Pattern source was not found.", {"patternPath": pattern}, True)
        EVENT_BUS.publish("PatternInstantiationPreviewed", "InstantiationService", {"patternPath": pattern, "propertyRepo": property_id})
        return {
            "status": "preview",
            "patternPath": pattern,
            "propertyRepository": property_id,
            "wouldCreate": [
                "property specification record",
                "traceability links",
                "validation task",
                "review task",
            ],
            "committed": False,
        }


class GitService:
    def summary(self) -> dict[str, Any]:
        status = git_status()
        return {
            "status": status,
            "surfaces": ["diffs", "history", "branches", "commits", "engineering reviews", "EDRs", "merge previews", "repository comparisons"],
            "canonicalHistory": "git",
        }

    def branches(self) -> dict[str, Any]:
        result = run_git(["branch", "--list", "--no-color"])
        branches = [line.strip() for line in result.get("stdout", "").splitlines() if line.strip()]
        return {"available": result["available"], "branches": branches[:100], "error": result.get("error")}

    def log(self) -> dict[str, Any]:
        result = run_git(["log", "--oneline", "-20"])
        entries = [line for line in result.get("stdout", "").splitlines() if line.strip()]
        return {"available": result["available"], "entries": entries, "error": result.get("error")}


def run_git(args: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=STATE.config.repo_root,
            check=False,
            text=True,
            capture_output=True,
            timeout=STATE.config.git_timeout_seconds,
        )
    except Exception as exc:  # noqa: BLE001
        return {"available": False, "stdout": "", "stderr": "", "error": str(exc)}
    return {
        "available": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "error": None if result.returncode == 0 else result.stderr.strip(),
    }


def service_catalog() -> dict[str, Any]:
    services = [
        "RepositoryService",
        "WorkspaceService",
        "SearchService",
        "ParserService",
        "IndexService",
        "KnowledgeGraphService",
        "CompilerService",
        "ValidationService",
        "GitService",
        "TaskService",
        "PluginService",
        "AIService",
        "PropertyService",
        "InstantiationService",
        "DigitalTwinService",
    ]
    return {
        "status": "service-oriented",
        "uiIndependent": True,
        "services": [{"name": service, "state": "active" if service in active_services() else "interface-ready"} for service in services],
    }


def active_services() -> set[str]:
    return {
        "RepositoryService",
        "WorkspaceService",
        "SearchService",
        "ParserService",
        "IndexService",
        "KnowledgeGraphService",
        "CompilerService",
        "ValidationService",
        "GitService",
        "PluginService",
        "AIService",
        "PropertyService",
        "InstantiationService",
    }


def platform_payload() -> dict[str, Any]:
    return {
        "serviceCatalog": service_catalog(),
        "repositories": RepositoryService().registry(),
        "workspace": WorkspaceService().current_workspace(),
        "property": PropertyService().model(),
        "instantiation": InstantiationService().workflow(),
        "compiler": CompilerService().pipeline(),
        "digitalTwin": DigitalTwinService().interface(),
        "plugins": PluginService().manifest(),
        "ai": AIService().providers(),
        "jarvis": JarvisService().interface(),
        "git": GitService().summary(),
        "events": EVENT_BUS.recent(),
    }


def aurora_command_payload(command: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    try:
        return aurora_core.execute(command, params or {}, STATE.config)
    except aurora_core.AuroraCommandError as exc:
        raise ClientError(exc.status, exc.code, exc.reason, exc.context, exc.recoverable) from exc


def aurora_command_data(command: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    return aurora_command_payload(command, params)["data"]


def normalized_param(value: str, name: str, max_length: int) -> str:
    normalized = value.strip()
    if not normalized:
        raise ClientError(400, f"MISSING_{name.upper()}", f"{name} is required.", {}, True)
    if len(normalized) > max_length:
        raise ClientError(400, f"{name.upper()}_TOO_LONG", f"{name} exceeds the maximum length.", {"maxLength": max_length}, True)
    return normalized


class StudioHandler(BaseHTTPRequestHandler):
    server_version = "BuildBibleStudio/0.3"

    def do_GET(self) -> None:  # noqa: N802
        self.run_safely(self.route_get)

    def route_get(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path == "/api/health":
            return self.send_json(aurora_command_data("health"))
        if path == "/api/index":
            force = parse_qs(parsed.query).get("force", ["0"])[0] == "1"
            return self.send_json(aurora_command_data("index", {"force": force}))
        if path == "/api/cli":
            params = parse_qs(parsed.query)
            command = params.pop("command", [""])[0]
            command_params = {key: values[-1] for key, values in params.items()}
            return self.send_json(aurora_command_payload(command, command_params))
        if path == "/api/platform":
            return self.send_json(aurora_command_data("platform"))
        if path == "/api/repositories":
            return self.send_json(aurora_command_data("repository.list"))
        if path == "/api/workspace":
            return self.send_json(aurora_command_data("workspace.current"))
        if path == "/api/property":
            return self.send_json(aurora_command_data("property.list"))
        if path == "/api/navigator":
            object_id = parse_qs(parsed.query).get("object", [None])[0]
            return self.send_json(aurora_command_data("property.navigator", {"object": object_id}))
        if path == "/api/instantiate/preview":
            params = parse_qs(parsed.query)
            pattern_path = params.get("pattern", [""])[0]
            property_repo = params.get("property", [""])[0]
            return self.send_json(aurora_command_data("instantiate.preview", {"pattern": pattern_path, "property": property_repo}))
        if path == "/api/compiler":
            return self.send_json(aurora_command_data("compiler.pipeline"))
        if path == "/api/compiler/run":
            target = parse_qs(parsed.query).get("target", ["Digital Twin"])[0]
            return self.send_json(aurora_command_data("compile.plan", {"target": target}))
        if path == "/api/digital-twin":
            return self.send_json(aurora_command_data("digital-twin.status"))
        if path == "/api/plugins":
            return self.send_json(aurora_command_data("plugin.list"))
        if path == "/api/ai":
            return self.send_json(aurora_command_data("ai.providers"))
        if path == "/api/jarvis":
            return self.send_json(aurora_command_data("jarvis.interface"))
        if path == "/api/events":
            return self.send_json(aurora_command_data("events.list"))
        if path == "/api/search":
            query = parse_qs(parsed.query).get("q", [""])[0]
            return self.send_json(aurora_command_data("search", {"query": query}))
        if path == "/api/document":
            rel = parse_qs(parsed.query).get("path", [""])[0]
            return self.send_json(aurora_command_data("document.get", {"path": rel}))
        if path == "/api/validate":
            return self.send_json(aurora_command_data("validate"))
        if path == "/api/git":
            return self.send_json(aurora_command_data("git.status"))
        if path == "/api/git/branches":
            return self.send_json(aurora_command_data("git.branch"))
        if path == "/api/git/log":
            return self.send_json(aurora_command_data("git.history"))
        return self.send_static(path)

    def run_safely(self, handler: Callable[[], None]) -> None:
        try:
            handler()
        except ClientError as exc:
            self.send_json_error(exc.status, exc.code, exc.reason, exc.context, exc.recoverable)
        except Exception as exc:  # noqa: BLE001
            context = {"type": type(exc).__name__}
            if STATE.config.debug:
                context["traceback"] = traceback.format_exc()
            self.send_json_error(500, "INTERNAL_ERROR", "Unexpected server error.", context, False)

    def send_json(self, data: Any) -> None:
        encoded = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(200)
        self.security_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def send_document(self, rel: str) -> None:
        if not rel:
            raise ClientError(400, "MISSING_PATH", "Document path is required.", {}, True)
        candidate = (STATE.config.repo_root / rel).resolve()
        try:
            candidate.relative_to(STATE.config.repo_root)
        except ValueError:
            raise ClientError(403, "PATH_OUTSIDE_REPOSITORY", "Path escapes repository root.", {"path": rel}, False)
        if not is_allowed_source_path(candidate):
            raise ClientError(403, "PATH_NOT_INDEXED_SOURCE", "Path is outside indexed source roots.", {"path": rel}, False)
        if not candidate.exists() or candidate.suffix.lower() not in TEXT_SUFFIXES:
            raise ClientError(404, "DOCUMENT_NOT_FOUND", "Document was not found or is not a supported text file.", {"path": rel}, True)
        self.send_json({"path": safe_relative(candidate), "text": read_text(candidate)})

    def send_static(self, path: str) -> None:
        if path == "/":
            path = "/index.html"
        candidate = (STATE.config.static_root / path.lstrip("/")).resolve()
        try:
            candidate.relative_to(STATE.config.static_root)
        except ValueError:
            raise ClientError(403, "STATIC_PATH_FORBIDDEN", "Static path is forbidden.", {"path": path}, False)
        if not candidate.exists() or not candidate.is_file():
            raise ClientError(404, "STATIC_NOT_FOUND", "Static asset was not found.", {"path": path}, True)
        content = candidate.read_bytes()
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.security_headers()
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store" if candidate.name == "index.html" else "public, max-age=60")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_json_error(self, status: int, code: str, reason: str, context: dict[str, Any], recoverable: bool) -> None:
        encoded = json.dumps({
            "status": "error",
            "error_code": code,
            "reason": reason,
            "context": context,
            "recoverable": recoverable,
        }, indent=2).encode("utf-8")
        self.send_response(status)
        self.security_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'")

    def log_message(self, format: str, *args: Any) -> None:
        print(f"{self.address_string()} - {format % args}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Build Bible Studio.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    parser.add_argument("--check", action="store_true", help="Build the index once and exit.")
    parser.add_argument("--repo-root", default=str(REPO_ROOT), help="Repository root to index.")
    parser.add_argument("--source-root", action="append", dest="source_roots", help="Source root to index; may be repeated.")
    parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES)
    parser.add_argument("--max-file-bytes", type=int, default=DEFAULT_MAX_FILE_BYTES)
    parser.add_argument("--max-search-results", type=int, default=DEFAULT_MAX_SEARCH_RESULTS)
    parser.add_argument("--max-graph-nodes", type=int, default=DEFAULT_MAX_GRAPH_NODES)
    parser.add_argument("--cache-ttl", type=float, default=DEFAULT_CACHE_TTL_SECONDS)
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    source_roots = tuple(args.source_roots or DEFAULT_SOURCE_ROOTS)
    STATE.config = StudioConfig(
        repo_root=repo_root,
        static_root=STATIC_ROOT,
        source_roots=source_roots,
        max_files=args.max_files,
        max_file_bytes=args.max_file_bytes,
        max_search_results=args.max_search_results,
        max_graph_nodes=args.max_graph_nodes,
        cache_ttl_seconds=args.cache_ttl,
        debug=args.debug,
    )
    STATE.config.validate()
    if args.check:
        index = get_index(force=True)
        errors = index["validation"]["counts"].get("error", 0)
        print(json.dumps({
            "documents": index["summary"]["documents"],
            "validation": index["validation"]["status"],
            "errors": errors,
            "health": health_payload()["status"],
        }, indent=2))
        return 1 if errors else 0
    server = ThreadingHTTPServer((args.host, args.port), StudioHandler)
    print(f"Build Bible Studio running at http://{args.host}:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Build Bible Studio.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
