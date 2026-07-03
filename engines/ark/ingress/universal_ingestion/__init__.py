"""Universal ingestion MVP for ARK ingress.

Contract:
- Inputs: local source archives and explicit IngestionConfig instances.
- Outputs: immutable dataclasses, structured failures, and append-only JSONL files.
- Runtime constraint: O(zip_entries + conversations + messages + artifacts), bounded
  by IngestionConfig caps.
- Memory assumption: O(max_json_bytes + max_messages_per_import), bounded by config.
- Failure cases: invalid source, unsupported format, oversized input, malformed
  ChatGPT export, write collision, and resource cap exhaustion.
- Determinism: RID generation, normalization, storage paths, search, and timeline
  ordering are deterministic for identical source bytes and configuration.
"""

from .api import IngestionAPI
from .chatgpt import ChatGPTZipAdapter
from .models import Failure, HealthStatus, IngestionConfig, IngestionResult, ObservationRecord
from .rid import cshake256_rid
from .storage import AppendOnlyObservationStore

__all__ = [
    "AppendOnlyObservationStore",
    "ChatGPTZipAdapter",
    "Failure",
    "HealthStatus",
    "IngestionAPI",
    "IngestionConfig",
    "IngestionResult",
    "ObservationRecord",
    "cshake256_rid",
]
