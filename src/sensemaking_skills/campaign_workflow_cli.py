"""Static agent-facing Campaign workflow navigation.

These paths describe composition of existing surfaces. They never inspect a
repository to choose a flow, execute steps, infer a responsibility, or grant
authority.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

import click


JsonEcho = Callable[[dict[str, Any]], None]


WORKFLOWS: dict[str, dict[str, Any]] = {
    "single-repository": {
        "purpose": "Start and finish consequential work in one explicitly selected repository.",
        "steps": [
            {"id": "inspect_strategy", "surface": "campaign strategy inspect", "decision_gate": False},
            {"id": "select_responsibility", "surface": "agent semantic judgment", "decision_gate": True},
            {"id": "handoff", "surface": "campaign strategy handoff", "decision_gate": False},
            {"id": "preflight", "surface": "campaign preflight", "decision_gate": False},
            {"id": "capability_context", "surface": "campaign capability-context --responsibility-type <explicit>", "decision_gate": False},
            {"id": "select_and_execute", "surface": "agent selects bounded capability / ordinary coding work", "decision_gate": True},
            {"id": "validate", "surface": "repository-native validation + Campaign evidence admission", "decision_gate": False},
            {"id": "terminal_decision", "surface": "campaign advance|defer|close", "decision_gate": True},
            {"id": "closeout", "surface": "campaign closeout (after terminal close only)", "decision_gate": False},
            {"id": "archive_optional", "surface": "campaign archive", "decision_gate": True},
        ],
    },
    "fresh-context": {
        "purpose": "Reconstruct an existing Campaign in a fresh agent/context without relying on chat memory.",
        "steps": [
            {"id": "resume", "surface": "campaign resume-profile --profile working", "decision_gate": False},
            {"id": "preflight", "surface": "campaign preflight", "decision_gate": False},
            {"id": "diagnose_if_needed", "surface": "campaign doctor", "decision_gate": False},
            {"id": "interpret", "surface": "agent decides whether current responsibility remains warranted", "decision_gate": True},
            {"id": "continue_or_stop", "surface": "bounded work or explicit Campaign decision", "decision_gate": True},
        ],
    },
    "transferred-campaign": {
        "purpose": "Inspect, import, and explicitly reconnect a transported Campaign without repository discovery.",
        "steps": [
            {"id": "inspect_bundle", "surface": "campaign bundle-inspect", "decision_gate": False},
            {"id": "preview_resume", "surface": "campaign bundle-resume-context", "decision_gate": False},
            {"id": "authorize_import", "surface": "agent/human import decision", "decision_gate": True},
            {"id": "import", "surface": "campaign bundle-import", "decision_gate": False},
            {"id": "rebind_primary", "surface": "campaign target rebind --target-repo <explicit-path>", "decision_gate": True},
            {"id": "rebind_additional", "surface": "campaign multi-target rebind --alias <explicit> --target-repo <explicit-path>", "decision_gate": True},
            {"id": "preflight", "surface": "campaign preflight", "decision_gate": False},
            {"id": "continue", "surface": "agent interprets reconstructed state and selects bounded continuation", "decision_gate": True},
        ],
    },
    "multi-repository": {
        "purpose": "Carry one explicit responsibility across an explicitly bounded repository target set.",
        "steps": [
            {"id": "select_responsibility", "surface": "agent semantic judgment", "decision_gate": True},
            {"id": "handoff", "surface": "campaign strategy handoff", "decision_gate": False},
            {"id": "add_targets", "surface": "campaign multi-target add", "decision_gate": True},
            {"id": "declare_relations", "surface": "campaign multi-target relate", "decision_gate": True},
            {"id": "verify_targets", "surface": "campaign multi-target verify", "decision_gate": False},
            {"id": "verify_relations", "surface": "campaign multi-target dependency-check", "decision_gate": False},
            {"id": "preflight", "surface": "campaign preflight", "decision_gate": False},
            {"id": "execute", "surface": "agent-controlled bounded repository work", "decision_gate": True},
            {"id": "refresh_changed_targets", "surface": "campaign multi-target refresh --alias <explicit>", "decision_gate": True},
            {"id": "terminal_decision", "surface": "campaign advance|defer|close", "decision_gate": True},
            {"id": "closeout", "surface": "campaign closeout (after terminal close only)", "decision_gate": False},
        ],
    },
}


def _payload(flow: str) -> dict[str, Any]:
    selected = WORKFLOWS[flow]
    return {
        "ok": True,
        "code": "CAMPAIGN_WORKFLOW_NAVIGATION",
        "flow": flow,
        "purpose": selected["purpose"],
        "steps": selected["steps"],
        "flow_selected_by_tool": False,
        "steps_executed": False,
        "responsibility_selected": False,
        "capability_selected": False,
        "authority_granted": False,
        "semantic_truth_established": False,
        "explicit_limit": "Golden paths are static navigation for composing existing surfaces. The active agent still decides whether this flow applies and owns every semantic/authority gate.",
    }


def register_campaign_workflow_commands(campaign: click.Group, *, json_echo: JsonEcho) -> None:
    @campaign.group(name="workflow")
    def workflow_group() -> None:
        """Show static golden paths; never route or execute Campaign work."""

    @workflow_group.command(name="list")
    @click.option("--json", "output_json", is_flag=True)
    def workflow_list(output_json: bool) -> None:
        payload = {
            "ok": True,
            "code": "CAMPAIGN_WORKFLOW_LIST",
            "flows": [
                {"id": key, "purpose": value["purpose"]}
                for key, value in WORKFLOWS.items()
            ],
            "flow_selected_by_tool": False,
            "semantic_recommendation_included": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))

    @workflow_group.command(name="show")
    @click.argument("flow", type=click.Choice(list(WORKFLOWS)))
    @click.option("--json", "output_json", is_flag=True)
    def workflow_show(flow: str, output_json: bool) -> None:
        payload = _payload(flow)
        if output_json:
            json_echo(payload)
        else:
            click.echo(f"CAMPAIGN WORKFLOW: {flow}")
            click.echo(payload["purpose"])
            for index, step in enumerate(payload["steps"], start=1):
                gate = " [AGENT DECISION]" if step["decision_gate"] else ""
                click.echo(f"{index}. {step['surface']}{gate}")
            click.echo()
            click.echo(payload["explicit_limit"])
