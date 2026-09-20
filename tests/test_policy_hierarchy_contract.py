"""Mechanical contract checks for Policy Hierarchy Completion v0.

These tests verify that canonical policy surfaces and boundary statements remain
present. They do not establish semantic correctness or policy usefulness.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "policy-hierarchy-v0.md"
INQUIRY = ROOT / "skills" / "using-sensemaking" / "references" / "inquiry-policy-v0.md"
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


def test_status_selects_inquiry_policy_as_current_construction_responsibility() -> None:
    status = STATUS.read_text(encoding="utf-8")

    assert "Policy Hierarchy Completion v0" in status
    assert "Issue #399" in status
    assert "CURRENT CONSTRUCTION RESPONSIBILITY = INQUIRY_POLICY_V0" in status
    assert "PRIMARY CONSTRUCTION PROGRAM = POLICY_HIERARCHY_COMPLETION_V0" in status
    assert "SYNTHETIC STRATEGICPLANNER TESTING = STOPPED" in status
    assert "Do **not** freeze RC3" in status


def test_policy_hierarchy_does_not_create_runtime_or_schema_surface() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    release = (ROOT / "release-v1.0.yaml").read_text(encoding="utf-8")

    assert "policy_hierarchy" not in pyproject
    assert "inquiry_policy" not in pyproject
    assert 'schema_version: "2"' in release
