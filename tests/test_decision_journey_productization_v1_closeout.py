"""Terminal qualification checks for Issue #432 Decision Journey Productization v1."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "STATUS.md"
HANDOFF = ROOT / "docs" / "decision-journey-productization-v1-handoff.md"
CONTRACT = ROOT / "docs" / "decision-journey-productization-v1.md"


def test_handoff_records_feature_and_integrated_qualification() -> None:
    text = HANDOFF.read_text(encoding="utf-8")
    for value in (
        "#432",
        "#433",
        "56517a2cb24ca163d6b98701989739647731bc7b",
        "13b9404cecd406d676e581504b5e66a10b4fd23e",
        "35526024012",
        "35526024056",
        "35526107299",
        "35526107307",
    ):
        assert value in text
    assert "COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF" in text
    assert "reconstruction != causal truth" in text
    assert "STATUS.md = integrated current Level-3 projection" in text


def test_status_returns_to_normal_use_without_reopening_prior_milestones() -> None:
    status = STATUS.read_text(encoding="utf-8")
    assert "Decision Journey Productization v1 — COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF" in status
    assert "ISSUE_432_DECISION_JOURNEY_PRODUCTIZATION_V1 = COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF" in status
    assert "ISSUE_430_STRATEGIC_CONTINUITY_REFINEMENT_V1 = COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF" in status
    assert "ISSUE_416_STRATEGIC_CONTINUITY_RECONCILIATION_MULTI_REPO_V1 = COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF" in status
    assert "POLICY_HIERARCHY_COMPLETION_V0 = COMPLETE_INTEGRATED_COMPOSABLE" in status
    assert "SYNTHETIC STRATEGICPLANNER TESTING = STOPPED" in status


def test_contract_is_canonical_and_preserves_authority_boundaries() -> None:
    contract = CONTRACT.read_text(encoding="utf-8")
    assert "COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF" in contract
    for phrase in (
        "mechanical reconstruction != causal truth",
        "profile selected by caller != automatic routing",
        "guide suggestion != capability invocation",
        "mechanical composition != product-value proof",
    ):
        assert phrase in contract

    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "StrategicPlanner" not in pyproject
    assert "OuterLoopEngine" not in pyproject
