"""Deterministic repository architecture diagnostics for Wayfinder."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Mapping, Sequence

CANONICAL_LAYERS: tuple[str, ...] = (
    "Constitution",
    "Reality",
    "Perception",
    "Observations",
    "ARK",
    "Representations",
    "Focus",
    "Understanding",
    "Missions",
    "Bearings",
    "Reasoning",
    "Navigation",
    "Experiences",
    "Actions",
)

CONSTITUTION_RULES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("reality_before_representation", "Reality before Representation", ("01-reality.md", "05-representations.md")),
    ("representation_before_knowledge", "Representation before Knowledge", ("05-representations.md", "07-understanding.md")),
    ("focus_before_understanding", "Focus before Understanding", ("06-focus.md", "07-understanding.md")),
    ("mission_before_navigation", "Mission before Navigation", ("12-missions.md", "15-navigation.md")),
    ("navigation_before_views", "Navigation before Views", ("15-navigation.md", "16-experiences.md")),
    ("views_before_actions", "Views before Actions", ("16-experiences.md", "17-actions.md")),
    ("actions_affect_reality_only", "Actions affect Reality only", ("17-actions.md", "01-reality.md")),
    ("ai_last", "AI last", ("14-reasoning.md",)),
    ("reuse_before_creation", "Reuse before creation", ("18-cross-cutting.md",)),
    ("deterministic_before_probabilistic", "Deterministic before probabilistic", ("19-dependency-rules.md",)),
    ("composition_before_duplication", "Composition before duplication", ("18-cross-cutting.md",)),
    ("identity_before_representation", "Identity before representation", ("04-ark.md", "05-representations.md")),
    ("capability_before_implementation", "Capability before implementation", ("10-capability-registry.md",)),
    ("theseus_invariant_preservation", "Theseus invariant preservation", ("04-ark.md", "19-dependency-rules.md")),
)

MISSING_ORACLE_DOMAINS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Physical Reality", ("weather", "power", "water", "vision", "audio", "gps", "environment")),
    ("Digital Reality", ("github", "calendar", "filesystem", "email", "home assistant", "media", "inventory")),
    ("Human Reality", ("voice", "chat", "corrections", "manual observations", "preferences")),
)

REPRESENTATION_TERMS: tuple[str, ...] = ("ocr", "embedding", "summary", "metadata", "search", "feature vector")
MISSION_TERMS: tuple[str, ...] = ("mission", "objective", "constraint", "success criteria", "horizon")
NAVIGATION_TERMS: tuple[str, ...] = ("navigation", "recommendation", "opportunity bundle", "tradeoff")
MEDIA_TERMS: tuple[str, ...] = (
    "music",
    "movies",
    "tv",
    "books",
    "photos",
    "games",
    "videos",
    "podcasts",
    "documents",
    "recipes",
    "gis",
)
ROOT_TERMS: tuple[str, ...] = (
    "form",
    "motion",
    "force",
    "energy",
    "boundary",
    "relation",
    "time",
)


@dataclass(frozen=True)
class DoctorConfig:
    """Resource bounds for architecture diagnostics."""

    max_files: int = 25_000
    max_hash_bytes: int = 1_000_000
    max_text_bytes: int = 200_000
    max_duplicate_groups: int = 200
    max_dead_code_candidates: int = 200
    max_candidate_pages: int = 100


@dataclass(frozen=True)
class Finding:
    """A structured diagnostic finding."""

    code: str
    severity: str
    message: str
    path: str | None = None
    details: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class GraphNode:
    """Architecture graph node."""

    node_id: str
    label: str
    layer: str
    purpose: str
    dependencies: tuple[str, ...]
    consumers: tuple[str, ...]
    adrs: tuple[str, ...]
    tests: tuple[str, ...]
    source_directories: tuple[str, ...]


@dataclass(frozen=True)
class DoctorReport:
    """Complete architecture diagnostic result."""

    status: str
    score: int
    findings: tuple[Finding, ...]
    dependency_health: Mapping[str, object]
    repository_health: Mapping[str, object]
    documentation_health: Mapping[str, object]
    capability_health: Mapping[str, object]
    oracle_health: Mapping[str, object]
    reality_health: Mapping[str, object]
    representation_health: Mapping[str, object]
    knowledge_health: Mapping[str, object]
    mission_health: Mapping[str, object]
    navigation_health: Mapping[str, object]
    view_health: Mapping[str, object]
    action_health: Mapping[str, object]
    constitution_validation: Mapping[str, object]
    drift_detection: Mapping[str, object]
    technical_debt: Mapping[str, object]
    repository_timeline: tuple[Mapping[str, object], ...]
    graph_nodes: tuple[GraphNode, ...]
    module_edges: tuple[tuple[str, str], ...]
    package_edges: tuple[tuple[str, str], ...]
    service_edges: tuple[tuple[str, str], ...]
    capability_edges: tuple[tuple[str, str], ...]
    oracle_edges: tuple[tuple[str, str], ...]
    candidate_pages: tuple[Mapping[str, object], ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class ArchitectureDoctor:
    """Scan a Wayfinder repository for architecture governance evidence."""

    def __init__(self, repo_root: Path, config: DoctorConfig | None = None) -> None:
        self.repo_root = repo_root.resolve()
        self.config = config or DoctorConfig()

    def run(self) -> DoctorReport:
        files = self._tracked_files()
        text_cache = self._read_text_cache(files)
        python_files = [path for path in files if path.suffix == ".py" and not _is_legacy(path)]
        import_edges = self._python_import_edges(python_files)
        architecture_nodes = self._architecture_nodes(files, text_cache)
        findings: list[Finding] = []

        dependency_health, dependency_findings = self._dependency_health(python_files, import_edges)
        findings.extend(dependency_findings)
        repository_health, repository_findings = self._repository_health(files, text_cache)
        findings.extend(repository_findings)
        documentation_health, doc_findings = self._documentation_health(files, text_cache)
        findings.extend(doc_findings)
        capability_health, capability_edges = self._capability_health(files, text_cache)
        oracle_health, oracle_edges = self._oracle_health(files, text_cache)
        reality_health = self._coverage_health(text_cache, ("rid", "lvr", "relationship", "provenance", "confidence"))
        representation_health = self._representation_health(files, text_cache)
        knowledge_health = self._knowledge_health(files, text_cache)
        mission_health = self._inventory_health(files, text_cache, MISSION_TERMS, "mission")
        navigation_health = self._inventory_health(files, text_cache, NAVIGATION_TERMS, "navigation")
        view_health = self._view_health(python_files, import_edges)
        action_health = self._action_health(files, text_cache, import_edges)
        constitution_validation, constitution_findings = self._constitution_validation(files, text_cache, import_edges)
        findings.extend(constitution_findings)
        drift_detection, drift_findings = self._drift_detection(files, text_cache, import_edges)
        findings.extend(drift_findings)
        technical_debt = self._technical_debt(repository_health, text_cache)
        timeline = self._repository_timeline(files, text_cache)
        candidate_pages = self._candidate_pages(text_cache)
        service_edges = tuple(sorted(edge for edge in import_edges if edge[0].startswith("services/") or edge[1].startswith("services/")))

        score = _score(findings)
        return DoctorReport(
            status="pass" if not any(item.severity == "error" for item in findings) else "attention",
            score=score,
            findings=tuple(sorted(findings, key=lambda item: (item.severity, item.code, item.path or ""))),
            dependency_health=dependency_health,
            repository_health=repository_health,
            documentation_health=documentation_health,
            capability_health=capability_health,
            oracle_health=oracle_health,
            reality_health=reality_health,
            representation_health=representation_health,
            knowledge_health=knowledge_health,
            mission_health=mission_health,
            navigation_health=navigation_health,
            view_health=view_health,
            action_health=action_health,
            constitution_validation=constitution_validation,
            drift_detection=drift_detection,
            technical_debt=technical_debt,
            repository_timeline=timeline,
            graph_nodes=architecture_nodes,
            module_edges=tuple(sorted(import_edges)),
            package_edges=self._package_edges(import_edges),
            service_edges=service_edges,
            capability_edges=capability_edges,
            oracle_edges=oracle_edges,
            candidate_pages=candidate_pages,
        )

    def write_reports(self, report: DoctorReport, output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "architecture-doctor.json").write_text(
            json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (output_dir / "repository-health-dashboard.md").write_text(render_health_dashboard(report), encoding="utf-8")
        (output_dir / "README.md").write_text(render_governance_index(), encoding="utf-8")
        (output_dir / "architecture-graph.mmd").write_text(render_mermaid(report.graph_nodes), encoding="utf-8")
        (output_dir / "architecture-graph.dot").write_text(render_graphviz(report.graph_nodes), encoding="utf-8")
        (output_dir / "capability-dashboard.md").write_text(render_capability_dashboard(report), encoding="utf-8")
        (output_dir / "oracle-coverage.md").write_text(render_oracle_coverage(report), encoding="utf-8")
        (output_dir / "technical-debt-dashboard.md").write_text(render_technical_debt(report), encoding="utf-8")
        (output_dir / "repository-timeline.md").write_text(render_timeline(report), encoding="utf-8")
        (output_dir / "architecture-drift.md").write_text(render_mapping_report("Architecture Drift Detector", report.drift_detection), encoding="utf-8")
        (output_dir / "constitution-validation.md").write_text(render_mapping_report("Constitution Validator", report.constitution_validation), encoding="utf-8")
        (output_dir / "candidate-pages.md").write_text(render_candidate_pages(report), encoding="utf-8")
        (output_dir / "media-graph-audit.md").write_text(render_media_graph_audit(report), encoding="utf-8")
        (output_dir / "seven-roots-audit.md").write_text(render_seven_roots_audit(report), encoding="utf-8")
        (output_dir / "repository-governance-guide.md").write_text(render_governance_guide(), encoding="utf-8")

    def _tracked_files(self) -> list[Path]:
        git_dir = self.repo_root / ".git"
        if git_dir.exists():
            result = subprocess.run(
                ["git", "ls-files"],
                cwd=self.repo_root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if result.returncode == 0:
                files = [self.repo_root / line for line in result.stdout.splitlines() if line.strip()]
                return sorted(path for path in files[: self.config.max_files] if path.is_file())
        discovered = []
        for path in self.repo_root.rglob("*"):
            if len(discovered) >= self.config.max_files:
                break
            if path.is_file() and ".git" not in path.parts:
                discovered.append(path)
        return sorted(discovered)

    def _read_text_cache(self, files: Sequence[Path]) -> dict[str, str]:
        cache: dict[str, str] = {}
        for path in files:
            relative = _relative(path, self.repo_root)
            if (
                not _is_text_candidate(path)
                or _is_heavy_generated_path(relative)
                or path.stat().st_size > self.config.max_text_bytes
            ):
                continue
            try:
                cache[relative] = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
        return cache

    def _python_import_edges(self, python_files: Sequence[Path]) -> tuple[tuple[str, str], ...]:
        edges: set[tuple[str, str]] = set()
        local_roots = {"engines", "services", "contracts", "capabilities", "constitution", "canon", "tooling"}
        module_by_path = {_relative(path, self.repo_root): _module_name(path, self.repo_root) for path in python_files}
        module_to_path = {module: path for path, module in module_by_path.items()}
        for path in python_files:
            source = _relative(path, self.repo_root)
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeDecodeError):
                continue
            for node in ast.walk(tree):
                target_name: str | None = None
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        target_name = alias.name
                        self._add_import_edge(edges, source, target_name, module_to_path, local_roots)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        target_name = node.module
                    elif node.level and source in module_by_path:
                        target_name = _resolve_relative_import(module_by_path[source], node.level, "")
                    if target_name:
                        self._add_import_edge(edges, source, target_name, module_to_path, local_roots)
        return tuple(sorted(edges))

    def _add_import_edge(
        self,
        edges: set[tuple[str, str]],
        source: str,
        target_name: str,
        module_to_path: Mapping[str, str],
        local_roots: set[str],
    ) -> None:
        root = target_name.split(".", 1)[0]
        if root not in local_roots:
            return
        target_path = _match_module_path(target_name, module_to_path)
        if target_path and target_path != source:
            edges.add((source, target_path))

    def _architecture_nodes(self, files: Sequence[Path], text_cache: Mapping[str, str]) -> tuple[GraphNode, ...]:
        docs = sorted(path for path in files if _relative(path, self.repo_root).startswith("docs/architecture/") and path.name[:2].isdigit())
        adrs = sorted(path for path in files if _relative(path, self.repo_root).startswith("docs/adrs/") and path.name.endswith(".md"))
        test_paths = tuple(sorted(_relative(path, self.repo_root) for path in files if "/tests/" in _relative(path, self.repo_root)))
        raw_nodes = []
        for path in docs:
            relative = _relative(path, self.repo_root)
            raw_nodes.append(
                (
                    path,
                    relative,
                    _safe_id(path.stem[3:]),
                    _first_heading(text_cache.get(relative, ""), path.stem),
                    _layer_from_arch_doc(path.name),
                )
            )
        nodes: list[GraphNode] = []
        for index, (path, relative, node_id, title, layer) in enumerate(raw_nodes):
            deps = (raw_nodes[index - 1][2],) if index > 0 else ()
            consumers = (raw_nodes[index + 1][2],) if index + 1 < len(raw_nodes) else ()
            matching_adrs = tuple(
                sorted(
                    _relative(adr, self.repo_root)
                    for adr in adrs
                    if relative in text_cache.get(_relative(adr, self.repo_root), "")
                )
            )
            nodes.append(
                GraphNode(
                    node_id=node_id,
                    label=title,
                    layer=layer,
                    purpose=_first_paragraph(text_cache.get(relative, "")),
                    dependencies=tuple(deps),
                    consumers=tuple(consumers),
                    adrs=matching_adrs,
                    tests=tuple(item for item in test_paths if _node_test_hint(layer, item)),
                    source_directories=_source_dirs_for_layer(layer),
                )
            )
        return tuple(nodes)

    def _dependency_health(
        self,
        python_files: Sequence[Path],
        import_edges: Sequence[tuple[str, str]],
    ) -> tuple[dict[str, object], list[Finding]]:
        findings: list[Finding] = []
        service_engine = [edge for edge in import_edges if edge[0].startswith("services/") and edge[1].startswith("engines/")]
        engine_view = [
            edge
            for edge in import_edges
            if edge[0].startswith("engines/") and not edge[0].startswith("engines/views/")
            and edge[1].startswith("engines/views/")
        ]
        layer_violations = [edge for edge in import_edges if _layer_index(edge[0]) < _layer_index(edge[1])]
        cycles = _cycles(import_edges)
        for edge in service_engine:
            findings.append(Finding("SERVICE_ENGINE_IMPORT", "error", "Service imports engine implementation.", edge[0], {"target": edge[1]}))
        for edge in engine_view:
            findings.append(Finding("ENGINE_VIEW_IMPORT", "warning", "Engine imports view implementation.", edge[0], {"target": edge[1]}))
        for edge in layer_violations:
            findings.append(Finding("LAYER_SHORTCUT", "warning", "Upstream layer imports downstream layer.", edge[0], {"target": edge[1]}))
        return (
            {
                "active_python_files": len(python_files),
                "import_edges": len(import_edges),
                "layer_violations": len(layer_violations),
                "circular_dependencies": len(cycles),
                "cross_layer_shortcuts": len(layer_violations),
                "service_engine_violations": len(service_engine),
                "engine_view_violations": len(engine_view),
                "cycles": cycles[:20],
            },
            findings,
        )

    def _repository_health(
        self,
        files: Sequence[Path],
        text_cache: Mapping[str, str],
    ) -> tuple[dict[str, object], list[Finding]]:
        findings: list[Finding] = []
        hash_groups: dict[str, list[str]] = defaultdict(list)
        skipped = 0
        for path in files:
            relative = _relative(path, self.repo_root)
            if _is_heavy_generated_path(relative):
                skipped += 1
                continue
            size = path.stat().st_size
            if size > self.config.max_hash_bytes:
                skipped += 1
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            hash_groups[digest].append(relative)
        duplicate_groups = [
            sorted(paths)
            for paths in hash_groups.values()
            if len(paths) > 1 and not all(_is_generated_or_ignored_path(path) for path in paths)
        ]
        duplicate_groups = sorted(duplicate_groups, key=lambda group: (-len(group), group[0]))[: self.config.max_duplicate_groups]
        legacy_modules = sorted(path for path in (_relative(item, self.repo_root) for item in files) if "/legacy/" in path or path.endswith("/legacy"))
        deprecated_interfaces = sorted(path for path, text in text_cache.items() if "deprecated" in text.lower())[:100]
        compatibility_aliases = sorted(path for path, text in text_cache.items() if "compatibility alias" in text.lower() or "compatibility shim" in text.lower())[:100]
        dead_code = sorted(path for path, text in text_cache.items() if re.search(r"\b(dead code|unused|orphan)\b", text, re.I))[: self.config.max_dead_code_candidates]
        if duplicate_groups:
            findings.append(Finding("DUPLICATE_HASH_GROUPS", "warning", "Duplicate tracked file hashes detected.", details={"groups": len(duplicate_groups)}))
        return (
            {
                "tracked_files": len(files),
                "duplicate_hash_groups": len(duplicate_groups),
                "duplicate_examples": duplicate_groups[:20],
                "hash_skipped_large_files": skipped,
                "legacy_modules": len(legacy_modules),
                "legacy_examples": legacy_modules[:50],
                "dead_code_candidates": len(dead_code),
                "dead_code_examples": dead_code[:50],
                "compatibility_aliases": len(compatibility_aliases),
                "deprecated_interfaces": len(deprecated_interfaces),
            },
            findings,
        )

    def _documentation_health(
        self,
        files: Sequence[Path],
        text_cache: Mapping[str, str],
    ) -> tuple[dict[str, object], list[Finding]]:
        findings: list[Finding] = []
        md_files = sorted(path for path in files if path.suffix == ".md")
        missing_links = _missing_markdown_links(self.repo_root, md_files, text_cache)
        adr_files = [path for path in md_files if _relative(path, self.repo_root).startswith("docs/adrs/") and path.name[:4].isdigit()]
        adrs_without_arch = [
            _relative(path, self.repo_root)
            for path in adr_files
            if "../architecture/" not in text_cache.get(_relative(path, self.repo_root), "")
        ]
        arch_refs_missing = [
            _relative(path, self.repo_root)
            for path in adr_files
            if "## Architecture Sections" not in text_cache.get(_relative(path, self.repo_root), "")
        ]
        dirs = sorted({path.parent for path in files if not _is_generated_or_ignored_path(_relative(path, self.repo_root))})
        missing_readmes = sorted(_relative(path, self.repo_root) for path in dirs if path != self.repo_root and not (path / "README.md").exists())[:200]
        doc_dirs = sorted({path.parent for path in md_files})
        linked_docs = _linked_doc_targets(self.repo_root, md_files, text_cache)
        orphan_docs = sorted(_relative(path, self.repo_root) for path in md_files if _relative(path, self.repo_root) not in linked_docs and path.name != "README.md")[:200]
        for path, target in missing_links[:25]:
            findings.append(Finding("BROKEN_DOC_LINK", "warning", "Broken documentation link.", path, {"target": target}))
        for path in adrs_without_arch:
            findings.append(Finding("ADR_MISSING_ARCHITECTURE_REFERENCE", "warning", "ADR does not cite architecture section.", path))
        return (
            {
                "markdown_files": len(md_files),
                "doc_directories": len(doc_dirs),
                "missing_adr_links": len(adrs_without_arch),
                "missing_architecture_references": len(arch_refs_missing),
                "missing_readme_files": len(missing_readmes),
                "missing_readme_examples": missing_readmes[:50],
                "broken_documentation_links": len(missing_links),
                "broken_link_examples": missing_links[:50],
                "orphan_documentation": len(orphan_docs),
                "orphan_documentation_examples": orphan_docs[:50],
            },
            findings,
        )

    def _capability_health(
        self,
        files: Sequence[Path],
        text_cache: Mapping[str, str],
    ) -> tuple[dict[str, object], tuple[tuple[str, str], ...]]:
        capability_docs = sorted(path for path in text_cache if "capabilit" in text_cache[path].lower())
        headings = _headings_by_keyword(text_cache, "capability")
        registered = sorted(set(_clean_heading(heading) for heading in headings if _clean_heading(heading)))
        owners = _owner_candidates(text_cache)
        orphan = [item for item in registered if not any(item.lower() in owner.lower() for owner in owners)]
        duplicates = _duplicates(item.lower() for item in registered)
        edges = tuple(sorted(("capability-registry", item.lower().replace(" ", "-")) for item in registered[:200]))
        return (
            {
                "registered_capabilities": len(registered),
                "capability_examples": registered[:50],
                "orphan_capabilities": len(orphan),
                "orphan_examples": orphan[:50],
                "duplicate_capabilities": len(duplicates),
                "duplicate_examples": duplicates[:50],
                "missing_capability_owners": len(orphan),
                "capability_docs": len(capability_docs),
                "coverage": _percent(len(registered) - len(orphan), max(len(registered), 1)),
            },
            edges,
        )

    def _oracle_health(
        self,
        files: Sequence[Path],
        text_cache: Mapping[str, str],
    ) -> tuple[dict[str, object], tuple[tuple[str, str], ...]]:
        oracle_dirs = sorted(
            {
                _oracle_root(_relative(path, self.repo_root))
                for path in files
                if _relative(path, self.repo_root).startswith("engines/")
                and "/tests/" not in _relative(path, self.repo_root)
                and ("oracle" in path.name.lower() or "oracle" in _relative(path, self.repo_root).lower())
            }
        )
        inventory = []
        edges: list[tuple[str, str]] = []
        oracle_text = "\n".join(
            value
            for path, value in text_cache.items()
            if any(path.startswith(directory) for directory in oracle_dirs)
        ).lower()
        for directory in oracle_dirs:
            text = "\n".join(value for path, value in text_cache.items() if path.startswith(directory))
            parent = str(Path(directory).parent)
            children = sorted(str(Path(item).name) for item in oracle_dirs if Path(item).parent.as_posix() == directory)
            observation_types = sorted(set(re.findall(r"\b([A-Z][A-Za-z]+Observation|[a-z_]+_observation)\b", text)))[:50]
            inventory.append(
                {
                    "oracle": directory,
                    "scope": _first_heading(text, Path(directory).name),
                    "parent": parent,
                    "children": children,
                    "observation_types": observation_types,
                    "confidence_propagation": "confidence" in text.lower(),
                    "provenance_propagation": "provenance" in text.lower(),
                    "coverage": _percent(int("provenance" in text.lower()) + int("confidence" in text.lower()), 2),
                }
            )
            edges.append((parent, directory))
        missing_domains: dict[str, list[str]] = {}
        for group, domains in MISSING_ORACLE_DOMAINS:
            missing_domains[group] = [domain for domain in domains if domain not in oracle_text]
        return (
            {
                "oracle_count": len(inventory),
                "oracles": inventory,
                "missing_observation_domains": missing_domains,
            },
            tuple(sorted(edges)),
        )

    def _coverage_health(self, text_cache: Mapping[str, str], terms: Sequence[str]) -> dict[str, object]:
        coverage = {}
        all_text = "\n".join(text_cache.values()).lower()
        for term in terms:
            coverage[term] = all_text.count(term.lower())
        complete = sum(1 for count in coverage.values() if count > 0)
        return {"coverage": _percent(complete, len(terms)), "terms": coverage}

    def _representation_health(self, files: Sequence[Path], text_cache: Mapping[str, str]) -> dict[str, object]:
        coverage = self._coverage_health(text_cache, REPRESENTATION_TERMS)
        media_coverage = self._coverage_health(text_cache, MEDIA_TERMS)
        derived_refs = sum(1 for text in text_cache.values() if "derived" in text.lower() and "representation" in text.lower())
        representation_paths = sorted(path for path in text_cache if "representation" in path.lower() or "retrieval" in path.lower() or "search" in path.lower())
        return {
            **coverage,
            "media_terms": media_coverage["terms"],
            "representation_docs": representation_paths[:50],
            "derived_representation_references": derived_refs,
            "derived_boundary_status": "pass" if derived_refs else "attention",
        }

    def _knowledge_health(self, files: Sequence[Path], text_cache: Mapping[str, str]) -> dict[str, object]:
        quality_path = self.repo_root / "Knowledge" / "reports" / "quality_gates.json"
        quality: dict[str, object] = {}
        if quality_path.exists():
            try:
                quality = json.loads(quality_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                quality = {"status": "unreadable"}
        knowledge_files = [path for path in files if _relative(path, self.repo_root).startswith("Knowledge/")]
        generated_refs = sum(1 for text in text_cache.values() if "knowledge is generated" in text.lower() or "knowledge is derived" in text.lower())
        return {
            "knowledge_files": len(knowledge_files),
            "quality_gates": quality,
            "knowledge_is_generated": generated_refs > 0,
            "reality_remains_canonical": "Reality remains canonical" in "\n".join(text_cache.values()),
            "provenance_missing_count": quality.get("provenance_missing_count", "unknown"),
        }

    def _inventory_health(
        self,
        files: Sequence[Path],
        text_cache: Mapping[str, str],
        terms: Sequence[str],
        label: str,
    ) -> dict[str, object]:
        coverage = self._coverage_health(text_cache, terms)
        paths = sorted(path for path, text in text_cache.items() if label in path.lower() or label in text.lower())[:50]
        return {**coverage, "inventory_paths": paths, "orphan_count": 0 if paths else 1}

    def _view_health(self, python_files: Sequence[Path], import_edges: Sequence[tuple[str, str]]) -> dict[str, object]:
        view_files = [_relative(path, self.repo_root) for path in python_files if _relative(path, self.repo_root).startswith("engines/views/")]
        reasoning_imports = [edge for edge in import_edges if edge[0].startswith("engines/views/") and "reason" in edge[1].lower()]
        navigation_imports = [edge for edge in import_edges if edge[0].startswith("engines/views/") and "navigation" in edge[1].lower()]
        return {
            "view_files": len(view_files),
            "views_perform_reasoning": bool(reasoning_imports),
            "reasoning_imports": reasoning_imports,
            "navigation_consumers": navigation_imports,
            "interchangeable_status": "pass" if view_files else "attention",
        }

    def _action_health(
        self,
        files: Sequence[Path],
        text_cache: Mapping[str, str],
        import_edges: Sequence[tuple[str, str]],
    ) -> dict[str, object]:
        action_paths = sorted(path for path, text in text_cache.items() if "action" in path.lower() or "action" in text.lower())[:100]
        action_to_ark = [edge for edge in import_edges if "action" in edge[0].lower() and "ark" in edge[1].lower()]
        return {
            "action_references": len(action_paths),
            "action_examples": action_paths[:50],
            "actions_update_ark": bool(action_to_ark),
            "action_to_ark_imports": action_to_ark,
            "reobserve_boundary_documented": any("re-observed" in text.lower() or "reobserved" in text.lower() for text in text_cache.values()),
        }

    def _constitution_validation(
        self,
        files: Sequence[Path],
        text_cache: Mapping[str, str],
        import_edges: Sequence[tuple[str, str]],
    ) -> tuple[dict[str, object], list[Finding]]:
        findings: list[Finding] = []
        architecture_files = {_relative(path, self.repo_root) for path in files if _relative(path, self.repo_root).startswith("docs/architecture/")}
        rules = []
        seven_roots = self._coverage_health(text_cache, ROOT_TERMS)
        for rule_id, label, evidence_files in CONSTITUTION_RULES:
            present = all(f"docs/architecture/{evidence}" in architecture_files for evidence in evidence_files)
            rules.append({"rule": label, "status": "pass" if present else "missing", "evidence": list(evidence_files)})
            if not present:
                findings.append(Finding("CONSTITUTION_RULE_MISSING_EVIDENCE", "warning", f"Missing evidence for {label}.", details={"rule": rule_id}))
        layer_violations = [edge for edge in import_edges if _layer_index(edge[0]) < _layer_index(edge[1])]
        return (
            {
                "rules": rules,
                "seven_roots_terms": seven_roots["terms"],
                "layer_violations": len(layer_violations),
                "status": "pass" if not layer_violations and all(item["status"] == "pass" for item in rules) else "attention",
            },
            findings,
        )

    def _drift_detection(
        self,
        files: Sequence[Path],
        text_cache: Mapping[str, str],
        import_edges: Sequence[tuple[str, str]],
    ) -> tuple[dict[str, object], list[Finding]]:
        findings: list[Finding] = []
        generated_canonical = [
            _relative(path, self.repo_root)
            for path in files
            if _relative(path, self.repo_root).startswith("Knowledge/")
            and path.suffix in {".md", ".json", ".jsonl"}
        ]
        duplicate_caps = _duplicates(_clean_heading(item).lower() for item in _headings_by_keyword(text_cache, "capability"))
        layer_bypass = [edge for edge in import_edges if _layer_index(edge[0]) < _layer_index(edge[1])]
        if layer_bypass:
            findings.append(Finding("ARCHITECTURAL_DRIFT_LAYER_BYPASS", "warning", "New or existing modules bypass canonical layer direction.", details={"count": len(layer_bypass)}))
        return (
            {
                "layer_bypass_edges": len(layer_bypass),
                "duplicate_capability_terms": duplicate_caps[:50],
                "generated_artifacts_tracked": len(generated_canonical),
                "generated_artifact_status": "tracked-as-derived-evidence",
                "knowledge_replaces_reality": False,
            },
            findings,
        )

    def _technical_debt(self, repository_health: Mapping[str, object], text_cache: Mapping[str, str]) -> dict[str, object]:
        todo_paths = sorted(path for path, text in text_cache.items() if "todo" in text.lower() or "fixme" in text.lower())[:100]
        blockers = sorted(path for path, text in text_cache.items() if "blocker" in text.lower() or "blocked" in text.lower())[:100]
        return {
            "duplicate_code": repository_health.get("duplicate_hash_groups", 0),
            "legacy_aliases": repository_health.get("compatibility_aliases", 0),
            "compatibility_shims": repository_health.get("compatibility_aliases", 0),
            "todos": len(todo_paths),
            "todo_examples": todo_paths[:50],
            "deprecated_apis": repository_health.get("deprecated_interfaces", 0),
            "migration_blockers": len(blockers),
            "priority_order": [
                "Storage service proof",
                "Candidate Pages",
                "Compatibility Layer",
                "Generated/legacy surface labeling",
                "Dependency linter warning mode",
            ],
        }

    def _repository_timeline(self, files: Sequence[Path], text_cache: Mapping[str, str]) -> tuple[Mapping[str, object], ...]:
        events: list[dict[str, object]] = []
        for path in sorted(files):
            relative = _relative(path, self.repo_root)
            if relative.startswith("docs/adrs/") and path.name[:4].isdigit():
                text = text_cache.get(relative, "")
                events.append({"type": "adr", "id": path.stem, "title": _first_heading(text, path.stem), "path": relative})
            if "milestone" in relative.lower() or "release" in relative.lower():
                events.append({"type": "milestone", "title": path.stem, "path": relative})
        return tuple(events[:200])

    def _candidate_pages(self, text_cache: Mapping[str, str]) -> tuple[Mapping[str, object], ...]:
        heading_counts = Counter(_clean_heading(heading).lower() for heading in _all_headings(text_cache))
        pages = []
        for heading, count in sorted(heading_counts.items(), key=lambda item: (-item[1], item[0])):
            if count < 3 or not heading:
                continue
            paths = sorted(path for path, text in text_cache.items() if re.search(rf"^#+\s+{re.escape(heading)}\s*$", text, re.I | re.M))
            pages.append(
                {
                    "candidate_page_id": _stable_id("candidate-page", heading),
                    "concept": heading,
                    "occurrences": count,
                    "evidence_paths": paths[:20],
                    "status": "review_required",
                    "promotion": "never_auto_promote",
                }
            )
            if len(pages) >= self.config.max_candidate_pages:
                break
        return tuple(pages)

    def _package_edges(self, import_edges: Sequence[tuple[str, str]]) -> tuple[tuple[str, str], ...]:
        packages = set()
        for source, target in import_edges:
            packages.add((_package_id(source), _package_id(target)))
        return tuple(sorted(edge for edge in packages if edge[0] != edge[1]))


def render_health_dashboard(report: DoctorReport) -> str:
    sections = [
        "# Repository Health Dashboard",
        "",
        f"Status: `{report.status}`",
        f"Architecture Health Score: `{report.score}`",
        "",
        "## Health Summary",
        "",
        _mapping_table(
            {
                "Dependency": report.dependency_health,
                "Repository": report.repository_health,
                "Documentation": report.documentation_health,
                "Capability": report.capability_health,
                "Oracle": report.oracle_health,
                "Reality": report.reality_health,
                "Representation": report.representation_health,
                "Knowledge": report.knowledge_health,
                "Mission": report.mission_health,
                "Navigation": report.navigation_health,
                "Views": report.view_health,
                "Actions": report.action_health,
            }
        ),
        "",
        "## Findings",
        "",
        _findings_table(report.findings),
    ]
    return "\n".join(sections) + "\n"


def render_governance_index() -> str:
    return """# Repository Governance

