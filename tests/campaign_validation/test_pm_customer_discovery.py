"""Qualification tests for the PM Customer Discovery vertical slice."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from sensemaking_skills import setup_skills as setup_skills_module
from sensemaking_skills.campaign_semantics import CampaignState
from sensemaking_skills.campaigns import (
    ArtifactAdmissionService,
    ArtifactValidationRejectedError,
    CampaignService,
)
from sensemaking_skills.campaigns.capabilities import load_capability_registry

REPO_ROOT = Path(__file__).resolve().parents[2]
PM_IDS = (
    "persona_definition",
    "discovery_findings",
    "synthesis_report",
    "opportunity_map",
    "hypothesis_statement",
)
PM_SKILLS = ("persona", "discovery", "interview-synthesis", "opportunity-tree", "hypothesis")
SECTIONS = {
    "persona_definition": ("Persona summary", "Context and profile", "Jobs to Be Done", "Pains and desired outcomes", "Current solutions and behaviors", "Evidence and confidence", "Assumptions and research gaps"),
    "discovery_findings": ("Problem framing", "Existing evidence", "Hypotheses and uncertainties", "Learning plan", "Decision criteria", "Unresolved questions"),
    "synthesis_report": ("Research context and sources", "Jobs to Be Done", "Behavioral patterns", "Problems and contradictions", "Evidence excerpts", "Implications and next research"),
    "opportunity_map": ("Desired outcome", "Opportunities", "Opportunity comparison", "Candidate solutions and risky assumptions", "Learning tests", "Recommended branch"),
    "hypothesis_statement": ("Hypothesis", "Context and evidence", "Target and expected behavior", "Measures and thresholds", "Risk assumptions", "Validation approach", "Success, pivot, and kill criteria"),
}


def _router_module():
    path = REPO_ROOT / "scripts" / "validate-and-report.py"
    spec = importlib.util.spec_from_file_location("pm_validate_and_report", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _data(artifact_id: str) -> dict:
    if artifact_id == "persona_definition":
        return {"artifact_id": artifact_id, "schema_version": "1", "persona_id": "persona-1", "status": "provisional", "segment": "serial authors", "primary_job": "maintain long-horizon narrative intent", "evidence_refs": [], "assumptions": [], "unresolved_questions": []}
    if artifact_id == "discovery_findings":
        return {"artifact_id": artifact_id, "schema_version": "1", "problem_statement": "authors lose long-horizon intent across a series", "hypotheses": [{"id": "H-1", "statement": "state fragmentation contributes to drift", "status": "untested", "evidence_refs": [], "learning_method": "inspect supplied evidence", "decision_criterion": "evidence changes whether continuity memory is prioritized"}], "unresolved_questions": []}
    if artifact_id == "synthesis_report":
        return {"artifact_id": artifact_id, "schema_version": "1", "source_interviews": ["interview-1"], "findings": [{"id": "F-1", "statement": "the respondent reports continuity recovery work", "source_refs": ["interview-1"], "frequency": {"count": 1, "total": 1}, "confidence": "low"}], "contradictions": [], "unresolved_questions": []}
    if artifact_id == "opportunity_map":
        return {"artifact_id": artifact_id, "schema_version": "1", "desired_outcome": {"statement": "reduce continuity recovery effort", "metric": None, "baseline": None, "target": None}, "opportunities": [{"id": "O-1", "statement": "make durable narrative state easier to reconstruct", "status": "assumption", "evidence_refs": [], "importance": 5, "satisfaction": 2, "score": 3}], "recommended_branch": None, "unresolved_questions": []}
    return {"artifact_id": artifact_id, "schema_version": "1", "hypothesis_id": "HYP-1", "target_segment": "serial authors", "problem_or_opportunity": "continuity reconstruction is expensive", "intervention": "surface durable series context", "expected_outcome": "authors spend less effort recovering context", "primary_measure": "context-recovery effort", "success_criterion": "observed recovery effort decreases", "kill_criterion": "recovery effort does not improve enough to justify complexity", "evidence_refs": [], "assumptions": ["recovery effort is consequential"], "validation_method": "bounded prototype evaluation", "status": "proposed"}


def _write_artifact(tmp_path: Path, artifact_id: str, data: dict | None = None) -> Path:
    payload = data or _data(artifact_id)
    prose = [f"# {artifact_id}", ""]
    for section in SECTIONS[artifact_id]:
        prose.extend([f"## {section}", "Fixture content.", ""])
    prose.extend(["## Machine-readable handoff", "```yaml", yaml.safe_dump(payload, sort_keys=False).rstrip(), "```", ""])
    path = tmp_path / f"{artifact_id}.md"
    path.write_text("\n".join(prose), encoding="utf-8")
    return path


def _route(path: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
    completed = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate-and-report.py"), str(path), "--repo-root", str(REPO_ROOT)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed, json.loads(completed.stdout)


def test_router_selects_pm_validator_for_exact_pilot_artifacts() -> None:
    router = _router_module()
    for artifact_id in PM_IDS:
        assert router.select_validator(artifact_id) == "scripts/validate-pm-artifact.py"
    assert router.select_validator("session_summary") == "scripts/validate-artifact.py"


@pytest.mark.parametrize("artifact_id", PM_IDS)
def test_valid_pm_artifact_routes_through_specialized_validator(tmp_path: Path, artifact_id: str) -> None:
    path = _write_artifact(tmp_path, artifact_id)
    completed, payload = _route(path)
    assert completed.returncode == 0, completed.stderr + completed.stdout
    assert payload["valid"] is True
    assert payload["artifact_id"] == artifact_id
    assert payload["validator"] == "validate-pm-artifact.py"


def test_persona_rejects_empirical_status_without_evidence(tmp_path: Path) -> None:
    data = _data("persona_definition")
    data["status"] = "evidence_backed"
    path = _write_artifact(tmp_path, "persona_definition", data)
    completed, payload = _route(path)
    assert completed.returncode == 1
    assert any(e["error_id"] == "PM_EVIDENCE_REQUIRED" for e in payload["errors"])


def test_discovery_rejects_validated_status_that_the_contract_does_not_authorize(tmp_path: Path) -> None:
    data = _data("discovery_findings")
    data["hypotheses"][0]["status"] = "validated"
    path = _write_artifact(tmp_path, "discovery_findings", data)
    completed, payload = _route(path)
    assert completed.returncode == 1
    assert any(e["error_id"] == "PM_INVALID_STATUS" for e in payload["errors"])


def test_synthesis_rejects_unresolved_source_and_impossible_frequency(tmp_path: Path) -> None:
    data = _data("synthesis_report")
    data["findings"][0]["source_refs"] = ["missing-interview"]
    data["findings"][0]["frequency"] = {"count": 2, "total": 1}
    path = _write_artifact(tmp_path, "synthesis_report", data)
    completed, payload = _route(path)
    assert completed.returncode == 1
    codes = {e["error_id"] for e in payload["errors"]}
    assert {"PM_UNKNOWN_SOURCE_REF", "PM_INVALID_FREQUENCY"}.issubset(codes)


def test_opportunity_rejects_score_not_derived_from_declared_inputs(tmp_path: Path) -> None:
    data = _data("opportunity_map")
    data["opportunities"][0]["score"] = 4.9
    path = _write_artifact(tmp_path, "opportunity_map", data)
    completed, payload = _route(path)
    assert completed.returncode == 1
    assert any(e["error_id"] == "PM_SCORE_MISMATCH" for e in payload["errors"])


def test_hypothesis_rejects_result_status_without_result_evidence_contract(tmp_path: Path) -> None:
    data = _data("hypothesis_statement")
    data["status"] = "passed"
    path = _write_artifact(tmp_path, "hypothesis_statement", data)
    completed, payload = _route(path)
    assert completed.returncode == 1
    assert any(e["error_id"] == "PM_INVALID_STATUS" for e in payload["errors"])


def test_campaign_admission_binds_specialized_pm_validator(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(CampaignState(campaign_id="CMP-PM", mission="prove PM artifact admission", status="active", current_state="initialized"))
    artifact = _write_artifact(tmp_path, "persona_definition")
    result = ArtifactAdmissionService(workspace).admit(artifact, framework_root=REPO_ROOT)
    assert result.artifact_id == "persona_definition"
    assert result.admission.validator == "validate-pm-artifact.py"
    assert result.validation_result["valid"] is True
    assert result.artifact_ref in set(ArtifactAdmissionService(workspace).store.evidence_refs())


def test_campaign_admission_rejects_invalid_pm_artifact(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(CampaignState(campaign_id="CMP-PM-REJECT", mission="prove PM admission fails closed", status="active", current_state="initialized"))
    data = _data("persona_definition")
    data["status"] = "evidence_backed"
    artifact = _write_artifact(tmp_path, "persona_definition", data)
    with pytest.raises(ArtifactValidationRejectedError):
        ArtifactAdmissionService(workspace).admit(artifact, framework_root=REPO_ROOT)


def test_campaign_catalog_exposes_pilot_as_unranked_declared_capabilities() -> None:
    registry = load_capability_registry()
    expected = {
        "persona": ("customer_understanding", "persona_definition"),
        "discovery": ("problem_discovery", "discovery_findings"),
        "interview-synthesis": ("research_synthesis", "synthesis_report"),
        "opportunity-tree": ("opportunity_mapping", "opportunity_map"),
        "hypothesis": ("product_hypothesis", "hypothesis_statement"),
    }
    for capability_id, (responsibility_type, output) in expected.items():
        item = registry.get(capability_id)
        assert item is not None
        assert item.kind == "skill"
        assert item.capability.accepted_responsibility_types == (responsibility_type,)
        assert item.capability.output_artifact == output
        assert item.mutates_repository is False
        assert item.returns_control is True


def test_same_canonical_pm_skill_bytes_are_installed_to_multiple_harness_roots(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = REPO_ROOT / "skills"
    monkeypatch.setattr(setup_skills_module, "get_package_skills_dir", lambda: source)
    project = tmp_path / "project"
    project.mkdir()
    assert setup_skills_module.setup_skills(target="all", scope="project", project_root=project)
    roots = (project / ".agents" / "skills", project / ".claude" / "skills", project / ".opencode" / "skills")
    for skill in PM_SKILLS:
        canonical = (source / skill / "SKILL.md").read_bytes()
        for root in roots:
            assert (root / skill / "SKILL.md").read_bytes() == canonical
            assert (root / skill / "references" / "output-contract.md").read_bytes() == (source / skill / "references" / "output-contract.md").read_bytes()
