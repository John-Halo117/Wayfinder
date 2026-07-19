# Conversation Ingestion v2

This bounded compiler ingests Build Bible-related conversations as evidence. It does not promote canonical knowledge.

## Pipeline

`source → semantic observation → capability → concept → pattern → system → standard → latent doctrine → human review`

User and assistant statements are preserved with equal evidentiary weight. Every observation carries an immutable source revision, conversation/message identity, exact character span, and original wording. Repeated wording increases raw frequency; maturity uses independent conversation count so one long conversation cannot manufacture consensus.

Latent doctrine proposals require at least three independent conversations and three physical contexts. They remain non-canonical until a person selects `draft_canonical_change` and follows Build Bible change control.

## Commands

```bash
python3 governance/intelligence/conversation_ingestion.py discover exports/ --manifest governance/imports/conversations-v2.json
python3 governance/intelligence/conversation_ingestion.py run governance/imports/conversations-v2.json
python3 governance/intelligence/conversation_ingestion.py validate
```

Codex JSONL sessions must be listed explicitly with `source_type: codex_session` and a `conversation_id`. Automatic discovery deliberately skips them because a session can contain several referenced conversations.

Outputs are deterministic JSONL review artifacts in `governance/reports/conversation-ingestion-v2/`. Source and batch caps fail explicitly; an invalid source is recorded without discarding valid sources in the same batch.
