"""Bounded multi-conversation ingestion for non-canonical Build Bible review."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


BUILD_BIBLE = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = BUILD_BIBLE / "governance" / "reports" / "conversation-ingestion-v2"
RAW_ROOT = BUILD_BIBLE / "governance" / "imports" / "source-corpus" / "raw"
SOURCE_MANIFEST = BUILD_BIBLE / "governance" / "imports" / "source-corpus" / "manifest.jsonl"
SCHEMA_VERSION = "2.0"
MAX_SOURCES = 500
MAX_SOURCE_BYTES = 64 * 1024 * 1024
MAX_CONVERSATION_BYTES = 16 * 1024 * 1024
MAX_MESSAGES = 2_000
MAX_OBSERVATIONS = 50_000
MAX_RELATIONSHIPS = 250_000

BUILD_TERMS = frozenset({
    "architecture", "barn", "bathroom", "build bible", "building", "cabinet", "construction",
    "door", "drain", "electrical", "energy", "farm", "food forest", "foundation", "garage",
    "garden", "greenhouse", "home", "homestead", "house", "hvac", "insulation", "kitchen",
    "land", "landscape", "lighting", "maintenance", "material", "pantry", "plumbing", "pond",
    "pool", "property", "roof", "room", "sauna", "site", "storage", "structure", "utility",
    "wall", "waste", "water", "window", "workshop",
})
CAPABILITY_TERMS = {
    "observation": "environmental-monitoring", "monitor": "environmental-monitoring",
    "daylight": "lighting", "light": "lighting", "security": "security-monitoring",
    "access": "physical-access", "repair": "service-access", "service": "service-access",
    "replace": "replacement-access", "storage": "material-storage", "store": "material-storage",
    "water": "water-supply", "drain": "drainage", "heat": "thermal-conditioning",
    "cool": "thermal-conditioning", "ventilat": "ventilation", "air": "air-filtration",
    "network": "data-connectivity", "data": "data-connectivity", "power": "power-supply",
    "energy": "power-supply", "food": "food-production", "grow": "food-production",
    "future": "future-expansion", "expand": "future-expansion", "autom": "automation-control",
}
DOMAIN_TERMS = {
    "buildings": ("house", "building", "room", "wall", "door", "window", "roof", "foundation"),
    "utilities": ("water", "drain", "electrical", "power", "hvac", "network", "utility"),
    "landscape": ("land", "garden", "orchard", "forest", "pond", "meadow", "wildflower"),
    "operations": ("clean", "maintain", "repair", "inspect", "workflow", "batch"),
    "materials": ("wood", "stone", "brass", "iron", "copper", "glass", "linen", "wool"),
    "human-habitat": ("movement", "circadian", "sleep", "barefoot", "floor-first", "wellness"),
    "resilience": ("backup", "failure", "contain", "security", "privacy", "reserve", "redundan"),
}
CLAIM_TYPES = (
    ("correction", ("correction", "instead", "not ", "rather", "refine")),
    ("requirement", ("must", "shall", "should", "need to", "never", "always")),
    ("constraint", ("only if", "unless", "constraint", "avoid", "cannot", "don't")),
    ("failure_mode", ("failure", "fails", "leak", "clog", "damage", "risk")),
    ("tradeoff", ("tradeoff", "upfront", "however", "but ", "cost more", "downside")),
    ("cost_claim", ("cost", "save", "cheaper", "expensive", "$", "lifetime")),
    ("maintenance_obligation", ("maintain", "inspect", "clean", "lubricate", "replace")),
    ("anti_pattern", ("avoid", "don't", "dead space", "monoculture", "inaccessible")),
    ("preference", ("i want", "i'd", "prefer", "favorite", "love")),
    ("example", ("example", "such as", "for instance")),
)
LIST_PREFIX = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+")
SENTENCE = re.compile(r"[^.!?\n]+(?:[.!?]+|$)")
CLAUSE = re.compile(r"[^;]+(?:;|$)")
WORD = re.compile(r"[a-z0-9][a-z0-9+-]*", re.I)


class PipelineError(RuntimeError):
    def __init__(self, code: str, reason: str, context: Mapping[str, Any] | None = None, recoverable: bool = True) -> None:
        super().__init__(f"{code}: {reason}")
        self.code = code
        self.reason = reason
        self.context = dict(context or {})
        self.recoverable = recoverable

    def record(self) -> dict[str, Any]:
        return {"status": "error", "error_code": self.code, "reason": self.reason, "context": self.context, "recoverable": self.recoverable}


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_id(namespace: str, value: str) -> str:
    return f"{namespace}:" + digest(value.encode("utf-8"))[:24]


def normalize(value: str) -> str:
    return " ".join(value.casefold().split())


def words(value: str) -> set[str]:
    return {item.casefold() for item in WORD.findall(value)}


def read_json(path: Path) -> Any:
    if not path.is_file():
        raise PipelineError("SOURCE_NOT_FOUND", "source file does not exist", {"path": str(path)})
    if path.stat().st_size > MAX_SOURCE_BYTES:
        raise PipelineError("SOURCE_TOO_LARGE", "source exceeds byte cap", {"path": str(path), "cap": MAX_SOURCE_BYTES})
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PipelineError("INVALID_JSON", "source is not valid UTF-8 JSON", {"path": str(path)}) from error


def extract_from_session(path: Path, conversation_id: str) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError as error:
                raise PipelineError("INVALID_SESSION", "session contains invalid JSON", {"path": str(path), "line": line_number}) from error
            payload = event.get("payload", {})
            if event.get("type") != "response_item" or payload.get("type") != "message" or payload.get("role") != "user":
                continue
            for part in payload.get("content", []):
                text = part.get("text") if isinstance(part, dict) else None
                if not isinstance(text, str) or conversation_id not in text:
                    continue
                start = text.find('{"conversationId"')
                if start < 0:
                    continue
                candidate, _ = decoder.raw_decode(text[start:])
                if isinstance(candidate, dict) and candidate.get("conversationId") == conversation_id:
                    return candidate
    raise PipelineError("CONVERSATION_NOT_FOUND", "conversation reference was not found in session", {"path": str(path), "conversation_id": conversation_id})


def load_conversation(entry: Mapping[str, Any]) -> dict[str, Any]:
    source_type = entry.get("source_type")
    path = Path(str(entry.get("path", ""))).expanduser().resolve()
    if source_type in {"chatgpt_export", "attached_json"}:
        value = read_json(path)
    elif source_type == "codex_session":
        if path.stat().st_size > MAX_SOURCE_BYTES:
            raise PipelineError("SOURCE_TOO_LARGE", "session exceeds byte cap", {"path": str(path)})
        conversation_id = entry.get("conversation_id")
        if not isinstance(conversation_id, str) or not conversation_id:
            raise PipelineError("INVALID_MANIFEST", "codex_session requires conversation_id", {"path": str(path)})
        value = extract_from_session(path, conversation_id)
    else:
        raise PipelineError("INVALID_SOURCE_TYPE", "unsupported source_type", {"source_type": source_type})
    if not isinstance(value, dict):
        raise PipelineError("INVALID_CONVERSATION", "conversation root must be an object", {"path": str(path)})
    expected_id = entry.get("conversation_id")
    if expected_id and value.get("conversationId") != expected_id:
        raise PipelineError("CONVERSATION_ID_MISMATCH", "conversation ID does not match manifest", {"expected": expected_id, "actual": value.get("conversationId")})
    validate_conversation(value)
    return value


def validate_conversation(value: Mapping[str, Any]) -> None:
    conversation_id = value.get("conversationId")
    messages = value.get("conversation")
    if not isinstance(conversation_id, str) or not conversation_id:
        raise PipelineError("INVALID_CONVERSATION", "conversationId is required")
    if not isinstance(value.get("title", ""), str) or not isinstance(messages, list):
        raise PipelineError("INVALID_CONVERSATION", "title and conversation list are required", {"conversation_id": conversation_id})
    if len(messages) > MAX_MESSAGES:
        raise PipelineError("MESSAGE_LIMIT", "conversation exceeds message cap", {"conversation_id": conversation_id, "cap": MAX_MESSAGES})
    if len(canonical_json(value)) > MAX_CONVERSATION_BYTES:
        raise PipelineError("CONVERSATION_TOO_LARGE", "conversation exceeds content cap", {"conversation_id": conversation_id})


def message_text(message: Mapping[str, Any]) -> str:
    values = []
    for part in message.get("content", []):
        if isinstance(part, Mapping) and isinstance(part.get("text"), str):
            values.append(part["text"])
    return "\n".join(values)


def relevance(value: Mapping[str, Any]) -> tuple[str, list[str], float]:
    title = str(value.get("title", ""))
    messages = value.get("conversation", [])
    sample = title + "\n" + "\n".join(message_text(item) for item in messages[:40] if isinstance(item, Mapping))
    lowered = sample.casefold()
    hits = sorted(term for term in BUILD_TERMS if term in lowered)
    score = min(1.0, len(hits) / 5.0)
    return ("accepted" if len(hits) >= 2 else "excluded", hits, score)


def semantic_spans(text: str) -> Iterable[tuple[int, int, str]]:
    offset = 0
    for raw_line in text.splitlines(keepends=True):
        content = raw_line.rstrip("\r\n")
        stripped = LIST_PREFIX.sub("", content).strip()
        if not stripped or stripped in {"---", "```", "↓"}:
            offset += len(raw_line)
            continue
        content_start = content.find(stripped)
        for sentence_match in SENTENCE.finditer(stripped):
            sentence_value = sentence_match.group(0).strip()
            if not sentence_value:
                continue
            for clause_match in CLAUSE.finditer(sentence_value):
                claim = clause_match.group(0).strip().rstrip(";").strip()
                if not claim:
                    continue
                local = stripped.find(claim, sentence_match.start())
                start = offset + content_start + local
                yield start, start + len(claim), claim
        offset += len(raw_line)


def claim_type(value: str) -> str:
    lowered = value.casefold()
    for kind, terms in CLAIM_TYPES:
        if any(term in lowered for term in terms):
            return kind
    return "concept"


def domains(value: str) -> list[str]:
    lowered = value.casefold()
    return sorted(domain for domain, terms in DOMAIN_TERMS.items() if any(term in lowered for term in terms))


def capability_types(value: str) -> list[str]:
    lowered = value.casefold()
    return sorted({capability for stem, capability in CAPABILITY_TERMS.items() if stem in lowered})


def confidence(value: str, kind: str) -> float:
    base = 0.65
    if kind in {"requirement", "constraint", "correction"}:
        base += 0.15
    if len(words(value)) < 3:
        base -= 0.20
    return round(max(0.1, min(1.0, base)), 2)


def cost_impact(value: str) -> str:
    lowered = value.casefold()
    if any(term in lowered for term in ("major cost", "expensive", "thousands", "lifetime cost", "save money")):
        return "high"
    if any(term in lowered for term in ("cost", "cheap", "save", "labor", "waste")):
        return "medium"
    return "unknown"


def lifecycle_stage(value: str) -> list[str]:
    lowered = value.casefold()
    stages = []
    mapping = {
        "site": ("site", "land", "earthwork"), "design": ("design", "plan"),
        "construction": ("construct", "rough-in", "framing", "install"),
        "operation": ("operate", "daily", "use", "living"),
        "maintenance": ("maintain", "repair", "inspect", "clean"),
        "replacement": ("replace", "upgrade", "remove"),
    }
    for stage, terms in mapping.items():
        if any(term in lowered for term in terms):
            stages.append(stage)
    return stages or ["unspecified"]


def extract_observations(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    conversation = source["conversation"]
    source_revision = source["source_revision"]
    result = []
    for message_index, message in enumerate(conversation["conversation"], start=1):
        if not isinstance(message, Mapping):
            raise PipelineError("INVALID_MESSAGE", "message must be an object", {"conversation_id": conversation["conversationId"], "message": message_index})
        role = message.get("role")
        if role not in {"user", "assistant", "system", "tool"}:
            raise PipelineError("INVALID_ROLE", "message role is invalid", {"conversation_id": conversation["conversationId"], "message": message_index})
        text = message_text(message)
        for ordinal, (start, end, claim) in enumerate(semantic_spans(text), start=1):
            provenance = f"{source_revision}#message-{message_index}:span-{start}-{end}"
            kind = claim_type(claim)
            result.append({
                "schema_version": SCHEMA_VERSION,
                "observation_id": stable_id("bbobs", provenance + "\n" + claim),
                "source_revision": source_revision,
                "conversation_id": conversation["conversationId"],
                "message_id": f"message:{message_index:06d}",
                "speaker": role,
                "timestamp": message.get("timestamp"),
                "span": {"start": start, "end": end, "ordinal": ordinal},
                "original_wording": claim,
                "normalized_wording": " ".join(claim.split()),
                "candidate_type": kind,
                "capability_types": capability_types(claim),
                "domains": domains(claim),
                "confidence": confidence(claim, kind),
                "scope": "physical-world" if domains(claim) else "unresolved",
                "maturity": "raw",
                "cost_impact": cost_impact(claim),
                "lifecycle_stages": lifecycle_stage(claim),
                "status": "review_required",
                "provenance": provenance,
            })
            if len(result) > MAX_OBSERVATIONS:
                raise PipelineError("OBSERVATION_LIMIT", "batch exceeds observation cap", {"cap": MAX_OBSERVATIONS})
    return result


def compile_candidates(observations: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for item in observations:
        grouped[(str(item["candidate_type"]), normalize(str(item["normalized_wording"])))].append(item)
    candidates = []
    observation_to_candidate: dict[str, str] = {}
    for (kind, normalized), support in sorted(grouped.items()):
        candidate_id = stable_id("bbcandidate", kind + "\n" + normalized)
        conversations = sorted({str(item["conversation_id"]) for item in support})
        speakers = Counter(str(item["speaker"]) for item in support)
        domain_values = sorted({domain for item in support for domain in item["domains"]})
        capability_values = sorted({cap for item in support for cap in item["capability_types"]})
        contradictions = sorted(str(item["observation_id"]) for item in support if item["candidate_type"] == "correction")
        candidate = {
            "schema_version": SCHEMA_VERSION,
            "candidate_id": candidate_id,
            "candidate_type": kind,
            "normalized_wording": support[0]["normalized_wording"],
            "supporting_observation_ids": sorted(str(item["observation_id"]) for item in support),
            "capability_types": capability_values,
            "domains": domain_values,
            "score": {
                "confidence": round(sum(float(item["confidence"]) for item in support) / len(support), 3),
                "raw_frequency": len(support),
                "independent_conversation_count": len(conversations),
                "evidence_count": len(support),
                "cross_context_stability": round(min(1.0, len(domain_values) / 3.0), 3),
                "scope_breadth": len(domain_values),
                "maturity": "emerging" if len(conversations) >= 3 else "raw",
                "cost_impact": max((str(item["cost_impact"]) for item in support), key=("unknown", "medium", "high").index),
                "lifecycle_coverage": len({stage for item in support for stage in item["lifecycle_stages"]}),
                "contradiction_count": len(contradictions),
                "speaker_counts": dict(sorted(speakers.items())),
            },
            "contradiction_observation_ids": contradictions,
            "semantic_cluster_status": "exact_normalization_only",
            "canonical_owner_candidate": "BUILD",
            "status": "review_required",
        }
        candidates.append(candidate)
        for item in support:
            observation_to_candidate[str(item["observation_id"])] = candidate_id

    relationships = []
    message_groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    for item in observations:
        message_groups[(str(item["conversation_id"]), str(item["message_id"]))].append(observation_to_candidate[str(item["observation_id"])])
    seen_edges = set()
    for (conversation_id, message_id), candidate_ids in sorted(message_groups.items()):
        ordered = list(dict.fromkeys(candidate_ids))
        for left, right in zip(ordered, ordered[1:]):
            if left == right:
                continue
            key = (left, right, conversation_id, message_id)
            if key in seen_edges:
                continue
            seen_edges.add(key)
            relationships.append({
                "relationship_id": stable_id("bbedge", "\n".join(key)),
                "type": "related_to",
                "source": left,
                "target": right,
                "evidence": {"conversation_id": conversation_id, "message_id": message_id},
                "status": "review_required",
            })
            if len(relationships) > MAX_RELATIONSHIPS:
                raise PipelineError("RELATIONSHIP_LIMIT", "batch exceeds relationship cap", {"cap": MAX_RELATIONSHIPS})

    latent_doctrines = []
    for candidate in candidates:
        score = candidate["score"]
        if score["independent_conversation_count"] >= 3 and score["scope_breadth"] >= 3:
            latent_doctrines.append({
                "doctrine_candidate_id": stable_id("bbdoctrine", str(candidate["candidate_id"])),
                "basis_candidate_id": candidate["candidate_id"],
                "proposed_wording": candidate["normalized_wording"],
                "independent_conversation_count": score["independent_conversation_count"],
                "physical_contexts": candidate["domains"],
                "contradiction_count": score["contradiction_count"],
                "status": "review_required",
                "canonicality": "non_canonical_derived_projection",
            })
    return candidates, relationships, latent_doctrines


def project_layers(candidates: Sequence[Mapping[str, Any]], relationships: Sequence[Mapping[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Create review-only capability-through-standard projections."""
    capability_support: dict[str, list[str]] = defaultdict(list)
    domain_support: dict[str, list[str]] = defaultdict(list)
    concepts, patterns, standards = [], [], []
    for candidate in candidates:
        candidate_id = str(candidate["candidate_id"])
        for capability in candidate["capability_types"]:
            capability_support[str(capability)].append(candidate_id)
        for domain in candidate["domains"]:
            domain_support[str(domain)].append(candidate_id)
        concepts.append({"concept_candidate_id": stable_id("bbconcept", candidate_id), "basis_candidate_id": candidate_id, "label": candidate["normalized_wording"], "capability_types": candidate["capability_types"], "domains": candidate["domains"], "status": "review_required", "canonicality": "non_canonical_derived_projection"})
        if candidate["candidate_type"] in {"requirement", "preference", "example"}:
            patterns.append({"pattern_candidate_id": stable_id("bbpattern", candidate_id), "basis_candidate_id": candidate_id, "statement": candidate["normalized_wording"], "capability_types": candidate["capability_types"], "domains": candidate["domains"], "status": "review_required", "canonicality": "non_canonical_derived_projection"})
        if candidate["candidate_type"] in {"requirement", "constraint", "maintenance_obligation", "anti_pattern"}:
            standards.append({"standard_candidate_id": stable_id("bbstandard", candidate_id), "basis_candidate_id": candidate_id, "statement": candidate["normalized_wording"], "standard_kind": candidate["candidate_type"], "score": candidate["score"], "status": "review_required", "canonicality": "non_canonical_derived_projection"})
    capabilities = [{"capability_candidate_id": stable_id("bbcapability", name), "capability_type": name, "supporting_candidate_ids": sorted(set(support)), "evidence_count": len(set(support)), "status": "review_required", "canonicality": "non_canonical_derived_projection"} for name, support in sorted(capability_support.items())]
    systems = [{"system_candidate_id": stable_id("bbsystem", domain), "domain": domain, "supporting_candidate_ids": sorted(set(support)), "relationship_count": sum(1 for edge in relationships if edge["source"] in support or edge["target"] in support), "status": "review_required", "canonicality": "non_canonical_derived_projection"} for domain, support in sorted(domain_support.items())]
    return {"capabilities": capabilities, "concepts": concepts, "patterns": patterns, "systems": systems, "standards": standards}


