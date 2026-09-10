"""Repository qualification tests for PM Launch / GTM / Communication Wave 6."""
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
IDS = (
    "readiness_report",
    "gtm_plan",
    "battlecard",
    "feature_announcement",
    "stakeholder_update",
)
SECTIONS = {
    "readiness_report": (
        "Launch context", "Evidence inventory", "Cross-functional readiness",
        "Launch-blocking conditions", "Go or no-go recommendation",
        "Rollback and monitoring", "Authority and unknowns",
    ),
    "gtm_plan": (
        "Objective and audience", "Evidence and positioning", "Channel strategy",
        "Messaging", "Timeline and coordination", "Metrics and contingencies",
        "Authority and unknowns",
    ),
    "battlecard": (
        "Scope and currentness", "Evidence inventory", "Competitive claims",
        "Comparison and where each side wins", "Objections and discovery questions",
        "Win-loss patterns and unknowns",
    ),
    "feature_announcement": (
        "Audience and release scope", "Source evidence", "Headline and summary",
        "Changes and user value", "Fixes performance and known issues",
        "Coming soon and commitments", "Publication boundary and unknowns",
    ),
    "stakeholder_update": (
        "Audience and currentness", "Executive summary", "Situation and evidence",
        "Analysis and decisions", "Next steps", "Risks and unresolved questions",
        "Distribution boundary",
    ),
}


def payload(artifact_id: str) -> dict:
    if artifact_id == "readiness_report":
        return {
            "artifact_id": artifact_id,
            "schema_version": "1",
            "status": "assessed",
            "launch_scope": "repository-qualified PM capability wave",
            "launch_tier": "tier2",
            "target_window": None,
            "evidence_window": "candidate-head",
            "evidence_refs": ["ci-product"],
            "checks": [{
                "id": "READY-1", "function": "engineering",
                "requirement": "candidate-head product checks pass",
                "criticality": "launch_blocking", "state": "evidence_backed_complete",
                "evidence_refs": ["ci-product"], "note": "exact-head evidence",
            }],
            "recommendation": "go",
            "conditions": [],
            "rollback_triggers": [{"id": "ROLLBACK-1", "statement": "regression appears", "status": "proposed"}],
            "monitoring_requirements": ["preserve exact-head status"],
            "external_launch_authority_ref": None,
            "unresolved_questions": [],
        }
    if artifact_id == "gtm_plan":
        return {
            "artifact_id": artifact_id, "schema_version": "1", "status": "proposed",
            "offer": "agent-agnostic PM capability domain", "target_segment": "product teams",
            "objective": "test repository-qualified positioning", "evidence_window": "2026-Q3",
            "evidence_refs": ["research-1"],
            "positioning_claims": [{
                "id": "GTM-C1", "statement": "the repository exposes agent-agnostic PM skills",
                "evidence_status": "observed", "evidence_refs": ["research-1"],
            }],
            "channels": [{"id": "GTM-CH1", "name": "documentation", "rationale": "reachable controlled surface", "source_claim_refs": ["GTM-C1"], "status": "proposed"}],
            "messages": [{"id": "GTM-M1", "audience": "product teams", "text": "evaluate durable PM workflows", "source_claim_refs": ["GTM-C1"], "status": "proposed"}],
            "metrics": [{
                "id": "GTM-K1", "name": "qualified evaluations", "baseline": None,
                "baseline_status": "unknown", "baseline_evidence_refs": [], "target": 3,
                "target_status": "proposed", "target_authority_ref": None,
            }],
            "timeline": [{
                "id": "GTM-T1", "action": "prepare evaluation materials", "timing": None,
                "commitment_status": "proposed", "authority_ref": None, "external_action": False,
            }],
            "contingencies": [], "external_execution_authority_ref": None,
            "unresolved_questions": [],
        }
    if artifact_id == "battlecard":
        return {
            "artifact_id": artifact_id, "schema_version": "1", "status": "draft",
            "our_product": "Sensemaking Skills", "competitor": "Alternative X", "segment": "agent-native product teams",
            "evidence_cutoff": "2026-09-10", "evidence_refs": ["our-docs", "competitor-source"],
            "claims": [
                {"id": "BC-C1", "side": "us", "statement": "supports durable Campaign state", "evidence_status": "observed", "evidence_refs": ["our-docs"]},
                {"id": "BC-C2", "side": "competitor", "statement": "documents prompt workflows", "evidence_status": "observed", "evidence_refs": ["competitor-source"]},
            ],
            "comparisons": [{
                "id": "BC-X1", "dimension": "durable state", "our_claim_ref": "BC-C1",
                "competitor_claim_ref": "BC-C2", "assessment": "us_advantage", "evidence_status": "inferred",
            }],
            "talk_tracks": [{"id": "BC-T1", "type": "discovery_question", "text": "How do you resume work across sessions?", "source_claim_refs": ["BC-C1", "BC-C2"], "status": "proposed"}],
            "valid_until": None, "unresolved_questions": [],
        }
    if artifact_id == "feature_announcement":
        return {
            "artifact_id": artifact_id, "schema_version": "1", "status": "draft",
            "audience": "repository users", "as_of": "candidate-head",
            "release_evidence_refs": ["merge-evidence"],
            "items": [{
                "id": "ANN-1", "type": "feature", "title": "PM customer modeling",
                "statement": "customer-modeling capabilities are merged", "user_benefit": "more evidence-aware customer analysis",
                "availability": "shipped", "claim_status": "observed", "evidence_refs": ["merge-evidence"],
                "commitment_status": "proposed", "authority_ref": None,
            }],
            "cta": None, "publication_state": "draft", "publication_authority_ref": None,
            "unresolved_questions": [],
        }
    return {
        "artifact_id": artifact_id, "schema_version": "1", "status": "draft",
        "audience": "maintainers", "purpose": "inform", "as_of": "candidate-head",
        "source_refs": ["campaign-state"],
        "claims": [
            {"id": "SU-C1", "statement": "Wave 5 is merged", "epistemic_status": "observed", "evidence_refs": ["campaign-state"], "derivation_rule": None, "authority_ref": None},
            {"id": "SU-C2", "statement": "repository-side PM migration is nearing completion", "epistemic_status": "derived", "evidence_refs": ["campaign-state"], "derivation_rule": "count remaining migration rows", "authority_ref": None},
        ],
        "decisions": [{"id": "SU-D1", "statement": "continue Wave 6", "status": "proposed", "authority_ref": None}],
        "next_steps": [{"id": "SU-N1", "action": "qualify Wave 6", "owner_role": "maintainer", "timing": None, "commitment_status": "proposed", "authority_ref": None}],
        "risks": [{"id": "SU-R1", "statement": "native-harness qualification remains pending", "evidence_status": "observed", "evidence_refs": ["campaign-state"]}],
        "decision_request": None, "publication_state": "draft", "unresolved_questions": [],
    }


