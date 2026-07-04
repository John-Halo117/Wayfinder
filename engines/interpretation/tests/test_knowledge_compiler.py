from engines.ark.ingress.reality_ingestion import RealityIngestionPipeline
from engines.interpretation.knowledge_compiler import (
    KnowledgeCompiler,
    KnowledgeCompilerConfig,
)


def _observation(observation_id, message_id, text):
    return {
        "observation_id": observation_id,
        "timestamp": "2026-01-01T00:00:00Z",
        "source": "unit-test-oracle",
        "artifact_type": "Message",
        "original_location": f"fixture/conversations.json#{message_id}",
        "conversation_reference": "conv-1",
        "message_reference": message_id,
        "author": "Tester",
        "role": "user",
        "raw_content": {"content_type": "text", "parts": [text]},
        "attachments": (),
        "metadata": {},
        "provenance": {
            "original_file": "conversations.json",
            "original_path": "conversations.json",
            "byte_offset": None,
            "conversation_id": "conv-1",
            "message_id": message_id,
            "attachment_id": None,
            "parser_name": "unit-test-oracle",
            "parser_version": "1.0.0",
            "import_timestamp": "2026-01-01T00:00:00Z",
            "hash": f"hash-{observation_id}",
        },
        "parsing_status": "parsed",
        "confidence": 1.0,
    }


def _preserved_records():
    pipeline = RealityIngestionPipeline()
    observations = (
        _observation(
            "obs-1",
            "msg-1",
            "Decision: The Knowledge Compiler consumes only ARK preserved observations. "
            "Reality precedes representation. TODO validate replay support.",
        ),
        _observation(
            "obs-2",
            "msg-2",
            "Knowledge Compiler is a candidate interpretation layer. "
            "Reality precedes representation. Capsule handoff should preserve continuity.",
        ),
        _observation(
            "obs-3",
            "msg-3",
            "Rename Vault to Knowledge Vault. Deprecated Vault conflicts with Knowledge Vault ownership.",
        ),
    )
    result = pipeline.ingest(observations=observations, source="unit-test-oracle")
    assert result.status == "ok"
    return result.preserved_observations, result.last_verified_reality


def test_compiler_consumes_ark_preserved_reality_and_is_deterministic():
    preserved, _ = _preserved_records()
    compiler = KnowledgeCompiler(
        config=KnowledgeCompilerConfig(known_terms=("Reality", "Observation", "ARK"))
    )

    first = compiler.compile(preserved)
    second = compiler.compile(preserved)

    assert first.status == "ok"
    assert [item.candidate_id for item in first.candidates] == [
        item.candidate_id for item in second.candidates
    ]
    assert {item.candidate_type for item in first.candidates}.issuperset(
        {"concept", "decision", "principle", "todo", "capsule", "novelty", "duplicate"}
    )


def test_candidates_preserve_provenance_and_remain_proposed():
    preserved, _ = _preserved_records()
    compiler = KnowledgeCompiler()

    result = compiler.compile(preserved)
    candidate = next(item for item in result.candidates if item.candidate_type == "decision")

    assert candidate.status == "proposed"
    assert candidate.provenance.compiler_version == "1.0.0"
    assert candidate.provenance.rule_set_version == "1.0.0"
    assert candidate.provenance.supporting_observations
    assert candidate.provenance.supporting_conversations == ("conv-1",)
    assert candidate.provenance.evidence[0].source_oracle == "unit-test-oracle"


def test_compiler_does_not_update_lvr_or_storage():
    preserved, lvr_before = _preserved_records()
    compiler = KnowledgeCompiler()

    result = compiler.compile(preserved)

    assert result.status == "ok"
    assert lvr_before.sequence == len(preserved)
    assert all(item.candidate_id.startswith("knowledge-candidate:") for item in result.candidates)


def test_glossary_and_contradiction_candidates_use_existing_baseline():
    preserved, _ = _preserved_records()
    compiler = KnowledgeCompiler(
        config=KnowledgeCompilerConfig(
            deprecated_terms={"Vault": "Knowledge Vault"},
            ownership_terms={"Knowledge Vault": "contracts"},
        )
    )

    result = compiler.compile(preserved)
    candidate_types = {item.candidate_type for item in result.candidates}

    assert "glossary" in candidate_types
    assert "contradiction" in candidate_types
    assert any(
        item.metadata.get("deprecated_term") == "vault"
        for item in result.candidates
        if item.candidate_type == "glossary"
    )


def test_validation_reports_missing_provenance_without_discarding_uncertainty():
    preserved, _ = _preserved_records()
    malformed = dict(preserved[0].raw_observation)
    del malformed["provenance"]

    compiler = KnowledgeCompiler()
    result = compiler.compile((malformed,))

    assert result.status == "error"
    assert any(issue.error_code == "MISSING_PROVENANCE" for issue in result.validation_report)
