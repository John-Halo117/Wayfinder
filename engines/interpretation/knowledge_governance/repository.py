"""Candidate repository and promotion target implementations."""

from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
from json import dumps
from typing import Mapping, Protocol

from engines.interpretation.knowledge_compiler.models import CandidateArtifact, to_plain as compiler_plain

from .models import (
    DEFAULT_REVIEWED_AT,
    PROMOTION_TARGETS,
    CandidateGroup,
    CandidateRecord,
    GovernanceActionResult,
    GovernanceLimits,
    GovernanceValidationIssue,
    MergeHistoryEntry,
    PromotionRecord,
    PromotionTargetName,
    REVIEW_STATES,
    ReviewEvent,
    ReviewEventRecord,
    ReviewHistoryEntry,
    ReviewState,
    ReviewView,
    to_plain,
)

VALID_TRANSITIONS: Mapping[str, tuple[str, ...]] = {
    "discovered": ("under_review",),
    "under_review": ("approved", "rejected", "deferred", "superseded"),
    "approved": ("promoted", "superseded"),
    "rejected": (),
    "deferred": ("under_review", "superseded"),
    "superseded": (),
    "promoted": (),
}


class PromotionTarget(Protocol):
    """Promotion target repository boundary."""

    def store(self, record: PromotionRecord) -> GovernanceActionResult:
        """Store a durable promoted knowledge record."""


class InMemoryPromotionTarget:
    """Bounded in-memory promotion target proof."""

    def __init__(self, target: PromotionTargetName, *, max_records: int = 100_000) -> None:
        if target not in PROMOTION_TARGETS:
            raise ValueError("invalid promotion target")
        if max_records <= 0:
            raise ValueError("max_records must be positive")
        self._target = target
        self._max_records = max_records
        self._records: dict[str, PromotionRecord] = {}

    @property
    def records(self) -> tuple[PromotionRecord, ...]:
        return tuple(sorted(self._records.values(), key=lambda item: item.promotion_id))

    def store(self, record: PromotionRecord) -> GovernanceActionResult:
        if record.target != self._target:
            issue = _issue(
                "INVALID_PROMOTION_TARGET",
                "Promotion record target does not match target repository.",
                {"promotion_id": record.promotion_id, "target": record.target, "repository": self._target},
                severity="error",
                recoverable=False,
            )
            return GovernanceActionResult("error", (), validation_report=(issue,))
        existing = self._records.get(record.promotion_id)
        if existing is not None:
            if to_plain(existing) == to_plain(record):
                return GovernanceActionResult("ok", (), promotion_records=(existing,))
            issue = _issue(
                "DUPLICATE_PROMOTION",
                "Promotion ID already exists with different content.",
                {"promotion_id": record.promotion_id},
                severity="error",
                recoverable=False,
            )
            return GovernanceActionResult("error", (), validation_report=(issue,))
        if len(self._records) >= self._max_records:
            issue = _issue(
                "PROMOTION_TARGET_LIMIT",
                "Promotion target record limit exceeded.",
                {"target": self._target, "limit": self._max_records},
                severity="error",
            )
            return GovernanceActionResult("error", (), validation_report=(issue,))
        self._records[record.promotion_id] = record
        return GovernanceActionResult("ok", (), promotion_records=(record,))


