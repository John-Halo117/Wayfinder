"""Command line interface for Wayfinder architecture intelligence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .doctor import ArchitectureDoctor, DoctorConfig, render_health_dashboard


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="wf", description="Wayfinder repository governance diagnostics.")
    subparsers = parser.add_subparsers(dest="command")
    _add_doctor_parser(subparsers.add_parser("doctor", help="Run the Architecture Doctor."))
    _add_doctor_parser(subparsers.add_parser("health", help="Alias for doctor."))
    architecture = subparsers.add_parser("architecture", help="Architecture governance commands.")
    architecture_sub = architecture.add_subparsers(dest="architecture_command")
    _add_doctor_parser(architecture_sub.add_parser("check", help="Validate repository architecture."))
    _add_doctor_parser(architecture_sub.add_parser("graph", help="Generate architecture graphs."), graph_only=True)
    return parser.parse_args(argv)


def _add_doctor_parser(parser: argparse.ArgumentParser, *, graph_only: bool = False) -> None:
    parser.add_argument("--repo-root", default=".", help="Repository root to scan.")
    parser.add_argument("--output-dir", default="docs/governance", help="Directory for generated reports.")
    parser.add_argument("--write", action="store_true", help="Write governance reports.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Console output format.")
    parser.add_argument("--fail-on-violations", action="store_true", help="Exit non-zero when error findings exist.")
    parser.add_argument("--max-files", type=int, default=DoctorConfig.max_files, help="Maximum files to scan.")
    parser.set_defaults(graph_only=graph_only)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command is None:
        args.command = "doctor"
    if args.command == "architecture" and args.architecture_command is None:
        args.architecture_command = "check"
    config = DoctorConfig(max_files=args.max_files)
    doctor = ArchitectureDoctor(Path(args.repo_root), config=config)
    report = doctor.run()
    if args.write:
        doctor.write_reports(report, Path(args.repo_root) / args.output_dir)
    if args.format == "json":
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(render_health_dashboard(report))
    if args.fail_on_violations and report.status != "pass":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
