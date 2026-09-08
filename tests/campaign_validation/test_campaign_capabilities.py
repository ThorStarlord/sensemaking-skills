"""P6 qualification for real, unranked capability inspection."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import Authority, CampaignState, Responsibility
from sensemaking_skills.campaign_semantics.models import Capability
from sensemaking_skills.campaign_semantics.registry import (
    AvailabilityStatus,
    CapabilityRegistry,
    RegisteredCapability,
)
from sensemaking_skills.campaigns import (
    AdvanceDecision,
    CampaignDecisionService,
    CampaignService,
    CampaignTransactionError,
)
from sensemaking_skills.campaigns.capabilities import (
    CampaignCapabilityService,
    CapabilityCatalogError,
    load_capability_registry,
)
from sensemaking_skills.cli import CAMPAIGN_WORKSPACE_EXIT, cli


REPO_ROOT = Path(__file__).resolve().parents[2]


def _initialize_active(workspace: Path, *, authority: Authority = Authority.AUTHORIZED_AUTONOMOUSLY) -> None:
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-P6",
            mission="inspect real capabilities without semantic routing",
            status="active",
            current_state="initialized",
        )
    )
    CampaignDecisionService(workspace).advance(
        AdvanceDecision(
            transition_id="TR-P6-ACTIVE",
            to_state="responsibility_active",
            decision="the agent explicitly authored the responsibility before capability inspection",
            next_responsibility=Responsibility(
                id="R-P6",
                statement="inspect declared capabilities for this responsibility",
                trigger_evidence=(),
                decision_blocked="which capability, if any, the agent should select",
                scope="P6 capability inspection only",
                authority=authority,
                success_conditions=("candidate metadata is visible without routing",),
            ),
        )
    )


def _mapping_keys(value: Any) -> tuple[str, ...]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.append(str(key))
            keys.extend(_mapping_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.extend(_mapping_keys(nested))
    return tuple(keys)


def test_default_catalog_loads_real_skill_and_workflow_identities() -> None:
    registry = load_capability_registry()

    repo = registry.get("repo-sensemaker")
    assert repo is not None
    assert repo.kind == "skill"
    assert repo.capability.accepted_responsibility_types == ("repository_diagnosis",)
    assert repo.availability is AvailabilityStatus.EXTERNAL

    active_workflow = registry.get("fast-path-workflow")
    assert active_workflow is not None
    assert active_workflow.kind == "workflow"
    assert active_workflow.availability is AvailabilityStatus.EXTERNAL

    compatibility = registry.get("implementation-workflow")
    assert compatibility is not None
    assert compatibility.availability is AvailabilityStatus.UNAVAILABLE
    assert "compatibility_only" in compatibility.availability_reason


def test_packaged_skill_capability_outputs_match_canonical_skill_registry() -> None:
    catalog = yaml.safe_load(
        (REPO_ROOT / "src/sensemaking_skills/defaults/capability-registry.yaml").read_text(
            encoding="utf-8"
        )
    )
    skill_registry = yaml.safe_load(
        (REPO_ROOT / "skills/workflow-planner/references/skill-registry.yaml").read_text(
            encoding="utf-8"
        )
    )

    canonical: dict[str, dict] = {}
    for ecosystem in skill_registry["ecosystems"].values():
        for skill in ecosystem.get("skills", []):
            canonical[skill["id"]] = skill

    for item in catalog["capabilities"]:
        if item["kind"] != "skill":
            continue
        assert item["id"] in canonical, (
            f"P6 capability {item['id']!r} is not a canonical Skill registry identity"
        )
        assert item["output_artifact"] == canonical[item["id"]].get("artifact"), (
            f"P6 output contract drift for {item['id']!r}"
        )


def test_proposed_and_deprecated_skill_identities_do_not_masquerade_as_available() -> None:
    registry = load_capability_registry()

    triage = registry.get("triage")
    tdd = registry.get("tdd")
    assert triage is not None and triage.availability is AvailabilityStatus.UNAVAILABLE
    assert tdd is not None and tdd.availability is AvailabilityStatus.UNAVAILABLE
    assert "proposed" in triage.availability_reason
    assert "deprecated" in tdd.availability_reason


def test_catalog_rejects_duplicate_ids_fail_closed(tmp_path: Path) -> None:
    catalog = tmp_path / "capability-registry.yaml"
    catalog.write_text(
        """schema_version: \"1\"\ncapabilities:\n  - &item\n    id: repo-sensemaker\n    kind: skill\n    source: test\n    accepted_responsibility_types: [test]\n    output_artifact: repository_sensemaking_brief\n    mutates_repository: false\n    authority: authorized_autonomously\n    availability: external\n    availability_reason: shipped Skill used to exercise duplicate detection\n    returns_control: true\n  - <<: *item\n""",
        encoding="utf-8",
    )

    with pytest.raises(CapabilityCatalogError, match="duplicate capability id"):
        load_capability_registry(catalog_path=catalog)


