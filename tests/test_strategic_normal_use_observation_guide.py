"""Regression coverage for Strategic Sensemaking normal-use observation guidance."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "normal-use" / "strategic-sensemaking-observation-guide.md"
LANE = ROOT / "docs" / "research" / "normal-use-evidence-lane.md"
LOOP_SKILL = ROOT / "skills" / "strategic-sensemaking-loop" / "SKILL.md"
LOOP_DOC = ROOT / "docs" / "strategic-sensemaking-loop-v1.md"


def test_observation_guide_covers_six_normal_use_questions() -> None:
    text = GUIDE.read_text(encoding="utf-8")

    for phrase in (
        "breadth before convergence",
        "frontier-candidate compression",
        "proportional depth",
        "semantic resume",
        "BUILD versus unnecessary inquiry",
        "Goal Fitness and qualification frontier",
    ):
        assert phrase in text

    assert "Strategic Exploration Summary" in text
    assert "Decision relevance is." in text or "Decision relevance is" in text
    assert "construction-eligible" in text
    assert "overcorrection" in text


def test_observation_guide_is_not_new_runtime_or_benchmark() -> None:
    text = GUIDE.read_text(encoding="utf-8")

    for phrase in (
        "normal-use observation\n!= synthetic benchmark",
        "one awkward episode\n!= architectural defect",
        "a Sensemaking quality score",
        "a BUILD-rate target",
        "a benchmark leaderboard",
        "mandatory episode capture",
        "automatic telemetry",
        "a new policy layer",
        "a new experiment program",
        "automatic strategy reopening",
    ):
        assert phrase in text


def test_observation_guide_extends_existing_evidence_lane() -> None:
    guide = GUIDE.read_text(encoding="utf-8")
    lane = LANE.read_text(encoding="utf-8")

    assert "docs/research/normal-use-evidence-lane.md" in guide
    assert "Do not create a parallel evidence database" in guide
    assert "docs/normal-use/strategic-sensemaking-observation-guide.md" in lane
    assert "do not create a parallel tracker" in lane


def test_loop_exposes_observation_without_making_it_a_stage() -> None:
    skill = LOOP_SKILL.read_text(encoding="utf-8")
    doc = LOOP_DOC.read_text(encoding="utf-8")

    assert "strategic-sensemaking-observation-guide.md" in skill
    assert "normal-use observation\n!= loop stage" in skill
    assert "Do not delay work" in skill

    assert "## Normal-use product observation" in doc
    assert "observability\n!= benchmark" in doc
    assert "not a parallel tracker" in doc


def test_cross_episode_escalation_requires_recurrence() -> None:
    text = GUIDE.read_text(encoding="utf-8")

    assert "isolated oddity\n-> preserve evidence" in text
    assert "repeated materially similar friction\n-> cross-episode reconciliation" in text
    assert "stable decision-relevant failure boundary\n-> reopen Strategic Sensemaking strategy" in text
    assert "A single failure does not warrant another Skill" in text
