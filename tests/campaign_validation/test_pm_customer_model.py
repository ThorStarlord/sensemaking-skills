"""Repository qualification tests for PM Customer Modeling Wave 5."""
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
IDS = ("journey_map", "ideal_customer_profile")
SECTIONS = {
    "journey_map": (
        "Persona and scope",
        "Evidence inventory",
        "Journey stages",
        "Critical moments",
        "Opportunities and unknowns",
    ),
    "ideal_customer_profile": (
        "Scope and evidence",
        "Profile",
        "Behaviors and buying context",
        "Jobs needs and pains",
        "Ideal-of-ideal and disqualifiers",
        "GTM implications",
        "Validation gaps",
    ),
}


def payload(artifact_id: str) -> dict:
    if artifact_id == "journey_map":
        return {
            "artifact_id": artifact_id,
            "schema_version": "1",
            "status": "mixed",
            "persona_ref": "PERSONA-1",
            "scope": "onboarding",
            "evidence_window": "2026-Q3",
            "evidence_refs": ["interview-1"],
            "stages": [
                {
                    "id": "STAGE-1",
                    "name": "Onboarding",
                    "order": 1,
                    "touchpoints": ["first login"],
                    "actions": ["attempt first task"],
                    "questions": ["what should I do first?"],
                    "emotions": [
                        {
                            "value": "uncertain",
                            "evidence_status": "observed",
                            "evidence_refs": ["interview-1"],
                        }
                    ],
                    "pain_points": ["unclear starting point"],
                    "opportunities": ["make the next action explicit"],
                    "metrics": [
                        {
                            "name": "completion_rate",
                            "value": None,
                            "evidence_status": "unknown",
                            "evidence_refs": [],
                        }
                    ],
                }
            ],
            "critical_moments": [
                {
                    "id": "MOMENT-1",
                    "type": "aha",
                    "stage_ref": "STAGE-1",
                    "statement": "completing the first useful task may establish value",
                    "evidence_status": "hypothesis",
                    "evidence_refs": [],
                }
            ],
            "recommendations": [],
            "unresolved_questions": [],
        }
    return {
        "artifact_id": artifact_id,
        "schema_version": "1",
        "status": "mixed",
        "segment": "B2B product teams",
        "evidence_window": "2026-Q3",
        "evidence_refs": ["cohort-1"],
        "profile_claims": [
            {
                "id": "ICP-C1",
                "dimension": "team_context",
                "value": "cross-functional product team",
                "evidence_status": "observed",
                "evidence_refs": ["cohort-1"],
            }
        ],
        "behaviors": [
            {
                "id": "ICP-B1",
                "statement": "prefers reusable durable context",
                "evidence_status": "hypothesis",
                "evidence_refs": [],
            }
        ],
        "jobs": [
            {
                "id": "ICP-J1",
                "statement": "preserve product decision context across sessions",
                "evidence_status": "hypothesis",
                "evidence_refs": [],
            }
        ],
        "pains": [
            {
                "id": "ICP-P1",
                "statement": "reconstructing prior decisions is costly",
                "evidence_status": "hypothesis",
                "evidence_refs": [],
            }
        ],
        "ideal_indicators": [
            {
                "id": "ICP-I1",
                "statement": "frequent multi-session product work",
                "evidence_status": "hypothesis",
                "evidence_refs": [],
            }
        ],
        "disqualifiers": [
            {
                "id": "ICP-D1",
                "type": "soft",
                "statement": "single-session work with no continuity need",
                "evidence_status": "hypothesis",
                "evidence_refs": [],
            }
        ],
        "gtm_implications": [
            {
                "id": "ICP-G1",
                "function": "product",
                "recommendation": "test durable-context value with cross-functional teams",
                "source_claim_refs": ["ICP-C1"],
                "status": "proposed",
            }
        ],
        "unresolved_questions": [],
    }


def write(tmp_path: Path, artifact_id: str, data: dict | None = None) -> Path:
    parts = [f"# {artifact_id}", ""]
    for section in SECTIONS[artifact_id]:
        parts += [f"## {section}", "Fixture.", ""]
    parts += [
        "## Machine-readable handoff",
        "```yaml",
        yaml.safe_dump(data or payload(artifact_id), sort_keys=False).rstrip(),
        "```",
        "",
    ]
    path = tmp_path / f"{artifact_id}.md"
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def route(path: Path) -> tuple[int, dict]:
    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate-and-report.py"),
            str(path),
            "--repo-root",
            str(REPO_ROOT),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.returncode, json.loads(completed.stdout)


