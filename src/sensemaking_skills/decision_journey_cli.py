"""Decision Journey Productization v1 read-only projections.

These commands compose already-authored strategic, Campaign, execution,
reconciliation, and change-impact surfaces. They never select strategy,
responsibility, action, closure, or authority.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import click
import yaml

from .campaign_semantics import ContractError, canonicalize
from .campaigns import CampaignService, CampaignWorkspaceError
from .campaigns.execution import CampaignExecutionService
from .campaigns.reconciliation import CampaignReconciliationService


def _echo(payload: dict[str, Any], output_json: bool) -> None:
    text = json.dumps(
        payload,
        indent=None if output_json else 2,
        sort_keys=True,
        ensure_ascii=False,
    )
    click.echo(text)


def _load_artifact(path: Path, allowed: set[str]) -> dict[str, Any]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise click.ClickException(str(exc)) from exc
    blocks = re.findall(r"```yaml\s+(.*?)\s+```", content, re.DOTALL)
    for block in reversed(blocks):
        try:
            value = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if isinstance(value, dict) and value.get("artifact_id") in allowed:
            return value
    expected = ", ".join(sorted(allowed))
    raise click.ClickException(
        f"No supported YAML machine block found; expected: {expected}"
    )


def _artifact_ref(data: dict[str, Any], fallback: str) -> str:
    for key in (
        "analysis_ref",
        "reconciliation_ref",
        "delta_ref",
        "closure_ref",
        "journey_id",
    ):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return fallback


def _strategy_projection(data: dict[str, Any], path: Path) -> dict[str, Any]:
    return {
        "ref": _artifact_ref(data, path.name),
        "target_repository": data.get("target_repository"),
        "target_source_identity": data.get("target_source_identity"),
        "strategic_disposition": data.get("strategic_disposition"),
        "selected_path_id": data.get("selected_path_id"),
        "candidate_repository_responsibility": data.get(
            "candidate_repository_responsibility"
        ),
        "candidate_path_transition_ref": data.get(
            "candidate_path_transition_ref"
        ),
        "continuity": data.get("continuity"),
    }


def _campaign_projection(workspace: Path) -> dict[str, Any]:
    snapshot = CampaignService(workspace).resume()
    working = CampaignExecutionService(workspace).working_context()
    reconciliation = CampaignReconciliationService(workspace).inspect()
    state = snapshot.state
    return {
        "campaign_id": state.campaign_id,
        "mission": state.mission,
        "status": state.status,
        "current_state": state.current_state,
        "authority": (
            state.authority.value if state.authority is not None else None
        ),
        "active_responsibility": (
            canonicalize(state.active_responsibility)
            if state.active_responsibility is not None
            else None
        ),
        "active_uncertainty": (
            canonicalize(state.active_uncertainty)
            if state.active_uncertainty is not None
            else None
        ),
        "transition_count": len(snapshot.transitions),
        "evidence_refs": list(snapshot.evidence_refs),
        "working_context": working,
        "reconciliation": {
            "report_count": len(reconciliation.reports),
            "disposition_required_count": (
                reconciliation.disposition_required_count
            ),
            "disposition_recorded_count": (
                reconciliation.disposition_recorded_count
            ),
            "legacy_unbound_count": reconciliation.legacy_unbound_count,
        },
    }


def _impact_projection(data: dict[str, Any], path: Path) -> dict[str, Any]:
    items = [
        item
        for item in (data.get("impact_items") or [])
        if isinstance(item, dict)
    ]
    return {
        "ref": _artifact_ref(data, path.name),
        "change": data.get("change"),
        "closure_effect": data.get("closure_effect"),
        "surface_ids": [
            item.get("surface_id")
            for item in items
            if isinstance(item.get("surface_id"), str)
        ],
        "followup_responsibilities": data.get(
            "followup_responsibilities",
            [],
        ),
    }


def _manifest_diagnostics(
    manifest: dict[str, Any],
    *,
    strategy: dict[str, Any] | None,
    campaign: dict[str, Any] | None,
    strategic_reconciliations: list[dict[str, Any]],
    returned_strategy: dict[str, Any] | None,
    impacts: list[dict[str, Any]],
) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []

    def mismatch(code: str, detail: str) -> None:
        diagnostics.append({"code": code, "detail": detail})

    origin = manifest.get("strategic_origin_ref")
    if origin:
        if strategy is None:
            mismatch("JOURNEY_STRATEGIC_ORIGIN_MISSING", str(origin))
        elif origin != strategy["ref"]:
            mismatch(
                "JOURNEY_STRATEGIC_ORIGIN_REF_MISMATCH",
                f"declared {origin}; supplied {strategy['ref']}",
            )

    campaign_id = manifest.get("campaign_id")
    if campaign_id:
        if campaign is None:
            mismatch("JOURNEY_CAMPAIGN_MISSING", str(campaign_id))
        elif campaign_id != campaign["campaign_id"]:
            mismatch(
                "JOURNEY_CAMPAIGN_ID_MISMATCH",
                f"declared {campaign_id}; "
                f"supplied {campaign['campaign_id']}",
            )

    known_handoffs: set[str] = set()
    known_results: set[str] = set()
    if campaign is not None:
        working = campaign["working_context"]
        handoff = working.get("latest_execution_handoff")
        result = working.get("latest_worker_result")
        if isinstance(handoff, dict) and isinstance(
            handoff.get("handoff_id"),
            str,
        ):
            known_handoffs.add(handoff["handoff_id"])
        if isinstance(result, dict) and isinstance(
            result.get("result_id"),
            str,
        ):
            known_results.add(result["result_id"])

    for handoff_id in manifest.get("execution_handoff_ids", []) or []:
        if handoff_id not in known_handoffs:
            mismatch(
                "JOURNEY_EXECUTION_HANDOFF_NOT_RECONSTRUCTED",
                str(handoff_id),
            )
    for result_id in manifest.get("execution_result_ids", []) or []:
        if result_id not in known_results:
            mismatch(
                "JOURNEY_EXECUTION_RESULT_NOT_RECONSTRUCTED",
                str(result_id),
            )

    supplied_reconciliation_refs = {
        item["ref"] for item in strategic_reconciliations
    }
    for ref in manifest.get("strategic_reconciliation_refs", []) or []:
        if ref not in supplied_reconciliation_refs:
            mismatch(
                "JOURNEY_STRATEGIC_RECONCILIATION_MISSING",
                str(ref),
            )

    return_ref = manifest.get("strategic_return_ref")
    if return_ref:
        if returned_strategy is None:
            mismatch("JOURNEY_STRATEGIC_RETURN_MISSING", str(return_ref))
        elif return_ref != returned_strategy["ref"]:
            mismatch(
                "JOURNEY_STRATEGIC_RETURN_REF_MISMATCH",
                f"declared {return_ref}; "
                f"supplied {returned_strategy['ref']}",
            )

    supplied_impact_refs = {item["ref"] for item in impacts}
    for ref in manifest.get("change_impact_refs", []) or []:
        if ref not in supplied_impact_refs:
            mismatch("JOURNEY_CHANGE_IMPACT_MISSING", str(ref))

    return diagnostics


@click.group(name="journey")
def journey_group() -> None:
    """Reconstruct decision journeys without making semantic decisions."""


@journey_group.command(name="inspect")
@click.option(
    "--manifest",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=None,
)
@click.option(
    "--strategy-artifact",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=None,
)
@click.option(
    "--workspace",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
)
@click.option(
    "--strategic-reconciliation",
    "strategic_reconciliations",
    multiple=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--return-strategy-artifact",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=None,
)
@click.option(
    "--change-impact-artifact",
    "change_impact_artifacts",
    multiple=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--json", "output_json", is_flag=True)
def inspect_journey(
    manifest: Path | None,
    strategy_artifact: Path | None,
    workspace: Path | None,
    strategic_reconciliations: tuple[Path, ...],
    return_strategy_artifact: Path | None,
    change_impact_artifacts: tuple[Path, ...],
    output_json: bool,
) -> None:
    """Project explicitly supplied stages and report missing declared links."""
    if not any(
        (
            manifest,
            strategy_artifact,
            workspace,
            strategic_reconciliations,
            return_strategy_artifact,
            change_impact_artifacts,
        )
    ):
        raise click.ClickException("Supply at least one journey source.")

    try:
        strategy = (
            _strategy_projection(
                _load_artifact(
                    strategy_artifact,
                    {"strategic_repository_analysis"},
                ),
                strategy_artifact,
            )
            if strategy_artifact
            else None
        )
        campaign = _campaign_projection(workspace) if workspace else None
        reconciliations = []
        for path in strategic_reconciliations:
            data = _load_artifact(path, {"strategic_reconciliation"})
            reconciliations.append(
                {"ref": _artifact_ref(data, path.name), "artifact": data}
            )
        returned = (
            _strategy_projection(
                _load_artifact(
                    return_strategy_artifact,
                    {"strategic_repository_analysis"},
                ),
                return_strategy_artifact,
            )
            if return_strategy_artifact
            else None
        )
        impacts = [
            _impact_projection(
                _load_artifact(path, {"change_impact_analysis"}),
                path,
            )
            for path in change_impact_artifacts
        ]
        manifest_data = (
            _load_artifact(manifest, {"decision_journey"})
            if manifest
            else None
        )
    except (CampaignWorkspaceError, ContractError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    diagnostics = (
        _manifest_diagnostics(
            manifest_data,
            strategy=strategy,
            campaign=campaign,
            strategic_reconciliations=reconciliations,
            returned_strategy=returned,
            impacts=impacts,
        )
        if manifest_data
        else []
    )
    working = campaign["working_context"] if campaign else {}
    payload = {
        "ok": not diagnostics,
        "code": "DECISION_JOURNEY_INSPECT",
        "journey_id": (
            _artifact_ref(manifest_data, manifest.name)
            if manifest_data and manifest
            else None
        ),
        "stages": {
            "strategic_origin": strategy,
            "responsibility": (
                campaign.get("active_responsibility")
                if campaign
                else None
            ),
            "campaign": campaign,
            "execution_handoff": working.get(
                "latest_execution_handoff"
            ),
            "worker_result": working.get("latest_worker_result"),
            "campaign_reconciliation": (
                campaign.get("reconciliation") if campaign else None
            ),
            "strategic_reconciliation": reconciliations,
            "change_impact": impacts,
            "strategic_return": returned,
        },
        "diagnostics": diagnostics,
        "mechanical_reconstruction_only": True,
        "causal_truth_inferred": False,
        "semantic_recommendation_included": False,
        "closure_inferred": False,
        "implementation_authorized": False,
    }
    _echo(payload, output_json)
    if diagnostics:
        raise click.exceptions.Exit(3)


@journey_group.command(name="context")
@click.option(
    "--profile",
    required=True,
    type=click.Choice(
        ["strategic", "responsibility", "execution", "reassessment"]
    ),
)
@click.option(
    "--strategy-artifact",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=None,
)
@click.option(
    "--workspace",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
)
@click.option(
    "--return-strategy-artifact",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=None,
)
@click.option(
    "--change-impact-artifact",
    "change_impact_artifacts",
    multiple=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--json", "output_json", is_flag=True)
def context_pack(
    profile: str,
    strategy_artifact: Path | None,
    workspace: Path | None,
    return_strategy_artifact: Path | None,
    change_impact_artifacts: tuple[Path, ...],
    output_json: bool,
) -> None:
    """Project an explicitly selected purpose-specific context pack."""
    try:
        strategy = (
            _strategy_projection(
                _load_artifact(
                    strategy_artifact,
                    {"strategic_repository_analysis"},
                ),
                strategy_artifact,
            )
            if strategy_artifact
            else None
        )
        campaign = _campaign_projection(workspace) if workspace else None
        returned = (
            _strategy_projection(
                _load_artifact(
                    return_strategy_artifact,
                    {"strategic_repository_analysis"},
                ),
                return_strategy_artifact,
            )
            if return_strategy_artifact
            else None
        )
        impacts = [
            _impact_projection(
                _load_artifact(path, {"change_impact_analysis"}),
                path,
            )
            for path in change_impact_artifacts
        ]
    except (CampaignWorkspaceError, ContractError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    if profile == "strategic":
        if strategy is None:
            raise click.ClickException(
                "strategic profile requires --strategy-artifact"
            )
        context = {"strategic_analysis": strategy}
    elif profile == "responsibility":
        if campaign is None:
            raise click.ClickException(
                "responsibility profile requires --workspace"
            )
        working = campaign["working_context"]
        context = {
            "campaign_id": campaign["campaign_id"],
            "mission": campaign["mission"],
            "active_responsibility": campaign["active_responsibility"],
            "active_uncertainty": campaign["active_uncertainty"],
            "authority": campaign["authority"],
            "targets": working.get("targets", []),
            "stop_conditions": working.get("stop_conditions", []),
        }
    elif profile == "execution":
        if campaign is None:
            raise click.ClickException(
                "execution profile requires --workspace"
            )
        working = campaign["working_context"]
        context = {
            "campaign_id": campaign["campaign_id"],
            "active_responsibility": campaign["active_responsibility"],
            "authority": campaign["authority"],
            "targets": working.get("targets", []),
            "evidence_refs": campaign["evidence_refs"],
            "latest_execution_handoff": working.get(
                "latest_execution_handoff"
            ),
            "latest_worker_result": working.get(
                "latest_worker_result"
            ),
            "stop_conditions": working.get("stop_conditions", []),
        }
    else:
        if campaign is None and returned is None and not impacts:
            raise click.ClickException(
                "reassessment profile requires --workspace, "
                "--return-strategy-artifact, or "
                "--change-impact-artifact"
            )
        context = {
            "campaign_reconciliation": (
                campaign.get("reconciliation") if campaign else None
            ),
            "latest_worker_result": (
                campaign["working_context"].get(
                    "latest_worker_result"
                )
                if campaign
                else None
            ),
            "change_impacts": impacts,
            "strategic_return": returned,
        }

    payload = {
        "ok": True,
        "code": "DECISION_JOURNEY_CONTEXT",
        "profile": profile,
        "context": context,
        "profile_selected_by_caller": True,
        "automatic_routing_performed": False,
        "next_action_selected": False,
        "semantic_recommendation_included": False,
    }
    _echo(payload, output_json)


@journey_group.command(name="delta")
@click.option(
    "--artifact",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--before",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--after",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--json", "output_json", is_flag=True)
def decision_delta(
    artifact: Path,
    before: Path,
    after: Path,
    output_json: bool,
) -> None:
    """Validate an authored semantic decision delta against analysis refs."""
    delta = _load_artifact(artifact, {"strategic_decision_delta"})
    old = _strategy_projection(
        _load_artifact(before, {"strategic_repository_analysis"}),
        before,
    )
    new = _strategy_projection(
        _load_artifact(after, {"strategic_repository_analysis"}),
        after,
    )
    diagnostics: list[dict[str, str]] = []
    if delta.get("prior_analysis_ref") != old["ref"]:
        diagnostics.append(
            {
                "code": "DECISION_DELTA_PRIOR_REF_MISMATCH",
                "detail": (
                    f"declared {delta.get('prior_analysis_ref')}; "
                    f"supplied {old['ref']}"
                ),
            }
        )
    if delta.get("current_analysis_ref") != new["ref"]:
        diagnostics.append(
            {
                "code": "DECISION_DELTA_CURRENT_REF_MISMATCH",
                "detail": (
                    f"declared {delta.get('current_analysis_ref')}; "
                    f"supplied {new['ref']}"
                ),
            }
        )
    for field in (
        "semantic_truth_established",
        "strategy_selected_by_delta",
        "implementation_authorized_by_delta",
    ):
        if delta.get(field) is not False:
            diagnostics.append(
                {
                    "code": "DECISION_DELTA_BOUNDARY_INVALID",
                    "detail": f"{field} must be false",
                }
            )

    payload = {
        "ok": not diagnostics,
        "code": "STRATEGIC_DECISION_DELTA",
        "delta_ref": _artifact_ref(delta, artifact.name),
        "prior_analysis_ref": old["ref"],
        "current_analysis_ref": new["ref"],
        "disposition_before": old["strategic_disposition"],
        "disposition_after": new["strategic_disposition"],
        "selected_path_before": old["selected_path_id"],
        "selected_path_after": new["selected_path_id"],
        "authored_delta": {
            "continuity_disposition": delta.get(
                "continuity_disposition"
            ),
            "unchanged_commitments": delta.get(
                "unchanged_commitments",
                [],
            ),
            "new_evidence_refs": delta.get("new_evidence_refs", []),
            "assumption_changes": delta.get(
                "assumption_changes",
                [],
            ),
            "decision_change": delta.get("decision_change"),
            "semantic_reason": delta.get("semantic_reason"),
        },
        "diagnostics": diagnostics,
        "mechanical_comparison_is_not_semantic_reason": True,
        "semantic_interpretation_authored": True,
        "strategy_selected_by_command": False,
    }
    _echo(payload, output_json)
    if diagnostics:
        raise click.exceptions.Exit(3)


@journey_group.command(name="impact-closure")
@click.option(
    "--impact-artifact",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--closure-artifact",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--json", "output_json", is_flag=True)
def impact_closure(
    impact_artifact: Path,
    closure_artifact: Path,
    output_json: bool,
) -> None:
    """Compare anticipated impact surfaces with authored observed state."""
    impact_data = _load_artifact(
        impact_artifact,
        {"change_impact_analysis"},
    )
    impact = _impact_projection(impact_data, impact_artifact)
    closure = _load_artifact(
        closure_artifact,
        {"change_evidence_closure"},
    )
    diagnostics: list[dict[str, str]] = []
    if closure.get("change_impact_ref") != impact["ref"]:
        diagnostics.append(
            {
                "code": "IMPACT_CLOSURE_REF_MISMATCH",
                "detail": (
                    f"declared {closure.get('change_impact_ref')}; "
                    f"supplied {impact['ref']}"
                ),
            }
        )
    known = set(impact["surface_ids"])
    verified = set(closure.get("verified_surface_ids", []) or [])
    unresolved = set(
        closure.get("unresolved_surface_ids", []) or []
    )
    unknown = sorted((verified | unresolved) - known)
    if unknown:
        diagnostics.append(
            {
                "code": "IMPACT_CLOSURE_SURFACE_UNKNOWN",
                "detail": ", ".join(unknown),
            }
        )
    overlap = sorted(verified & unresolved)
    if overlap:
        diagnostics.append(
            {
                "code": "IMPACT_CLOSURE_SURFACE_CONFLICT",
                "detail": ", ".join(overlap),
            }
        )
    for field in (
        "closure_inferred_by_artifact",
        "followup_execution_authorized_by_artifact",
        "semantic_truth_established",
    ):
        if closure.get(field) is not False:
            diagnostics.append(
                {
                    "code": "IMPACT_CLOSURE_BOUNDARY_INVALID",
                    "detail": f"{field} must be false",
                }
            )
    accounted = verified | unresolved
    payload = {
        "ok": not diagnostics,
        "code": "CHANGE_EVIDENCE_CLOSURE_COMPARE",
        "impact_ref": impact["ref"],
        "closure_ref": _artifact_ref(
            closure,
            closure_artifact.name,
        ),
        "anticipated_surface_ids": impact["surface_ids"],
        "verified_surface_ids": sorted(verified),
        "unresolved_surface_ids": sorted(unresolved),
        "unaccounted_surface_ids": sorted(known - accounted),
        "observed_evidence_refs": closure.get(
            "observed_evidence_refs",
            [],
        ),
        "reconciliation_refs": closure.get(
            "reconciliation_refs",
            [],
        ),
        "authored_closure_disposition": closure.get(
            "closure_disposition"
        ),
        "semantic_reason": closure.get("semantic_reason"),
        "diagnostics": diagnostics,
        "closure_inferred_by_command": False,
        "followup_authorized_by_command": False,
        "difference_is_reassessment_evidence_only": True,
    }
    _echo(payload, output_json)
    if diagnostics:
        raise click.exceptions.Exit(3)


_GUIDE = {
    "repository-future": {
        "capability": "strategic-repository-analysis",
        "entry_point": "skills/strategic-repository-analysis/SKILL.md",
        "why": (
            "The repository/product future is open and no bounded "
            "responsibility is selected."
        ),
    },
    "responsibility-unclear": {
        "capability": "using-sensemaking + repo-sensemaker",
        "entry_point": "skills/using-sensemaking/SKILL.md",
        "why": (
            "The requested outcome exists, but the correct repository "
            "responsibility is uncertain."
        ),
    },
    "selected-work": {
        "capability": "Campaign / execution handoff",
        "entry_point": "docs/campaign-execution-interface-v1.md",
        "why": (
            "The responsibility is already selected and needs "
            "controlled delegation."
        ),
    },
    "returned-work": {
        "capability": "Learning / Reconciliation",
        "entry_point": (
            "docs/strategic-reconciliation-and-decision-packets-v1.md"
        ),
        "why": (
            "Returned evidence must be interpreted before "
            "continuation or closure."
        ),
    },
    "repository-changed": {
        "capability": "Strategic Continuity",
        "entry_point": "docs/strategic-continuity-v1.md",
        "why": (
            "A prior strategic analysis exists and repository/evidence "
            "currentness changed."
        ),
    },
    "change-consequences": {
        "capability": "change-impact-analysis",
        "entry_point": "skills/change-impact-analysis/SKILL.md",
        "why": (
            "A bounded change may affect consequential adjacent "
            "surfaces or closure claims."
        ),
    },
    "multi-repo-boundary": {
        "capability": "multi-repository-strategic-analysis",
        "entry_point": (
            "skills/multi-repository-strategic-analysis/SKILL.md"
        ),
        "why": (
            "The decision concerns capability ownership or boundaries "
            "across an explicitly selected repository set."
        ),
    },
}


@journey_group.command(name="guide")
@click.option(
    "--intent",
    required=True,
    type=click.Choice(sorted(_GUIDE)),
)
@click.option("--json", "output_json", is_flag=True)
def guide(intent: str, output_json: bool) -> None:
    """Show static guidance for one caller-selected intent; never route."""
    payload = {
        "ok": True,
        "code": "DECISION_JOURNEY_GUIDE",
        "intent": intent,
        **_GUIDE[intent],
        "intent_selected_by_caller": True,
        "automatic_routing_performed": False,
        "capability_invoked_by_command": False,
        "authority_granted_by_command": False,
    }
    _echo(payload, output_json)


def register_decision_journey_commands(root: click.Group) -> None:
    """Register Decision Journey Productization v1 read-only surfaces."""
    root.add_command(journey_group)
