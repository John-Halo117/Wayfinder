"""Command line entry point for the ChatGPT export Oracle."""

from __future__ import annotations

import argparse

from .oracle import DEFAULT_IMPORT_TIMESTAMP, import_export, write_import_outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Import a ChatGPT export into canonical Oracle streams.")
    parser.add_argument("export_path", help="ChatGPT export directory, zip, or file")
    parser.add_argument("output_dir", help="Directory for deterministic import outputs")
    parser.add_argument(
        "--import-timestamp",
        default=DEFAULT_IMPORT_TIMESTAMP,
        help="Import timestamp to record in provenance. Defaults to a deterministic timestamp.",
    )
    args = parser.parse_args()

    result = import_export(args.export_path, import_timestamp=args.import_timestamp)
    write_import_outputs(result, args.export_path, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
