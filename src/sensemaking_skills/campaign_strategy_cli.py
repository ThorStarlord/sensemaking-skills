"""Read-only Level-3 strategy projections and explicit Campaign handoff.

These surfaces transport already-authored strategic state. They do not rank the
Strategic Frontier, choose a responsibility, or revise the product thesis.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from .campaign_semantics import Authority, CampaignState, ContractError, Responsibility
from .campaigns import CampaignService, CampaignWorkspaceError


ErrorEmitter = Callable[..., None]
JsonEcho = Callable[[dict[str, Any]], None]

_REQUIRED_SECTIONS = (
    "### Current product strategy",
    "### Current capability state",
    "### Material limitations and evidence ceilings",
    "### Strategic Frontier",
    "### Current highest-leverage boundary",
    "### Current decision-changing uncertainty",
    "### Current warranted repository-level responsibility",
    "### Authority / owner direction",
    "### Thesis review state",
)
_FRONTIER_RE = re.compile(
    r"^\s*\d+\.\s+\*\*(?P<name>.+?)\s+(?:—|–|-)\s+(?P<disposition>.+?)\.\*\*",
    re.MULTILINE,
)
_THESIS_RE = re.compile(r"THESIS_REVIEW_REQUIRED`?\s*:\s*\*\*?\s*`?(YES|NO)`?", re.IGNORECASE)


def _heading_level(line: str) -> int | None:
    match = re.match(r"^(#+)\s+", line)
    return len(match.group(1)) if match else None


def _section(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    matches = [index for index, line in enumerate(lines) if line.strip() == heading]
    if len(matches) != 1:
        return None
    start = matches[0]
    level = _heading_level(lines[start])
    if level is None:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        candidate = _heading_level(lines[index])
        if candidate is not None and candidate <= level:
            end = index
            break
    return "\n".join(lines[start + 1 : end]).strip()


def _status_projection(status_path: Path) -> dict[str, Any]:
    raw = status_path.read_bytes()
    text = raw.decode("utf-8")
    missing = [heading for heading in _REQUIRED_SECTIONS if _section(text, heading) is None]
    frontier_section = _section(text, "### Strategic Frontier") or ""
    frontier = [
        {"name": match.group("name").strip(), "disposition": match.group("disposition").strip()}
        for match in _FRONTIER_RE.finditer(frontier_section)
    ]
    thesis_section = _section(text, "### Thesis review state") or ""
    thesis_match = _THESIS_RE.search(thesis_section)
    sections = {
        heading.removeprefix("### "): _section(text, heading)
        for heading in _REQUIRED_SECTIONS
    }
    return {
        "status_path": str(status_path),
        "status_sha256": hashlib.sha256(raw).hexdigest(),
        "required_sections_present": not missing,
        "missing_sections": missing,
        "strategic_frontier": frontier,
        "highest_leverage_boundary": sections["Current highest-leverage boundary"],
        "decision_changing_uncertainty": sections["Current decision-changing uncertainty"],
        "warranted_responsibility": sections["Current warranted repository-level responsibility"],
        "thesis_review_required": thesis_match.group(1).upper() if thesis_match else None,
        "sections": sections,
        "semantic_ranking_performed": False,
        "semantic_recommendation_included": False,
        "semantic_truth_established": False,
    }


def _write_handoff(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def register_campaign_strategy_commands(
    campaign: click.Group,
    *,
    emit_error: ErrorEmitter,
    json_echo: JsonEcho,
) -> None:
    @campaign.group(name="strategy")
    def strategy_group() -> None:
        """Inspect/transport Level-3 state without strategic decision automation."""

    @strategy_group.command(name="inspect")
    @click.option("--repo-root", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def strategy_inspect(repo_root: Path, output_json: bool) -> None:
        """Project mechanically addressable Level-3 state from STATUS.md."""
        status_path = repo_root.resolve() / "STATUS.md"
        if not status_path.is_file():
            raise click.ClickException(f"STATUS.md not found under {repo_root}")
        try:
            payload = _status_projection(status_path)
        except UnicodeError as exc:
            raise click.ClickException(f"STATUS.md is not valid UTF-8: {exc}") from exc
        payload = {"ok": payload["required_sections_present"], "code": "STRATEGY_INSPECT", **payload}
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not payload["required_sections_present"]:
            raise click.exceptions.Exit(3)

    @strategy_group.command(name="diff")
    @click.option("--from-status", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
    @click.option("--to-status", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def strategy_diff(from_status: Path, to_status: Path, output_json: bool) -> None:
        """Compare durable Level-3 representations without judging which is better."""
        before = _status_projection(from_status)
        after = _status_projection(to_status)
        changed_sections: dict[str, dict[str, Any]] = {}
        before_sections = before["sections"]
        after_sections = after["sections"]
        for key in sorted(set(before_sections) | set(after_sections)):
            if before_sections.get(key) != after_sections.get(key):
                changed_sections[key] = {"from": before_sections.get(key), "to": after_sections.get(key)}
        payload = {
            "ok": before["required_sections_present"] and after["required_sections_present"],
            "code": "STRATEGY_DIFF",
            "from_sha256": before["status_sha256"],
            "to_sha256": after["status_sha256"],
            "changed_sections": changed_sections,
            "frontier_from": before["strategic_frontier"],
            "frontier_to": after["strategic_frontier"],
            "thesis_review_from": before["thesis_review_required"],
            "thesis_review_to": after["thesis_review_required"],
            "semantic_ranking_performed": False,
            "better_state_selected": False,
            "semantic_truth_established": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        if not payload["ok"]:
            raise click.exceptions.Exit(3)

    @strategy_group.command(name="handoff")
    @click.option("--repo-root", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--workspace", required=True, type=click.Path(path_type=Path))
    @click.option("--campaign-id", required=True)
    @click.option("--mission", required=True)
    @click.option("--frontier-item", required=True, help="Exact Strategic Frontier item explicitly selected by the agent/owner")
    @click.option("--responsibility-id", required=True)
    @click.option("--responsibility-type", required=True, help="Explicit classification; never inferred")
    @click.option("--responsibility-statement", required=True)
    @click.option("--decision-blocked", required=True)
    @click.option("--scope", required=True)
    @click.option("--authority", required=True, type=click.Choice([item.value for item in Authority]))
    @click.option("--success-condition", "success_conditions", multiple=True, required=True)
    @click.option("--target-repo", default=None, type=click.Path(exists=True, file_okay=False, path_type=Path))
    @click.option("--json", "output_json", is_flag=True)
    def strategy_handoff(
        repo_root: Path,
        workspace: Path,
        campaign_id: str,
        mission: str,
        frontier_item: str,
        responsibility_id: str,
        responsibility_type: str,
        responsibility_statement: str,
        decision_blocked: str,
        scope: str,
        authority: str,
        success_conditions: tuple[str, ...],
        target_repo: Path | None,
        output_json: bool,
    ) -> None:
        """Create a Campaign from an explicit Level-3 selection; never select it."""
        status_path = repo_root.resolve() / "STATUS.md"
        if not status_path.is_file():
            raise click.ClickException(f"STATUS.md not found under {repo_root}")
        projection = _status_projection(status_path)
        frontier_names = {item["name"] for item in projection["strategic_frontier"]}
        if frontier_item not in frontier_names:
            raise click.ClickException("--frontier-item must exactly match one current Strategic Frontier item")
        if not responsibility_type.strip():
            raise click.ClickException("--responsibility-type must be non-empty")
        resolved_authority = Authority(authority)
        responsibility = Responsibility(
            id=responsibility_id,
            statement=responsibility_statement,
            trigger_evidence=(),
            decision_blocked=decision_blocked,
            scope=scope,
            authority=resolved_authority,
            success_conditions=success_conditions,
        )
        state = CampaignState(
            campaign_id=campaign_id,
            mission=mission,
            status="active",
            current_state="strategy_handoff",
            active_responsibility=responsibility,
            authority=resolved_authority,
            extensions={
                "strategy_handoff": {
                    "status_sha256": projection["status_sha256"],
                    "frontier_item": frontier_item,
                    "responsibility_type": responsibility_type.strip(),
                    "selection_source": "explicit_agent_or_owner_input",
                }
            },
        )
        try:
            snapshot = CampaignService(workspace, target_repo=target_repo).initialize(state)
        except (CampaignWorkspaceError, ContractError) as exc:
            emit_error(exc, output_json=output_json)
            return
        handoff = {
            "schema_version": "1",
            "campaign_id": campaign_id,
            "source_status_sha256": projection["status_sha256"],
            "source_status_path": str(status_path),
            "frontier_item": frontier_item,
            "responsibility_id": responsibility_id,
            "responsibility_type": responsibility_type.strip(),
            "selection_performed_by_tool": False,
            "authorization_inferred_by_tool": False,
            "semantic_truth_established": False,
        }
        _write_handoff(workspace.resolve() / "strategy-handoff.json", handoff)
        payload = {
            "ok": True,
            "code": "STRATEGY_CAMPAIGN_HANDOFF_CREATED",
            "campaign_id": snapshot.state.campaign_id,
            "workspace": str(workspace.resolve()),
            "frontier_item": frontier_item,
            "responsibility_id": responsibility_id,
            "responsibility_type": responsibility_type.strip(),
            "source_status_sha256": projection["status_sha256"],
            "selection_performed_by_tool": False,
            "semantic_recommendation_included": False,
        }
        if output_json:
            json_echo(payload)
        else:
            click.echo(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