class CandidateRepository:
    """Deterministic repository for candidate review and promotion state."""

    def __init__(
        self,
        *,
        limits: GovernanceLimits = GovernanceLimits(),
        reviewed_at: str = DEFAULT_REVIEWED_AT,
        targets: Mapping[str, PromotionTarget] | None = None,
    ) -> None:
        _validate_limits(limits)
        self._limits = limits
        self._reviewed_at = reviewed_at
        self._records: dict[str, CandidateRecord] = {}
        self._groups: dict[str, CandidateGroup] = {}
        self._events: tuple[ReviewEventRecord, ...] = ()
        self._targets: dict[str, PromotionTarget] = {
            target: InMemoryPromotionTarget(target) for target in PROMOTION_TARGETS
        }
        if targets is not None:
            self._targets.update(targets)

    @property
    def records(self) -> tuple[CandidateRecord, ...]:
        return tuple(sorted(self._records.values(), key=lambda item: item.candidate.candidate_id))

    @property
    def groups(self) -> tuple[CandidateGroup, ...]:
        return tuple(sorted(self._groups.values(), key=lambda item: item.group_id))

    @property
    def events(self) -> tuple[ReviewEventRecord, ...]:
        return self._events

    def add_candidates(self, candidates: tuple[CandidateArtifact, ...]) -> GovernanceActionResult:
        if len(self._records) + len(candidates) > self._limits.max_candidates:
            issue = _issue(
                "CANDIDATE_LIMIT_EXCEEDED",
                "Candidate repository limit exceeded.",
                {"limit": self._limits.max_candidates},
                severity="error",
            )
            return GovernanceActionResult("error", (), validation_report=(issue,))
        records = []
        issues = []
        events = []
        for candidate in sorted(candidates, key=lambda item: item.candidate_id):
            existing = self._records.get(candidate.candidate_id)
            if existing is not None:
                records.append(existing)
                continue
            issue = self._validate_candidate(candidate)
            if issue is not None:
                issues.append(issue)
                continue
            group_id, group_key = _group_identity(candidate)
            record = CandidateRecord(
                candidate=candidate,
                state="discovered",
                version=1,
                group_id=group_id,
                created_at=self._reviewed_at,
                updated_at=self._reviewed_at,
            )
            self._records[candidate.candidate_id] = record
            self._add_to_group(candidate, group_id, group_key)
            event = _event(
                "CandidateCreated",
                "knowledge.governance.candidate.created",
                {"candidate_id": candidate.candidate_id, "group_id": group_id},
            )
            events.append(_event_record(event))
            if len(self._groups[group_id].candidate_ids) > 1:
                grouped = _event(
                    "CandidateGrouped",
                    "knowledge.governance.candidate.grouped",
                    {"candidate_id": candidate.candidate_id, "group_id": group_id},
                )
                events.append(_event_record(grouped))
            records.append(record)
        self._append_events(tuple(events))
        status = "ok" if not any(issue.severity == "error" for issue in issues) else "error"
        return GovernanceActionResult(status, tuple(records), validation_report=tuple(issues), events=tuple(events))

    def transition(
        self,
        candidate_id: str,
        to_state: ReviewState,
        *,
        action: str,
        reviewer: str,
        rationale: str,
        superseded_by: str | None = None,
    ) -> GovernanceActionResult:
        issues = self._validate_human_action(candidate_id, reviewer, rationale)
        record = self._records.get(candidate_id)
        if record is None:
            issues.append(
                _issue(
                    "ORPHANED_CANDIDATE",
                    "Candidate does not exist in repository.",
                    {"candidate_id": candidate_id},
                    severity="error",
                )
            )
            return GovernanceActionResult("error", (), validation_report=tuple(issues))
        if to_state not in REVIEW_STATES:
            issues.append(
                _issue(
                    "INVALID_REVIEW_STATE",
                    "Review state is not supported.",
                    {"candidate_id": candidate_id, "state": to_state},
                    severity="error",
                )
            )
        if to_state not in VALID_TRANSITIONS[record.state]:
            issues.append(
                _issue(
                    "INVALID_REVIEW_TRANSITION",
                    "Candidate cannot transition directly to requested state.",
                    {"candidate_id": candidate_id, "from_state": record.state, "to_state": to_state},
                    severity="error",
                )
            )
        if to_state == "superseded" and (not superseded_by or superseded_by not in self._records):
            issues.append(
                _issue(
                    "BROKEN_SUPERSESSION_REFERENCE",
                    "Superseded candidates must reference an existing replacement candidate.",
                    {"candidate_id": candidate_id, "superseded_by": superseded_by},
                    severity="error",
                )
            )
        if issues:
            return GovernanceActionResult("error", (record,), validation_report=tuple(issues))
        event = _event(
            _event_type_for_state(to_state),
            _event_route_for_state(to_state),
            {"candidate_id": candidate_id, "from_state": record.state, "to_state": to_state},
        )
        if len(record.review_history) >= self._limits.max_history_entries_per_candidate:
            issues.append(
                _issue(
                    "REVIEW_HISTORY_LIMIT_EXCEEDED",
                    "Candidate review history exceeds configured maximum.",
                    {"candidate_id": candidate_id, "limit": self._limits.max_history_entries_per_candidate},
                    severity="error",
                )
            )
            return GovernanceActionResult("error", (record,), validation_report=tuple(issues))
        history = ReviewHistoryEntry(
            action=action,
            from_state=record.state,
            to_state=to_state,
            reviewer=_normalize_reviewer(reviewer),
            rationale=_normalize_rationale(rationale, self._limits),
            at=self._reviewed_at,
            event_id=event.event_id,
        )
        updated = replace(
            record,
            state=to_state,
            version=record.version + 1,
            updated_at=self._reviewed_at,
            review_history=(*record.review_history, history),
            superseded_by=superseded_by if to_state == "superseded" else record.superseded_by,
        )
        self._records[candidate_id] = updated
        event_records = [_event_record(event)]
        if to_state in {"approved", "rejected", "deferred", "superseded"}:
            completed = _event(
                "ReviewCompleted",
                "knowledge.governance.review.completed",
                {"candidate_id": candidate_id, "state": to_state},
            )
            event_records.append(_event_record(completed))
        self._append_events(tuple(event_records))
        return GovernanceActionResult("ok", (updated,), events=tuple(event_records))

    def merge(
        self,
        source_candidate_ids: tuple[str, ...],
        target_candidate_id: str,
        *,
        reviewer: str,
        rationale: str,
    ) -> GovernanceActionResult:
        issues = []
        if target_candidate_id not in self._records:
            issues.append(
                _issue(
                    "MERGE_TARGET_MISSING",
                    "Merge target candidate does not exist.",
                    {"target_candidate_id": target_candidate_id},
                    severity="error",
                )
            )
        for candidate_id in source_candidate_ids:
            issues.extend(self._validate_human_action(candidate_id, reviewer, rationale))
            if candidate_id == target_candidate_id:
                issues.append(
                    _issue(
                        "PROMOTION_LOOP",
                        "Merge source cannot be the merge target.",
                        {"candidate_id": candidate_id},
                        severity="error",
                        recoverable=False,
                    )
                )
            if candidate_id not in self._records:
                issues.append(
                    _issue(
                        "ORPHANED_CANDIDATE",
                        "Merge source candidate does not exist.",
                        {"candidate_id": candidate_id},
                        severity="error",
                    )
                )
        if issues:
            return GovernanceActionResult("error", (), validation_report=tuple(issues))
        event = _event(
            "CandidateMerged",
            "knowledge.governance.candidate.merged",
            {"source_candidate_ids": source_candidate_ids, "target_candidate_id": target_candidate_id},
        )
        merge_history = MergeHistoryEntry(
            source_candidate_ids=tuple(sorted(source_candidate_ids)),
            target_candidate_id=target_candidate_id,
            reviewer=_normalize_reviewer(reviewer),
            rationale=_normalize_rationale(rationale, self._limits),
            at=self._reviewed_at,
            event_id=event.event_id,
        )
        updated = []
        for candidate_id in sorted(source_candidate_ids):
            record = self._records[candidate_id]
            candidate_result = self.transition(
                candidate_id,
                "superseded",
                action="merge",
                reviewer=reviewer,
                rationale=rationale,
                superseded_by=target_candidate_id,
            )
            if candidate_result.status == "error":
                return candidate_result
            superseded = candidate_result.candidate_records[0]
            superseded = replace(superseded, merge_history=(*superseded.merge_history, merge_history))
            self._records[candidate_id] = superseded
            updated.append(superseded)
        target = self._records[target_candidate_id]
        target = replace(target, merge_history=(*target.merge_history, merge_history), version=target.version + 1)
        self._records[target_candidate_id] = target
        updated.append(target)
        event_record = _event_record(event)
        self._append_events((event_record,))
        return GovernanceActionResult("ok", tuple(updated), events=(event_record,))

    def promote(
        self,
        candidate_id: str,
        *,
        target: PromotionTargetName,
        reviewer: str,
        rationale: str,
        rollback: str,
    ) -> GovernanceActionResult:
        issues = self._validate_human_action(candidate_id, reviewer, rationale)
        rollback_text = rollback.strip()
        if not rollback_text:
            issues.append(
                _issue(
                    "ROLLBACK_MISSING",
                    "Promotion requires rollback rationale.",
                    {"candidate_id": candidate_id},
                    severity="error",
                )
            )
        if target not in PROMOTION_TARGETS:
            issues.append(
                _issue(
                    "INVALID_PROMOTION_TARGET",
                    "Promotion target is unsupported.",
                    {"candidate_id": candidate_id, "target": target},
                    severity="error",
                )
            )
        record = self._records.get(candidate_id)
        if record is None:
            issues.append(
                _issue("ORPHANED_CANDIDATE", "Candidate does not exist.", {"candidate_id": candidate_id}, severity="error")
            )
            return GovernanceActionResult("error", (), validation_report=tuple(issues))
        if record.state != "approved":
            issues.append(
                _issue(
                    "PROMOTION_REQUIRES_APPROVAL",
                    "Candidate must be approved before promotion.",
                    {"candidate_id": candidate_id, "state": record.state},
                    severity="error",
                )
            )
        if not record.review_history:
            issues.append(
                _issue(
                    "MISSING_REVIEW_HISTORY",
                    "Candidate cannot be promoted without review history.",
                    {"candidate_id": candidate_id},
                    severity="error",
                )
            )
        if record.candidate.provenance.supporting_observations == ():
            issues.append(
                _issue(
                    "MISSING_PROVENANCE",
                    "Candidate cannot be promoted without supporting observations.",
                    {"candidate_id": candidate_id},
                    severity="error",
                )
            )
        if record.promotion_history:
            issues.append(
                _issue(
                    "DUPLICATE_PROMOTION",
                    "Candidate has already been promoted.",
                    {"candidate_id": candidate_id},
                    severity="error",
                    recoverable=False,
                )
            )
        if issues:
            return GovernanceActionResult("error", (record,), validation_report=tuple(issues))
        promotion = _promotion_record(
            record,
            target=target,
            reviewer=_normalize_reviewer(reviewer),
            rationale=_normalize_rationale(rationale, self._limits),
            rollback=rollback_text,
            promoted_at=self._reviewed_at,
        )
        target_result = self._targets[target].store(promotion)
        if target_result.status == "error":
            return GovernanceActionResult(
                "error",
                (record,),
                validation_report=target_result.validation_report,
                promotion_records=target_result.promotion_records,
            )
        event = _event(
            "CandidatePromoted",
            "knowledge.governance.candidate.promoted",
            {"candidate_id": candidate_id, "promotion_id": promotion.promotion_id, "target": target},
        )
        history = ReviewHistoryEntry(
            action="promote",
            from_state=record.state,
            to_state="promoted",
            reviewer=_normalize_reviewer(reviewer),
            rationale=_normalize_rationale(rationale, self._limits),
            at=self._reviewed_at,
            event_id=event.event_id,
        )
        updated = replace(
            record,
            state="promoted",
            version=record.version + 1,
            updated_at=self._reviewed_at,
            review_history=(*record.review_history, history),
            promotion_history=(*record.promotion_history, promotion),
        )
        self._records[candidate_id] = updated
        event_record = _event_record(event)
        self._append_events((event_record,))
        return GovernanceActionResult("ok", (updated,), promotion_records=(promotion,), events=(event_record,))

    def views(self) -> tuple[ReviewView, ...]:
        records = self.records
        view_specs = {
            "New Concepts": lambda item: item.candidate.candidate_type == "concept" and item.state == "discovered",
            "Pending ADRs": lambda item: item.candidate.candidate_type == "adr" and item.state in {"discovered", "under_review", "approved"},
            "Glossary Candidates": lambda item: item.candidate.candidate_type == "glossary",
            "Constitutional Amendments": lambda item: item.candidate.candidate_type == "amendment",
            "Contradictions": lambda item: item.candidate.candidate_type == "contradiction",
            "Duplicate Concepts": lambda item: item.candidate.candidate_type == "duplicate",
            "Novel Ideas": lambda item: item.candidate.candidate_type == "novelty",
            "Recurring Principles": lambda item: item.candidate.candidate_type == "principle",
            "Open TODOs": lambda item: item.candidate.candidate_type == "todo" and item.state not in {"rejected", "promoted"},
            "Low Confidence Candidates": lambda item: item.candidate.confidence < 0.5,
            "High Impact Candidates": lambda item: item.candidate.candidate_type in {"amendment", "decision", "adr", "contradiction"},
        }
        views = []
        for name, predicate in view_specs.items():
            candidate_ids = tuple(item.candidate.candidate_id for item in records if predicate(item))
            views.append(ReviewView(name=name, candidate_ids=candidate_ids, generated_at=self._reviewed_at))
        return tuple(sorted(views, key=lambda item: item.name))

    def _validate_candidate(self, candidate: CandidateArtifact) -> GovernanceValidationIssue | None:
        if not candidate.provenance.supporting_observations:
            return _issue(
                "MISSING_PROVENANCE",
                "Candidate must retain supporting observation provenance.",
                {"candidate_id": candidate.candidate_id},
                severity="error",
            )
        if not candidate.candidate_id.strip():
            return _issue(
                "CANDIDATE_ID_MISSING",
                "Candidate ID is required.",
                {"title": candidate.title},
                severity="error",
            )
        return None

    def _add_to_group(self, candidate: CandidateArtifact, group_id: str, group_key: str) -> None:
        existing = self._groups.get(group_id)
        candidate_ids = (candidate.candidate_id,)
        if existing is not None:
            candidate_ids = tuple(sorted((*existing.candidate_ids, candidate.candidate_id)))
        if existing is None and len(self._groups) >= self._limits.max_groups:
            raise ValueError("candidate group limit exceeded")
        self._groups[group_id] = CandidateGroup(
            group_id=group_id,
            group_key=group_key,
            candidate_type=candidate.candidate_type,
            candidate_ids=candidate_ids,
            title=f"{candidate.candidate_type}:{group_key}",
        )

    def _validate_human_action(self, candidate_id: str, reviewer: str, rationale: str) -> list[GovernanceValidationIssue]:
        issues = []
        try:
            _normalize_reviewer(reviewer, self._limits)
        except ValueError as exc:
            issues.append(
                _issue("REVIEWER_INVALID", str(exc), {"candidate_id": candidate_id}, severity="error")
            )
        try:
            _normalize_rationale(rationale, self._limits)
        except ValueError as exc:
            issues.append(
                _issue("RATIONALE_INVALID", str(exc), {"candidate_id": candidate_id}, severity="error")
            )
        return issues

    def _append_events(self, events: tuple[ReviewEventRecord, ...]) -> None:
        self._events = (*self._events, *events)


