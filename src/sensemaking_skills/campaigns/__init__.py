"""File-backed campaign workspace and deterministic lifecycle primitives.

The active coding agent retains semantic control: it decides what evidence
means and supplies lifecycle decisions. This package validates and persists the
durable structural consequences of those decisions.
"""

from .admission import (
    ArtifactAdmission,
    ArtifactAdmissionContractError,
)
from .artifacts import (
    ArtifactAdmissionResult,
    ArtifactAdmissionService,
)
from .bundle import (
    CampaignBundleDiagnostic,
    CampaignBundleService,
    CampaignBundleVerification,
)
from .decisions import (
    AdvanceDecision,
    CampaignDecisionService,
    CloseDecision,
    DeferDecision,
)
from .errors import (
    ArtifactValidationRejectedError,
    ArtifactValidatorError,
    CampaignAlreadyExistsError,
    CampaignIdentityError,
    CampaignIntegrityError,
    CampaignNotInitializedError,
    CampaignTransactionError,
    CampaignWorkspaceError,
)
from .lineage import (
    CampaignLineageContractError,
    CampaignLineageResult,
    CampaignLineageService,
    ConsumptionEdge,
    ConsumptionReceipt,
    EvidenceBinding,
    LineageEvidence,
    TransitionLineage,
    load_consumption_receipt,
)
from .reconciliation import (
    CampaignReconciliationResult,
    CampaignReconciliationService,
    ReconciliationAdmission,
    ReconciliationEvidence,
)
from .schema_evolution import (
    CampaignSchemaArtifactStatus,
    CampaignSchemaEvolutionService,
    CampaignSchemaStatus,
    CampaignSchemaUpgradeResult,
    SchemaMigrationReceipt,
    dump_schema_migration_receipt,
    load_schema_migration_receipt,
)
from .service import (
    CampaignDiagnostic,
    CampaignSnapshot,
    CampaignValidationResult,
)
from .target_snapshot import (
    CampaignService,
    capture_target_snapshot,
    target_snapshots_equivalent,
)
from .narrative import (
    CampaignNarrativeContractError,
    CampaignNarrativeVerificationService,
    NarrativeVerificationReceipt,
    NarrativeVerificationResult,
    NarrativeVerificationStatus,
    dump_narrative_verification_receipt,
    load_narrative_claims,
    load_narrative_verification_receipt,
)
from .store import CampaignStore
from .workspace import CampaignWorkspace

__all__ = [
    "AdvanceDecision",
    "ArtifactAdmission",
    "ArtifactAdmissionContractError",
    "ArtifactAdmissionResult",
    "ArtifactAdmissionService",
    "ArtifactValidationRejectedError",
    "ArtifactValidatorError",
    "CampaignAlreadyExistsError",
    "CampaignBundleDiagnostic",
    "CampaignBundleService",
    "CampaignBundleVerification",
    "CampaignDecisionService",
    "CampaignDiagnostic",
    "CampaignIdentityError",
    "CampaignIntegrityError",
    "CampaignLineageContractError",
    "CampaignLineageResult",
    "CampaignLineageService",
    "CampaignNarrativeContractError",
    "CampaignNarrativeVerificationService",
    "CampaignNotInitializedError",
    "CampaignReconciliationResult",
    "CampaignReconciliationService",
    "CampaignSchemaArtifactStatus",
    "CampaignSchemaEvolutionService",
    "CampaignSchemaStatus",
    "CampaignSchemaUpgradeResult",
    "CampaignService",
    "CampaignSnapshot",
    "CampaignStore",
    "CampaignTransactionError",
    "CampaignValidationResult",
    "CampaignWorkspace",
    "CampaignWorkspaceError",
    "CloseDecision",
    "ConsumptionEdge",
    "ConsumptionReceipt",
    "DeferDecision",
    "EvidenceBinding",
    "LineageEvidence",
    "NarrativeVerificationReceipt",
    "NarrativeVerificationResult",
    "NarrativeVerificationStatus",
    "ReconciliationAdmission",
    "ReconciliationEvidence",
    "SchemaMigrationReceipt",
    "TransitionLineage",
    "capture_target_snapshot",
    "dump_narrative_verification_receipt",
    "dump_schema_migration_receipt",
    "load_consumption_receipt",
    "load_narrative_claims",
    "load_narrative_verification_receipt",
    "load_schema_migration_receipt",
    "target_snapshots_equivalent",
]
