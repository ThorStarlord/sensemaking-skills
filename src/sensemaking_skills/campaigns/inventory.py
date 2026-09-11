"""Mechanical inventory of Campaign workspaces under an explicit root."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sensemaking_skills.campaign_semantics import ContractError

from .completion import inspect_archive_marker
from .errors import CampaignWorkspaceError
from .preflight import CampaignPreflightService
from .service import CampaignService


@dataclass(frozen=True)
class CampaignInventoryEntry:
    workspace: str
    campaign_id: str | None
    status: str | None
    current_state: str | None
    target_repository_id: str | None
    integrity: str
    active_responsibility_id: str | None
    last_transition_id: str | None
    archived: bool = False
    archive_integrity: str = "NOT_APPLICABLE"
    diagnostics: tuple[str, ...] = ()


def inspect_campaign_root(
    root: str | Path,
    *,
    include_archived: bool = False,
) -> tuple[CampaignInventoryEntry, ...]:
    base = Path(root).resolve()
    if not base.is_dir():
        raise ValueError(f"campaign inventory root does not exist: {base}")
    entries: list[CampaignInventoryEntry] = []
    for child in sorted((item for item in base.iterdir() if item.is_dir()), key=lambda item: item.name):
        archive = inspect_archive_marker(child)
        if archive.present and archive.valid and not include_archived:
            continue
        archive_diagnostics = tuple(archive.diagnostics)
        archive_integrity = "PASS" if archive.present and archive.valid else ("FAIL" if archive.present else "NOT_APPLICABLE")
        try:
            snapshot = CampaignService(child).resume()
        except (CampaignWorkspaceError, ContractError, OSError, ValueError) as exc:
            entries.append(
                CampaignInventoryEntry(
                    workspace=str(child),
                    campaign_id=None,
                    status=None,
                    current_state=None,
                    target_repository_id=None,
                    integrity="INVALID",
                    active_responsibility_id=None,
                    last_transition_id=None,
                    archived=archive.present and archive.valid,
                    archive_integrity=archive_integrity,
                    diagnostics=(*archive_diagnostics, str(exc)),
                )
            )
            continue
        try:
            preflight = CampaignPreflightService(child).inspect()
            integrity = "PASS" if preflight.ready and archive_integrity != "FAIL" else "FAIL"
            diagnostics = tuple(
                diagnostic
                for check in preflight.checks
                if check.status == "fail"
                for diagnostic in check.diagnostics
            )
            diagnostics = (*archive_diagnostics, *diagnostics)
        except (CampaignWorkspaceError, ContractError, OSError, ValueError) as exc:
            integrity = "FAIL"
            diagnostics = (*archive_diagnostics, str(exc))
        target = snapshot.state.target_snapshot
        responsibility = snapshot.state.active_responsibility
        entries.append(
            CampaignInventoryEntry(
                workspace=str(child),
                campaign_id=snapshot.state.campaign_id,
                status=snapshot.state.status,
                current_state=snapshot.state.current_state,
                target_repository_id=target.repository_id if target is not None else None,
                integrity=integrity,
                active_responsibility_id=responsibility.id if responsibility is not None else None,
                last_transition_id=snapshot.transitions[-1].id if snapshot.transitions else None,
                archived=archive.present and archive.valid,
                archive_integrity=archive_integrity,
                diagnostics=diagnostics,
            )
        )
    return tuple(entries)


def inventory_payload(entries: tuple[CampaignInventoryEntry, ...]) -> dict[str, Any]:
    return {
        "ok": all(item.integrity != "INVALID" for item in entries),
        "code": "CAMPAIGN_INVENTORY",
        "campaign_count": sum(1 for item in entries if item.campaign_id is not None),
        "archived_count": sum(1 for item in entries if item.archived),
        "entry_count": len(entries),
        "entries": [
            {
                "workspace": item.workspace,
                "campaign_id": item.campaign_id,
                "status": item.status,
                "current_state": item.current_state,
                "target_repository_id": item.target_repository_id,
                "integrity": item.integrity,
                "active_responsibility_id": item.active_responsibility_id,
                "last_transition_id": item.last_transition_id,
                "archived": item.archived,
                "archive_integrity": item.archive_integrity,
                "diagnostics": list(item.diagnostics),
            }
            for item in entries
        ],
        "prioritization_performed": False,
        "semantic_recommendation_included": False,
        "semantic_truth_established": False,
        "explicit_limit": "Inventory enumerates workspace state, archive marker, and mechanical integrity only; it does not prioritize Campaigns or equate archive with success.",
    }
