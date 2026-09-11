"""Mechanical Campaign doctor built on Campaign Preflight v0.

Doctor classifies already-detected mechanical failures into deterministic
inspection/remediation classes. It never edits state, chooses a semantic repair,
or decides whether work should continue.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .preflight import CampaignPreflightService


@dataclass(frozen=True)
class CampaignDoctorFinding:
    check_id: str
    diagnostic_class: str
    detail: str
    suggested_inspection: str
    diagnostics: tuple[str, ...]


@dataclass(frozen=True)
class CampaignDoctorResult:
    campaign_id: str | None
    clean: bool
    findings: tuple[CampaignDoctorFinding, ...]
    preflight_ready: bool
    semantic_recommendation_included: bool = False
    automatic_repair_performed: bool = False


_DIAGNOSTIC_CLASSES: Mapping[str, tuple[str, str]] = {
    "campaign_integrity": (
        "CAMPAIGN_RECONSTRUCTION_INVALID",
        "sensemaking-skills campaign validate --workspace <workspace>",
    ),
    "target_binding": (
        "TARGET_BINDING_INVALID",
        "sensemaking-skills campaign validate --workspace <workspace>",
    ),
    "authority_metadata": (
        "AUTHORITY_METADATA_INVALID",
        "sensemaking-skills campaign inspect --workspace <workspace>",
    ),
    "handoff_integrity": (
        "HANDOFF_BINDING_INVALID",
        "sensemaking-skills campaign inspect --workspace <workspace>",
    ),
    "semantic_reference_integrity": (
        "SEMANTIC_REFERENCE_INTEGRITY_INVALID",
        "sensemaking-skills campaign semantic-state --workspace <workspace>",
    ),
    "capability_catalog": (
        "CAPABILITY_CATALOG_INVALID",
        "sensemaking-skills campaign capabilities --workspace <workspace> --responsibility-type <agent-supplied-type>",
    ),
}


class CampaignDoctorService:
    """Turn mechanical preflight failures into bounded diagnostic classes."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace)

    def inspect(self, responsibility_type: str | None = None) -> CampaignDoctorResult:
        preflight = CampaignPreflightService(self.workspace).inspect(responsibility_type)
        findings: list[CampaignDoctorFinding] = []
        for check in preflight.checks:
            if check.status != "fail":
                continue
            diagnostic_class, command = _DIAGNOSTIC_CLASSES.get(
                check.id,
                ("MECHANICAL_PREFLIGHT_FAILURE", "sensemaking-skills campaign preflight --workspace <workspace>"),
            )
            findings.append(
                CampaignDoctorFinding(
                    check_id=check.id,
                    diagnostic_class=diagnostic_class,
                    detail=check.detail,
                    suggested_inspection=command.replace("<workspace>", str(self.workspace)),
                    diagnostics=check.diagnostics,
                )
            )
        return CampaignDoctorResult(
            campaign_id=preflight.campaign_id,
            clean=not findings,
            findings=tuple(findings),
            preflight_ready=preflight.ready,
        )


def doctor_payload(result: CampaignDoctorResult) -> dict[str, Any]:
    return {
        "ok": result.clean,
        "code": "CAMPAIGN_DOCTOR_CLEAN" if result.clean else "CAMPAIGN_DOCTOR_FINDINGS",
        "campaign_id": result.campaign_id,
        "preflight_ready": result.preflight_ready,
        "findings": [
            {
                "check_id": item.check_id,
                "diagnostic_class": item.diagnostic_class,
                "detail": item.detail,
                "suggested_inspection": item.suggested_inspection,
                "diagnostics": list(item.diagnostics),
            }
            for item in result.findings
        ],
        "semantic_recommendation_included": False,
        "automatic_repair_performed": False,
        "explicit_limit": "Doctor identifies mechanical diagnostic paths only; it does not choose or perform a semantic repair.",
    }
