"""P5 qualification for explicit agent-authored campaign decisions."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

from sensemaking_skills.campaign_semantics import (
    Authority,
    CampaignState,
    Responsibility,
    TerminalState,
)
from sensemaking_skills.campaigns import (
    AdvanceDecision,
    CampaignDecisionService,
    CampaignService,
    CampaignTransactionError,
    CloseDecision,
    DeferDecision,
)
from sensemaking_skills.cli import CAMPAIGN_WORKSPACE_EXIT, cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def _initialize(workspace: Path, *, campaign_id: str = "CMP-P5") -> CampaignService:
    service = CampaignService(workspace)
    service.initialize(
        CampaignState(
            campaign_id=campaign_id,
            mission="persist explicit agent-authored campaign decisions",
            status="active",
            current_state="initialized",
        )
    )
    return service


def _responsibility(
    *,
    evidence: tuple[str, ...] = (),
    authority: Authority = Authority.AUTHORIZED_AUTONOMOUSLY,
) -> Responsibility:
    return Responsibility(
        id="R-P5-1",
        statement="perform the bounded P5 responsibility selected by the agent",
        trigger_evidence=evidence,
        decision_blocked="whether this bounded responsibility is complete",
        scope="P5 decision qualification only",
        authority=authority,
        success_conditions=("explicit durable decision is reconstructible",),
    )


def _advance_args(workspace: Path, *, evidence: str | None = None) -> list[str]:
    args = [
        "campaign",
        "advance",
        "--workspace",
        str(workspace),
        "--transition-id",
        "TR-P5-ADVANCE",
        "--to-state",
        "bounded_work",
        "--decision",
        "the admitted evidence warrants one bounded responsibility",
        "--responsibility-id",
        "R-P5-1",
        "--responsibility-statement",
        "perform the bounded P5 responsibility selected by the agent",
        "--decision-blocked",
        "whether this bounded responsibility is complete",
        "--scope",
        "P5 decision qualification only",
        "--authority",
        Authority.AUTHORIZED_AUTONOMOUSLY.value,
        "--success-condition",
        "explicit durable decision is reconstructible",
        "--json",
    ]
    if evidence is not None:
        args.extend(["--evidence", evidence])
    return args


def test_advance_persists_exact_agent_authored_responsibility_and_fresh_resume(tmp_path):
    workspace = tmp_path / "campaign"
    service = _initialize(workspace)
    evidence_path = service.store.workspace.evidence_dir / "brief.md"
    evidence_path.write_text("validated decision evidence", encoding="utf-8")
    evidence_ref = "evidence/brief.md"

    authored = AdvanceDecision(
        transition_id="TR-P5-ADVANCE",
        to_state="bounded_work",
        decision="the evidence warrants one bounded responsibility",
        evidence=(evidence_ref,),
        next_responsibility=_responsibility(evidence=(evidence_ref,)),
    )

    snapshot = CampaignDecisionService(workspace).advance(authored)

    assert snapshot.state.current_state == "bounded_work"
    assert snapshot.state.status == "active"
    assert snapshot.state.active_responsibility == authored.next_responsibility
    assert snapshot.state.authority is Authority.AUTHORIZED_AUTONOMOUSLY
    assert snapshot.transitions[-1].id == "TR-P5-ADVANCE"
    assert snapshot.transitions[-1].evidence == (evidence_ref,)
    assert snapshot.transitions[-1].next_responsibility == "R-P5-1"
    # Transition authority describes the source decision boundary; the new
    # responsibility carries its own explicit authority in the replacement state.
    assert snapshot.transitions[-1].authority is None

    fresh = CampaignService(workspace).resume()
    assert fresh.state == snapshot.state
    assert fresh.transitions == snapshot.transitions
    assert fresh.trace == snapshot.trace


def test_advance_rejects_missing_trigger_evidence_before_lifecycle_commit(tmp_path):
    workspace = tmp_path / "campaign"
    service = _initialize(workspace)

    with pytest.raises(CampaignTransactionError, match="missing trigger evidence"):
        CampaignDecisionService(workspace).advance(
            AdvanceDecision(
                transition_id="TR-MISSING",
                to_state="bounded_work",
                decision="do not fabricate evidence",
                evidence=("evidence/missing.md",),
                next_responsibility=_responsibility(
                    evidence=("evidence/missing.md",)
                ),
            )
        )

    assert service.store.load_state().current_state == "initialized"
    assert service.store.load_transitions() == ()


def test_defer_uses_existing_p2_primitive_and_preserves_reopen_contract(tmp_path):
    workspace = tmp_path / "campaign"
    service = _initialize(workspace)
    CampaignDecisionService(workspace).advance(
        AdvanceDecision(
            transition_id="TR-ADVANCE",
            to_state="bounded_work",
            decision="begin the selected bounded responsibility",
            next_responsibility=_responsibility(),
        )
    )

    snapshot = CampaignDecisionService(workspace).defer(
        DeferDecision(
            transition_id="TR-DEFER",
            to_state="awaiting_dependency",
            decision="defer rather than invent progress",
            reason="an external dependency is not available",
            reopen_when=("the dependency becomes available",),
            not_reopened_by=("elapsed time alone",),
        )
    )

    assert snapshot.state.current_state == "awaiting_dependency"
    assert snapshot.state.active_responsibility is None
    assert snapshot.state.authority is None
    assert snapshot.state.deferred_responsibilities[-1].responsibility_id == "R-P5-1"
    assert snapshot.state.deferred_responsibilities[-1].reopen_when == (
        "the dependency becomes available",
    )
    assert snapshot.state.deferred_responsibilities[-1].not_reopened_by == (
        "elapsed time alone",
    )
    assert snapshot.transitions[-1].id == "TR-DEFER"
    assert service.validate().valid


def test_close_persists_terminal_decision_and_later_advance_fails_closed(tmp_path):
    workspace = tmp_path / "campaign"
    _initialize(workspace)

    closed = CampaignDecisionService(workspace).close(
        CloseDecision(
            transition_id="TR-CLOSE",
            to_state="owner_boundary",
            decision="the next decision belongs to the owner",
            terminal_state=TerminalState.OWNER_DECISION_REQUIRED,
        )
    )

    assert closed.state.status == "terminal"
    assert closed.state.current_state == "owner_boundary"
    assert closed.state.terminal_state is TerminalState.OWNER_DECISION_REQUIRED
    assert closed.transitions[-1].terminal_state is TerminalState.OWNER_DECISION_REQUIRED

    with pytest.raises(CampaignTransactionError, match="terminal campaigns cannot advance"):
        CampaignDecisionService(workspace).advance(
            AdvanceDecision(
                transition_id="TR-ILLEGAL",
                to_state="illegal",
                decision="must not advance a terminal campaign",
                next_responsibility=_responsibility(),
            )
        )

    fresh = CampaignService(workspace).resume()
    assert fresh.state == closed.state
    assert fresh.transitions == closed.transitions


def test_cli_advance_json_exposes_exact_authored_decision_without_recommendation(
    runner, tmp_path
):
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    evidence_path = workspace / "evidence" / "brief.md"
    evidence_path.write_text("decision evidence", encoding="utf-8")

    result = runner.invoke(
        cli,
        _advance_args(workspace, evidence="evidence/brief.md"),
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_ADVANCED"
    assert payload["current_state"] == "bounded_work"
    assert payload["authority"] == Authority.AUTHORIZED_AUTONOMOUSLY.value
    assert payload["active_responsibility"]["id"] == "R-P5-1"
    assert payload["active_responsibility"]["trigger_evidence"] == [
        "evidence/brief.md"
    ]
    assert payload["transition"]["id"] == "TR-P5-ADVANCE"
    assert payload["transition"]["evidence"] == ["evidence/brief.md"]
    encoded = json.dumps(payload).lower()
    assert "suggested next" not in encoded
    assert "recommended capability" not in encoded


def test_cli_advance_rejects_orphan_artifact_that_is_not_admitted_evidence(
    runner, tmp_path
):
    workspace = tmp_path / "campaign"
    _initialize(workspace)
    orphan = workspace / "artifacts" / "orphan.md"
    orphan.write_text("looks like an artifact but has no admission receipt", encoding="utf-8")

    result = runner.invoke(
        cli,
        _advance_args(workspace, evidence="artifacts/orphan.md"),
    )

    assert result.exit_code == CAMPAIGN_WORKSPACE_EXIT
    payload = json.loads(result.output)
    assert payload["code"] == "CAMPAIGN_TRANSACTION_ERROR"
    assert "missing trigger evidence" in payload["message"]
    fresh = CampaignService(workspace).resume()
    assert fresh.state.current_state == "initialized"
    assert fresh.transitions == ()


def test_cli_defer_and_close_have_stable_json_surfaces(runner, tmp_path):
    defer_workspace = tmp_path / "defer-campaign"
    _initialize(defer_workspace, campaign_id="CMP-P5-DEFER")
    advance = runner.invoke(cli, _advance_args(defer_workspace))
    assert advance.exit_code == 0, advance.output

    deferred = runner.invoke(
        cli,
        [
            "campaign",
            "defer",
            "--workspace",
            str(defer_workspace),
            "--transition-id",
            "TR-P5-DEFER",
            "--to-state",
            "awaiting_dependency",
            "--decision",
            "defer at the explicit dependency boundary",
            "--reason",
            "dependency unavailable",
            "--reopen-when",
            "dependency becomes available",
            "--not-reopened-by",
            "elapsed time alone",
            "--json",
        ],
    )
    assert deferred.exit_code == 0, deferred.output
    deferred_payload = json.loads(deferred.output)
    assert deferred_payload["code"] == "CAMPAIGN_DEFERRED"
    assert deferred_payload["current_state"] == "awaiting_dependency"
    assert deferred_payload["active_responsibility"] is None
    assert deferred_payload["transition"]["id"] == "TR-P5-DEFER"

    close_workspace = tmp_path / "close-campaign"
    _initialize(close_workspace, campaign_id="CMP-P5-CLOSE")
    closed = runner.invoke(
        cli,
        [
            "campaign",
            "close",
            "--workspace",
            str(close_workspace),
            "--transition-id",
            "TR-P5-CLOSE",
            "--to-state",
            "qualified",
            "--decision",
            "the exact candidate is qualified and ready for owner merge",
            "--terminal-state",
            TerminalState.QUALIFIED_PR_READY.value,
            "--json",
        ],
    )
    assert closed.exit_code == 0, closed.output
    closed_payload = json.loads(closed.output)
    assert closed_payload["code"] == "CAMPAIGN_CLOSED"
    assert closed_payload["status"] == "terminal"
    assert closed_payload["terminal_state"] == TerminalState.QUALIFIED_PR_READY.value
    assert closed_payload["transition"]["terminal_state"] == (
        TerminalState.QUALIFIED_PR_READY.value
    )


def test_cli_advance_survives_fresh_process_reconstruction(tmp_path):
    workspace = tmp_path / "campaign"
    base = [sys.executable, "-m", "sensemaking_skills.cli", "campaign"]

    initialized = subprocess.run(
        [
            *base,
            "init",
            "--workspace",
            str(workspace),
            "--campaign-id",
            "CMP-P5-SUBPROCESS",
            "--mission",
            "prove P5 fresh-process decision reconstruction",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert initialized.returncode == 0, initialized.stderr or initialized.stdout

    evidence_path = workspace / "evidence" / "brief.md"
    evidence_path.write_text("fresh-process evidence", encoding="utf-8")

    advanced = subprocess.run(
        [
            *base,
            "advance",
            "--workspace",
            str(workspace),
            "--transition-id",
            "TR-P5-SUBPROCESS",
            "--to-state",
            "bounded_work",
            "--decision",
            "agent explicitly selects one bounded responsibility",
            "--evidence",
            "evidence/brief.md",
            "--responsibility-id",
            "R-P5-SUBPROCESS",
            "--responsibility-statement",
            "perform the explicitly selected responsibility",
            "--decision-blocked",
            "whether the responsibility is complete",
            "--scope",
            "fresh-process P5 proof",
            "--authority",
            Authority.AUTHORIZED_AUTONOMOUSLY.value,
            "--success-condition",
            "fresh process reconstructs the decision",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert advanced.returncode == 0, advanced.stderr or advanced.stdout
    assert json.loads(advanced.stdout)["code"] == "CAMPAIGN_ADVANCED"

    status = subprocess.run(
        [*base, "status", "--workspace", str(workspace), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert status.returncode == 0, status.stderr or status.stdout
    status_payload = json.loads(status.stdout)
    assert status_payload["current_state"] == "bounded_work"
    assert status_payload["active_responsibility"]["id"] == "R-P5-SUBPROCESS"

    history = subprocess.run(
        [*base, "history", "--workspace", str(workspace), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert history.returncode == 0, history.stderr or history.stdout
    history_payload = json.loads(history.stdout)
    assert history_payload["transition_count"] == 1
    assert history_payload["transitions"][0]["id"] == "TR-P5-SUBPROCESS"
