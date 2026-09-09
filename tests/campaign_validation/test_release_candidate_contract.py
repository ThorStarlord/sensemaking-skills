"""Release-candidate contracts for the v0.3.0 Campaign release.

These tests intentionally lock only mechanically decidable release claims. They
must not grow into a synthetic real-harness/external-repository experiment.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import sensemaking_skills


REPO_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_VERSION = "0.3.0"


def _read(relative: str) -> str:
    return (REPO_ROOT / relative).read_text(encoding="utf-8")


def test_release_version_authorities_agree() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    assert pyproject["project"]["version"] == EXPECTED_VERSION

    setup_text = _read("setup.py")
    setup_versions = re.findall(r'^\s*version="([^"]+)"', setup_text, flags=re.MULTILINE)
    assert setup_versions == [EXPECTED_VERSION]

    assert sensemaking_skills.__version__ == EXPECTED_VERSION


def test_live_release_docs_identify_v030() -> None:
    readme = _read("README.md")
    status = _read("STATUS.md")
    getting_started = _read("GETTING_STARTED.md")
    installation = _read("INSTALLATION.md")
    changelog = _read("CHANGELOG.md")
    publishing = _read("docs/PUBLISHING.md")

    assert "**Version:** 0.3.0" in readme
    assert "**Version:** 0.3.0" in status
    assert "Getting Started with Sensemaking Skills v0.3.0" in getting_started
    assert "Installation & Setup Guide — Sensemaking Skills v0.3.0" in installation
    assert "## [0.3.0] - 2026-09-09" in changelog
    assert "# Publishing Sensemaking Skills v0.3.0" in publishing


def test_external_harness_dogfood_is_explicitly_non_blocking() -> None:
    protocol = _read("docs/v0.3-external-qualification-protocol.md")
    plan = _read("docs/productization-v0.3.md")
    status = _read("STATUS.md")

    assert "NON-BLOCKING POST-RELEASE DOGFOOD PROTOCOL" in protocol
    assert "does not gate v0.3.0 publication" in protocol
    assert "not a v0.3.0 release gate" in plan
    assert "not a v0.3.0 release gate" in status


def test_v030_claim_ceiling_preserves_harness_distinction() -> None:
    combined = "\n".join(
        [
            _read("README.md"),
            _read("STATUS.md"),
            _read("docs/productization-v0.3.md"),
        ]
    )
    assert "Skill copied to discovery root" in combined
    assert "harness observed Skill" in combined
    assert "universal real-harness Skill discovery" in combined


def test_sdist_manifest_carries_validator_runtime_sources() -> None:
    manifest = _read("MANIFEST.in")
    assert "recursive-include skills *" in manifest
    assert "recursive-include scripts *" in manifest
    assert "include docs/canonical-vocabulary.yaml" in manifest


def test_release_candidate_workflow_qualifies_both_distribution_forms() -> None:
    workflow = _read(".github/workflows/release-candidate.yml")

    assert "python -m build" in workflow
    assert "python -m twine check dist/*" in workflow
    assert "sensemaking_skills-0.3.0-py3-none-any.whl" in workflow
    assert "sensemaking_skills-0.3.0.tar.gz" in workflow
    assert "Fresh wheel install proof" in workflow
    assert "Fresh sdist install proof" in workflow
    assert 'ref: ${{ github.event.pull_request.head.sha || github.sha }}' in workflow


def test_tag_publish_workflow_checks_metadata_before_upload() -> None:
    workflow = _read(".github/workflows/publish.yml")
    check_index = workflow.index("python -m twine check dist/*")
    upload_index = workflow.index("python -m twine upload dist/*")
    assert check_index < upload_index
