"""Repository qualification for Strategic Sensemaking Loop v1."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "strategic-sensemaking-loop" / "SKILL.md"
RESUME = ROOT / "skills" / "strategic-sensemaking-loop" / "references" / "resume-and-routing-v1.md"
AGENT = ROOT / "skills" / "strategic-sensemaking-loop" / "agents" / "openai.yaml"
REGISTRY = ROOT / "skills" / "workflow-planner" / "references" / "skill-registry.yaml"
RELEASE = ROOT / "release-v1.0.yaml"
CONTRACTS = ROOT / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
GETTING_STARTED = ROOT / "GETTING_STARTED.md"
RECONCILIATION = ROOT / "artifacts" / "history" / "2026-09-22-strategic-reconciliation.md"


def test_loop_skill_frontmatter_and_specialized_skill_references() -> None:
    text = SKILL.read_text(encoding="utf-8")

    assert "name: strategic-sensemaking-loop" in text

    for skill_id in (
        "strategic-repository-analysis",
        "using-sensemaking",
        "handoff",
        "strategic-repository-reconciliation",
        "owner-decision-capsule",
    ):
        assert skill_id in text


def test_loop_skill_and_resume_reference_strategic_disposition_tokens() -> None:
    text = SKILL.read_text(encoding="utf-8")
    resume = RESUME.read_text(encoding="utf-8")

    for marker in ("OWNER_DECISION", "THESIS_REVIEW"):
        assert marker in text
        assert marker in resume


def test_loop_resume_reference_names_repository_qualification_workflow() -> None:
    resume = RESUME.read_text(encoding="utf-8")

    assert "repository-qualification.yml" in resume


def test_post_tracer_strategic_reconciliation_validates_and_reaffirms() -> None:
    commands = (
        [
            sys.executable,
            str(ROOT / "scripts" / "validate-artifact.py"),
            "strategic_reconciliation",
            str(RECONCILIATION),
            "--repo-root",
            str(ROOT),
        ],
        [
            sys.executable,
            str(ROOT / "scripts" / "validate-strategic-companion.py"),
            str(RECONCILIATION),
        ],
    )
    for command in commands:
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr

    text = RECONCILIATION.read_text(encoding="utf-8")
    assert "Strategic effect: REAFFIRM." in text
    assert "strategic_effect: REAFFIRM" in text
    assert "Organization representation established" in text
    assert "!= Organization runtime warranted" in text
    assert "independent semantic multi-agent benefit remains unestablished" in text

def test_loop_resume_reference_names_owner_decision_capsule_artifact() -> None:
    resume = RESUME.read_text(encoding="utf-8")

    assert "owner_decision_capsule" in resume


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


def test_loop_is_named_in_getting_started() -> None:
    getting_started = GETTING_STARTED.read_text(encoding="utf-8")

    assert "strategic-sensemaking-loop" in getting_started
