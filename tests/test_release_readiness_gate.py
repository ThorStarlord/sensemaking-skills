from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import tomllib
import yaml


_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate-release-readiness.py"
_SPEC = spec_from_file_location("validate_release_readiness", _SCRIPT)
assert _SPEC and _SPEC.loader
_MODULE = module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
readiness_diagnostics = _MODULE.readiness_diagnostics

ROOT = Path(__file__).resolve().parents[1]


def test_development_metadata_is_beta_and_not_final() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    contract = yaml.safe_load((ROOT / "release-v1.0.yaml").read_text(encoding="utf-8"))
    source_version = pyproject["project"]["version"]
    target_version = contract["release"]["version"]
    assert contract["release"]["status"] == "development"
    assert source_version == f"{target_version}.dev0"
    assert "Development Status :: 4 - Beta" in pyproject["project"]["classifiers"]
    assert "Development Status :: 5 - Production/Stable" not in pyproject["project"]["classifiers"]


def test_final_release_gate_reports_unresolved_release_and_governance_gates() -> None:
    diagnostics = readiness_diagnostics(ROOT)

    assert any("release target is" in item for item in diagnostics)
    assert any("release status is development" in item for item in diagnostics)
    assert any("release-owner authorization" in item for item in diagnostics)
    assert any("exact release head CI evidence" in item for item in diagnostics)
    assert not any("real external harness evidence" in item for item in diagnostics)


def test_contract_declares_reduced_scope_when_external_claims_are_excluded() -> None:
    contract = yaml.safe_load(
        (ROOT / "release-v1.0.yaml").read_text(encoding="utf-8")
    )
    assert contract["release"]["scope_classification"] == "reduced"


