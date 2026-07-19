"""Deterministic rebuildable knowledge indexes."""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from hashlib import sha256
from json import dumps
from typing import Iterable, Mapping

from engines.interpretation.knowledge_governance.models import PromotionRecord, to_plain as governance_plain

from .models import (
    DEFAULT_INDEXED_AT,
    INDEX_TYPES,
    INDEX_VERSION,
    IndexManifest,
    IndexMutationResult,
    IndexValidationIssue,
    IndexVerificationResult,
    KnowledgeDocument,
    KnowledgeIndexLimits,
    RankingContribution,
    RetrievalMode,
    RetrievalResponse,
    RetrievalResult,
    to_plain,
)

TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,9}\b")
CAPABILITY_TERMS = {
    "capability",
    "capabilities",
    "provider",
    "providers",
    "service",
    "services",
    "engine",
    "engines",
    "contract",
    "contracts",
    "oracle",
    "storage",
    "identity",
    "event",
    "configuration",
    "policy",
}


class KnowledgeIndexStore:
    """Replaceable in-memory proof of knowledge indexing and retrieval."""

    def __init__(
        self,
        *,
        limits: KnowledgeIndexLimits = KnowledgeIndexLimits(),
        indexed_at: str = DEFAULT_INDEXED_AT,
    ) -> None:
        _validate_limits(limits)
        self._limits = limits
        self._indexed_at = indexed_at
        self._documents: dict[str, KnowledgeDocument] = {}
        self._manifest: IndexManifest | None = None
        self._token_index: dict[str, set[str]] = {}
        self._term_frequencies: dict[str, Counter[str]] = {}
        self._document_lengths: dict[str, int] = {}
        self._vectors: dict[str, tuple[float, ...]] = {}
        self._rid_index: dict[str, set[str]] = {}
        self._concept_index: dict[str, set[str]] = {}
        self._capability_index: dict[str, set[str]] = {}
        self._acronym_index: dict[str, set[str]] = {}
        self._relationship_index: dict[str, set[str]] = {}
        self._timeline: tuple[str, ...] = ()

    @property
    def manifest(self) -> IndexManifest | None:
        return self._manifest

    @property
    def documents(self) -> tuple[KnowledgeDocument, ...]:
        return tuple(sorted(self._documents.values(), key=lambda item: item.promotion_id))

    def delete_indexes(self) -> IndexMutationResult:
        """Delete every derived index and document projection."""

        self._documents = {}
        self._manifest = None
        self._clear_indexes()
        return IndexMutationResult(status="ok", manifest=None)

    def rebuild(self, promotions: Iterable[PromotionRecord]) -> IndexMutationResult:
        """Delete and rebuild every index from promoted knowledge."""

        promotion_records = tuple(sorted(promotions, key=lambda item: item.promotion_id))
        if len(promotion_records) > self._limits.max_documents:
            issue = _issue(
                "INDEX_DOCUMENT_LIMIT_EXCEEDED",
                "Promotion record count exceeds configured index limit.",
                {"limit": self._limits.max_documents, "count": len(promotion_records)},
                severity="error",
            )
            return IndexMutationResult(status="error", manifest=None, validation_report=(issue,))
        documents = tuple(_promotion_to_document(item) for item in promotion_records)
        issues_list = []
        for document in documents:
            issue = self._validate_document(document)
            if issue is not None:
                issues_list.append(issue)
        issues = tuple(issues_list)
        if any(item.severity == "error" for item in issues):
            return IndexMutationResult(status="error", manifest=None, validation_report=issues)
        self._documents = {item.promotion_id: item for item in documents}
        self._build_indexes()
        return IndexMutationResult(status="ok", manifest=self._manifest, validation_report=issues)

    def incremental_update(self, promotions: Iterable[PromotionRecord]) -> IndexMutationResult:
        """Update indexes with new or replacement promotion records."""

        incoming = tuple(sorted(promotions, key=lambda item: item.promotion_id))
        if len(self._documents) + len([item for item in incoming if item.promotion_id not in self._documents]) > self._limits.max_documents:
            issue = _issue(
                "INDEX_DOCUMENT_LIMIT_EXCEEDED",
                "Incremental update would exceed configured index limit.",
                {"limit": self._limits.max_documents},
                severity="error",
            )
            return IndexMutationResult("error", self._manifest, (issue,))
        issues = []
        for promotion in incoming:
            document = _promotion_to_document(promotion)
            issue = self._validate_document(document)
            if issue is not None:
                issues.append(issue)
                continue
            self._documents[document.promotion_id] = document
        if any(item.severity == "error" for item in issues):
            return IndexMutationResult("error", self._manifest, tuple(issues))
        self._build_indexes()
        return IndexMutationResult("ok", self._manifest, tuple(issues))

    def verify(self) -> IndexVerificationResult:
        """Verify index integrity without repairing it."""

        issues: list[IndexValidationIssue] = []
        if self._manifest is None:
            issues.append(
                _issue("MISSING_INDEXES", "No index manifest exists.", {}, severity="error")
            )
            return IndexVerificationResult("error", None, tuple(issues))
        if self._manifest.content_hash != self._content_hash():
            issues.append(
                _issue(
                    "STALE_INDEX",
                    "Index manifest hash does not match current document projections.",
                    {"manifest_hash": self._manifest.content_hash, "current_hash": self._content_hash()},
                    severity="error",
                )
            )
        for document in self._documents.values():
            if not document.provenance or not document.supporting_observations:
                issues.append(
                    _issue(
                        "MISSING_PROVENANCE",
                        "Indexed document is missing provenance.",
                        {"promotion_id": document.promotion_id},
                        severity="error",
                    )
                )
            for term in _tokens(document.text):
                if document.promotion_id not in self._token_index.get(term, set()):
                    issues.append(
                        _issue(
                            "BROKEN_INDEX_REFERENCE",
                            "Token index is missing a document reference.",
                            {"promotion_id": document.promotion_id, "term": term},
                            severity="error",
                        )
                    )
                    break
            if document.promotion_id not in self._vectors:
                issues.append(
                    _issue(
                        "EMBEDDING_DRIFT",
                        "Embedding index is missing a deterministic vector.",
                        {"promotion_id": document.promotion_id},
                        severity="error",
                    )
                )
            elif self._vectors[document.promotion_id] != _vector(_tokens(document.text), self._limits.embedding_dimensions):
                issues.append(
                    _issue(
                        "EMBEDDING_DRIFT",
                        "Embedding vector differs from deterministic rebuild.",
                        {"promotion_id": document.promotion_id},
                        severity="error",
                    )
                )
        indexed_ids = set()
        for index in (
            self._token_index,
            self._rid_index,
            self._concept_index,
            self._capability_index,
            self._acronym_index,
            self._relationship_index,
        ):
            for ids in index.values():
                indexed_ids.update(ids)
        for promotion_id in indexed_ids:
            if promotion_id not in self._documents:
                issues.append(
                    _issue(
                        "ORPHANED_INDEX_ENTRY",
                        "Index references a missing promoted knowledge document.",
                        {"promotion_id": promotion_id},
                        severity="error",
                    )
                )
        status = "ok" if not any(item.severity == "error" for item in issues) else "error"
        return IndexVerificationResult(status, self._manifest, tuple(sorted(issues, key=lambda item: item.issue_id)))

    def search(self, query: str, *, mode: RetrievalMode = "hybrid", limit: int = 10) -> RetrievalResponse:
        """Search promoted knowledge through one retrieval mode."""

        issues = self._query_issues(query, limit)
        if self._manifest is None:
            issues.append(_issue("MISSING_INDEXES", "Indexes must be built before retrieval.", {}, severity="error"))
            return RetrievalResponse(query=query, mode=mode, results=(), validation_report=tuple(issues))
        if issues:
            return RetrievalResponse(query=query, mode=mode, results=(), validation_report=tuple(issues))
        tokens = _query_terms(query, self._limits.max_query_terms)
        scores: dict[str, list[RankingContribution]] = defaultdict(list)
        if mode in {"full_text", "hybrid"}:
            for promotion_id, score, reason in self._full_text_scores(query, tokens):
                scores[promotion_id].append(RankingContribution("full_text", score, reason))
        if mode in {"bm25", "hybrid"}:
            for promotion_id, score, reason in self._bm25_scores(tokens):
                scores[promotion_id].append(RankingContribution("bm25", score, reason))
        if mode in {"embedding", "hybrid"}:
            for promotion_id, score, reason in self._embedding_scores(tokens):
                scores[promotion_id].append(RankingContribution("embedding", score, reason))
        if mode not in {"full_text", "bm25", "embedding", "hybrid"}:
            ids = self._lookup_ids(mode, query)
            for promotion_id in ids:
                scores[promotion_id].append(RankingContribution(mode, 1.0, f"{mode} lookup matched `{query}`"))
        results = self._rank(query, mode, tokens, scores, limit)
        return RetrievalResponse(query=query, mode=mode, results=results, validation_report=())

    def find(self, query: str, *, limit: int = 10) -> RetrievalResponse:
        return self.search(query, mode="hybrid", limit=limit)

    def lookup(self, reference_type: RetrievalMode, value: str, *, limit: int = 10) -> RetrievalResponse:
        """Lookup by RID, concept, capability, acronym, relationship, or promotion."""

        return self.search(value, mode=reference_type, limit=limit)

    def related(self, reference: str, *, limit: int = 10) -> RetrievalResponse:
        ids = self._relationship_index.get(reference, set()) | self._relationship_index.get(reference.lower(), set())
        scores = {
            promotion_id: [RankingContribution("relationship", 1.0, f"Relationship index links `{reference}`.")]
            for promotion_id in ids
        }
        return RetrievalResponse(
            query=reference,
            mode="relationship",
            results=self._rank(reference, "relationship", _tokens(reference), scores, limit),
        )

    def neighbors(self, reference: str, *, limit: int = 10) -> RetrievalResponse:
        return self.related(reference, limit=limit)

    def timeline(
        self,
        *,
        conversation_id: str | None = None,
        reverse: bool = False,
        limit: int = 100,
    ) -> RetrievalResponse:
        ids = list(reversed(self._timeline)) if reverse else list(self._timeline)
        results = []
        for promotion_id in ids:
            document = self._documents[promotion_id]
            if conversation_id and conversation_id not in document.supporting_conversations:
                continue
            results.append(
                RetrievalResult(
                    document=document,
                    score=1.0,
                    contributions=(RankingContribution("timeline", 1.0, "Chronological index order."),),
                    matched_terms=(),
                )
            )
            if len(results) >= min(limit, self._limits.max_results):
                break
        return RetrievalResponse(query=conversation_id or "*", mode="timeline", results=tuple(results))

    def history(self, candidate_id: str, *, limit: int = 100) -> RetrievalResponse:
        return self.lookup("relationship", candidate_id, limit=limit)

    def autocomplete(self, prefix: str, *, limit: int = 10) -> tuple[str, ...]:
        normalized = prefix.strip().lower()
        if not normalized:
            return ()
        terms = set(self._token_index) | set(self._concept_index) | set(self._capability_index) | set(self._acronym_index)
        return tuple(sorted(term for term in terms if term.startswith(normalized))[: min(limit, self._limits.max_results)])

    def suggestions(self, prefix: str, *, limit: int = 10) -> tuple[str, ...]:
        return self.autocomplete(prefix, limit=limit)

    def _clear_indexes(self) -> None:
        self._token_index = {}
        self._term_frequencies = {}
        self._document_lengths = {}
        self._vectors = {}
        self._rid_index = {}
        self._concept_index = {}
        self._capability_index = {}
        self._acronym_index = {}
        self._relationship_index = {}
        self._timeline = ()

    def _build_indexes(self) -> None:
        self._clear_indexes()
        for document in self._documents.values():
            tokens = _tokens(document.text)
            if len(tokens) > self._limits.max_terms_per_document:
                tokens = tokens[: self._limits.max_terms_per_document]
            frequencies = Counter(tokens)
            self._term_frequencies[document.promotion_id] = frequencies
            self._document_lengths[document.promotion_id] = sum(frequencies.values())
            self._vectors[document.promotion_id] = _vector(tokens, self._limits.embedding_dimensions)
            for term in frequencies:
                self._token_index.setdefault(term, set()).add(document.promotion_id)
            self._index_reference(self._rid_index, document.promotion_id, document.promotion_id)
            self._index_reference(self._rid_index, document.promoted_artifact_id, document.promotion_id)
            for value in (*document.supporting_reality_ids, *document.supporting_observations):
                self._index_reference(self._rid_index, value, document.promotion_id)
            for value in _concept_terms(document):
                self._index_reference(self._concept_index, value, document.promotion_id)
            for value in _capability_terms(document):
                self._index_reference(self._capability_index, value, document.promotion_id)
            for value in _acronyms(document.text):
                self._index_reference(self._acronym_index, value, document.promotion_id)
            for value in (
                document.promotion_id,
                document.promoted_artifact_id,
                *document.candidate_ids,
                *document.supporting_observations,
                *document.supporting_reality_ids,
                *document.supporting_conversations,
            ):
                self._index_reference(self._relationship_index, value, document.promotion_id)
        self._timeline = tuple(
            item.promotion_id
            for item in sorted(self._documents.values(), key=lambda doc: (doc.promoted_at, doc.promotion_id))
        )
        self._manifest = IndexManifest(
            index_version=INDEX_VERSION,
            indexed_at=self._indexed_at,
            document_count=len(self._documents),
            index_types=INDEX_TYPES,
            content_hash=self._content_hash(),
        )

    def _content_hash(self) -> str:
        payload = to_plain(tuple(sorted(self._documents.values(), key=lambda item: item.promotion_id)))
        return sha256(dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")).hexdigest()

    def _validate_document(self, document: KnowledgeDocument) -> IndexValidationIssue | None:
        if not document.promotion_id or not document.promoted_artifact_id:
            return _issue(
                "BROKEN_REFERENCE",
                "Knowledge document is missing promotion identity.",
                {"promotion_id": document.promotion_id},
                severity="error",
            )
        if not document.supporting_observations or not document.provenance:
            return _issue(
                "MISSING_PROVENANCE",
                "Knowledge document is missing promotion or observation provenance.",
                {"promotion_id": document.promotion_id},
                severity="error",
            )
        return None

    def _query_issues(self, query: str, limit: int) -> list[IndexValidationIssue]:
        issues = []
        if not query.strip():
            issues.append(_issue("QUERY_EMPTY", "Query is required.", {}, severity="error"))
        if limit <= 0 or limit > self._limits.max_results:
            issues.append(
                _issue(
                    "QUERY_LIMIT_INVALID",
                    "Result limit must be positive and within configured maximum.",
                    {"limit": limit, "max_results": self._limits.max_results},
                    severity="error",
                )
            )
        return issues

    def _full_text_scores(self, query: str, tokens: tuple[str, ...]) -> tuple[tuple[str, float, str], ...]:
        allowed = self._boolean_filter(query, tokens)
        phrase = " ".join(tokens)
        scores = []
        for document in self._documents.values():
            if allowed is not None and document.promotion_id not in allowed:
                continue
            matched = tuple(term for term in tokens if term in self._term_frequencies.get(document.promotion_id, {}))
            score = float(len(matched))
            if phrase and phrase in " ".join(_tokens(document.text)):
                score += 2.0
            if score > 0:
                scores.append((document.promotion_id, score, f"Matched {len(matched)} query terms and phrase bonus."))
        return tuple(scores)

    def _bm25_scores(self, tokens: tuple[str, ...]) -> tuple[tuple[str, float, str], ...]:
        if not tokens or not self._documents:
            return ()
        doc_count = len(self._documents)
        avg_len = sum(self._document_lengths.values()) / max(1, doc_count)
        k1 = 1.5
        b = 0.75
        scores = []
        for promotion_id, frequencies in self._term_frequencies.items():
            score = 0.0
            matched = 0
            doc_len = self._document_lengths.get(promotion_id, 0)
            for term in tokens:
                tf = frequencies.get(term, 0)
                if tf == 0:
                    continue
                matched += 1
                df = len(self._token_index.get(term, set()))
                idf = math.log(1 + (doc_count - df + 0.5) / (df + 0.5))
                score += idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / max(avg_len, 1.0)))
            if score > 0:
                scores.append((promotion_id, score, f"BM25 matched {matched} terms with deterministic lexical ranking."))
        return tuple(scores)

    def _embedding_scores(self, tokens: tuple[str, ...]) -> tuple[tuple[str, float, str], ...]:
        query_vector = _vector(tokens, self._limits.embedding_dimensions)
        scores = []
        for promotion_id, vector in self._vectors.items():
            score = _cosine(query_vector, vector)
            if score > 0:
                scores.append((promotion_id, score, "Deterministic token-vector similarity matched."))
        return tuple(scores)

    def _lookup_ids(self, mode: str, value: str) -> set[str]:
        normalized = value.strip().lower()
        if mode == "rid":
            return self._rid_index.get(value.strip(), set()) | self._rid_index.get(normalized, set())
        if mode == "concept":
            return self._concept_index.get(normalized, set())
        if mode == "capability":
            return self._capability_index.get(normalized, set())
        if mode == "acronym":
            return self._acronym_index.get(value.strip().upper(), set()) | self._acronym_index.get(normalized, set())
        if mode == "relationship":
            return self._relationship_index.get(value.strip(), set()) | self._relationship_index.get(normalized, set())
        return set()

    def _rank(
        self,
        query: str,
        mode: str,
        tokens: tuple[str, ...],
        scores: Mapping[str, list[RankingContribution]],
        limit: int,
    ) -> tuple[RetrievalResult, ...]:
        results = []
        for promotion_id, contributions in scores.items():
            if promotion_id not in self._documents:
                continue
            if mode == "hybrid":
                weighted = 0.0
                for contribution in contributions:
                    weight = {"full_text": 0.35, "bm25": 0.45, "embedding": 0.20}.get(contribution.index_name, 1.0)
                    weighted += contribution.score * weight
                score = weighted
            else:
                score = sum(item.score for item in contributions)
            matched_terms = tuple(
                term for term in tokens if term in self._term_frequencies.get(promotion_id, {})
            )
            results.append(
                RetrievalResult(
                    document=self._documents[promotion_id],
                    score=round(score, 6),
                    contributions=tuple(sorted(contributions, key=lambda item: item.index_name)),
                    matched_terms=matched_terms,
                )
            )
        return tuple(
            sorted(results, key=lambda item: (-item.score, item.document.promoted_at, item.document.promotion_id))[
                : min(limit, self._limits.max_results)
            ]
        )

    def _boolean_filter(self, query: str, tokens: tuple[str, ...]) -> set[str] | None:
        upper = query.upper()
        if " AND " not in upper and " OR " not in upper and " NOT " not in upper:
            return None
        if " OR " in upper:
            result: set[str] = set()
            for token in tokens:
                result.update(self._token_index.get(token, set()))
            return result
        include = set(self._documents)
        exclude: set[str] = set()
        negating = False
        for raw in query.split():
            op = raw.upper()
            if op in {"AND", "OR"}:
                continue
            if op == "NOT":
                negating = True
                continue
            term = _normalize_token(raw)
            ids = self._token_index.get(term, set())
            if negating:
                exclude.update(ids)
                negating = False
            else:
                include = include.intersection(ids)
        return include - exclude

    @staticmethod
    def _index_reference(index: dict[str, set[str]], value: str, promotion_id: str) -> None:
        text = value.strip()
        if not text:
            return
        index.setdefault(text, set()).add(promotion_id)
        index.setdefault(text.lower(), set()).add(promotion_id)


