"""Integration contracts for Strategic Repository Sensemaking v1.

These checks establish product-surface composition and authority boundaries.
They do not establish strategic correctness or comparative usefulness.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRATEGIC_SKILL = ROOT / "skills" / "strategic-repository-analysis" / "SKILL.md"
PATH_GUIDE = (
    ROOT
    / "skills"
    / "strategic-repository-analysis"
    / "references"
    / "construction-path-synthesis-v1.md"
)
REPO_SENSEMAKER = ROOT / "skills" / "repo-sensemaker" / "SKILL.md"
USING = ROOT / "skills" / "using-sensemaking" / "SKILL.md"
OUTER = ROOT / "docs" / "strategic-outer-loop.md"
README = ROOT / "README.md"


def test_strategic_skill_names_strategic_disposition_tokens() -> None:
    skill = STRATEGIC_SKILL.read_text(encoding="utf-8")

    for token in (
        "BUILD",
        "INVESTIGATE",
        "DEFER",
        "NO_CHANGE",
        "OWNER_DECISION",
        "THESIS_REVIEW",
    ):
        assert token in skill


def test_construction_path_guide_names_strategic_disposition_tokens() -> None:
    guide = PATH_GUIDE.read_text(encoding="utf-8")

    assert "NO_CHANGE" in guide
    assert "OWNER_DECISION" in guide
    assert "THESIS_REVIEW" in guide
    assert "INVESTIGATE" in guide


def test_repo_sensemaker_links_strategic_repository_analysis_skill() -> None:
    text = REPO_SENSEMAKER.read_text(encoding="utf-8")

    assert "../strategic-repository-analysis/SKILL.md" in text


def test_using_sensemaking_names_strategic_analysis_skill_and_brief_artifact() -> None:
    text = USING.read_text(encoding="utf-8")

    assert "strategic-repository-analysis" in text
    assert "repository_sensemaking_brief" in text


def test_outer_loop_names_strategic_repository_analysis_artifact() -> None:
    outer = OUTER.read_text(encoding="utf-8")

    assert "strategic_repository_analysis" in outer


def test_readme_names_strategic_repository_analysis_skill() -> None:
    readme = README.read_text(encoding="utf-8")

    assert "strategic-repository-analysis" in readme


def test_no_runtime_planner_or_schema_v3_is_added_by_integration() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    release = (ROOT / "release-v1.0.yaml").read_text(encoding="utf-8")

    assert "StrategicPlanner" not in pyproject
    assert "OuterLoopEngine" not in pyproject
    assert "strategic_planner" not in pyproject
    assert 'schema_version: "2"' in release


def test_strategic_skill_names_v2_grounding_contract_fields() -> None:
    skill = STRATEGIC_SKILL.read_text(encoding="utf-8")

    for field in (
        "schema_version: 2",
        "frontier_refs",
        "why_plausible",
        "builds_on_capability_ids",
        "required_capability_ids",
    ):
        assert field in skill
