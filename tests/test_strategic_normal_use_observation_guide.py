"""Regression coverage for Strategic Sensemaking normal-use observation guidance."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "normal-use" / "strategic-sensemaking-observation-guide.md"
LANE = ROOT / "docs" / "research" / "normal-use-evidence-lane.md"
LOOP_SKILL = ROOT / "skills" / "strategic-sensemaking-loop" / "SKILL.md"


def test_observation_guide_and_evidence_lane_link_each_other() -> None:
    guide = GUIDE.read_text(encoding="utf-8")
    lane = LANE.read_text(encoding="utf-8")

    assert "docs/research/normal-use-evidence-lane.md" in guide
    assert "docs/normal-use/strategic-sensemaking-observation-guide.md" in lane


def test_loop_skill_links_observation_guide() -> None:
    skill = LOOP_SKILL.read_text(encoding="utf-8")

    assert "strategic-sensemaking-observation-guide.md" in skill
