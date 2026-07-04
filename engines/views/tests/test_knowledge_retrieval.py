from engines.ark.ingress.reality_ingestion import RealityIngestionPipeline
from engines.interpretation.knowledge_compiler import KnowledgeCompiler
from engines.interpretation.knowledge_governance import KnowledgeGovernanceEngine
from engines.views.knowledge_retrieval import KnowledgeIndexStore


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


def _compiled_candidates():
    pipeline = RealityIngestionPipeline()
    preserved = pipeline.ingest(
        observations=(
            _observation(
                "obs-1",
                "msg-1",
                "Decision: ARK retrieval indexes promoted knowledge after human review. "
                "The Knowledge Index supports RID lookup and ADR history.",
            ),
            _observation(
                "obs-2",
                "msg-2",
                "Principle: Indexes are disposable and rebuildable. "
                "The capability index references services, engines, providers, and contracts.",
            ),
            _observation(
                "obs-3",
                "msg-3",
                "TODO validate timeline retrieval for capsule handoff and API autocomplete.",
            ),
        ),
        source="unit-test-oracle",
    )
    assert preserved.status == "ok"
    compiled = KnowledgeCompiler().compile(preserved.preserved_observations)
    assert compiled.status == "ok"
    return compiled.candidates


def _candidate_of_type(candidates, candidate_type):
    return next(item for item in candidates if item.candidate_type == candidate_type)


def _candidate_with_title(candidates, candidate_type, title_part):
    return next(
        item
        for item in candidates
        if item.candidate_type == candidate_type and title_part.lower() in item.title.lower()
    )


def _promotions():
    candidates = _compiled_candidates()
    engine = KnowledgeGovernanceEngine()
    engine.store_candidates(candidates)
    selected = (
        (_candidate_of_type(candidates, "decision"), "adr_repository"),
        (_candidate_of_type(candidates, "principle"), "constitution"),
        (_candidate_of_type(candidates, "todo"), "execution_backlog"),
        (_candidate_with_title(candidates, "concept", "Capability"), "knowledge_repository"),
    )
    promotions = []
    for candidate, target in selected:
        engine.start_review(candidate.candidate_id, reviewer="human", rationale=f"Review {candidate.candidate_type}.")
        engine.approve(candidate.candidate_id, reviewer="human", rationale=f"Approve {candidate.candidate_type}.")
        result = engine.promote(
            candidate.candidate_id,
            target=target,
            reviewer="human",
            rationale=f"Promote {candidate.candidate_type}.",
            rollback=f"Remove promoted {candidate.candidate_type}.",
        )
        assert result.status == "ok"
        promotions.extend(result.promotion_records)
    return tuple(promotions)


def test_rebuild_delete_and_rebuild_are_deterministic():
    promotions = _promotions()
    store = KnowledgeIndexStore()

    first = store.rebuild(promotions)
    first_results = store.search("promoted knowledge human review", mode="hybrid").results
    store.delete_indexes()
    missing = store.verify()
    second = store.rebuild(promotions)
    second_results = store.search("promoted knowledge human review", mode="hybrid").results

    assert first.status == "ok"
    assert missing.status == "error"
    assert any(issue.error_code == "MISSING_INDEXES" for issue in missing.validation_report)
    assert second.status == "ok"
    assert first.manifest.content_hash == second.manifest.content_hash
    assert [item.document.promotion_id for item in first_results] == [
        item.document.promotion_id for item in second_results
    ]


def test_hybrid_search_preserves_provenance_and_explainable_ranking():
    store = KnowledgeIndexStore()
    store.rebuild(_promotions())

    response = store.search("ARK promoted knowledge", mode="hybrid", limit=5)
    result = response.results[0]

    assert response.validation_report == ()
    assert result.score > 0
    assert {item.index_name for item in result.contributions}.issuperset({"full_text", "bm25", "embedding"})
    assert result.document.promotion_id
    assert result.document.supporting_observations
    assert result.document.source_oracles == ("unit-test-oracle",)
    assert result.document.compiler_version == "1.0.0"
    assert result.document.promotion_version == 1


def test_lookup_indexes_cover_rid_concept_capability_acronym_and_relationships():
    promotions = _promotions()
    store = KnowledgeIndexStore()
    store.rebuild(promotions)
    first = promotions[0]

    by_observation = store.lookup("rid", "obs-1")
    by_concept = store.lookup("concept", "knowledge")
    by_capability = store.lookup("capability", "capability")
    by_acronym = store.lookup("acronym", "ARK")
    related = store.related(first.candidate_ids[0])

    assert by_observation.results
    assert by_concept.results
    assert by_capability.results
    assert by_acronym.results
    assert related.results
    assert related.results[0].document.promotion_id == first.promotion_id


def test_incremental_update_timeline_history_and_autocomplete():
    promotions = _promotions()
    store = KnowledgeIndexStore()
    first = store.incremental_update(promotions[:2])
    second = store.incremental_update(promotions[2:])
    timeline = store.timeline(conversation_id="conv-1")
    history = store.history(promotions[0].candidate_ids[0])
    completions = store.autocomplete("know")
    suggestions = store.suggestions("cap")

    assert first.status == "ok"
    assert second.status == "ok"
    assert len(timeline.results) == 4
    assert history.results
    assert "knowledge" in completions
    assert "capability" in suggestions


def test_boolean_full_text_and_validation_are_deterministic():
    store = KnowledgeIndexStore()
    empty = store.search("ARK", mode="hybrid")
    store.rebuild(_promotions())
    boolean = store.search("knowledge AND promoted NOT missing", mode="full_text")
    invalid_limit = store.search("knowledge", mode="hybrid", limit=0)
    verification = store.verify()

    assert any(issue.error_code == "MISSING_INDEXES" for issue in empty.validation_report)
    assert boolean.results
    assert any(contribution.index_name == "full_text" for contribution in boolean.results[0].contributions)
    assert any(issue.error_code == "QUERY_LIMIT_INVALID" for issue in invalid_limit.validation_report)
    assert verification.status == "ok"
