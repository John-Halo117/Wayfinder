"""Build a deterministic source manifest for ChatGPT export mining.

The manifest keeps rerun commands compact and avoids accidentally ingesting
duplicate temp copies of the same JSON export shard.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

DEFAULT_METADATA_STEMS: tuple[str, ...] = (
    "export_manifest",
    "conversation_asset_file_names",
    "library_files",
    "message_feedback",
    "shared_conversations",
    "user",
    "user_settings",
)


@dataclass(frozen=True)
class ManifestBuildResult:
    """Structured result for manifest construction."""

    output: str
    source_count: int
    conversation_shards: int
    metadata_json: int
    dat_files: int
    total_bytes: int


class ManifestBuildError(ValueError):
    """Raised when the source manifest cannot be built deterministically."""


def build_source_manifest(
    source_dir: Path,
    output: Path,
    *,
    conversation_version: int | None = None,
    metadata_stems: Sequence[str] = DEFAULT_METADATA_STEMS,
) -> ManifestBuildResult:
    """Write a deterministic source manifest from a temp export directory."""

    if not source_dir.is_dir():
        raise ManifestBuildError(f"source directory does not exist: {source_dir}")
    paths: list[Path] = []
    paths.extend(_select_conversation_shards(source_dir, conversation_version))
    for stem in metadata_stems:
        selected = _select_latest_named_json(source_dir, stem)
        if selected is not None:
            paths.append(selected)
    paths.extend(sorted(source_dir.glob("file_*.dat")))
    paths.extend(sorted(source_dir.glob("file-*.dat")))

    existing: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved.is_file() and resolved not in seen:
            existing.append(resolved)
            seen.add(resolved)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(str(path) for path in existing) + "\n", encoding="utf-8")
    return ManifestBuildResult(
        output=str(output),
        source_count=len(existing),
        conversation_shards=sum(1 for path in existing if path.name.startswith("conversations-")),
        metadata_json=sum(1 for path in existing if path.suffix.lower() == ".json" and not path.name.startswith("conversations-")),
        dat_files=sum(1 for path in existing if path.suffix.lower() == ".dat"),
        total_bytes=sum(path.stat().st_size for path in existing),
    )


def _select_conversation_shards(source_dir: Path, conversation_version: int | None) -> list[Path]:
    by_index: dict[int, list[tuple[int, Path]]] = {}
    pattern = re.compile(r"^conversations-(\d{3})(?: \((\d+)\))?\.json$")
    for path in source_dir.glob("conversations-*.json"):
        match = pattern.match(path.name)
        if not match:
            continue
        index = int(match.group(1))
        version = int(match.group(2) or 0)
        by_index.setdefault(index, []).append((version, path))
    selected: list[Path] = []
    for index in sorted(by_index):
        candidates = sorted(by_index[index], key=lambda item: (item[0], item[1].name))
        if conversation_version is None:
            selected.append(candidates[-1][1])
            continue
        matches = [path for version, path in candidates if version == conversation_version]
        if matches:
            selected.append(matches[-1])
    return selected


def _select_latest_named_json(source_dir: Path, stem: str) -> Path | None:
    pattern = re.compile(rf"^{re.escape(stem)}(?: \((\d+)\))?\.json$")
    candidates: list[tuple[int, str, Path]] = []
    for path in source_dir.glob(f"{stem}*.json"):
        match = pattern.match(path.name)
        if not match:
            continue
        candidates.append((int(match.group(1) or 0), path.name, path))
    if not candidates:
        return None
    return sorted(candidates)[-1][2]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a deterministic ChatGPT export source manifest.")
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--conversation-version", type=int, default=None)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = build_source_manifest(
        Path(args.source_dir),
        Path(args.output),
        conversation_version=args.conversation_version,
    )
    print(json.dumps(result.__dict__, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
