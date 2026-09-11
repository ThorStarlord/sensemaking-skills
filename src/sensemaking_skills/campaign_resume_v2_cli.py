"""Resume Capsule v2 progressive-disclosure CLI."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import ContractError, canonicalize
from .campaigns import CampaignService, CampaignWorkspaceError
from .campaigns.resume_capsule import RESUME_PROFILES, build_resume_capsule
from .semantic_architecture import SemanticStateStore


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]


def _semantic_summary(workspace: Path) -> dict[str, Any]:
    path = workspace / "semantic-state.jsonl"
    records, diagnostics = SemanticStateStore(path).load_raw()
    return {
        "present": bool(records) or path.exists(),
        "valid": not diagnostics,
        "entry_count": len(records),
        "latest_entry": records[-1]["entry"] if records else None,
        "diagnostics": [canonicalize(item) for item in diagnostics],
        "schema_in_campaign_state": False,
        "semantic_truth_established": False,
    }


def register_campaign_resume_v2_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    @campaign.command(name="resume-profile")
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--profile", type=click.Choice(list(RESUME_PROFILES)), default="working", show_default=True)
    @click.option("--recent-transitions", type=click.IntRange(0, 50), default=5, show_default=True)
    @click.option("--max-items", type=click.IntRange(1, 1000), default=None)
    @click.option("--include-preflight", is_flag=True, help="Include mechanical preflight in working profile; audit always includes it")
    @click.option("--json", "output_json", is_flag=True)
    def campaign_resume_profile(
        workspace: Path,
        profile: str,
        recent_transitions: int,
        max_items: int | None,
        include_preflight: bool,
        output_json: bool,
    ) -> None:
        """Emit Resume Capsule v2 using deterministic progressive disclosure."""
        try:
            snapshot = CampaignService(workspace).resume()
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        payload = build_resume_capsule(
            workspace=workspace,
            snapshot=snapshot,
            semantic_summary=_semantic_summary(workspace),
            recent_transitions=recent_transitions,
            compact=False,
            include_preflight=include_preflight,
            profile=profile,
            max_items=max_items,
        )
        if output_json:
            json_echo(payload)
        else:
            click.echo("CAMPAIGN_RESUME_CONTEXT_V2")
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
