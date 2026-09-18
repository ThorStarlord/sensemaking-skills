from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import tomllib
import yaml


def test_development_metadata_is_beta_and_not_final() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    contract = yaml.safe_load((ROOT / "release-v1.0.yaml").read_text(encoding="utf-8"))
    source_version = pyproject["project"]["version"]
    target_version = contract["release"]["version"]
    assert contract["release"]["status"] == "development"
    assert source_version == f"{target_version}.dev0"
    assert "Development Status :: 4 - Beta" in pyproject["project"]["classifiers"]
    assert "Development Status :: 5 - Production/Stable" not in pyproject["project"]["classifiers"]

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate-release-readiness.py"
_SPEC = spec_from_file_location("validate_release_readiness", _SCRIPT)
assert _SPEC and _SPEC.loader
_MODULE = module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
readiness_diagnostics = _MODULE.readiness_diagnostics


ROOT = Path(__file__).resolve().parents[1]


def test_final_release_gate_reports_unresolved_release_and_governance_gates() -> None:
    diagnostics = readiness_diagnostics(ROOT)

    assert any("release target is" in item for item in diagnostics)
    assert any("release status is development" in item for item in diagnostics)
    assert any("release-owner authorization" in item for item in diagnostics)
    assert any("exact release head" in item for item in diagnostics)
    assert not any("real external harness evidence" in item for item in diagnostics)


def test_contract_declares_reduced_scope_when_external_claims_are_excluded() -> None:
    import yaml

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

    assert any("release status is candidate" in item for item in diagnostics)
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


def test_status_projects_post_rc2_development_responsibility() -> None:
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")

    assert "POST_RC2_DEVELOPMENT_ACTIVE" in status
    assert "Execution Interface & Agent-Factorization v1" in status
    assert "Implement the owner-directed post-RC2 development program" in status
    assert "Issue #384" in status
    assert "PyPI publication or final `1.0.0`" in status
    current_responsibility = status.split(
        "### Current warranted repository-level responsibility", 1
    )[1].split("### Active execution vehicle", 1)[0]
    assert "**None.**" not in current_responsibility

