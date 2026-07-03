"""Conversation substrate canonical model.

Contract:
- Inputs: vendor conversation exports mapped by adapters.
- Outputs: conversation/message observation candidates.
- Runtime constraint: O(conversations + messages), bounded by IngestionConfig.
- Memory assumption: O(messages), bounded by IngestionConfig.
- Failure cases: malformed conversation, malformed message, and cap exhaustion.
- Determinism: message ordering is stable by timestamp and source ID.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class ConversationMessage:
    message_id: str
    timestamp: str
    actor: str
    content: str
    metadata: Mapping[str, object]


@dataclass(frozen=True)
class ConversationThread:
    conversation_id: str
    title: str
    timestamp: str
    messages: tuple[ConversationMessage, ...]
    metadata: Mapping[str, object]
