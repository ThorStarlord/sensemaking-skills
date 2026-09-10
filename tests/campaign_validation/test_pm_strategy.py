"""Repository qualification tests for PM strategy and prioritization."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from sensemaking_skills.campaign_semantics import CampaignState
from sensemaking_skills.campaigns import ArtifactAdmissionService, CampaignService
from sensemaking_skills.campaigns.capabilities import load_capability_registry

REPO_ROOT = Path(__file__).resolve().parents[2]
IDS = ("market_analysis", "strategy_doc", "prioritized_list", "north_star_metric", "okr_list", "roadmap", "business_canvas")
SECTIONS = {
    "market_analysis": ("Scope and evidence cutoff", "Competitors and sources", "Comparison", "Strengths weaknesses gaps and threats", "Positioning options", "Recommendations and uncertainties"),
    "strategy_doc": ("Vision and context", "Target segments and non-targets", "Problems and evidence", "Strategic choices and non-choices", "Differentiation and business model", "Measures and roadmap themes", "Risks dependencies and open decisions"),
    "prioritized_list": ("Decision context", "Candidate evidence and scoring", "Recommended order and trade-offs", "Dependencies and validation needs", "Deferred items"),
    "north_star_metric": ("Value model and evidence", "Candidate metrics", "Candidate assessment", "Proposed North Star", "Input metrics and guardrails", "Measurement gaps and review cadence"),
    "okr_list": ("Strategy and cycle", "Objectives and key results", "Alignment", "Supporting initiatives", "Review cadence", "Uncertainties"),
    "roadmap": ("Goals and planning assumptions", "Themes and initiatives", "Dependencies and sequence", "Milestones and outcomes", "Capacity and contingency", "Review triggers and uncertainties"),
    "business_canvas": ("Canvas", "Evidence and assumptions", "Critical hypotheses", "Validation order", "Unknowns and limitations"),
}


def data(artifact_id: str) -> dict:
    if artifact_id == "market_analysis":
        return {"artifact_id": artifact_id, "schema_version": "1", "evidence_cutoff": "2026-09-10", "product": "Example", "segment": "teams", "competitors": [{"id": "COMP-1", "name": "Alternative", "claims": [{"dimension": "pricing", "value": "public price", "evidence_status": "observed", "source_refs": ["source-1"], "observed_at": "2026-09-10"}]}], "gaps": [], "positioning_options": [], "recommendations": [], "unresolved_questions": []}
    if artifact_id == "strategy_doc":
        return {"artifact_id": artifact_id, "schema_version": "1", "status": "proposed", "vision": "Durable product reasoning", "target_segments": ["teams"], "non_targets": [], "problem_refs": ["problem-1"], "choices": [{"id": "CHOICE-1", "statement": "focus", "rationale": "evidence", "evidence_refs": ["problem-1"]}], "non_choices": [], "differentiation_hypotheses": [], "monetization_hypotheses": [], "measures": [{"name": "successful resumes", "baseline": None, "target": "increase", "evidence_status": "proposed", "evidence_refs": []}], "roadmap_themes": [], "risks": [], "assumptions": [], "unresolved_questions": []}
    if artifact_id == "prioritized_list":
        return {"artifact_id": artifact_id, "schema_version": "1", "scoring_method": "rice", "goal_refs": ["goal-1"], "items": [{"id": "ITEM-1", "statement": "improve resume", "reach": 10, "impact": 2, "confidence": 0.5, "effort": 2, "score": 5.0, "evidence_refs": ["goal-1"], "dependencies": [], "decision": "now", "rationale": "best current fit"}], "recommended_order": ["ITEM-1"], "unresolved_questions": []}
    if artifact_id == "north_star_metric":
        scores = {"understandable": 5, "customer_centric": 5, "sustainable_value": 4, "vision_alignment": 5, "quantitative": 4, "actionable": 4, "leading_indicator": 3}
        return {"artifact_id": artifact_id, "schema_version": "1", "status": "proposed", "business_game": "productivity", "candidates": [{"id": "NSM-1", "name": "Useful Resumes", "definition": "successful durable resumes", "scores": scores, "rationale": "value delivery"}], "selected_candidate_id": "NSM-1", "baseline": {"value": None, "evidence_status": "unknown", "evidence_refs": []}, "targets": [], "input_metrics": [], "guardrails": [], "unresolved_questions": []}
    if artifact_id == "okr_list":
        return {"artifact_id": artifact_id, "schema_version": "1", "status": "proposed", "cycle": "next", "strategy_refs": ["strategy-1"], "objectives": [{"id": "OBJ-1", "statement": "Make durable continuation reliable", "owner_role": "product lead", "aligns_to": ["strategy-1"], "key_results": [{"id": "KR-1", "measure": "successful fresh-context resumes", "result_type": "outcome", "baseline": None, "baseline_status": "unknown", "baseline_evidence_refs": [], "target": "increase", "target_status": "proposed"}], "initiatives": []}], "review_cadence": "monthly", "unresolved_questions": []}
    if artifact_id == "roadmap":
        return {"artifact_id": artifact_id, "schema_version": "1", "status": "proposed", "period": "next", "goal_refs": ["goal-1"], "initiatives": [{"id": "INIT-1", "theme": "durability", "statement": "improve resume", "source_priority_refs": ["ITEM-1"], "dependencies": [], "timing": None, "timing_status": "unknown", "authority_ref": None, "expected_outcomes": ["better continuation"], "confidence": "medium"}], "milestones": [], "capacity_assumptions": [], "review_triggers": [], "unresolved_questions": []}
    blocks = {name: {"value": [], "evidence_status": "hypothesis", "evidence_refs": []} for name in ("problem", "solution", "unique_value_proposition", "unfair_advantage", "customer_segments", "channels", "revenue_streams", "cost_structure", "key_metrics")}
    blocks["unique_value_proposition"]["value"] = "Durable sensemaking"
    blocks["unfair_advantage"]["value"] = "unknown"
    return {"artifact_id": artifact_id, "schema_version": "1", "status": "hypothesis", "blocks": blocks, "critical_hypotheses": [{"id": "H-1", "statement": "durability matters", "risk": "high", "evidence_refs": [], "validation_method": "dogfood"}], "unresolved_questions": []}


def write(tmp_path: Path, artifact_id: str, payload: dict | None = None) -> Path:
    parts = [f"# {artifact_id}", ""]
    for section in SECTIONS[artifact_id]:
        parts += [f"## {section}", "Fixture.", ""]
    parts += ["## Machine-readable handoff", "```yaml", yaml.safe_dump(payload or data(artifact_id), sort_keys=False).rstrip(), "```", ""]
    path = tmp_path / f"{artifact_id}.md"
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def route(path: Path) -> tuple[int, dict]:
    cp = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "validate-and-report.py"), str(path), "--repo-root", str(REPO_ROOT)], cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    return cp.returncode, json.loads(cp.stdout)


def router_module():
    path = REPO_ROOT / "scripts" / "validate-and-report.py"
    spec = importlib.util.spec_from_file_location("pm_strategy_router", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_router_maps_all_strategy_artifacts() -> None:
    router = router_module()
    for artifact_id in IDS:
        assert router.select_validator(artifact_id) == "scripts/validate-pm-strategy.py"


@pytest.mark.parametrize("artifact_id", IDS)
def test_valid_strategy_artifacts_pass(tmp_path: Path, artifact_id: str) -> None:
    code, payload = route(write(tmp_path, artifact_id))
    assert code == 0, payload
    assert payload["valid"] is True
    assert payload["validator"] == "validate-pm-strategy.py"


def test_observed_competitor_claim_requires_source(tmp_path: Path) -> None:
    payload = data("market_analysis")
    payload["competitors"][0]["claims"][0]["source_refs"] = []
    code, result = route(write(tmp_path, "market_analysis", payload))
    assert code == 1
    assert any(e["error_id"] == "PM_EVIDENCE_REQUIRED" for e in result["errors"])


def test_strategy_cannot_self_ratify(tmp_path: Path) -> None:
    payload = data("strategy_doc"); payload["status"] = "approved"
    code, result = route(write(tmp_path, "strategy_doc", payload))
    assert code == 1
    assert any(e["error_id"] == "PM_INVALID_STATUS" for e in result["errors"])


def test_rice_arithmetic_is_checked_not_used_as_router(tmp_path: Path) -> None:
    payload = data("prioritized_list"); payload["items"][0]["score"] = 99
    code, result = route(write(tmp_path, "prioritized_list", payload))
    assert code == 1
    assert any(e["error_id"] == "PM_SCORE_MISMATCH" for e in result["errors"])


def test_observed_north_star_baseline_requires_evidence(tmp_path: Path) -> None:
    payload = data("north_star_metric"); payload["baseline"] = {"value": 10, "evidence_status": "observed", "evidence_refs": []}
    code, result = route(write(tmp_path, "north_star_metric", payload))
    assert code == 1
    assert any(e["error_id"] == "PM_EVIDENCE_REQUIRED" for e in result["errors"])


def test_okr_rejects_output_as_key_result(tmp_path: Path) -> None:
    payload = data("okr_list"); payload["objectives"][0]["key_results"][0]["result_type"] = "output"
    code, result = route(write(tmp_path, "okr_list", payload))
    assert code == 1
    assert any(e["error_id"] == "PM_OUTPUT_NOT_OUTCOME" for e in result["errors"])


def test_committed_roadmap_timing_requires_authority(tmp_path: Path) -> None:
    payload = data("roadmap"); payload["initiatives"][0]["timing_status"] = "committed"; payload["initiatives"][0]["timing"] = "2027-Q1"
    code, result = route(write(tmp_path, "roadmap", payload))
    assert code == 1
    assert any(e["error_id"] == "PM_AUTHORITY_REQUIRED" for e in result["errors"])


def test_canvas_cannot_self_declare_validation(tmp_path: Path) -> None:
    payload = data("business_canvas"); payload["status"] = "validated"
    code, result = route(write(tmp_path, "business_canvas", payload))
    assert code == 1
    assert any(e["error_id"] == "PM_INVALID_STATUS" for e in result["errors"])


def test_campaign_admission_binds_strategy_validator(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(CampaignState(campaign_id="CMP-PM-W3", mission="qualify strategy admission", status="active", current_state="initialized"))
    result = ArtifactAdmissionService(workspace).admit(write(tmp_path, "strategy_doc"), framework_root=REPO_ROOT)
    assert result.admission.validator == "validate-pm-strategy.py"
    assert result.validation_result["valid"] is True


def test_campaign_catalog_exposes_wave3_unranked() -> None:
    registry = load_capability_registry()
    expected = {
        "competitive-analysis": ("market_understanding", "market_analysis"),
        "strategy": ("product_strategy", "strategy_doc"),
        "prioritize": ("prioritization", "prioritized_list"),
        "north-star": ("product_strategy", "north_star_metric"),
        "okr": ("product_strategy", "okr_list"),
        "roadmap": ("product_strategy", "roadmap"),
        "lean-canvas": ("product_strategy", "business_canvas"),
    }
    for capability_id, (responsibility, output) in expected.items():
        item = registry.get(capability_id)
        assert item is not None
        assert item.capability.accepted_responsibility_types == (responsibility,)
        assert item.capability.output_artifact == output
        assert item.mutates_repository is False
        assert item.returns_control is True
    product_strategy_ids = {x.capability.id for x in registry.candidates("product_strategy")}
    assert {"strategy", "north-star", "okr", "roadmap", "lean-canvas"}.issubset(product_strategy_ids)
