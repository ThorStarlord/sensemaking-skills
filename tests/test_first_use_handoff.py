"""First-use handoff mechanics."""

from __future__ import annotations

import json
from pathlib import Path

from sensemaking_skills.first_use import prepare_handoff


def _fake_skill(tmp_path: Path) -> Path:
    skill = tmp_path / "skills" / "using-sensemaking"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: using-sensemaking\ndescription: test copy\n---\n",
        encoding="utf-8",
    )
    return skill


def test_prepare_handoff_writes_verified_paths(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    (target / "README.md").write_text("# Target\n", encoding="utf-8")
    (target / "pyproject.toml").write_text(
        "[project]\nname = 'target'\n", encoding="utf-8"
    )
    skill = _fake_skill(tmp_path)
    output = tmp_path / "out"

    payload = prepare_handoff(
        target, output, question="What is here?", skill_path=skill,
    )

    assert payload["artifact_id"] == "sensemaking_first_use_handoff"
    assert payload["analysis_performed"] is False
    assert payload["semantic_truth_established"] is False
    assert payload["action_authorized"] is False
    assert payload["target"]["path"] == str(target.resolve())
    assert payload["installed_skill"]["skill_dir"] == str(skill.resolve())
    assert payload["installed_skill"]["currency"] == "DIFFERS_FROM_PACKAGE_SOURCE"
    assert payload["target"]["inventory"]["entry_documents"] == ["README.md"]
    assert payload["target"]["inventory"]["manifests"] == ["pyproject.toml"]
    assert (output / "handoff.json").is_file()
    assert (output / "handoff.md").is_file()

    written = json.loads((output / "handoff.json").read_text(encoding="utf-8"))
    assert written["prompt"] == payload["prompt"]
    assert str(target.resolve()) in payload["prompt"]
    assert str(skill.resolve()) in payload["prompt"]
    assert "What is here?" in payload["prompt"]
    assert "does not analyze repository semantics" in payload["limits"][0]


def test_prepare_handoff_refuses_a_non_skill_path(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    output = tmp_path / "out"

    try:
        prepare_handoff(target, output, skill_path=tmp_path / "missing")
    except ValueError as exc:
        assert "using-sensemaking" in str(exc)
    else:  # pragma: no cover - explicit failure path
        raise AssertionError("missing Skill path was accepted")
