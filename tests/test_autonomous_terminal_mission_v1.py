"""Regression coverage for Autonomous Terminal Mission Continuation v1."""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "strategic-sensemaking-loop" / "SKILL.md"
REFERENCE = (
    ROOT
    / "skills"
    / "strategic-sensemaking-loop"
    / "references"
    / "autonomous-terminal-mission-v1.md"
)
AGENT = ROOT / "skills" / "strategic-sensemaking-loop" / "agents" / "openai.yaml"
USING = ROOT / "skills" / "using-sensemaking" / "SKILL.md"
DELEGATED = ROOT / "skills" / "using-sensemaking" / "references" / "delegated-goal-patterns.md"


def test_full_autonomy_is_profile_of_existing_front_door() -> None:
    skill = SKILL.read_text(encoding="utf-8")
    ref = REFERENCE.read_text(encoding="utf-8")

    assert "references/autonomous-terminal-mission-v1.md" in skill
    assert "strategic-sensemaking-loop" in ref
    assert not (ROOT / "skills" / "autonomous-terminal-mission").exists()


def test_skill_metadata_triggers_terminal_missions_without_new_frontmatter_fields() -> None:
    text = SKILL.read_text(encoding="utf-8")
    _, raw, _ = text.split("---", 2)
    metadata = yaml.safe_load(raw)

    assert set(metadata) == {"name", "description"}
    description = str(metadata["description"])
    assert "FULL AUTONOMY" in description
    assert "FULL DELEGATION" in description
    assert "terminal" in description.lower()

    agent = yaml.safe_load(AGENT.read_text(encoding="utf-8"))
    assert "one prompt" in agent["interface"]["short_description"].lower()
    assert "full-autonomy terminal missions" in agent["interface"]["short_description"].lower()


def test_using_sensemaking_links_loop_and_terminal_mission_reference() -> None:
    using = USING.read_text(encoding="utf-8")
    delegated = DELEGATED.read_text(encoding="utf-8")

    assert "strategic-sensemaking-loop" in using
    assert "references/autonomous-terminal-mission-v1.md" in using
    assert "autonomous-terminal-mission-v1.md" in delegated
