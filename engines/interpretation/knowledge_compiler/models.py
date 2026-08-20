"""Knowledge Compiler configuration and result models.

Cross-layer candidate/provenance shapes are owned by contracts.knowledge and are
re-exported here for compatibility with existing compiler consumers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping

from contracts.knowledge.models import (
    CANDIDATE_TYPES,
    CandidateArtifact,
    CandidateKind,
    CandidateProvenance,
    EvidenceReference,
    to_plain,
)

DEFAULT_COMPILED_AT = "1970-01-01T00:00:00Z"
COMPILER_VERSION = "1.0.0"
RULE_SET_VERSION = "1.0.0"


@dataclass(frozen=True)
class CompilerLimits:
    """Bounded resource limits for deterministic compilation."""

    max_observations: int = 100_000
    max_observation_bytes: int = 2 * 1024 * 1024
    max_candidates: int = 100_000
    max_terms_per_observation: int = 256
    max_raw_text_chars: int = 200_000


@dataclass(frozen=True)
class KnowledgeCompilerConfig:
    """Compiler configuration and existing knowledge baseline."""

    known_terms: tuple[str, ...] = ()
    deprecated_terms: Mapping[str, str] = field(default_factory=dict)
    ownership_terms: Mapping[str, str] = field(default_factory=dict)
    compiled_at: str = DEFAULT_COMPILED_AT


@dataclass(frozen=True)
class CompilerValidationIssue:
    """Validation issue emitted without discarding uncertainty."""

    issue_id: str
    severity: Literal["info", "warning", "error"]
    error_code: str
    reason: str
    context: Mapping[str, Any]
    recoverable: bool


@dataclass(frozen=True)
class CompilerResult:
    """Complete deterministic compiler output."""

    status: str
    compile_id: str
    compiler_version: str
    rule_set_version: str
    compiled_at: str
    candidates: tuple[CandidateArtifact, ...]
    validation_report: tuple[CompilerValidationIssue, ...]
