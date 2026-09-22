"""Regression coverage for Version 1.0 terminalization guardrails."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
CLAUDE = ROOT / "CLAUDE.md"
CONTEXT = ROOT / "CONTEXT.md"
STATUS = ROOT / "STATUS.md"
USER_INTENT = ROOT / "00-user-intent.md"
RELEASE_CONTRACT = ROOT / "docs" / "release-v1.0-contract.md"
RELEASE = ROOT / "release-v1.0.yaml"
LOOP = ROOT / "skills" / "strategic-sensemaking-loop" / "SKILL.md"
LOOP_RESUME = (
    ROOT
    / "skills"
    / "strategic-sensemaking-loop"
    / "references"
    / "resume-and-routing-v1.md"
)
GOAL_FITNESS = (
    ROOT
    / "skills"
    / "strategic-repository-analysis"
    / "references"
    / "goal-fitness-and-completion-v1.md"
)
RECONCILIATION = ROOT / "skills" / "strategic-repository-reconciliation" / "SKILL.md"


def test_current_v1_state_is_closed_world_terminalization() -> None:
    context = CONTEXT.read_text(encoding="utf-8")
    status = STATUS.read_text(encoding="utf-8")
    intent = USER_INTENT.read_text(encoding="utf-8")

    assert "closed-world version terminalization" in context
    assert "OPERATING MODE = VERSION_1_TERMINALIZATION" in status
    assert "VERSION_1_SCOPE = FROZEN" in status
    assert "NEW_PRODUCT_CONSTRUCTION = CLOSED" in status
    assert "Version 1.0 product-scope obligation set is closed" in intent


def test_agent_bootstrap_respects_terminalization() -> None:
    agents = AGENTS.read_text(encoding="utf-8")
    claude = CLAUDE.read_text(encoding="utf-8")

    assert "**Respect terminalization.**" in agents
    assert "**Terminalization changes work admission.**" in claude
    assert "Do not reopen Level 3 merely because another" in claude


def test_release_contract_defines_scope_freeze_without_new_release_schema() -> None:
    contract = RELEASE_CONTRACT.read_text(encoding="utf-8")
    release = yaml.safe_load(RELEASE.read_text(encoding="utf-8"))

    assert "## Scope freeze and work admission" in contract
    assert "finished Version 1.0\n= frozen obligations satisfied" in contract
    assert "The `1.0.0rc3` target is a reduced-scope release" in contract
    assert "The `1.0.0rc2` target is a reduced-scope release" not in contract

    # Keep the correction semantic; do not add another machine-legible ontology.
    assert "phase" not in release["release"]
    assert "scope_frozen" not in release["release"]
    assert "blocker_admission" not in release["release"]


def test_strategic_loop_requires_positive_evidence_to_reopen_terminal_scope() -> None:
    loop = LOOP.read_text(encoding="utf-8")
    resume = LOOP_RESUME.read_text(encoding="utf-8")

    assert "#### Terminalization reopening guard" in loop
    assert "positive evidence establishes one" in loop
    assert "terminal NO_CHANGE + closed scope" in loop
    assert "no positive blocker evidence is present" in resume
    assert "STOP rather than automatically reassessing Level 3" in resume


def test_goal_fitness_switches_from_open_world_to_closed_world_completion() -> None:
    text = GOAL_FITNESS.read_text(encoding="utf-8")

    assert "## 5A. Closed-world completion during terminalization" in text
    assert "positive blocker evidence is required to reopen current-version construction" in text
    assert "taxonomy inconsistency != construction gap by default" in text


def test_reaffirm_with_no_next_responsibility_is_terminal() -> None:
    text = RECONCILIATION.read_text(encoding="utf-8")

    assert "6A. When the effect is `NO_MODEL_CHANGE` or `REAFFIRM`" in text
    assert "REAFFIRM + responsibility complete + no established next responsibility -> STOP" in text
    assert "completed change != automatic Level-3 reassessment" in text
