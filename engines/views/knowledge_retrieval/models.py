"""Retrieval contracts for disposable knowledge indexes."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal, Mapping

DEFAULT_INDEXED_AT = "1970-01-01T00:00:00Z"
INDEX_VERSION = "1.0.0"
INDEX_TYPES: tuple[str, ...] = (
    "full_text",
    "bm25",
    "embedding",
    "hybrid",
    "timeline",
    "rid",
    "concept",
    "capability",
    "acronym",
    "relationship",
)

RetrievalMode = Literal[
    "full_text",
    "bm25",
    "embedding",
    "hybrid",
    "timeline",
    "rid",
    "concept",
    "capability",
    "acronym",
    "relationship",
]


@dataclass(frozen=True)
class KnowledgeIndexLimits:
    """Bounded resource limits for an index store."""

    max_documents: int = 100_000
    max_terms_per_document: int = 10_000
    max_results: int = 1_000
    embedding_dimensions: int = 64
    max_query_terms: int = 128


@dataclass(frozen=True)
class KnowledgeDocument:
    """Indexable projection of a durable promotion record."""

    promotion_id: str
    promoted_artifact_id: str
    target: str
    version: int
    title: str
    summary: str
    text: str
    promoted_at: str
    candidate_ids: tuple[str, ...]
    supporting_observations: tuple[str, ...]
    supporting_reality_ids: tuple[str, ...]
    supporting_conversations: tuple[str, ...]
    supporting_messages: tuple[str, ...]
    source_oracles: tuple[str, ...]
    compiler_version: str | None
    promotion_version: int
    confidence: float | None
    uncertainty: str | None
    provenance: Mapping[str, Any]


@dataclass(frozen=True)
class RankingContribution:
    """Explainable score contribution from one index."""

    index_name: str
    score: float
    reason: str


@dataclass(frozen=True)
class RetrievalResult:
    """Search result with preserved provenance."""

    document: KnowledgeDocument
    score: float
    contributions: tuple[RankingContribution, ...]
    matched_terms: tuple[str, ...]


@dataclass(frozen=True)
class RetrievalResponse:
    """Bounded deterministic retrieval response."""

    query: str
    mode: RetrievalMode
    results: tuple[RetrievalResult, ...]
    validation_report: tuple["IndexValidationIssue", ...] = ()


@dataclass(frozen=True)
class IndexManifest:
    """Index build metadata."""

    index_version: str
    indexed_at: str
    document_count: int
    index_types: tuple[str, ...]
    content_hash: str


@dataclass(frozen=True)
class IndexValidationIssue:
    """Index validation issue."""

    issue_id: str
    severity: Literal["info", "warning", "error"]
    error_code: str
    reason: str
    context: Mapping[str, object]
    recoverable: bool


@dataclass(frozen=True)
class IndexVerificationResult:
    """Verification result for rebuildable indexes."""

    status: str
    manifest: IndexManifest | None
    validation_report: tuple[IndexValidationIssue, ...]


@dataclass(frozen=True)
class IndexMutationResult:
    """Result for delete, rebuild, and update operations."""

    status: str
    manifest: IndexManifest | None
    validation_report: tuple[IndexValidationIssue, ...] = ()


def to_plain(value: Any) -> Any:
    """Convert retrieval records into JSON-ready values."""

    if hasattr(value, "__dataclass_fields__"):
        return to_plain(asdict(value))
    if isinstance(value, tuple):
        return [to_plain(item) for item in value]
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): to_plain(item) for key, item in value.items()}
    return value
