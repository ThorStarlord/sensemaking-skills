"""Terminal currentness checks for Strategic Repository Sensemaking v1."""

from __future__ import annotations

from pathlib import Path

import tomllib
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_candidate_reservoir_names_strategic_repository_analysis() -> None:
    text = (ROOT / "docs" / "strategic-candidate-directions.md").read_text(
        encoding="utf-8"
    )

    assert "strategic-repository-analysis" in text
    assert "strategic_repository_analysis" in text


def test_current_public_surface_records_the_capability() -> None:
    public = (ROOT / "docs" / "public-surface-v1.0.md").read_text(encoding="utf-8")

    assert "strategic-repository-analysis" in public
    assert "strategic_repository_analysis" in public


def test_release_is_rc5_development_and_no_runtime_planner_is_promoted() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    release_text = (ROOT / "release-v1.0.yaml").read_text(encoding="utf-8")
    release = yaml.safe_load(release_text)

    assert pyproject["project"]["version"] == "1.0.0rc5.dev0"
    assert release["release"]["version"] == "1.0.0rc5"
    assert release["release"]["status"] == "development"
    assert 'schema_version: "2"' in release_text
    assert "StrategicPlanner" not in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "OuterLoopEngine" not in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
