"""Mechanical boundary checks for Adaptive Agency Abstraction Stack v0.

These tests pin representation and integration claims only. They do not prove
semantic correctness, empirical usefulness, or a need for organization runtime.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "docs" / "research" / "adaptive-agency-abstraction-stack-v0.md"
RECONCILIATION = (
    ROOT / "docs" / "research" / "adaptive-agency-abstraction-stack-v0-reconciliation.md"
)
GENERAL = ROOT / "docs" / "research" / "general-agency-model-v0.1.md"
PRACTICAL = (
    ROOT
    / "skills"
    / "using-sensemaking"
    / "references"
    / "practical-agent-architecture-v0.md"
)
HANDOFF = ROOT / "docs" / "adaptive-agency-abstraction-stack-v0-handoff.md"
STATUS = ROOT / "STATUS.md"


def test_abstraction_stack_uses_three_planes_and_separate_promotion_ladder() -> None:
    model = MODEL.read_text(encoding="utf-8")

    for phrase in (
        "Capability Plane",
        "Coordination Plane",
        "Governance / Persistence Plane",
        "Promotion / Evolution Ladder",
        "Root Primitive",
        "Cognitive Operator",
        "Capability / Skill",
        "Organization",
        "Institution",
    ):
        assert phrase in model

    assert "Campaign != Organization" in model
    assert "capability growth != authority growth" in model
    assert "agent-created abstraction != self-granted permission" in model
    assert "repeated successful coordination != automatic canonical promotion" in model


def test_reconciliation_keeps_organization_outside_current_runtime_authority() -> None:
    reconciliation = RECONCILIATION.read_text(encoding="utf-8")

    assert "organization modeled != organization runtime warranted" in reconciliation
    assert "Campaign != Organization" in reconciliation
    assert "ADR 0029" in reconciliation
    assert "RUNTIME_GAP" in reconciliation
    assert "NO_RUNTIME_GAP_ESTABLISHED" in reconciliation


def test_general_and_practical_architecture_reference_the_bounded_model() -> None:
    general = GENERAL.read_text(encoding="utf-8")
    practical = PRACTICAL.read_text(encoding="utf-8")

    assert "Adaptive Agency Abstraction Stack v0" in general
    assert "Organization is not a mandatory lifecycle stage" in general
    assert "Adaptive Agency Abstraction Stack v0" in practical
    assert "Campaign != Organization" in practical
    assert "organization pattern != execution authority" in practical


def test_closeout_returns_to_normal_use_without_product_expansion() -> None:
    handoff = HANDOFF.read_text(encoding="utf-8")
    status = STATUS.read_text(encoding="utf-8")

    assert "NO_RUNTIME_GAP_ESTABLISHED" in handoff
    assert "NO_PRODUCT_BOUNDARY_CHANGE" in handoff
    assert "NORMAL_USE_VALIDATION" in handoff

    assert "Adaptive Agency Abstraction Stack v0" in status
    assert "CURRENT CONSTRUCTION RESPONSIBILITY = NONE" in status
    assert "Level-3 disposition: `NO_CHANGE`" in status
    assert "NORMAL_USE_VALIDATION" in status
