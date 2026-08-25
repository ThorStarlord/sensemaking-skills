"""Freeze a candidates/ directory into a manifest + sha256, per the
Autonomous Task v2 commit-then-salt chronology. Must be run exactly once
per tranche, after all candidates in that tranche are authored and
individually qualified ADMISSIBLE.
"""
import json
import sys
from pathlib import Path

import yaml

from hash_utils import sha256_manifest

REQUIRED_BASE = {"candidate_id", "family", "complexity_level"}
REQUIRED_T1_T2_HASHES = {
    "task_text_sha256",
    "oracle_spec_sha256",
    "complexity_breakdown_sha256",
    "initial_state_or_fixture_spec_sha256",
}
REQUIRED_T3_HASHES = {"spec_sha256"}


def load_candidate_record(path: Path) -> dict:
    record = yaml.safe_load(path.read_text(encoding="utf-8"))
    qualification = str(record.get("qualification", ""))
    assert qualification.strip().startswith("ADMISSIBLE"), (
        f"{path}: not ADMISSIBLE, cannot enter a frozen manifest "
        f"(qualification={qualification!r})"
    )
    family = record.get("family")
    hash_fields = REQUIRED_T1_T2_HASHES if family in ("T1", "T2") else REQUIRED_T3_HASHES
    required = REQUIRED_BASE | hash_fields
    missing = required - record.keys()
    assert not missing, f"{path}: missing required fields {missing}"
    return {k: record[k] for k in required}


def main(candidates_dir: str, out_path: str) -> None:
    paths = sorted(Path(candidates_dir).glob("*.md"))
    records = [load_candidate_record(p) for p in paths]
    assert len(records) == 18, (
        f"expected 18 admissible candidates in {candidates_dir}, found {len(records)}"
    )
    ids = [r["candidate_id"] for r in records]
    assert len(ids) == len(set(ids)), f"duplicate candidate_id in manifest: {ids}"

    by_cell: dict[tuple, int] = {}
    for r in records:
        cell = (r["family"], r["complexity_level"])
        by_cell[cell] = by_cell.get(cell, 0) + 1
    expected_cells = {
        ("T1", "MEDIUM"), ("T1", "HIGH"),
        ("T2", "MEDIUM"), ("T2", "HIGH"),
        ("T3", "MEDIUM"), ("T3", "HIGH"),
    }
    assert set(by_cell.keys()) == expected_cells, (
        f"cell mismatch: found {set(by_cell.keys())}, expected {expected_cells}"
    )
    for cell, count in by_cell.items():
        assert count == 3, f"cell {cell} has {count} candidates, expected exactly 3"

    manifest_hash = sha256_manifest(records)
    Path(out_path).write_text(
        json.dumps(
            {"manifest_hash": manifest_hash, "records": records},
            indent=2, sort_keys=True,
        ),
        encoding="utf-8",
    )
    print(manifest_hash)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
