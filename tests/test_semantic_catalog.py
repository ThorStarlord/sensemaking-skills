"""Read-only Skill Manifest / Domain Pack catalog qualification."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.cli import cli


ROOT = Path(__file__).resolve().parents[1]


def test_semantic_catalog_filters_exact_skill_without_selection():
    result = CliRunner().invoke(
        cli,
        [
            "semantic",
            "catalog",
            "--manifests-dir",
            str(ROOT / "skill-manifests"),
            "--domain-packs-dir",
            str(ROOT / "domain-packs"),
            "--repo-root",
            str(ROOT),
            "--skill-id",
            "repo-sensemaker",
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "SEMANTIC_CATALOG"
    assert payload["skill_manifest_count"] == 1
    manifest = payload["skill_manifests"][0]
    assert manifest["skill_id"] == "repo-sensemaker"
    assert manifest["canonical_skill_exists"] is True
    assert payload["selection_performed"] is False
    assert payload["semantic_truth_established"] is False
    assert "rank" in payload["explicit_limit"]


def test_semantic_catalog_filters_engineering_domain_and_exposes_pack():
    result = CliRunner().invoke(
        cli,
        [
            "semantic",
            "catalog",
            "--manifests-dir",
            str(ROOT / "skill-manifests"),
            "--domain-packs-dir",
            str(ROOT / "domain-packs"),
            "--repo-root",
            str(ROOT),
            "--domain-id",
            "engineering",
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["repository_conformance_valid"] is True
    assert payload["domain_pack_count"] == 1
    pack = payload["domain_packs"][0]
    assert pack["domain_id"] == "engineering"
    assert "skill-manifests/repo-sensemaker.yaml" in pack["skill_manifests"]
    assert payload["skill_manifest_count"] >= 4


def test_semantic_catalog_rejects_blank_filter():
    result = CliRunner().invoke(
        cli,
        [
            "semantic",
            "catalog",
            "--manifests-dir",
            str(ROOT / "skill-manifests"),
            "--skill-id",
            "   ",
            "--json",
        ],
    )
    assert result.exit_code != 0
    assert "must be non-empty" in result.output
