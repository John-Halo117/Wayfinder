"""Inventory and map an external construction corpus without importing it."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

CORPUS = Path.home() / "Downloads"
ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "governance" / "reports"
MAX_FILES = 100
MAX_FILE_BYTES = 1_000_000
MAX_EVIDENCE_UNITS = 5_000
FILES = (
    "Network Security Setup_240812_022610.txt", "Circular Waste System_240812_022610.txt",
    "Water System Design_240825_192710.txt", "Homemade Items List_240812_022701.txt",
    "House Structure List_240812_022638.txt", "Farm Produce_240728_230850.txt",
    "Kitchen Equipment List_240828_142024.txt", "Notes_240816_012415.txt",
    "Cleaning System_251126_202608.txt", "Notes_240816_012409.txt",
    "Car_200809_011132_220903_022606.txt", "Wood Stove System_240812_022638.txt",
    "Home Management Systems_240812_032913.txt", "Bathroom system_250709_135812.txt",
    "Notes_240816_012300.txt", "Notes_250308_170529.txt",
    "Drinks_200809_011344_220903_022556.txt", "Notes_240816_012317.txt",
    "Rural Property Security_240812_022610.txt", "Rainwater Harvesting System_240823_222622.txt",
    "Grocery Shopping Tips_240812_022701.txt", "New Prefab Home Description_250709_135719.txt",
    "Food Storage System_240812_022737.txt", "Home Lighting System_240817_020419.txt",
    "Root Cellar Setup_240812_022737.txt", "HVAC Setup in Wilder, Tennessee_250514_181746.txt",
    "Electrical System_240817_020947.txt", "Notes_240816_012401.txt",
    "Laundry System_250308_171234.txt", "Energy Efficiency List_240819_195728.txt",
    "Bedroom System_240812_022610.txt", "Health System_240901_155220.txt",
    "Home Network Setup_240812_022721.txt", "Smart Kitchen System_240812_022721.txt",
    "Coffee Brewing Systems_240812_022701.txt", "Pantry System Components_240812_022737.txt",
    "AI Home System_240812_022737.txt", "Dark Sky System_240801_141034.txt",
)
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+-]*", re.I)
PREFIX_RE = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s*")
STOP = {"a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is", "it", "of", "on", "or", "the", "to", "with"}

DESTINATIONS = (
    ("Doctrine", ("stewardship", "generation", "optionality", "simplicity")),
    ("Constitution", ("always", "never", "must", "shall", "inaccessible")),
    ("Standard", ("minimum", "maximum", "standard", "label", "color-cod", "regular", "priority", "zero-threshold", "accessible")),
    ("Capability", ("preparation", "cooking", "cleaning", "repair", "fabrication", "preservation", "monitoring", "security", "privacy", "hygiene")),
    ("Construction Resource", ("water", "power", "electric", "data", "network", "air", "heat", "light", "drain", "storage", "access", "documentation")),
    ("Pattern", ("spine", "zone", "workflow", "layout", "transition", "corridor", "core", "closed-loop", "isolation")),
    ("Assembly", ("wall", "chase", "module", "door", "window", "shelv", "cabinet", "manifold", "porch", "foundation")),
    ("Room", ("kitchen", "bathroom", "bedroom", "laundry", "pantry", "mudroom", "room")),
    ("Structure", ("house", "home", "barn", "greenhouse", "workshop", "cellar", "building", "structure")),
    ("Property", ("property", "road", "garden", "farm", "orchard", "pond", "irrigation", "livestock")),
    ("System", ("system", "hvac", "plumbing", "solar", "security", "network", "rainwater", "waste")),
)
DEPENDENCIES = {
    "Doctrine": "doctrine/README.md", "Constitution": "indexes/constitutional-index.md",
    "Standard": "indexes/standards-index.md", "Capability": "registries/capability-catalog.md",
    "Construction Resource": "registries/ontologies/resource-flow-ontology.md",
    "Pattern": "indexes/patterns-index.md", "Assembly": "registries/composition/pattern-composition-model.md",
    "System": "domains/utilities/README.md", "Room": "domains/spaces/universal-room-pattern.md",
    "Structure": "domains/buildings/patterns/README.md", "Property": "domains/site/property-pattern.md",
    "Appendix": "INDEX.md",
}


def decode(data: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            pass
    raise ValueError("unsupported text encoding")


def tokens(value: str) -> set[str]:
    return {token.casefold() for token in TOKEN_RE.findall(value) if token.casefold() not in STOP and len(token) > 2}


def evidence_units(text: str) -> list[str]:
    return [PREFIX_RE.sub("", line).strip() for line in text.splitlines() if PREFIX_RE.sub("", line).strip()]


def destination_for(artifact: str, value: str, unit: int) -> tuple[str, str, str]:
    """Classify one evidence unit without substring or filename leakage."""
    words = tokens(value)
    lowered = value.casefold().strip().rstrip(":")
    artifact_words = tokens(Path(artifact).stem)
    is_heading = unit == 1 and len(words) <= 6

    room_words = {"bathroom", "bedroom", "kitchen", "laundry", "pantry", "mudroom"}
    structure_words = {"house", "greenhouse", "workshop", "barn", "cellar", "building", "structure"}
    system_words = {"system", "hvac", "plumbing", "electrical", "network", "rainwater", "security", "waste"}
    resource_words = {"water", "power", "electricity", "data", "air", "heat", "lighting", "light", "drainage", "storage", "access"}
    assembly_words = {"manifold", "wall", "chase", "module", "window", "door", "porch", "foundation", "shelving", "cabinet"}
    property_words = {"property", "garden", "orchard", "trail", "pond", "irrigation", "pasture"}
    capability_words = {"preparation", "cooking", "cleaning", "repair", "fabrication", "preservation", "monitoring", "hygiene", "privacy"}
    product_artifacts = {"car", "drinks", "farm", "grocery", "homemade", "equipment"}

    if is_heading and words & room_words:
        return "Room", "high", "Artifact heading names a spatial room composition."
    if is_heading and words & structure_words:
        return "Structure", "high", "Artifact heading names a physical structure composition."
    if is_heading and words & system_words:
        return "System", "high", "Artifact heading names a construction-domain system."
    if artifact_words & product_artifacts and not (words & (assembly_words | property_words)):
        return "Appendix", "high", "Product, produce, or preference evidence is retained without promotion."
    if words & {"always", "never", "must", "shall"}:
        return "Constitution", "medium", "Normative language is a candidate enforceable construction rule."
    if words & {"minimum", "standard", "labeling", "color-coding", "accessible"}:
        return "Standard", "medium", "Implementation guidance is a candidate construction standard."
    if words & property_words:
        return "Property", "high", "Evidence explicitly concerns a property-scale element."
    if words & assembly_words:
        return "Assembly", "medium", "Evidence names a reusable physical construction component."
    if words & room_words:
        return "Room", "medium", "Evidence explicitly references a spatial room composition."
    if words & structure_words and not words & {"assistant", "automation", "smart"}:
        return "Structure", "medium", "Evidence explicitly references a physical structure."
    if words & system_words:
        return "System", "medium", "Evidence explicitly references a construction-domain system."
    if words & resource_words:
        return "Construction Resource", "medium", "Evidence consumes or constrains a construction-domain resource."
    if words & capability_words:
        return "Capability", "medium", "Evidence describes a reusable outcome rather than a room or product."
    if words & {"workflow", "transition", "closed-loop", "isolation", "zoning"}:
        return "Pattern", "medium", "Evidence describes recurring design intent."
    return "Appendix", "low", "No canonical promotion is justified by the available evidence."


def main() -> None:
    if len(FILES) > MAX_FILES:
        raise RuntimeError("file cap exceeded")
    records: list[dict[str, object]] = []
    evidence: list[dict[str, object]] = []
    for name in sorted(FILES):
        path = CORPUS / name
        data = path.read_bytes()
        if len(data) > MAX_FILE_BYTES:
            raise RuntimeError(f"file cap exceeded: {name}")
        text, encoding = decode(data)
        units = evidence_units(text)
        topic_counts = Counter(token for unit in units for token in sorted(tokens(unit)))
        artifact_destination = destination_for(name, units[0] if units else "", 1)
        record = {
            "artifact": name, "provenance": {"original_path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "encoding": encoding},
            "purpose": units[0] if units else "Empty source artifact", "topics": [word for word, _ in topic_counts.most_common(12)],
            "relationships": [], "duplicate_candidates": [], "canonical_owner_candidate": artifact_destination[0],
            "confidence": artifact_destination[1], "evidence_unit_count": len(units),
        }
        records.append(record)
        for index, unit in enumerate(units, 1):
            destination, confidence, rationale = destination_for(name, unit, index)
            evidence.append({"source_artifact": name, "source_unit": index, "evidence": unit, "destination": destination,
                             "rationale": rationale, "confidence": confidence,
                             "dependencies": [DEPENDENCIES[destination]], "duplicate_references": [], "expected_duplication_reduction": 0})
    if len(evidence) > MAX_EVIDENCE_UNITS:
        raise RuntimeError("evidence cap exceeded")

    token_sets = [tokens(str(item["evidence"])) for item in evidence]
    duplicates: dict[int, list[int]] = defaultdict(list)
    for left in range(len(evidence)):
        for right in range(left + 1, len(evidence)):
            union = token_sets[left] | token_sets[right]
            similarity = len(token_sets[left] & token_sets[right]) / len(union) if union else 0
            if similarity >= 0.60:
                duplicates[left].append(right)
                duplicates[right].append(left)
    for index, related in duplicates.items():
        refs = [f"{evidence[i]['source_artifact']}#unit-{evidence[i]['source_unit']}" for i in related]
        evidence[index]["duplicate_references"] = refs
        evidence[index]["expected_duplication_reduction"] = len(refs)
    visited: set[int] = set()
    for start in range(len(evidence)):
        if start in visited:
            continue
        stack = [start]
        component: list[int] = []
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            component.append(current)
            stack.extend(duplicates.get(current, []))
        references = sorted(
            f"{evidence[index]['source_artifact']}#unit-{evidence[index]['source_unit']}"
            for index in component
        )
        representative = references[0]
        cluster_id = "sha256:" + hashlib.sha256("\n".join(references).encode("utf-8")).hexdigest()
        for index in component:
            reference = f"{evidence[index]['source_artifact']}#unit-{evidence[index]['source_unit']}"
            evidence[index]["duplicate_cluster_id"] = cluster_id
            evidence[index]["canonical_evidence_candidate"] = representative
            evidence[index]["disposition"] = "candidate" if reference == representative else "duplicate_reference"
    by_artifact = {str(item["artifact"]): item for item in records}
    for index, related in duplicates.items():
        source = str(evidence[index]["source_artifact"])
        refs = {str(evidence[i]["source_artifact"]) for i in related if evidence[i]["source_artifact"] != source}
        by_artifact[source]["duplicate_candidates"] = sorted(set(by_artifact[source]["duplicate_candidates"]) | refs)
    for record in records:
        topics_set = set(record["topics"])
        record["relationships"] = sorted(other["artifact"] for other in records if other is not record and len(topics_set & set(other["topics"])) >= 2)

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "source-corpus-provenance-inventory.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in records), encoding="utf-8")
    (REPORTS / "source-corpus-concept-backlog.jsonl").write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in evidence), encoding="utf-8")

    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in evidence:
        groups[str(item["destination"])].append(item)
    lines = ["# Source Corpus Canonical Import Review Plan", "", "Status: approval required; no import performed", "",
             f"Corpus: {len(records)} artifacts, {len(evidence)} evidence units. Inputs remain at their original paths.", "",
             "## Approval Boundary", "", "Approval should name one or more owner batches. Approval does not extend to other batches.", ""]
    for owner in [row[0] for row in DESTINATIONS] + ["Appendix"]:
        items = groups.get(owner, [])
        if not items:
            continue
        sources = sorted({str(item["source_artifact"]) for item in items})
        duplicate_units = sum(bool(item["duplicate_references"]) for item in items)
        lines += [f"## {owner}", "", f"- Evidence units: {len(items)}", f"- Source artifacts: {', '.join(f'`{source}`' for source in sources)}",
                  f"- Units with duplicate candidates: {duplicate_units}", f"- Canonical dependency: `{DEPENDENCIES[owner]}`",
                  "- Proposed action after approval: review evidence semantically, merge only equivalent claims, preserve source hash and unit backlink, and add canonical references.",
                  "- Rollback: revert the batch commit; source corpus and pre-import reports remain unchanged.", ""]
    lines += ["## Batch Validation", "", "After each approved batch:", "", "1. Validate every new or changed relative link.",
              "2. Validate graph relationship direction and absence of orphan nodes.", "3. Confirm the canonical owner against governance and CivPhys boundaries.",
              "4. Compare duplicate candidates before and after the batch.", "5. Regenerate inventory and verify provenance hashes and deterministic output.", ""]
    (REPORTS / "source-corpus-canonical-import-plan.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
