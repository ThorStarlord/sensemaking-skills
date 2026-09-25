"""Repository qualification for Strategic Sensemaking Loop v1."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "strategic-sensemaking-loop" / "SKILL.md"
RESUME = ROOT / "skills" / "strategic-sensemaking-loop" / "references" / "resume-and-routing-v1.md"
VALUE_ACTION = ROOT / "skills" / "strategic-sensemaking-loop" / "references" / "value-action-and-delegation-v1.md"
EXPLORATION = ROOT / "skills" / "strategic-repository-analysis" / "references" / "strategic-exploration-funnel-v1.md"
AGENT = ROOT / "skills" / "strategic-sensemaking-loop" / "agents" / "openai.yaml"
REGISTRY = ROOT / "skills" / "workflow-planner" / "references" / "skill-registry.yaml"
RELEASE = ROOT / "release-v1.0.yaml"
CONTRACTS = ROOT / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"
OUTER = ROOT / "docs" / "strategic-outer-loop.md"
GETTING_STARTED = ROOT / "GETTING_STARTED.md"
RECONCILIATION = ROOT / "artifacts" / "strategic_reconciliation.md"


def _flat(text: str) -> str:
    """Collapse line wrapping so prose phrase assertions are wrap-insensitive."""
    return " ".join(text.split())


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
    assert "automatically authoritative" in _flat(resume)


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

    assert "After producing an adequate capsule, **stop for the owner**." in _flat(text)
    assert "Never synthesize or guess the owner's selection." in _flat(text)
    assert "do not recreate the capsule merely because one exists" in _flat(text)

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


def test_loop_prefers_value_producing_warranted_action_without_scoring() -> None:
    text = SKILL.read_text(encoding="utf-8")
    ref = VALUE_ACTION.read_text(encoding="utf-8")

    assert "Value-Producing Action Preference" in text
    assert "value-producing warranted action != lowest-risk action automatically" in text
    assert "Prefer the highest-value **warranted and authorized** action" in ref
    assert "safe-enough high-value action" in ref
    assert "omission cost" in ref
    assert "numeric expected-value scoring" in ref


def test_reversible_build_has_conditional_dominance_not_universal_bias() -> None:
    ref = VALUE_ACTION.read_text(encoding="utf-8")

    assert "Reversible-build dominance test" in _flat(ref)
    assert "REVERSIBLE BUILD normally dominates" in _flat(ref)
    assert "reversible build possible" in ref
    assert "!= reversible build automatically warranted" in ref
    assert "Prefer READ/INSPECT/VERIFY" in ref
    assert "Prefer an experiment when the decision genuinely requires evidence" in ref


def test_high_delegation_envelope_allows_repository_work_but_preserves_protected_transitions() -> None:
    text = SKILL.read_text(encoding="utf-8")
    ref = VALUE_ACTION.read_text(encoding="utf-8")

    assert "high-delegation repository envelope" in _flat(text)
    assert "bounded construction, reversible builds" in _flat(text)
    assert "repository qualification" in text
    assert "warranted probes/experiments" in text
    assert "high delegation\n!= unlimited authority" in ref
    assert "Level-4 product-thesis choices" in ref
    assert "production release/deployment" in ref
    assert "credentials, secrets, billing" in ref


def test_blocked_gate_does_not_force_repository_wide_freeze_or_allow_bypass() -> None:
    text = SKILL.read_text(encoding="utf-8")
    ref = VALUE_ACTION.read_text(encoding="utf-8")

    assert "blocked responsibility != repository-wide freeze automatically" in text
    assert "no independently warranted repository responsibility can proceed" in text
    assert "do not evade the gate" in ref
    assert "another **independently warranted** value-creating responsibility" in ref
    assert "independent work exists" in ref
    assert "!= permission to bypass blocked verification" in ref


def test_consequential_final_report_exposes_compact_decision_trace() -> None:
    text = SKILL.read_text(encoding="utf-8")
    ref = VALUE_ACTION.read_text(encoding="utf-8")

    assert "Decision Trace" in text
    assert "material alternatives actually considered" in text
    assert "value each would create if successful" in text
    assert "materially more conservative move" in text
    assert "materially more aggressive move" in text

    assert "MATERIAL ALTERNATIVES CONSIDERED" in ref
    assert "VALUE CREATED IF SUCCESSFUL" in ref
    assert "user-facing observability" in ref
    assert "not private scratch reasoning" in ref


def test_loop_runs_exploration_funnel_only_at_analyze_boundaries() -> None:
    text = SKILL.read_text(encoding="utf-8")
    guide = EXPLORATION.read_text(encoding="utf-8")

    assert "When this boundary is genuinely active" in text
    assert "Strategic Exploration Funnel" in text
    assert "system map" in text
    assert "breadth exploration" in text
    assert "frontier candidates" in text
    assert "depth drill" in text

    assert "ANALYZE / REOPEN_ANALYSIS" in guide
    assert "RESPONSIBILITY / EXECUTE / VERIFY / RECONCILE" in guide
    assert "preserve current Level 3 unless evidence genuinely reopens it" in guide


def test_loop_does_not_repeat_breadth_analysis_during_mid_episode_resume() -> None:
    text = SKILL.read_text(encoding="utf-8")
    resume = RESUME.read_text(encoding="utf-8")

    assert "Do not run the breadth/depth funnel during" in text
    assert "RESPONSIBILITY / EXECUTE / VERIFY / RECONCILE" in text
    assert "Do not rerun a Skill merely because it appears earlier in the conceptual loop." in resume
    assert "mandatory repository-wide breadth exploration during settled execution or verification" in text


def test_analyze_final_report_exposes_strategic_exploration_summary() -> None:
    text = SKILL.read_text(encoding="utf-8")

    assert "Strategic Exploration Summary" in text
    assert "major systems examined" in text
    assert "breadth opportunity themes/observations" in text
    assert "frontier candidates synthesized" in text
    assert "which candidates advanced to depth and why" in text
    assert "selected Strategic Frontier" in text
    assert "selected construction path" in text
    assert "breadth -> depth -> selection visible to the owner" in text
