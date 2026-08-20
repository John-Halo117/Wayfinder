#!/usr/bin/env python3
"""Retired legacy autonomous-repair entrypoint.

Historical implementation remains recoverable from Git history. It is intentionally
non-executable as an autonomous repair mechanism because the legacy version used
shell execution without the current authority, rollback, and verification contracts.
"""
raise SystemExit(
    "Retired legacy entrypoint: use the current qualified repair/execution pipeline."
)
