import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import studio_server as studio  # noqa: E402
import aurora_cli  # noqa: E402
import aurora_core  # noqa: E402


class StudioServerTests(unittest.TestCase):
    def setUp(self):
        self.previous_state = studio.STATE.config
        self.previous_cache = studio.STATE.cache
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "BUILD_BIBLE" / "doctrine").mkdir(parents=True)
        (root / "BUILD_BIBLE" / "schemas").mkdir(parents=True)
        (root / "BUILD_OPERATIONS").mkdir(parents=True)
        (root / "BUILD_BIBLE" / "README.md").write_text("# Bible\n\n[Doctrine](doctrine/README.md)\n", encoding="utf-8")
        (root / "BUILD_BIBLE" / "doctrine" / "README.md").write_text("# Doctrine\n", encoding="utf-8")
        (root / "BUILD_BIBLE" / "schemas" / "example.schema.json").write_text(json.dumps({"type": "object"}), encoding="utf-8")
        (root / "BUILD_OPERATIONS" / "README.md").write_text("# Operations\n", encoding="utf-8")
        studio.STATE.config = studio.StudioConfig(
            repo_root=root,
            static_root=studio.STATIC_ROOT,
            cache_ttl_seconds=30.0,
            git_timeout_seconds=1.0,
        )
        studio.STATE.cache = studio.IndexCache()

    def tearDown(self):
        studio.STATE.config = self.previous_state
        studio.STATE.cache = self.previous_cache
        self.tmp.cleanup()

    def test_index_builds_with_validation(self):
        index = studio.get_index(force=True)
        self.assertEqual(index["summary"]["documents"], 4)
        self.assertEqual(index["validation"]["status"], "passed")
        self.assertEqual(index["summary"]["layers"]["root"], 1)
        self.assertEqual(index["summary"]["layers"]["operations"], 1)

    def test_search_uses_full_text(self):
        docs = studio.load_documents()
        results = studio.search_documents(docs, "Doctrine")
        self.assertTrue(results)
        self.assertEqual(results[0]["path"], "BUILD_BIBLE/doctrine/README.md")

    def test_health_reports_roots(self):
        payload = studio.health_payload()
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(len(payload["roots"]), 2)

    def test_forbidden_source_path(self):
        outside = Path(self.tmp.name) / "other.md"
        outside.write_text("# Other\n", encoding="utf-8")
        self.assertFalse(studio.is_allowed_source_path(outside.resolve()))

    def test_broken_reference_reports_error(self):
        root = studio.STATE.config.repo_root
        (root / "BUILD_BIBLE" / "bad.md").write_text("# Bad\n\n[Missing](nope.md)\n", encoding="utf-8")
        studio.STATE.cache = studio.IndexCache()
        index = studio.get_index(force=True)
        self.assertEqual(index["validation"]["status"], "failed")
        self.assertEqual(index["validation"]["counts"]["error"], 1)

    def test_platform_services_are_exposed(self):
        payload = studio.platform_payload()
        self.assertIn("serviceCatalog", payload)
        self.assertIn("repositories", payload)
        self.assertIn("workspace", payload)
        self.assertIn("jarvis", payload)
        self.assertFalse(payload["jarvis"]["implemented"])

    def test_instantiation_preview_does_not_commit(self):
        preview = studio.InstantiationService().preview("BUILD_BIBLE/doctrine/README.md", "PROPERTY_EXAMPLE")
        self.assertEqual(preview["status"], "preview")
        self.assertFalse(preview["committed"])

    def test_instantiation_rejects_non_build_bible_pattern(self):
        with self.assertRaises(studio.ClientError):
            studio.InstantiationService().preview("README.md", "PROPERTY_EXAMPLE")

    def test_aurora_command_contract_searches_repository(self):
        payload = aurora_core.execute("search", {"query": "Doctrine"}, studio.STATE.config)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["command"], "search")
        self.assertEqual(payload["data"]["results"][0]["path"], "BUILD_BIBLE/doctrine/README.md")

    def test_aurora_cli_supports_json_output(self):
        code = aurora_cli.main([
            "--repo-root",
            str(studio.STATE.config.repo_root),
            "search",
            "Doctrine",
        ])
        self.assertEqual(code, 0)

    def test_command_catalog_exposes_p7_domains(self):
        catalog = aurora_core.command_catalog()
        self.assertIn("repository", catalog["domains"])
        self.assertIn("compile", catalog["domains"])
        self.assertIn("digital-twin", catalog["domains"])
        self.assertIn("json", catalog["outputModes"])


if __name__ == "__main__":
    unittest.main()
