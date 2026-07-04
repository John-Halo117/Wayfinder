"""Deterministic view projections over promoted and candidate knowledge."""

from __future__ import annotations

from hashlib import sha256
from json import dumps
from typing import Any, Mapping

from engines.interpretation.knowledge_governance.models import CandidateRecord, to_plain as governance_plain
from engines.views.knowledge_retrieval.models import KnowledgeDocument, RetrievalResponse, RetrievalResult
from engines.views.knowledge_retrieval.store import KnowledgeIndexStore

from .models import (
    DEFAULT_VIEW_GENERATED_AT,
    VIEWS_VERSION,
    VIEW_TYPES,
    ViewDefinition,
    ViewItem,
    ViewProvenance,
    ViewResult,
    ViewValidationIssue,
    ViewsConfig,
    ViewsLimits,
    ViewType,
    to_plain,
)


class KnowledgeViewsEngine:
    """Compose deterministic projections without owning knowledge."""

    def __init__(
        self,
        index_store: KnowledgeIndexStore,
        *,
        candidate_records: tuple[CandidateRecord, ...] = (),
        config: ViewsConfig = ViewsConfig(),
        limits: ViewsLimits = ViewsLimits(),
    ) -> None:
        _validate_limits(limits)
        self._index_store = index_store
        self._candidate_records = tuple(sorted(candidate_records, key=lambda item: item.candidate.candidate_id))
        self._config = config
        self._limits = limits

    def timeline(self, *, conversation_id: str | None = None, reverse: bool = False, limit: int = 100) -> ViewResult:
        response = self._index_store.timeline(conversation_id=conversation_id, reverse=reverse, limit=limit)
        items = tuple(
            self._item_from_document(
                result.document,
                item_type="timeline_entry",
                group=result.document.target,
                sort_key=f"{result.document.promoted_at}:{result.document.promotion_id}",
                extra={"matched_terms": result.matched_terms, "score": result.score},
            )
            for result in response.results
        )
        return self._view(
            "timeline",
            "Chronological history of promoted knowledge.",
            items,
            filters={"conversation_id": conversation_id, "reverse": reverse, "limit": limit},
            grouping="target",
            sort_order="promoted_at asc, promotion_id asc",
            validation_report=tuple(_index_issues(response.validation_report)),
        )

    def architecture(self) -> ViewResult:
        documents = self._documents()
        items = []
        for document in documents:
            lower = document.text.lower()
            groups = []
            if any(term in lower for term in ("engine", "engines")):
                groups.append("engines")
            if any(term in lower for term in ("service", "services", "storage", "identity", "event", "configuration", "policy")):
                groups.append("services")
            if any(term in lower for term in ("contract", "contracts")):
                groups.append("contracts")
            if any(term in lower for term in ("capability", "provider", "providers", "oracle")):
                groups.append("capabilities")
            for group in groups or ("architecture",):
                items.append(
                    self._item_from_document(
                        document,
                        item_type="architecture_reference",
                        group=group,
                        sort_key=f"{group}:{document.title}:{document.promotion_id}",
                        extra={"architecture_group": group},
                    )
                )
        return self._view(
            "architecture",
            "Architecture projection for engines, services, contracts, capabilities, dependencies, and ownership.",
            tuple(items),
            filters={},
            grouping="architecture_group",
            sort_order="group asc, title asc",
        )

    def conversation(self, conversation_id: str) -> ViewResult:
        response = self._index_store.timeline(conversation_id=conversation_id)
        items = []
        for result in response.results:
            document = result.document
            messages = document.supporting_messages or ("unknown-message",)
            for message_id in messages:
                items.append(
                    self._item_from_document(
                        document,
                        item_type="conversation_entry",
                        group=conversation_id,
                        sort_key=f"{message_id}:{document.promotion_id}",
                        extra={"conversation_id": conversation_id, "message_id": message_id},
                    )
                )
        return self._view(
            "conversation",
            "Conversation reconstruction from preserved observation references.",
            tuple(items),
            filters={"conversation_id": conversation_id},
            grouping="conversation_id",
            sort_order="message_id asc, promotion_id asc",
            validation_report=tuple(_index_issues(response.validation_report)),
        )

    def concept(self, concept: str) -> ViewResult:
        response = self._index_store.lookup("concept", concept)
        items = tuple(
            self._item_from_document(
                result.document,
                item_type="concept_reference",
                group=concept.lower(),
                sort_key=f"{result.document.promoted_at}:{result.document.title}:{result.document.promotion_id}",
                extra={"concept": concept, "score": result.score},
            )
            for result in response.results
        )
        return self._view(
            "concept",
            "Concept projection with support, related references, history, aliases, and promotion history.",
            items,
            filters={"concept": concept},
            grouping="concept",
            sort_order="promoted_at asc, title asc",
            validation_report=tuple(_index_issues(response.validation_report)),
        )

    def decision(self, query: str = "decision") -> ViewResult:
        response = self._index_store.search(query, mode="hybrid")
        items = tuple(
            self._item_from_document(
                result.document,
                item_type="decision_reference",
                group=result.document.target,
                sort_key=f"{result.document.promoted_at}:{result.document.promotion_id}",
                extra={"query": query, "score": result.score, "matched_terms": result.matched_terms},
            )
            for result in response.results
            if "decision" in result.document.text.lower() or result.document.target == "adr_repository"
        )
        return self._view(
            "decision",
            "Decision projection with evidence, supporting conversations, review history, and promotion history.",
            items,
            filters={"query": query},
            grouping="target",
            sort_order="promoted_at asc, promotion_id asc",
            validation_report=tuple(_index_issues(response.validation_report)),
        )

    def glossary(self) -> ViewResult:
        documents = self._documents()
        items = tuple(
            self._item_from_document(
                document,
                item_type="glossary_entry",
                group=document.target,
                sort_key=f"{document.title}:{document.promotion_id}",
                extra={
                    "aliases": _metadata_value(document, "aliases", ()),
                    "deprecated_terms": _metadata_value(document, "deprecated_terms", ()),
                    "owner": document.target,
                    "acronyms": tuple(term for term in document.text.split() if term.isupper()),
                },
            )
            for document in documents
            if document.target == "glossary" or "glossary" in document.text.lower() or "alias" in document.text.lower()
        )
        return self._view(
            "glossary",
            "Projected glossary entries, aliases, deprecated terms, owners, definitions, and acronyms.",
            items,
            filters={"target": "glossary"},
            grouping="owner",
            sort_order="title asc",
        )

    def capsule(self) -> ViewResult:
        documents = self._documents()
        items = tuple(
            self._item_from_document(
                document,
                item_type="capsule_reference",
                group="capsule_repository",
                sort_key=f"{document.promoted_at}:{document.promotion_id}",
                extra={"re_entry_context": document.summary},
            )
            for document in documents
            if document.target == "capsule_repository" or "capsule" in document.text.lower() or "continuity" in document.text.lower()
        )
        return self._view(
            "capsule",
            "Approved capsule projection preserving links to source observations.",
            items,
            filters={"target": "capsule_repository"},
            grouping="capsule_repository",
            sort_order="promoted_at asc",
        )

    def objective(self) -> ViewResult:
        documents = self._documents()
        items = tuple(
            self._item_from_document(
                document,
                item_type="objective_reference",
                group=_objective_group(document),
                sort_key=f"{_objective_group(document)}:{document.promoted_at}:{document.promotion_id}",
                extra={"progress": _objective_progress(document)},
            )
            for document in documents
            if any(term in document.text.lower() for term in ("objective", "todo", "progress", "dependency", "dependencies"))
        )
        return self._view(
            "objective",
            "Objective projection for related decisions, progress, dependencies, and open TODOs.",
            items,
            filters={},
            grouping="objective_status",
            sort_order="group asc, promoted_at asc",
        )

    def review_queue(self) -> ViewResult:
        items = tuple(self._item_from_candidate(record) for record in self._candidate_records)
        return self._view(
            "review_queue",
            "Candidate review queue for pending concepts, ADRs, glossary entries, amendments, conflicts, duplicates, and low-confidence items.",
            items,
            filters={"states": ("discovered", "under_review", "approved", "deferred")},
            grouping="candidate_type",
            sort_order="state asc, candidate_type asc, candidate_id asc",
        )

    def search_results(self, response: RetrievalResponse) -> ViewResult:
        items = tuple(
            self._item_from_retrieval_result(result)
            for result in response.results
        )
        return self._view(
            "search_results",
            "Search result presentation preserving ranking explanations and provenance.",
            items,
            filters={"query": response.query, "mode": response.mode},
            grouping="retrieval_mode",
            sort_order="score desc, promotion_id asc",
            validation_report=tuple(_index_issues(response.validation_report)),
        )

    def compose(self, *views: ViewResult, view_id: str = "composed") -> ViewResult:
        items: list[ViewItem] = []
        issues: list[ViewValidationIssue] = []
        for view in views:
            items.extend(view.items)
            issues.extend(view.validation_report)
        deduped = {item.item_id: item for item in items}
        return self._view(
            "composed",
            "Composed deterministic view projection.",
            tuple(deduped.values()),
            filters={"source_views": tuple(view.view_id for view in views), "composition_id": view_id},
            grouping="source_view_group",
            sort_order="source sort_key asc",
            validation_report=tuple(issues),
        )

    def _documents(self) -> tuple[KnowledgeDocument, ...]:
        return self._index_store.documents

    def _view(
        self,
        view_type: str,
        purpose: str,
        items: tuple[ViewItem, ...],
        *,
        filters: Mapping[str, Any],
        grouping: str,
        sort_order: str,
        validation_report: tuple[ViewValidationIssue, ...] = (),
    ) -> ViewResult:
        if view_type not in VIEW_TYPES:
            raise ValueError("unsupported view type")
        issues = list(validation_report)
        if len(filters) > self._limits.max_filters:
            issues.append(
                _issue(
                    "INVALID_FILTERS",
                    "Filter count exceeds configured maximum.",
                    {"view_type": view_type, "limit": self._limits.max_filters},
                    severity="error",
                )
            )
        if len(items) > self._limits.max_items:
            issues.append(
                _issue(
                    "VIEW_ITEM_LIMIT_EXCEEDED",
                    "View item count exceeds configured maximum.",
                    {"view_type": view_type, "limit": self._limits.max_items},
                    severity="error",
                )
            )
            items = items[: self._limits.max_items]
        for item in items:
            if not item.provenance.supporting_observations and item.provenance.promotion_id is not None:
                issues.append(
                    _issue(
                        "MISSING_PROVENANCE",
                        "Displayed item is missing supporting observation provenance.",
                        {"item_id": item.item_id},
                        severity="error",
                    )
                )
        sorted_items = tuple(sorted(items, key=lambda item: (item.group or "", item.sort_key, item.item_id)))
        groups = _groups(sorted_items)
        if len(groups) > self._limits.max_groups:
            issues.append(
                _issue(
                    "VIEW_GROUP_LIMIT_EXCEEDED",
                    "View group count exceeds configured maximum.",
                    {"view_type": view_type, "limit": self._limits.max_groups},
                    severity="error",
                )
            )
        definition = ViewDefinition(
            view_id=_stable_id("view-definition", view_type, filters, grouping, sort_order),
            view_type=view_type,  # type: ignore[arg-type]
            purpose=purpose,
            inputs=("durable_knowledge", "knowledge_retrieval"),
            outputs=("view_projection",),
            dependencies=("Knowledge Retrieval", "Knowledge Governance", "Promotion Records"),
            filters=dict(filters),
            grouping=grouping,
            sort_order=sort_order,
            refresh_strategy="regenerate_from_promoted_knowledge",
            visibility=self._config.visibility,
            permissions=self._config.permissions,
        )
        return ViewResult(
            view_id=_stable_id("view", view_type, filters, tuple(item.item_id for item in sorted_items)),
            view_type=view_type,  # type: ignore[arg-type]
            generated_at=self._config.generated_at,
            definition=definition,
            items=sorted_items,
            groups=groups,
            validation_report=tuple(sorted(issues, key=lambda item: item.issue_id)),
        )

    def _item_from_document(
        self,
        document: KnowledgeDocument,
        *,
        item_type: str,
        group: str | None,
        sort_key: str,
        extra: Mapping[str, Any],
    ) -> ViewItem:
        return ViewItem(
            item_id=_stable_id("view-item", item_type, document.promotion_id, group, sort_key, extra),
            title=_truncate(document.title, self._limits.max_text_length),
            item_type=item_type,
            summary=_truncate(document.summary, self._limits.max_text_length),
            group=group,
            sort_key=sort_key,
            fields={
                "target": document.target,
                "promoted_at": document.promoted_at,
                "candidate_ids": document.candidate_ids,
                **dict(extra),
            },
            provenance=_provenance_from_document(document),
        )

    def _item_from_retrieval_result(self, result: RetrievalResult) -> ViewItem:
        return self._item_from_document(
            result.document,
            item_type="search_result",
            group="retrieval",
            sort_key=f"{1_000_000 - int(result.score * 1000):08d}:{result.document.promotion_id}",
            extra={
                "score": result.score,
                "matched_terms": result.matched_terms,
                "ranking": tuple(to_plain(item) for item in result.contributions),
            },
        )

    def _item_from_candidate(self, record: CandidateRecord) -> ViewItem:
        candidate = record.candidate
        return ViewItem(
            item_id=_stable_id("view-item", "review_queue", candidate.candidate_id, record.state),
            title=_truncate(candidate.title, self._limits.max_text_length),
            item_type="review_queue_entry",
            summary=_truncate(candidate.summary, self._limits.max_text_length),
            group=candidate.candidate_type,
            sort_key=f"{record.state}:{candidate.candidate_type}:{candidate.candidate_id}",
            fields={
                "candidate_id": candidate.candidate_id,
                "candidate_type": candidate.candidate_type,
                "state": record.state,
                "confidence": candidate.confidence,
                "uncertainty": candidate.uncertainty,
                "group_id": record.group_id,
            },
            provenance=ViewProvenance(
                promotion_id=None,
                promoted_artifact_id=None,
                supporting_observations=candidate.provenance.supporting_observations,
                supporting_conversations=candidate.provenance.supporting_conversations,
                supporting_messages=candidate.provenance.supporting_messages,
                source_oracles=candidate.provenance.source_oracles,
                compiler_version=candidate.provenance.compiler_version,
                promotion_version=None,
                confidence=candidate.confidence,
                uncertainty=candidate.uncertainty,
                review_history=tuple(governance_plain(item) for item in record.review_history),
                promotion_history=tuple(governance_plain(item) for item in record.promotion_history),
            ),
        )


