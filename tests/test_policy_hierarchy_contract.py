"""Mechanical contract checks for Policy Hierarchy Completion v0.

These tests verify that canonical policy surfaces and boundary statements remain
present. They do not establish semantic correctness or policy usefulness.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "policy-hierarchy-v0.md"
INQUIRY = ROOT / "skills" / "using-sensemaking" / "references" / "inquiry-policy-v0.md"
METAREASONING = ROOT / "skills" / "using-sensemaking" / "references" / "metareasoning-policy-v0.md"
EXPLORATION = ROOT / "skills" / "using-sensemaking" / "references" / "exploration-policy-v0.md"
WARRANT_CHOICE = ROOT / "skills" / "using-sensemaking" / "references" / "warrant-choice-policy-v0.md"
BOOTSTRAP = ROOT / "skills" / "using-sensemaking" / "SKILL.md"
PRACTICAL = ROOT / "skills" / "using-sensemaking" / "references" / "practical-agent-architecture-v0.md"
OUTER = ROOT / "docs" / "strategic-outer-loop.md"
STATUS = ROOT / "STATUS.md"


def test_policy_hierarchy_v0_preserves_semantic_control_boundaries() -> None:
    policy = POLICY.read_text(encoding="utf-8")

    for layer in (
        "STRATEGIC POLICY",
        "INQUIRY POLICY",
        "METAREASONING POLICY",
        "EXPLORATION POLICY",
        "WARRANT / CHOICE POLICY",
        "ACTION / EXECUTION",
        "LEARNING / RECONCILIATION POLICY",
    ):
        assert layer in policy

    assert "policy layer\n!= runtime service" in policy
    assert "capability exists\n!= policy must activate" in policy
    assert "unresolved uncertainty\n!= inquiry required" in policy
    assert "generic `AgentState`" in policy
    assert "OuterLoopEngine" in policy
    assert "automatic Skill/workflow/Campaign selection" in policy


def test_inquiry_policy_v0_supports_zero_inquiry_and_source_boundaries() -> None:
    inquiry = INQUIRY.read_text(encoding="utf-8")

    for outcome in (
        "NO_INQUIRY_NEEDED",
        "INQUIRY_REQUIRED",
        "OWNER_INTENT_REQUIRED",
        "EXTERNAL_EVIDENCE_REQUIRED",
        "VERIFICATION_REQUIRED",
    ):
        assert outcome in inquiry

    assert "uncertainty exists\n!= inquiry required" in inquiry
    assert "more evidence possible\n!= more evidence worth obtaining" in inquiry
    assert "inquiry selected\n!= action authorized" in inquiry
    assert "owner intent" in inquiry.lower()
    assert "smallest sufficient inquiry" in inquiry
    assert "No numeric score is required." in inquiry


def test_metareasoning_policy_v0_exposes_qualitative_control_moves() -> None:
    metareasoning = METAREASONING.read_text(encoding="utf-8")

    for move in ("ACT", "INQUIRE", "CHALLENGE", "EXPLORE", "VERIFY", "ESCALATE", "STOP"):
        assert f"`{move}`" in metareasoning

    assert "continue reasoning when expected decision improvement" in metareasoning
    assert "No numeric calculation is required." in metareasoning
    assert "control move selected\n!= responsibility authorized" in metareasoning
    assert "not a service, scheduler, score, state machine, or automatic router" in metareasoning


def test_metareasoning_policy_is_integrated_without_displacing_strategic_analysis() -> None:
    bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
    practical = PRACTICAL.read_text(encoding="utf-8")
    outer = OUTER.read_text(encoding="utf-8")
    status = STATUS.read_text(encoding="utf-8")

    assert "Metareasoning Policy v0" in bootstrap
    assert "references/metareasoning-policy-v0.md" in bootstrap
    assert "metareasoning-policy-v0.md" in practical
    assert "Metareasoning Policy" in outer
    assert "Metareasoning Policy v0" in status
    assert "Policy Hierarchy Completion v0" in status
    assert "PRIMARY CONSTRUCTION PROGRAM = STRATEGIC_REPOSITORY_SENSEMAKING_V1" in status
    assert "COMPOSABLE POLICY PROGRAM = POLICY_HIERARCHY_COMPLETION_V0" in status


def test_exploration_policy_v0_exposes_iterative_search_modes() -> None:
    exploration = EXPLORATION.read_text(encoding="utf-8")

    for mode in (
        "EXPLOIT",
        "EXPLORE",
        "CHALLENGE",
        "DIAGNOSE",
        "RECOMBINE",
        "RESTART",
        "VERIFY",
        "EXIT_SEARCH",
    ):
        assert f"`{mode}`" in exploration

    assert "search history exists\n!= persistent SearchState required" in exploration
    assert "Exploration Policy\n!= Strategic Frontier ranking" in exploration
    assert "not a search engine, planner, score, enum contract, persistent search tree, or automatic router" in exploration
    assert "SearchState.json" in exploration
    assert "EXIT_SEARCH" in exploration


def test_exploration_policy_is_integrated_without_displacing_strategic_analysis() -> None:
    bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
    practical = PRACTICAL.read_text(encoding="utf-8")
    outer = OUTER.read_text(encoding="utf-8")
    status = STATUS.read_text(encoding="utf-8")

    assert "Exploration Policy v0" in bootstrap
    assert "references/exploration-policy-v0.md" in bootstrap
    assert "exploration-policy-v0.md" in practical
    assert "Exploration Policy" in outer
    assert "Exploration Policy v0" in status
    assert "PRIMARY CONSTRUCTION PROGRAM = STRATEGIC_REPOSITORY_SENSEMAKING_V1" in status
    assert "COMPOSABLE POLICY PROGRAM = POLICY_HIERARCHY_COMPLETION_V0" in status


def test_warrant_choice_policy_v0_is_target_specific_and_non_authorizing() -> None:
    warrant = WARRANT_CHOICE.read_text(encoding="utf-8")

    for disposition in (
        "WARRANTED",
        "NOT_WARRANTED",
        "MORE_EVIDENCE_REQUIRED",
        "AUTHORITY_REQUIRED",
        "OWNER_DECISION_REQUIRED",
        "CHALLENGE_REQUIRED",
        "EXPLORATION_REQUIRED",
        "VERIFICATION_REQUIRED",
        "SMALLER_INTERVENTION_PREFERRED",
        "NO_SELECTION",
    ):
        assert f"`{disposition}`" in warrant

    assert "warrant for target A\n!= warrant for target B" in warrant
    assert "WARRANTED\n!= authorized" in warrant
    assert "candidate set exists\n!= one candidate must be selected" in warrant
    assert "not a permission token, score, rule engine, ranking service, or automatic chooser" in warrant


def test_warrant_choice_policy_is_integrated_without_displacing_strategic_analysis() -> None:
    bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
    practical = PRACTICAL.read_text(encoding="utf-8")
    outer = OUTER.read_text(encoding="utf-8")
    status = STATUS.read_text(encoding="utf-8")

    assert "Warrant / Choice Policy v0" in bootstrap
    assert "references/warrant-choice-policy-v0.md" in bootstrap
    assert "warrant-choice-policy-v0.md" in practical
    assert "Warrant / Choice Policy" in outer
    assert "Warrant / Choice Policy v0" in status
    assert "PRIMARY CONSTRUCTION PROGRAM = STRATEGIC_REPOSITORY_SENSEMAKING_V1" in status
    assert "COMPOSABLE POLICY PROGRAM = POLICY_HIERARCHY_COMPLETION_V0" in status


def test_inquiry_policy_is_integrated_into_agent_and_control_surfaces() -> None:
    bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
    practical = PRACTICAL.read_text(encoding="utf-8")
    outer = OUTER.read_text(encoding="utf-8")

    assert "Inquiry Policy v0" in bootstrap
    assert "references/inquiry-policy-v0.md" in bootstrap
    assert "NO_INQUIRY_NEEDED" in bootstrap

    assert "inquiry-policy-v0.md" in practical
    assert "apply Inquiry Policy" in practical

    assert "policy-hierarchy-v0.md" in outer
    assert "Inquiry Policy" in outer
    assert "semantic control contracts" in outer


def test_status_preserves_inquiry_policy_integration_when_later_owner_work_is_selected() -> None:
    status = STATUS.read_text(encoding="utf-8")

    assert "Policy Hierarchy Completion v0" in status
    assert "Issue #399" in status
    assert "Inquiry Policy v0" in status
    assert "Metareasoning Policy v0" in status
    assert "Exploration Policy v0" in status
    assert "Warrant / Choice Policy v0" in status
    assert "COMPOSABLE POLICY PROGRAM = POLICY_HIERARCHY_COMPLETION_V0" in status
    assert "EXPERIMENT PREREQUISITE = NONE" in status
    assert "Do **not** freeze RC3" in status


def test_policy_hierarchy_does_not_create_runtime_or_schema_surface() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    release = (ROOT / "release-v1.0.yaml").read_text(encoding="utf-8")

    assert "policy_hierarchy" not in pyproject
    assert "inquiry_policy" not in pyproject
    assert "metareasoning_policy" not in pyproject
    assert "exploration_policy" not in pyproject
    assert "warrant_choice_policy" not in pyproject
    assert "WarrantEngine" not in pyproject
    assert "SearchState" not in pyproject
    assert 'schema_version: "2"' in release
