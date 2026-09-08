from __future__ import annotations

from sensemaking_skills.campaign_semantics import (
    Authority,
    CampaignState,
    Responsibility,
    TerminalState,
)
from sensemaking_skills.campaigns import (
    AdvanceDecision,
    CampaignDecisionService,
    CampaignLineageService,
    CampaignService,
    CloseDecision,
    DeferDecision,
)


def _initialize(workspace, campaign_id: str) -> None:
    CampaignService(workspace).initialize(
        CampaignState(
            campaign_id=campaign_id,
            mission="prove lineage for every P5 decision surface",
            status="active",
            current_state="initialized",
        )
    )


def _responsibility() -> Responsibility:
    return Responsibility(
        id="R-LINEAGE",
        statement="exercise explicit authored decision lineage",
        trigger_evidence=(),
        decision_blocked="which authored lifecycle decision follows",
        scope="P8 decision-path qualification",
        authority=Authority.AUTHORIZED_AUTONOMOUSLY,
        success_conditions=("decision lineage is bound",),
    )


def test_defer_decision_gets_bound_consumption_receipt(tmp_path):
    workspace = tmp_path / "defer"
    _initialize(workspace, "CMP-P8-DEFER")
    decisions = CampaignDecisionService(workspace)
    decisions.advance(
        AdvanceDecision(
            transition_id="TR-START",
            to_state="work",
            decision="begin explicit bounded work",
            next_responsibility=_responsibility(),
        )
    )
    evidence = workspace / "evidence" / "dependency.md"
    evidence.write_text("dependency unavailable", encoding="utf-8")

    decisions.defer(
        DeferDecision(
            transition_id="TR-DEFER",
            to_state="awaiting_dependency",
            decision="defer at the explicit dependency boundary",
            reason="dependency unavailable",
            evidence=("evidence/dependency.md",),
        )
    )

    lineage = CampaignLineageService(workspace).inspect()
    by_id = {item.transition_id: item for item in lineage.transitions}
    assert by_id["TR-START"].binding_status == "bound"
    assert by_id["TR-DEFER"].binding_status == "bound"
    edges = [edge for edge in lineage.consumption_edges if edge.transition_id == "TR-DEFER"]
    assert len(edges) == 1
    assert edges[0].evidence_ref == "evidence/dependency.md"
    assert edges[0].consumed_sha256 is not None


def test_close_decision_gets_bound_consumption_receipt(tmp_path):
    workspace = tmp_path / "close"
    _initialize(workspace, "CMP-P8-CLOSE")
    evidence = workspace / "evidence" / "qualification.md"
    evidence.write_text("bounded qualification result", encoding="utf-8")

    CampaignDecisionService(workspace).close(
        CloseDecision(
            transition_id="TR-CLOSE",
            to_state="qualified",
            decision="agent explicitly classifies the Campaign as qualified",
            terminal_state=TerminalState.QUALIFIED_PR_READY,
            evidence=("evidence/qualification.md",),
        )
    )

    lineage = CampaignLineageService(workspace).inspect()
    assert lineage.transitions[0].transition_id == "TR-CLOSE"
    assert lineage.transitions[0].binding_status == "bound"
    assert lineage.transitions[0].receipt_ref is not None
    assert lineage.consumption_edges[0].evidence_ref == "evidence/qualification.md"
    assert lineage.consumption_edges[0].binding_status == "bound"