def _validate_limits(limits: ViewsLimits) -> None:
    for field in ("max_items", "max_groups", "max_filters", "max_text_length"):
        if getattr(limits, field) <= 0:
            raise ValueError(f"{field} must be positive")


def _provenance_from_document(document: KnowledgeDocument) -> ViewProvenance:
    review_history = ()
    promotion_history = ()
    if isinstance(document.provenance, Mapping):
        review_history = tuple(document.provenance.get("review_history", ()) or ())
        promotion_history = tuple(document.provenance.get("promotion_history", ()) or ())
    return ViewProvenance(
        promotion_id=document.promotion_id,
        promoted_artifact_id=document.promoted_artifact_id,
        supporting_observations=document.supporting_observations,
        supporting_conversations=document.supporting_conversations,
        supporting_messages=document.supporting_messages,
        source_oracles=document.source_oracles,
        compiler_version=document.compiler_version,
        promotion_version=document.promotion_version,
        confidence=document.confidence,
        uncertainty=document.uncertainty,
        review_history=review_history,
        promotion_history=promotion_history,
    )


def _metadata_value(document: KnowledgeDocument, key: str, default: Any) -> Any:
    candidate_metadata = document.provenance.get("candidate_provenance", {}) if isinstance(document.provenance, Mapping) else {}
    if isinstance(candidate_metadata, Mapping) and key in candidate_metadata:
        return candidate_metadata[key]
    return default


