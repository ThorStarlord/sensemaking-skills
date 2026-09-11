from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-strategic-state.py"

REQUIRED_SURFACES = (
    "docs/product-strategy.md",
    "docs/strategic-outer-loop.md",
    "docs/strategic-state-contract.md",
    "docs/product-thesis-revision.md",
)


def _run(repo_root: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(repo_root),
            "--json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed, json.loads(completed.stdout)


def _error_ids(payload: dict) -> set[str]:
    return {error["error_id"] for error in payload["errors"]}


def _minimal_status(*, thesis: str = "NO", frontier: str | None = None) -> str:
    if frontier is None:
        frontier = (
            "1. **Foundation — COMPLETE / INTEGRATED.** Present.\n"
            "2. **Next candidate — CANDIDATE / NOT AUTHORIZED.** Deferred."
        )
    return f"""# Status

## Strategic Repository Evolution state — Level 3

### Current product strategy

- **Level-4 authority:** `docs/product-strategy.md`.
- **Control model:** `docs/strategic-outer-loop.md`.
- **Level-3 contract:** `docs/strategic-state-contract.md`.
- **Level-4 revision contract:** `docs/product-thesis-revision.md`.

### Current capability state

Current mechanically represented capability state.

### Material limitations and evidence ceilings

Repository qualification is not semantic truth.

### Strategic Frontier

{frontier}

### Current highest-leverage boundary

No current boundary is selected.

### Current decision-changing uncertainty

None is selected for this fixture.

### Current warranted repository-level responsibility

None automatically selected.

### Authority / owner direction

No additional authority is implied by this fixture.

### Thesis review state

`THESIS_REVIEW_REQUIRED`: **{thesis}**.

## Current next step

Reassess from current repository state.
"""


def _write_valid_repo(repo_root: Path, *, status: str | None = None) -> None:
    for relative in REQUIRED_SURFACES:
        path = repo_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {path.name}\n", encoding="utf-8")
    (repo_root / "STATUS.md").write_text(
        _minimal_status() if status is None else status,
        encoding="utf-8",
    )


def test_current_repository_strategic_state_is_valid() -> None:
    completed, payload = _run(ROOT)
    assert completed.returncode == 0, (completed.stdout, completed.stderr)
    assert payload["valid"] is True
    assert payload["errors"] == []
    assert payload["semantic_truth_established"] is False


def test_missing_status_fails(tmp_path: Path) -> None:
    for relative in REQUIRED_SURFACES:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# authority\n", encoding="utf-8")

    completed, payload = _run(tmp_path)
    assert completed.returncode == 1
    assert "STRATEGIC_STATE_STATUS_NOT_FOUND" in _error_ids(payload)
    assert payload["semantic_truth_established"] is False


def test_missing_required_authority_surface_fails(tmp_path: Path) -> None:
    _write_valid_repo(tmp_path)
    (tmp_path / "docs/product-strategy.md").unlink()

    completed, payload = _run(tmp_path)
    assert completed.returncode == 1
    ids = _error_ids(payload)
    assert "STRATEGIC_STATE_REQUIRED_SURFACE_MISSING" in ids
    assert "STRATEGIC_STATE_POINTER_BROKEN" in ids


def test_missing_required_section_fails(tmp_path: Path) -> None:
    status = _minimal_status().replace(
        "### Current capability state\n\nCurrent mechanically represented capability state.\n\n",
        "",
    )
    _write_valid_repo(tmp_path, status=status)

    completed, payload = _run(tmp_path)
    assert completed.returncode == 1
    assert "STRATEGIC_STATE_SECTION_MISSING" in _error_ids(payload)


def test_duplicate_required_section_fails(tmp_path: Path) -> None:
    status = _minimal_status().replace(
        "### Current capability state\n",
        "### Current capability state\n\nDuplicate trigger.\n\n### Current capability state\n",
        1,
    )
    _write_valid_repo(tmp_path, status=status)

    completed, payload = _run(tmp_path)
    assert completed.returncode == 1
    assert "STRATEGIC_STATE_SECTION_DUPLICATE" in _error_ids(payload)


def test_missing_canonical_pointer_fails(tmp_path: Path) -> None:
    status = _minimal_status().replace(
        "- **Control model:** `docs/strategic-outer-loop.md`.\n",
        "",
    )
    _write_valid_repo(tmp_path, status=status)

    completed, payload = _run(tmp_path)
    assert completed.returncode == 1
    assert "STRATEGIC_STATE_POINTER_MISSING" in _error_ids(payload)


def test_duplicate_canonical_pointer_fails(tmp_path: Path) -> None:
    pointer = "- **Control model:** `docs/strategic-outer-loop.md`.\n"
    status = _minimal_status().replace(pointer, pointer + pointer)
    _write_valid_repo(tmp_path, status=status)

    completed, payload = _run(tmp_path)
    assert completed.returncode == 1
    assert "STRATEGIC_STATE_POINTER_DUPLICATE" in _error_ids(payload)


def test_mismatched_canonical_pointer_fails_even_when_target_exists(tmp_path: Path) -> None:
    status = _minimal_status().replace(
        "`docs/strategic-outer-loop.md`",
        "`docs/alternate-outer-loop.md`",
    )
    _write_valid_repo(tmp_path, status=status)
    (tmp_path / "docs/alternate-outer-loop.md").write_text("# alternate\n", encoding="utf-8")

    completed, payload = _run(tmp_path)
    assert completed.returncode == 1
    assert "STRATEGIC_STATE_POINTER_MISMATCH" in _error_ids(payload)


def test_missing_thesis_review_marker_fails(tmp_path: Path) -> None:
    status = _minimal_status().replace(
        "`THESIS_REVIEW_REQUIRED`: **NO**.",
        "No thesis review marker is declared.",
    )
    _write_valid_repo(tmp_path, status=status)

    completed, payload = _run(tmp_path)
    assert completed.returncode == 1
    assert "STRATEGIC_STATE_THESIS_REVIEW_MISSING" in _error_ids(payload)


def test_duplicate_thesis_review_marker_fails(tmp_path: Path) -> None:
    status = _minimal_status().replace(
        "`THESIS_REVIEW_REQUIRED`: **NO**.",
        "`THESIS_REVIEW_REQUIRED`: **NO**.\n`THESIS_REVIEW_REQUIRED`: **NO**.",
    )
    _write_valid_repo(tmp_path, status=status)

    completed, payload = _run(tmp_path)
    assert completed.returncode == 1
    assert "STRATEGIC_STATE_THESIS_REVIEW_DUPLICATE" in _error_ids(payload)


def test_invalid_thesis_review_literal_fails(tmp_path: Path) -> None:
    _write_valid_repo(tmp_path, status=_minimal_status(thesis="MAYBE"))

    completed, payload = _run(tmp_path)
    assert completed.returncode == 1
    assert "STRATEGIC_STATE_THESIS_REVIEW_INVALID" in _error_ids(payload)


def test_duplicate_normalized_frontier_identity_fails(tmp_path: Path) -> None:
    frontier = (
        "1. **Strategic State Validator — ACTIVE.** First.\n"
        "2. **strategic   state validator — COMPLETE.** Second."
    )
    _write_valid_repo(tmp_path, status=_minimal_status(frontier=frontier))

    completed, payload = _run(tmp_path)
    assert completed.returncode == 1
    assert "STRATEGIC_STATE_FRONTIER_DUPLICATE_ITEM" in _error_ids(payload)


def test_multiple_distinct_frontier_candidates_are_valid(tmp_path: Path) -> None:
    frontier = (
        "1. **Candidate A — CANDIDATE / NOT AUTHORIZED.** One.\n"
        "2. **Candidate B — DEFERRED BY OWNER DIRECTION.** Two.\n"
        "3. **Candidate C — COMPLETE / INTEGRATED.** Three."
    )
    _write_valid_repo(tmp_path, status=_minimal_status(frontier=frontier))

    completed, payload = _run(tmp_path)
    assert completed.returncode == 0, (completed.stdout, completed.stderr)
    assert payload["valid"] is True


def test_no_active_boundary_is_valid(tmp_path: Path) -> None:
    _write_valid_repo(tmp_path)

    completed, payload = _run(tmp_path)
    assert completed.returncode == 0, (completed.stdout, completed.stderr)
    assert payload["valid"] is True


def test_semantically_questionable_prose_is_not_scored(tmp_path: Path) -> None:
    status = _minimal_status().replace(
        "Current mechanically represented capability state.",
        "This strategy is definitely the best strategy in the universe.",
    )
    _write_valid_repo(tmp_path, status=status)

    completed, payload = _run(tmp_path)
    assert completed.returncode == 0, (completed.stdout, completed.stderr)
    assert payload["valid"] is True
    assert payload["semantic_truth_established"] is False


def test_json_result_declares_mechanical_checks_only(tmp_path: Path) -> None:
    _write_valid_repo(tmp_path)

    completed, payload = _run(tmp_path)
    assert completed.returncode == 0
    assert payload["checks"] == [
        "required_authority_surfaces",
        "required_level3_section_anchors",
        "canonical_authority_pointers",
        "thesis_review_marker_shape",
        "strategic_frontier_identity_uniqueness",
    ]
    assert payload["semantic_truth_established"] is False
