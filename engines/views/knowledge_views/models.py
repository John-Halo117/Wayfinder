"""Contracts for disposable knowledge view projections."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal, Mapping

DEFAULT_VIEW_GENERATED_AT = "1970-01-01T00:00:00Z"
VIEWS_VERSION = "1.0.0"
VIEW_TYPES: tuple[str, ...] = (
    "timeline",
    "architecture",
    "conversation",
    "concept",
    "decision",
    "glossary",
    "capsule",
    "objective",
    "review_queue",
    "search_results",
    "composed",
)

ViewType = Literal[
    "timeline",
    "architecture",
    "conversation",
    "concept",
    "decision",
    "glossary",
    "capsule",
    "objective",
    "review_queue",
    "search_results",
    "composed",
]


@dataclass(frozen=True)
class ViewsLimits:
    """Bounded resource limits for view generation."""

    max_items: int = 10_000
    max_groups: int = 1_000
    max_filters: int = 32
    max_text_length: int = 4_096


@dataclass(frozen=True)
class ViewsConfig:
    """Stable view-generation configuration."""

    generated_at: str = DEFAULT_VIEW_GENERATED_AT
    visibility: str = "internal"
    permissions: tuple[str, ...] = ("read",)


@dataclass(frozen=True)
class ViewDefinition:
    """Self-describing view contract."""

    view_id: str
    view_type: ViewType
    purpose: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    dependencies: tuple[str, ...]
    filters: Mapping[str, Any]
    grouping: str
    sort_order: str
    refresh_strategy: str
    visibility: str
    permissions: tuple[str, ...]


@dataclass(frozen=True)
class ViewProvenance:
    """Traceability for one displayed item."""

    promotion_id: str | None
    promoted_artifact_id: str | None
    supporting_observations: tuple[str, ...]
    supporting_conversations: tuple[str, ...]
    supporting_messages: tuple[str, ...]
    source_oracles: tuple[str, ...]
    compiler_version: str | None
    promotion_version: int | None
    confidence: float | None
    uncertainty: str | None
    review_history: tuple[Mapping[str, Any], ...]
    promotion_history: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True)
class ViewItem:
    """Presentation item that references source knowledge."""

    item_id: str
    title: str
    item_type: str
    summary: str
    group: str | None
    sort_key: str
    fields: Mapping[str, Any]
    provenance: ViewProvenance


@dataclass(frozen=True)
class ViewValidationIssue:
    """View validation issue."""

    issue_id: str
    severity: Literal["info", "warning", "error"]
    error_code: str
    reason: str
    context: Mapping[str, object]
    recoverable: bool


@dataclass(frozen=True)
class ViewResult:
    """Complete deterministic view projection."""

    view_id: str
    view_type: ViewType
    generated_at: str
    definition: ViewDefinition
    items: tuple[ViewItem, ...]
    groups: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    validation_report: tuple[ViewValidationIssue, ...] = ()


def to_plain(value: Any) -> Any:
    """Convert view dataclasses into JSON-ready values."""

    if hasattr(value, "__dataclass_fields__"):
        return to_plain(asdict(value))
    if isinstance(value, tuple):
        return [to_plain(item) for item in value]
    if isinstance(value, list):
        return [to_plain(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): to_plain(item) for key, item in value.items()}
    return value