def _validate_limits(limits: GovernanceLimits) -> None:
    for field in (
        "max_candidates",
        "max_groups",
        "max_history_entries_per_candidate",
        "max_promotions",
        "max_rationale_length",
        "max_reviewer_length",
    ):
        if getattr(limits, field) <= 0:
            raise ValueError(f"{field} must be positive")


def _normalize_reviewer(reviewer: str, limits: GovernanceLimits | None = None) -> str:
    max_length = 128 if limits is None else limits.max_reviewer_length
    normalized = reviewer.strip()
    if not normalized:
        raise ValueError("reviewer is required")
    if len(normalized) > max_length:
        raise ValueError("reviewer exceeds maximum length")
    return normalized


def _normalize_rationale(rationale: str, limits: GovernanceLimits) -> str:
    normalized = rationale.strip()
    if not normalized:
        raise ValueError("reviewer rationale is required")
    if len(normalized) > limits.max_rationale_length:
        raise ValueError("reviewer rationale exceeds maximum length")
    return normalized


def _group_identity(candidate: CandidateArtifact) -> tuple[str, str]:
    metadata = candidate.metadata
    key_source = (
        str(metadata.get("term"))
        or str(metadata.get("deprecated_term"))
        or str(metadata.get("normalized_sentence"))
        or candidate.title
    )
    group_key = _normalize_key(f"{candidate.candidate_type}:{key_source}")
    return _stable_id("candidate-group", group_key), group_key


