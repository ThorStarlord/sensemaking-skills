"""Shared mechanical IO primitives for bounded Campaign companion records.

This module owns representation mechanics only: canonical JSON hashing, atomic
JSON replacement, and fsync'd JSONL append. Companion schemas and semantic
meaning remain with their owning modules.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping


def canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    """Return the repository's compact, sorted UTF-8 JSON representation."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def mapping_sha256(value: Mapping[str, Any]) -> str:
    """Hash a mapping using ``canonical_json_bytes``."""
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    """Atomically replace one pretty-printed JSON object and fsync its bytes."""
    path = Path(path)
    temp = path.with_name(f".{path.name}.tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(dict(value), handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


def append_jsonl_fsync(path: Path, value: Mapping[str, Any]) -> None:
    """Append one sorted JSON object plus newline and fsync before returning."""
    with Path(path).open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(dict(value), sort_keys=True, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
