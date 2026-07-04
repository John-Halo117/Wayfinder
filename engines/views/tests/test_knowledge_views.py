from engines.ark.ingress.reality_ingestion import RealityIngestionPipeline
from engines.interpretation.knowledge_compiler import KnowledgeCompiler
from engines.interpretation.knowledge_governance import KnowledgeGovernanceEngine
from engines.views.knowledge_retrieval import KnowledgeIndexStore
from engines.views.knowledge_views import KnowledgeViewsEngine


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


def _candidate_with(candidates, candidate_type, text):
    return next(
        item
        for item in candidates
        if item.candidate_type == candidate_type and text.lower() in (item.title + item.summary).lower()
    )


def _fixture():
    pipeline = RealityIngestionPipeline()
    preserved = pipeline.ingest(
        observations=(
            _observation(
                "obs-1",
                "msg-1",
                "Decision: Views project promoted knowledge for architecture audiences. "
                "Architecture View includes Engines, Services, Contracts, Capability, and ownership.",
            ),
            _observation(
                "obs-2",
                "msg-2",
                "Principle: Views are disposable projections. "
                "Reality precedes representation and knowledge precedes views.",
            ),
            _observation(
                "obs-3",
                "msg-3",
                "Glossary definition: KVI means Knowledge View Item. Alias: View Item.",
            ),
            _observation(
                "obs-4",
                "msg-4",
                "Capsule handoff should preserve continuity and source observations.",
            ),
            _observation(
                "obs-5",
                "msg-5",
                "TODO complete Objective View dependencies and progress tracking.",
            ),
        ),
        source="unit-test-oracle",
    )
    assert preserved.status == "ok"
    compiled = KnowledgeCompiler().compile(preserved.preserved_observations)
    assert compiled.status == "ok"
    governance = KnowledgeGovernanceEngine()
    governance.store_candidates(compiled.candidates)
    selected = (
        (_candidate_with(compiled.candidates, "decision", "architecture"), "adr_repository"),
        (_candidate_with(compiled.candidates, "principle", "disposable"), "constitution"),
        (_candidate_with(compiled.candidates, "glossary", "glossary"), "glossary"),
        (_candidate_with(compiled.candidates, "capsule", "capsule"), "capsule_repository"),
        (_candidate_with(compiled.candidates, "todo", "objective"), "execution_backlog"),
        (_candidate_with(compiled.candidates, "concept", "Capability"), "knowledge_repository"),
    )
    promotions = []
    for candidate, target in selected:
        governance.start_review(candidate.candidate_id, reviewer="human", rationale=f"Review {candidate.candidate_type}.")
        governance.approve(candidate.candidate_id, reviewer="human", rationale=f"Approve {candidate.candidate_type}.")
        promoted = governance.promote(
            candidate.candidate_id,
            target=target,
            reviewer="human",
            rationale=f"Promote {candidate.candidate_type}.",
            rollback=f"Remove promoted {candidate.candidate_type}.",
        )
        assert promoted.status == "ok"
        promotions.extend(promoted.promotion_records)
    index = KnowledgeIndexStore()
    rebuild = index.rebuild(tuple(promotions))
    assert rebuild.status == "ok"
    views = KnowledgeViewsEngine(index, candidate_records=governance.repository.records)
    return views, index, governance.repository.records


def test_timeline_conversation_and_composition_are_deterministic():
    views, _, _ = _fixture()

    first = views.timeline(conversation_id="conv-1")
    second = views.timeline(conversation_id="conv-1")
    conversation = views.conversation("conv-1")
    composed = views.compose(first, conversation, view_id="timeline-conversation")

    assert first.view_id == second.view_id
    assert [item.item_id for item in first.items] == [item.item_id for item in second.items]
    assert first.items
    assert conversation.items
    assert composed.items
    assert all(item.provenance.supporting_observations for item in composed.items)


def test_architecture_concept_decision_glossary_capsule_and_objective_views():
    views, _, _ = _fixture()

    architecture = views.architecture()
    concept = views.concept("capability")
    decision = views.decision("architecture")
    glossary = views.glossary()
    capsule = views.capsule()
    objective = views.objective()

    assert architecture.groups
    assert any(group in architecture.groups for group in ("engines", "services", "contracts", "capabilities"))
    assert concept.items
    assert decision.items
    assert glossary.items
    assert capsule.items
    assert objective.items
    assert objective.groups


def test_review_queue_view_projects_candidates_without_promoting_them():
    views, _, records = _fixture()

    review_queue = views.review_queue()

    assert review_queue.items
    assert len(review_queue.items) == len(records)
    assert {"concept", "decision", "glossary"}.issubset(set(review_queue.groups))
    assert all(item.provenance.promotion_id is None for item in review_queue.items)
    assert all(item.provenance.supporting_observations for item in review_queue.items)


def test_search_results_view_preserves_ranking_and_provenance():
    views, index, _ = _fixture()
    response = index.search("views architecture promoted", mode="hybrid")

    search_view = views.search_results(response)
    first = search_view.items[0]

    assert search_view.definition.filters["query"] == "views architecture promoted"
    assert first.fields["ranking"]
    assert first.provenance.promotion_id
    assert first.provenance.compiler_version == "1.0.0"
    assert first.provenance.promotion_version == 1


def test_view_validation_reports_retrieval_errors_without_repair():
    empty_index = KnowledgeIndexStore()
    views = KnowledgeViewsEngine(empty_index)
    response = empty_index.search("missing", mode="hybrid")

    search_view = views.search_results(response)

    assert search_view.validation_report
    assert any(issue.error_code == "MISSING_INDEXES" for issue in search_view.validation_report)
