#!/usr/bin/env python3
"""Aurora command contract and reusable execution layer.

This module is the stable command interface used by the CLI, GUI server, and
future clients. It owns command dispatch and delegates implementation to
UI-independent services.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


MAX_COMMAND_EVENTS = 50


@dataclass(frozen=True)
class RuntimeConfig:
    repo_root: Path
    source_roots: tuple[str, ...]
    max_files: int
    max_file_bytes: int
    max_search_results: int
    max_graph_nodes: int
    cache_ttl_seconds: float
    git_timeout_seconds: float
    debug: bool = False


@dataclass(frozen=True)
class CommandResult:
    status: str
    command: str
    data: dict[str, Any]
    events: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def payload(self) -> dict[str, Any]:
        return asdict(self)


class AuroraCommandError(Exception):
    def __init__(
        self,
        code: str,
        reason: str,
        context: dict[str, Any] | None = None,
        recoverable: bool = True,
        status: int = 400,
    ) -> None:
        super().__init__(reason)
        self.code = code
        self.reason = reason
        self.context = context or {}
        self.recoverable = recoverable
        self.status = status

    def payload(self) -> dict[str, Any]:
        return {
            "status": "error",
            "error_code": self.code,
            "reason": self.reason,
            "context": self.context,
            "recoverable": self.recoverable,
        }


def default_runtime_config() -> RuntimeConfig:
    studio = _studio()
    config = studio.STATE.config
    return RuntimeConfig(
        repo_root=Path(config.repo_root),
        source_roots=tuple(config.source_roots),
        max_files=int(config.max_files),
        max_file_bytes=int(config.max_file_bytes),
        max_search_results=int(config.max_search_results),
        max_graph_nodes=int(config.max_graph_nodes),
        cache_ttl_seconds=float(config.cache_ttl_seconds),
        git_timeout_seconds=float(config.git_timeout_seconds),
        debug=bool(config.debug),
    )


def execute(command: str, params: dict[str, Any] | None = None, runtime: RuntimeConfig | Any | None = None) -> dict[str, Any]:
    """Execute one Aurora command and return the canonical JSON payload."""
    studio = _studio()
    if runtime is not None:
        _apply_runtime(studio, runtime)
    params = params or {}
    handler = COMMANDS.get(command)
    if handler is None:
        raise AuroraCommandError("UNKNOWN_COMMAND", "Aurora command is not registered.", {"command": command}, True, 400)
    try:
        data = handler(studio, params)
    except studio.ClientError as exc:
        raise AuroraCommandError(exc.code, exc.reason, exc.context, exc.recoverable, exc.status) from exc
    return CommandResult(
        status="ok",
        command=command,
        data=data,
        events=studio.EVENT_BUS.recent(MAX_COMMAND_EVENTS),
    ).payload()


def command_catalog() -> dict[str, Any]:
    domains: dict[str, list[str]] = {}
    for command in sorted(COMMANDS):
        domain = command.split(".", 1)[0]
        domains.setdefault(domain, []).append(command)
    return {
        "executable": "aurora",
        "contract": "p7-cli-over-gui",
        "outputModes": ["json", "human", "yaml", "markdown", "table", "graph"],
        "domains": domains,
    }


def _apply_runtime(studio: Any, runtime: RuntimeConfig | Any) -> None:
    repo_root = Path(getattr(runtime, "repo_root")).resolve()
    source_roots = tuple(getattr(runtime, "source_roots"))
    studio.STATE.config = studio.StudioConfig(
        repo_root=repo_root,
        static_root=studio.STATIC_ROOT,
        source_roots=source_roots,
        max_files=int(getattr(runtime, "max_files")),
        max_file_bytes=int(getattr(runtime, "max_file_bytes")),
        max_search_results=int(getattr(runtime, "max_search_results")),
        max_graph_nodes=int(getattr(runtime, "max_graph_nodes")),
        cache_ttl_seconds=float(getattr(runtime, "cache_ttl_seconds")),
        git_timeout_seconds=float(getattr(runtime, "git_timeout_seconds")),
        debug=bool(getattr(runtime, "debug", False)),
    )
    studio.STATE.config.validate()


def _studio() -> Any:
    import studio_server

    return studio_server


def _bool_param(params: dict[str, Any], name: str, default: bool = False) -> bool:
    value = params.get(name, default)
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"1", "true", "yes", "on"}


def _string_param(params: dict[str, Any], name: str, default: str = "") -> str:
    value = params.get(name, default)
    return str(value)


def _cmd_catalog(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return command_catalog()


def _cmd_health(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.health_payload()


def _cmd_index(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.get_index(force=_bool_param(params, "force"))


def _cmd_document_get(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    rel = _string_param(params, "path")
    if not rel:
        raise studio.ClientError(400, "MISSING_PATH", "Document path is required.", {}, True)
    candidate = (studio.STATE.config.repo_root / rel).resolve()
    try:
        candidate.relative_to(studio.STATE.config.repo_root)
    except ValueError:
        raise studio.ClientError(403, "PATH_OUTSIDE_REPOSITORY", "Path escapes repository root.", {"path": rel}, False)
    if not studio.is_allowed_source_path(candidate):
        raise studio.ClientError(403, "PATH_NOT_INDEXED_SOURCE", "Path is outside indexed source roots.", {"path": rel}, False)
    if not candidate.exists() or candidate.suffix.lower() not in studio.TEXT_SUFFIXES:
        raise studio.ClientError(404, "DOCUMENT_NOT_FOUND", "Document was not found or is not a supported text file.", {"path": rel}, True)
    return {"path": studio.safe_relative(candidate), "text": studio.read_text(candidate)}


def _cmd_search(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    query = _string_param(params, "query")
    docs = studio.load_documents()
    return {"query": query, "results": studio.search_documents(docs, query)}


def _cmd_query(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    expression = _string_param(params, "expression")
    docs = studio.load_documents()
    return {
        "expression": expression,
        "strategy": "search-backed-query",
        "results": studio.search_documents(docs, expression),
    }


def _cmd_validate(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.get_index(force=_bool_param(params, "force"))["validation"]


def _cmd_lint(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    validation = studio.get_index(force=_bool_param(params, "force"))["validation"]
    return {
        "status": validation["status"],
        "diagnostics": validation["diagnostics"],
        "counts": validation["counts"],
        "rules": ["BBREF-001", "BBSCHEMA-001", "BBLAYER-001", "BBGEN-001", "BBREADME-001", "BBROOT-001"],
    }


def _cmd_graph(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    graph = studio.get_index()["graph"]
    graph_type = _string_param(params, "type", "dependencies")
    return {"type": graph_type, "graph": graph}


def _cmd_platform(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.platform_payload()


def _cmd_repository_list(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.RepositoryService().registry()


def _cmd_workspace_current(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.WorkspaceService().current_workspace()


def _cmd_workspace_list(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    workspace = studio.WorkspaceService().current_workspace()
    return {"workspaces": [workspace]}


def _cmd_workspace_open(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    name = _string_param(params, "name", "local")
    workspace = studio.WorkspaceService().current_workspace()
    return {"requested": name, "workspace": workspace, "opened": workspace["id"] in {name, "local", "homestead"}}


def _cmd_property_list(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.PropertyService().model()


def _cmd_property_navigator(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.PropertyService().navigator(params.get("object"))


def _cmd_instantiate(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    pattern = _string_param(params, "pattern")
    property_repo = _string_param(params, "property", "property-local")
    return studio.InstantiationService().preview(pattern, property_repo)


def _cmd_compile(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    target = _string_param(params, "target", "Digital Twin")
    return studio.CompilerService().plan_compile(studio.normalized_param(target, "target", 80))


def _cmd_compiler_pipeline(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.CompilerService().pipeline()


def _cmd_review_repository(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    index = studio.get_index(force=_bool_param(params, "force"))
    return index["reports"] | {"validation": index["validation"]}


def _cmd_report_architecture(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    index = studio.get_index(force=_bool_param(params, "force"))
    return {"summary": index["summary"], "reports": index["reports"], "platform": index["platform"]}


def _cmd_git_status(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.GitService().summary()


def _cmd_git_diff(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.run_git(["diff", "--stat"])


def _cmd_git_history(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.GitService().log()


def _cmd_git_branch(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.GitService().branches()


def _cmd_plugin_list(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.PluginService().manifest()


def _cmd_ai_providers(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.AIService().providers()


def _cmd_jarvis_interface(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.JarvisService().interface()


def _cmd_events_list(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return {"events": studio.EVENT_BUS.recent(MAX_COMMAND_EVENTS)}


def _cmd_build_bible_index(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    index = studio.get_index(force=_bool_param(params, "force"))
    return {
        "summary": index["summary"],
        "documents": [doc for doc in index["documents"] if doc["path"].startswith("BUILD_BIBLE/")],
    }


def _cmd_digital_twin_status(studio: Any, params: dict[str, Any]) -> dict[str, Any]:
    return studio.DigitalTwinService().interface()


COMMANDS = {
    "catalog": _cmd_catalog,
    "health": _cmd_health,
    "index": _cmd_index,
    "document.get": _cmd_document_get,
    "search": _cmd_search,
    "query": _cmd_query,
    "validate": _cmd_validate,
    "lint": _cmd_lint,
    "graph.dependencies": _cmd_graph,
    "platform": _cmd_platform,
    "repository.list": _cmd_repository_list,
    "workspace.current": _cmd_workspace_current,
    "workspace.list": _cmd_workspace_list,
    "workspace.open": _cmd_workspace_open,
    "property.list": _cmd_property_list,
    "property.navigator": _cmd_property_navigator,
    "instantiate.preview": _cmd_instantiate,
    "compile.plan": _cmd_compile,
    "compiler.pipeline": _cmd_compiler_pipeline,
    "review.repository": _cmd_review_repository,
    "report.architecture": _cmd_report_architecture,
    "git.status": _cmd_git_status,
    "git.diff": _cmd_git_diff,
    "git.history": _cmd_git_history,
    "git.branch": _cmd_git_branch,
    "plugin.list": _cmd_plugin_list,
    "ai.providers": _cmd_ai_providers,
    "jarvis.interface": _cmd_jarvis_interface,
    "events.list": _cmd_events_list,
    "build-bible.index": _cmd_build_bible_index,
    "digital-twin.status": _cmd_digital_twin_status,
}
