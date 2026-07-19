from engines.ark.ingress.reality_ingestion import RealityIngestionPipeline
from engines.interpretation.knowledge_compiler import KnowledgeCompiler
from engines.interpretation.knowledge_governance import KnowledgeGovernanceEngine


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


def _candidate_result():
    pipeline = RealityIngestionPipeline()
    preserved = pipeline.ingest(
        observations=(
            _observation(
                "obs-1",
                "msg-1",
                "Decision: Knowledge Governance requires human review before promotion. "
                "Reality precedes representation.",
            ),
            _observation(
                "obs-2",
                "msg-2",
                "Decision: Knowledge Governance requires human review before promotion. "
                "Reality precedes representation.",
            ),
            _observation(
                "obs-3",
                "msg-3",
                "TODO add promotion rollback evidence. Capsule handoff should preserve continuity.",
            ),
        ),
        source="unit-test-oracle",
    )
    assert preserved.status == "ok"
    compiled = KnowledgeCompiler().compile(preserved.preserved_observations)
    assert compiled.status == "ok"
    return compiled


def _candidate_of_type(candidates, candidate_type):
    return next(item for item in candidates if item.candidate_type == candidate_type)


def test_repository_stores_candidates_groups_and_views_deterministically():
    compiled = _candidate_result()
    first = KnowledgeGovernanceEngine()
    second = KnowledgeGovernanceEngine()

    first_result = first.store_candidates(compiled.candidates)
    second_result = second.store_candidates(compiled.candidates)

    assert first_result.status == "ok"
    assert [item.candidate.candidate_id for item in first.repository.records] == [
        item.candidate.candidate_id for item in second.repository.records
    ]
    assert [item.group_id for item in first.repository.groups] == [
        item.group_id for item in second.repository.groups
    ]
    assert any(len(group.candidate_ids) > 1 for group in first.repository.groups)
    assert {view.name for view in first.review_views()}.issuperset(
        {"Pending ADRs", "Open TODOs", "High Impact Candidates", "Duplicate Concepts"}
    )


def test_candidate_cannot_bypass_review_before_approval_or_promotion():
    compiled = _candidate_result()
    engine = KnowledgeGovernanceEngine()
    engine.store_candidates(compiled.candidates)
    decision = _candidate_of_type(compiled.candidates, "decision")

    direct_approval = engine.approve(
        decision.candidate_id,
        reviewer="human",
        rationale="Approving without review should fail.",
    )
    direct_promotion = engine.promote(
        decision.candidate_id,
        target="adr_repository",
        reviewer="human",
        rationale="Promotion without approval should fail.",
        rollback="Remove promoted ADR record.",
    )

    assert direct_approval.status == "error"
    assert any(issue.error_code == "INVALID_REVIEW_TRANSITION" for issue in direct_approval.validation_report)
    assert direct_promotion.status == "error"
    assert any(issue.error_code == "PROMOTION_REQUIRES_APPROVAL" for issue in direct_promotion.validation_report)


def test_human_review_approval_and_promotion_preserve_history_and_provenance():
    compiled = _candidate_result()
    engine = KnowledgeGovernanceEngine()
    engine.store_candidates(compiled.candidates)
    decision = _candidate_of_type(compiled.candidates, "decision")

    review = engine.start_review(
        decision.candidate_id,
        reviewer="human",
        rationale="Reviewing architectural decision candidate.",
    )
    approval = engine.approve(
        decision.candidate_id,
        reviewer="human",
        rationale="Decision is ready to become a proposed ADR record.",
    )
    promotion = engine.promote(
        decision.candidate_id,
        target="adr_repository",
        reviewer="human",
        rationale="Promote approved decision into durable ADR repository.",
        rollback="Remove this promoted ADR record and keep candidate history.",
    )

    promoted_record = promotion.candidate_records[0]
    promotion_record = promotion.promotion_records[0]

    assert review.status == "ok"
    assert approval.status == "ok"
    assert promotion.status == "ok"
    assert promoted_record.state == "promoted"
    assert len(promoted_record.review_history) == 3
    assert promoted_record.promotion_history == (promotion_record,)
    assert promotion_record.provenance["candidate_id"] == decision.candidate_id
    assert promotion_record.provenance["candidate_provenance"]["supporting_observations"]


def test_duplicate_promotion_is_reported_not_silently_reapplied():
    compiled = _candidate_result()
    engine = KnowledgeGovernanceEngine()
    engine.store_candidates(compiled.candidates)
    todo = _candidate_of_type(compiled.candidates, "todo")
    engine.start_review(todo.candidate_id, reviewer="human", rationale="Review TODO candidate.")
    engine.approve(todo.candidate_id, reviewer="human", rationale="Approve TODO for backlog.")
    first = engine.promote(
        todo.candidate_id,
        target="execution_backlog",
        reviewer="human",
        rationale="Promote TODO to backlog.",
        rollback="Remove backlog item.",
    )
    second = engine.promote(
        todo.candidate_id,
        target="execution_backlog",
        reviewer="human",
        rationale="Promote TODO to backlog.",
        rollback="Remove backlog item.",
    )

    assert first.status == "ok"
    assert second.status == "error"
    assert any(issue.error_code == "PROMOTION_REQUIRES_APPROVAL" for issue in second.validation_report)


def test_human_merge_supersedes_sources_without_collapsing_evidence():
    compiled = _candidate_result()
    duplicate_candidates = tuple(item for item in compiled.candidates if item.candidate_type == "principle")
    assert len(duplicate_candidates) >= 2
    engine = KnowledgeGovernanceEngine()
    engine.store_candidates(compiled.candidates)
    target = duplicate_candidates[0]
    source = duplicate_candidates[1]
    engine.start_review(source.candidate_id, reviewer="human", rationale="Review duplicate principle.")

    merged = engine.merge(
        (source.candidate_id,),
        target_candidate_id=target.candidate_id,
        reviewer="human",
        rationale="Merge duplicate principle candidate into stronger target.",
    )

    source_record = engine.repository.records[
        [item.candidate.candidate_id for item in engine.repository.records].index(source.candidate_id)
    ]
    target_record = engine.repository.records[
        [item.candidate.candidate_id for item in engine.repository.records].index(target.candidate_id)
    ]

    assert merged.status == "ok"
    assert source_record.state == "superseded"
    assert source_record.superseded_by == target.candidate_id
    assert source_record.merge_history[0].source_candidate_ids == (source.candidate_id,)
    assert target_record.merge_history[0].target_candidate_id == target.candidate_id
