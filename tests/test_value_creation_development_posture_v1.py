"""Contract checks for Value-Creation & Development Posture Reconciliation v1.

These tests protect the guidance surfaces from drifting back toward uncertainty
maximalism, liability-minimizing control, or release-terminalization by default.
They do not establish product usefulness or semantic optimality.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRATEGY = ROOT / "docs" / "product-strategy.md"
OPERATING = ROOT / "docs" / "product-operating-model.md"
LEVEL2_WORKFLOW = ROOT / "docs" / "agent-native-operating-workflow.md"
CONTEXT = ROOT / "CONTEXT.md"
README = ROOT / "README.md"
GETTING_STARTED = ROOT / "GETTING_STARTED.md"
POLICY = ROOT / "docs" / "policy-hierarchy-v0.md"
USING = ROOT / "skills" / "using-sensemaking" / "SKILL.md"
ADAPTIVE_GUIDANCE = (
    ROOT / "skills" / "using-sensemaking" / "references" / "adaptive-guidance-v0.md"
)
INQUIRY = ROOT / "skills" / "using-sensemaking" / "references" / "inquiry-policy-v0.md"
METAREASONING = (
    ROOT / "skills" / "using-sensemaking" / "references" / "metareasoning-policy-v0.md"
)
EXPLORATION = (
    ROOT / "skills" / "using-sensemaking" / "references" / "exploration-policy-v0.md"
)
STRATEGIC = ROOT / "skills" / "strategic-repository-analysis" / "SKILL.md"
GOAL_FITNESS = (
    ROOT
    / "skills"
    / "strategic-repository-analysis"
    / "references"
    / "goal-fitness-and-completion-v1.md"
)
LOOP = ROOT / "skills" / "strategic-sensemaking-loop" / "SKILL.md"
STATUS = ROOT / "STATUS.md"
PYPROJECT = ROOT / "pyproject.toml"


def test_product_strategy_prefers_warranted_value_under_uncertainty() -> None:
    text = STRATEGY.read_text(encoding="utf-8")

    assert "Optimize for valuable, warranted progress under uncertainty" in text
    assert "Treat commission and omission risks symmetrically" in text
    assert "Scale rigor to consequence, not to uncertainty alone" in text
    assert "uncertainty exists\n!= action prohibited" in text
    assert "strict validator selected\n-> validator remains strict" in text


def test_operating_model_makes_lifecycle_posture_qualitative_not_runtime_state() -> None:
    text = OPERATING.read_text(encoding="utf-8")

    assert "Six situational factors" in text
    assert "Development / lifecycle posture" in text
    assert "Active development" in text
    assert "Version terminalization" in text
    assert "Release hardening" in text
    assert "value-creation bias\n!= reckless action" in text
    assert "Do not persist a lifecycle state" in text


def test_using_sensemaking_advances_outcome_before_uncertainty_elimination() -> None:
    text = USING.read_text(encoding="utf-8")

    assert "Advance the governing outcome with the smallest sufficiently warranted move" in text
    assert "Sensemaking optimizes for **valuable, warranted progress under uncertainty**" in text
    assert "risk of commission" in text
    assert "risk of omission" in text
    assert "subjective engineering judgment\n!= owner-reserved intent" in text
    assert "human evidence could improve confidence\n!= human evidence required" in text
    assert "strict and fail-closed" in text



def test_current_context_and_adaptive_guidance_use_six_factor_outcome_first_model() -> None:
    context = CONTEXT.read_text(encoding="utf-8")
    guidance = ADAPTIVE_GUIDANCE.read_text(encoding="utf-8")
    workflow = LEVEL2_WORKFLOW.read_text(encoding="utf-8")

    assert "Advance the governing outcome with the smallest sufficiently warranted move" in context
    assert "Value creation is risk-adjusted, not liability-minimized" in context
    assert "Lifecycle posture changes the default bias, not local truth" in context

    assert "## 1. Six contextual factors" in guidance
    assert "Development / lifecycle posture" in guidance
    assert "value-creation bias\n!= reckless action" in guidance

    assert "six contextual factors from the current adaptive guidance model" in workflow
    assert "development / lifecycle posture" in workflow
    assert "active development + cheap reversible authorized work" in workflow



def test_human_entry_points_expose_lifecycle_posture_without_stage_routing() -> None:
    readme = README.read_text(encoding="utf-8")
    getting = GETTING_STARTED.read_text(encoding="utf-8")

    assert "development/lifecycle posture" in readme
    assert "release target != product evolution closed" in readme
    assert "uncertainty exists != action prohibited" in readme

    assert "**development / lifecycle posture**" in getting
    assert "Advance the governing outcome with the smallest sufficiently" in getting
    assert "cheap reversible\nauthorized construction" in getting
    assert "release target != product evolution closed" in getting


def test_inquiry_and_metareasoning_include_omission_and_delay_cost() -> None:
    inquiry = INQUIRY.read_text(encoding="utf-8")
    metareasoning = METAREASONING.read_text(encoding="utf-8")

    assert "COST OF DELAY / OMISSION IF WE DO NOT ACT" in inquiry
    assert "engineering judgment under delegated authority\n!= owner-intent gap" in inquiry
    assert "RISK OF COMMISSION + RISK OF OMISSION" in metareasoning
    assert "cheap + reversible + authorized + plausibly valuable + information-producing" in metareasoning
    assert "residual uncertainty alone\n!= reason to prefer INQUIRE / VERIFY / ESCALATE" in metareasoning


def test_exploration_reuses_existing_modes_for_product_evolution_search() -> None:
    text = EXPLORATION.read_text(encoding="utf-8")

    assert "Product-evolution search lenses" in text
    for lens in ("IDENTITY", "DEPTH", "ADJACENCY", "COMPOSITION", "PRUNING", "HARDENING"):
        assert lens in text

    for mode in ("EXPLOIT", "EXPLORE", "CHALLENGE", "RECOMBINE", "RESTART", "VERIFY", "EXIT_SEARCH"):
        assert mode in text

    assert "not new modes, schema fields" in text


def test_strategic_analysis_distinguishes_open_evolution_from_terminalization() -> None:
    skill = STRATEGIC.read_text(encoding="utf-8")
    goal = GOAL_FITNESS.read_text(encoding="utf-8")
    loop = LOOP.read_text(encoding="utf-8")

    assert "Establish development / lifecycle posture" in skill
    assert "Search capability identity, depth, adjacency, composition, pruning, and hardening" in skill
    assert "release target exists\n!= product evolution closed" in skill
    assert "Version terminalization" in goal
    assert "release candidate discussed\n!= product evolution closed" in goal
    assert "Development posture before routing" in loop
    assert "Do not infer terminalization merely from an RC/version target" in loop


def test_status_records_open_product_evolution_and_release_as_downstream() -> None:
    text = STATUS.read_text(encoding="utf-8")

    assert "OPEN PRODUCT EVOLUTION / ACTIVE DEVELOPMENT" in text
    assert "VALUE_CREATION_AND_SEMANTIC_CONSISTENCY_NORMAL_USE" in text
    assert "VERSION_1_TERMINALIZATION = NOT_GOVERNING_UNTIL_INTENTIONAL_SCOPE_FREEZE" in text
    assert "RELEASE_HARDENING = DOWNSTREAM_MILESTONE" in text


def test_reinterpretation_adds_no_lifecycle_runtime_or_score() -> None:
    pyproject = PYPROJECT.read_text(encoding="utf-8")
    policy = POLICY.read_text(encoding="utf-8")

    for forbidden in ("LifecycleState", "ValueCreationScore", "LifecycleManager", "DevelopmentPostureRouter"):
        assert forbidden not in pyproject

    assert "Do not create a `LifecycleState`, `ValueCreationScore`" in policy
