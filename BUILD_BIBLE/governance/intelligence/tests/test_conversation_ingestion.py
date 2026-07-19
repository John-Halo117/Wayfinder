import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import conversation_ingestion as ingestion


def conversation(identifier, text, role="user"):
    return {"conversationId": identifier, "title": "Build Bible house", "conversation": [{"role": role, "content": [{"content_type": "text", "text": text}]}]}


class ConversationIngestionTests(unittest.TestCase):
    def test_semantic_spans_preserve_exact_offsets(self):
        text = "- Add a floor drain; preserve service access."
        spans = list(ingestion.semantic_spans(text))
        self.assertEqual([text[a:b] for a, b, _ in spans], ["Add a floor drain", "preserve service access."])

    def test_equal_speaker_evidence_and_independent_counts(self):
        observations = []
        for identifier, role in (("c1", "user"), ("c2", "assistant")):
            item = conversation(identifier, "House water garden systems should remain accessible.", role)
            observations.extend(ingestion.extract_observations({"conversation": item, "source_revision": identifier}))
        candidates, _, _ = ingestion.compile_candidates(observations)
        candidate = candidates[0]
        self.assertEqual(candidate["score"]["independent_conversation_count"], 2)
        self.assertEqual(candidate["score"]["speaker_counts"], {"assistant": 1, "user": 1})

    def test_latent_doctrine_needs_three_conversations_and_contexts(self):
        observations = []
        for identifier in ("c1", "c2", "c3"):
            item = conversation(identifier, "House water garden systems should remain accessible.")
            observations.extend(ingestion.extract_observations({"conversation": item, "source_revision": identifier}))
        _, _, doctrines = ingestion.compile_candidates(observations)
        self.assertEqual(len(doctrines), 1)

    def test_pipeline_is_deterministic_and_excludes_irrelevant_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            accepted = root / "accepted.json"
            excluded = root / "excluded.json"
            accepted.write_text(json.dumps(conversation("c1", "The house kitchen needs storage and water drainage.")), encoding="utf-8")
            excluded.write_text(json.dumps({"conversationId": "c2", "title": "Poem", "conversation": [{"role": "user", "content": [{"text": "Write a rhyme about clouds."}]}]}), encoding="utf-8")
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"sources": [{"source_type": "chatgpt_export", "path": str(accepted)}, {"source_type": "chatgpt_export", "path": str(excluded)}]}), encoding="utf-8")
            old_raw, old_manifest = ingestion.RAW_ROOT, ingestion.SOURCE_MANIFEST
            ingestion.RAW_ROOT, ingestion.SOURCE_MANIFEST = root / "raw", root / "sources.jsonl"
            try:
                output = root / "output"
                first = ingestion.run_pipeline(manifest, output)
                snapshot = {p.name: p.read_bytes() for p in output.iterdir()}
                second = ingestion.run_pipeline(manifest, output)
                self.assertEqual(first, second)
                self.assertEqual(snapshot, {p.name: p.read_bytes() for p in output.iterdir()})
                self.assertEqual(first["accepted_source_count"], 1)
                self.assertEqual(first["excluded_source_count"], 1)
                self.assertEqual(ingestion.validate_output(output)["status"], "passed")
            finally:
                ingestion.RAW_ROOT, ingestion.SOURCE_MANIFEST = old_raw, old_manifest


if __name__ == "__main__":
    unittest.main()
