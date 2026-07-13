"""Build a deterministic Phase 0 inventory and Phase 1 canonical migration map."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "governance" / "reports"
MAX_ARTIFACTS = 10_000
MAX_TEXT_BYTES = 2_000_000
EXCLUDED = {
    "governance/reports/build-bible-artifact-inventory.jsonl",
    "governance/reports/build-bible-canonical-migration-map.md",
    "governance/reports/construction-knowledge-extraction-report.md",
    "governance/reports/source-corpus-canonical-import-plan.md",
    "governance/reports/source-corpus-concept-backlog.jsonl",
    "governance/reports/source-corpus-provenance-inventory.jsonl",
}
LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
RULE_RE = re.compile(r"\b(always|never|must|shall|should|prefer|minimum|default)\b", re.I)


def layer_for(path: str) -> str:
    first = path.split("/", 1)[0]
    mapping = {
        "doctrine": "Build Bible doctrine",
        "contracts": "Ecosystem Commons candidate",
        "schemas": "Ecosystem Commons candidate",
        "registries": "Build Bible domain model",
        "domains": "Build Bible domain",
        "reality": "ARK-qualified reality record",
        "lifecycle": "Build Bible lifecycle domain",
        "generation": "non-canonical generated-artifact boundary",
        "digital-twin": "Build Bible derived model",
        "governance": "Build Bible governance",
        "templates": "Build Bible authoring support",
        "indexes": "Build Bible derived index",
    }
    return mapping.get(first, "Build Bible navigation")


def candidate_for(path: str, owner: str) -> str:
    if owner == "Ecosystem Commons candidate":
        return "retain pending contract/schema ownership review; publish through Commons if shared"
    if owner == "ARK-qualified reality record":
        return "retain as domain source; persist verified evidence through ARK contracts"
    return f"retain at {path}; extract only when duplicate evidence proves a higher reusable owner"


def first_paragraph(text: str) -> str:
    blocks = re.split(r"\n\s*\n", text.strip())
    for block in blocks:
        value = " ".join(line.strip() for line in block.splitlines() if not line.startswith("#"))
        if value:
            return value[:500]
    return "Navigation or structural artifact."


def concept_owner(concept: str, paths: list[str]) -> str:
    value = concept.casefold()
    if any(word in value for word in ("standard", "verification", "label", "minimum")):
        return "Build Bible construction standard"
    if any(word in value for word in ("resource", "flow", "water", "power", "air", "heat", "light")):
        return "Build Bible construction resource"
    if any(word in value for word in ("assembly", "module", "wall", "chase", "bay")):
        return "Build Bible assembly"
    if any(word in value for word in ("pattern", "spine", "zone", "corridor", "core")):
        return "Build Bible pattern"
    if any(path.startswith("contracts/") or path.startswith("schemas/") for path in paths):
        return "Existing Build Bible contract/schema; Commons review required"
    return "Existing narrowest Build Bible owner; classification review required"


def write_extraction_report(raw: list[dict[str, object]], heading_owners: dict[str, list[str]]) -> None:
    by_path = {str(item["artifact"]): item for item in raw}
    candidates: list[dict[str, object]] = []
    ignored = {
        "applies to", "capabilities", "capacity", "constraints", "contents", "decision",
        "dependencies", "does not own", "examples", "expansion", "expansion rule",
        "expansion rules", "failure", "failure isolation", "future expansion",
        "generation targets", "history", "identity", "interfaces", "invariants",
        "lifecycle", "maintenance", "namespaces", "optional capabilities", "owns",
        "patterns", "purpose", "relationships", "required capabilities", "required fields",
        "required report fields", "required standard", "resources", "responsibilities",
        "result states", "rule", "rules", "scope", "service records", "serviceability",
        "spatial address", "status", "verification", "verification states",
    }
    for normalized, paths in heading_owners.items():
        unique_paths = sorted(set(paths))
        if len(unique_paths) < 2 or normalized in ignored:
            continue
        dependencies = sorted({
            link for path in unique_paths
            for link in by_path[path]["relationships"]
        })[:20]
        owner = concept_owner(normalized, unique_paths)
        confidence = "high" if owner.startswith("Build Bible") else "medium"
        candidates.append({
            "concept": normalized,
            "occurrences": len(unique_paths),
            "current_owners": sorted({str(by_path[path]["canonical_owner"]) for path in unique_paths}),
            "candidate_owner": owner,
            "confidence": confidence,
            "dependencies": dependencies,
            "consumers": unique_paths,
            "expected_duplication_reduction": len(unique_paths) - 1,
        })
    candidates.sort(key=lambda item: (-int(item["expected_duplication_reduction"]), str(item["concept"])))
    top = candidates[:100]
    report = OUTPUT_DIR / "construction-knowledge-extraction-report.md"
    lines = [
        "# Construction Knowledge Extraction Report",
        "",
        "Status: deterministic candidate backlog; no extraction authorized",
        "",
        "Candidates are repeated structural concepts, not confirmed duplicates. Ranking favors the largest potential reference consolidation. Generic headings are excluded.",
        "",
        "## Recommended Extraction Order",
        "",
    ]
    for index, item in enumerate(top, 1):
        dependencies = ", ".join(f"`{value}`" for value in item["dependencies"]) or "None detected"
        consumers = ", ".join(f"`{value}`" for value in item["consumers"])
        owners = ", ".join(str(value) for value in item["current_owners"])
        lines += [
            f"### {index}. {str(item['concept']).title()}",
            "",
            f"- Occurrences: {item['occurrences']}",
            f"- Current owners: {owners}",
            f"- Candidate canonical owner: {item['candidate_owner']}",
            f"- Confidence: {item['confidence']}",
            f"- Dependencies: {dependencies}",
            f"- Consumers: {consumers}",
            f"- Expected duplication reduction: up to {item['expected_duplication_reduction']} repeated declarations replaced by references",
            "- Gate: confirm semantic equivalence and the narrowest canonical owner before extraction.",
            "",
        ]
    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    files = sorted(p for p in ROOT.rglob("*") if p.is_file())
    if len(files) > MAX_ARTIFACTS:
        raise RuntimeError(f"artifact cap exceeded: {len(files)} > {MAX_ARTIFACTS}")

    raw: list[dict[str, object]] = []
    heading_owners: dict[str, list[str]] = defaultdict(list)
    for file in files:
        relative = file.relative_to(ROOT).as_posix()
        if relative in EXCLUDED or relative.startswith("governance/imports/") or "__pycache__" in file.parts:
            continue
        data = file.read_bytes()
        if len(data) > MAX_TEXT_BYTES:
            raise RuntimeError(f"text cap exceeded for {relative}")
        text = data.decode("utf-8")
        headings = [h.strip() for h in HEADING_RE.findall(text)]
        for heading in set(headings):
            heading_owners[heading.casefold()].append(relative)
        links = sorted(set(link for link in LINK_RE.findall(text) if not link.startswith(("http://", "https://", "#"))))
        owner = layer_for(relative)
        raw.append({
            "artifact": relative,
            "purpose": first_paragraph(text),
            "scope": headings[0] if headings else file.stem,
            "topics": headings[1:9],
            "relationships": links[:64],
            "provenance": {"source": relative, "sha256": hashlib.sha256(data).hexdigest()},
            "canonical_owner": owner,
            "candidate_destination": candidate_for(relative, owner),
            "confidence": "high" if headings and owner != "Build Bible navigation" else "medium",
            "rule_language_count": len(RULE_RE.findall(text)),
        })

    duplicate_counts = Counter({key: len(paths) for key, paths in heading_owners.items() if len(paths) > 1})
    for record in raw:
        record["duplicate_concepts"] = sorted(
            heading for heading in record["topics"]
            if duplicate_counts.get(str(heading).casefold(), 0) > 1
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    inventory = OUTPUT_DIR / "build-bible-artifact-inventory.jsonl"
    inventory.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in raw), encoding="utf-8")

    owner_counts = Counter(str(item["canonical_owner"]) for item in raw)
    migration = OUTPUT_DIR / "build-bible-canonical-migration-map.md"
    lines = [
        "# Build Bible Canonical Domain Embedding Migration Map\n",
        "Status: Phase 0 inventory complete; Phase 1 mapping baseline\n",
        "## Decision\n",
        "The Build Bible is the construction-domain source tree beneath Wayfinder ontology and CivPhys. "
        "Construction resources are domain abstractions, not CivPhys primitives. No content movement is authorized by this map.\n",
        "## Inventory Summary\n",
        f"- Artifacts inventoried: {len(raw)}",
        f"- Repeated heading candidates: {len(duplicate_counts)}",
        "- Inventory: [build-bible-artifact-inventory.jsonl](build-bible-artifact-inventory.jsonl)",
        "- Extraction backlog: [construction-knowledge-extraction-report.md](construction-knowledge-extraction-report.md)",
        "\n## Canonical Mapping\n",
    ]
    lines.extend(f"- {owner}: {count}" for owner, count in sorted(owner_counts.items()))
    lines += [
        "\n## Compatibility Rules\n",
        "- CivPhys retains its irreducible primitive vocabulary.",
        "- Water, power, data, air, heat, light, and similar terms are construction-domain resources.",
        "- Build Bible contracts and schemas remain in place until a separate review proves they are ecosystem-shared and approves Commons publication.",
        "- Existing doctrine remains authoritative; Eisengarten is a pending external dependency and is not invented here.",
        "- Reality claims require evidence and owner-qualified ARK persistence.",
        "- Generated indexes and artifacts are non-canonical and reproducible from source.",
        "\n## Migration Sequence\n",
        "1. Review medium-confidence records and repeated-heading candidates.",
        "2. Establish a construction-resource classification that derives from Wayfinder Resource and CivPhys mechanics.",
        "3. Deepen missing composed patterns using existing contracts and standards.",
        "4. Extract assemblies only where repeated implementation evidence exists.",
        "5. Convert room patterns to lightweight mission/capability/resource/pattern/assembly/system compositions.",
        "6. Validate one end-to-end property slice before broader migration.",
        "\n## Gate\n",
        "Content extraction or relocation requires review of the inventory record, confirmed canonical ownership, provenance-preserving references, and rollback guidance.",
    ]
    migration.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_extraction_report(raw, heading_owners)


if __name__ == "__main__":
    main()
