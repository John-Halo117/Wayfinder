"""Import the approved source corpus as immutable, non-canonical raw evidence."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from source_corpus_migration import FILES

SOURCE = Path.home() / "Downloads"
BUILD_BIBLE = Path(__file__).resolve().parents[2]
IMPORT_ROOT = BUILD_BIBLE / "governance" / "imports" / "source-corpus"
RAW = IMPORT_ROOT / "raw"
MANIFEST = IMPORT_ROOT / "manifest.jsonl"
MAX_FILES = 100
MAX_FILE_BYTES = 1_000_000


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if len(FILES) > MAX_FILES:
        raise RuntimeError(f"file cap exceeded: {len(FILES)} > {MAX_FILES}")
    RAW.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    expected = set(FILES)
    for stale in sorted(path for path in RAW.iterdir() if path.is_file() and path.name not in expected):
        raise RuntimeError(f"unexpected raw artifact requires review: {stale.name}")
    for name in sorted(FILES):
        source = SOURCE / name
        target = RAW / name
        size = source.stat().st_size
        if size > MAX_FILE_BYTES:
            raise RuntimeError(f"file cap exceeded for {name}: {size}")
        source_hash = digest(source)
        if target.exists() and digest(target) != source_hash:
            raise RuntimeError(f"existing raw import differs: {name}")
        shutil.copyfile(source, target)
        target_hash = digest(target)
        if target_hash != source_hash:
            raise RuntimeError(f"copy verification failed: {name}")
        records.append({
            "artifact": name,
            "status": "raw_noncanonical",
            "original_path": str(source),
            "imported_path": target.relative_to(BUILD_BIBLE).as_posix(),
            "bytes": size,
            "sha256": source_hash,
            "source_preserved": True,
        })
    MANIFEST.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
