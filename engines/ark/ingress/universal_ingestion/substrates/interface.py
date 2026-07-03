"""Canonical substrate interfaces for Universal Asset Ingestion.

Contract:
- Inputs: local source paths, import IDs, and bounded IngestionConfig caps.
- Outputs: substrate parse outputs containing observations, artifacts, and errors.
- Runtime constraint: adapter-specific but bounded by IngestionConfig.
- Memory assumption: adapter-specific but bounded by IngestionConfig.
- Failure cases: invalid source, unsupported source, malformed source, and cap exhaustion.
- Determinism: adapters must produce stable outputs for identical source bytes.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ..models import ArtifactRecord, Failure, IngestionConfig, ObservationRecord


@dataclass(frozen=True)
class SubstrateParseResult:
    """Normalized substrate output before append-only storage."""

    source_sha256: str
    observations: tuple[ObservationRecord, ...]
    artifacts: tuple[ArtifactRecord, ...]
    errors: tuple[Failure, ...]


class SubstrateAdapter(Protocol):
    """Protocol implemented by all substrate adapters."""

    substrate: str
    adapter: str
    parser_version: str

    def parse(self, source: Path, *, import_id: str) -> SubstrateParseResult:
        """Parse source into canonical observation and artifact candidates."""