def _event_type_for_state(state: ReviewState) -> str:
    return {
        "under_review": "CandidateUpdated",
        "approved": "CandidateApproved",
        "rejected": "CandidateRejected",
        "deferred": "CandidateDeferred",
        "superseded": "CandidateSuperseded",
        "promoted": "CandidatePromoted",
        "discovered": "CandidateCreated",
    }[state]


def _event_route_for_state(state: ReviewState) -> str:
    return f"knowledge.governance.candidate.{state}"


def _promotion_record(
    record: CandidateRecord,
    *,
    target: PromotionTargetName,
    reviewer: str,
    rationale: str,
    rollback: str,
    promoted_at: str,
) -> PromotionRecord:
    candidate = record.candidate
    artifact = {
        "title": candidate.title,
        "summary": candidate.summary,
        "candidate_type": candidate.candidate_type,
        "confidence": candidate.confidence,
        "uncertainty": candidate.uncertainty,
        "metadata": compiler_plain(candidate.metadata),
    }
    provenance = {
        "candidate_id": candidate.candidate_id,
        "candidate_provenance": compiler_plain(candidate.provenance),
        "review_history": to_plain(record.review_history),
        "merge_history": to_plain(record.merge_history),
        "governance_version": "1.0.0",
    }
    promotion_id = _stable_id("promotion", target, candidate.candidate_id, artifact, provenance)
    return PromotionRecord(
        promotion_id=promotion_id,
        version=1,
        target=target,
        promoted_artifact_id=_stable_id("promoted-artifact", target, candidate.candidate_id),
        candidate_ids=(candidate.candidate_id,),
        reviewer=reviewer,
        rationale=rationale,
        rollback=rollback,
        promoted_at=promoted_at,
        artifact=artifact,
        provenance=provenance,
    )


def _event(event_type: str, route: str, payload: Mapping[str, object]) -> ReviewEvent:
    event_id = _stable_id("governance-event", event_type, route, payload)
    return ReviewEvent(
        event_id=event_id,
        event_type=event_type,
        route=route,
        payload=payload,
        metadata={"governance_version": "1.0.0"},
    )


def _event_record(event: ReviewEvent) -> ReviewEventRecord:
    return ReviewEventRecord(event=event, status="ok")


def _issue(
    error_code: str,
    reason: str,
    context: Mapping[str, object],
    *,
    severity: str,
    recoverable: bool = True,
) -> GovernanceValidationIssue:
    issue_id = _stable_id("governance-issue", error_code, reason, context, severity)
    return GovernanceValidationIssue(
        issue_id=issue_id,
        severity=severity,  # type: ignore[arg-type]
        error_code=error_code,
        reason=reason,
        context=context,
        recoverable=recoverable,
    )


def _normalize_key(value: str) -> str:
    return " ".join(value.strip().lower().split())


def _stable_id(prefix: str, *parts: object) -> str:
    payload = dumps(to_plain(parts), sort_keys=True, separators=(",", ":"), default=str)
    return f"{prefix}:{sha256(payload.encode('utf-8')).hexdigest()}"
