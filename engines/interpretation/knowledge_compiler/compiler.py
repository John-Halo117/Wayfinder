"""Deterministic compiler from preserved reality to candidate knowledge."""

from __future__ import annotations

import re
from dataclasses import asdict, is_dataclass
from hashlib import sha256
from json import dumps
from typing import Any, Iterable, Mapping

from .models import (
    CANDIDATE_TYPES,
    COMPILER_VERSION,
    RULE_SET_VERSION,
    CandidateArtifact,
    CandidateProvenance,
    CompilerLimits,
    CompilerResult,
    CompilerValidationIssue,
    EvidenceReference,
    KnowledgeCompilerConfig,
    to_plain,
)

ARCHITECTURAL_TERMS = (
    "Reality",
    "Observation",
    "Evidence",
    "Provenance",
    "Representation",
    "Oracle",
    "ARK",
    "Knowledge Compiler",
    "Candidate Knowledge",
    "Jarvis",
    "Capsule",
    "Capability",
    "Provider",
    "Plugin",
    "Vault",
    "Knowledge Vault",
    "RID",
    "Weave",
    "Relationship",
    "Constitution",
    "Glossary",
    "ADR",
    "LVR",
    "Last Verified Reality",
)
DECISION_MARKERS = (
    "decide",
    "decided",
    "decision",
    "established",
    "canonical",
    "accepted",
    "renamed",
    "promoted",
    "boundary",
    "shall",
    "must",
)
PRINCIPLE_MARKERS = (
    "principle",
    "always",
    "never",
    "prefer",
    "reality precedes",
    "observe before",
    "preserve before",
    "capabilities are invariant",
    "implementations are replaceable",
)
TODO_MARKERS = (
    "todo",
    "fixme",
    "future work",
    "open question",
    "migration",
    "incomplete",
    "needs validation",
    "later phase",
)
AMENDMENT_MARKERS = (
    "constitutional",
    "constitution",
    "amendment",
    "promote",
    "canonical owner",
    "ownership rule",
    "new engine",
    "new capability",
    "new lifecycle",
)
CAPSULE_MARKERS = ("capsule", "continuity", "handoff", "re-entry", "context bundle")
CONFLICT_MARKERS = ("conflict", "contradiction", "versus", "vs.", "deprecated", "rename", "renamed")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+|\n+")
TERM_RE = re.compile(r"\b[A-Z][A-Za-z0-9]*(?:\s+[A-Z][A-Za-z0-9]*){0,3}\b")