def _promotion_to_document(record: PromotionRecord) -> KnowledgeDocument:
    artifact = record.artifact
    provenance = record.provenance
    candidate_provenance = provenance.get("candidate_provenance", {})
    metadata = artifact.get("metadata", {})
    text = " ".join(
        str(part)
        for part in (
            artifact.get("title", ""),
            artifact.get("summary", ""),
            artifact.get("candidate_type", ""),
            artifact.get("uncertainty", ""),
            dumps(metadata, sort_keys=True, default=str),
            record.rationale,
            record.rollback,
        )
        if str(part).strip()
    )
    return KnowledgeDocument(
        promotion_id=record.promotion_id,
        promoted_artifact_id=record.promoted_artifact_id,
        target=record.target,
        version=record.version,
        title=str(artifact.get("title", "")),
        summary=str(artifact.get("summary", "")),
        text=text,
        promoted_at=record.promoted_at,
        candidate_ids=record.candidate_ids,
        supporting_observations=tuple(str(item) for item in candidate_provenance.get("supporting_observations", ())),
        supporting_reality_ids=tuple(str(item) for item in candidate_provenance.get("supporting_reality_ids", ())),
        supporting_conversations=tuple(str(item) for item in candidate_provenance.get("supporting_conversations", ())),
        supporting_messages=tuple(str(item) for item in candidate_provenance.get("supporting_messages", ())),
        source_oracles=tuple(str(item) for item in candidate_provenance.get("source_oracles", ())),
        compiler_version=str(candidate_provenance.get("compiler_version", "")) or None,
        promotion_version=record.version,
        confidence=float(artifact["confidence"]) if "confidence" in artifact else None,
        uncertainty=str(artifact.get("uncertainty", "")) or None,
        provenance=governance_plain(provenance),
    )


