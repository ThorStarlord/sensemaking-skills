"""Local-only Campaign provenance projection for engineering boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sensemaking_skills.campaign_semantics import target_snapshot_sha256

from .preflight import CampaignPreflightService
from .target_snapshot import CampaignService
from .uncertainty_history import UncertaintyHistoryService


@dataclass(frozen=True)
class CampaignProvenance:
    campaign_id: str
    responsibility_id: str | None
    responsibility_statement: str | None
    responsibility_authority: str | None
    target_ref: str | None
    first_transition_target_before_sha256: str | None
    latest_transition_target_after_sha256: str | None
    transition_count: int
    latest_transition_id: str | None
    evidence_refs: tuple[str, ...]
    preflight_ready: bool
    uncertainty_history_valid: bool
    semantic_truth_established: bool = False


def _enum(value: Any) -> str | None:
    if value is None:
        return None
    return value.value if hasattr(value, "value") else str(value)


class CampaignProvenanceService:
    """Project existing durable provenance without publishing it anywhere."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace)
        self.lifecycle = CampaignService(workspace)

    def inspect(self) -> CampaignProvenance:
        snapshot = self.lifecycle.resume()
        state = snapshot.state
        responsibility = state.active_responsibility
        target_ref = None
        if state.target_snapshot is not None:
            target_ref = f"target-snapshot-sha256:{target_snapshot_sha256(state.target_snapshot)}"
        first_before = None
        latest_after = None
        if snapshot.transitions:
            first_before = next(
                (
                    item.target_snapshot_before_sha256
                    for item in snapshot.transitions
                    if item.target_snapshot_before_sha256 is not None
                ),
                None,
            )
            latest_after = next(
                (
                    item.target_snapshot_after_sha256
                    for item in reversed(snapshot.transitions)
                    if item.target_snapshot_after_sha256 is not None
                ),
                None,
            )
        preflight = CampaignPreflightService(self.workspace).inspect()
        uncertainty = UncertaintyHistoryService(self.workspace).load()
        return CampaignProvenance(
            campaign_id=state.campaign_id,
            responsibility_id=responsibility.id if responsibility is not None else None,
            responsibility_statement=(
                responsibility.statement if responsibility is not None else None
            ),
            responsibility_authority=(
                _enum(responsibility.authority) if responsibility is not None else _enum(state.authority)
            ),
            target_ref=target_ref,
            first_transition_target_before_sha256=first_before,
            latest_transition_target_after_sha256=latest_after,
            transition_count=len(snapshot.transitions),
            latest_transition_id=(snapshot.transitions[-1].id if snapshot.transitions else None),
            evidence_refs=tuple(snapshot.evidence_refs),
            preflight_ready=preflight.ready,
            uncertainty_history_valid=uncertainty.valid,
        )


def provenance_payload(value: CampaignProvenance) -> dict[str, Any]:
    return {
        "campaign_id": value.campaign_id,
        "responsibility": {
            "id": value.responsibility_id,
            "statement": value.responsibility_statement,
            "authority": value.responsibility_authority,
        },
        "target": {
            "current_ref": value.target_ref,
            "first_transition_before_sha256": value.first_transition_target_before_sha256,
            "latest_transition_after_sha256": value.latest_transition_target_after_sha256,
        },
        "transition_count": value.transition_count,
        "latest_transition_id": value.latest_transition_id,
        "evidence_refs": list(value.evidence_refs),
        "preflight_ready": value.preflight_ready,
        "uncertainty_history_valid": value.uncertainty_history_valid,
        "semantic_truth_established": False,
        "published": False,
        "explicit_limit": "Local provenance rendering does not publish to GitHub or establish semantic correctness.",
    }


def render_provenance_markdown(value: CampaignProvenance) -> str:
    """Render deterministic Markdown suitable for manual PR description inclusion."""
    payload = provenance_payload(value)
    responsibility = payload["responsibility"]
    target = payload["target"]
    evidence = payload["evidence_refs"]
    evidence_lines = "\n".join(f"  - `{item}`" for item in evidence) if evidence else "  - none"
    return (
        "### Sensemaking Campaign Provenance\n\n"
        f"- Campaign: `{payload['campaign_id']}`\n"
        f"- Responsibility: `{responsibility['id'] or 'none'}`"
        + (f" — {responsibility['statement']}" if responsibility["statement"] else "")
        + "\n"
        f"- Responsibility authority: `{responsibility['authority'] or 'none'}`\n"
        f"- Current target ref: `{target['current_ref'] or 'none'}`\n"
        f"- First transition target-before digest: `{target['first_transition_before_sha256'] or 'none'}`\n"
        f"- Latest transition target-after digest: `{target['latest_transition_after_sha256'] or 'none'}`\n"
        f"- Latest transition: `{payload['latest_transition_id'] or 'none'}`\n"
        f"- Transition count: `{payload['transition_count']}`\n"
        f"- Mechanical preflight ready: `{'yes' if payload['preflight_ready'] else 'no'}`\n"
        f"- Uncertainty history valid: `{'yes' if payload['uncertainty_history_valid'] else 'no'}`\n"
        "- Evidence refs:\n"
        f"{evidence_lines}\n\n"
        "> Local projection only. It has not been published to GitHub and does not establish semantic correctness.\n"
    )