def router():
    path = REPO_ROOT / "scripts" / "validate-and-report.py"
    spec = importlib.util.spec_from_file_location("pm_customer_model_router", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_router_maps_customer_model_artifacts() -> None:
    module = router()
    for artifact_id in IDS:
        assert module.select_validator(artifact_id) == "scripts/validate-pm-customer-model.py"
    assert module.select_validator("pricing_model") == "scripts/validate-pm-measurement.py"


@pytest.mark.parametrize("artifact_id", IDS)
def test_valid_customer_model_artifacts_pass(tmp_path: Path, artifact_id: str) -> None:
    code, result = route(write(tmp_path, artifact_id))
    assert code == 0, result
    assert result["valid"] is True
    assert result["artifact_id"] == artifact_id
    assert result["validator"] == "validate-pm-customer-model.py"


def test_journey_observed_emotion_requires_evidence(tmp_path: Path) -> None:
    data = payload("journey_map")
    data["stages"][0]["emotions"][0]["evidence_refs"] = []
    code, result = route(write(tmp_path, "journey_map", data))
    assert code == 1
    assert any(error["error_id"] == "PM_EVIDENCE_REQUIRED" for error in result["errors"])


def test_journey_observed_metric_requires_evidence(tmp_path: Path) -> None:
    data = payload("journey_map")
    data["stages"][0]["metrics"][0].update(
        value=0.42, evidence_status="observed", evidence_refs=[]
    )
    code, result = route(write(tmp_path, "journey_map", data))
    assert code == 1
    assert any(error["error_id"] == "PM_EVIDENCE_REQUIRED" for error in result["errors"])


def test_journey_critical_moment_must_reference_known_stage(tmp_path: Path) -> None:
    data = payload("journey_map")
    data["critical_moments"][0]["stage_ref"] = "STAGE-MISSING"
    code, result = route(write(tmp_path, "journey_map", data))
    assert code == 1
    assert any(error["error_id"] == "PM_UNKNOWN_REF" for error in result["errors"])


def test_journey_hypothesis_status_cannot_hide_observed_claim(tmp_path: Path) -> None:
    data = payload("journey_map")
    data["status"] = "hypothesis"
    code, result = route(write(tmp_path, "journey_map", data))
    assert code == 1
    assert any(error["error_id"] == "PM_STATUS_CONFLICT" for error in result["errors"])


def test_icp_observed_claim_requires_evidence(tmp_path: Path) -> None:
    data = payload("ideal_customer_profile")
    data["profile_claims"][0]["evidence_refs"] = []
    code, result = route(write(tmp_path, "ideal_customer_profile", data))
    assert code == 1
    assert any(error["error_id"] == "PM_EVIDENCE_REQUIRED" for error in result["errors"])


def test_icp_gtm_implication_must_reference_known_customer_claim(tmp_path: Path) -> None:
    data = payload("ideal_customer_profile")
    data["gtm_implications"][0]["source_claim_refs"] = ["ICP-MISSING"]
    code, result = route(write(tmp_path, "ideal_customer_profile", data))
    assert code == 1
    assert any(error["error_id"] == "PM_UNKNOWN_REF" for error in result["errors"])


def test_icp_hypothesis_status_cannot_hide_observed_claim(tmp_path: Path) -> None:
    data = payload("ideal_customer_profile")
    data["status"] = "hypothesis"
    code, result = route(write(tmp_path, "ideal_customer_profile", data))
    assert code == 1
    assert any(error["error_id"] == "PM_STATUS_CONFLICT" for error in result["errors"])


def test_campaign_admission_binds_customer_model_validator(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-PM-W5",
            mission="qualify PM customer modeling",
            status="active",
            current_state="initialized",
        )
    )
    result = ArtifactAdmissionService(workspace).admit(
        write(tmp_path, "journey_map"), framework_root=REPO_ROOT
    )
    assert result.artifact_id == "journey_map"
    assert result.admission.validator == "validate-pm-customer-model.py"
    assert result.validation_result["valid"] is True


def test_campaign_catalog_exposes_customer_modeling_without_ranking() -> None:
    registry = load_capability_registry()
    expected = {
        "customer-journey": ("customer_understanding", "journey_map"),
        "ideal-customer-profile": ("customer_understanding", "ideal_customer_profile"),
    }
    for capability_id, (responsibility, output) in expected.items():
        item = registry.get(capability_id)
        assert item is not None
        assert item.capability.accepted_responsibility_types == (responsibility,)
        assert item.capability.output_artifact == output
        assert item.mutates_repository is False
        assert item.returns_control is True

    candidates = registry.candidates("customer_understanding")
    candidate_ids = {item.capability.id for item in candidates}
    assert {"persona", "customer-journey", "ideal-customer-profile"}.issubset(candidate_ids)
