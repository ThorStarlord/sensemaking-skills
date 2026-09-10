"""CLI integration tests for the mechanical Semantic Architecture substrate."""

from __future__ import annotations

import json

from click.testing import CliRunner

from sensemaking_skills.cli import cli


def test_semantic_probe_and_map_build_roundtrip(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "app.py").write_text("import json\n# marker\n", encoding="utf-8")
    probe_path = tmp_path / "probe.json"
    semantic_map_path = tmp_path / "map.json"
    runner = CliRunner()

    probe = runner.invoke(
        cli,
        [
            "semantic",
            "probe",
            "--repo",
            str(repo),
            "--target-ref",
            "sha:test",
            "--kind",
            "python-imports",
            "--output",
            str(probe_path),
            "--json",
        ],
    )
    assert probe.exit_code == 0, probe.output
    probe_payload = json.loads(probe.output)
    assert probe_payload["code"] == "SEMANTIC_PROBE_COMPLETE"
    assert probe_payload["semantic_truth_established"] is False
    assert probe_path.is_file()

    semantic_map = runner.invoke(
        cli,
        [
            "semantic",
            "map-build",
            "--map-id",
            "MAP-CLI",
            "--target-ref",
            "sha:test",
            "--observations",
            str(probe_path),
            "--output",
            str(semantic_map_path),
            "--json",
        ],
    )
    assert semantic_map.exit_code == 0, semantic_map.output
    map_payload = json.loads(semantic_map.output)
    assert map_payload["code"] == "REPOSITORY_SEMANTIC_MAP_BUILT"
    assert map_payload["semantic_truth_established"] is False
    assert semantic_map_path.is_file()


def test_semantic_exact_search_requires_explicit_pattern(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    result = CliRunner().invoke(
        cli,
        [
            "semantic",
            "probe",
            "--repo",
            str(repo),
            "--target-ref",
            "sha:test",
            "--kind",
            "exact-search",
        ],
    )
    assert result.exit_code != 0
    assert "--pattern is required" in result.output


def test_semantic_state_cli_is_append_only_and_parent_checked(tmp_path):
    path = tmp_path / "semantic-state.jsonl"
    runner = CliRunner()
    first = runner.invoke(
        cli,
        [
            "semantic",
            "state-append",
            "--state-file",
            str(path),
            "--entry-id",
            "S1",
            "--source-skill",
            "repo-sensemaker",
            "--artifact-ref",
            "brief.md",
            "--target-ref",
            "sha:test",
            "--json",
        ],
    )
    assert first.exit_code == 0, first.output

    second = runner.invoke(
        cli,
        [
            "semantic",
            "state-append",
            "--state-file",
            str(path),
            "--entry-id",
            "S2",
            "--source-skill",
            "architectural-review",
            "--artifact-ref",
            "review.md",
            "--target-ref",
            "sha:test",
            "--parent",
            "S1",
            "--json",
        ],
    )
    assert second.exit_code == 0, second.output

    shown = runner.invoke(
        cli,
        ["semantic", "state-show", "--state-file", str(path), "--json"],
    )
    assert shown.exit_code == 0, shown.output
    payload = json.loads(shown.output)
    assert payload["code"] == "SEMANTIC_STATE_VALID"
    assert len(payload["records"]) == 2


def test_repository_conformance_cli_accepts_checked_in_manifests():
    result = CliRunner().invoke(
        cli,
        [
            "semantic",
            "conformance",
            "--manifests-dir",
            "skill-manifests",
            "--domain-packs-dir",
            "domain-packs",
            "--repo-root",
            ".",
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "SEMANTIC_CONFORMANCE_VALID"
    assert payload["skill_manifest_count"] >= 31
    assert payload["domain_pack_count"] >= 2
    assert payload["semantic_truth_established"] is False