class KnowledgeCompiler:
    """Produce deterministic candidate knowledge from ARK-preserved records."""

    def __init__(
        self,
        *,
        config: KnowledgeCompilerConfig = KnowledgeCompilerConfig(),
        limits: CompilerLimits = CompilerLimits(),
    ) -> None:
        _validate_limits(limits)
        self._config = config
        self._limits = limits
        self._known_terms = {_normalize_term(term) for term in config.known_terms if term.strip()}
        self._deprecated_terms = {
            _normalize_term(key): _normalize_term(value) for key, value in config.deprecated_terms.items()
        }
        self._ownership_terms = {
            _normalize_term(key): value.strip() for key, value in config.ownership_terms.items()
        }

    def compile(
        self,
        preserved_observations: Iterable[object],
        *,
        preserved_relationships: Iterable[object] = (),
    ) -> CompilerResult:
        """Compile preserved ARK observations into candidate artifacts."""

        observations = tuple(_as_mapping(item) for item in preserved_observations)
        relationships = tuple(_as_mapping(item) for item in preserved_relationships)
        _check_count("observations", len(observations), self._limits.max_observations)
        compile_id = _stable_id("knowledge-compile", observations, relationships, self._config.compiled_at)
        issues: list[CompilerValidationIssue] = []
        normalized = tuple(self._normalize_observation(item, issues) for item in observations)
        candidates: list[CandidateArtifact] = []

        candidates.extend(self._concept_candidates(normalized))
        candidates.extend(self._decision_candidates(normalized))
        candidates.extend(self._principle_candidates(normalized))
        candidates.extend(self._adr_candidates(normalized))
        candidates.extend(self._glossary_candidates(normalized))
        candidates.extend(self._amendment_candidates(normalized))
        candidates.extend(self._capsule_candidates(normalized))
        candidates.extend(self._todo_candidates(normalized))
        candidates.extend(self._novelty_candidates(normalized))
        candidates.extend(self._duplicate_candidates(normalized))
        candidates.extend(self._contradiction_candidates(normalized))
        candidates.extend(self._relationship_duplicate_candidates(relationships, normalized))

        deduped = tuple(sorted(_dedupe_candidates(candidates), key=lambda item: item.candidate_id))
        if len(deduped) > self._limits.max_candidates:
            issues.append(
                _issue(
                    "CANDIDATE_LIMIT_EXCEEDED",
                    "Compiler candidate count exceeds configured maximum.",
                    {"limit": self._limits.max_candidates, "candidate_count": len(deduped)},
                    severity="error",
                )
            )
            deduped = deduped[: self._limits.max_candidates]
        for candidate in deduped:
            if candidate.confidence < 0.5:
                issues.append(
                    _issue(
                        "LOW_CONFIDENCE_CANDIDATE",
                        "Candidate was emitted with low confidence and must remain uncertain.",
                        {"candidate_id": candidate.candidate_id, "candidate_type": candidate.candidate_type},
                        severity="warning",
                    )
                )
        status = "ok" if not any(issue.severity == "error" for issue in issues) else "error"
        return CompilerResult(
            status=status,
            compile_id=compile_id,
            compiler_version=COMPILER_VERSION,
            rule_set_version=RULE_SET_VERSION,
            compiled_at=self._config.compiled_at,
            candidates=deduped,
            validation_report=tuple(sorted(issues, key=lambda item: item.issue_id)),
        )

    def _normalize_observation(
        self,
        observation: Mapping[str, object],
        issues: list[CompilerValidationIssue],
    ) -> Mapping[str, object]:
        observation_id = str(observation.get("observation_id", "")).strip()
        raw_text = _extract_text(observation)
        if len(raw_text) > self._limits.max_raw_text_chars:
            raw_text = raw_text[: self._limits.max_raw_text_chars]
            issues.append(
                _issue(
                    "OBSERVATION_TEXT_TRUNCATED_FOR_COMPILATION",
                    "Observation text exceeded compiler inspection limit; candidate uncertainty increased.",
                    {"observation_id": observation_id, "limit": self._limits.max_raw_text_chars},
                    severity="warning",
                )
            )
        if len(dumps(to_plain(observation), sort_keys=True, default=str).encode("utf-8")) > self._limits.max_observation_bytes:
            issues.append(
                _issue(
                    "OBSERVATION_PAYLOAD_LIMIT_EXCEEDED",
                    "Observation payload exceeds compiler limit.",
                    {"observation_id": observation_id, "limit": self._limits.max_observation_bytes},
                    severity="error",
                )
            )
        provenance = observation.get("provenance")
        if not isinstance(provenance, Mapping):
            issues.append(
                _issue(
                    "MISSING_PROVENANCE",
                    "Preserved observation is missing provenance.",
                    {"observation_id": observation_id},
                    severity="error",
                )
            )
            provenance = {}
        if not observation_id:
            issues.append(
                _issue(
                    "MISSING_OBSERVATION_ID",
                    "Preserved observation is missing observation_id.",
                    {"content_hash": observation.get("content_hash")},
                    severity="error",
                )
            )
        return {
            "observation": observation,
            "observation_id": observation_id,
            "text": raw_text,
            "lower_text": raw_text.lower(),
            "terms": _extract_terms(raw_text, self._limits.max_terms_per_observation),
            "sentences": _sentences(raw_text),
            "provenance": provenance,
            "evidence": _evidence_reference(observation),
        }

    def _concept_candidates(self, observations: tuple[Mapping[str, object], ...]) -> tuple[CandidateArtifact, ...]:
        by_term: dict[str, list[Mapping[str, object]]] = {}
        canonical_lookup = {_normalize_term(term): term for term in ARCHITECTURAL_TERMS}
        for item in observations:
            observed_terms = set(item["terms"])
            for term in ARCHITECTURAL_TERMS:
                if _normalize_term(term) in observed_terms or term.lower() in item["lower_text"]:
                    by_term.setdefault(canonical_lookup[_normalize_term(term)], []).append(item)
            for term in observed_terms:
                if term not in self._known_terms and len(term) >= 3:
                    by_term.setdefault(_title_term(term), []).append(item)
        candidates: list[CandidateArtifact] = []
        for term, support in by_term.items():
            unique_support = _unique_obs(support)
            if len(unique_support) < 2 and _normalize_term(term) not in {_normalize_term(value) for value in ARCHITECTURAL_TERMS}:
                continue
            confidence = _confidence(0.45, len(unique_support), 0.08)
            candidates.append(
                self._candidate(
                    "concept",
                    f"Concept candidate: {term}",
                    f"Recurring concept-like term `{term}` appears in preserved observations.",
                    confidence,
                    "Candidate concept requires human review before promotion.",
                    unique_support,
                    {"term": term, "occurrences": len(unique_support)},
                )
            )
        return tuple(candidates)

    def _decision_candidates(self, observations: tuple[Mapping[str, object], ...]) -> tuple[CandidateArtifact, ...]:
        return self._sentence_candidates(
            observations,
            "decision",
            DECISION_MARKERS,
            "Decision candidate",
            "Sentence appears to record an architectural or operational decision.",
            base_confidence=0.56,
        )

    def _principle_candidates(self, observations: tuple[Mapping[str, object], ...]) -> tuple[CandidateArtifact, ...]:
        return self._sentence_candidates(
            observations,
            "principle",
            PRINCIPLE_MARKERS,
            "Principle candidate",
            "Sentence appears to express a reusable architectural principle.",
            base_confidence=0.58,
        )

    def _adr_candidates(self, observations: tuple[Mapping[str, object], ...]) -> tuple[CandidateArtifact, ...]:
        candidates = []
        for item in observations:
            text = item["lower_text"]
            if "adr" in text or ("decision" in text and ("because" in text or "tradeoff" in text)):
                candidates.append(
                    self._candidate(
                        "adr",
                        "ADR candidate",
                        "Observation appears to contain a decision plus rationale or explicit ADR language.",
                        0.62,
                        "Candidate ADR is not approved and needs governance review.",
                        (item,),
                        {"suggested_status": "proposed"},
                    )
                )
        return tuple(candidates)

    def _glossary_candidates(self, observations: tuple[Mapping[str, object], ...]) -> tuple[CandidateArtifact, ...]:
        candidates = []
        for item in observations:
            text = item["text"]
            lowered = item["lower_text"]
            if "means" in lowered or "definition" in lowered or "alias" in lowered or "deprecated" in lowered:
                terms = tuple(_title_term(term) for term in item["terms"][:8])
                candidates.append(
                    self._candidate(
                        "glossary",
                        "Glossary candidate",
                        "Observation appears to define, rename, alias, or deprecate terminology.",
                        0.6,
                        "Glossary update is only a candidate until reviewed.",
                        (item,),
                        {"terms": terms, "excerpt": _excerpt(text)},
                    )
                )
            for deprecated, replacement in self._deprecated_terms.items():
                if deprecated in lowered:
                    candidates.append(
                        self._candidate(
                            "glossary",
                            f"Deprecated terminology candidate: {_title_term(deprecated)}",
                            f"Observation uses deprecated term `{_title_term(deprecated)}`; preferred replacement is `{_title_term(replacement)}`.",
                            0.74,
                            "Deprecation evidence should be reconciled with current glossary.",
                            (item,),
                            {"deprecated_term": deprecated, "replacement": replacement},
                        )
                    )
        return tuple(candidates)

    def _amendment_candidates(self, observations: tuple[Mapping[str, object], ...]) -> tuple[CandidateArtifact, ...]:
        return self._sentence_candidates(
            observations,
            "amendment",
            AMENDMENT_MARKERS,
            "Constitutional amendment candidate",
            "Sentence may imply constitutional ownership or lifecycle evolution.",
            base_confidence=0.55,
        )

    def _capsule_candidates(self, observations: tuple[Mapping[str, object], ...]) -> tuple[CandidateArtifact, ...]:
        candidates = []
        by_conversation: dict[str, list[Mapping[str, object]]] = {}
        for item in observations:
            conversation_id = _conversation_id(item)
            if conversation_id:
                by_conversation.setdefault(conversation_id, []).append(item)
            if any(marker in item["lower_text"] for marker in CAPSULE_MARKERS):
                candidates.append(
                    self._candidate(
                        "capsule",
                        "Capsule candidate",
                        "Observation mentions continuity, handoff, re-entry, or capsule language.",
                        0.6,
                        "Candidate capsule needs review before continuity packaging.",
                        (item,),
                        {"conversation_id": conversation_id},
                    )
                )
        for conversation_id, support in sorted(by_conversation.items()):
            if len(support) >= 3:
                candidates.append(
                    self._candidate(
                        "capsule",
                        f"Capsule candidate: {conversation_id}",
                        "Conversation contains multiple preserved observations and may be useful as a continuity capsule.",
                        _confidence(0.5, len(support), 0.04),
                        "Grouping is structural, not semantic truth.",
                        tuple(support),
                        {"conversation_id": conversation_id, "observation_count": len(support)},
                    )
                )
        return tuple(candidates)

    def _todo_candidates(self, observations: tuple[Mapping[str, object], ...]) -> tuple[CandidateArtifact, ...]:
        return self._sentence_candidates(
            observations,
            "todo",
            TODO_MARKERS,
            "TODO candidate",
            "Sentence appears to capture future work, migration, validation, or an open question.",
            base_confidence=0.63,
        )

    def _novelty_candidates(self, observations: tuple[Mapping[str, object], ...]) -> tuple[CandidateArtifact, ...]:
        by_term: dict[str, list[Mapping[str, object]]] = {}
        for item in observations:
            for term in item["terms"]:
                if term not in self._known_terms and len(term) >= 3:
                    by_term.setdefault(term, []).append(item)
        candidates = []
        for term, support in sorted(by_term.items()):
            if len(support) < 2:
                continue
            candidates.append(
                self._candidate(
                    "novelty",
                    f"Novelty candidate: {_title_term(term)}",
                    "Term appears repeatedly but is not in the supplied known-knowledge baseline.",
                    _confidence(0.52, len(support), 0.06),
                    "Novelty is relative only to supplied baseline, not absolute truth.",
                    tuple(_unique_obs(support)),
                    {"term": _title_term(term)},
                )
            )
        return tuple(candidates)

    def _duplicate_candidates(self, observations: tuple[Mapping[str, object], ...]) -> tuple[CandidateArtifact, ...]:
        normalized_sentences: dict[str, list[Mapping[str, object]]] = {}
        for item in observations:
            for sentence in item["sentences"]:
                key = _normalize_sentence(sentence)
                if len(key) >= 24:
                    normalized_sentences.setdefault(key, []).append(item)
        candidates = []
        for sentence_key, support in sorted(normalized_sentences.items()):
            unique_support = tuple(_unique_obs(support))
            if len(unique_support) < 2:
                continue
            candidates.append(
                self._candidate(
                    "duplicate",
                    "Duplicate candidate",
                    "Multiple observations repeat substantially similar language.",
                    _confidence(0.62, len(unique_support), 0.07),
                    "Duplicate detection is lexical and may miss semantic differences.",
                    unique_support,
                    {"normalized_sentence": sentence_key},
                )
            )
        return tuple(candidates)

    def _contradiction_candidates(self, observations: tuple[Mapping[str, object], ...]) -> tuple[CandidateArtifact, ...]:
        candidates = []
        by_term: dict[str, list[Mapping[str, object]]] = {}
        for item in observations:
            if any(marker in item["lower_text"] for marker in CONFLICT_MARKERS):
                for term in item["terms"]:
                    by_term.setdefault(term, []).append(item)
        for term, support in sorted(by_term.items()):
            unique_support = tuple(_unique_obs(support))
            if len(unique_support) >= 1:
                candidates.append(
                    self._candidate(
                        "contradiction",
                        f"Contradiction candidate: {_title_term(term)}",
                        "Conflict, rename, deprecation, or contradiction language appears around this term.",
                        _confidence(0.46, len(unique_support), 0.06),
                        "Requires human review; lexical conflict markers do not prove contradiction.",
                        unique_support,
                        {"term": _title_term(term)},
                    )
                )
        for term, owner in sorted(self._ownership_terms.items()):
            conflicting = tuple(item for item in observations if term in item["lower_text"] and owner.lower() not in item["lower_text"])
            if len(conflicting) >= 2:
                candidates.append(
                    self._candidate(
                        "contradiction",
                        f"Ownership ambiguity candidate: {_title_term(term)}",
                        f"Term `{_title_term(term)}` appears without its expected owner `{owner}` in repeated observations.",
                        0.5,
                        "Owner omission is only a weak ambiguity signal.",
                        conflicting,
                        {"term": term, "expected_owner": owner},
                    )
                )
        return tuple(candidates)

    def _relationship_duplicate_candidates(
        self,
        relationships: tuple[Mapping[str, object], ...],
        observations: tuple[Mapping[str, object], ...],
    ) -> tuple[CandidateArtifact, ...]:
        if not relationships:
            return ()
        by_shape: dict[tuple[str, str, str], int] = {}
        for relationship in relationships:
            key = (
                str(relationship.get("relationship_type", "")),
                str(relationship.get("source_id", "")),
                str(relationship.get("target_id", "")),
            )
            by_shape[key] = by_shape.get(key, 0) + 1
        candidates = []
        support = tuple(observations[:2])
        for key, count in sorted(by_shape.items()):
            if count > 1 and support:
                candidates.append(
                    self._candidate(
                        "duplicate",
                        "Duplicate relationship candidate",
                        "Multiple preserved relationships share the same explicit type and endpoints.",
                        _confidence(0.65, count, 0.04),
                        "Relationship duplication is structural and requires topology review.",
                        support,
                        {"relationship_type": key[0], "source_id": key[1], "target_id": key[2], "count": count},
                    )
                )
        return tuple(candidates)

    def _sentence_candidates(
        self,
        observations: tuple[Mapping[str, object], ...],
        candidate_type: str,
        markers: tuple[str, ...],
        title: str,
        summary: str,
        *,
        base_confidence: float,
    ) -> tuple[CandidateArtifact, ...]:
        candidates = []
        for item in observations:
            for sentence in item["sentences"]:
                lowered = sentence.lower()
                if any(marker in lowered for marker in markers):
                    candidates.append(
                        self._candidate(
                            candidate_type,
                            title,
                            f"{summary} Excerpt: {_excerpt(sentence)}",
                            base_confidence,
                            "Rule-based candidate; wording may be contextual or aspirational.",
                            (item,),
                            {"marker_family": candidate_type, "excerpt": _excerpt(sentence)},
                        )
                    )
        return tuple(candidates)

    def _candidate(
        self,
        candidate_type: str,
        title: str,
        summary: str,
        confidence: float,
        uncertainty: str,
        support: tuple[Mapping[str, object], ...],
        metadata: Mapping[str, Any],
    ) -> CandidateArtifact:
        if candidate_type not in CANDIDATE_TYPES:
            raise ValueError("unsupported candidate type")
        support = tuple(_unique_obs(support))
        provenance = _candidate_provenance(support, self._config.compiled_at)
        payload = {
            "candidate_type": candidate_type,
            "title": title,
            "summary": summary,
            "supporting_observations": provenance.supporting_observations,
            "metadata": metadata,
        }
        return CandidateArtifact(
            candidate_id=_stable_id("knowledge-candidate", payload),
            candidate_type=candidate_type,  # type: ignore[arg-type]
            title=title,
            summary=summary,
            confidence=round(min(max(confidence, 0.0), 1.0), 4),
            uncertainty=uncertainty,
            status="proposed",
            provenance=provenance,
            metadata=_freeze_mapping(metadata),
        )


