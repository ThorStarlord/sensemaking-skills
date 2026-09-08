"""P4 integration tests for validated artifact admission."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from sensemaking_skills.campaign_semantics import CampaignState
from sensemaking_skills.campaigns import (
    ArtifactAdmissionService,
    ArtifactValidationRejectedError,
    ArtifactValidatorError,
    CampaignIntegrityError,
    CampaignService,
    CampaignStore,
    CampaignWorkspaceError,
)
from sensemaking_skills.campaigns.admission import load_artifact_admission


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "architectural-review-recommendation"
VALID_ARTIFACT = FIXTURES / "fixture-valid-pursue.md"
INVALID_ARTIFACT = FIXTURES / "fixture-invalid-missing-evidence.md"


def _initialize(workspace: Path) -> CampaignService:
    service = CampaignService(workspace)
    service.initialize(
        CampaignState(
            campaign_id="CMP-P4",
            mission="admit only canonically validated artifact bytes",
            status="active",
            current_state="initialized",
        )
    )
    return service


def _symlink_or_skip(link: Path, target: Path, *, target_is_directory: bool = False):
    try:
        link.symlink_to(target, target_is_directory=target_is_directory)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"symlink capability unavailable: {exc}")


def test_valid_artifact_is_content_addressed_and_receipt_bound(tmp_path):
    workspace = tmp_path / "campaign"
    service = _initialize(workspace)

    result = ArtifactAdmissionService(workspace).admit(
        VALID_ARTIFACT,
        framework_root=REPO_ROOT,
    )

    assert result.artifact_id == "architectural_review_recommendation"
    assert result.admission.validator == "validate-architectural-review-recommendation.py"
    assert result.validation_result["valid"] is True
    assert len(result.artifact_sha256) == 64
    assert result.artifact_ref.startswith(
        f"artifacts/architectural_review_recommendation/{result.artifact_sha256}."
    )
    assert result.admission_ref.startswith(
        "admissions/architectural_review_recommendation/"
    )

    copied = workspace / result.artifact_ref
    receipt_path = workspace / result.admission_ref
    assert copied.read_bytes() == VALID_ARTIFACT.read_bytes()
    loaded = load_artifact_admission(receipt_path)
    assert loaded == result.admission
    assert loaded.artifact_sha256 == result.artifact_sha256
    assert len(loaded.router_sha256) == 64
    assert len(loaded.validator_sha256) == 64

    refs = set(CampaignStore(workspace).evidence_refs())
    assert result.artifact_ref in refs
    assert result.admission_ref in refs
    assert set(service.resume().evidence_refs) == refs


def test_generic_validator_fallback_can_admit_registered_artifact(tmp_path):
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    artifact = tmp_path / "discovery-findings.md"
    artifact.write_text(
        "# Discovery findings\n\n"
        "## 13. Machine-readable handoff\n\n"
        "```yaml\n"
        "artifact_id: discovery_findings\n"
        "```\n",
        encoding="utf-8",
    )

    result = ArtifactAdmissionService(workspace).admit(
        artifact,
        framework_root=REPO_ROOT,
    )

    assert result.artifact_id == "discovery_findings"
    assert result.admission.validator == "validate-artifact.py"
    assert result.validation_result["valid"] is True
    refs = set(CampaignStore(workspace).evidence_refs())
    assert result.artifact_ref in refs
    assert result.admission_ref in refs


def test_invalid_artifact_is_rejected_before_any_evidence_is_admitted(tmp_path):
    workspace = tmp_path / "campaign"
    _initialize(workspace)

    with pytest.raises(ArtifactValidationRejectedError) as exc_info:
        ArtifactAdmissionService(workspace).admit(
            INVALID_ARTIFACT,
            framework_root=REPO_ROOT,
        )

    assert exc_info.value.validation_result["valid"] is False
    assert exc_info.value.validation_result["validator"] == (
        "validate-architectural-review-recommendation.py"
    )
    assert CampaignStore(workspace).evidence_refs() == ()
    assert list((workspace / "artifacts").rglob("*")) == []
    assert list((workspace / "admissions").rglob("*")) == []


def test_validator_boundary_failure_is_not_misreported_as_artifact_invalid(tmp_path):
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    empty_framework = tmp_path / "empty-framework"
    empty_framework.mkdir()

    with pytest.raises(ArtifactValidatorError, match="canonical validator router"):
        ArtifactAdmissionService(workspace).admit(
            VALID_ARTIFACT,
            framework_root=empty_framework,
        )

    assert CampaignStore(workspace).evidence_refs() == ()


def test_manual_file_under_artifacts_never_acquires_evidence_status(tmp_path):
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    manual = workspace / "artifacts" / "manual.md"
    manual.write_text("not canonically admitted", encoding="utf-8")

    assert CampaignStore(workspace).evidence_refs() == ()
    assert CampaignService(workspace).resume().evidence_refs == ()


def test_admitted_artifact_tamper_fails_closed(tmp_path):
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    result = ArtifactAdmissionService(workspace).admit(
        VALID_ARTIFACT,
        framework_root=REPO_ROOT,
    )

    (workspace / result.artifact_ref).write_text("tampered", encoding="utf-8")

    with pytest.raises(CampaignIntegrityError) as exc_info:
        CampaignStore(workspace).evidence_refs()
    assert "ADMITTED_ARTIFACT_DIGEST_MISMATCH" in exc_info.value.diagnostic_codes

    with pytest.raises(CampaignIntegrityError) as resume_error:
        CampaignService(workspace).resume()
    assert "ADMITTED_ARTIFACT_DIGEST_MISMATCH" in resume_error.value.diagnostic_codes


def test_admission_receipt_tamper_breaks_content_address(tmp_path):
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    result = ArtifactAdmissionService(workspace).admit(
        VALID_ARTIFACT,
        framework_root=REPO_ROOT,
    )
    receipt_path = workspace / result.admission_ref
    payload = yaml.safe_load(receipt_path.read_text(encoding="utf-8"))
    payload["router_sha256"] = "0" * 64
    receipt_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    with pytest.raises(CampaignIntegrityError) as exc_info:
        CampaignStore(workspace).evidence_refs()
    assert "INVALID_ARTIFACT_ADMISSION" in exc_info.value.diagnostic_codes


def test_artifact_write_refuses_preexisting_symlink_escape(tmp_path):
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    outside = tmp_path / "outside"
    outside.mkdir()
    artifact_id_dir = workspace / "artifacts" / "architectural_review_recommendation"
    _symlink_or_skip(artifact_id_dir, outside, target_is_directory=True)

    with pytest.raises(CampaignWorkspaceError, match="escapes its physical root"):
        ArtifactAdmissionService(workspace).admit(
            VALID_ARTIFACT,
            framework_root=REPO_ROOT,
        )

    assert list(outside.iterdir()) == []


def test_receipt_write_refuses_preexisting_symlink_escape(tmp_path):
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    outside = tmp_path / "outside"
    outside.mkdir()
    admission_id_dir = workspace / "admissions" / "architectural_review_recommendation"
    _symlink_or_skip(admission_id_dir, outside, target_is_directory=True)

    with pytest.raises(CampaignWorkspaceError, match="escapes its physical root"):
        ArtifactAdmissionService(workspace).admit(
            VALID_ARTIFACT,
            framework_root=REPO_ROOT,
        )

    assert list(outside.iterdir()) == []
    # A poisoned workspace must also fail closed during later evidence reads.
    with pytest.raises(CampaignWorkspaceError, match="physically contained"):
        CampaignStore(workspace).evidence_refs()


def test_failed_receipt_write_leaves_only_unadmitted_orphan(tmp_path, monkeypatch):
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    admission_service = ArtifactAdmissionService(workspace)
    real_write_receipt = ArtifactAdmissionService._write_receipt

    def fail_receipt(*args, **kwargs):
        raise OSError("simulated receipt persistence failure")

    monkeypatch.setattr(
        ArtifactAdmissionService,
        "_write_receipt",
        staticmethod(fail_receipt),
    )
    with pytest.raises(OSError, match="simulated receipt persistence failure"):
        admission_service.admit(VALID_ARTIFACT, framework_root=REPO_ROOT)

    assert CampaignStore(workspace).evidence_refs() == ()
    assert any((workspace / "artifacts").rglob("*.md"))
    assert list((workspace / "admissions").rglob("*.yaml")) == []

    monkeypatch.setattr(
        ArtifactAdmissionService,
        "_write_receipt",
        staticmethod(real_write_receipt),
    )
    admitted = ArtifactAdmissionService(workspace).admit(
        VALID_ARTIFACT,
        framework_root=REPO_ROOT,
    )
    assert admitted.artifact_ref in CampaignStore(workspace).evidence_refs()


def test_legacy_workspace_without_admissions_directory_remains_readable(tmp_path):
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    (workspace / "admissions").rmdir()
    raw = workspace / "evidence" / "legacy.txt"
    raw.write_text("legacy evidence", encoding="utf-8")

    assert CampaignStore(workspace).evidence_refs() == ("evidence/legacy.txt",)
