from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def test_version_1_metadata_is_not_beta() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "1.0.0"' in pyproject
    assert 'Development Status :: 5 - Production/Stable' in pyproject
    assert 'Development Status :: 4 - Beta' not in pyproject

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate-release-readiness.py"
_SPEC = spec_from_file_location("validate_release_readiness", _SCRIPT)
assert _SPEC and _SPEC.loader
_MODULE = module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
readiness_diagnostics = _MODULE.readiness_diagnostics


ROOT = Path(__file__).resolve().parents[1]


def test_final_release_gate_reports_unresolved_external_and_governance_gates() -> None:
    diagnostics = readiness_diagnostics(ROOT)

    assert any("release-owner authorization" in item for item in diagnostics)
    assert any("exact release head" in item for item in diagnostics)
    assert not any("real external harness evidence" in item for item in diagnostics)


def test_contract_declares_reduced_scope_when_external_claims_are_excluded() -> None:
    import yaml

    contract = yaml.safe_load(
        (ROOT / "release-v1.0.yaml").read_text(encoding="utf-8")
    )
    assert contract["release"]["scope_classification"] == "reduced"


def test_candidate_contract_cannot_be_reported_as_finally_ready(tmp_path: Path) -> None:
    contract = (ROOT / "release-v1.0.yaml").read_text(encoding="utf-8")
    (tmp_path / "release-v1.0.yaml").write_text(contract, encoding="utf-8")
    (tmp_path / "qualification-evidence").mkdir()
    (tmp_path / "qualification-evidence" / "STATUS.md").write_text(
        "Current empirical PASS: NONE\n", encoding="utf-8"
    )

    diagnostics = readiness_diagnostics(tmp_path)

    assert any("release status is candidate" in item for item in diagnostics)
