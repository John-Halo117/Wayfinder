"""Import and atomize one referenced ChatGPT conversation as reviewable evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from source_corpus_migration import DEPENDENCIES, destination_for


BUILD_BIBLE = Path(__file__).resolve().parents[2]
IMPORT_ROOT = BUILD_BIBLE / "governance" / "imports" / "source-corpus"
RAW_ROOT = IMPORT_ROOT / "raw"
MANIFEST = IMPORT_ROOT / "manifest.jsonl"
REPORTS = BUILD_BIBLE / "governance" / "reports"
MAX_SESSION_BYTES = 64 * 1024 * 1024
MAX_MESSAGES = 2_000
MAX_OBSERVATIONS = 50_000
MAX_CONTENT_BYTES = 16 * 1024 * 1024
SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
LIST_PREFIX = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_id(namespace: str, value: str) -> str:
    return f"{namespace}:" + sha256(value.encode("utf-8"))[:24]


def extract_conversation(session: Path, conversation_id: str) -> dict[str, Any]:
    if session.stat().st_size > MAX_SESSION_BYTES:
        raise RuntimeError("session file exceeds resource cap")
    decoder = json.JSONDecoder()
    with session.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError as error:
                raise RuntimeError(f"invalid session JSON at line {line_number}") from error
            payload = event.get("payload", {})
            if event.get("type") != "response_item" or payload.get("type") != "message" or payload.get("role") != "user":
                continue
            for part in payload.get("content", []):
                text = part.get("text") if isinstance(part, dict) else None
                if not isinstance(text, str) or conversation_id not in text:
                    continue
                marker = '{"conversationId"'
                start = text.find(marker)
                if start < 0:
                    continue
                value, _ = decoder.raw_decode(text[start:])
                if isinstance(value, dict) and value.get("conversationId") == conversation_id:
                    return value
    raise RuntimeError(f"conversation not found: {conversation_id}")


def textual_parts(message: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for part in message.get("content", []):
        if isinstance(part, dict) and isinstance(part.get("text"), str):
            result.append(part["text"])
    return result


def atomic_units(text: str) -> list[str]:
    units: list[str] = []
    for block in text.splitlines():
        value = LIST_PREFIX.sub("", block).strip()
        if not value or value in {"---", "```", "↓"}:
            continue
        for sentence in SENTENCE_BOUNDARY.split(value):
            normalized = sentence.strip()
            if normalized:
                units.append(normalized)
    return units


def write_if_absent(path: Path, data: bytes) -> None:
    if path.exists():
        if path.read_bytes() != data:
            raise RuntimeError(f"immutable source differs: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def update_manifest(record: dict[str, Any]) -> None:
    records = []
    if MANIFEST.exists():
        records = [json.loads(line) for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line]
    by_artifact = {item["artifact"]: item for item in records}
    prior = by_artifact.get(record["artifact"])
    if prior is not None and prior != record:
        raise RuntimeError("manifest entry conflicts with immutable source")
    by_artifact[record["artifact"]] = record
    MANIFEST.write_text("".join(json.dumps(by_artifact[key], sort_keys=True) + "\n" for key in sorted(by_artifact)), encoding="utf-8")


def compile_evidence(conversation: dict[str, Any], artifact: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    messages = conversation.get("conversation")
    if not isinstance(messages, list) or len(messages) > MAX_MESSAGES:
        raise RuntimeError("conversation message cap exceeded or conversation is invalid")
    observations: list[dict[str, Any]] = []
    normalized_groups: dict[str, list[str]] = defaultdict(list)
    for message_index, message in enumerate(messages, start=1):
        if not isinstance(message, dict):
            raise RuntimeError(f"invalid message at index {message_index}")
        role = message.get("role")
        if role not in {"user", "assistant", "system", "tool"}:
            raise RuntimeError(f"invalid role at message {message_index}")
        unit_index = 0
        for part_index, part in enumerate(textual_parts(message), start=1):
            for unit in atomic_units(part):
                unit_index += 1
                provenance = f"{artifact}#message-{message_index}:part-{part_index}:unit-{unit_index}"
                observation_id = stable_id("bbobs", provenance + "\n" + unit)
                destination, confidence, rationale = destination_for(artifact, unit, unit_index)
                normalized = " ".join(unit.casefold().split())
                normalized_groups[normalized].append(observation_id)
                observations.append({
                    "observation_id": observation_id,
                    "source_artifact": artifact,
                    "conversation_id": conversation["conversationId"],
                    "message_id": f"message:{message_index:06d}",
                    "message_role": role,
                    "source_part": part_index,
                    "source_unit": unit_index,
                    "original_wording": unit,
                    "normalized_wording": " ".join(unit.split()),
                    "destination_candidate": destination,
                    "canonical_owner_candidate": "BUILD",
                    "confidence": confidence,
                    "rationale": rationale,
                    "dependencies": [DEPENDENCIES[destination]],
                    "status": "raw_candidate",
                    "provenance": provenance,
                })
                if len(observations) > MAX_OBSERVATIONS:
                    raise RuntimeError("observation cap exceeded")
    for observation in observations:
        key = observation["original_wording"].casefold()
        duplicates = normalized_groups[" ".join(key.split())]
        observation["equivalent_observation_ids"] = [item for item in duplicates if item != observation["observation_id"]]

    concepts = []
    for normalized, observation_ids in sorted(normalized_groups.items()):
        exemplar = next(item for item in observations if item["observation_id"] == observation_ids[0])
        concepts.append({
            "concept_id": stable_id("bbconcept", normalized),
            "normalized_wording": exemplar["normalized_wording"],
            "supporting_observation_ids": observation_ids,
            "source_count": len(observation_ids),
            "destination_candidate": exemplar["destination_candidate"],
            "canonical_owner_candidate": "BUILD",
            "status": "review_required",
        })
    return observations, concepts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("session", type=Path)
    parser.add_argument("conversation_id")
    args = parser.parse_args()
    conversation = extract_conversation(args.session, args.conversation_id)
    raw = (json.dumps(conversation, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if len(raw) > MAX_CONTENT_BYTES:
        raise RuntimeError("conversation content cap exceeded")
    artifact = f"ChatGPT_{args.conversation_id}.json"
    raw_path = RAW_ROOT / artifact
    write_if_absent(raw_path, raw)
    update_manifest({
        "artifact": artifact,
        "status": "raw_noncanonical",
        "original_path": f"chatgpt-conversation://{args.conversation_id}",
        "imported_path": raw_path.relative_to(BUILD_BIBLE).as_posix(),
        "bytes": len(raw),
        "sha256": sha256(raw),
        "source_preserved": True,
    })
    observations, concepts = compile_evidence(conversation, artifact)
    stem = f"chatgpt-{args.conversation_id}"
    (REPORTS / f"{stem}-observations.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in observations), encoding="utf-8"
    )
    (REPORTS / f"{stem}-concepts.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in concepts), encoding="utf-8"
    )
    repeated = sum(1 for item in concepts if item["source_count"] > 1)
    review = [
        "# ChatGPT Conversation Mining Review", "", "Status: non-canonical; semantic review required", "",
        f"- Conversation: `{args.conversation_id}`", f"- Title: {conversation.get('title', '')}",
        f"- Source artifact: [`{artifact}`](../imports/source-corpus/raw/{artifact})",
        f"- Atomic observations: {len(observations)}", f"- Exact normalized concepts: {len(concepts)}",
        f"- Repeated exact concepts: {repeated}", "",
        "Every observation retains message, content-part, and atomic-unit provenance. Exact duplicates remain as evidence and are linked rather than deleted.", "",
        "## Promotion Boundary", "", "No item in these generated reports is canonical. Review must compare candidates with existing doctrine, patterns, standards, and domain owners before promotion.", "",
    ]
    (REPORTS / f"{stem}-review.md").write_text("\n".join(review), encoding="utf-8")
    print(json.dumps({"artifact": artifact, "observations": len(observations), "concepts": len(concepts), "repeated": repeated}, sort_keys=True))


if __name__ == "__main__":
    main()