def test_development_contract_cannot_be_reported_as_finally_ready(tmp_path: Path) -> None:
    contract = (ROOT / "release-v1.0.yaml").read_text(encoding="utf-8")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    (tmp_path / "release-v1.0.yaml").write_text(contract, encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(pyproject, encoding="utf-8")
    (tmp_path / "qualification-evidence").mkdir()
    (tmp_path / "qualification-evidence" / "STATUS.md").write_text(
        "Current empirical PASS: NONE\n", encoding="utf-8"
    )

    diagnostics = readiness_diagnostics(tmp_path)

    assert any("release status is development" in item for item in diagnostics)
    assert any("release target is" in item for item in diagnostics)


def test_reduced_scope_checklist_does_not_require_excluded_native_harness_claim() -> None:
    contract = yaml.safe_load(
        (ROOT / "release-v1.0.yaml").read_text(encoding="utf-8")
    )
    checklist = (ROOT / "docs" / "release-v1.0-checklist.md").read_text(
        encoding="utf-8"
    )

    assert contract["support"]["native_harnesses"] == []
    assert (
        "[x] Engineering native-harness evidence is frozen, or engineering native "
        "support is excluded from 1.0."
        in checklist
    )


def _write_ready_fixture(tmp_path: Path, *, source_sha: str) -> tuple[Path, Path, Path]:
    contract = yaml.safe_load(
        (ROOT / "release-v1.0.yaml").read_text(encoding="utf-8")
    )
    contract["release"]["version"] = "1.0.0"
    contract["release"]["status"] = "ready"
    (tmp_path / "release-v1.0.yaml").write_text(
        yaml.safe_dump(contract, sort_keys=False),
        encoding="utf-8",
    )

    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    pyproject = pyproject.replace(
        'version = "1.0.0rc3.dev0"',
        'version = "1.0.0"',
    ).replace(
        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
    )
    (tmp_path / "pyproject.toml").write_text(pyproject, encoding="utf-8")

    (tmp_path / "qualification-evidence").mkdir()
    (tmp_path / "qualification-evidence" / "STATUS.md").write_text(
        "Current empirical PASS: NONE\n",
        encoding="utf-8",
    )

    evidence_dir = tmp_path / ".release-evidence"
    evidence_dir.mkdir()
    ci_path = evidence_dir / "ci.yaml"
    ci_path.write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "release_version": "1.0.0",
                "source_sha": source_sha,
                "product_validation": {
                    "workflow": "Product Validation",
                    "run_id": 1001,
                    "conclusion": "success",
                },
                "release_candidate_distribution": {
                    "workflow": "Release Candidate Distribution",
                    "run_id": 1002,
                    "conclusion": "success",
                },
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    owner_path = evidence_dir / "owner-authorization.yaml"
    owner_path.write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "release_version": "1.0.0",
                "source_sha": source_sha,
                "decision": "AUTHORIZE_FINAL_1_0_PUBLICATION",
                "authorized_by": "release-owner",
                "authorized_at": "2026-09-22T00:00:00Z",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    digest_path = tmp_path / "release-SHA256SUMS.txt"
    digest_path.write_text(
        "\n".join(
            [
                "a" * 64 + "  sensemaking_skills-1.0.0-py3-none-any.whl",
                "b" * 64 + "  sensemaking_skills-1.0.0.tar.gz",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return ci_path, owner_path, digest_path


def test_final_release_gate_has_a_satisfiable_ready_path(
    tmp_path: Path, monkeypatch
) -> None:
    source_sha = "1" * 40
    ci_path, owner_path, digest_path = _write_ready_fixture(
        tmp_path,
        source_sha=source_sha,
    )

    def fake_git(_repo_root: Path, *args: str) -> str | None:
        if args == ("rev-parse", "HEAD"):
            return source_sha
        if args == ("status", "--porcelain"):
            return ""
        return None

    monkeypatch.setattr(_MODULE, "_git", fake_git)

    diagnostics = readiness_diagnostics(
        tmp_path,
        ci_evidence_path=ci_path,
        owner_authorization_path=owner_path,
        artifact_digests_path=digest_path,
    )

    assert diagnostics == []


def test_final_release_gate_rejects_stale_ci_source_identity(
    tmp_path: Path, monkeypatch
) -> None:
    current_sha = "2" * 40
    ci_path, owner_path, digest_path = _write_ready_fixture(
        tmp_path,
        source_sha="1" * 40,
    )

    def fake_git(_repo_root: Path, *args: str) -> str | None:
        if args == ("rev-parse", "HEAD"):
            return current_sha
        if args == ("status", "--porcelain"):
            return ""
        return None

    monkeypatch.setattr(_MODULE, "_git", fake_git)

    diagnostics = readiness_diagnostics(
        tmp_path,
        ci_evidence_path=ci_path,
        owner_authorization_path=owner_path,
        artifact_digests_path=digest_path,
    )

    assert any(
        "CI evidence source_sha does not match current Git HEAD" in item
        for item in diagnostics
    )
    assert any(
        "release-owner authorization source_sha does not match current Git HEAD" in item
        for item in diagnostics
    )


def test_final_release_gate_rejects_failed_required_ci(
    tmp_path: Path, monkeypatch
) -> None:
    source_sha = "3" * 40
    ci_path, owner_path, digest_path = _write_ready_fixture(
        tmp_path,
        source_sha=source_sha,
    )
    ci = yaml.safe_load(ci_path.read_text(encoding="utf-8"))
    ci["product_validation"]["conclusion"] = "failure"
    ci_path.write_text(yaml.safe_dump(ci, sort_keys=False), encoding="utf-8")

    def fake_git(_repo_root: Path, *args: str) -> str | None:
        if args == ("rev-parse", "HEAD"):
            return source_sha
        if args == ("status", "--porcelain"):
            return ""
        return None

    monkeypatch.setattr(_MODULE, "_git", fake_git)

    diagnostics = readiness_diagnostics(
        tmp_path,
        ci_evidence_path=ci_path,
        owner_authorization_path=owner_path,
        artifact_digests_path=digest_path,
    )

    assert any(
        "product_validation.conclusion must be 'success'" in item
        for item in diagnostics
    )


def test_status_preserves_execution_interface_closeout_during_new_construction() -> None:
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")

    assert "NORMAL_USE_VALIDATION" in status
    assert "Execution Interface & Agent-Factorization v1 — COMPLETE" in status
    assert "Policy Hierarchy Completion v0" in status
    assert "CURRENT CONSTRUCTION RESPONSIBILITY =" in status
    assert "SUPPORTING EVIDENCE MODE = NORMAL_USE_VALIDATION" in status
    assert "Issue #393" in status
    assert "Issue #384" in status
    assert "1.0.0rc3.dev0" in status
    assert "Do **not** freeze RC3" in status
    assert "POST_RC2_DEVELOPMENT_ACTIVE" not in status
    assert "EXECUTION_INTERFACE_V1_CLOSEOUT" not in status
    assert "CURRENT CONSTRUCTION RESPONSIBILITY = EXECUTION_INTERFACE_V1_CLOSEOUT" not in status