def write(tmp_path: Path, artifact_id: str, data: dict | None = None) -> Path:
    parts = [f"# {artifact_id}", ""]
    for section in SECTIONS[artifact_id]:
        parts += [f"## {section}", "Fixture.", ""]
    parts += ["## Machine-readable handoff", "```yaml", yaml.safe_dump(data or payload(artifact_id), sort_keys=False).rstrip(), "```", ""]
    path = tmp_path / f"{artifact_id}.md"
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def route(path: Path) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate-and-report.py"), str(path), "--repo-root", str(REPO_ROOT)],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    )
    return completed.returncode, json.loads(completed.stdout)


def router():
    path = REPO_ROOT / "scripts" / "validate-and-report.py"
    spec = importlib.util.spec_from_file_location("pm_launch_router", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_router_maps_wave6_artifacts() -> None:
    module = router()
    for artifact_id in IDS:
        assert module.select_validator(artifact_id) == "scripts/validate-pm-launch-communication.py"
    assert module.select_validator("ideal_customer_profile") == "scripts/validate-pm-customer-model.py"


@pytest.mark.parametrize("artifact_id", IDS)
def test_valid_wave6_artifacts_pass(tmp_path: Path, artifact_id: str) -> None:
    code, result = route(write(tmp_path, artifact_id))
    assert code == 0, result
    assert result["valid"] is True
    assert result["validator"] == "validate-pm-launch-communication.py"


def test_readiness_completion_requires_evidence(tmp_path: Path) -> None:
    data = payload("readiness_report")
    data["checks"][0]["evidence_refs"] = []
    code, result = route(write(tmp_path, "readiness_report", data))
    assert code == 1
    assert any(e["error_id"] == "PM_EVIDENCE_REQUIRED" for e in result["errors"])


def test_readiness_go_rejects_unresolved_blocker(tmp_path: Path) -> None:
    data = payload("readiness_report")
    data["checks"][0]["state"] = "blocked"
    data["checks"][0]["evidence_refs"] = []
    code, result = route(write(tmp_path, "readiness_report", data))
    assert code == 1
    assert any(e["error_id"] == "PM_BLOCKER_CONFLICT" for e in result["errors"])


def test_gtm_observed_positioning_requires_evidence(tmp_path: Path) -> None:
    data = payload("gtm_plan")
    data["positioning_claims"][0]["evidence_refs"] = []
    code, result = route(write(tmp_path, "gtm_plan", data))
    assert code == 1
    assert any(e["error_id"] == "PM_EVIDENCE_REQUIRED" for e in result["errors"])


def test_gtm_ratified_timeline_requires_authority(tmp_path: Path) -> None:
    data = payload("gtm_plan")
    data["timeline"][0]["commitment_status"] = "ratified"
    code, result = route(write(tmp_path, "gtm_plan", data))
    assert code == 1
    assert any(e["error_id"] == "PM_AUTHORITY_REQUIRED" for e in result["errors"])


def test_battlecard_observed_competitor_claim_requires_evidence(tmp_path: Path) -> None:
    data = payload("battlecard")
    data["claims"][1]["evidence_refs"] = []
    code, result = route(write(tmp_path, "battlecard", data))
    assert code == 1
    assert any(e["error_id"] == "PM_EVIDENCE_REQUIRED" for e in result["errors"])


def test_battlecard_comparison_enforces_claim_side(tmp_path: Path) -> None:
    data = payload("battlecard")
    data["comparisons"][0]["our_claim_ref"] = "BC-C2"
    code, result = route(write(tmp_path, "battlecard", data))
    assert code == 1
    assert any(e["error_id"] == "PM_REF_TYPE_MISMATCH" for e in result["errors"])


def test_release_notes_cannot_claim_shipped_without_evidence(tmp_path: Path) -> None:
    data = payload("feature_announcement")
    data["items"][0]["evidence_refs"] = []
    code, result = route(write(tmp_path, "feature_announcement", data))
    assert code == 1
    codes = {e["error_id"] for e in result["errors"]}
    assert "PM_RELEASE_EVIDENCE_REQUIRED" in codes


def test_release_notes_cannot_claim_publication(tmp_path: Path) -> None:
    data = payload("feature_announcement")
    data["publication_state"] = "published"
    code, result = route(write(tmp_path, "feature_announcement", data))
    assert code == 1
    assert any(e["error_id"] == "PM_EXTERNAL_ACTION_STATE" for e in result["errors"])


def test_stakeholder_derived_claim_requires_rule(tmp_path: Path) -> None:
    data = payload("stakeholder_update")
    data["claims"][1]["derivation_rule"] = None
    code, result = route(write(tmp_path, "stakeholder_update", data))
    assert code == 1
    assert any(e["error_id"] == "PM_DERIVATION_REQUIRED" for e in result["errors"])


def test_stakeholder_ratified_decision_requires_authority(tmp_path: Path) -> None:
    data = payload("stakeholder_update")
    data["decisions"][0]["status"] = "ratified"
    code, result = route(write(tmp_path, "stakeholder_update", data))
    assert code == 1
    assert any(e["error_id"] == "PM_AUTHORITY_REQUIRED" for e in result["errors"])


def test_stakeholder_decision_request_requires_concrete_request(tmp_path: Path) -> None:
    data = payload("stakeholder_update")
    data["purpose"] = "decision_request"
    code, result = route(write(tmp_path, "stakeholder_update", data))
    assert code == 1
    assert any(e["error_id"] == "PM_DECISION_REQUEST_REQUIRED" for e in result["errors"])


def test_campaign_admission_binds_wave6_validator(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(CampaignState(campaign_id="CMP-PM-W6", mission="qualify PM communication", status="active", current_state="initialized"))
    result = ArtifactAdmissionService(workspace).admit(write(tmp_path, "stakeholder_update"), framework_root=REPO_ROOT)
    assert result.artifact_id == "stakeholder_update"
    assert result.admission.validator == "validate-pm-launch-communication.py"
    assert result.validation_result["valid"] is True


def test_campaign_catalog_exposes_wave6_without_external_mutation_authority() -> None:
    registry = load_capability_registry()
    expected = {
        "launch-checklist": ("risk_and_readiness", "readiness_report"),
        "gtm": ("commercial_strategy", "gtm_plan"),
        "battlecard": ("commercial_strategy", "battlecard"),
        "release-notes": ("communication", "feature_announcement"),
        "stakeholder-update": ("communication", "stakeholder_update"),
    }
    for capability_id, (responsibility, output) in expected.items():
        item = registry.get(capability_id)
        assert item is not None
        assert item.capability.accepted_responsibility_types == (responsibility,)
        assert item.capability.output_artifact == output
        assert item.mutates_repository is False
        assert item.returns_control is True
