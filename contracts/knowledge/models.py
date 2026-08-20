"""Canonical data contracts exchanged across knowledge layers.

These shapes are deliberately implementation-neutral. Compiler, governance, and
retrieval may produce or consume them, but none of those implementations owns the
schema merely because it currently creates an instance.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal, Mapping

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

PromotionTargetName = Literal[
    "glossary",
    "constitution",
    "adr_repository",
    "capsule_repository",
    "execution_backlog",
    "knowledge_repository",
]
PROMOTION_TARGETS: tuple[str, ...] = (
    "glossary",
    "constitution",
    "adr_repository",
    "capsule_repository",
    "execution_backlog",
    "knowledge_repository",
)


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
    """Provenance attached to every proposed knowledge candidate."""

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
class PromotionRecord:
    """Durable human-governed promotion record consumed by downstream projections."""

    promotion_id: str
    version: int
    target: PromotionTargetName
    promoted_artifact_id: str
    candidate_ids: tuple[str, ...]
    reviewer: str
    rationale: str
    rollback: str
    promoted_at: str
    artifact: Mapping[str, Any]
    provenance: Mapping[str, Any]


def to_plain(value: Any) -> Any:
    """Convert contract dataclasses into JSON-ready values."""

    if hasattr(value, "__dataclass_fields__"):
        return to_plain(asdict(value))
    if isinstance(value, tuple):
        return [to_plain(item) for item in value]
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): to_plain(item) for key, item in value.items()}
    return value
