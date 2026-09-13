from __future__ import annotations

from pathlib import Path

import yaml

from sensemaking_skills import cli


ROOT = Path(__file__).resolve().parents[1]


def test_json_contract_matches_payload_builders() -> None:
    contract = yaml.safe_load(
        (ROOT / "docs" / "cli-json-contract-v1.0.yaml").read_text(encoding="utf-8")
    )
    assert contract["schema_version"] == 1

    status = cli._status_payload(type("Snapshot", (), {
        "state": type("State", (), {
            "campaign_id": "CMP-1", "mission": "m", "schema_version": "2",
            "status": "active", "current_state": "initialized", "authority": None,
            "terminal_state": None, "active_responsibility": None,
            "active_uncertainty": None,
        })(),
        "transitions": (), "evidence_refs": (), "policy": None, "handoff": None,
    })())
    history = cli._history_payload(type("Snapshot", (), {
        "state": type("State", (), {"campaign_id": "CMP-1", "current_state": "initialized"})(),
        "trace": type("Trace", (), {"initial_state": "initialized"})(),
        "transitions": (),
    })())

    assert set(contract["commands"]["campaign-status"]["success_required"]) <= status.keys() | {"code"}
    assert set(contract["commands"]["campaign-history"]["success_required"]) <= history.keys() | {"code"}
    assert set(contract["commands"]["campaign-validate"]["success_required"]) == {
        "ok", "valid", "code", "diagnostics"
    }
