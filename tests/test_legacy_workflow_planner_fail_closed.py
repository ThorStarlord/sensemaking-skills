"""Regression contract: the legacy workflow planner fails closed.

Background (the defect these tests lock down):
  The legacy Python ``WorkflowPlannerSkill`` read the repository sensemaking
  brief, chose a workflow from a static table, and wrote a simplified plan to
  ``artifacts/workflow_orchestration_plan.md``. That flat path is not the
  canonical plan path (``artifacts/plan_{workflow_id}.md``); the generated
  sections and fields do not satisfy the ``workflow_orchestration_plan``
  contract; and the static table emits fog types and workflow IDs outside the
  canonical vocabulary and the workflow registry. The skill nevertheless
  returned ``success: True``, so it could replace a tracked plan while reporting
  success. Reviewed knowledge records this as
  ``observation:legacy-plan-producer-overwrites-tracked-plan``.

Owner decision (T2): keep the legacy API importable, but make the invalid plan
producer fail closed. These tests assert that contract on every legacy route,
for a valid, an invalid and an absent brief:
  1. the compatibility surface remains importable and callable;
  2. every route returns the same explicit, deterministic failure (code
     LEGACY_PLANNER_UNSUPPORTED) that names the agent-native ``workflow-planner``
     Skill and claims no plan, selected workflow or execution authority;
  3. the target repository is unchanged: existing plans and the brief keep their
     bytes, and no file or directory is created.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from sensemaking_skills.config import SkillsConfig
from sensemaking_skills.runner import SkillsOrchestrator
from sensemaking_skills.skills import BaseSkill, WorkflowPlannerSkill

REPO_ROOT = Path(__file__).resolve().parents[1]

SENTINEL_PLAN = b"# Tracked legacy plan (sentinel)\n\nMust survive every legacy route.\n"
SENTINEL_CANONICAL_PLAN = b"# Canonical plan (sentinel)\n"

# The legacy planner selects its fog type from brief text: this brief reads as a
# Sensemaking project, so the defective path would succeed and write a plan.
VALID_BRIEF = (
    b"# Repository Sensemaking Brief\n\n"
    b"primary_fog_type: product_fog\n\n"
    b"The repository contains CONTEXT.md and a workflows directory.\n"
)
INVALID_BRIEF = b"# Not a brief\n\nNo contract fields here.\n"

BRIEF_STATES = {
    "valid-brief": VALID_BRIEF,
    "invalid-brief": INVALID_BRIEF,
    "no-brief": None,
}


def _config(repo: Path) -> SkillsConfig:
    return SkillsConfig({"project_root": str(repo)})


def _target_repo(root: Path, brief: bytes | None) -> Path:
    repo = root / "target-repo"
    artifacts = repo / "artifacts"
    artifacts.mkdir(parents=True)
    (artifacts / "workflow_orchestration_plan.md").write_bytes(SENTINEL_PLAN)
    (artifacts / "plan_fast-path-workflow.md").write_bytes(SENTINEL_CANONICAL_PLAN)
    if brief is not None:
        (artifacts / "repository_sensemaking_brief.md").write_bytes(brief)
    (repo / "CONTEXT.md").write_text("# Context\n", encoding="utf-8")
    (repo / "workflows").mkdir()
    return repo


def _snapshot(root: Path) -> dict[str, bytes | None]:
    """Every path under root, with file bytes (None for directories)."""
    return {
        path.relative_to(root).as_posix(): None if path.is_dir() else path.read_bytes()
        for path in sorted(root.rglob("*"))
    }


def _direct_run(config: SkillsConfig) -> dict:
    return WorkflowPlannerSkill(config).run()


def _orchestrator_run(config: SkillsConfig) -> dict:
    return SkillsOrchestrator(config=config).run_workflow_planner_skill()


def _run_skill(config: SkillsConfig) -> dict:
    return SkillsOrchestrator(config=config).run_skill(WorkflowPlannerSkill(config))


def _instantiate_then_run(config: SkillsConfig) -> dict:
    skill = SkillsOrchestrator(config=config).instantiate_skill("WorkflowPlannerSkill")
    assert isinstance(skill, WorkflowPlannerSkill)
    return skill.run()


LEGACY_ROUTES = {
    "direct-run": _direct_run,
    "run_workflow_planner_skill": _orchestrator_run,
    "run_skill": _run_skill,
    "instantiate_skill": _instantiate_then_run,
}


def test_compatibility_surface_remains_importable_and_callable() -> None:
    from sensemaking_skills.skills.workflow_planner import WorkflowPlannerSkill as module_class

    assert module_class is WorkflowPlannerSkill
    assert issubclass(WorkflowPlannerSkill, BaseSkill)
    assert callable(SkillsOrchestrator.run_workflow_planner_skill)
    assert callable(SkillsOrchestrator.run_skill)
    assert callable(SkillsOrchestrator.instantiate_skill)


def test_instantiate_skill_returns_an_instance_not_a_result(tmp_path: Path) -> None:
    orchestrator = SkillsOrchestrator(config=_config(_target_repo(tmp_path, VALID_BRIEF)))

    skill = orchestrator.instantiate_skill("WorkflowPlannerSkill")

    assert isinstance(skill, WorkflowPlannerSkill)
    assert not isinstance(skill, dict)


def test_unrelated_orchestrator_behaviour_is_preserved(tmp_path: Path) -> None:
    from sensemaking_skills.skills import RepoSensemakerSkill

    orchestrator = SkillsOrchestrator(config=_config(_target_repo(tmp_path, None)))

    assert isinstance(orchestrator.instantiate_skill("RepoSensemakerSkill"), RepoSensemakerSkill)
    assert orchestrator.instantiate_skill("NoSuchSkill") is None


@pytest.mark.parametrize("brief_state", list(BRIEF_STATES))
@pytest.mark.parametrize("route_name", list(LEGACY_ROUTES))
def test_route_reports_explicit_unsupported_failure(
    tmp_path: Path, route_name: str, brief_state: str
) -> None:
    config = _config(_target_repo(tmp_path, BRIEF_STATES[brief_state]))

    result = LEGACY_ROUTES[route_name](config)

    assert result["success"] is False
    assert result["artifact_id"] is None
    assert result["code"] == "LEGACY_PLANNER_UNSUPPORTED"
    # No fabricated planning result, selected workflow, or execution authority.
    assert result["fog_type"] is None
    assert result["recommended_workflows"] == []
    assert result["chosen_workflow_id"] is None
    assert result["authority"] is None
    assert "unsupported" in result["message"].lower()
    assert "workflow-planner" in result["message"]


@pytest.mark.parametrize("brief_state", list(BRIEF_STATES))
def test_all_routes_return_the_same_failure(tmp_path: Path, brief_state: str) -> None:
    results = {}
    for route_name, route in LEGACY_ROUTES.items():
        repo = _target_repo(tmp_path / route_name, BRIEF_STATES[brief_state])
        results[route_name] = route(_config(repo))

    first = next(iter(results.values()))
    assert first["success"] is False, first
    assert all(result == first for result in results.values()), results


@pytest.mark.parametrize("brief_state", list(BRIEF_STATES))
@pytest.mark.parametrize("route_name", list(LEGACY_ROUTES))
def test_route_never_overwrites_existing_plans(
    tmp_path: Path, route_name: str, brief_state: str
) -> None:
    repo = _target_repo(tmp_path, BRIEF_STATES[brief_state])

    LEGACY_ROUTES[route_name](_config(repo))

    artifacts = repo / "artifacts"
    assert (artifacts / "workflow_orchestration_plan.md").read_bytes() == SENTINEL_PLAN
    assert (artifacts / "plan_fast-path-workflow.md").read_bytes() == SENTINEL_CANONICAL_PLAN


@pytest.mark.parametrize("brief_state", list(BRIEF_STATES))
@pytest.mark.parametrize("route_name", list(LEGACY_ROUTES))
def test_route_leaves_repository_tree_unchanged(
    tmp_path: Path, route_name: str, brief_state: str
) -> None:
    repo = _target_repo(tmp_path, BRIEF_STATES[brief_state])
    before = _snapshot(repo)

    LEGACY_ROUTES[route_name](_config(repo))

    assert _snapshot(repo) == before


def test_failure_message_is_ascii_and_names_the_agent_native_skill(tmp_path: Path) -> None:
    result = _direct_run(_config(_target_repo(tmp_path, VALID_BRIEF)))

    assert result["message"].isascii()
    assert "agent-native" in result["message"]


def test_agent_native_workflow_planner_contract_remains_present() -> None:
    skill_md = (REPO_ROOT / "skills" / "workflow-planner" / "SKILL.md").read_text(encoding="utf-8")
    contracts = (
        REPO_ROOT / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
    ).read_text(encoding="utf-8")

    assert "name: workflow-planner" in skill_md
    assert "id: workflow_orchestration_plan" in contracts
