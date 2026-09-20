"""Terminal qualification checks for Issue #438 Experiment Economy v1."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "STATUS.md"
HANDOFF = ROOT / "docs" / "experiment-economy-proportional-rigor-v1-handoff.md"
ECONOMY = (
    ROOT / "skills" / "using-sensemaking" / "references" / "experiment-economy-v1.md"
)
INQUIRY = ROOT / "skills" / "using-sensemaking" / "references" / "inquiry-policy-v0.md"
METAREASONING = (
    ROOT / "skills" / "using-sensemaking" / "references" / "metareasoning-policy-v0.md"
)
STRATEGIC = ROOT / "skills" / "strategic-repository-analysis" / "SKILL.md"


def test_handoff_records_exact_feature_qualification_and_claim_ceiling() -> None:
    text = HANDOFF.read_text(encoding="utf-8")

    for value in (
        "#438",
        "#439",
        "1c134966901b9be7726b4e07bd23e411baa1d55f",
        "9237320910cd696344482a51fafbe140c3cfcb8f",
        "35539356624",
        "35539356616",
    ):
        assert value in text

    assert "zero file differences" in text
    assert "COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF" in text
    assert "preliminary normal-use evidence" in text
    assert "scientifically demonstrated systematic experiment bias" in text


def test_status_returns_to_normal_use_without_opening_experiment_program() -> None:
    status = STATUS.read_text(encoding="utf-8")

    assert (
        "Issue #438 Experiment Economy & Proportional Rigor v1 "
        "is complete/integrated and in normal-use handoff"
    ) in status
    assert (
        "Issue #435 Strategic Repository Analysis Semantic Grounding v1 "
        "is complete/integrated and in normal-use handoff"
    ) in status
    assert (
        "ISSUE_438_EXPERIMENT_ECONOMY_PROPORTIONAL_RIGOR_V1 "
        "= COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF"
    ) in status
    assert "CURRENT CONSTRUCTION RESPONSIBILITY = NONE" in status
    assert "PRIMARY CONSTRUCTION PROGRAM = NONE" in status
    assert "OPERATING MODE = NORMAL_USE_VALIDATION" in status
    assert "EXPERIMENT PREREQUISITE = NONE" in status
    assert "SYNTHETIC STRATEGICPLANNER TESTING = STOPPED" in status
    assert "NO ACTIVE ISSUE #438 CONSTRUCTION PACKAGE" in status


def test_terminal_guidance_preserves_experiment_economy_boundaries() -> None:
    economy = ECONOMY.read_text(encoding="utf-8")
    inquiry = INQUIRY.read_text(encoding="utf-8")
    meta = METAREASONING.read_text(encoding="utf-8")
    strategic = STRATEGIC.read_text(encoding="utf-8")

    assert "Experiment Warrant Gate" in economy
    assert "Minimum Sufficient Experimental Rigor" in economy
    assert "Confounder Warrant" in economy
    assert "INVESTIGATE\n!= EXPERIMENT" in inquiry
    assert "`ACT` may still dominate" in meta
    assert "research-grade isolation\n!= default product-development evidence" in strategic


def test_closeout_adds_no_experiment_runtime_or_scoring_surface() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    for forbidden in (
        "ExperimentEngine",
        "ExperimentRouter",
        "EvidenceGradeSelector",
        "RigorScore",
    ):
        assert forbidden not in pyproject