def test_catalog_rejects_unknown_fields_fail_closed(tmp_path: Path) -> None:
    catalog = tmp_path / "capability-registry.yaml"
    catalog.write_text(
        """schema_version: \"1\"\ncapabilities:\n  - id: malformed\n    kind: skill\n    source: test\n    accepted_responsibility_types: [test]\n    output_artifact: result\n    mutates_repository: false\n    authority: authorized_autonomously\n    availability: unknown\n    availability_reason: test identity is intentionally unresolved\n    returns_control: true\n    semantic_score: 0.99\n""",
        encoding="utf-8",
    )

    with pytest.raises(CapabilityCatalogError, match="unknown fields"):
        load_capability_registry(catalog_path=catalog)


def test_catalog_rejects_live_skill_identity_without_shipped_implementation(tmp_path: Path) -> None:
    catalog = tmp_path / "capability-registry.yaml"
    catalog.write_text(
        """schema_version: \"1\"\ncapabilities:\n  - id: invented-live-skill\n    kind: skill\n    source: test\n    accepted_responsibility_types: [test]\n    output_artifact: result\n    mutates_repository: false\n    authority: authorized_autonomously\n    availability: external\n    availability_reason: claimed external capability for qualification\n    returns_control: true\n""",
        encoding="utf-8",
    )

    with pytest.raises(CapabilityCatalogError, match="no current shipped Skill implementation"):
        load_capability_registry(catalog_path=catalog)


def test_catalog_requires_reason_for_non_available_status(tmp_path: Path) -> None:
    catalog = tmp_path / "capability-registry.yaml"
    catalog.write_text(
        """schema_version: \"1\"\ncapabilities:\n  - id: repo-sensemaker\n    kind: skill\n    source: test\n    accepted_responsibility_types: [test]\n    output_artifact: repository_sensemaking_brief\n    mutates_repository: false\n    authority: authorized_autonomously\n    availability: external\n    returns_control: true\n""",
        encoding="utf-8",
    )

    with pytest.raises(CapabilityCatalogError, match="availability_reason is required"):
        load_capability_registry(catalog_path=catalog)


def test_catalog_rejects_non_string_availability_reason(tmp_path: Path) -> None:
    catalog = tmp_path / "capability-registry.yaml"
    catalog.write_text(
        """schema_version: \"1\"\ncapabilities:\n  - id: repo-sensemaker\n    kind: skill\n    source: test\n    accepted_responsibility_types: [test]\n    output_artifact: repository_sensemaking_brief\n    mutates_repository: false\n    authority: authorized_autonomously\n    availability: external\n    availability_reason: [not, text]\n    returns_control: true\n""",
        encoding="utf-8",
    )

    with pytest.raises(CapabilityCatalogError, match="availability_reason must be a string"):
        load_capability_registry(catalog_path=catalog)


def test_inspection_requires_active_responsibility(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-P6-NONE",
            mission="prove detached capability lookup fails closed",
            status="active",
            current_state="initialized",
        )
    )

    with pytest.raises(CampaignTransactionError, match="requires one active responsibility"):
        CampaignCapabilityService(workspace).inspect("architecture_review")


