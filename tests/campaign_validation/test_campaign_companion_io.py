"""Mechanical regression tests for shared bounded companion IO."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from sensemaking_skills.campaigns.companion_io import (
    append_jsonl_fsync,
    atomic_write_json,
    canonical_json_bytes,
    mapping_sha256,
)


def test_canonical_json_bytes_are_sorted_compact_and_utf8() -> None:
    assert canonical_json_bytes({"b": 2, "a": 1}) == b'{"a":1,"b":2}'
    assert canonical_json_bytes({"text": "caf\u00e9"}) == '{"text":"caf\u00e9"}'.encode("utf-8")


def test_mapping_sha256_is_insertion_order_independent() -> None:
    first = {"b": 2, "a": 1}
    second = {"a": 1, "b": 2}
    expected = hashlib.sha256(b'{"a":1,"b":2}').hexdigest()
    assert mapping_sha256(first) == expected
    assert mapping_sha256(second) == expected


def test_atomic_write_json_replaces_pretty_sorted_utf8_with_newline(tmp_path: Path) -> None:
    path = tmp_path / "companion.json"
    atomic_write_json(path, {"b": 2, "a": 1})
    assert path.read_bytes() == b'{\n  "a": 1,\n  "b": 2\n}\n'
    assert not (tmp_path / ".companion.json.tmp").exists()

    atomic_write_json(path, {"z": "caf\u00e9"})
    assert json.loads(path.read_text(encoding="utf-8")) == {"z": "caf\u00e9"}
    assert path.read_bytes().endswith(b"\n")


def test_append_jsonl_fsync_appends_one_sorted_object_per_line(tmp_path: Path) -> None:
    path = tmp_path / "history.jsonl"
    append_jsonl_fsync(path, {"b": 2, "a": 1})
    append_jsonl_fsync(path, {"d": 4, "c": 3})
    assert path.read_text(encoding="utf-8").splitlines() == [
        '{"a": 1, "b": 2}',
        '{"c": 3, "d": 4}',
    ]