def _validate_limits(limits: KnowledgeIndexLimits) -> None:
    for field in ("max_documents", "max_terms_per_document", "max_results", "embedding_dimensions", "max_query_terms"):
        if getattr(limits, field) <= 0:
            raise ValueError(f"{field} must be positive")


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(_normalize_token(match) for match in TOKEN_RE.findall(text) if _normalize_token(match))


def _query_terms(query: str, limit: int) -> tuple[str, ...]:
    terms = []
    for token in _tokens(query):
        if token in {"and", "or", "not"}:
            continue
        terms.append(token)
        if len(terms) >= limit:
            break
    return tuple(dict.fromkeys(terms))


def _normalize_token(token: str) -> str:
    return token.strip().lower()


def _vector(tokens: tuple[str, ...], dimensions: int) -> tuple[float, ...]:
    values = [0.0] * dimensions
    for token, count in Counter(tokens).items():
        bucket = int(sha256(token.encode("utf-8")).hexdigest()[:8], 16) % dimensions
        values[bucket] += float(count)
    length = math.sqrt(sum(value * value for value in values))
    if length == 0:
        return tuple(values)
    return tuple(round(value / length, 12) for value in values)


def _cosine(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def _concept_terms(document: KnowledgeDocument) -> tuple[str, ...]:
    metadata = document.provenance
    terms = set()
    for value in (document.title, document.summary, document.target):
        for token in _tokens(value):
            if len(token) >= 4:
                terms.add(token)
    artifact_metadata = metadata.get("candidate_provenance", {})
    if isinstance(artifact_metadata, Mapping):
        for value in artifact_metadata.get("supporting_conversations", ()):
            terms.add(str(value).lower())
    return tuple(sorted(terms))


def _capability_terms(document: KnowledgeDocument) -> tuple[str, ...]:
    tokens = set(_tokens(document.text))
    return tuple(sorted(tokens.intersection(CAPABILITY_TERMS)))


def _acronyms(text: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(match.upper() for match in ACRONYM_RE.findall(text)))


def _issue(
    error_code: str,
    reason: str,
    context: Mapping[str, object],
    *,
    severity: str,
    recoverable: bool = True,
) -> IndexValidationIssue:
    payload = dumps({"error_code": error_code, "reason": reason, "context": context, "severity": severity}, sort_keys=True)
    issue_id = f"index-issue:{sha256(payload.encode('utf-8')).hexdigest()}"
    return IndexValidationIssue(
        issue_id=issue_id,
        severity=severity,  # type: ignore[arg-type]
        error_code=error_code,
        reason=reason,
        context=context,
        recoverable=recoverable,
    )
