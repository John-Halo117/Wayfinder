#!/usr/bin/env python3
"""Aurora canonical command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import aurora_core


OUTPUT_MODES = ("json", "human", "yaml", "markdown", "table", "graph")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aurora", description="Aurora engineering CLI.")
    parser.add_argument("--repo-root", default=str(aurora_core.default_runtime_config().repo_root))
    parser.add_argument("--source-root", action="append", dest="source_roots")
    parser.add_argument("--max-files", type=int, default=aurora_core.default_runtime_config().max_files)
    parser.add_argument("--max-file-bytes", type=int, default=aurora_core.default_runtime_config().max_file_bytes)
    parser.add_argument("--max-search-results", type=int, default=aurora_core.default_runtime_config().max_search_results)
    parser.add_argument("--max-graph-nodes", type=int, default=aurora_core.default_runtime_config().max_graph_nodes)
    parser.add_argument("--cache-ttl", type=float, default=aurora_core.default_runtime_config().cache_ttl_seconds)
    parser.add_argument("--git-timeout", type=float, default=aurora_core.default_runtime_config().git_timeout_seconds)
    parser.add_argument("--format", choices=OUTPUT_MODES, default="json")
    parser.add_argument("--debug", action="store_true")

    subparsers = parser.add_subparsers(dest="domain", required=True)

    subparsers.add_parser("catalog")
    subparsers.add_parser("health")
    subparsers.add_parser("index").add_argument("--force", action="store_true")

    document = subparsers.add_parser("document")
    document_sub = document.add_subparsers(dest="action", required=True)
    document_get = document_sub.add_parser("get")
    document_get.add_argument("path")

    search = subparsers.add_parser("search")
    search.add_argument("query")

    query = subparsers.add_parser("query")
    query.add_argument("expression")

    subparsers.add_parser("validate").add_argument("--force", action="store_true")
    subparsers.add_parser("lint").add_argument("--force", action="store_true")

    graph = subparsers.add_parser("graph")
    graph.add_argument("type", nargs="?", default="dependencies")

    subparsers.add_parser("platform")

    repository = subparsers.add_parser("repository")
    repository_sub = repository.add_subparsers(dest="action", required=True)
    repository_sub.add_parser("list")

    workspace = subparsers.add_parser("workspace")
    workspace_sub = workspace.add_subparsers(dest="action", required=True)
    workspace_sub.add_parser("current")
    workspace_sub.add_parser("list")
    workspace_open = workspace_sub.add_parser("open")
    workspace_open.add_argument("name")

    property_parser = subparsers.add_parser("property")
    property_sub = property_parser.add_subparsers(dest="action", required=True)
    property_sub.add_parser("list")
    property_nav = property_sub.add_parser("navigator")
    property_nav.add_argument("--object")

    instantiate = subparsers.add_parser("instantiate")
    instantiate.add_argument("pattern")
    instantiate.add_argument("--property", default="property-local")

    compile_parser = subparsers.add_parser("compile")
    compile_parser.add_argument("target", nargs="?", default="Digital Twin")

    compiler = subparsers.add_parser("compiler")
    compiler_sub = compiler.add_subparsers(dest="action", required=True)
    compiler_sub.add_parser("pipeline")

    review = subparsers.add_parser("review")
    review.add_argument("scope", nargs="?", default="repository")
    review.add_argument("--force", action="store_true")

    report = subparsers.add_parser("report")
    report.add_argument("kind", nargs="?", default="architecture")
    report.add_argument("--force", action="store_true")

    git = subparsers.add_parser("git")
    git_sub = git.add_subparsers(dest="action", required=True)
    for action in ("status", "diff", "history", "branch"):
        git_sub.add_parser(action)

    plugin = subparsers.add_parser("plugin")
    plugin_sub = plugin.add_subparsers(dest="action", required=True)
    plugin_sub.add_parser("list")

    ai = subparsers.add_parser("ai")
    ai_sub = ai.add_subparsers(dest="action", required=True)
    ai_sub.add_parser("providers")

    jarvis = subparsers.add_parser("jarvis")
    jarvis_sub = jarvis.add_subparsers(dest="action", required=True)
    jarvis_sub.add_parser("interface")

    events = subparsers.add_parser("events")
    events_sub = events.add_subparsers(dest="action", required=True)
    events_sub.add_parser("list")

    build_bible = subparsers.add_parser("build-bible")
    build_bible_sub = build_bible.add_subparsers(dest="action", required=True)
    build_bible_index = build_bible_sub.add_parser("index")
    build_bible_index.add_argument("--force", action="store_true")

    digital_twin = subparsers.add_parser("digital-twin")
    digital_twin_sub = digital_twin.add_subparsers(dest="action", required=True)
    digital_twin_sub.add_parser("status")

    return parser


def runtime_from_args(args: argparse.Namespace) -> aurora_core.RuntimeConfig:
    defaults = aurora_core.default_runtime_config()
    return aurora_core.RuntimeConfig(
        repo_root=Path(args.repo_root).resolve(),
        source_roots=tuple(args.source_roots or defaults.source_roots),
        max_files=args.max_files,
        max_file_bytes=args.max_file_bytes,
        max_search_results=args.max_search_results,
        max_graph_nodes=args.max_graph_nodes,
        cache_ttl_seconds=args.cache_ttl,
        git_timeout_seconds=args.git_timeout,
        debug=args.debug,
    )


def command_from_args(args: argparse.Namespace) -> tuple[str, dict[str, Any]]:
    domain = args.domain
    if domain in {"catalog", "health", "platform"}:
        return domain, {}
    if domain == "index":
        return "index", {"force": args.force}
    if domain == "document":
        return "document.get", {"path": args.path}
    if domain == "search":
        return "search", {"query": args.query}
    if domain == "query":
        return "query", {"expression": args.expression}
    if domain == "validate":
        return "validate", {"force": args.force}
    if domain == "lint":
        return "lint", {"force": args.force}
    if domain == "graph":
        return f"graph.{args.type}", {"type": args.type}
    if domain == "repository":
        return "repository.list", {}
    if domain == "workspace":
        if args.action == "open":
            return "workspace.open", {"name": args.name}
        return f"workspace.{args.action}", {}
    if domain == "property":
        if args.action == "navigator":
            return "property.navigator", {"object": args.object}
        return "property.list", {}
    if domain == "instantiate":
        return "instantiate.preview", {"pattern": args.pattern, "property": args.property}
    if domain == "compile":
        return "compile.plan", {"target": args.target}
    if domain == "compiler":
        return "compiler.pipeline", {}
    if domain == "review":
        return "review.repository", {"scope": args.scope, "force": args.force}
    if domain == "report":
        return "report.architecture", {"kind": args.kind, "force": args.force}
    if domain == "git":
        return f"git.{args.action}", {}
    if domain == "plugin":
        return "plugin.list", {}
    if domain == "ai":
        return "ai.providers", {}
    if domain == "jarvis":
        return "jarvis.interface", {}
    if domain == "events":
        return "events.list", {}
    if domain == "build-bible":
        return "build-bible.index", {"force": args.force}
    if domain == "digital-twin":
        return "digital-twin.status", {}
    raise aurora_core.AuroraCommandError("UNKNOWN_DOMAIN", "Aurora domain is not registered.", {"domain": domain}, True)


def render(payload: dict[str, Any], output_mode: str) -> str:
    if output_mode == "json":
        return json.dumps(payload, indent=2)
    if output_mode == "yaml":
        return to_yaml(payload)
    if output_mode == "markdown":
        return to_markdown(payload)
    if output_mode == "table":
        return to_table(payload)
    if output_mode == "graph":
        return to_graph(payload)
    return to_human(payload)


def to_human(payload: dict[str, Any]) -> str:
    lines = [
        f"Aurora command: {payload.get('command', 'unknown')}",
        f"Status: {payload.get('status', 'unknown')}",
    ]
    data = payload.get("data", {})
    if isinstance(data, dict):
        for key, value in list(data.items())[:12]:
            lines.append(f"{key}: {compact(value)}")
    return "\n".join(lines)


def to_markdown(payload: dict[str, Any]) -> str:
    lines = [f"# Aurora {payload.get('command', 'command')}", "", f"- Status: `{payload.get('status', 'unknown')}`"]
    data = payload.get("data", {})
    if isinstance(data, dict):
        for key, value in data.items():
            lines.append(f"- {key}: `{compact(value)}`")
    return "\n".join(lines)


def to_table(payload: dict[str, Any]) -> str:
    data = payload.get("data", {})
    rows = [["field", "value"], ["status", payload.get("status", "unknown")], ["command", payload.get("command", "unknown")]]
    if isinstance(data, dict):
        rows.extend([[key, compact(value)] for key, value in list(data.items())[:20]])
    widths = [max(len(str(row[index])) for row in rows) for index in range(2)]
    return "\n".join(f"{row[0]:<{widths[0]}}  {row[1]:<{widths[1]}}" for row in rows)


def to_graph(payload: dict[str, Any]) -> str:
    data = payload.get("data", {})
    graph = data.get("graph", data) if isinstance(data, dict) else {}
    if not isinstance(graph, dict) or "nodes" not in graph:
        return json.dumps(payload, indent=2)
    lines = ["graph TD"]
    for node in graph.get("nodes", [])[:80]:
        node_id = safe_mermaid_id(node.get("id", "node"))
        label = str(node.get("title") or node.get("path") or node.get("id"))
        lines.append(f'  {node_id}["{label[:80]}"]')
    for edge in graph.get("edges", [])[:160]:
        source = safe_mermaid_id(edge.get("source", "source"))
        target = safe_mermaid_id(edge.get("target", "target"))
        label = str(edge.get("type", "references"))
        lines.append(f'  {source} -- "{label}" --> {target}')
    return "\n".join(lines)


def to_yaml(value: Any, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.append(to_yaml(item, indent + 2))
            else:
                lines.append(f"{pad}{key}: {scalar(item)}")
        return "\n".join(lines)
    if isinstance(value, list):
        lines = []
        for item in value[:200]:
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(to_yaml(item, indent + 2))
            else:
                lines.append(f"{pad}- {scalar(item)}")
        return "\n".join(lines)
    return f"{pad}{scalar(value)}"


def compact(value: Any) -> str:
    if isinstance(value, list):
        return f"{len(value)} items"
    if isinstance(value, dict):
        return f"{len(value)} fields"
    return str(value)


def scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value)
    if any(char in text for char in [":", "#", "\n", "{", "}", "[", "]"]):
        return json.dumps(text)
    return text


def safe_mermaid_id(value: Any) -> str:
    text = "".join(char if char.isalnum() else "_" for char in str(value))
    return text or "node"


def main(argv: list[str] | None = None) -> int:
    argv = normalize_global_options(list(sys.argv[1:] if argv is None else argv))
    parser = build_parser()
    args = parser.parse_args(argv)
    command, params = command_from_args(args)
    try:
        payload = aurora_core.execute(command, params, runtime_from_args(args))
    except aurora_core.AuroraCommandError as exc:
        print(render(exc.payload(), args.format), file=sys.stderr)
        return 1
    print(render(payload, args.format))
    return 0


def normalize_global_options(argv: list[str]) -> list[str]:
    promoted: list[str] = []
    remaining: list[str] = []
    index = 0
    while index < len(argv):
        item = argv[index]
        if item == "--format" and index + 1 < len(argv):
            promoted.extend([item, argv[index + 1]])
            index += 2
            continue
        if item.startswith("--format="):
            promoted.append(item)
            index += 1
            continue
        remaining.append(item)
        index += 1
    return promoted + remaining


if __name__ == "__main__":
    raise SystemExit(main())
