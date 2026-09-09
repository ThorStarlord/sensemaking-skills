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
    CampaignService,
    CampaignSnapshot,
    CampaignValidationResult,
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
    "CampaignDecisionService",
    "CampaignDiagnostic",
    "CampaignIdentityError",
    "CampaignIntegrityError",
    "CampaignLineageContractError",
    "CampaignLineageResult",
    "CampaignLineageService",
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
    "ReconciliationAdmission",
    "ReconciliationEvidence",
    "SchemaMigrationReceipt",
    "TransitionLineage",
    "dump_schema_migration_receipt",
    "load_consumption_receipt",
    "load_schema_migration_receipt",
]
