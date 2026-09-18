"""Mechanically decidable release contracts for the Version 1.0 candidate."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path

import yaml

import sensemaking_skills
from sensemaking_skills.campaign_semantics import CURRENT_SCHEMA_VERSION
from sensemaking_skills.external_qualification import PROTOCOL_ID


REPO_ROOT = Path(__file__).resolve().parents[2]


def _read(relative: str) -> str:
    return (REPO_ROOT / relative).read_text(encoding="utf-8")


def _release_identity() -> tuple[str, str, str]:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    contract = yaml.safe_load(_read("release-v1.0.yaml"))
    return (
        pyproject["project"]["version"],
        contract["release"]["version"],
        contract["release"]["status"],
    )


def test_pyproject_is_the_single_source_version_authority() -> None:
    source_version, target_version, status = _release_identity()
    assert sensemaking_skills.__version__ == source_version
    if status == "development":
        assert source_version == f"{target_version}.dev0"
    else:
        assert source_version == target_version

    setup_text = _read("setup.py")
    assert "version=" not in setup_text

    package_json = json.loads(_read("package.json"))
    assert "version" not in package_json


def test_current_release_docs_match_current_architecture() -> None:
    source_version, target_version, status = _release_identity()
    readme = _read("README.md")
    status_doc = _read("STATUS.md")
    plan = _read("docs/productization-v0.3.md")
    changelog = _read("CHANGELOG.md")

    assert "## [0.3.0] - 2026-09-09" in changelog
    assert source_version in readme
    assert target_version in readme
    assert source_version in status_doc
    assert target_version in status_doc
    assert status == "development"
    assert "Campaign schema v2" in status_doc
    assert "product/lab split" in status_doc
    assert "real-harness qualification verifier" in status_doc
    assert "P11 — v0.3 release baseline" in plan


def test_schema_and_external_qualification_contracts_are_in_release_baseline() -> None:
    assert CURRENT_SCHEMA_VERSION == "2"
    assert PROTOCOL_ID == "v0.3-external-golden-path-dogfood-v1"

    plan = _read("docs/productization-v0.3.md")
    readme = _read("README.md")
    assert "v1 -> v2" in plan
    assert "real-harness PASS evidence is empirical" in plan
    assert "verifier PASS != semantic truth" in readme


def test_canonical_campaign_docs_use_schema_v2_and_current_product_authority() -> None:
    semantics = _read("docs/campaign-semantics.md")
    campaign = _read("docs/sensemaking-campaign.md")

    assert f'`schema_version` to be `"{CURRENT_SCHEMA_VERSION}"`' in semantics
    assert '`schema_version` to be `"1"`' not in semantics
    assert "historical v1" in semantics.lower()
    assert "unknown future versions fail closed" in semantics

    assert "ADR 0029" in campaign
    assert "ADR 0026" in campaign
    assert "Why is automatic downstream routing deferred? | ADR 0014" not in campaign


def test_sdist_manifest_carries_validator_runtime_sources() -> None:
    manifest = _read("MANIFEST.in")
    assert "recursive-include skills *" in manifest
    assert "recursive-include scripts *" in manifest
    assert "include docs/canonical-vocabulary.yaml" in manifest


def test_release_distribution_workflow_derives_current_identity() -> None:
    workflow = _read(".github/workflows/release-candidate.yml")

    assert "python -m build" in workflow
    assert "python -m twine check dist/*" in workflow
    assert "source_version=" in workflow
    assert "target_version=" in workflow
    assert "release_status=" in workflow
    assert "sensemaking_skills-1.0.0rc1" not in workflow
    assert "Fresh wheel install proof" in workflow
    assert "Fresh sdist install proof" in workflow
    assert "test_campaign_schema_evolution.py" in workflow
    assert "test_external_golden_path_qualification.py" in workflow
    assert "validate-product-boundary.py" in workflow
    assert 'ref: ${{ github.event.pull_request.head.sha || github.sha }}' in workflow


def test_product_validation_owns_installed_release_portability() -> None:
    product = _read(".github/workflows/validation.yml")
    lab = _read(".github/workflows/lab-validation.yml")

    assert "test_installed_wheel_p11.py" in product
    assert 'ignore-glob="tests/campaign_validation/test_installed_wheel_*.py"' in lab


def test_tag_publish_workflow_checks_metadata_before_upload() -> None:
    workflow = _read(".github/workflows/publish.yml")
    check_index = workflow.index("python -m twine check dist/*")
    upload_index = workflow.index("python -m twine upload dist/*")
    assert check_index < upload_index
