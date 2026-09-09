"""Qualification evidence receipt contract and rejection tests."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
import yaml

from sensemaking_skills.qualification_evidence import (
    EVIDENCE_SCOPE,
    QualificationEvidenceError,
    build_qualification_evidence,
    load_qualification_evidence,
    verify_qualification_evidence,
    write_qualification_evidence,
)

_FIXTURE = Path(__file__).parents[1] / "fixtures" / "external_golden_path" / "pass"


def _copy_fixture(tmp_path: Path) -> Path:
    destination = tmp_path / "attempt"
    shutil.copytree(_FIXTURE, destination)
    return destination


def _load_manifest(attempt: Path) -> dict:
    return yaml.safe_load((attempt / "attempt.yaml").read_text(encoding="utf-8"))


def _write_manifest(attempt: Path, data: dict) -> None:
    (attempt / "attempt.yaml").write_text(
        yaml.safe_dump(data, sort_keys=False),
        encoding="utf-8",
    )


def test_receipt_binds_exact_attempt_identity_and_evidence() -> None:
    receipt = build_qualification_evidence(_FIXTURE)

    assert receipt.attempt_id == "DOGFOOD-QUAL-001"
    assert receipt.outcome == "PASS"
    assert receipt.qualified is True
    assert receipt.evidence_scope == EVIDENCE_SCOPE
    assert receipt.manifest_sha256
    assert receipt.package_sha256
    assert receipt.receipt_sha256
    assert receipt.sensemaking_candidate["version"] == "0.3.0"
    assert receipt.runtime["harness"] == "claude"
    assert receipt.external_target["repository"] != "ThorStarlord/sensemaking-skills"
    assert {item.path for item in receipt.verified_evidence} == {
        "evidence/setup.yaml",
        "evidence/native-invocation.yaml",
        "evidence/lifecycle.txt",
        "evidence/handoff.yaml",
        "evidence/resume.yaml",
    }
    assert all(len(item.sha256) == 64 for item in receipt.verified_evidence)


def test_receipt_is_deterministic_for_unchanged_attempt() -> None:
    first = build_qualification_evidence(_FIXTURE)
    second = build_qualification_evidence(_FIXTURE)

    assert first.to_dict() == second.to_dict()
    assert first.receipt_sha256 == second.receipt_sha256
    assert first.package_sha256 == second.package_sha256


def test_written_receipt_round_trips_and_verifies(tmp_path: Path) -> None:
    output = tmp_path / "qualification-evidence.json"
    expected = write_qualification_evidence(_FIXTURE, output)

    loaded = load_qualification_evidence(output)
    verified = verify_qualification_evidence(_FIXTURE, output)

    assert loaded == expected.to_dict()
    assert verified == expected


def test_invalid_attempt_cannot_produce_qualification_evidence(tmp_path: Path) -> None:
    attempt = _copy_fixture(tmp_path)
    with (attempt / "evidence" / "lifecycle.txt").open("a", encoding="utf-8") as handle:
        handle.write("tampered\n")

    with pytest.raises(QualificationEvidenceError) as exc_info:
        build_qualification_evidence(attempt)

    assert exc_info.value.code == "QUALIFICATION_ATTEMPT_NOT_STRUCTURALLY_VALID"


def test_existing_receipt_is_never_overwritten(tmp_path: Path) -> None:
    output = tmp_path / "qualification-evidence.json"
    output.write_text("owner evidence\n", encoding="utf-8")

    with pytest.raises(QualificationEvidenceError) as exc_info:
        write_qualification_evidence(_FIXTURE, output)

    assert exc_info.value.code == "QUALIFICATION_EVIDENCE_OUTPUT_EXISTS"
    assert output.read_text(encoding="utf-8") == "owner evidence\n"


def test_receipt_tampering_fails_digest_check(tmp_path: Path) -> None:
    output = tmp_path / "qualification-evidence.json"
    write_qualification_evidence(_FIXTURE, output)
    payload = json.loads(output.read_text(encoding="utf-8"))
    payload["runtime"]["harness_version"] = "rewritten-after-verification"
    output.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(QualificationEvidenceError) as exc_info:
        load_qualification_evidence(output)

    assert exc_info.value.code == "QUALIFICATION_EVIDENCE_RECEIPT_DIGEST_MISMATCH"


def test_receipt_rejects_unknown_claim_fields(tmp_path: Path) -> None:
    output = tmp_path / "qualification-evidence.json"
    write_qualification_evidence(_FIXTURE, output)
    payload = json.loads(output.read_text(encoding="utf-8"))
    payload["empirical_truth"] = True
    output.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(QualificationEvidenceError) as exc_info:
        load_qualification_evidence(output)

    assert exc_info.value.code == "QUALIFICATION_EVIDENCE_RECEIPT_INVALID"


def test_existing_receipt_no_longer_verifies_after_attempt_changes(tmp_path: Path) -> None:
    attempt = _copy_fixture(tmp_path)
    output = tmp_path / "qualification-evidence.json"
    write_qualification_evidence(attempt, output)
    with (attempt / "evidence" / "lifecycle.txt").open("a", encoding="utf-8") as handle:
        handle.write("later mutation\n")

    with pytest.raises(QualificationEvidenceError) as exc_info:
        verify_qualification_evidence(attempt, output)

    assert exc_info.value.code == "QUALIFICATION_ATTEMPT_NOT_STRUCTURALLY_VALID"


def test_structurally_valid_fail_is_preserved_as_nonqualified_evidence(tmp_path: Path) -> None:
    attempt = _copy_fixture(tmp_path)
    data = _load_manifest(attempt)
    data["lifecycle"]["steps"][-1]["status"] = "FAIL"
    data["outcome"]["classification"] = "FAIL"
    data["outcome"]["notes"] = "Terminal decision failed after fresh-context resume."
    _write_manifest(attempt, data)

    receipt = build_qualification_evidence(attempt)

    assert receipt.outcome == "FAIL"
    assert receipt.qualified is False
    assert receipt.receipt_sha256


def test_receipt_scope_does_not_claim_empirical_origin() -> None:
    receipt = build_qualification_evidence(_FIXTURE).to_dict()

    assert receipt["evidence_scope"] == "mechanically_verified_frozen_attempt"
    assert "real_harness_attested" not in receipt
    assert "empirical_truth" not in receipt