Generated architecture intelligence reports for Wayfinder.

Run:

```bash
./wf doctor --write
./wf architecture check --write
```

Reports:

- [Repository Health Dashboard](repository-health-dashboard.md)
- [Architecture Drift Detector](architecture-drift.md)
- [Constitution Validator](constitution-validation.md)
- [Architecture Graph Mermaid](architecture-graph.mmd)
- [Architecture Graph Graphviz](architecture-graph.dot)
- [Capability Dashboard](capability-dashboard.md)
- [Oracle Coverage Report](oracle-coverage.md)
- [Media Graph Audit](media-graph-audit.md)
- [Seven Roots Audit](seven-roots-audit.md)
- [Repository Timeline](repository-timeline.md)
- [Technical Debt Dashboard](technical-debt-dashboard.md)
- [Candidate Pages](candidate-pages.md)
- [Repository Governance Guide](repository-governance-guide.md)
- [Machine-Readable Doctor Report](architecture-doctor.json)
"""


def render_capability_dashboard(report: DoctorReport) -> str:
    health = report.capability_health
    rows = [
        "| Capability | Coverage | Tests | Owner |",
        "| --- | ---: | --- | --- |",
    ]
    for item in health.get("capability_examples", [])[:50]:
        rows.append(f"| {item} | {health.get('coverage', 0)}% | △ | Capability Registry |")
    if len(rows) == 2:
        rows.append("| Capability Registry | 0% | △ | Unassigned |")
    return "# Capability Dashboard\n\n" + "\n".join(rows) + "\n"


def render_oracle_coverage(report: DoctorReport) -> str:
    lines = ["# Oracle Coverage Report", ""]
    for oracle in report.oracle_health.get("oracles", []):
        lines.extend(
            [
                f"## {oracle['oracle']}",
                "",
                f"- Scope: {oracle['scope']}",
                f"- Parent: `{oracle['parent']}`",
                f"- Children: {', '.join(oracle['children']) or 'none'}",
                f"- Observation types: {', '.join(oracle['observation_types']) or 'not declared'}",
                f"- Confidence propagation: {oracle['confidence_propagation']}",
                f"- Provenance propagation: {oracle['provenance_propagation']}",
                f"- Coverage: {oracle['coverage']}%",
                "",
            ]
        )
    lines.append("## Missing Observation Domains")
    lines.append("")
    for group, domains in report.oracle_health.get("missing_observation_domains", {}).items():
        lines.append(f"- {group}: {', '.join(domains) if domains else 'none detected as missing'}")
    return "\n".join(lines) + "\n"


def render_technical_debt(report: DoctorReport) -> str:
    return render_mapping_report("Technical Debt Dashboard", report.technical_debt)


def render_timeline(report: DoctorReport) -> str:
    lines = ["# Repository Timeline", ""]
    for event in report.repository_timeline:
        path = str(event.get("path", ""))
        lines.append(f"- `{event.get('type')}`: [{event.get('title')}]({_governance_link(path)})")
    return "\n".join(lines) + "\n"


def render_mapping_report(title: str, mapping: Mapping[str, object]) -> str:
    return f"# {title}\n\n" + _mapping_table(mapping) + "\n"


def render_candidate_pages(report: DoctorReport) -> str:
    lines = ["# Candidate Page Generator", "", "Candidate Pages are review prompts only. They are never auto-promoted.", ""]
    for page in report.candidate_pages:
        lines.extend(
            [
                f"## {page['concept']}",
                "",
                f"- Candidate Page ID: `{page['candidate_page_id']}`",
                f"- Occurrences: {page['occurrences']}",
                f"- Status: {page['status']}",
                f"- Promotion: {page['promotion']}",
                "- Evidence:",
            ]
        )
        for path in page["evidence_paths"][:10]:
            lines.append(f"  - `{path}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_media_graph_audit(report: DoctorReport) -> str:
    terms = report.representation_health.get("media_terms", {})
    lines = ["# Media Graph Audit", "", "| Domain | Repository Mentions | Status |", "| --- | ---: | --- |"]
    all_health = report.representation_health
    for term in MEDIA_TERMS:
        count = int(terms.get(term, 0)) if term in terms else 0
        lines.append(f"| {term.title()} | {count} | {'present' if count else 'missing or not canonical'} |")
    lines.extend(["", f"Derived representation boundary: `{all_health.get('derived_boundary_status')}`"])
    return "\n".join(lines) + "\n"


def render_seven_roots_audit(report: DoctorReport) -> str:
    lines = ["# Seven Roots Audit", "", "Seven Roots must remain internal semantic machinery, not UI dependencies.", ""]
    lines.append("| Root | Repository Mentions |")
    lines.append("| --- | ---: |")
    root_counts = report.constitution_validation.get("seven_roots_terms", {})
    for root in ROOT_TERMS:
        lines.append(f"| {root.title()} | {root_counts.get(root, 0)} |")
    lines.extend(["", "- UI direct dependency status: not detected by current import scan."])
    return "\n".join(lines) + "\n"


def render_governance_guide() -> str:
    return """# Repository Governance Guide

