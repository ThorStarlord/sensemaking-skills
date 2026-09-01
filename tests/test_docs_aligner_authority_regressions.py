"""Regression fixtures for docs-aligner authority/currentness hardening (Hybrid C).

C6 — prior-adjudication fixture: provisional workflow_orchestration_plan omitting
     diagnosis-dependent fields must NOT be emitted as confirmed contradiction when
     ADR 0025 Accepted + artifact-contracts note explicitly documents the exception.

C5 — incomplete absence-search fixture: asserting MODEL_WARRANT "not wired"
     into scripts/workflow-runtime.py is invalid when search scope excluded scripts/.

These are reusable behavior tests for the narrow pre-classification + negative-evidence
rules added to skills/docs-aligner/SKILL.md (step 3b, rules 7-8). They characterize
repository reality so a future docs-aligner run can be scored against them.
"""

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_c6_prior_adjudication_positive():
    adr = REPO / "docs/adr/0025-workflow-orchestration-plan-lifecycle.md"
    assert adr.exists(), "ADR 0025 must exist for C6 fixture"
    text = adr.read_text(encoding="utf-8", errors="ignore")
    assert "ACCEPTED" in text
    assert "Two-stage orchestration-plan lifecycle is approved" in text
    assert "provisional execution skeleton" in text

    contract = REPO / "skills/workflow-planner/references/artifact-contracts.yaml"
    assert contract.exists()
    ctext = contract.read_text(encoding="utf-8", errors="ignore")
    assert "provisional" in ctext.lower()
    assert "may omit" in ctext.lower() or "may omit `primary_fog_type`" in ctext
    assert "ADR 0025" in ctext

    skill = REPO / "skills/docs-aligner/SKILL.md"
    assert skill.exists()
    stext = skill.read_text(encoding="utf-8", errors="ignore")
    assert "previously_adjudicated" in stext
    assert "Authority/Currentness Triage" in stext


def test_c6_contract_requires_finalized_only():
    contract = REPO / "skills/workflow-planner/references/artifact-contracts.yaml"
    text = contract.read_text(encoding="utf-8", errors="ignore")
    assert "Only the finalized plan is required to satisfy validate-plan.py" in text


def test_c5_incomplete_search_negative_evidence():
    runtime = REPO / "scripts/workflow-runtime.py"
    assert runtime.exists(), "runtime surface must exist for C5 fixture"
    rtext = runtime.read_text(encoding="utf-8", errors="ignore")
    assert "_run_seam_warrant" in rtext, "MODEL_WARRANT seam must be present in runtime (C5 was false positive)"

    skill = REPO / "skills/docs-aligner/SKILL.md"
    stext = skill.read_text(encoding="utf-8", errors="ignore")
    assert "Negative Evidence Discipline" in stext
    assert "Do not assert absence" in stext
    assert "search scope covers every repository surface named by the claim" in stext


def test_c5_reconciliation_disputes_wiring_claim():
    report = REPO / "artifacts/reconciliation_report.md"
    assert report.exists()
    text = report.read_text(encoding="utf-8", errors="ignore")
    assert "C5" in text
    assert "disputed" in text.lower()
    assert "_run_seam_warrant" in text or "scripts/workflow-runtime.py" in text


def test_c2_ownership_ratified_not_implemented():
    recon = REPO / "artifacts/reconciliation_report.md"
    assert recon.exists()
    text = recon.read_text(encoding="utf-8", errors="ignore")
    assert "docs/canonical-vocabulary.yaml" in text
    assert "authored canonical" in text.lower()
    assert "generated" in text.lower()
    assert "semantic-equivalence" in text.lower() or "semantic" in text.lower()


def test_skill_gate_discipline_present():
    skill = REPO / "skills/docs-aligner/SKILL.md"
    text = skill.read_text(encoding="utf-8", errors="ignore")
    assert "gate: none" in text
    assert "review_alignment_report" in text
    assert "Gate Discipline" in text
