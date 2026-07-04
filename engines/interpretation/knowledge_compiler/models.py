"""Candidate artifact contracts for the Knowledge Compiler."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal, Mapping

DEFAULT_COMPILED_AT = "1970-01-01T00:00:00Z"
COMPILER_VERSION = "1.0.0"
RULE_SET_VERSION = "1.0.0"

CandidateKind = Literal[
    "concept",
    "decision",
    "principle",
    "adr",
    "glossary",
    "amendment",
    "capsule",
    "todo",
    "novelty",
    "duplicate",
    "contradiction",
]
CANDIDATE_TYPES: tuple[str, ...] = (
    "concept",
    "decision",
    "principle",
    "adr",
    "glossary",
    "amendment",
    "capsule",
    "todo",
    "novelty",
    "duplicate",
    "contradiction",
)


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
class EvidenceReference:
    """Traceable support from a preserved observation."""

    observation_id: str
    reality_id: str | None
    conversation_id: str | None
    message_id: str | None
    source_oracle: str | None
    timestamp: str | None
    import_timestamp: str | None
    content_hash: str | None


@dataclass(frozen=True)
class CandidateProvenance:
    """Compiler provenance attached to every candidate artifact."""

    compiler_version: str
    rule_set_version: str
    compiled_at: str
    supporting_observations: tuple[str, ...]
    supporting_reality_ids: tuple[str, ...]
    supporting_conversations: tuple[str, ...]
    supporting_messages: tuple[str, ...]
    supporting_timestamps: tuple[str, ...]
    source_oracles: tuple[str, ...]
    evidence: tuple[EvidenceReference, ...]


@dataclass(frozen=True)
class CandidateArtifact:
    """A proposed knowledge artifact, never canonical truth."""

    candidate_id: str
    candidate_type: CandidateKind
    title: str
    summary: str
    confidence: float
    uncertainty: str
    status: str
    provenance: CandidateProvenance
    metadata: Mapping[str, Any] = field(default_factory=dict)


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


def to_plain(value: Any) -> Any:
    """Convert compiler dataclasses into JSON-ready values."""

    if hasattr(value, "__dataclass_fields__"):
        return to_plain(asdict(value))
    if isinstance(value, tuple):
        return [to_plain(item) for item in value]
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): to_plain(item) for key, item in value.items()}
    return value