Run architecture diagnostics before architecture-sensitive changes:

```bash
./wf doctor --write
./wf architecture check --write --fail-on-violations
```

Governance rules:

- Architecture docs define the canonical model.
- ADRs define evidence-backed decisions and must cite architecture sections.
- Code implements architecture and must not bypass canonical layers.
- Generated knowledge remains derived evidence.
- Candidate Pages require human review and are never auto-promoted.
- CI should run the architecture check in warning mode until legacy exceptions
  are intentionally classified.
"""


def render_mermaid(nodes: Sequence[GraphNode]) -> str:
    lines = ["flowchart LR"]
    for node in nodes:
        lines.append(f'  {node.node_id}["{_escape_graph_label(node.label)}"]')
    for node in nodes:
        for dependency in node.dependencies:
            if dependency != node.node_id:
                lines.append(f"  {dependency} --> {node.node_id}")
    return "\n".join(lines) + "\n"


def render_graphviz(nodes: Sequence[GraphNode]) -> str:
    lines = ["digraph WayfinderArchitecture {", "  rankdir=LR;"]
    for node in nodes:
        label = _escape_graph_label(f"{node.label}\\nLayer: {node.layer}")
        lines.append(f'  {node.node_id} [label="{label}"];')
    for node in nodes:
        for dependency in node.dependencies:
            if dependency != node.node_id:
                lines.append(f"  {dependency} -> {node.node_id};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def _relative(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.resolve().relative_to(repo_root).as_posix()


def _is_legacy(path: Path) -> bool:
    return "legacy" in path.parts


def _is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in {".py", ".md", ".json", ".jsonl", ".txt", ".toml", ".yml", ".yaml"} or path.name in {"wf"}


def _is_generated_or_ignored_path(path: str) -> bool:
    return path.startswith("Knowledge/") or path.startswith(".wayfinder-validation/") or "/__pycache__/" in path


def _is_heavy_generated_path(path: str) -> bool:
    if path.startswith("Knowledge/Graph/") or path.startswith("Knowledge/search/"):
        return True
    if path.startswith("Knowledge/") and not path.startswith("Knowledge/reports/") and not path.endswith("README.md"):
        return True
    return path.startswith(".wayfinder-validation/")


def _oracle_root(path: str) -> str:
    parts = path.split("/")
    for index, part in enumerate(parts):
        if "oracle" in part.lower():
            return "/".join(parts[: index + 1])
    return str(Path(path).parent)


def _module_name(path: Path, repo_root: Path) -> str:
    relative = _relative(path, repo_root)
    if relative.endswith("/__init__.py"):
        relative = relative[: -len("/__init__.py")]
    elif relative.endswith(".py"):
        relative = relative[:-3]
    return relative.replace("/", ".").replace("-", "_")


def _resolve_relative_import(source_module: str, level: int, module: str) -> str:
    parts = source_module.split(".")[:-level]
    if module:
        parts.append(module)
    return ".".join(parts)


def _match_module_path(module: str, module_to_path: Mapping[str, str]) -> str | None:
    normalized = module.replace("-", "_")
    candidates = [normalized]
    parts = normalized.split(".")
    while len(parts) > 1:
        parts.pop()
        candidates.append(".".join(parts))
    for candidate in candidates:
        if candidate in module_to_path:
            return module_to_path[candidate]
    return None


def _first_heading(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.M)
    return match.group(1).strip() if match else fallback


def _first_paragraph(text: str) -> str:
    paragraphs = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip() and not chunk.startswith("#")]
    return paragraphs[0].replace("\n", " ")[:240] if paragraphs else ""


def _layer_from_arch_doc(name: str) -> str:
    stem = name[3:-3] if name.endswith(".md") else name
    title = stem.replace("-", " ").title()
    for layer in CANONICAL_LAYERS:
        if layer.lower() in title.lower():
            return layer
    return title


def _source_dirs_for_layer(layer: str) -> tuple[str, ...]:
    mapping = {
        "Constitution": ("constitution/", "canon/"),
        "Perception": ("engines/ark/ingress/", "external/"),
        "Observations": ("contracts/observations/", "engines/ark/ingress/chatgpt_oracle/"),
        "ARK": ("engines/ark/ingress/reality_ingestion/",),
        "Representations": ("contracts/representations/", "engines/views/knowledge_retrieval/"),
        "Focus": ("engines/interpretation/knowledge_governance/",),
        "Understanding": ("engines/interpretation/knowledge_compiler/",),
        "Missions": ("domains/",),
        "Bearings": ("contracts/bearings/",),
        "Reasoning": ("engines/jarvis/",),
        "Navigation": ("contracts/recommendations/",),
        "Experiences": ("engines/views/", "internal/"),
        "Actions": ("operations/", "engines/foundry/"),
    }
    return mapping.get(layer, ())


def _node_test_hint(layer: str, path: str) -> bool:
    lower = path.lower()
    hints = {
        "ARK": "ark",
        "Perception": "oracle",
        "Understanding": "compiler",
        "Focus": "governance",
        "Representations": "retrieval",
        "Experiences": "views",
    }
    return hints.get(layer, layer.lower()) in lower


def _layer_index(path: str) -> int:
    if path.startswith("constitution/") or path.startswith("canon/"):
        return 0
    if "chatgpt_oracle" in path or path.startswith("external/"):
        return 2
    if path.startswith("contracts/observations/"):
        return 3
    if "reality_ingestion" in path or path.startswith("engines/ark/"):
        return 4
    if "knowledge_retrieval" in path or path.startswith("contracts/representations/"):
        return 5
    if "knowledge_governance" in path:
        return 6
    if "knowledge_compiler" in path:
        return 7
    if path.startswith("domains/"):
        return 8
    if path.startswith("contracts/bearings/"):
        return 9
    if path.startswith("engines/jarvis/"):
        return 10
    if path.startswith("contracts/recommendations/"):
        return 11
    if path.startswith("engines/views/") or path.startswith("internal/"):
        return 12
    if path.startswith("operations/") or path.startswith("engines/foundry/"):
        return 13
    if path.startswith("services/"):
        return 4
    if path.startswith("tooling/"):
        return 7
    return 99


def _cycles(edges: Sequence[tuple[str, str]]) -> list[list[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    for source, target in edges:
        graph[source].add(target)
    cycles: list[list[str]] = []
    for start in sorted(graph):
        queue: deque[tuple[str, list[str]]] = deque((target, [start, target]) for target in sorted(graph[start]))
        seen = 0
        while queue and seen < 200:
            seen += 1
            node, path = queue.popleft()
            if node == start and len(path) > 2:
                cycles.append(path)
                break
            if len(path) > 8:
                continue
            for target in sorted(graph.get(node, ())):
                if target == start or target not in path:
                    queue.append((target, path + [target]))
        if len(cycles) >= 20:
            break
    return cycles


def _missing_markdown_links(repo_root: Path, md_files: Sequence[Path], text_cache: Mapping[str, str]) -> list[tuple[str, str]]:
    missing: list[tuple[str, str]] = []
    for path in md_files:
        relative = _relative(path, repo_root)
        text = text_cache.get(relative, "")
        for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if raw.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = raw.split("#", 1)[0]
            if not target:
                continue
            if not (path.parent / target).resolve().exists():
                missing.append((relative, raw))
    return missing


def _linked_doc_targets(repo_root: Path, md_files: Sequence[Path], text_cache: Mapping[str, str]) -> set[str]:
    targets: set[str] = set()
    for path in md_files:
        relative = _relative(path, repo_root)
        text = text_cache.get(relative, "")
        for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if raw.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = raw.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if resolved.exists() and resolved.is_file() and resolved.suffix == ".md":
                targets.add(_relative(resolved, repo_root))
    return targets


def _headings_by_keyword(text_cache: Mapping[str, str], keyword: str) -> list[str]:
    headings = []
    for text in text_cache.values():
        for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.M):
            if keyword.lower() in heading.lower():
                headings.append(heading)
    return headings


def _all_headings(text_cache: Mapping[str, str]) -> list[str]:
    headings = []
    for text in text_cache.values():
        headings.extend(re.findall(r"^#{1,6}\s+(.+)$", text, re.M))
    return headings


def _clean_heading(heading: str) -> str:
    return re.sub(r"[`*_#]", "", heading).strip(" :-")


def _owner_candidates(text_cache: Mapping[str, str]) -> set[str]:
    owners: set[str] = set()
    for text in text_cache.values():
        for match in re.findall(r"(?:owner|owns|owned by)[:\s]+([A-Za-z0-9 _/-]{3,80})", text, re.I):
            owners.add(match.strip())
    return owners


def _duplicates(items: Iterable[str]) -> list[str]:
    counts = Counter(item for item in items if item)
    return sorted(item for item, count in counts.items() if count > 1)


def _stable_id(prefix: str, value: str) -> str:
    return f"{prefix}-{hashlib.sha256(value.encode('utf-8')).hexdigest()[:12]}"


def _safe_id(value: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower()).strip("_")
    return safe or "node"


def _percent(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        return 0
    return round((numerator / denominator) * 100)


def _score(findings: Sequence[Finding]) -> int:
    score = 100
    for finding in findings:
        if finding.severity == "error":
            score -= 15
        elif finding.severity == "warning":
            score -= 5
    return max(score, 0)


def _package_id(path: str) -> str:
    parts = path.split("/")
    return "/".join(parts[:3]) if len(parts) >= 3 else "/".join(parts)


def _escape_graph_label(label: str) -> str:
    return label.replace("\\", "\\\\").replace('"', '\\"')


def _mapping_table(mapping: Mapping[str, object]) -> str:
    lines = ["| Metric | Value |", "| --- | --- |"]
    for key, value in mapping.items():
        if isinstance(value, Mapping):
            rendered = f"`{len(value)}` fields"
        elif isinstance(value, (list, tuple)):
            rendered = f"`{len(value)}` items"
        else:
            rendered = f"`{value}`"
        lines.append(f"| {key} | {rendered} |")
    return "\n".join(lines)


def _governance_link(repo_path: str) -> str:
    if repo_path.startswith("docs/"):
        return "../" + repo_path[len("docs/") :]
    return "../../" + repo_path


def _findings_table(findings: Sequence[Finding]) -> str:
    lines = ["| Severity | Code | Path | Message |", "| --- | --- | --- | --- |"]
    for finding in findings[:200]:
        lines.append(f"| {finding.severity} | `{finding.code}` | `{finding.path or ''}` | {finding.message} |")
    if len(lines) == 2:
        lines.append("| pass | `NONE` |  | No findings. |")
    return "\n".join(lines)
