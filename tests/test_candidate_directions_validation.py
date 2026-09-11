"""Mechanical tests for strategic candidate-directions authority markers."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-candidate-directions.py"
SPEC = importlib.util.spec_from_file_location("validate_candidate_directions", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_repository_candidate_directions_contract_is_valid():
    assert MODULE.validate_candidate_directions(ROOT) == []


def test_candidate_directions_rejects_missing_non_authority_marker(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    source = (ROOT / "docs" / "strategic-candidate-directions.md").read_text(encoding="utf-8")
    source = source.replace(
        "**Status:** exploratory / non-authoritative idea reservoir",
        "**Status:** current roadmap",
        1,
    )
    (docs / "strategic-candidate-directions.md").write_text(source, encoding="utf-8")

    diagnostics = MODULE.validate_candidate_directions(tmp_path)
    assert diagnostics
    assert diagnostics[0]["code"] == "CANDIDATE_DIRECTIONS_AUTHORITY_MARKER_MISSING"


def test_candidate_directions_validator_does_not_establish_priority(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    source = (ROOT / "docs" / "strategic-candidate-directions.md").read_text(encoding="utf-8")
    (docs / "strategic-candidate-directions.md").write_text(source, encoding="utf-8")
    assert MODULE.validate_candidate_directions(tmp_path) == []
    assert not hasattr(MODULE, "rank_candidates")
    assert not hasattr(MODULE, "select_candidate")
