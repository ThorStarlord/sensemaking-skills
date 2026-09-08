"""P9 reconciliation lifecycle read model for durable Sensemaking Campaigns.

This module does not parse reconciliation verdicts into Campaign decisions.
It mechanically identifies admitted reconciliation/repair-verification artifacts
and correlates their exact artifact refs with P8 transition-consumption lineage.

The active coding agent remains responsible for deciding whether reconciliation
evidence warrants repair, advance, defer, close, or no further work.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath

import yaml

from .admission import ArtifactAdmissionContractError, load_artifact_admission
from .errors import CampaignIntegrityError
from .lineage import CampaignLineageService, ConsumptionEdge


RECONCILIATION_ARTIFACT_IDS = frozenset(
    {"reconciliation_report", "repair_verification_report"}
)


@dataclass(frozen=True)
class ReconciliationAdmission:
    """Exact P4 admission provenance for one reconciliation artifact."""

    ref: str
    validator: str
    validation_timestamp: str
    validation_result_sha256: str


@dataclass(frozen=True)
class ReconciliationEvidence:
    """Mechanically reconstructible disposition state for one admitted report."""

    artifact_id: str
    artifact_ref: str
    artifact_sha256: str
    admissions: tuple[ReconciliationAdmission, ...]
    disposition_status: str
    disposition_required: bool
    bound_transition_ids: tuple[str, ...]
    legacy_unbound_transition_ids: tuple[str, ...]


@dataclass(frozen=True)
class CampaignReconciliationResult:
    """Read-only P9 reconciliation state derived from P4 + P8 durable facts."""

    campaign_id: str
    reports: tuple[ReconciliationEvidence, ...]
    disposition_required_count: int
    disposition_recorded_count: int
    legacy_unbound_count: int


class CampaignReconciliationService:
    """Reconstruct reconciliation lifecycle state without semantic routing."""

    def __init__(self, workspace: str | Path) -> None:
        self.lineage = CampaignLineageService(workspace)
        # Reuse the lifecycle/store canonical workspace root rather than resolving
        # the caller-supplied spelling independently.
        self.workspace = self.lineage.store.root

    def inspect(self) -> CampaignReconciliationResult:
        """Return admitted reconciliation evidence and explicit consumption state.

        A report is ``disposition_recorded`` only when at least one committed P8
        ``bound`` consumption edge cites the exact admitted artifact ref. A
        historical/direct-P2 evidence reference without P8 binding remains
        ``legacy_unbound`` and still requires an explicit P9-era disposition.
        """
        lineage = self.lineage.inspect()
        reports: list[ReconciliationEvidence] = []

        edges_by_ref: dict[str, list[ConsumptionEdge]] = {}
        for edge in lineage.consumption_edges:
            edges_by_ref.setdefault(edge.evidence_ref, []).append(edge)

        for evidence in lineage.evidence:
            if evidence.kind != "admitted_artifact":
                continue
            artifact_id = evidence.provenance.get("artifact_id")
            if artifact_id not in RECONCILIATION_ARTIFACT_IDS:
                continue
            if not isinstance(artifact_id, str):
                raise CampaignIntegrityError(
                    "reconciliation artifact provenance has invalid artifact_id",
                    diagnostic_codes=("RECONCILIATION_PROVENANCE_INVALID",),
                )

            raw_admission_refs = evidence.provenance.get("admission_refs")
            if not isinstance(raw_admission_refs, list) or not raw_admission_refs:
                raise CampaignIntegrityError(
                    "reconciliation artifact has no exact P4 admission provenance",
                    diagnostic_codes=("RECONCILIATION_ADMISSION_MISSING",),
                )

            admissions = tuple(
                sorted(
                    (
                        self._load_admission(
                            ref,
                            campaign_id=lineage.campaign_id,
                            artifact_id=artifact_id,
                            artifact_ref=evidence.ref,
                            artifact_sha256=evidence.current_sha256,
                        )
                        for ref in raw_admission_refs
                    ),
                    key=lambda item: item.ref,
                )
            )

            edges = edges_by_ref.get(evidence.ref, [])
            bound_transition_ids = tuple(
                sorted(
                    {
                        edge.transition_id
                        for edge in edges
                        if edge.binding_status == "bound"
                    }
                )
            )
            legacy_unbound_transition_ids = tuple(
                sorted(
                    {
                        edge.transition_id
                        for edge in edges
                        if edge.binding_status == "legacy_unbound"
                    }
                )
            )

            if bound_transition_ids:
                disposition_status = "disposition_recorded"
                disposition_required = False
            elif legacy_unbound_transition_ids:
                disposition_status = "legacy_unbound"
                disposition_required = True
            else:
                disposition_status = "disposition_required"
                disposition_required = True

            reports.append(
                ReconciliationEvidence(
                    artifact_id=artifact_id,
                    artifact_ref=evidence.ref,
                    artifact_sha256=evidence.current_sha256,
                    admissions=admissions,
                    disposition_status=disposition_status,
                    disposition_required=disposition_required,
                    bound_transition_ids=bound_transition_ids,
                    legacy_unbound_transition_ids=legacy_unbound_transition_ids,
                )
            )

        ordered = tuple(
            sorted(reports, key=lambda item: (item.artifact_id, item.artifact_ref))
        )
        return CampaignReconciliationResult(
            campaign_id=lineage.campaign_id,
            reports=ordered,
            disposition_required_count=sum(
                item.disposition_required for item in ordered
            ),
            disposition_recorded_count=sum(
                item.disposition_status == "disposition_recorded" for item in ordered
            ),
            legacy_unbound_count=sum(
                item.disposition_status == "legacy_unbound" for item in ordered
            ),
        )

    def _load_admission(
        self,
        ref: object,
        *,
        campaign_id: str,
        artifact_id: str,
        artifact_ref: str,
        artifact_sha256: str,
    ) -> ReconciliationAdmission:
        if not isinstance(ref, str) or not ref:
            raise CampaignIntegrityError(
                "reconciliation admission ref is not a non-empty string",
                diagnostic_codes=("RECONCILIATION_PROVENANCE_INVALID",),
            )
        parsed = PurePosixPath(ref)
        if (
            parsed.is_absolute()
            or ".." in parsed.parts
            or "." in parsed.parts
            or len(parsed.parts) != 3
            or parsed.parts[0] != "admissions"
            or parsed.parts[1] != artifact_id
        ):
            raise CampaignIntegrityError(
                f"reconciliation admission ref is invalid: {ref}",
                diagnostic_codes=("RECONCILIATION_PROVENANCE_INVALID",),
            )

        path = self.workspace / parsed
        try:
            admission = load_artifact_admission(path)
        except (ArtifactAdmissionContractError, OSError, yaml.YAMLError) as exc:
            raise CampaignIntegrityError(
                "reconciliation admission receipt is invalid",
                diagnostic_codes=("INVALID_RECONCILIATION_ADMISSION",),
            ) from exc

        if admission.campaign_id != campaign_id:
            raise CampaignIntegrityError(
                "reconciliation admission belongs to a different Campaign",
                diagnostic_codes=("RECONCILIATION_CAMPAIGN_ID_MISMATCH",),
            )
        if (
            admission.artifact_id != artifact_id
            or admission.artifact_ref != artifact_ref
            or admission.artifact_sha256 != artifact_sha256
        ):
            raise CampaignIntegrityError(
                "reconciliation admission provenance disagrees with admitted artifact",
                diagnostic_codes=("RECONCILIATION_ADMISSION_MISMATCH",),
            )

        return ReconciliationAdmission(
            ref=ref,
            validator=admission.validator,
            validation_timestamp=admission.validation_timestamp,
            validation_result_sha256=admission.validation_result_sha256,
        )
