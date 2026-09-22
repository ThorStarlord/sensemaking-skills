"""Repository qualification for Strategic Sensemaking Loop v1."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "strategic-sensemaking-loop" / "SKILL.md"
RESUME = ROOT / "skills" / "strategic-sensemaking-loop" / "references" / "resume-and-routing-v1.md"
AGENT = ROOT / "skills" / "strategic-sensemaking-loop" / "agents" / "openai.yaml"
REGISTRY = ROOT / "skills" / "workflow-planner" / "references" / "skill-registry.yaml"
RELEASE = ROOT / "release-v1.0.yaml"
CONTRACTS = ROOT / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
OUTER = ROOT / "docs" / "strategic-outer-loop.md"
GETTING_STARTED = ROOT / "GETTING_STARTED.md"


def test_loop_skill_exists_as_thin_front_door_over_specialized_skills() -> None:
    text = SKILL.read_text(encoding="utf-8")

    assert "name: strategic-sensemaking-loop" in text
    assert "single front door" in text
    assert "one front door != one semantic responsibility" in text

    for skill_id in (
        "strategic-repository-analysis",
        "using-sensemaking",
        "handoff",
        "strategic-repository-reconciliation",
        "owner-decision-capsule",
    ):
        assert skill_id in text

    assert "Do **not** create a new master strategic artifact" in text
    assert "deterministic planner/router" in text or "deterministic semantic router" in text


def test_loop_resumes_from_semantic_boundary_and_skips_completed_stages() -> None:
    text = SKILL.read_text(encoding="utf-8")
    resume = RESUME.read_text(encoding="utf-8")

    for marker in (
        "ANALYZE",
        "RESPONSIBILITY",
        "EXECUTE",
        "RECONCILE",
        "OWNER_DECISION",
        "THESIS_REVIEW",
        "STOP",
    ):
        assert marker in text
        assert marker in resume

    assert "latest semantically valid boundary" in text
    assert "Do not rerun an earlier stage merely because it is part of the canonical loop." in text
    assert "Do not rerun a Skill merely because it appears earlier in the conceptual loop." in resume
    assert "newer mtime" in resume
    assert "newest file" in resume


def test_loop_allows_direct_execution_without_fabricating_skill_identity() -> None:
    text = SKILL.read_text(encoding="utf-8")
    resume = RESUME.read_text(encoding="utf-8")

    assert "same active agent + clear bounded action" in text
    assert "-> execute directly" in text
    assert "Use `handoff` only when a prompt handoff to a **registered Skill**" in text
    assert "Do not invent a Skill identity for a workflow" in text

    assert "repository-qualification.yml" in resume
    assert "!= repository-qualification Skill" in resume
    assert "GitHub Action" in resume or "GitHub Actions" in resume
    assert "not a Skill identity" in resume



def test_loop_treats_organization_as_optional_read_only_execution_evidence() -> None:
    text = SKILL.read_text(encoding="utf-8")
    resume = RESUME.read_text(encoding="utf-8")

    for phrase in (
        "Organization visible != Organization warranted",
        "role binding != actor allocation",
        "Organization Pattern != execution authority",
        "organization inspect / organization role / organization skill-profile",
        "not a new resume state",
        "not Skill selection",
        "not actor allocation",
        "not execution authorization",
    ):
        assert phrase in text

    assert "Skip Organization inspection when" in resume
    assert "Organization inspection is not a loop stage" in resume
    assert "organization valid" in resume
    assert "!= organization warranted" in resume
    assert "role binding" in resume
    assert "!= actor allocation" in resume

def test_loop_stops_at_owner_boundary_and_resumes_from_explicit_owner_choice() -> None:
    text = SKILL.read_text(encoding="utf-8")
    resume = RESUME.read_text(encoding="utf-8")

    assert "After producing an adequate capsule, **stop for the owner**." in text
    assert "Never synthesize or guess the owner's selection." in text
    assert "do not recreate the capsule merely because one exists" in text

    assert "owner_decision_capsule" in resume
    assert "+ no explicit owner selection" in resume
    assert "-> STOP" in resume
    assert "+ explicit current owner selection" in resume
    assert "-> using-sensemaking" in resume


def test_loop_does_not_create_master_artifact_contract() -> None:
    contracts = yaml.safe_load(CONTRACTS.read_text(encoding="utf-8"))["artifacts"]
    artifact_ids = {item["id"] for item in contracts}

    assert "strategic_sensemaking_loop" not in artifact_ids
    assert "strategic_sensemaking_state" not in artifact_ids
    assert "strategic_sensemaking_loop_state" not in artifact_ids


def test_loop_is_registered_internal_and_has_agent_metadata() -> None:
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    core = {item["id"]: item for item in registry["ecosystems"]["core"]["skills"]}

    assert "strategic-sensemaking-loop" in core
    item = core["strategic-sensemaking-loop"]
    assert item["artifact"] == "session_summary"
    assert item["availability"]["type"] == "local_command"
    assert item["invocation"]["command"] == "/strategic-sensemaking-loop"

    release = yaml.safe_load(RELEASE.read_text(encoding="utf-8"))
    assert "strategic-sensemaking-loop" in release["skill_inventory"]["internal"]
    assert "strategic-sensemaking-loop" not in release["skill_inventory"]["supported"]

    agent = yaml.safe_load(AGENT.read_text(encoding="utf-8"))
    assert agent["interface"]["display_name"] == "Strategic Sensemaking Loop"
    assert "one prompt" in agent["interface"]["short_description"].lower()


def test_loop_is_documented_as_orchestration_not_new_control_level() -> None:
    outer = OUTER.read_text(encoding="utf-8")
    getting_started = GETTING_STARTED.read_text(encoding="utf-8")

    assert "one-prompt front" in outer
    assert "does not add a fifth control level" in outer
    assert "strategic-sensemaking-loop" in getting_started
    assert "skips stages that are already complete" in getting_started
