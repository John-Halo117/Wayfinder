#!/usr/bin/env python3
"""Wayfinder CLI wrapper.

Contract:
- Inputs: bounded argv sequences accepted by the universal ingestion CLI.
- Outputs: JSON command output and process exit codes.
- Runtime constraint: delegated command runtime bounded by IngestionConfig.
- Memory assumption: delegated command memory bounded by IngestionConfig.
- Failure cases: invalid arguments or delegated structured failures.
- Determinism: delegated command behavior is deterministic except timestamps.
"""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from engines.ark.ingress.universal_ingestion.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
