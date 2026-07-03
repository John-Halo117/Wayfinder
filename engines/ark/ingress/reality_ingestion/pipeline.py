"""Canonical ARK reality ingestion pipeline."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from hashlib import sha256
from json import dumps
from typing import Any, Iterable, Mapping, Protocol

from .events import EventSink, NoopEventSink
from .models import (
    DEFAULT_PRESERVED_AT,
    IdentityResolutionRecord,
    IngestionValidationIssue,
    LastVerifiedReality,
    PreservedObservationRecord,
    PreservedRelationshipRecord,
    PromotionHistoryEntry,
    RealityEvent,
    RealityIngestionLimits,
    RealityIngestionResult,
    to_plain,
)
from .storage import InMemoryRealityStorage, RealityStorage

REQUIRED_PROVENANCE_FIELDS = (
    "original_file",
    "original_path",
    "parser_version",
    "import_timestamp",
    "hash",
)


class IdentityResolver(Protocol):
    """Identity Service protocol consumed by ARK."""

    def resolve(self, query: str) -> object:
        """Resolve a RID or alias query."""


class RealityIngestionPipeline:
    """Validate and preserve canonical observations without interpretation."""

    def __init__(
        self,
        *,
        identity_service: IdentityResolver | None = None,
        storage: RealityStorage | None = None,
        event_sink: EventSink | None = None,
        limits: RealityIngestionLimits = RealityIngestionLimits(),
        preserved_at: str = DEFAULT_PRESERVED_AT,
    ) -> None:
        _validate_limits(limits)
        self._identity_service = identity_service
        self._storage = storage or InMemoryRealityStorage(
            max_observations=limits.max_observations,
            max_relationships=limits.max_relationships,
        )
        self._event_sink = event_sink or NoopEventSink()
        self._limits = limits
        self._preserved_at = preserved_at

    @property
    def storage(self) -> RealityStorage:
        """Expose the injected storage boundary for replay and inspection."""

        return self._storage

    def ingest(
        self,
        *,
        observations: Iterable[object],
        relationships: Iterable[object] = (),
        artifacts: Iterable[object] = (),
        source: str = "canonical-observation-source",
        correlation_id: str | None = None,
    ) -> RealityIngestionResult:
        """Preserve one batch of canonical observation contract records."""

        observation_inputs = tuple(_as_mapping(item) for item in observations)
        relationship_inputs = tuple(_as_mapping(item) for item in relationships)
        artifact_inputs = tuple(_as_mapping(item) for item in artifacts)
        _check_count("observations", len(observation_inputs), self._limits.max_observations)
        _check_count("relationships", len(relationship_inputs), self._limits.max_relationships)
        _check_count("artifacts", len(artifact_inputs), self._limits.max_artifacts)

        batch_hash = _content_hash(
            {
                "observations": observation_inputs,
                "relationships": relationship_inputs,
                "artifacts": artifact_inputs,
                "source": source,
            }
        )
        batch_id = _stable_id("reality-batch", batch_hash)
        issues: list[IngestionValidationIssue] = []
        identity_resolutions: list[IdentityResolutionRecord] = []
        preserved_observations: list[PreservedObservationRecord] = []
        preserved_relationships: list[PreservedRelationshipRecord] = []
        events = []

        seen_observations: dict[str, str] = {}
        accepted_observation_ids: set[str] = set()
        known_artifact_ids = _artifact_ids(artifact_inputs)

        for observation in observation_inputs:
            observation_id = str(observation.get("observation_id", "")).strip()
            content_hash = _content_hash(observation)
            validation_errors = self._validate_observation(observation, issues)
            if observation_id in seen_observations and seen_observations[observation_id] != content_hash:
                validation_errors = True
                issues.append(
                    _issue(
                        "DUPLICATE_OBSERVATION",
                        "Duplicate observation_id has different content in the same batch.",
                        {"observation_id": observation_id},
                        severity="error",
                        recoverable=False,
                    )
                )
            seen_observations[observation_id] = content_hash
            if validation_errors:
                events.append(
                    self._publish(
                        _event(
                            "ObservationRejected",
                            "ark.observation.rejected",
                            {"observation_id": observation_id, "batch_id": batch_id},
                            batch_id,
                            correlation_id,
                        )
                    )
                )
                continue

            identity_record, identity_conflict = self._resolve_identity(observation, issues)
            identity_resolutions.append(identity_record)
            if identity_conflict:
                events.append(
                    self._publish(
                        _event(
                            "IdentityConflict",
                            "ark.identity.conflict",
                            {"observation_id": observation_id, "batch_id": batch_id},
                            batch_id,
                            correlation_id,
                        )
                    )
                )
                events.append(
                    self._publish(
                        _event(
                            "ObservationRejected",
                            "ark.observation.rejected",
                            {"observation_id": observation_id, "batch_id": batch_id},
                            batch_id,
                            correlation_id,
                        )
                    )
                )
                continue
            if identity_record.status == "resolved":
                events.append(
                    self._publish(
                        _event(
                            "IdentityResolved",
                            "ark.identity.resolved",
                            {
                                "observation_id": observation_id,
                                "canonical_rid": identity_record.canonical_rid,
                                "batch_id": batch_id,
                            },
                            batch_id,
                            correlation_id,
                        )
                    )
                )

            record = self._build_observation_record(
                observation,
                content_hash=content_hash,
                canonical_rid=identity_record.canonical_rid,
            )
            write_result = self._storage.preserve_observation(record)
            if write_result.status == "error" or write_result.record is None:
                failure = write_result.failure
                issues.append(
                    _issue(
                        getattr(failure, "error_code", "STORAGE_FAILURE"),
                        getattr(failure, "reason", "storage failed to preserve observation"),
                        dict(getattr(failure, "context", {}) or {"observation_id": observation_id}),
                        severity="error",
                        recoverable=getattr(failure, "recoverable", True),
                    )
                )
                continue
            preserved = write_result.record
            if isinstance(preserved, PreservedObservationRecord):
                preserved_observations.append(preserved)
                accepted_observation_ids.add(preserved.observation_id)
                if write_result.status == "preserved":
                    events.append(
                        self._publish(
                            _event(
                                "ObservationPreserved",
                                "ark.observation.preserved",
                                {
                                    "observation_id": preserved.observation_id,
                                    "sequence": preserved.sequence,
                                    "batch_id": batch_id,
                                },
                                batch_id,
                                correlation_id,
                            )
                        )
                    )

        valid_reference_ids = accepted_observation_ids | known_artifact_ids
        seen_relationships: dict[str, str] = {}
        for relationship in relationship_inputs:
            relationship_id = str(relationship.get("relationship_id", "")).strip()
            content_hash = _content_hash(relationship)
            validation_errors = self._validate_relationship(relationship, valid_reference_ids, issues)
            if relationship_id in seen_relationships and seen_relationships[relationship_id] != content_hash:
                validation_errors = True
                issues.append(
                    _issue(
                        "DUPLICATE_RELATIONSHIP",
                        "Duplicate relationship_id has different content in the same batch.",
                        {"relationship_id": relationship_id},
                        severity="error",
                        recoverable=False,
                    )
                )
            seen_relationships[relationship_id] = content_hash
            if validation_errors:
                continue
            record = self._build_relationship_record(relationship, content_hash=content_hash)
            write_result = self._storage.preserve_relationship(record)
            if write_result.status == "error" or write_result.record is None:
                failure = write_result.failure
                issues.append(
                    _issue(
                        getattr(failure, "error_code", "STORAGE_FAILURE"),
                        getattr(failure, "reason", "storage failed to preserve relationship"),
                        dict(getattr(failure, "context", {}) or {"relationship_id": relationship_id}),
                        severity="error",
                        recoverable=getattr(failure, "recoverable", True),
                    )
                )
                continue
            preserved = write_result.record
            if isinstance(preserved, PreservedRelationshipRecord):
                preserved_relationships.append(preserved)
                if write_result.status == "preserved":
                    events.append(
                        self._publish(
                            _event(
                                "RelationshipPreserved",
                                "ark.relationship.preserved",
                                {
                                    "relationship_id": preserved.relationship_id,
                                    "sequence": preserved.sequence,
                                    "batch_id": batch_id,
                                },
                                batch_id,
                                correlation_id,
                            )
                        )
                    )

        for issue in issues:
            if issue.severity == "error":
                events.append(
                    self._publish(
                        _event(
                            "ValidationFailed",
                            "ark.validation.failed",
                            {
                                "issue_id": issue.issue_id,
                                "error_code": issue.error_code,
                                "batch_id": batch_id,
                            },
                            batch_id,
                            correlation_id,
                        )
                    )
                )

        if any(item.status == "ok" and item.event.event_type in {"ObservationPreserved", "RelationshipPreserved"} for item in events):
            events.append(
                self._publish(
                    _event(
                        "ImportCompleted",
                        "ark.import.completed",
                        {
                            "batch_id": batch_id,
                            "preserved_observations": len(preserved_observations),
                            "preserved_relationships": len(preserved_relationships),
                        },
                        batch_id,
                        correlation_id,
                    )
                )
            )

        for event_record in events:
            if event_record.status == "error" and event_record.failure is not None:
                issues.append(
                    _issue(
                        event_record.failure.error_code,
                        event_record.failure.reason,
                        {
                            **dict(event_record.failure.context),
                            "event_id": event_record.event.event_id,
                        },
                        severity="error",
                        recoverable=event_record.failure.recoverable,
                    )
                )

        status = "ok" if not any(issue.severity == "error" for issue in issues) else "error"
        return RealityIngestionResult(
            status=status,
            batch_id=batch_id,
            source=source,
            preserved_observations=tuple(sorted(preserved_observations, key=lambda item: item.sequence)),
            preserved_relationships=tuple(sorted(preserved_relationships, key=lambda item: item.sequence)),
            identity_resolutions=tuple(sorted(identity_resolutions, key=lambda item: item.observation_id)),
            validation_report=tuple(sorted(issues, key=lambda item: item.issue_id)),
            event_publications=tuple(events),
            last_verified_reality=self._storage.last_verified_reality(),
        )

    def replay(
        self,
        *,
        after_observation_sequence: int = 0,
        after_relationship_sequence: int = 0,
        limit: int | None = None,
    ) -> object:
        """Replay through the storage boundary."""

        return self._storage.replay(
            after_observation_sequence=after_observation_sequence,
            after_relationship_sequence=after_relationship_sequence,
            limit=limit,
        )

    def _validate_observation(
        self,
        observation: Mapping[str, object],
        issues: list[IngestionValidationIssue],
    ) -> bool:
        has_error = False
        observation_id = str(observation.get("observation_id", "")).strip()
        for field in ("observation_id", "source", "artifact_type", "original_location"):
            if not str(observation.get(field, "")).strip():
                has_error = True
                issues.append(
                    _issue(
                        "OBSERVATION_CONTRACT_VIOLATION",
                        "Observation is missing a required contract field.",
                        {"field": field, "observation_id": observation_id},
                        severity="error",
                    )
                )
        timestamp = observation.get("timestamp")
        if timestamp is None or str(timestamp).strip() == "":
            issues.append(
                _issue(
                    "OBSERVATION_TIMESTAMP_MISSING",
                    "Observation timestamp is missing; preservation continues with provenance timestamp only.",
                    {"observation_id": observation_id},
                    severity="warning",
                )
            )
        provenance = observation.get("provenance")
        if not isinstance(provenance, Mapping):
            has_error = True
            issues.append(
                _issue(
                    "PROVENANCE_MISSING",
                    "Observation is missing provenance.",
                    {"observation_id": observation_id},
                    severity="error",
                )
            )
            return has_error
        if len(provenance) > self._limits.max_provenance_keys:
            has_error = True
            issues.append(
                _issue(
                    "PROVENANCE_LIMIT_EXCEEDED",
                    "Provenance key count exceeds configured maximum.",
                    {"observation_id": observation_id, "limit": self._limits.max_provenance_keys},
                    severity="error",
                )
            )
        for field in REQUIRED_PROVENANCE_FIELDS:
            if not str(provenance.get(field, "")).strip():
                has_error = True
                issues.append(
                    _issue(
                        "PROVENANCE_FIELD_MISSING",
                        "Provenance is missing a required field.",
                        {"field": field, "observation_id": observation_id},
                        severity="error",
                    )
                )
        metadata = observation.get("metadata", {})
        if isinstance(metadata, Mapping) and len(metadata) > self._limits.max_metadata_keys:
            has_error = True
            issues.append(
                _issue(
                    "OBSERVATION_METADATA_LIMIT_EXCEEDED",
                    "Observation metadata key count exceeds configured maximum.",
                    {"observation_id": observation_id, "limit": self._limits.max_metadata_keys},
                    severity="error",
                )
            )
        if len(dumps(to_plain(observation), sort_keys=True, default=str).encode("utf-8")) > self._limits.max_payload_bytes:
            has_error = True
            issues.append(
                _issue(
                    "OBSERVATION_PAYLOAD_LIMIT_EXCEEDED",
                    "Observation payload exceeds configured maximum.",
                    {"observation_id": observation_id, "limit": self._limits.max_payload_bytes},
                    severity="error",
                )
            )
        return has_error

    def _validate_relationship(
        self,
        relationship: Mapping[str, object],
        valid_reference_ids: set[str],
        issues: list[IngestionValidationIssue],
    ) -> bool:
        has_error = False
        relationship_id = str(relationship.get("relationship_id", "")).strip()
        for field in ("relationship_id", "relationship_type", "source_id", "target_id"):
            if not str(relationship.get(field, "")).strip():
                has_error = True
                issues.append(
                    _issue(
                        "RELATIONSHIP_CONTRACT_VIOLATION",
                        "Relationship is missing a required contract field.",
                        {"field": field, "relationship_id": relationship_id},
                        severity="error",
                    )
                )
        provenance = relationship.get("provenance")
        if not isinstance(provenance, Mapping):
            has_error = True
            issues.append(
                _issue(
                    "RELATIONSHIP_PROVENANCE_MISSING",
                    "Relationship is missing provenance.",
                    {"relationship_id": relationship_id},
                    severity="error",
                )
            )
        for endpoint in ("source_id", "target_id"):
            endpoint_value = str(relationship.get(endpoint, "")).strip()
            if (
                endpoint_value
                and endpoint_value not in valid_reference_ids
                and not self._storage.contains_reference(endpoint_value)
            ):
                has_error = True
                issues.append(
                    _issue(
                        "RELATIONSHIP_REFERENCE_BROKEN",
                        "Relationship endpoint does not reference a preserved observation or known artifact.",
                        {
                            "relationship_id": relationship_id,
                            "endpoint": endpoint,
                            "endpoint_id": endpoint_value,
                        },
                        severity="error",
                    )
                )
        return has_error

    def _resolve_identity(
        self,
        observation: Mapping[str, object],
        issues: list[IngestionValidationIssue],
    ) -> tuple[IdentityResolutionRecord, bool]:
        observation_id = str(observation.get("observation_id", "")).strip()
        queries = _identity_queries(observation)
        if self._identity_service is None or not queries:
            return IdentityResolutionRecord(observation_id, "unresolved", None, queries), False
        resolved: dict[str, str] = {}
        failures: list[str] = []
        for query in queries:
            result = self._identity_service.resolve(query)
            if getattr(result, "status", "") == "ok" and getattr(result, "canonical_rid", None):
                resolved[query] = str(getattr(result, "canonical_rid"))
            else:
                failure = getattr(result, "failure", None)
                failures.append(str(getattr(failure, "error_code", "IDENTITY_NOT_RESOLVED")))
        canonical_rids = tuple(dict.fromkeys(resolved.values()))
        if len(canonical_rids) > 1:
            issues.append(
                _issue(
                    "IDENTITY_CONFLICT",
                    "Observation identity queries resolved to multiple canonical RIDs.",
                    {"observation_id": observation_id, "canonical_rids": canonical_rids},
                    severity="error",
                    recoverable=False,
                )
            )
            return IdentityResolutionRecord(observation_id, "conflict", None, queries, "IDENTITY_CONFLICT"), True
        if canonical_rids:
            return IdentityResolutionRecord(observation_id, "resolved", canonical_rids[0], queries), False
        return (
            IdentityResolutionRecord(
                observation_id,
                "unresolved",
                None,
                queries,
                failures[0] if failures else "IDENTITY_NOT_RESOLVED",
            ),
            False,
        )

    def _build_observation_record(
        self,
        observation: Mapping[str, object],
        *,
        content_hash: str,
        canonical_rid: str | None,
    ) -> PreservedObservationRecord:
        observation_id = str(observation["observation_id"])
        provenance = _as_mapping(observation["provenance"])
        return PreservedObservationRecord(
            preservation_id=_stable_id("ark-observation", observation_id, content_hash),
            sequence=0,
            observation_id=observation_id,
            source=str(observation["source"]),
            artifact_type=str(observation["artifact_type"]),
            timestamp=_nullable_text(observation.get("timestamp")),
            original_location=str(observation["original_location"]),
            canonical_rid=canonical_rid,
            content_hash=content_hash,
            raw_observation=_freeze_mapping(observation),
            provenance=_freeze_mapping(provenance),
            validation_status="accepted",
            parsing_status=_nullable_text(observation.get("parsing_status")),
            preserved_at=self._preserved_at,
            promotion_history=(
                PromotionHistoryEntry("observation_preserved", self._preserved_at, "ark", content_hash),
            ),
        )

    def _build_relationship_record(
        self,
        relationship: Mapping[str, object],
        *,
        content_hash: str,
    ) -> PreservedRelationshipRecord:
        relationship_id = str(relationship["relationship_id"])
        provenance = _as_mapping(relationship["provenance"])
        return PreservedRelationshipRecord(
            preservation_id=_stable_id("ark-relationship", relationship_id, content_hash),
            sequence=0,
            relationship_id=relationship_id,
            relationship_type=str(relationship["relationship_type"]),
            source_id=str(relationship["source_id"]),
            target_id=str(relationship["target_id"]),
            content_hash=content_hash,
            raw_relationship=_freeze_mapping(relationship),
            provenance=_freeze_mapping(provenance),
            validation_status="accepted",
            preserved_at=self._preserved_at,
        )

    def _publish(self, event: RealityEvent) -> object:
        return self._event_sink.publish(event)


def _validate_limits(limits: RealityIngestionLimits) -> None:
    for field in (
        "max_observations",
        "max_relationships",
        "max_artifacts",
        "max_payload_bytes",
        "max_provenance_keys",
        "max_metadata_keys",
    ):
        if getattr(limits, field) <= 0:
            raise ValueError(f"{field} must be positive")


def _check_count(name: str, count: int, limit: int) -> None:
    if count > limit:
        raise ValueError(f"{name} count exceeds configured maximum")


def _as_mapping(value: object) -> Mapping[str, object]:
    if is_dataclass(value):
        plain = asdict(value)
    elif isinstance(value, Mapping):
        plain = dict(value)
    elif hasattr(value, "__dict__"):
        plain = dict(vars(value))
    else:
        raise TypeError("canonical records must be mappings or dataclass-like objects")
    return _freeze_mapping(plain)


def _freeze_mapping(value: Mapping[str, object]) -> Mapping[str, object]:
    frozen: dict[str, object] = {}
    for key, item in value.items():
        if is_dataclass(item):
            frozen[str(key)] = _freeze_mapping(asdict(item))
        elif isinstance(item, Mapping):
            frozen[str(key)] = _freeze_mapping(item)
        elif isinstance(item, tuple):
            frozen[str(key)] = tuple(_freeze_sequence(item))
        elif isinstance(item, list):
            frozen[str(key)] = tuple(_freeze_sequence(item))
        else:
            frozen[str(key)] = item
    return frozen


def _freeze_sequence(value: Iterable[object]) -> Iterable[object]:
    for item in value:
        if is_dataclass(item):
            yield _freeze_mapping(asdict(item))
        elif isinstance(item, Mapping):
            yield _freeze_mapping(item)
        elif isinstance(item, (list, tuple)):
            yield tuple(_freeze_sequence(item))
        else:
            yield item


def _artifact_ids(artifacts: tuple[Mapping[str, object], ...]) -> set[str]:
    artifact_ids: set[str] = set()
    for artifact in artifacts:
        artifact_id = str(artifact.get("artifact_id", "")).strip()
        if artifact_id:
            artifact_ids.add(artifact_id)
    return artifact_ids


def _identity_queries(observation: Mapping[str, object]) -> tuple[str, ...]:
    queries: list[str] = []
    metadata = observation.get("metadata", {})
    if isinstance(metadata, Mapping):
        for key in ("rid", "subject_rid", "identity_rid"):
            value = metadata.get(key)
            if isinstance(value, str) and value.strip():
                queries.append(value.strip())
    for field in ("conversation_reference", "message_reference", "observation_id"):
        value = observation.get(field)
        if isinstance(value, str) and value.strip():
            queries.append(value.strip())
    return tuple(dict.fromkeys(queries))


def _content_hash(value: object) -> str:
    encoded = dumps(to_plain(value), sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(encoded).hexdigest()


def _stable_id(prefix: str, *parts: object) -> str:
    payload = "\x1f".join(str(part) for part in parts)
    return f"{prefix}:{sha256(payload.encode('utf-8')).hexdigest()}"


def _issue(
    error_code: str,
    reason: str,
    context: Mapping[str, object],
    *,
    severity: str = "error",
    recoverable: bool = True,
) -> IngestionValidationIssue:
    issue_hash = _content_hash({"error_code": error_code, "reason": reason, "context": context, "severity": severity})
    return IngestionValidationIssue(
        issue_id=_stable_id("ark-issue", issue_hash),
        severity=severity,  # type: ignore[arg-type]
        error_code=error_code,
        reason=reason,
        context=_freeze_mapping(context),
        recoverable=recoverable,
    )


def _event(
    event_type: str,
    route: str,
    payload: Mapping[str, object],
    batch_id: str,
    correlation_id: str | None,
) -> RealityEvent:
    event_payload = _freeze_mapping(payload)
    event_id = _stable_id("ark-event", event_type, route, event_payload)
    return RealityEvent(
        event_id=event_id,
        event_type=event_type,
        route=route,
        payload=event_payload,
        correlation_id=correlation_id or batch_id,
        metadata={"batch_id": batch_id},
    )


def _nullable_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