def _validate_limits(limits: CompilerLimits) -> None:
    for field in (
        "max_observations",
        "max_observation_bytes",
        "max_candidates",
        "max_terms_per_observation",
        "max_raw_text_chars",
    ):
        if getattr(limits, field) <= 0:
            raise ValueError(f"{field} must be positive")


def _check_count(name: str, count: int, limit: int) -> None:
    if count > limit:
        raise ValueError(f"{name} count exceeds configured maximum")


def _as_mapping(value: object) -> Mapping[str, object]:
    if is_dataclass(value):
        return _freeze_mapping(asdict(value))
    if isinstance(value, Mapping):
        return _freeze_mapping(value)
    if hasattr(value, "__dict__"):
        return _freeze_mapping(vars(value))
    raise TypeError("compiler inputs must be preserved-record mappings or dataclasses")


def _freeze_mapping(value: Mapping[str, object]) -> Mapping[str, object]:
    frozen: dict[str, object] = {}
    for key, item in value.items():
        if is_dataclass(item):
            frozen[str(key)] = _freeze_mapping(asdict(item))
        elif isinstance(item, Mapping):
            frozen[str(key)] = _freeze_mapping(item)
        elif isinstance(item, list):
            frozen[str(key)] = tuple(item)
        else:
            frozen[str(key)] = item
    return frozen


