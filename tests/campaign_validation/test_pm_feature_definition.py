"""Repository qualification tests for the PM feature-definition wave."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from sensemaking_skills.campaign_semantics import CampaignState
from sensemaking_skills.campaigns import (
    ArtifactAdmissionService,
    ArtifactValidationRejectedError,
    CampaignService,
)
from sensemaking_skills.campaigns.capabilities import load_capability_registry

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_IDS = ("story_list", "criteria_list", "risk_analysis")
SECTIONS = {
    "story_list": ("Source and scope", "Stories", "Dependencies and sequencing", "Open questions"),
    "criteria_list": ("Source requirements", "Acceptance scenarios", "Coverage notes", "Unresolved decisions"),
    "risk_analysis": ("Context and assumptions", "Tigers", "Paper tigers", "Elephants", "Mitigations and monitoring", "Recommendation"),
}


def _router_module():
    path = REPO_ROOT / "scripts" / "validate-and-report.py"
    spec = importlib.util.spec_from_file_location("pm_feature_validate_and_report", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _data(artifact_id: str) -> dict:
    if artifact_id == "story_list":
        return {
            "artifact_id": artifact_id,
            "schema_version": "1",
            "source_artifact_ref": "artifacts/prd.md",
            "scope_status": "approved",
            "stories": [
                {
                    "id": "STORY-1",
                    "actor": "author",
                    "want": "resume a long-form project from durable state",
                    "value": "avoid reconstructing project context manually",
                    "source_refs": ["PRD-F1"],
                    "acceptance_intent": ["durable state can be loaded without prior chat"],
                    "dependencies": [],
                    "scope_status": "approved",
                }
            ],
            "unresolved_questions": [],
        }
    if artifact_id == "criteria_list":
        return {
            "artifact_id": artifact_id,
            "schema_version": "1",
            "source_artifact_ref": "artifacts/story_list.md",
            "scenarios": [
                {
                    "id": "AC-1",
                    "source_story_ref": "STORY-1",
                    "category": "happy_path",
                    "given": "durable project state exists",
                    "when": "a fresh context resumes the project",
                    "then": ["the current goal and unresolved questions are reconstructible"],
                    "status": "specified",
                }
            ],
            "unresolved_questions": [],
        }
    return {
        "artifact_id": artifact_id,
        "schema_version": "1",
        "source_artifact_ref": "artifacts/prd.md",
        "risks": [
            {
                "id": "RISK-1",
                "class": "elephant",
                "statement": "native harness behavior remains empirically unqualified",
                "evidence_status": "observed",
                "evidence_refs": ["docs/product-management/dogfood/STATUS.md"],
                "urgency": "investigate",
                "impact": "medium",
                "probability": "unknown",
                "mitigation": "run native-harness dogfood before promotion",
                "owner_role": "product maintainer",
                "success_criterion": "preserved native-harness attempt exists",
                "escalation_signal": "stable support claim is proposed before evidence exists",
            }
        ],
        "recommendation": "go_with_conditions",
        "conditions": ["retain qualification-debt claim ceiling"],
        "unresolved_questions": [],
    }


def _write_artifact(tmp_path: Path, artifact_id: str, data: dict | None = None) -> Path:
    payload = data or _data(artifact_id)
    prose = [f"# {artifact_id}", ""]
    for section in SECTIONS[artifact_id]:
        prose.extend([f"## {section}", "Fixture content.", ""])
    prose.extend(
        [
            "## Machine-readable handoff",
            "```yaml",
            yaml.safe_dump(payload, sort_keys=False).rstrip(),
            "```",
            "",
        ]
    )
    path = tmp_path / f"{artifact_id}.md"
    path.write_text("\n".join(prose), encoding="utf-8")
    return path


def _route(path: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
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
    return completed, json.loads(completed.stdout)


def test_router_selects_feature_definition_validator() -> None:
    router = _router_module()
    for artifact_id in ARTIFACT_IDS:
        assert router.select_validator(artifact_id) == "scripts/validate-pm-feature-definition.py"
    assert router.select_validator("hypothesis_statement") == "scripts/validate-pm-artifact.py"


@pytest.mark.parametrize("artifact_id", ARTIFACT_IDS)
def test_valid_feature_definition_artifact_passes(tmp_path: Path, artifact_id: str) -> None:
    completed, payload = _route(_write_artifact(tmp_path, artifact_id))
    assert completed.returncode == 0, completed.stderr + completed.stdout
    assert payload["valid"] is True
    assert payload["artifact_id"] == artifact_id
    assert payload["validator"] == "validate-pm-feature-definition.py"


def test_story_list_rejects_duplicate_identity_and_missing_traceability(tmp_path: Path) -> None:
    data = _data("story_list")
    duplicate = dict(data["stories"][0])
    duplicate["source_refs"] = []
    data["stories"].append(duplicate)
    completed, payload = _route(_write_artifact(tmp_path, "story_list", data))
    assert completed.returncode == 1
    codes = {error["error_id"] for error in payload["errors"]}
    assert "PM_DUPLICATE_ID" in codes
    assert "PM_SOURCE_REQUIRED" in codes


def test_criteria_list_rejects_claimed_execution_status(tmp_path: Path) -> None:
    data = _data("criteria_list")
    data["scenarios"][0]["status"] = "passed"
    completed, payload = _route(_write_artifact(tmp_path, "criteria_list", data))
    assert completed.returncode == 1
    assert any(error["error_id"] == "PM_INVALID_STATUS" for error in payload["errors"])


def test_risk_analysis_rejects_pure_hypothesis_as_current_tiger(tmp_path: Path) -> None:
    data = _data("risk_analysis")
    data["risks"][0]["class"] = "tiger"
    data["risks"][0]["evidence_status"] = "hypothetical"
    completed, payload = _route(_write_artifact(tmp_path, "risk_analysis", data))
    assert completed.returncode == 1
    assert any(error["error_id"] == "PM_TIGER_NEEDS_EVIDENCE" for error in payload["errors"])


def test_campaign_admission_binds_feature_definition_validator(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-PM-W2",
            mission="qualify feature-definition admission",
            status="active",
            current_state="initialized",
        )
    )
    artifact = _write_artifact(tmp_path, "story_list")
    result = ArtifactAdmissionService(workspace).admit(artifact, framework_root=REPO_ROOT)
    assert result.artifact_id == "story_list"
    assert result.admission.validator == "validate-pm-feature-definition.py"
    assert result.validation_result["valid"] is True


def test_campaign_admission_rejects_invalid_feature_definition(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-PM-W2-REJECT",
            mission="prove feature-definition admission fails closed",
            status="active",
            current_state="initialized",
        )
    )
    data = _data("criteria_list")
    data["scenarios"][0]["status"] = "passed"
    with pytest.raises(ArtifactValidationRejectedError):
        ArtifactAdmissionService(workspace).admit(
            _write_artifact(tmp_path, "criteria_list", data), framework_root=REPO_ROOT
        )


def test_campaign_catalog_exposes_wave2_without_duplicate_prd_authority() -> None:
    registry = load_capability_registry()
    expected = {
        "to-prd": ("product_specification", "prd"),
        "user-stories": ("delivery_specification", "story_list"),
        "acceptance-criteria": ("delivery_specification", "criteria_list"),
        "pre-mortem": ("risk_and_readiness", "risk_analysis"),
    }
    for capability_id, (responsibility_type, output) in expected.items():
        item = registry.get(capability_id)
        assert item is not None
        assert item.kind == "skill"
        assert item.capability.accepted_responsibility_types == (responsibility_type,)
        assert item.capability.output_artifact == output
        assert item.mutates_repository is False
        assert item.returns_control is True

    assert registry.get("prd") is None
    prd_producers = [
        item.capability.capability_id
        for item in registry.entries
        if item.capability.output_artifact == "prd" and item.availability != "unavailable"
    ]
    assert prd_producers == ["to-prd"]
