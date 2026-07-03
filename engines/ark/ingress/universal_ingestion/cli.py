"""CLI for the universal ingestion MVP.

Contract:
- Inputs: argv sequences from a local operator.
- Outputs: JSON summaries on stdout and process exit codes.
- Runtime constraint: bounded by IngestionConfig and selected command.
- Memory assumption: bounded by IngestionConfig.
- Failure cases: invalid arguments, unsupported command, failed ingestion, invalid
  query, and storage errors.
- Determinism: command results are deterministic except manifest timestamps.
"""

from __future__ import annotations

import argparse
from json import dumps
from pathlib import Path
from typing import Sequence

from .api import IngestionAPI
from .models import IngestionConfig, to_plain


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wf", description="Wayfinder ingestion MVP")
    parser.add_argument("--storage-root", default="ARK", help="Append-only storage root")
    subcommands = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subcommands.add_parser("ingest")
    ingest_parser.add_argument("ingest_args", nargs="+")

    search_parser = subcommands.add_parser("search")
    search_parser.add_argument("query")

    timeline_parser = subcommands.add_parser("timeline")
    timeline_parser.add_argument("query", nargs="?")

    subcommands.add_parser("imports")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    api = IngestionAPI(Path(args.storage_root), IngestionConfig())
    if args.command == "ingest":
        if len(args.ingest_args) == 1:
            result = api.ingest(Path(args.ingest_args[0]))
        elif len(args.ingest_args) == 2:
            result = api.ingest(args.ingest_args[0], Path(args.ingest_args[1]))
        else:
            parser = _parser()
            parser.error("ingest expects SOURCE or SUBSTRATE SOURCE")
        print(dumps(to_plain(result), sort_keys=True, ensure_ascii=False, default=str))
        return 0 if result.status == "ok" else 1
    if args.command == "search":
        result = api.search(args.query)
        print(dumps(to_plain(result), sort_keys=True, ensure_ascii=False, default=str))
        return 0 if result.status == "ok" else 1
    if args.command == "timeline":
        result = api.timeline(args.query)
        print(dumps(to_plain(result), sort_keys=True, ensure_ascii=False, default=str))
        return 0 if result.status == "ok" else 1
    if args.command == "imports":
        print(dumps(api.imports(), sort_keys=True, ensure_ascii=False, default=str))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