def _extract_text(observation: Mapping[str, object]) -> str:
    raw = observation.get("raw_observation", observation)
    pieces: list[str] = []
    _collect_text(raw, pieces)
    return "\n".join(piece for piece in pieces if piece.strip())


def _collect_text(value: object, pieces: list[str]) -> None:
    if value is None:
        return
    if isinstance(value, str):
        pieces.append(value)
        return
    if isinstance(value, Mapping):
        for key, item in sorted(value.items(), key=lambda entry: str(entry[0])):
            if str(key) in {"content_hash", "hash"}:
                continue
            _collect_text(item, pieces)
        return
    if isinstance(value, (tuple, list)):
        for item in value:
            _collect_text(item, pieces)


def _extract_terms(text: str, limit: int) -> tuple[str, ...]:
    terms = []
    for match in TERM_RE.findall(text):
        normalized = _normalize_term(match)
        if len(normalized) < 3:
            continue
        terms.append(normalized)
        if len(terms) >= limit:
            break
    return tuple(dict.fromkeys(terms))


def _sentences(text: str) -> tuple[str, ...]:
    sentences = []
    for sentence in SENTENCE_RE.split(text):
        normalized = " ".join(sentence.split())
        if len(normalized) >= 8:
            sentences.append(normalized)
    return tuple(sentences)


