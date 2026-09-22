"""Qualification for Capability & Organization Tracer v0."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from sensemaking_skills.cli import cli


ROOT = Path(__file__).resolve().parents[1]


def test_default_repository_change_cell_is_mechanically_valid():
    result = CliRunner().invoke(
        cli,
        [
            "organization",
            "inspect",
            "--repo-root",
            str(ROOT),
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "ORGANIZATION_PATTERN_VALID"
    assert payload["valid"] is True
    assert payload["organization_id"] == "repository-change-cell-v0"
    assert len(payload["roles"]) == 5
    assert payload["selection_performed"] is False
    assert payload["authorization_granted"] is False
    assert payload["execution_performed"] is False

    builder = next(item for item in payload["roles"] if item["id"] == "builder")
    assert builder["covered_capabilities"] == ["repository_implementation"]
    assert builder["bindings"][0]["kind"] == "executor"
    assert builder["bindings"][0]["id"] == "external_coding_agent"


def test_skill_profile_combines_overlay_with_existing_manifest():
    result = CliRunner().invoke(
        cli,
        [
            "organization",
            "skill-profile",
            "--skill-id",
            "repair-verifier",
            "--repo-root",
            str(ROOT),
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    profile = payload["profile"]
    assert profile["package_role"] == "situated_skill"
    assert "bounded_verification" in profile["capability_families"]
    assert profile["canonical_skill_exists"] is True
    assert profile["manifest"]["domain"] == "engineering"
    assert profile["manifest"]["responsibilities"] == ["repair_verification"]
    assert profile["profile_overlay_authoritative"] is False
    assert payload["selection_performed"] is False


def test_role_view_exposes_edges_without_allocating_an_actor():
    result = CliRunner().invoke(
        cli,
        [
            "organization",
            "role",
            "--role-id",
            "reconciler",
            "--repo-root",
            str(ROOT),
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "ORGANIZATION_ROLE_VIEW"
    assert payload["role"]["id"] == "reconciler"
    assert payload["role"]["bindings"][0]["id"] == "output-reconciler"
    assert payload["selection_performed"] is False
    assert payload["authorization_granted"] is False
    assert payload["execution_performed"] is False
    assert payload["inbound_relationships"]
    assert payload["outbound_relationships"]


def test_inspect_fails_closed_when_required_capability_is_uncovered(tmp_path: Path):
    profiles = tmp_path / "profiles.yaml"
    profiles.write_text(
        """schema_version: 0
profiles:
  - skill_id: verifier
    package_role: situated_skill
    capability_families: [bounded_verification]
    typical_roles: [verifier]
    authority_posture: advise
    effect_boundary: read_only
""",
        encoding="utf-8",
    )
    pattern = tmp_path / "pattern.yaml"
    pattern.write_text(
        """schema_version: 0
organization_id: broken-cell
objective_class: test
roles:
  - id: verifier
    responsibility: verify
    capability_requirements: [evidence_reconciliation]
    authority: advise_only
    receives: []
    returns: []
    bindings:
      - kind: skill
        id: verifier
relationships: []
limits: []
""",
        encoding="utf-8",
    )

    result = CliRunner().invoke(
        cli,
        [
            "organization",
            "inspect",
            "--pattern",
            str(pattern),
            "--profiles",
            str(profiles),
            "--json",
        ],
    )
    assert result.exit_code == 3, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "ORGANIZATION_PATTERN_INVALID"
    assert any(
        item["code"] == "ORG_CAPABILITY_UNSATISFIED"
        for item in payload["diagnostics"]
    )
    assert payload["selection_performed"] is False


def test_status_selects_tracer_without_reopening_completed_milestones():
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
    assert (
        "ISSUE_459_CAPABILITY_ORGANIZATION_TRACER_V0 = "
        "ACTIVE_OWNER_DIRECTED_EXECUTABLE_TRACER"
    ) in status
    assert (
        "CURRENT CONSTRUCTION RESPONSIBILITY = "
        "CAPABILITY_ORGANIZATION_TRACER_V0"
    ) in status
    assert "PRIMARY CONSTRUCTION PROGRAM = ISSUE_459_EXECUTABLE_TRACER" in status
    assert (
        "ISSUE_416_STRATEGIC_CONTINUITY_RECONCILIATION_MULTI_REPO_V1 = "
        "COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF"
    ) in status
    assert (
        "POLICY_HIERARCHY_COMPLETION_V0 = "
        "COMPLETE_INTEGRATED_COMPOSABLE"
    ) in status
    assert "SYNTHETIC STRATEGICPLANNER TESTING = STOPPED" in status
