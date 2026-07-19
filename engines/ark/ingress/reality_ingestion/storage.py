"""Replaceable append-only storage boundary for ARK reality ingestion."""

from __future__ import annotations

from dataclasses import replace
from typing import Protocol

from .models import (
    DEFAULT_PRESERVED_AT,
    IngestionFailure,
    LastVerifiedReality,
    PreservedObservationRecord,
    PreservedRelationshipRecord,
    RealityReplayResult,
    StorageWriteResult,
)


class RealityStorage(Protocol):
    """Storage Service abstraction consumed by ARK."""

    def preserve_observation(self, record: PreservedObservationRecord) -> StorageWriteResult:
        """Append or idempotently return an observation preservation record."""

    def preserve_relationship(self, record: PreservedRelationshipRecord) -> StorageWriteResult:
        """Append or idempotently return a relationship preservation record."""

    def last_verified_reality(self) -> LastVerifiedReality:
        """Return the current LVR cursor."""

    def contains_reference(self, reference_id: str) -> bool:
        """Return whether storage already knows an observation reference."""

    def replay(
        self,
        *,
        after_observation_sequence: int = 0,
        after_relationship_sequence: int = 0,
        limit: int | None = None,
    ) -> RealityReplayResult:
        """Replay preserved reality records after the supplied cursors."""


class InMemoryRealityStorage:
    """Bounded in-memory proof of the storage contract.

    This is a replaceable test implementation, not a selected durable backend.
    """

    def __init__(self, *, max_observations: int = 100_000, max_relationships: int = 250_000) -> None:
        if max_observations <= 0:
            raise ValueError("max_observations must be positive")
        if max_relationships <= 0:
            raise ValueError("max_relationships must be positive")
        self._max_observations = max_observations
        self._max_relationships = max_relationships
        self._observations: list[PreservedObservationRecord] = []
        self._relationships: list[PreservedRelationshipRecord] = []
        self._observations_by_id: dict[str, PreservedObservationRecord] = {}
        self._relationships_by_id: dict[str, PreservedRelationshipRecord] = {}
        self._lvr = LastVerifiedReality(0, None, None, DEFAULT_PRESERVED_AT)

    def preserve_observation(self, record: PreservedObservationRecord) -> StorageWriteResult:
        existing = self._observations_by_id.get(record.observation_id)
        if existing is not None:
            if existing.content_hash == record.content_hash:
                return StorageWriteResult("already_preserved", existing)
            return StorageWriteResult(
                "error",
                None,
                IngestionFailure.build(
                    "STORAGE_DUPLICATE_OBSERVATION",
                    "observation_id already exists with different content",
                    {"observation_id": record.observation_id},
                    recoverable=False,
                ),
            )
        if len(self._observations) >= self._max_observations:
            return StorageWriteResult(
                "error",
                None,
                IngestionFailure.build(
                    "STORAGE_OBSERVATION_LIMIT",
                    "observation storage limit exceeded",
                    {"max_observations": self._max_observations},
                ),
            )
        preserved = replace(record, sequence=len(self._observations) + 1)
        self._observations.append(preserved)
        self._observations_by_id[preserved.observation_id] = preserved
        self._lvr = LastVerifiedReality(
            sequence=preserved.sequence,
            observation_id=preserved.observation_id,
            content_hash=preserved.content_hash,
            updated_at=preserved.preserved_at,
        )
        return StorageWriteResult("preserved", preserved)

    def preserve_relationship(self, record: PreservedRelationshipRecord) -> StorageWriteResult:
        existing = self._relationships_by_id.get(record.relationship_id)
        if existing is not None:
            if existing.content_hash == record.content_hash:
                return StorageWriteResult("already_preserved", existing)
            return StorageWriteResult(
                "error",
                None,
                IngestionFailure.build(
                    "STORAGE_DUPLICATE_RELATIONSHIP",
                    "relationship_id already exists with different content",
                    {"relationship_id": record.relationship_id},
                    recoverable=False,
                ),
            )
        if len(self._relationships) >= self._max_relationships:
            return StorageWriteResult(
                "error",
                None,
                IngestionFailure.build(
                    "STORAGE_RELATIONSHIP_LIMIT",
                    "relationship storage limit exceeded",
                    {"max_relationships": self._max_relationships},
                ),
            )
        preserved = replace(record, sequence=len(self._relationships) + 1)
        self._relationships.append(preserved)
        self._relationships_by_id[preserved.relationship_id] = preserved
        return StorageWriteResult("preserved", preserved)

    def last_verified_reality(self) -> LastVerifiedReality:
        return self._lvr

    def contains_reference(self, reference_id: str) -> bool:
        return reference_id in self._observations_by_id

    def replay(
        self,
        *,
        after_observation_sequence: int = 0,
        after_relationship_sequence: int = 0,
        limit: int | None = None,
    ) -> RealityReplayResult:
        if after_observation_sequence < 0 or after_relationship_sequence < 0:
            return RealityReplayResult(
                "error",
                (),
                (),
                after_observation_sequence,
                after_relationship_sequence,
                IngestionFailure.build("REPLAY_CURSOR_INVALID", "replay cursors must be non-negative"),
            )
        effective_limit = max(self._max_observations, self._max_relationships) if limit is None else limit
        if effective_limit <= 0:
            return RealityReplayResult(
                "error",
                (),
                (),
                after_observation_sequence,
                after_relationship_sequence,
                IngestionFailure.build("REPLAY_LIMIT_INVALID", "replay limit must be positive"),
            )
        observations = tuple(
            item for item in self._observations if item.sequence > after_observation_sequence
        )[:effective_limit]
        relationships = tuple(
            item for item in self._relationships if item.sequence > after_relationship_sequence
        )[:effective_limit]
        next_observation = observations[-1].sequence if observations else after_observation_sequence
        next_relationship = relationships[-1].sequence if relationships else after_relationship_sequence
        return RealityReplayResult("ok", observations, relationships, next_observation, next_relationship)