def _objective_group(document: KnowledgeDocument) -> str:
    lower = document.text.lower()
    if "todo" in lower:
        return "open_todo"
    if "dependency" in lower or "dependencies" in lower:
        return "dependency"
    if "progress" in lower:
        return "progress"
    return "objective"


def _objective_progress(document: KnowledgeDocument) -> str:
    lower = document.text.lower()
    if "todo" in lower:
        return "open"
    if document.target == "execution_backlog":
        return "backlog"
    return "related"


def _groups(items: tuple[ViewItem, ...]) -> Mapping[str, tuple[str, ...]]:
    grouped: dict[str, list[str]] = {}
    for item in items:
        group = item.group or "ungrouped"
        grouped.setdefault(group, []).append(item.item_id)
    return {key: tuple(value) for key, value in sorted(grouped.items())}


def _index_issues(issues: tuple[object, ...]) -> tuple[ViewValidationIssue, ...]:
    converted = []
    for issue in issues:
        converted.append(
            _issue(
                getattr(issue, "error_code", "INDEX_VALIDATION_ISSUE"),
                getattr(issue, "reason", "index validation issue"),
                dict(getattr(issue, "context", {}) or {}),
                severity=getattr(issue, "severity", "error"),
                recoverable=getattr(issue, "recoverable", True),
            )
        )
    return tuple(converted)


def _issue(
    error_code: str,
    reason: str,
    context: Mapping[str, object],
    *,
    severity: str,
    recoverable: bool = True,
) -> ViewValidationIssue:
    payload = dumps({"error_code": error_code, "reason": reason, "context": context, "severity": severity}, sort_keys=True)
    return ViewValidationIssue(
        issue_id=f"view-issue:{sha256(payload.encode('utf-8')).hexdigest()}",
        severity=severity,  # type: ignore[arg-type]
        error_code=error_code,
        reason=reason,
        context=context,
        recoverable=recoverable,
    )


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _stable_id(prefix: str, *parts: object) -> str:
    payload = dumps(to_plain(parts), sort_keys=True, separators=(",", ":"), default=str)
    return f"{prefix}:{sha256(payload.encode('utf-8')).hexdigest()}"