def test_service_returns_deterministic_unranked_candidate_order(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize_active(workspace)
    registry = CapabilityRegistry(
        [
            RegisteredCapability(
                capability=Capability("zeta", ("test_type",), "zeta_result"),
                kind="skill",
                mutates_repository=False,
                authority=Authority.AUTHORIZED_AUTONOMOUSLY,
                availability=AvailabilityStatus.UNKNOWN,
            ),
            RegisteredCapability(
                capability=Capability("alpha", ("test_type",), "alpha_result"),
                kind="skill",
                mutates_repository=False,
                authority=Authority.AUTHORIZED_AUTONOMOUSLY,
                availability=AvailabilityStatus.UNKNOWN,
            ),
        ]
    )

    result = CampaignCapabilityService(workspace).inspect(
        "test_type", registry=registry
    )
    assert [item.capability.id for item in result.candidates] == ["alpha", "zeta"]


def test_cli_exposes_candidates_without_routing_fields(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize_active(workspace)
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "campaign",
            "capabilities",
            "--workspace",
            str(workspace),
            "--responsibility-type",
            "architecture_review",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_CAPABILITIES"
    assert payload["responsibility_id"] == "R-P6"
    assert payload["responsibility_type"] == "architecture_review"
    assert payload["responsibility_authority"] == "authorized_autonomously"
    assert payload["candidate_count"] == 1
    assert payload["candidates"][0]["id"] == "architectural-review"
    assert payload["candidates"][0]["availability"] == "external"
    assert payload["candidates"][0]["required_authority"] == "authorized_autonomously"

    forbidden_key_markers = ("recommend", "rank", "score", "best", "selected")
    for key in _mapping_keys(payload):
        lowered = key.lower()
        assert all(marker not in lowered for marker in forbidden_key_markers), key


def test_cli_unknown_responsibility_type_is_honest_empty_success(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize_active(workspace)
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "campaign",
            "capabilities",
            "--workspace",
            str(workspace),
            "--responsibility-type",
            "owner_defined_unmapped_type",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["candidate_count"] == 0
    assert payload["candidates"] == []


def test_cli_keeps_responsibility_authority_separate_from_capability_requirement(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize_active(workspace, authority=Authority.AUTHORIZED_AUTONOMOUSLY)
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "campaign",
            "capabilities",
            "--workspace",
            str(workspace),
            "--responsibility-type",
            "documentation_alignment",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    candidate = payload["candidates"][0]
    assert payload["responsibility_authority"] == "authorized_autonomously"
    assert candidate["required_authority"] == "owner_authorization_required"
    assert candidate["availability"] == "external"
    assert "authorized" not in candidate


def test_cli_reports_compatibility_only_workflow_as_unavailable(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize_active(workspace)
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "campaign",
            "capabilities",
            "--workspace",
            str(workspace),
            "--responsibility-type",
            "implementation_execution_workflow",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["candidate_count"] == 1
    candidate = payload["candidates"][0]
    assert candidate["id"] == "implementation-workflow"
    assert candidate["availability"] == "unavailable"
    assert "compatibility_only" in candidate["availability_reason"]


def test_cli_does_not_infer_type_from_responsibility_prose(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    _initialize_active(workspace)
    runner = CliRunner()

    result = runner.invoke(
        cli,
        ["campaign", "capabilities", "--workspace", str(workspace), "--json"],
    )

    assert result.exit_code == 2
    assert "--responsibility-type" in result.output


def test_cli_without_active_responsibility_uses_existing_campaign_failure_class(tmp_path: Path) -> None:
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-P6-NONE-CLI",
            mission="prove capability inspection is campaign contextual",
            status="active",
            current_state="initialized",
        )
    )
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "campaign",
            "capabilities",
            "--workspace",
            str(workspace),
            "--responsibility-type",
            "architecture_review",
            "--json",
        ],
    )

    assert result.exit_code == CAMPAIGN_WORKSPACE_EXIT
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_TRANSACTION_ERROR"
    assert "requires one active responsibility" in payload["message"]
