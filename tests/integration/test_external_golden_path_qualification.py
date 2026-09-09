"""Integration contract tests for real-harness golden-path qualification."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
import yaml

from sensemaking_skills.external_qualification import main, validate_attempt

_FIXTURE = Path(__file__).parents[1] / "fixtures" / "external_golden_path" / "pass"


def _copy_fixture(tmp_path: Path) -> Path:
    destination = tmp_path / "attempt"
    shutil.copytree(_FIXTURE, destination)
    return destination


def _load_manifest(attempt: Path) -> dict:
    return yaml.safe_load((attempt / "attempt.yaml").read_text(encoding="utf-8"))


def _write_manifest(attempt: Path, data: dict) -> None:
    (attempt / "attempt.yaml").write_text(
        yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
    )


def _first_code(result) -> str | None:
    return result.diagnostics[0].code if result.diagnostics else None


def test_passing_fixture_qualifies_exact_evidence_package():
    result = validate_attempt(_FIXTURE)

    assert result.package_valid is True
    assert result.qualified is True
    assert result.outcome == "PASS"
    assert result.attempt_id == "DOGFOOD-QUAL-001"
    assert result.manifest_sha256
    assert set(result.verified_evidence) == {
        "evidence/setup.yaml",
        "evidence/native-invocation.yaml",
        "evidence/lifecycle.txt",
        "evidence/handoff.yaml",
        "evidence/resume.yaml",
    }
    assert result.diagnostics == ()


def test_cli_json_surface_is_machine_readable(capsys):
    exit_code = main([str(_FIXTURE), "--json"])
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["package_valid"] is True
    assert payload["qualified"] is True
    assert payload["outcome"] == "PASS"
    assert payload["diagnostics"] == []


def test_setup_receipt_cannot_substitute_for_native_invocation(tmp_path: Path):
    attempt = _copy_fixture(tmp_path)
    data = _load_manifest(attempt)
    data["harness_evidence"]["invocation_receipt"] = dict(
        data["harness_evidence"]["setup_receipt"]
    )
    _write_manifest(attempt, data)

    result = validate_attempt(attempt)

    assert result.package_valid is False
    assert result.qualified is False
    assert _first_code(result) == "NATIVE_INVOCATION_EVIDENCE_NOT_DISTINCT"


def test_tampered_evidence_digest_fails_closed(tmp_path: Path):
    attempt = _copy_fixture(tmp_path)
    with (attempt / "evidence" / "lifecycle.txt").open("a", encoding="utf-8") as handle:
        handle.write("tampered\n")

    result = validate_attempt(attempt)

    assert result.package_valid is False
    assert result.qualified is False
    assert _first_code(result) == "EVIDENCE_DIGEST_MISMATCH"


def test_manual_campaign_repair_blocks_qualification(tmp_path: Path):
    attempt = _copy_fixture(tmp_path)
    data = _load_manifest(attempt)
    data["operator_policy"]["manual_campaign_repair_allowed"] = True
    _write_manifest(attempt, data)

    result = validate_attempt(attempt)

    assert result.package_valid is False
    assert _first_code(result) == "PROHIBITED_OPERATOR_REPAIR_OR_CONTEXT"


def test_fresh_context_requires_distinct_agent_session(tmp_path: Path):
    attempt = _copy_fixture(tmp_path)
    data = _load_manifest(attempt)
    data["fresh_context"]["resume_session_id"] = data["fresh_context"]["source_session_id"]
    _write_manifest(attempt, data)

    result = validate_attempt(attempt)

    assert result.package_valid is False
    assert _first_code(result) == "FRESH_CONTEXT_SESSION_REUSED"


def test_lifecycle_order_is_canonical_and_complete(tmp_path: Path):
    attempt = _copy_fixture(tmp_path)
    data = _load_manifest(attempt)
    steps = data["lifecycle"]["steps"]
    steps[1], steps[2] = steps[2], steps[1]
    _write_manifest(attempt, data)

    result = validate_attempt(attempt)

    assert result.package_valid is False
    assert _first_code(result) == "LIFECYCLE_ORDER_MISMATCH"


def test_recorded_fail_is_preserved_but_not_qualified(tmp_path: Path):
    attempt = _copy_fixture(tmp_path)
    data = _load_manifest(attempt)
    data["lifecycle"]["steps"][-1]["status"] = "FAIL"
    data["outcome"]["classification"] = "FAIL"
    data["outcome"]["notes"] = "Terminal decision failed after fresh-context resume."
    _write_manifest(attempt, data)

    result = validate_attempt(attempt)

    assert result.package_valid is True
    assert result.qualified is False
    assert result.outcome == "FAIL"
    assert _first_code(result) == "ATTEMPT_RECORDED_FAIL"


def test_self_repository_is_not_an_external_qualification_target(tmp_path: Path):
    attempt = _copy_fixture(tmp_path)
    data = _load_manifest(attempt)
    data["external_target"]["repository"] = "ThorStarlord/sensemaking-skills"
    _write_manifest(attempt, data)

    result = validate_attempt(attempt)

    assert result.package_valid is False
    assert _first_code(result) == "SELF_TARGET_PROHIBITED"


@pytest.mark.skipif(not hasattr(Path, "symlink_to"), reason="symlinks unavailable")
def test_symlink_escape_evidence_is_rejected(tmp_path: Path):
    attempt = _copy_fixture(tmp_path)
    outside = tmp_path / "outside.txt"
    outside.write_text("outside\n", encoding="utf-8")
    target = attempt / "evidence" / "lifecycle.txt"
    target.unlink()
    try:
        target.symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"runtime cannot create symlinks: {exc}")

    data = _load_manifest(attempt)
    import hashlib

    digest = hashlib.sha256(outside.read_bytes()).hexdigest()
    for step in data["lifecycle"]["steps"]:
        for evidence in step["evidence"]:
            if evidence["path"] == "evidence/lifecycle.txt":
                evidence["sha256"] = digest
    _write_manifest(attempt, data)

    result = validate_attempt(attempt)

    assert result.package_valid is False
    assert _first_code(result) == "EVIDENCE_PATH_UNSAFE"
