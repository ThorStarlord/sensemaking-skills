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
GETTING_STARTED = ROOT / "GETTING_STARTED.md"
STATUS = ROOT / "STATUS.md"


def test_strategic_skill_owns_repository_evolution_not_task_execution() -> None:
    skill = STRATEGIC_SKILL.read_text(encoding="utf-8")

    for phrase in (
        "current-system model",
        "capability / limitation map",
        "Strategic Frontier",
        "Generate coherent construction paths",
        "Compare paths qualitatively",
        "decision-changing uncertainty",
        "BUILD",
        "INVESTIGATE",
        "DEFER",
        "NO_CHANGE",
        "OWNER_DECISION",
        "THESIS_REVIEW",
    ):
        assert phrase in skill

    assert "Do not assign numeric scores" in skill
    assert "Do not automatically create a Campaign, issue, PR, execution handoff, or code" in skill
    assert "strategic analysis != implementation authorization" in skill


def test_construction_path_reference_requires_coherent_distinct_futures() -> None:
    guide = PATH_GUIDE.read_text(encoding="utf-8")

    assert "construction path\n= future state" in guide
    assert "path diversity\n!= category coverage" in guide
    assert "Two paths are materially distinct" in guide
    assert "Do not create an artificial “do nothing” path" in guide
    assert "0–5 construction paths" in guide
    assert "zero paths\n!= missing required ceremony" in guide
    assert "BUILD\n-> at least one path" in guide
    assert "Coarse construction sequence" in guide
    assert "Do not use numbers, stars, weighted" in guide
    assert "path requires capability\n+ path is warranted\n!= capability implementation automatically authorized" in guide


def test_strategic_alternatives_are_conditional_and_zero_path_capable() -> None:
    skill = STRATEGIC_SKILL.read_text(encoding="utf-8")
    guide = PATH_GUIDE.read_text(encoding="utf-8")

    assert "Use zero paths when no construction trajectory is currently warranted/representable" in skill
    assert "zero real paths\n> manufactured alternative" in skill
    assert "Use zero paths when current evidence/authority does not support even one coherent" in guide
    assert "NO_CHANGE" in guide
    assert "OWNER_DECISION" in guide
    assert "THESIS_REVIEW" in guide
    assert "INVESTIGATE" in guide


def test_repo_sensemaker_remains_diagnostic_and_points_strategic_requests_upward() -> None:
    text = REPO_SENSEMAKER.read_text(encoding="utf-8")

    assert "Diagnostic boundary vs. strategic repository analysis" in text
    assert "../strategic-repository-analysis/SKILL.md" in text
    assert "diagnosis != strategic evolution synthesis" in text
    assert "weakest boundary != automatically selected strategic direction" in text
    assert "high-level questions about multiple coherent repository evolution" in text


def test_using_sensemaking_exposes_level3_analysis_without_mandatory_brief() -> None:
    text = USING.read_text(encoding="utf-8")

    assert "When the repository's future is the problem" in text
    assert "strategic-repository-analysis" in text
    assert "repo-sensemaker = diagnostic repository understanding" in text
    assert "strategic-repository-analysis = Level-3 repository evolution synthesis" in text
    assert "repository_sensemaking_brief" in text
    assert "not\na mandatory prerequisite" in text
    assert "strategic disposition\n!= implementation authorization" in text


def test_outer_loop_composes_first_class_construction_paths_without_planner() -> None:
    outer = OUTER.read_text(encoding="utf-8")

    assert "Strategic Repository Sensemaking and construction paths" in outer
    assert "strategic_repository_analysis" in outer
    assert "COHERENT CONSTRUCTION PATHS" in outer
    assert "construction path != backlog" in outer
    assert "path comparison != numeric ranking" in outer
    assert "strategic disposition != implementation authorization" in outer
    assert "Mechanical validation" in outer
    assert "cannot\nchoose a path" in outer


def test_human_entry_points_distinguish_diagnosis_from_strategic_evolution() -> None:
    readme = README.read_text(encoding="utf-8")
    getting = GETTING_STARTED.read_text(encoding="utf-8")

    assert "Deciding how a repository/product could evolve from here" in readme
    assert "strategic-repository-analysis" in readme
    assert "repository/product future itself is open" in readme

    assert "Repository/product future itself is open" in getting
    assert "what could this repository become" in getting
    assert "repository diagnosis\n!= repository evolution synthesis" in getting


def test_current_status_closes_path_synthesis_without_reopening_experiments() -> None:
    status = STATUS.read_text(encoding="utf-8")

    assert "Strategic Repository Sensemaking v1" in status
    assert "Strategic Repository Sensemaking v1 — COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF" in status
    assert "Policy Hierarchy Completion v0 — COMPLETE / INTEGRATED / COMPOSABLE" in status
    assert "EXPERIMENT PREREQUISITE = NONE" in status
    assert "SUPPORTING EVIDENCE MODE = NORMAL_USE_VALIDATION" in status


def test_no_runtime_planner_or_schema_v3_is_added_by_integration() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    release = (ROOT / "release-v1.0.yaml").read_text(encoding="utf-8")

    assert "StrategicPlanner" not in pyproject
    assert "OuterLoopEngine" not in pyproject
    assert "strategic_planner" not in pyproject
    assert 'schema_version: "2"' in release
