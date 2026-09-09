from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from sensemaking_skills.campaign_schema_cli import main as schema_cli
from sensemaking_skills.campaign_semantics import (
    CURRENT_SCHEMA_VERSION,
    CampaignState,
    ContractError,
    dump_campaign_state,
    load_campaign_handoff,
    load_campaign_state,
    migrate_payload,
)
from sensemaking_skills.campaigns import (
    CampaignSchemaEvolutionService,
    CampaignService,
    load_schema_migration_receipt,
)


def _legacy_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "campaign"
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id="CMP-SCHEMA",
            mission="prove schema evolution",
            status="active",
            current_state="initialized",
        )
    )
    for name in ("campaign-state.yaml", "trace.yaml"):
        path = workspace / name
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["schema_version"] = "1"
        if name == "campaign-state.yaml":
            payload["owner_routing"] = {"route_to": "owner"}
            payload.pop("extensions", None)
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    return workspace


def test_v1_state_migrates_to_v2_without_mutating_input():
    source = {
        "campaign_id": "c",
        "mission": "m",
        "status": "active",
        "current_state": "s",
        "schema_version": "1",
        "owner_routing": {"route_to": "owner"},
    }
    result = migrate_payload(source, artifact_kind="campaign_state")

    assert source["schema_version"] == "1"
    assert "owner_routing" in source
    assert result.source_version == "1"
    assert result.target_version == CURRENT_SCHEMA_VERSION
    assert result.payload["schema_version"] == CURRENT_SCHEMA_VERSION
    assert result.payload["extensions"]["owner_routing"] == {"route_to": "owner"}
    assert "owner_routing" not in result.payload

    model = load_campaign_state(source)
    assert model.schema_version == CURRENT_SCHEMA_VERSION
    assert model.extensions["owner_routing"]["route_to"] == "owner"


def test_v1_handoff_alias_and_embedded_state_migrate_together():
    handoff = load_campaign_handoff(
        {
            "campaign_id": "c",
            "schema_version": "1",
            "current_state": {
                "campaign_id": "c",
                "mission": "m",
                "status": "active",
                "current_state": "s",
                "schema_version": "1",
            },
            "allowed_actions": ["review"],
            "stop_conditions": ["owner_decision_required"],
        }
    )
    assert handoff.schema_version == CURRENT_SCHEMA_VERSION
    assert handoff.current_state.schema_version == CURRENT_SCHEMA_VERSION
    assert handoff.allowed_next_actions == ("review",)


def test_current_schema_rejects_legacy_alias_and_unknown_future_version():
    with pytest.raises(ContractError):
        load_campaign_handoff(
            {
                "campaign_id": "c",
                "schema_version": CURRENT_SCHEMA_VERSION,
                "current_state": {
                    "campaign_id": "c",
                    "mission": "m",
                    "status": "active",
                    "current_state": "s",
                    "schema_version": CURRENT_SCHEMA_VERSION,
                },
                "allowed_actions": ["review"],
                "stop_conditions": [],
            }
        )

    with pytest.raises(ContractError):
        load_campaign_state(
            {
                "campaign_id": "c",
                "mission": "m",
                "status": "active",
                "current_state": "s",
                "schema_version": "99",
            }
        )


def test_current_handoff_rejects_embedded_legacy_state():
    with pytest.raises(ContractError, match="legacy current_state"):
        load_campaign_handoff(
            {
                "campaign_id": "c",
                "schema_version": CURRENT_SCHEMA_VERSION,
                "current_state": {
                    "campaign_id": "c",
                    "mission": "m",
                    "status": "active",
                    "current_state": "s",
                    "schema_version": "1",
                },
                "allowed_next_actions": ["review"],
                "stop_conditions": [],
            }
        )


def test_new_dumps_are_current_schema():
    payload = dump_campaign_state(
        CampaignState(
            campaign_id="c",
            mission="m",
            status="active",
            current_state="s",
        )
    )
    assert payload["schema_version"] == CURRENT_SCHEMA_VERSION


def test_workspace_upgrade_writes_receipts_without_rewriting_legacy_bytes(tmp_path: Path):
    workspace = _legacy_workspace(tmp_path)
    state_before = (workspace / "campaign-state.yaml").read_bytes()
    trace_before = (workspace / "trace.yaml").read_bytes()

    service = CampaignSchemaEvolutionService(workspace)
    before = service.status()
    assert before.upgrade_required is True
    assert {item.migration_status for item in before.artifacts} == {"pending"}

    result = service.upgrade()
    assert result.after.qualified is True
    assert result.after.upgrade_required is False
    assert len(result.receipts_written) == 2
    assert (workspace / "campaign-state.yaml").read_bytes() == state_before
    assert (workspace / "trace.yaml").read_bytes() == trace_before
    assert {item.migration_status for item in result.after.artifacts} == {"qualified"}

    first_receipt = load_schema_migration_receipt(
        workspace / result.receipts_written[0]
    )
    assert first_receipt.migrated_payload["schema_version"] == CURRENT_SCHEMA_VERSION
    assert first_receipt.migrated_payload_sha256

    snapshot = CampaignService(workspace).resume()
    assert snapshot.state.schema_version == CURRENT_SCHEMA_VERSION
    assert snapshot.trace.schema_version == CURRENT_SCHEMA_VERSION


def test_receipts_are_exact_byte_bindings_and_stale_after_source_change(tmp_path: Path):
    workspace = _legacy_workspace(tmp_path)
    service = CampaignSchemaEvolutionService(workspace)
    service.upgrade()
    assert service.status().qualified is True

    state_path = workspace / "campaign-state.yaml"
    state_path.write_bytes(state_path.read_bytes() + b"\n")

    status = service.status()
    state_status = next(
        item for item in status.artifacts if item.artifact_ref == "campaign-state.yaml"
    )
    assert status.upgrade_required is True
    assert state_status.migration_status == "pending"
    assert state_status.receipt_ref is None


def test_upgrade_is_idempotent(tmp_path: Path):
    workspace = _legacy_workspace(tmp_path)
    service = CampaignSchemaEvolutionService(workspace)
    first = service.upgrade()
    second = service.upgrade()

    assert first.receipts_written
    assert second.receipts_written == ()
    assert second.after.qualified is True
    assert second.after.receipt_count == first.after.receipt_count


def test_agent_visible_cli_reports_and_upgrades(tmp_path: Path):
    workspace = _legacy_workspace(tmp_path)
    runner = CliRunner()

    status = runner.invoke(schema_cli, ["status", "--workspace", str(workspace), "--json"])
    assert status.exit_code == 0, status.output
    assert '"code": "CAMPAIGN_SCHEMA_UPGRADE_REQUIRED"' in status.output

    upgraded = runner.invoke(schema_cli, ["upgrade", "--workspace", str(workspace), "--json"])
    assert upgraded.exit_code == 0, upgraded.output
    assert '"code": "CAMPAIGN_SCHEMA_UPGRADED"' in upgraded.output

    current = runner.invoke(schema_cli, ["status", "--workspace", str(workspace), "--json"])
    assert current.exit_code == 0, current.output
    assert '"code": "CAMPAIGN_SCHEMA_CURRENT"' in current.output
