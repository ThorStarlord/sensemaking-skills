"""Immutable typed models for campaign policy/approval/configuration validation.

All models are frozen dataclasses. A successful validation returns a
``ValidatedCampaignBundle`` containing only immutable, validated data --
never an invocation capability, authorization token, provider client, or a
bare boolean/flag a later phase could mistake for authority. See the module
docstring in ``validators.py`` for the full rationale.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Sequence


@dataclass(frozen=True)
class ValidationContext:
    """Caller-supplied context a validation decision is made against.

    Never read from a hardcoded fixture identity or the environment --
    every field here must be supplied explicitly by the caller so a test (or
    a real consumer) cannot accidentally authorize itself via a fabricated
    default.
    """

    current_time: str  # RFC3339 timestamp, injected -- never read from wall clock.
    allowed_approver_identities: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class ValidationDiagnostic:
    """One validation failure. Deterministic, never an uncaught exception."""

    valid: bool
    failure_code: Optional[str] = None
    detail: str = ""
    path: Optional[str] = None


@dataclass(frozen=True)
class ValidationResult:
    """Result of validating a single artifact (policy, approval, or configuration).

    ``value`` is populated only when ``valid`` is True.
    """

    valid: bool
    failure_code: Optional[str] = None
    detail: str = ""
    path: Optional[str] = None
    value: Optional[Mapping[str, Any]] = None

    @staticmethod
    def ok(value: Mapping[str, Any]) -> "ValidationResult":
        return ValidationResult(valid=True, value=value)

    @staticmethod
    def fail(code: str, detail: str = "", path: Optional[str] = None) -> "ValidationResult":
        return ValidationResult(valid=False, failure_code=code, detail=detail, path=path)


@dataclass(frozen=True)
class CampaignPolicy:
    """Parsed, schema-valid, digest-consistent campaign policy document."""

    campaign_id: str
    policy_digest: str
    raw: Mapping[str, Any]


@dataclass(frozen=True)
class CampaignApproval:
    """Parsed, schema-valid campaign approval document (operative profile only)."""

    campaign_id: str
    policy_digest: str
    claimed_approver_identity: str
    raw: Mapping[str, Any]


@dataclass(frozen=True)
class ConfigurationIdentity:
    """Parsed, schema-valid, digest-consistent configuration-identity document."""

    configuration_id: str
    campaign_id: str
    raw: Mapping[str, Any]


@dataclass(frozen=True)
class ValidatedCampaignBundle:
    """The sole successful output of ``validate_campaign_bundle``.

    This is data, not authority: it carries the validated documents and
    nothing that could be mistaken for an invocation capability, an
    authorization token, a provider client, or a callable reaching provider
    code. Phase 3 (#119) is responsible for building the actual
    provider-boundary capability from validated data like this; this object
    is deliberately inert.
    """

    policy: CampaignPolicy
    approval: CampaignApproval
    configuration: ConfigurationIdentity
