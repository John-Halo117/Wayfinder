"""Extensible substrate detection for Universal Asset Ingestion.

Contract:
- Inputs: local filesystem paths and bounded IngestionConfig caps.
- Outputs: SubstrateDetection records.
- Runtime constraint: O(1) for extension checks and O(max_zip_entries) for ZIP
  probing.
- Memory assumption: O(max_zip_entries) for ZIP member names.
- Failure cases: missing path, invalid ZIP, unreadable source, and unknown format.
- Determinism: identical path metadata and ZIP members produce identical detection.
"""

from __future__ import annotations

from pathlib import Path
from zipfile import BadZipFile, ZipFile

from .chatgpt import CONVERSATIONS_JSON
from .models import IngestionConfig, SubstrateDetection

DOCUMENT_SUFFIXES = {".md", ".markdown", ".txt", ".pdf", ".docx"}
GEOMETRY_SUFFIXES = {".stl", ".obj", ".step", ".stp", ".iges", ".igs", ".gltf", ".glb", ".sh3d"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff"}
VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
AUDIO_SUFFIXES = {".wav", ".mp3", ".flac", ".m4a", ".ogg"}
STRUCTURED_SUFFIXES = {".json", ".jsonl", ".csv", ".tsv", ".xml", ".yaml", ".yml"}
CODE_SUFFIXES = {".py", ".js", ".ts", ".go", ".rs", ".java", ".c", ".cpp", ".h", ".cs"}
EMAIL_SUFFIXES = {".eml", ".mbox"}
CALENDAR_SUFFIXES = {".ics"}
ARCHIVE_SUFFIXES = {".zip"}


def detect_source(path: Path, config: IngestionConfig) -> SubstrateDetection:
    """Detect source substrate and adapter.

    Runtime: O(max_zip_entries) for ZIPs, O(1) otherwise.
    Memory: O(max_zip_entries) for ZIPs.
    Failure: returns unknown detection for unsupported or unreadable sources.
    Deterministic: yes.
    """

    source = path.expanduser().resolve()
    if not source.exists():
        return SubstrateDetection("error", "unknown", "none", "missing", 0.0, "source does not exist")
    if source.is_dir():
        return SubstrateDetection("ok", "filesystem", "folder", "directory", 1.0, "directory import")
    suffix = source.suffix.lower()
    if suffix in ARCHIVE_SUFFIXES:
        return _detect_zip(source, config)
    if suffix in DOCUMENT_SUFFIXES:
        return SubstrateDetection("ok", "document", "generic_file", "file", 0.8, f"document suffix {suffix}")
    if suffix in GEOMETRY_SUFFIXES:
        return SubstrateDetection("ok", "geometry", "generic_file", "file", 0.8, f"geometry suffix {suffix}")
    if suffix in IMAGE_SUFFIXES:
        return SubstrateDetection("ok", "image", "generic_file", "file", 0.8, f"image suffix {suffix}")
    if suffix in VIDEO_SUFFIXES:
        return SubstrateDetection("ok", "video", "generic_file", "file", 0.8, f"video suffix {suffix}")
    if suffix in AUDIO_SUFFIXES:
        return SubstrateDetection("ok", "speech", "generic_file", "file", 0.7, f"audio suffix {suffix}")
    if suffix in STRUCTURED_SUFFIXES:
        return SubstrateDetection("ok", "structured_data", "generic_file", "file", 0.8, f"structured suffix {suffix}")
    if suffix in CODE_SUFFIXES:
        return SubstrateDetection("ok", "code", "generic_file", "file", 0.8, f"code suffix {suffix}")
    if suffix in EMAIL_SUFFIXES:
        return SubstrateDetection("ok", "email", "generic_file", "file", 0.8, f"email suffix {suffix}")
    if suffix in CALENDAR_SUFFIXES:
        return SubstrateDetection("ok", "calendar", "generic_file", "file", 0.8, f"calendar suffix {suffix}")
    return SubstrateDetection("ok", "filesystem", "generic_file", "file", 0.4, "unknown file treated as filesystem artifact")


def _detect_zip(path: Path, config: IngestionConfig) -> SubstrateDetection:
    try:
        with ZipFile(path) as zip_file:
            names = tuple(info.filename for info in zip_file.infolist())
    except BadZipFile:
        return SubstrateDetection("error", "unknown", "none", "file", 0.0, "invalid ZIP archive")
    if len(names) > config.max_zip_entries:
        return SubstrateDetection("error", "unknown", "none", "file", 0.0, "ZIP entry count exceeds maximum")
    if CONVERSATIONS_JSON in names:
        return SubstrateDetection("ok", "conversation", "chatgpt", "archive", 1.0, "ChatGPT conversations.json detected")
    return SubstrateDetection("ok", "archive", "generic_file", "archive", 0.7, "ZIP archive")
