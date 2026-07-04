"""ARK reality ingestion boundary.

This package accepts canonical observations from observation sources and
preserves them through replaceable identity, storage, and event interfaces.
It intentionally contains no ChatGPT-specific logic.
"""

from .events import EventBusEventSink, NoopEventSink
from .models import (
    DEFAULT_PRESERVED_AT,
    IngestionFailure,
    IngestionValidationIssue,
    LastVerifiedReality,
    PreservedObservationRecord,
    PreservedRelationshipRecord,
    RealityEvent,
    RealityIngestionLimits,
    RealityIngestionResult,
)
from .pipeline import RealityIngestionPipeline
from .storage import InMemoryRealityStorage

__all__ = [
    "DEFAULT_PRESERVED_AT",
    "EventBusEventSink",
    "IngestionFailure",
    "IngestionValidationIssue",
    "InMemoryRealityStorage",
    "LastVerifiedReality",
    "NoopEventSink",
    "PreservedObservationRecord",
    "PreservedRelationshipRecord",
    "RealityEvent",
    "RealityIngestionLimits",
    "RealityIngestionPipeline",
    "RealityIngestionResult",
]
