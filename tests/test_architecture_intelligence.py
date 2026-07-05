from __future__ import annotations

import json
from pathlib import Path

from tooling.architecture_intelligence.doctor import ArchitectureDoctor, DoctorConfig


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_architecture_doctor_detects_service_engine_violation(tmp_path: Path) -> None:
    _write(tmp_path / "services" / "identity" / "identity_service.py", "import engines.views.knowledge_views.engine\n")
    _write(tmp_path / "engines" / "views" / "knowledge_views" / "engine.py", "VALUE = 1\n")
    _write(tmp_path / "docs" / "architecture" / "00-overview.md", "# Overview\n\nReality before representation.\n")

    report = ArchitectureDoctor(tmp_path).run()

    assert report.status == "attention"
    assert report.dependency_health["service_engine_violations"] == 1
    assert any(finding.code == "SERVICE_ENGINE_IMPORT" for finding in report.findings)


def test_architecture_doctor_writes_governance_reports(tmp_path: Path) -> None:
    _write(tmp_path / "docs" / "architecture" / "00-overview.md", "# 00 Overview\n\nCanonical pipeline.\n")
    _write(tmp_path / "docs" / "architecture" / "01-reality.md", "# 01 Reality\n\nReality remains canonical.\n")
    _write(tmp_path / "docs" / "adrs" / "0001-test.md", "# ADR-0001: Test\n\n## Architecture Sections\n\n- [00 Overview](../architecture/00-overview.md)\n")
    _write(tmp_path / "capabilities" / "README.md", "# Capability Registry\n\n## Storage Capability\n\nOwner: Storage\n")
    _write(tmp_path / "engines" / "ark" / "ingress" / "chatgpt_oracle" / "README.md", "# ChatGPT Oracle\n\nProvenance and confidence are propagated.\n")
    output = tmp_path / "docs" / "governance"

    doctor = ArchitectureDoctor(tmp_path, config=DoctorConfig(max_files=100))
    report = doctor.run()
    doctor.write_reports(report, output)

    assert (output / "architecture-doctor.json").exists()
    assert (output / "architecture-graph.mmd").exists()
    assert (output / "architecture-graph.dot").exists()
    assert (output / "repository-health-dashboard.md").exists()
    generated = json.loads((output / "architecture-doctor.json").read_text(encoding="utf-8"))
    assert generated["capability_health"]["registered_capabilities"] >= 1


def test_architecture_doctor_skips_heavy_generated_knowledge(tmp_path: Path) -> None:
    _write(tmp_path / "docs" / "architecture" / "00-overview.md", "# 00 Overview\n\nArchitecture.\n")
    _write(tmp_path / "Knowledge" / "Graph" / "nodes.jsonl", "x" * 500_000)
    _write(tmp_path / "Knowledge" / "reports" / "quality_gates.json", '{"provenance_missing_count": 0}')

    report = ArchitectureDoctor(tmp_path, config=DoctorConfig(max_files=100, max_text_bytes=1_000)).run()

    assert report.knowledge_health["provenance_missing_count"] == 0
    assert report.repository_health["hash_skipped_large_files"] >= 1
