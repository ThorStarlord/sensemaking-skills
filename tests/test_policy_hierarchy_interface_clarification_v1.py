"""Contract checks for Issue #426 policy-interface clarification.

These tests protect ownership/boundary semantics and integration references. They do
not establish empirical usefulness or semantic optimality.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UMBRELLA = ROOT / "docs" / "adaptive-semantic-control-architecture-v0.md"
README = ROOT / "README.md"
CONTEXT = ROOT / "CONTEXT.md"
GETTING_STARTED = ROOT / "GETTING_STARTED.md"


def test_navigation_surfaces_reference_the_crosswalk() -> None:
    assert UMBRELLA.exists()
    for path in (README, CONTEXT, GETTING_STARTED):
        text = path.read_text(encoding="utf-8")
        assert "adaptive-semantic-control-architecture-v0.md" in text


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
