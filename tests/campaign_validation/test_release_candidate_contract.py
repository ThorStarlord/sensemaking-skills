"""Mechanically decidable release contracts for Sensemaking Skills v0.3.0."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path

import sensemaking_skills
from sensemaking_skills.campaign_semantics import CURRENT_SCHEMA_VERSION
from sensemaking_skills.external_qualification import PROTOCOL_ID


REPO_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_VERSION = "0.3.0"


def _read(relative: str) -> str:
    return (REPO_ROOT / relative).read_text(encoding="utf-8")


def test_pyproject_is_the_single_release_version_authority() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    assert pyproject["project"]["version"] == EXPECTED_VERSION
    assert sensemaking_skills.__version__ == EXPECTED_VERSION

    setup_text = _read("setup.py")
    assert "version=" not in setup_text

    package_json = json.loads(_read("package.json"))
    assert "version" not in package_json


def test_v030_release_docs_match_current_architecture() -> None:
    readme = _read("README.md")
    status = _read("STATUS.md")
    plan = _read("docs/productization-v0.3.md")
    changelog = _read("CHANGELOG.md")

    assert "**Version:** 0.3.0" in readme
    assert "**Version:** 0.3.0" in status
    assert "## [0.3.0] - 2026-09-09" in changelog
    assert "Campaign schema v2" in status
    assert "product/lab split" in status
    assert "real-harness qualification verifier" in status
    assert "P11 — v0.3 release baseline" in plan


def test_schema_and_external_qualification_contracts_are_in_release_baseline() -> None:
    assert CURRENT_SCHEMA_VERSION == "2"
    assert PROTOCOL_ID == "v0.3-external-golden-path-dogfood-v1"

    plan = _read("docs/productization-v0.3.md")
    readme = _read("README.md")
    assert "v1 -> v2" in plan
    assert "real-harness PASS evidence is empirical" in plan
    assert "verifier PASS != semantic truth" in readme


def test_canonical_campaign_docs_reject_stale_schema_and_product_boundary_authority() -> None:
    semantics = _read("docs/campaign-semantics.md")
    campaign = _read("docs/sensemaking-campaign.md")

    assert f'requires `schema_version` to be `"{CURRENT_SCHEMA_VERSION}"`' in semantics
    assert 'requires `schema_version` to be `"1"`' not in semantics
    assert "historical v1" in semantics.lower()

    assert "Current product boundary and routing/planning non-goals" in campaign
    assert "ADR 0029" in campaign
    assert "Why is automatic downstream routing deferred? | ADR 0014" not in campaign


def test_sdist_manifest_carries_validator_runtime_sources() -> None:
    manifest = _read("MANIFEST.in")
    assert "recursive-include skills *" in manifest
    assert "recursive-include scripts *" in manifest
    assert "include docs/canonical-vocabulary.yaml" in manifest


def test_release_candidate_workflow_qualifies_current_boundaries() -> None:
    workflow = _read(".github/workflows/release-candidate.yml")

    assert "python -m build" in workflow
    assert "python -m twine check dist/*" in workflow
    assert "sensemaking_skills-0.3.0-py3-none-any.whl" in workflow
    assert "sensemaking_skills-0.3.0.tar.gz" in workflow
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
