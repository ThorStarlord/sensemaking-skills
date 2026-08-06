"""Immutable typed models for campaign policy/approval/configuration validation.

All models are frozen dataclasses. A successful validation returns a
``ValidatedCampaignBundle`` containing only immutable, validated data --
never an invocation capability, authorization token, provider client, or a
bare boolean/flag a later phase could mistake for authority. See the module
docstring in ``validators.py`` for the full rationale.

**Validator-owned provenance.** ``CampaignPolicy``, ``CampaignApproval``,
and ``ConfigurationIdentity`` cannot be constructed by ordinary public API
use -- calling ``CampaignPolicy(...)`` directly raises ``TypeError``.
Instances are created only by a module-private factory function
(``_create_campaign_policy`` etc.), which stamps a per-process sentinel
object held in a closure (never exported, never a predictable string,
boolean, or value copied from the document itself) onto the instance via
``object.__setattr__`` (bypassing both the disabled public constructor and
the frozen dataclass's normal attribute-mutation guard). A paired
module-private verifier (``_is_genuine_campaign_policy`` etc.) checks that
sentinel by identity. Dependent validators (``validate_campaign_approval``,
``validate_configuration_identity``) call the verifier, not a bare
``isinstance`` check, before trusting a ``policy`` argument -- so a plain
mapping, a hand-built instance via ``object.__new__`` guessing at a
`_provenance_seal` attribute, a `dataclasses.replace()` copy, or a
deserialized/pickled object cannot pass as a genuine, validator-produced
policy. This is NOT a claim of protection against hostile, arbitrary code
running inside the same interpreter (that code could reach into this
module's globals and call the private factory directly) -- it prevents
normal API misuse and accidental nominal-type forgery, which is the
boundary this phase's contract requires.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Optional, Sequence, Union


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
    # Report-only verification (post-expiry reporting, independent
    # reconstruction): when False, the policy still validates in full but
    # the wall clock is NOT required to sit inside the execution window.
    # This never authorizes a reservation or invocation; the execution
    # commands always enforce the window themselves (fail closed).
    enforce_validity_window: bool = True


@dataclass(frozen=True)
class ValidationDiagnostic:
    """One validation failure. Deterministic, never an uncaught exception."""

    valid: bool
    failure_code: Optional[str] = None
    detail: str = ""
    path: Optional[str] = None


#: Every shape a SUCCESSFUL ``ValidationResult.value`` can hold. Every one of
#: these is an immutable, typed model -- never a plain, mutable ``dict``.
#: ``validate_campaign_policy`` returns ``CampaignPolicy``;
#: ``validate_campaign_approval`` returns ``CampaignApproval``;
#: ``validate_configuration_identity`` returns ``ConfigurationIdentity``;
#: ``validate_campaign_bundle`` returns ``ValidatedCampaignBundle``.
ValidatedResultValue = Union[
    "CampaignPolicy", "CampaignApproval", "ConfigurationIdentity", "ValidatedCampaignBundle"
]


@dataclass(frozen=True)
class ValidationResult:
    """Result of validating a single artifact, OR the final campaign bundle.

    ``value`` is populated only when ``valid`` is True, and is always one of
    the immutable typed models enumerated in ``ValidatedResultValue`` above
    -- never a plain, mutable mapping. Each public ``validate_*`` function
    freezes (``immutable.freeze``) and wraps its result exactly once, at the
    public boundary, on the way out.
    """

    valid: bool
    failure_code: Optional[str] = None
    detail: str = ""
    path: Optional[str] = None
    value: Optional[ValidatedResultValue] = None

    @staticmethod
    def ok(value: ValidatedResultValue) -> "ValidationResult":
        return ValidationResult(valid=True, value=value)

    @staticmethod
    def fail(code: str, detail: str = "", path: Optional[str] = None) -> "ValidationResult":
        return ValidationResult(valid=False, failure_code=code, detail=detail, path=path)


def _forbid_public_construction(instance: object, class_name: str) -> None:
    raise TypeError(
        f"{class_name} cannot be constructed directly. It is produced only "
        f"by a successful call to the corresponding validate_* function."
    )


def _seal_dataclass(cls: type) -> tuple[Callable[..., Any], Callable[[Any], bool]]:
    """Return ``(create, is_genuine)`` for a frozen dataclass whose instances
    may be created ONLY via the returned ``create`` factory.

    ``create`` uses ``object.__new__`` (bypassing ``cls.__init__`` and thus
    ``__post_init__`` entirely) and stamps a per-process sentinel object --
    held only in this closure, never exported as a module global or an
    importable/predictable token -- onto the instance via
    ``object.__setattr__``. ``is_genuine`` checks that sentinel by identity.
    A caller who obtains a `cls` instance any other way (ordinary
    construction, ``dataclasses.replace``, manual ``object.__new__`` plus
    guessed attribute assignment, deserialization) will not have that exact
    sentinel object and so will not verify as genuine.
    """
    seal = object()

    def create(**kwargs: Any) -> Any:
        obj = object.__new__(cls)
        for key, value in kwargs.items():
            object.__setattr__(obj, key, value)
        object.__setattr__(obj, "_provenance_seal", seal)
        return obj

    def is_genuine(obj: Any) -> bool:
        return isinstance(obj, cls) and getattr(obj, "_provenance_seal", None) is seal

    return create, is_genuine


@dataclass(frozen=True)
class CampaignPolicy:
    """Parsed, schema-valid, digest-consistent campaign policy document.

    Not publicly constructible -- see the module docstring. Obtained only
    from a successful ``validate_campaign_policy(...)`` call.
    """

    campaign_id: str
    policy_digest: str
    raw: Mapping[str, Any]

    def __post_init__(self) -> None:
        _forbid_public_construction(self, "CampaignPolicy")


_create_campaign_policy, _is_genuine_campaign_policy = _seal_dataclass(CampaignPolicy)


@dataclass(frozen=True)
class CampaignApproval:
    """Parsed, schema-valid campaign approval document (operative profile only).

    Not publicly constructible -- see the module docstring. Obtained only
    from a successful ``validate_campaign_approval(...)`` call.
    """

    campaign_id: str
    policy_digest: str
    claimed_approver_identity: str
    raw: Mapping[str, Any]

    def __post_init__(self) -> None:
        _forbid_public_construction(self, "CampaignApproval")


_create_campaign_approval, _is_genuine_campaign_approval = _seal_dataclass(CampaignApproval)


@dataclass(frozen=True)
class ConfigurationIdentity:
    """Parsed, schema-valid, digest-consistent configuration-identity document.

    Not publicly constructible -- see the module docstring. Obtained only
    from a successful ``validate_configuration_identity(...)`` call.
    """

    configuration_id: str
    campaign_id: str
    raw: Mapping[str, Any]

    def __post_init__(self) -> None:
        _forbid_public_construction(self, "ConfigurationIdentity")


_create_configuration_identity, _is_genuine_configuration_identity = _seal_dataclass(ConfigurationIdentity)


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


def is_genuine_campaign_bundle(bundle: object) -> bool:
    """True iff ``bundle`` is a ``ValidatedCampaignBundle`` whose three
    documents were all produced by this package's validator pipeline.

    The bundle itself is a plain frozen dataclass (inert data), so its
    authenticity is decided by the per-document sentinels that only the
    validator-owned factories stamp. A bundle reconstructed from
    ``object.__new__`` and guessed attributes fails here -- this is the
    gate the Phase 3 issuer (exploratory_authorization) relies on.
    """
    return (
        isinstance(bundle, ValidatedCampaignBundle)
        and _is_genuine_campaign_policy(bundle.policy)
        and _is_genuine_campaign_approval(bundle.approval)
        and _is_genuine_configuration_identity(bundle.configuration)
    )
