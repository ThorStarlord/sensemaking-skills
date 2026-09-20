"""Contract checks for Issue #426 policy-interface clarification.

These tests protect ownership/boundary semantics and integration references. They do
not establish empirical usefulness or semantic optimality.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UMBRELLA = ROOT / "docs" / "adaptive-semantic-control-architecture-v0.md"
POLICY = ROOT / "docs" / "policy-hierarchy-v0.md"
COORDINATOR = ROOT / "skills" / "using-sensemaking" / "references" / "adaptive-policy-coordinator-v0.md"
USING = ROOT / "skills" / "using-sensemaking" / "SKILL.md"
CONTINUITY = ROOT / "docs" / "strategic-continuity-v1.md"
RECONCILIATION = ROOT / "docs" / "strategic-reconciliation-and-decision-packets-v1.md"
NORMAL_USE = ROOT / "docs" / "research" / "normal-use-evidence-lane.md"
STATUS = ROOT / "STATUS.md"
README = ROOT / "README.md"
CONTEXT = ROOT / "CONTEXT.md"
GETTING_STARTED = ROOT / "GETTING_STARTED.md"


def test_adaptive_semantic_control_is_a_crosswalk_not_new_authority() -> None:
    text = UMBRELLA.read_text(encoding="utf-8")
    for phrase in (
        "descriptive composition model",
        "Policy Hierarchy v0",
        "!= Policy Hierarchy v1",
        "!= new control level",
        "!= runtime",
        "!= authority",
        "Action / Execution",
        "Learning / Reconciliation",
        "Strategic Continuity v1",
    ):
        assert phrase in text
    assert "Action Policy v0" in text
    assert "deliberately **not** promoted" in text


def test_policy_responsibility_matrix_owns_distinct_questions() -> None:
    policy = POLICY.read_text(encoding="utf-8")
    for phrase in (
        "Policy responsibility matrix",
        "Question owned",
        "Explicit activation",
        "Valid zero-work / implicit result",
        "Does **not** own",
        "Typical consumer",
        "Durable surface",
        "Inquiry vs. Metareasoning",
        "Metareasoning `EXPLORE` vs. Exploration Policy",
        "Warrant / Choice vs. authority",
        "Verification vs. Learning / Reconciliation",
    ):
        assert phrase in policy
    assert "Action / Execution != Action Policy v0" in policy
    assert "Adaptive Policy Coordinator != superior policy authority" in policy


def test_strategic_reassessment_bridge_preserves_non_automatic_transitions() -> None:
    texts = "\n".join(
        p.read_text(encoding="utf-8")
        for p in (UMBRELLA, CONTINUITY, RECONCILIATION, USING, COORDINATOR)
    )
    for phrase in (
        "drift detected\n!= strategy invalid",
        "reassessment trigger observed\n!= strategy",
        "REOPEN_STRATEGY\n!= BUILD",
        "THESIS_REVIEW_REQUIRED\n!= thesis ratified",
        "policy disposition\n!= durable companion artifact",
    ):
        assert phrase in texts


def test_normal_use_observes_policy_friction_without_new_experiment_program() -> None:
    normal = NORMAL_USE.read_text(encoding="utf-8")
    assert "Policy-interface friction" in normal
    assert "which policy question became explicit" in normal
    assert "zero-work outcome" in normal
    assert "policy-interface observation" in normal
    assert "synthetic policy episode" in normal
    assert "automatic episode capture" in normal


def test_navigation_surfaces_reference_the_crosswalk() -> None:
    for path in (README, CONTEXT, GETTING_STARTED):
        text = path.read_text(encoding="utf-8")
        assert "adaptive-semantic-control-architecture-v0.md" in text


def test_issue_399_and_416_remain_terminal_while_426_closes_to_normal_use() -> None:
    status = STATUS.read_text(encoding="utf-8")
    assert "Policy Hierarchy Completion v0 — COMPLETE / INTEGRATED / COMPOSABLE" in status
    assert "Strategic Continuity, Reconciliation & Multi-Repository Sensemaking v1 — COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF" in status
    assert "Policy Hierarchy Interface Clarification v1 — COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF" in status
    assert "CURRENT CONSTRUCTION RESPONSIBILITY = NONE" in status
    assert "OPERATING MODE = NORMAL_USE_VALIDATION" in status
    assert "POLICY_HIERARCHY_COMPLETION_V0 = COMPLETE_INTEGRATED_COMPOSABLE" in status
    assert "ISSUE_416_STRATEGIC_CONTINUITY_RECONCILIATION_MULTI_REPO_V1 = COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF" in status
    assert "ISSUE_426_POLICY_HIERARCHY_INTERFACE_CLARIFICATION_V1 = COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF" in status


def test_clarification_does_not_add_semantic_runtime_or_state_schema() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    for prohibited in (
        "ActionPolicy",
        "AdaptiveSemanticControlEngine",
        "PolicyCoordinator",
        "CoordinatorState",
        "OuterLoopEngine",
        "StrategicPlanner",
        "LearningEngine",
        "BeliefState",
        "SearchState",
    ):
        assert prohibited not in pyproject