def write_jsonl(path: Path, values: Iterable[Mapping[str, Any]]) -> None:
    data = "".join(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n" for value in values)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(data, encoding="utf-8")
    temporary.replace(path)


def preserve_source(conversation: Mapping[str, Any], source_uri: str) -> tuple[str, Path, dict[str, Any]]:
    data = json.dumps(conversation, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    content_hash = digest(data)
    conversation_id = str(conversation["conversationId"])
    source_revision = f"chatgpt:{conversation_id}:sha256:{content_hash}"
    target = RAW_ROOT / f"ChatGPT_{conversation_id}_{content_hash[:12]}.json"
    if target.exists() and target.read_bytes() != data:
        raise PipelineError("IMMUTABLE_SOURCE_CONFLICT", "preserved source differs", {"path": str(target)}, False)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_bytes(data)
    try:
        imported_path = target.relative_to(BUILD_BIBLE).as_posix()
    except ValueError:
        imported_path = str(target)
    record = {
        "artifact": target.name, "status": "raw_noncanonical", "original_path": source_uri,
        "imported_path": imported_path, "bytes": len(data),
        "sha256": content_hash, "source_preserved": True, "source_revision": source_revision,
    }
    return source_revision, target, record


def update_source_manifest(records: Sequence[Mapping[str, Any]]) -> None:
    existing = []
    if SOURCE_MANIFEST.exists():
        existing = [json.loads(line) for line in SOURCE_MANIFEST.read_text(encoding="utf-8").splitlines() if line]
    merged = {str(item["artifact"]): dict(item) for item in existing}
    for item in records:
        key = str(item["artifact"])
        if key in merged and merged[key] != item:
            raise PipelineError("MANIFEST_CONFLICT", "source manifest entry conflicts", {"artifact": key}, False)
        merged[key] = dict(item)
    write_jsonl(SOURCE_MANIFEST, (merged[key] for key in sorted(merged)))


def run_pipeline(manifest_path: Path, output: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    manifest = read_json(manifest_path)
    entries = manifest.get("sources") if isinstance(manifest, Mapping) else None
    if not isinstance(entries, list) or len(entries) > MAX_SOURCES:
        raise PipelineError("INVALID_MANIFEST", "sources must be a bounded list", {"cap": MAX_SOURCES})
    output.mkdir(parents=True, exist_ok=True)
    source_records = []
    accepted_sources = []
    preserved_records = []
    failures = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, Mapping):
            failures.append(PipelineError("INVALID_MANIFEST", "source entry must be an object", {"index": index}).record())
            continue
        try:
            conversation = load_conversation(entry)
            disposition, hits, relevance_score = relevance(conversation)
            source_record = {
                "source_index": index, "conversation_id": conversation["conversationId"],
                "title": conversation.get("title", ""), "source_type": entry.get("source_type"),
                "path": str(entry.get("path", "")), "relevance": disposition,
                "relevance_score": relevance_score, "relevance_terms": hits,
            }
            source_records.append(source_record)
            if disposition == "excluded":
                continue
            source_uri = str(entry.get("source_uri") or entry.get("path"))
            source_revision, raw_path, preserved = preserve_source(conversation, source_uri)
            preserved_records.append(preserved)
            accepted_sources.append({"conversation": conversation, "source_revision": source_revision, "raw_path": str(raw_path)})
        except PipelineError as error:
            failures.append(error.record())
    update_source_manifest(preserved_records)
    observations = [item for source in accepted_sources for item in extract_observations(source)]
    candidates, relationships, doctrines = compile_candidates(observations)
    layers = project_layers(candidates, relationships)
    review_items = []
    for candidate in candidates:
        review_items.append({
            "review_id": stable_id("bbreview", str(candidate["candidate_id"])),
            "candidate_id": candidate["candidate_id"], "candidate_type": candidate["candidate_type"],
            "proposed_statement": candidate["normalized_wording"], "capability_types": candidate["capability_types"],
            "domains": candidate["domains"], "score": candidate["score"],
            "contradiction_observation_ids": candidate["contradiction_observation_ids"],
            "proposed_actions": ["reject", "defer", "merge", "supersede", "draft_canonical_change"],
            "status": "awaiting_human_review", "canonicality": "non_canonical_derived_projection",
        })
    write_jsonl(output / "sources.jsonl", source_records)
    write_jsonl(output / "observations.jsonl", observations)
    write_jsonl(output / "candidates.jsonl", candidates)
    for layer_name, values in layers.items():
        write_jsonl(output / f"{layer_name}.jsonl", values)
    write_jsonl(output / "relationships.jsonl", relationships)
    write_jsonl(output / "latent-doctrines.jsonl", doctrines)
    write_jsonl(output / "review-queue.jsonl", review_items)
    write_jsonl(output / "failures.jsonl", failures)
    summary = {
        "schema_version": SCHEMA_VERSION, "status": "review_required" if not failures else "completed_with_failures",
        "source_count": len(entries), "accepted_source_count": len(accepted_sources),
        "excluded_source_count": sum(1 for item in source_records if item["relevance"] == "excluded"),
        "failure_count": len(failures), "observation_count": len(observations),
        "candidate_count": len(candidates), "relationship_count": len(relationships),
        "latent_doctrine_count": len(doctrines), "review_item_count": len(review_items),
        "layer_counts": {name: len(values) for name, values in sorted(layers.items())},
        "speaker_weighting": "equal", "canonicality": "non_canonical_derived_projection",
    }
    (output / "batch-summary.json").write_bytes(canonical_json(summary))
    return summary


def discover(paths: Sequence[Path], destination: Path) -> dict[str, Any]:
    sources = []
    for path in sorted({item.expanduser().resolve() for item in paths}, key=str):
        if path.is_dir():
            candidates = sorted(path.glob("*.json")) + sorted(path.glob("*.jsonl"))
        else:
            candidates = [path]
        for candidate in candidates:
            if len(sources) >= MAX_SOURCES:
                raise PipelineError("SOURCE_LIMIT", "discovery exceeds source cap", {"cap": MAX_SOURCES})
            if candidate.suffix == ".jsonl":
                continue  # Requires an explicit conversation_id in a hand-authored manifest.
            sources.append({"source_type": "chatgpt_export", "path": str(candidate)})
    value = {"schema_version": SCHEMA_VERSION, "sources": sources}
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(canonical_json(value))
    return {"source_count": len(sources), "manifest": str(destination)}


def validate_output(output: Path) -> dict[str, Any]:
    required = ("sources.jsonl", "observations.jsonl", "candidates.jsonl", "capabilities.jsonl", "concepts.jsonl", "patterns.jsonl", "systems.jsonl", "standards.jsonl", "relationships.jsonl", "latent-doctrines.jsonl", "review-queue.jsonl", "failures.jsonl", "batch-summary.json")
    missing = [name for name in required if not (output / name).is_file()]
    if missing:
        raise PipelineError("MISSING_OUTPUT", "batch output is incomplete", {"missing": missing})
    summary = read_json(output / "batch-summary.json")
    counts = {}
    for name in required[:-1]:
        with (output / name).open(encoding="utf-8") as handle:
            counts[name] = sum(1 for line in handle if line.strip())
    expected = {
        "sources.jsonl": summary["source_count"] - summary["failure_count"],
        "observations.jsonl": summary["observation_count"], "candidates.jsonl": summary["candidate_count"],
        "relationships.jsonl": summary["relationship_count"], "latent-doctrines.jsonl": summary["latent_doctrine_count"],
        "review-queue.jsonl": summary["review_item_count"], "failures.jsonl": summary["failure_count"],
    }
    expected.update({f"{name}.jsonl": count for name, count in summary["layer_counts"].items()})
    mismatches = {name: {"expected": expected[name], "actual": count} for name, count in counts.items() if expected[name] != count}
    if mismatches:
        raise PipelineError("COUNT_MISMATCH", "batch counts do not match summary", mismatches, False)
    return {"status": "passed", "counts": counts, "canonicality": summary["canonicality"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    discover_parser = subparsers.add_parser("discover")
    discover_parser.add_argument("paths", nargs="+", type=Path)
    discover_parser.add_argument("--manifest", type=Path, required=True)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("manifest", type=Path)
    run_parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("output", type=Path, nargs="?", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        if args.command == "discover":
            result = discover(args.paths, args.manifest)
        elif args.command == "run":
            result = run_pipeline(args.manifest, args.output)
        else:
            result = validate_output(args.output)
        print(json.dumps({"status": "ok", "result": result}, sort_keys=True))
    except PipelineError as error:
        print(json.dumps(error.record(), sort_keys=True))
        raise SystemExit(2) from error


if __name__ == "__main__":
    main()
