"""Regression contract: the legacy repository-brief producer fails closed.

Background (the defect these tests lock down):
  `SkillsOrchestrator.run_repo_sensemaker_skill()` ran the legacy Python
  `RepoSensemakerSkill`, which generated a file inventory and wrote it to
  `<project_root>/artifacts/repository_sensemaking_brief.md` through
  `BaseSkill.write_artifact`. Run against a disposable clone on 2026-10-23, it
  replaced the tracked brief with content that fails `scripts/validate-brief.py`
  and returned `success: True` with `authority: "authorized_autonomously"`
  (artifacts/history/2026-10-23-repository-sensemaking-brief-observation.md,
  section 6).

  The two defects are distinct. The generated content does not satisfy the
  `repository_sensemaking_brief` contract wherever it is written, and the run
  overwrote a tracked artifact while reporting success. Correcting the output
  path alone would not correct the content.

Owner decision (Q-1): keep the legacy API importable, but make the producer
fail closed. These tests assert that contract on every legacy route:
  1. `SkillsOrchestrator`, `run_repo_sensemaker_skill` and `RepoSensemakerSkill`
     remain importable.
  2. Direct `run()`, `run_repo_sensemaker_skill()`, `run_skill()` and
     `instantiate_skill()` return the same explicit, deterministic structured
     failure: no success, no artifact id, no authority claim, and a message
     that names the agent-native `repo-sensemaker` Skill.
  3. The target repository is unchanged: an existing brief is not overwritten
     and no file or directory is created.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from sensemaking_skills.config import SkillsConfig
from sensemaking_skills.runner import SkillsOrchestrator
from sensemaking_skills.skills import BaseSkill, RepoSensemakerSkill

REPO_ROOT = Path(__file__).resolve().parents[1]

SENTINEL_BRIEF = (
    b"# Sentinel repository brief\n\n"
    b"Tracked content that the legacy producer must never overwrite.\n"
)

# Keys of the legacy result shape; callers that read them must not hit KeyError.
LEGACY_RESULT_KEYS = {
    "artifact_id",
    "success",
    "message",
    "repo_summary",
    "key_files_found",
    "active_uncertainty",
    "warranted_responsibility",
    "responsibility_basis",
    "capability_recommendation",
    "capability_availability",
    "authority",
    "workflow_id",
}


def _target_repo(tmp_path: Path, *, with_brief: bool = True) -> Path:
    repo = tmp_path / "target-repo"
    repo.mkdir()
    if with_brief:
        (repo / "artifacts").mkdir()
        (repo / "artifacts" / "repository_sensemaking_brief.md").write_bytes(SENTINEL_BRIEF)
    # Inputs the old inventory read, so a regression has something to write.
    (repo / "CONTEXT.md").write_text("# Context\n", encoding="utf-8")
    (repo / "README.md").write_text("# Target\n", encoding="utf-8")
    (repo / "pyproject.toml").write_text('[project]\nname = "target"\n', encoding="utf-8")
    return repo


def _snapshot(root: Path) -> dict[str, bytes | None]:
    """Every path under root, with file bytes (None for directories)."""
    return {
        path.relative_to(root).as_posix(): None if path.is_dir() else path.read_bytes()
        for path in sorted(root.rglob("*"))
    }


def _config(repo: Path) -> SkillsConfig:
    return SkillsConfig({"project_root": str(repo)})


def _direct_run(config: SkillsConfig) -> dict:
    return RepoSensemakerSkill(config).run()


def _run_repo_sensemaker_skill(config: SkillsConfig) -> dict:
    return SkillsOrchestrator(config=config).run_repo_sensemaker_skill()


def _run_skill(config: SkillsConfig) -> dict:
    return SkillsOrchestrator(config=config).run_skill(RepoSensemakerSkill(config))


def _instantiate_skill(config: SkillsConfig) -> dict:
    skill = SkillsOrchestrator(config=config).instantiate_skill("RepoSensemakerSkill")
    assert isinstance(skill, RepoSensemakerSkill)
    return skill.run()


LEGACY_ROUTES = {
    "direct-run": _direct_run,
    "run_repo_sensemaker_skill": _run_repo_sensemaker_skill,
    "run_skill": _run_skill,
    "instantiate_skill": _instantiate_skill,
}


def test_legacy_api_remains_importable() -> None:
    from sensemaking_skills.skills.repo_sensemaker import RepoSensemakerSkill as module_class

    assert module_class is RepoSensemakerSkill
    assert issubclass(RepoSensemakerSkill, BaseSkill)
    assert callable(SkillsOrchestrator.run_repo_sensemaker_skill)


@pytest.mark.parametrize("route", LEGACY_ROUTES.values(), ids=LEGACY_ROUTES.keys())
def test_legacy_route_reports_explicit_failure(tmp_path: Path, route) -> None:
    result = route(_config(_target_repo(tmp_path)))

    assert LEGACY_RESULT_KEYS <= set(result)
    assert result["success"] is False
    assert result["artifact_id"] is None
    assert result["code"] == "LEGACY_PRODUCER_UNSUPPORTED"
    # No autonomous-authority or capability claim survives the failure.
    assert result["authority"] is None
    assert result["capability_recommendation"] is None
    assert result["capability_availability"] == "unavailable"
    assert result["warranted_responsibility"] is None


@pytest.mark.parametrize("route", LEGACY_ROUTES.values(), ids=LEGACY_ROUTES.keys())
def test_legacy_route_does_not_overwrite_existing_brief(tmp_path: Path, route) -> None:
    repo = _target_repo(tmp_path)
    before = _snapshot(repo)

    route(_config(repo))

    assert (repo / "artifacts" / "repository_sensemaking_brief.md").read_bytes() == SENTINEL_BRIEF
    assert _snapshot(repo) == before


def test_legacy_routes_create_no_artifact(tmp_path: Path) -> None:
    repo = _target_repo(tmp_path, with_brief=False)
    before = _snapshot(repo)

    for route in LEGACY_ROUTES.values():
        route(_config(repo))

    assert not (repo / "artifacts").exists()
    assert _snapshot(repo) == before


def test_failure_is_deterministic_and_names_the_agent_native_skill(tmp_path: Path) -> None:
    config = _config(_target_repo(tmp_path))
    results = [route(config) for route in LEGACY_ROUTES.values()]
    results.append(LEGACY_ROUTES["direct-run"](config))

    assert all(result == results[0] for result in results)
    message = results[0]["message"]
    assert "unsupported" in message
    assert "repository_sensemaking_brief" in message
    assert "repo-sensemaker" in message
    # The message is printed by BaseSkill.log; console output must stay ASCII.
    assert message.isascii()


def test_redirect_target_is_the_declared_brief_producer() -> None:
    contracts = yaml.safe_load(
        (REPO_ROOT / "skills/workflow-planner/references/artifact-contracts.yaml").read_text(
            encoding="utf-8"
        )
    )
    brief = next(
        item for item in contracts["artifacts"] if item["id"] == "repository_sensemaking_brief"
    )

    assert brief["produced_by"] == "repo-sensemaker"
    assert (REPO_ROOT / "skills/repo-sensemaker/SKILL.md").is_file()
