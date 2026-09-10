from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-skill-registry-liveness.py"


def _run(repo_root: Path, registry: Path | None = None) -> tuple[subprocess.CompletedProcess[str], dict]:
    command = [
        sys.executable,
        str(SCRIPT),
        "--repo-root",
        str(repo_root),
        "--json",
    ]
    if registry is not None:
        command.extend(["--registry", str(registry)])
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed, json.loads(completed.stdout)


def _write_registry(repo_root: Path, skills: list[dict]) -> Path:
    registry = repo_root / "skill-registry.yaml"
    registry.write_text(
        yaml.safe_dump(
            {
                "ecosystems": {
                    "test": {
                        "name": "Test",
                        "skills": skills,
                    }
                }
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return registry


def _create_skill(repo_root: Path, skill_id: str) -> None:
    skill_dir = repo_root / "skills" / skill_id
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {skill_id}\ndescription: test\n---\n",
        encoding="utf-8",
    )


def _error_ids(payload: dict) -> set[str]:
    return {error["error_id"] for error in payload["errors"]}


def test_current_repository_registry_has_no_liveness_contradiction() -> None:
    completed, payload = _run(ROOT)
    assert completed.returncode == 0, (completed.stdout, completed.stderr)
    assert payload["valid"] is True
    assert payload["errors"] == []
    assert payload["semantic_truth_established"] is False


def test_rejects_no_current_implementation_note_when_skill_tree_exists(tmp_path: Path) -> None:
    _create_skill(tmp_path, "example")
    registry = _write_registry(
        tmp_path,
        [
            {
                "id": "example",
                "status": "deprecated",
                "status_note": "HISTORICAL/DEPRECATED - no current implementation yet; wayfinder-era skill.",
            }
        ],
    )

    completed, payload = _run(tmp_path, registry)
    assert completed.returncode == 1
    assert "SKILL_REGISTRY_STALE_ABSENCE_NOTE" in _error_ids(payload)
    assert payload["semantic_truth_established"] is False


def test_rejects_proposed_status_when_canonical_skill_exists(tmp_path: Path) -> None:
    _create_skill(tmp_path, "example")
    registry = _write_registry(
        tmp_path,
        [
            {
                "id": "example",
                "status": "proposed",
                "status_note": "STILL-PROPOSED - not yet implemented.",
            }
        ],
    )

    completed, payload = _run(tmp_path, registry)
    assert completed.returncode == 1
    assert "SKILL_REGISTRY_STALE_PROPOSED_STATUS" in _error_ids(payload)


def test_rejects_mismatched_current_canonical_path(tmp_path: Path) -> None:
    _create_skill(tmp_path, "example")
    _create_skill(tmp_path, "other")
    registry = _write_registry(
        tmp_path,
        [
            {
                "id": "example",
                "status": "deprecated",
                "status_note": (
                    "HISTORICAL/DEPRECATED - invocation metadata is historical; "
                    "current canonical implementation lives under skills/other/."
                ),
            }
        ],
    )

    completed, payload = _run(tmp_path, registry)
    assert completed.returncode == 1
    assert "SKILL_REGISTRY_MISMATCHED_CURRENT_PATH" in _error_ids(payload)


def test_rejects_broken_current_canonical_path(tmp_path: Path) -> None:
    registry = _write_registry(
        tmp_path,
        [
            {
                "id": "example",
                "status": "deprecated",
                "status_note": (
                    "HISTORICAL/DEPRECATED - invocation metadata is historical; "
                    "current canonical implementation lives under skills/example/."
                ),
            }
        ],
    )

    completed, payload = _run(tmp_path, registry)
    assert completed.returncode == 1
    assert "SKILL_REGISTRY_BROKEN_CURRENT_PATH" in _error_ids(payload)


def test_rejects_duplicate_registry_ids(tmp_path: Path) -> None:
    registry = _write_registry(
        tmp_path,
        [
            {"id": "example", "status": "deprecated"},
            {"id": "example", "status": "deprecated"},
        ],
    )

    completed, payload = _run(tmp_path, registry)
    assert completed.returncode == 1
    assert "SKILL_REGISTRY_DUPLICATE_ID" in _error_ids(payload)


def test_accepts_historical_absent_skill_with_truthful_absence_note(tmp_path: Path) -> None:
    registry = _write_registry(
        tmp_path,
        [
            {
                "id": "historical-only",
                "status": "deprecated",
                "status_note": "HISTORICAL/DEPRECATED - no implementation under skills/; retained for compatibility.",
            }
        ],
    )

    completed, payload = _run(tmp_path, registry)
    assert completed.returncode == 0, (completed.stdout, completed.stderr)
    assert payload["valid"] is True
    assert payload["semantic_truth_established"] is False


def test_accepts_deprecated_historical_invocation_with_current_skill(tmp_path: Path) -> None:
    _create_skill(tmp_path, "example")
    registry = _write_registry(
        tmp_path,
        [
            {
                "id": "example",
                "status": "deprecated",
                "status_note": (
                    "HISTORICAL/DEPRECATED - invocation metadata is historical; "
                    "current canonical implementation lives under skills/example/."
                ),
            }
        ],
    )

    completed, payload = _run(tmp_path, registry)
    assert completed.returncode == 0, (completed.stdout, completed.stderr)
    assert payload["valid"] is True
