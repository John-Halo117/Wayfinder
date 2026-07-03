"""Execution domain models.

Execution preserves the process of building reality. It records explicit
mission state and derives interpretation from that state without persistence
side effects.

Contract:
- Inputs: explicit mission records and implementation proposals.
- Outputs: immutable reports, progress, decisions, and promotion states.
- Runtime constraint: O(mission items + proposal items), bounded by local caps.
- Memory assumption: O(mission items + report findings), bounded by local caps.
- Failure cases: missing ids, invalid enum values, oversized collections, and
  invalid transitions raise ValueError.
- Determinism: all derivations are deterministic value-object operations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Mapping

MAX_ID_LENGTH = 128
MAX_TEXT_LENGTH = 1024
MAX_REASON_LENGTH = 512
MAX_METADATA_KEYS = 16
MAX_METADATA_VALUE_LENGTH = 512
MAX_MISSION_ITEMS = 64
MAX_REPORT_FINDINGS = 64


class ExecutionStatus(str, Enum):
    OK = "ok"
    ATTENTION = "attention"
    ERROR = "error"


class ConstraintKind(str, Enum):
    HARD = "hard"
    SOFT = "soft"


class AcceptanceStatus(str, Enum):
    OPEN = "open"
    SATISFIED = "satisfied"
    BLOCKED = "blocked"


class BearingStatus(str, Enum):
    ALIGNED = "aligned"
    NEEDS_ATTENTION = "needs_attention"
    MISALIGNED = "misaligned"


class BearingCheckKind(str, Enum):
    INTENT_ALIGNMENT = "intent_alignment"
    SCOPE_COMPLIANCE = "scope_compliance"
    FOCUS_ALIGNMENT = "focus_alignment"
    CONSTRAINT_COMPLIANCE = "constraint_compliance"
    ACCEPTANCE_IMPACT = "acceptance_impact"
    CHANGE_BUDGET_COMPLIANCE = "change_budget_compliance"
    ARCHITECTURAL_BUDGET_COMPLIANCE = "architectural_budget_compliance"


class DriftKind(str, Enum):
    MISSION = "mission_drift"
    SCOPE = "scope_drift"
    FOCUS = "focus_drift"
    ARCHITECTURAL = "architectural_drift"
    BUDGET = "budget_drift"


class DriftSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class DecisionStatus(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    REVERSED = "reversed"


class ParkingLotStatus(str, Enum):
    CAPTURED = "captured"
    REVIEWED = "reviewed"
    PROMOTED = "promoted"
    DISMISSED = "dismissed"


class PromotionStage(str, Enum):
    CAPTURED = "captured"
    RESEARCH = "research"
    SANDBOX = "sandbox"
    PROTOTYPE = "prototype"
    CAPABILITY = "capability"
    CORE = "core"


PROMOTION_ORDER = (
    PromotionStage.CAPTURED,
    PromotionStage.RESEARCH,
    PromotionStage.SANDBOX,
    PromotionStage.PROTOTYPE,
    PromotionStage.CAPABILITY,
    PromotionStage.CORE,
)


@dataclass(frozen=True)
class Intent:
    """What the mission is trying to accomplish."""

    intent_id: str
    statement: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "intent_id", _normalize_id(self.intent_id, "intent_id"))
        object.__setattr__(self, "statement", _normalize_text(self.statement, "statement", MAX_TEXT_LENGTH))


@dataclass(frozen=True)
class Scope:
    """A bounded area that is either included or explicitly excluded."""

    scope_id: str
    description: str
    in_scope: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "scope_id", _normalize_id(self.scope_id, "scope_id"))
        object.__setattr__(self, "description", _normalize_text(self.description, "description", MAX_TEXT_LENGTH))


@dataclass(frozen=True)
class Focus:
    """The current center of attention inside a mission."""

    focus_id: str
    description: str
    active_scope_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "focus_id", _normalize_id(self.focus_id, "focus_id"))
        object.__setattr__(self, "description", _normalize_text(self.description, "description", MAX_TEXT_LENGTH))
        if self.active_scope_id is not None:
            object.__setattr__(self, "active_scope_id", _normalize_id(self.active_scope_id, "active_scope_id"))


@dataclass(frozen=True)
class Context:
    """Observed context that may matter to execution."""

    context_id: str
    summary: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "context_id", _normalize_id(self.context_id, "context_id"))
        object.__setattr__(self, "summary", _normalize_text(self.summary, "summary", MAX_TEXT_LENGTH))


@dataclass(frozen=True)
class Constraint:
    """A hard or soft constraint on the mission."""

    constraint_id: str
    description: str
    kind: ConstraintKind = ConstraintKind.HARD

    def __post_init__(self) -> None:
        object.__setattr__(self, "constraint_id", _normalize_id(self.constraint_id, "constraint_id"))
        object.__setattr__(self, "description", _normalize_text(self.description, "description", MAX_TEXT_LENGTH))
        object.__setattr__(self, "kind", _coerce_enum(self.kind, ConstraintKind, "kind"))

    @property
    def required(self) -> bool:
        return self.kind is ConstraintKind.HARD


@dataclass(frozen=True)
class AcceptanceCriterion:
    """A condition that defines mission completion."""

    criterion_id: str
    description: str
    status: AcceptanceStatus = AcceptanceStatus.OPEN

    def __post_init__(self) -> None:
        object.__setattr__(self, "criterion_id", _normalize_id(self.criterion_id, "criterion_id"))
        object.__setattr__(self, "description", _normalize_text(self.description, "description", MAX_TEXT_LENGTH))
        object.__setattr__(self, "status", _coerce_enum(self.status, AcceptanceStatus, "status"))

    @property
    def satisfied(self) -> bool:
        return self.status is AcceptanceStatus.SATISFIED


@dataclass(frozen=True)
class ChangeBudget:
    """Bounded change surface for preserving maneuverability."""

    max_changed_files: int
    max_risk_score: int = 5

    def __post_init__(self) -> None:
        object.__setattr__(self, "max_changed_files", _normalize_non_negative_int(self.max_changed_files, "max_changed_files"))
        object.__setattr__(self, "max_risk_score", _normalize_non_negative_int(self.max_risk_score, "max_risk_score"))

    def allows(self, proposal: "ImplementationProposal") -> bool:
        return proposal.changed_files <= self.max_changed_files and proposal.risk_score <= self.max_risk_score


@dataclass(frozen=True)
class ArchitecturalBudget:
    """Bounded architectural impact for a mission."""

    max_new_dependencies: int = 0
    max_touched_domains: int = 1

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "max_new_dependencies",
            _normalize_non_negative_int(self.max_new_dependencies, "max_new_dependencies"),
        )
        object.__setattr__(
            self,
            "max_touched_domains",
            _normalize_non_negative_int(self.max_touched_domains, "max_touched_domains"),
        )

    def allows(self, proposal: "ImplementationProposal") -> bool:
        return (
            proposal.new_dependencies <= self.max_new_dependencies
            and proposal.touched_domains <= self.max_touched_domains
        )


@dataclass(frozen=True)
class AttentionBudget:
    """Bounded active attention for a mission."""

    max_active_items: int = 7

    def __post_init__(self) -> None:
        object.__setattr__(self, "max_active_items", _normalize_non_negative_int(self.max_active_items, "max_active_items"))

    def allows(self, item_count: int) -> bool:
        return _normalize_non_negative_int(item_count, "item_count") <= self.max_active_items


@dataclass(frozen=True)
class ImplementationProposal:
    """A proposed implementation to evaluate against the current mission."""

    proposal_id: str
    summary: str
    intent_id: str
    scope_ids: tuple[str, ...] = ()
    addressed_acceptance_ids: tuple[str, ...] = ()
    violated_constraint_ids: tuple[str, ...] = ()
    changed_files: int = 0
    risk_score: int = 0
    new_dependencies: int = 0
    touched_domains: int = 1
    notes: Mapping[str, object] = MappingProxyType({})

    def __post_init__(self) -> None:
        object.__setattr__(self, "proposal_id", _normalize_id(self.proposal_id, "proposal_id"))
        object.__setattr__(self, "summary", _normalize_text(self.summary, "summary", MAX_TEXT_LENGTH))
        object.__setattr__(self, "intent_id", _normalize_id(self.intent_id, "intent_id"))
        object.__setattr__(self, "scope_ids", _freeze_ids(self.scope_ids, "scope_ids"))
        object.__setattr__(
            self,
            "addressed_acceptance_ids",
            _freeze_ids(self.addressed_acceptance_ids, "addressed_acceptance_ids"),
        )
        object.__setattr__(
            self,
            "violated_constraint_ids",
            _freeze_ids(self.violated_constraint_ids, "violated_constraint_ids"),
        )
        object.__setattr__(self, "changed_files", _normalize_non_negative_int(self.changed_files, "changed_files"))
        object.__setattr__(self, "risk_score", _normalize_non_negative_int(self.risk_score, "risk_score"))
        object.__setattr__(self, "new_dependencies", _normalize_non_negative_int(self.new_dependencies, "new_dependencies"))
        object.__setattr__(self, "touched_domains", _normalize_non_negative_int(self.touched_domains, "touched_domains"))
        object.__setattr__(self, "notes", freeze_metadata(self.notes))


@dataclass(frozen=True)
class Progress:
    """Derived progress from acceptance criteria."""

    mission_id: str
    satisfied_count: int
    total_count: int
    blocked_count: int
    status: ExecutionStatus

    @property
    def complete(self) -> bool:
        return self.total_count > 0 and self.satisfied_count == self.total_count

    @property
    def completion_ratio(self) -> float:
        if self.total_count == 0:
            return 0.0
        return self.satisfied_count / self.total_count


@dataclass(frozen=True)
class BearingCheck:
    """One evaluation result in a bearing report."""

    kind: BearingCheckKind
    status: BearingStatus
    reason: str
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", _coerce_enum(self.kind, BearingCheckKind, "kind"))
        object.__setattr__(self, "status", _coerce_enum(self.status, BearingStatus, "status"))
        object.__setattr__(self, "reason", _normalize_text(self.reason, "reason", MAX_REASON_LENGTH))
        object.__setattr__(self, "evidence", _freeze_texts(self.evidence, "evidence", MAX_REPORT_FINDINGS))


@dataclass(frozen=True)
class BearingReport:
    """Structured bearing evaluation, never a bare boolean."""

    report_id: str
    mission_id: str
    proposal_id: str
    status: BearingStatus
    checks: tuple[BearingCheck, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "report_id", _normalize_id(self.report_id, "report_id"))
        object.__setattr__(self, "mission_id", _normalize_id(self.mission_id, "mission_id"))
        object.__setattr__(self, "proposal_id", _normalize_id(self.proposal_id, "proposal_id"))
        object.__setattr__(self, "status", _coerce_enum(self.status, BearingStatus, "status"))
        object.__setattr__(self, "checks", _freeze_items(self.checks, "checks"))

    @property
    def aligned(self) -> bool:
        return self.status is BearingStatus.ALIGNED


@dataclass(frozen=True)
class DriftFinding:
    """A drift finding with severity and evidence."""

    kind: DriftKind
    severity: DriftSeverity
    reason: str
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", _coerce_enum(self.kind, DriftKind, "kind"))
        object.__setattr__(self, "severity", _coerce_enum(self.severity, DriftSeverity, "severity"))
        object.__setattr__(self, "reason", _normalize_text(self.reason, "reason", MAX_REASON_LENGTH))
        object.__setattr__(self, "evidence", _freeze_texts(self.evidence, "evidence", MAX_REPORT_FINDINGS))


@dataclass(frozen=True)
class DriftReport:
    """Structured drift report that describes findings without deciding."""

    report_id: str
    mission_id: str
    proposal_id: str
    findings: tuple[DriftFinding, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "report_id", _normalize_id(self.report_id, "report_id"))
        object.__setattr__(self, "mission_id", _normalize_id(self.mission_id, "mission_id"))
        object.__setattr__(self, "proposal_id", _normalize_id(self.proposal_id, "proposal_id"))
        object.__setattr__(self, "findings", _freeze_items(self.findings, "findings"))

    @property
    def has_drift(self) -> bool:
        return bool(self.findings)


@dataclass(frozen=True)
class Decision:
    """A durable decision record for execution."""

    decision_id: str
    mission_id: str
    summary: str
    status: DecisionStatus
    reason: str
    actor: str
    reverses_decision_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision_id", _normalize_id(self.decision_id, "decision_id"))
        object.__setattr__(self, "mission_id", _normalize_id(self.mission_id, "mission_id"))
        object.__setattr__(self, "summary", _normalize_text(self.summary, "summary", MAX_TEXT_LENGTH))
        object.__setattr__(self, "status", _coerce_enum(self.status, DecisionStatus, "status"))
        object.__setattr__(self, "reason", _normalize_text(self.reason, "reason", MAX_REASON_LENGTH))
        object.__setattr__(self, "actor", _normalize_id(self.actor, "actor"))
        if self.reverses_decision_id is not None:
            object.__setattr__(
                self,
                "reverses_decision_id",
                _normalize_id(self.reverses_decision_id, "reverses_decision_id"),
            )


@dataclass(frozen=True)
class ParkingLotEntry:
    """Valuable idea captured instead of expanding the current mission."""

    entry_id: str
    mission_id: str
    summary: str
    reason_out_of_scope: str
    status: ParkingLotStatus = ParkingLotStatus.CAPTURED

    def __post_init__(self) -> None:
        object.__setattr__(self, "entry_id", _normalize_id(self.entry_id, "entry_id"))
        object.__setattr__(self, "mission_id", _normalize_id(self.mission_id, "mission_id"))
        object.__setattr__(self, "summary", _normalize_text(self.summary, "summary", MAX_TEXT_LENGTH))
        object.__setattr__(
            self,
            "reason_out_of_scope",
            _normalize_text(self.reason_out_of_scope, "reason_out_of_scope", MAX_REASON_LENGTH),
        )
        object.__setattr__(self, "status", _coerce_enum(self.status, ParkingLotStatus, "status"))


@dataclass(frozen=True)
class PromotionState:
    """Explicit, reversible lifecycle for ideas and capabilities."""

    promotion_id: str
    subject_id: str
    stage: PromotionStage
    reason: str
    actor: str
    previous_stage: PromotionStage | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "promotion_id", _normalize_id(self.promotion_id, "promotion_id"))
        object.__setattr__(self, "subject_id", _normalize_id(self.subject_id, "subject_id"))
        object.__setattr__(self, "stage", _coerce_enum(self.stage, PromotionStage, "stage"))
        object.__setattr__(self, "reason", _normalize_text(self.reason, "reason", MAX_REASON_LENGTH))
        object.__setattr__(self, "actor", _normalize_id(self.actor, "actor"))
        if self.previous_stage is not None:
            object.__setattr__(self, "previous_stage", _coerce_enum(self.previous_stage, PromotionStage, "previous_stage"))

    def transition(self, target_stage: PromotionStage | str, actor: str, reason: str) -> "PromotionState":
        """Move one lifecycle step up or down with an explicit reason."""

        target = _coerce_enum(target_stage, PromotionStage, "target_stage")
        current_index = PROMOTION_ORDER.index(self.stage)
        target_index = PROMOTION_ORDER.index(target)
        if abs(target_index - current_index) > 1:
            raise ValueError("promotion transitions must move one lifecycle step at a time")
        return PromotionState(
            promotion_id=self.promotion_id,
            subject_id=self.subject_id,
            stage=target,
            previous_stage=self.stage,
            actor=actor,
            reason=reason,
        )


@dataclass(frozen=True)
class Mission:
    """A bounded unit of execution with derived state."""

    mission_id: str
    intent: Intent
    scopes: tuple[Scope, ...]
    focus: Focus
    contexts: tuple[Context, ...] = ()
    constraints: tuple[Constraint, ...] = ()
    acceptance_criteria: tuple[AcceptanceCriterion, ...] = ()
    change_budget: ChangeBudget = field(default_factory=lambda: ChangeBudget(max_changed_files=10, max_risk_score=5))
    architectural_budget: ArchitecturalBudget = field(
        default_factory=lambda: ArchitecturalBudget(max_new_dependencies=0, max_touched_domains=1)
    )
    attention_budget: AttentionBudget = field(default_factory=lambda: AttentionBudget(max_active_items=7))

    def __post_init__(self) -> None:
        object.__setattr__(self, "mission_id", _normalize_id(self.mission_id, "mission_id"))
        object.__setattr__(self, "scopes", _freeze_items(self.scopes, "scopes"))
        object.__setattr__(self, "contexts", _freeze_items(self.contexts, "contexts"))
        object.__setattr__(self, "constraints", _freeze_items(self.constraints, "constraints"))
        object.__setattr__(self, "acceptance_criteria", _freeze_items(self.acceptance_criteria, "acceptance_criteria"))
        self._validate_unique("scope", [scope.scope_id for scope in self.scopes])
        self._validate_unique("context", [context.context_id for context in self.contexts])
        self._validate_unique("constraint", [constraint.constraint_id for constraint in self.constraints])
        self._validate_unique("criterion", [criterion.criterion_id for criterion in self.acceptance_criteria])
        if self.focus.active_scope_id is not None and self.focus.active_scope_id not in self.scope_ids:
            raise ValueError("focus active_scope_id must reference mission scope")

    @property
    def scope_ids(self) -> frozenset[str]:
        return frozenset(scope.scope_id for scope in self.scopes)

    @property
    def included_scope_ids(self) -> frozenset[str]:
        return frozenset(scope.scope_id for scope in self.scopes if scope.in_scope)

    @property
    def excluded_scope_ids(self) -> frozenset[str]:
        return frozenset(scope.scope_id for scope in self.scopes if not scope.in_scope)

    @property
    def hard_constraint_ids(self) -> frozenset[str]:
        return frozenset(constraint.constraint_id for constraint in self.constraints if constraint.required)

    @property
    def acceptance_ids(self) -> frozenset[str]:
        return frozenset(criterion.criterion_id for criterion in self.acceptance_criteria)

    def progress(self) -> Progress:
        """Derive progress from acceptance criteria."""

        total = len(self.acceptance_criteria)
        satisfied = sum(1 for criterion in self.acceptance_criteria if criterion.satisfied)
        blocked = sum(1 for criterion in self.acceptance_criteria if criterion.status is AcceptanceStatus.BLOCKED)
        if blocked:
            status = ExecutionStatus.ATTENTION
        elif total > 0 and satisfied == total:
            status = ExecutionStatus.OK
        else:
            status = ExecutionStatus.ATTENTION
        return Progress(
            mission_id=self.mission_id,
            satisfied_count=satisfied,
            total_count=total,
            blocked_count=blocked,
            status=status,
        )

    def evaluate_bearing(self, proposal: ImplementationProposal) -> BearingReport:
        """Evaluate whether a proposal remains aligned with the mission."""

        checks = (
            self._check_intent(proposal),
            self._check_scope(proposal),
            self._check_focus(proposal),
            self._check_constraints(proposal),
            self._check_acceptance(proposal),
            self._check_change_budget(proposal),
            self._check_architectural_budget(proposal),
        )
        status = _worst_bearing_status(checks)
        return BearingReport(
            report_id=f"bearing:{self.mission_id}:{proposal.proposal_id}",
            mission_id=self.mission_id,
            proposal_id=proposal.proposal_id,
            status=status,
            checks=checks,
        )

    def detect_drift(self, proposal: ImplementationProposal) -> DriftReport:
        """Describe drift signals without deciding what to do."""

        findings: list[DriftFinding] = []
        if proposal.intent_id != self.intent.intent_id:
            findings.append(
                DriftFinding(
                    kind=DriftKind.MISSION,
                    severity=DriftSeverity.CRITICAL,
                    reason="proposal intent does not match mission intent",
                    evidence=(proposal.intent_id, self.intent.intent_id),
                )
            )
        outside_scope = _sorted_tuple(set(proposal.scope_ids) - self.included_scope_ids)
        excluded_scope = _sorted_tuple(set(proposal.scope_ids) & self.excluded_scope_ids)
        if outside_scope or excluded_scope:
            findings.append(
                DriftFinding(
                    kind=DriftKind.SCOPE,
                    severity=DriftSeverity.WARNING,
                    reason="proposal touches scope outside the current mission",
                    evidence=outside_scope + excluded_scope,
                )
            )
        if self.focus.active_scope_id and self.focus.active_scope_id not in proposal.scope_ids:
            findings.append(
                DriftFinding(
                    kind=DriftKind.FOCUS,
                    severity=DriftSeverity.WARNING,
                    reason="proposal does not touch the active focus scope",
                    evidence=(self.focus.active_scope_id,),
                )
            )
        if not self.architectural_budget.allows(proposal):
            findings.append(
                DriftFinding(
                    kind=DriftKind.ARCHITECTURAL,
                    severity=DriftSeverity.WARNING,
                    reason="proposal exceeds architectural budget",
                    evidence=(
                        f"new_dependencies={proposal.new_dependencies}",
                        f"touched_domains={proposal.touched_domains}",
                    ),
                )
            )
        if not self.change_budget.allows(proposal):
            findings.append(
                DriftFinding(
                    kind=DriftKind.BUDGET,
                    severity=DriftSeverity.WARNING,
                    reason="proposal exceeds change budget",
                    evidence=(f"changed_files={proposal.changed_files}", f"risk_score={proposal.risk_score}"),
                )
            )
        return DriftReport(
            report_id=f"drift:{self.mission_id}:{proposal.proposal_id}",
            mission_id=self.mission_id,
            proposal_id=proposal.proposal_id,
            findings=tuple(findings),
        )

    def _check_intent(self, proposal: ImplementationProposal) -> BearingCheck:
        if proposal.intent_id == self.intent.intent_id:
            return BearingCheck(BearingCheckKind.INTENT_ALIGNMENT, BearingStatus.ALIGNED, "proposal targets mission intent")
        return BearingCheck(
            BearingCheckKind.INTENT_ALIGNMENT,
            BearingStatus.MISALIGNED,
            "proposal targets a different intent",
            evidence=(proposal.intent_id, self.intent.intent_id),
        )

    def _check_scope(self, proposal: ImplementationProposal) -> BearingCheck:
        outside = _sorted_tuple(set(proposal.scope_ids) - self.included_scope_ids)
        excluded = _sorted_tuple(set(proposal.scope_ids) & self.excluded_scope_ids)
        if not outside and not excluded:
            return BearingCheck(BearingCheckKind.SCOPE_COMPLIANCE, BearingStatus.ALIGNED, "proposal stays in mission scope")
        return BearingCheck(
            BearingCheckKind.SCOPE_COMPLIANCE,
            BearingStatus.MISALIGNED,
            "proposal touches out-of-scope work",
            evidence=outside + excluded,
        )

    def _check_focus(self, proposal: ImplementationProposal) -> BearingCheck:
        if self.focus.active_scope_id is None or self.focus.active_scope_id in proposal.scope_ids:
            return BearingCheck(BearingCheckKind.FOCUS_ALIGNMENT, BearingStatus.ALIGNED, "proposal supports current focus")
        return BearingCheck(
            BearingCheckKind.FOCUS_ALIGNMENT,
            BearingStatus.NEEDS_ATTENTION,
            "proposal does not support current focus",
            evidence=(self.focus.active_scope_id,),
        )

    def _check_constraints(self, proposal: ImplementationProposal) -> BearingCheck:
        violated_hard = _sorted_tuple(set(proposal.violated_constraint_ids) & self.hard_constraint_ids)
        unknown = _sorted_tuple(set(proposal.violated_constraint_ids) - {constraint.constraint_id for constraint in self.constraints})
        if not violated_hard and not unknown:
            return BearingCheck(
                BearingCheckKind.CONSTRAINT_COMPLIANCE,
                BearingStatus.ALIGNED,
                "proposal does not report constraint violations",
            )
        status = BearingStatus.MISALIGNED if violated_hard else BearingStatus.NEEDS_ATTENTION
        return BearingCheck(
            BearingCheckKind.CONSTRAINT_COMPLIANCE,
            status,
            "proposal reports constraint concerns",
            evidence=violated_hard + unknown,
        )

    def _check_acceptance(self, proposal: ImplementationProposal) -> BearingCheck:
        unknown = _sorted_tuple(set(proposal.addressed_acceptance_ids) - self.acceptance_ids)
        if unknown:
            return BearingCheck(
                BearingCheckKind.ACCEPTANCE_IMPACT,
                BearingStatus.NEEDS_ATTENTION,
                "proposal references unknown acceptance criteria",
                evidence=unknown,
            )
        if proposal.addressed_acceptance_ids:
            return BearingCheck(
                BearingCheckKind.ACCEPTANCE_IMPACT,
                BearingStatus.ALIGNED,
                "proposal advances explicit acceptance criteria",
                evidence=proposal.addressed_acceptance_ids,
            )
        return BearingCheck(
            BearingCheckKind.ACCEPTANCE_IMPACT,
            BearingStatus.NEEDS_ATTENTION,
            "proposal does not identify acceptance impact",
        )

    def _check_change_budget(self, proposal: ImplementationProposal) -> BearingCheck:
        if self.change_budget.allows(proposal):
            return BearingCheck(BearingCheckKind.CHANGE_BUDGET_COMPLIANCE, BearingStatus.ALIGNED, "proposal stays within change budget")
        return BearingCheck(
            BearingCheckKind.CHANGE_BUDGET_COMPLIANCE,
            BearingStatus.NEEDS_ATTENTION,
            "proposal exceeds change budget",
            evidence=(f"changed_files={proposal.changed_files}", f"risk_score={proposal.risk_score}"),
        )

    def _check_architectural_budget(self, proposal: ImplementationProposal) -> BearingCheck:
        if self.architectural_budget.allows(proposal):
            return BearingCheck(
                BearingCheckKind.ARCHITECTURAL_BUDGET_COMPLIANCE,
                BearingStatus.ALIGNED,
                "proposal stays within architectural budget",
            )
        return BearingCheck(
            BearingCheckKind.ARCHITECTURAL_BUDGET_COMPLIANCE,
            BearingStatus.NEEDS_ATTENTION,
            "proposal exceeds architectural budget",
            evidence=(f"new_dependencies={proposal.new_dependencies}", f"touched_domains={proposal.touched_domains}"),
        )

    @staticmethod
    def _validate_unique(field: str, values: list[str]) -> None:
        if len(values) != len(set(values)):
            raise ValueError(f"{field} ids must be unique")


def freeze_metadata(metadata: Mapping[str, object] | None = None) -> Mapping[str, object]:
    normalized = dict(metadata or {})
    if len(normalized) > MAX_METADATA_KEYS:
        raise ValueError("metadata exceeds maximum key count")
    checked: dict[str, object] = {}
    for key, value in normalized.items():
        checked[_normalize_text(str(key), "metadata key", MAX_ID_LENGTH)] = _normalize_metadata_value(value)
    return MappingProxyType(checked)


def _normalize_metadata_value(value: object) -> object:
    if len(str(value)) > MAX_METADATA_VALUE_LENGTH:
        raise ValueError("metadata value exceeds maximum length")
    return value


def _normalize_id(value: str, field: str) -> str:
    return _normalize_text(value, field, MAX_ID_LENGTH)


def _normalize_text(value: str, field: str, max_length: int) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field} is required")
    if len(normalized) > max_length:
        raise ValueError(f"{field} exceeds maximum length")
    return normalized


def _normalize_non_negative_int(value: int, field: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a non-negative integer")
    normalized = int(value)
    if normalized < 0:
        raise ValueError(f"{field} must be non-negative")
    return normalized


def _coerce_enum(value: object, enum_type: type[Enum], field: str) -> Enum:
    try:
        return enum_type(value)
    except ValueError as exc:
        raise ValueError(f"{field} is invalid") from exc


def _freeze_ids(values: tuple[str, ...], field: str) -> tuple[str, ...]:
    checked = tuple(_normalize_id(value, field) for value in values)
    if len(checked) > MAX_MISSION_ITEMS:
        raise ValueError(f"{field} exceeds maximum item count")
    if len(checked) != len(set(checked)):
        raise ValueError(f"{field} must be unique")
    return checked


def _freeze_texts(values: tuple[str, ...], field: str, max_count: int) -> tuple[str, ...]:
    checked = tuple(_normalize_text(value, field, MAX_REASON_LENGTH) for value in values)
    if len(checked) > max_count:
        raise ValueError(f"{field} exceeds maximum item count")
    return checked


def _freeze_items(values: tuple[object, ...], field: str) -> tuple[object, ...]:
    checked = tuple(values)
    if len(checked) > MAX_MISSION_ITEMS:
        raise ValueError(f"{field} exceeds maximum item count")
    return checked


def _sorted_tuple(values: set[str] | frozenset[str]) -> tuple[str, ...]:
    return tuple(sorted(values))


def _worst_bearing_status(checks: tuple[BearingCheck, ...]) -> BearingStatus:
    if any(check.status is BearingStatus.MISALIGNED for check in checks):
        return BearingStatus.MISALIGNED
    if any(check.status is BearingStatus.NEEDS_ATTENTION for check in checks):
        return BearingStatus.NEEDS_ATTENTION
    return BearingStatus.ALIGNED
