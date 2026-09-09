"""Small, inert semantic records for reconstructible agent campaigns.

These records describe state and evidence; they do not schedule work, grant
authority, or decide whether a responsibility is semantically warranted.
"""

from .models import (
    Authority, CampaignConstitution, CampaignHandoff, CampaignPolicy, CampaignState, CampaignTrace,
    Capability, CapabilityAvailability,
    ClaimEvidence, Dependency, DependencyType, DeferredResponsibility,
    ExternalBoundary, Responsibility, TerminalState, TransitionRecord,
    Uncertainty, to_dict, validate_campaign_state, validate_reconstruction,
)
from .registry import AvailabilityStatus, CapabilityRegistry, RegisteredCapability, RegistryDiagnostic
from .io import (
    ContractError, canonicalize, dump_campaign_handoff, dump_campaign_policy, dump_campaign_state,
    dump_responsibility,
    dump_campaign_trace, dump_transition_record, load_campaign_policy,
    load_campaign_handoff, load_campaign_state, load_campaign_trace, load_responsibility, load_transition_record,
)
from .schema import (
    CURRENT_SCHEMA_VERSION,
    LEGACY_SCHEMA_VERSION,
    SUPPORTED_SCHEMA_VERSIONS,
    SchemaMigrationError,
    SchemaMigrationResult,
    detect_schema_version,
    migrate_payload,
)

__all__ = [
    "Authority", "CampaignConstitution", "CampaignHandoff", "CampaignPolicy", "CampaignState",
    "Capability", "CapabilityAvailability",
    "CampaignTrace", "ClaimEvidence", "Dependency", "DependencyType",
    "DeferredResponsibility", "ExternalBoundary", "Responsibility",
    "TerminalState", "TransitionRecord", "Uncertainty",
    "to_dict", "validate_campaign_state", "validate_reconstruction",
    "AvailabilityStatus", "CapabilityRegistry", "RegisteredCapability", "RegistryDiagnostic",
    "ContractError", "canonicalize", "load_campaign_state", "dump_campaign_state",
    "load_responsibility", "dump_responsibility", "load_campaign_handoff", "dump_campaign_handoff",
    "load_campaign_policy", "dump_campaign_policy", "load_transition_record",
    "dump_transition_record", "load_campaign_trace", "dump_campaign_trace",
    "CURRENT_SCHEMA_VERSION", "LEGACY_SCHEMA_VERSION", "SUPPORTED_SCHEMA_VERSIONS",
    "SchemaMigrationError", "SchemaMigrationResult", "detect_schema_version", "migrate_payload",
]