def _normalize_term(term: str) -> str:
    return " ".join(term.strip().lower().split())


def _title_term(term: str) -> str:
    return " ".join(part.capitalize() if not part.isupper() else part for part in term.split())


def _normalize_sentence(sentence: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", sentence.lower()).strip()


def _excerpt(text: str, limit: int = 160) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def _conversation_id(item: Mapping[str, object]) -> str | None:
    provenance = item.get("provenance")
    if isinstance(provenance, Mapping):
        value = provenance.get("conversation_id")
        if isinstance(value, str) and value.strip():
            return value.strip()
    observation = item.get("observation")
    if isinstance(observation, Mapping):
        value = observation.get("conversation_reference")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _evidence_reference(observation: Mapping[str, object]) -> EvidenceReference:
    provenance = observation.get("provenance")
    if not isinstance(provenance, Mapping):
        provenance = {}
    return EvidenceReference(
        observation_id=str(observation.get("observation_id", "")).strip(),
        reality_id=_nullable_text(observation.get("canonical_rid")),
        conversation_id=_nullable_text(provenance.get("conversation_id")),
        message_id=_nullable_text(provenance.get("message_id")),
        source_oracle=_nullable_text(observation.get("source")) or _nullable_text(provenance.get("parser_name")),
        timestamp=_nullable_text(observation.get("timestamp")),
        import_timestamp=_nullable_text(provenance.get("import_timestamp")),
        content_hash=_nullable_text(observation.get("content_hash")) or _nullable_text(provenance.get("hash")),
    )


def _candidate_provenance(
    support: tuple[Mapping[str, object], ...],
    compiled_at: str,
) -> CandidateProvenance:
    evidence = tuple(_evidence_from_normalized(item) for item in support)
    return CandidateProvenance(
        compiler_version=COMPILER_VERSION,
        rule_set_version=RULE_SET_VERSION,
        compiled_at=compiled_at,
        supporting_observations=tuple(_unique_text(item.observation_id for item in evidence)),
        supporting_reality_ids=tuple(_unique_text(item.reality_id for item in evidence if item.reality_id)),
        supporting_conversations=tuple(_unique_text(item.conversation_id for item in evidence if item.conversation_id)),
        supporting_messages=tuple(_unique_text(item.message_id for item in evidence if item.message_id)),
        supporting_timestamps=tuple(_unique_text(item.timestamp for item in evidence if item.timestamp)),
        source_oracles=tuple(_unique_text(item.source_oracle for item in evidence if item.source_oracle)),
        evidence=evidence,
    )


def _evidence_from_normalized(item: Mapping[str, object]) -> EvidenceReference:
    evidence = item.get("evidence")
    if isinstance(evidence, EvidenceReference):
        return evidence
    observation = item.get("observation")
    if isinstance(observation, Mapping):
        return _evidence_reference(observation)
    return EvidenceReference("", None, None, None, None, None, None, None)


def _unique_obs(items: Iterable[Mapping[str, object]]) -> list[Mapping[str, object]]:
    seen = set()
    unique = []
    for item in items:
        observation_id = str(item.get("observation_id", ""))
        if observation_id and observation_id not in seen:
            seen.add(observation_id)
            unique.append(item)
    return unique


def _unique_text(items: Iterable[str | None]) -> list[str]:
    seen = set()
    unique = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def _dedupe_candidates(candidates: Iterable[CandidateArtifact]) -> list[CandidateArtifact]:
    by_id: dict[str, CandidateArtifact] = {}
    for candidate in candidates:
        existing = by_id.get(candidate.candidate_id)
        if existing is None or candidate.confidence > existing.confidence:
            by_id[candidate.candidate_id] = candidate
    return list(by_id.values())


def _confidence(base: float, support_count: int, increment: float) -> float:
    return min(0.95, base + max(0, support_count - 1) * increment)


def _stable_id(prefix: str, *parts: object) -> str:
    payload = dumps(to_plain(parts), sort_keys=True, separators=(",", ":"), default=str)
    return f"{prefix}:{sha256(payload.encode('utf-8')).hexdigest()}"


def _issue(
    error_code: str,
    reason: str,
    context: Mapping[str, object],
    *,
    severity: str,
    recoverable: bool = True,
) -> CompilerValidationIssue:
    issue_id = _stable_id("compiler-issue", error_code, reason, context, severity)
    return CompilerValidationIssue(
        issue_id=issue_id,
        severity=severity,  # type: ignore[arg-type]
        error_code=error_code,
        reason=reason,
        context=_freeze_mapping(context),
        recoverable=recoverable,
    )


def _nullable_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
