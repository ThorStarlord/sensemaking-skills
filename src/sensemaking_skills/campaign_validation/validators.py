"""Fail-closed validation for Two-Lane v1 campaign policy/approval/configuration documents.

Phase 2 (Issue #118) scope: this module validates DATA. A successful
``validate_campaign_bundle`` call returns a ``ValidatedCampaignBundle`` --
an immutable, inert data object. It never returns an invocation capability,
authorization token, provider client, or callable reaching provider code,
and no provider-facing module is imported anywhere in this package. Phase 3
(#119) is responsible for building the actual provider-boundary capability
from data this validates.

Every public ``validate_*`` function returns a ``ValidationResult`` (never
raises for ordinary invalid input -- parser/filesystem/KeyError/TypeError/
decimal exceptions are caught and converted to a deterministic
``ValidationResult.fail(...)``). ``failure_codes.CAMPAIGN_FAILURE_CODES`` is
the frozen, stable set of codes this module can return.

**Every successful public validator returns an immutable, typed model**
(``CampaignPolicy``, ``CampaignApproval``, ``ConfigurationIdentity``, or
``ValidatedCampaignBundle``) -- never a plain, mutable ``dict``. Internally,
private helpers operate on plain mappings during parsing/checking; the
public boundary freezes (``immutable.freeze``) and wraps exactly once, on
the way out. ``validate_campaign_approval`` and ``validate_configuration_identity``
consume an already-validated ``CampaignPolicy`` object (not an arbitrary
caller-supplied mapping) -- passing anything else fails closed rather than
silently trusting unvalidated data.

**Failure-code precedence is deterministic**, not a race against whichever
jsonschema error happens to sort first: the JSON Schemas are deliberately
loose on a handful of fields whose exact value (not just base type) is
owned exclusively by Python (see the ``$comment`` in each schema file) --
``policy_digest``/``configuration_id`` format and correctness, the four
``*_prohibited`` boolean VALUES, and every policy numeric limit/boundary/
cross-field rule, including the integer-lexeme-source-form rule the schema
language cannot express at all. A malformed value in one of those fields
therefore always produces its own specific code, never a generic
``*_SCHEMA_INVALID``; only a genuine structural violation (wrong scalar
TYPE, a missing required field, an unknown closed-object field) reaches
jsonschema at all for those fields.
"""

from __future__ import annotations

import dataclasses
import re
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping, Optional

import rfc8785

from . import digests, jcs, numeric_domain, schema_validation
from .failure_codes import CAMPAIGN_FAILURE_CODES
from .fs_adapter import ArtifactRootError, read_utf8_bytes, resolve_under_root
from .immutable import freeze
from .models import (
    CampaignApproval,
    CampaignPolicy,
    ConfigurationIdentity,
    ValidatedCampaignBundle,
    ValidationContext,
    ValidationResult,
    _create_campaign_approval,
    _create_campaign_policy,
    _create_configuration_identity,
    _is_genuine_campaign_policy,
)
from .yaml_profile import TwoLaneYamlError, parse_two_lane_yaml

__all__ = [
    "parse_two_lane_yaml",
    "compute_policy_digest",
    "compute_configuration_id",
    "validate_campaign_policy",
    "validate_campaign_approval",
    "validate_configuration_identity",
    "validate_campaign_bundle",
    "load_and_validate_policy_from_root",
    "load_and_validate_approval_from_root",
    "load_and_validate_configuration_from_root",
]

compute_policy_digest = digests.compute_policy_digest
compute_configuration_id = digests.compute_configuration_id

_SHA256_HEX_RE = re.compile(r"^[0-9a-f]{64}$")
_RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$"
)
_SAFE_INT_MIN = -9007199254740991
_SAFE_INT_MAX = 9007199254740991

# Placeholder detection uses two distinct, documented rules (never a bare
# substring search over free-form prose, which would misclassify legitimate
# text -- e.g. an approval_statement that happens to start "None of my
# objections remain" is NOT a placeholder):
#
# 1. EXACT-token rule: if the entire field value, stripped and lowercased,
#    equals one of these short English-word sentinels, it is a placeholder.
_EXACT_PLACEHOLDER_TOKENS = frozenset({
    "pending", "tbd", "todo", "none", "n/a", "changeme", "placeholder",
})
# 2. SUBSTRING rule: distinctive, bracketed template tokens vanishingly
#    unlikely to appear inside genuine prose, so a substring match is safe.
_SUBSTRING_PLACEHOLDER_MARKERS = (
    "<HUMAN-FILLS-IN", "FIXME", "<PRESENTED_DIGEST>", "<session-id>",
    "<message-id>",
)
_EXAMPLE_MARKER = "EXAMPLE_ONLY_NOT_AUTHORIZATION"
_MUTABLE_REF_TOKENS = frozenset({"head", "main", "master", "latest"})
_POLICY_INTEGER_FIELDS = (
    "max_attempt_slots",
    "max_provider_invocations",
    "max_attempts_per_configuration",
    "concurrency_ceiling",
)


def _parse_rfc3339(value: Any) -> Optional[datetime]:
    if not isinstance(value, str) or not _RFC3339_RE.match(value):
        return None
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return None
    return dt.astimezone(timezone.utc)


def _looks_like_mutable_ref(value: str) -> bool:
    if not isinstance(value, str):
        return True
    lowered = value.strip().lower()
    if lowered in _MUTABLE_REF_TOKENS:
        return True
    if lowered.startswith("origin/") or "/" in lowered and not re.match(r"^[0-9a-f]{40}$", lowered):
        return not re.match(r"^[0-9a-f]{40}$", value)
    return False


def _contains_placeholder(value: Any) -> bool:
    """Case-insensitive placeholder detection using the two documented rules
    above (module-level comment): exact-match against a short sentinel
    vocabulary, or substring match against unambiguous bracketed templates.
    """
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if stripped.lower() in _EXACT_PLACEHOLDER_TOKENS:
        return True
    return any(marker.lower() in value.lower() for marker in _SUBSTRING_PLACEHOLDER_MARKERS)


def _require_integer_lexeme(policy: Mapping[str, Any], field_name: str) -> Optional[ValidationResult]:
    """Reject a field whose parsed value is not a genuine ``int`` (i.e. whose
    YAML source lexeme carried a ``.``/exponent, such as ``5.0`` or ``5e0``),
    even though such a value may be mathematically integral, and independently
    enforce the interoperable safe-integer range. Both checks return
    ``CAMPAIGN_POLICY_LIMITS_INVALID`` -- this function, not the JSON Schema,
    is the sole owner of both the source-form and range decisions for these
    fields (see the schema's own ``$comment``).
    """
    value = policy.get(field_name)
    if type(value) is not int:
        return ValidationResult.fail(
            "CAMPAIGN_POLICY_LIMITS_INVALID",
            f"{field_name} must be an integer-lexeme source value (not a "
            f"decimal/exponent form like 5.0 or 5e0), got {value!r}",
        )
    if not (_SAFE_INT_MIN <= value <= _SAFE_INT_MAX):
        return ValidationResult.fail(
            "CAMPAIGN_POLICY_LIMITS_INVALID",
            f"{field_name} is outside the interoperable safe-integer range: {value!r}",
        )
    return None


def _safe(fn):
    """Run ``fn`` and convert any unexpected exception into an internal-error result."""
    try:
        return fn()
    except (KeyError, TypeError, ValueError, ArithmeticError, AttributeError) as exc:
        return ValidationResult.fail(
            "CAMPAIGN_INTERNAL_VALIDATION_ERROR", f"unexpected error: {exc}"
        )


# ---------------------------------------------------------------------------
# Campaign policy
# ---------------------------------------------------------------------------

@dataclasses.dataclass(frozen=True)
class _InternalResult:
    """Private intermediate result shape for internal-only helpers.

    Deliberately NOT the public ``ValidationResult`` class: a private
    mutable mapping (a freshly parsed document dict, a list of candidate
    (path, bytes) tuples) must never be placed inside a public
    ``ValidationResult.value``, which is documented and typed to hold only
    ``CampaignPolicy``/``CampaignApproval``/``ConfigurationIdentity``/
    ``ValidatedCampaignBundle``. ``_parse_document`` and ``_load_candidates``
    are private helpers whose result is always consumed and re-wrapped by
    their caller before anything is returned to a public caller.
    """

    valid: bool
    failure_code: Optional[str] = None
    detail: str = ""
    value: Any = None

    @staticmethod
    def ok(value: Any) -> "_InternalResult":
        return _InternalResult(valid=True, value=value)

    @staticmethod
    def fail(code: str, detail: str = "") -> "_InternalResult":
        return _InternalResult(valid=False, failure_code=code, detail=detail)


def _parse_document(source_bytes: bytes, *, missing_code: str,
                     profile_invalid_code: str,
                     open_map_root_field: Optional[str] = None) -> _InternalResult:
    if source_bytes is None:
        return _InternalResult.fail(missing_code, "document is missing")
    try:
        parsed = parse_two_lane_yaml(source_bytes, open_map_root_field=open_map_root_field)
    except TwoLaneYamlError as exc:
        return _InternalResult.fail(profile_invalid_code, f"{exc.code}: {exc.message}")
    if not isinstance(parsed, dict):
        return _InternalResult.fail(profile_invalid_code, "document did not parse to a mapping")
    return _InternalResult.ok(parsed)


def validate_campaign_policy(source_bytes: bytes,
                              context: ValidationContext) -> ValidationResult:
    """Validate a campaign policy document's source form, schema, limits,
    validity window, and digest. On success, ``.value`` is an immutable,
    typed ``CampaignPolicy`` (never a plain mutable mapping).
    """
    def _run() -> ValidationResult:
        parse_result = _parse_document(
            source_bytes,
            missing_code="CAMPAIGN_POLICY_MISSING",
            profile_invalid_code="CAMPAIGN_POLICY_SOURCE_PROFILE_INVALID",
        )
        if not parse_result.valid:
            return ValidationResult.fail(parse_result.failure_code, parse_result.detail)
        policy = parse_result.value

        # Missing or non-string is a structural fault (SCHEMA_INVALID); only
        # a well-formed string that names an unsupported version gets the
        # deliberate SCHEMA_UNSUPPORTED result. `.get()` alone would
        # conflate "absent" with "unsupported"; check presence explicitly.
        if "policy_schema_version" not in policy or not isinstance(policy["policy_schema_version"], str):
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_SCHEMA_INVALID",
                f"policy_schema_version is missing or not a string: {policy.get('policy_schema_version')!r}",
            )
        if policy["policy_schema_version"] != "1":
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_SCHEMA_UNSUPPORTED",
                f"unsupported policy_schema_version: {policy['policy_schema_version']!r}",
            )

        errors = schema_validation.policy_schema_errors(policy)
        if errors:
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_SCHEMA_INVALID", "; ".join(errors[:5])
            )

        if _parse_rfc3339(policy.get("prepared_at")) is None:
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_SCHEMA_INVALID",
                f"prepared_at is not a valid RFC3339 timestamp: {policy.get('prepared_at')!r}",
            )

        # policy_digest format/correctness is exclusively Python-owned (the
        # schema only requires it to be a string) -- see the deterministic
        # precedence note in this module's docstring.
        declared_digest = policy["policy_digest"]
        if not (isinstance(declared_digest, str) and _SHA256_HEX_RE.match(declared_digest)):
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_DIGEST_MALFORMED",
                f"policy_digest is not a well-formed sha256 hex string: {declared_digest!r}",
            )
        # Numeric-domain preflight: an oversized integer (outside the
        # interoperable safe-integer domain rfc8785 itself enforces) is an
        # ordinary, EXPECTED invalid-document case -- never
        # CAMPAIGN_INTERNAL_VALIDATION_ERROR. Checked recursively over the
        # WHOLE document (covers max_attempt_slots and friends,
        # token_ceiling, and cost_ceiling.amount in one pass) before digest
        # recomputation, so an oversized value never even reaches
        # rfc8785.dumps().
        if numeric_domain.find_out_of_domain_path(policy) is not None:
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_LIMITS_INVALID",
                f"a numeric field is outside the interoperable safe-integer "
                f"domain at {numeric_domain.find_out_of_domain_path(policy)}",
            )

        try:
            recomputed = digests.compute_policy_digest(policy)
        except (jcs.JCSError, rfc8785.CanonicalizationError, OverflowError) as exc:
            # Defense in depth: the preflight above should already have
            # caught any out-of-domain numeric value; if canonicalization
            # still fails for some other expected reason, it is still a
            # policy-limits-shaped problem, never an internal error.
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_LIMITS_INVALID",
                f"policy_digest could not be computed: {exc}",
            )
        if recomputed != declared_digest:
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_DIGEST_MISMATCH",
                f"recomputed digest {recomputed} != declared {declared_digest}",
            )

        limits_error = _check_policy_limits(policy)
        if limits_error:
            return limits_error

        window_result = _check_validity_window(policy, context)
        if window_result:
            return window_result

        return ValidationResult.ok(
            _create_campaign_policy(
                campaign_id=policy["campaign_id"],
                policy_digest=policy["policy_digest"],
                raw=freeze(policy),
            )
        )

    return _safe(_run)


def _check_policy_limits(policy: Mapping[str, Any]) -> Optional[ValidationResult]:
    for field_name in _POLICY_INTEGER_FIELDS:
        lexeme_error = _require_integer_lexeme(policy, field_name)
        if lexeme_error:
            return lexeme_error
    token_ceiling = policy.get("token_ceiling")
    if token_ceiling is not None:
        if type(token_ceiling) is not int:
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_LIMITS_INVALID",
                f"token_ceiling must be an integer-lexeme source value when non-null, "
                f"got {token_ceiling!r}",
            )
        if not (_SAFE_INT_MIN <= token_ceiling <= _SAFE_INT_MAX):
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_LIMITS_INVALID",
                f"token_ceiling is outside the interoperable safe-integer range: {token_ceiling!r}",
            )

    max_slots = policy["max_attempt_slots"]
    max_invocations = policy["max_provider_invocations"]
    max_per_config = policy["max_attempts_per_configuration"]
    concurrency = policy["concurrency_ceiling"]

    if max_slots < 1:
        return ValidationResult.fail("CAMPAIGN_POLICY_LIMITS_INVALID", "max_attempt_slots must be >= 1")
    if max_invocations < 0:
        return ValidationResult.fail("CAMPAIGN_POLICY_LIMITS_INVALID", "max_provider_invocations must be >= 0")
    if max_invocations > max_slots:
        return ValidationResult.fail(
            "CAMPAIGN_POLICY_LIMITS_INVALID",
            "max_provider_invocations must be <= max_attempt_slots",
        )
    if max_per_config < 1:
        return ValidationResult.fail(
            "CAMPAIGN_POLICY_LIMITS_INVALID", "max_attempts_per_configuration must be >= 1"
        )
    if concurrency < 1:
        return ValidationResult.fail("CAMPAIGN_POLICY_LIMITS_INVALID", "concurrency_ceiling must be >= 1")

    ids = policy["allowed_configuration_ids"]
    if len(ids) == 0:
        return ValidationResult.fail("CAMPAIGN_POLICY_LIMITS_INVALID", "allowed_configuration_ids must be non-empty")
    if len(set(ids)) != len(ids):
        return ValidationResult.fail("CAMPAIGN_POLICY_LIMITS_INVALID", "allowed_configuration_ids contains duplicates")
    if list(ids) != sorted(ids):
        return ValidationResult.fail(
            "CAMPAIGN_POLICY_LIMITS_INVALID", "allowed_configuration_ids is not lexicographically sorted"
        )
    for flag_name in (
        "target_mutation_prohibited",
        "fallback_prohibited",
        "repair_prohibited",
        "automatic_merge_prohibited",
    ):
        if policy[flag_name] is not True:
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_LIMITS_INVALID", f"{flag_name} must be exactly true"
            )

    # Execution-mode coupling (Lane A beta amendment, ADR 0023 section 21e).
    # The three fields are optional-and-absent for pre-amendment policies
    # (implicit provider_api); once declared they must be coherent, and the
    # coding_agent_native mode must leave no external model authorized.
    mode = policy.get("execution_mode")
    if mode is not None and mode not in ("provider_api", "coding_agent_native"):
        return ValidationResult.fail(
            "CAMPAIGN_POLICY_LIMITS_INVALID",
            f"execution_mode must be 'provider_api' or 'coding_agent_native', "
            f"got {mode!r}",
        )
    prohibited = policy.get("external_provider_api_prohibited")
    if prohibited is True and mode != "coding_agent_native":
        return ValidationResult.fail(
            "CAMPAIGN_POLICY_LIMITS_INVALID",
            "external_provider_api_prohibited: true requires execution_mode "
            "'coding_agent_native'",
        )
    if mode == "coding_agent_native":
        if prohibited is not True:
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_LIMITS_INVALID",
                "execution_mode 'coding_agent_native' requires "
                "external_provider_api_prohibited: true",
            )
        if not str(policy.get("execution_surface", "") or "").strip():
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_LIMITS_INVALID",
                "execution_mode 'coding_agent_native' requires a non-empty "
                "execution_surface",
            )
        if policy.get("allowed_models"):
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_LIMITS_INVALID",
                "execution_mode 'coding_agent_native' requires allowed_models: [] "
                "(no external model API is authorized)",
            )
    return None


def _check_validity_window(policy: Mapping[str, Any],
                            context: ValidationContext) -> Optional[ValidationResult]:
    window = policy["validity_window"]
    not_before = _parse_rfc3339(window.get("not_before"))
    not_after = _parse_rfc3339(window.get("not_after"))
    if not_before is None or not_after is None or not (not_before < not_after):
        return ValidationResult.fail(
            "CAMPAIGN_POLICY_VALIDITY_WINDOW_INVALID",
            "validity_window is malformed or not_before is not strictly before not_after",
        )

    now = _parse_rfc3339(context.current_time)
    if now is None:
        return ValidationResult.fail(
            "CAMPAIGN_POLICY_VALIDITY_WINDOW_INVALID",
            "context.current_time is not a valid RFC3339 timestamp",
        )
    if not context.enforce_validity_window:
        # Report-only verification (e.g. after campaign expiry): the
        # policy still validates in full (digests, limits, coherence) but
        # the wall clock is NOT required to sit inside the execution
        # window. This never authorizes a reservation or invocation --
        # the execution commands always enforce the window (fail closed).
        return None
    if now < not_before:
        return ValidationResult.fail("CAMPAIGN_POLICY_NOT_YET_VALID", "current time is before validity_window.not_before")
    if now >= not_after:
        return ValidationResult.fail("CAMPAIGN_POLICY_EXPIRED", "current time is at or after validity_window.not_after")
    return None


# ---------------------------------------------------------------------------
# Campaign approval
# ---------------------------------------------------------------------------

def validate_campaign_approval(source_bytes: bytes, policy: CampaignPolicy,
                                context: ValidationContext) -> ValidationResult:
    """Validate a campaign approval document against an already-validated
    ``CampaignPolicy`` (never an arbitrary caller-supplied mapping -- passing
    anything else fails closed with ``CAMPAIGN_INTERNAL_VALIDATION_ERROR``
    rather than silently trusting unvalidated data). On success, ``.value``
    is an immutable, typed ``CampaignApproval``.

    Never infers approval from merge state, write access, branch ownership,
    PR authorship, or silence -- only from the explicit fields on the
    approval document, checked against ``context.allowed_approver_identities``.
    """
    def _run() -> ValidationResult:
        if not _is_genuine_campaign_policy(policy):
            return ValidationResult.fail(
                "CAMPAIGN_INTERNAL_VALIDATION_ERROR",
                "policy argument must be a genuine CampaignPolicy produced by "
                f"validate_campaign_policy(), got {type(policy).__name__}",
            )

        parse_result = _parse_document(
            source_bytes,
            missing_code="CAMPAIGN_APPROVAL_MISSING",
            profile_invalid_code="CAMPAIGN_APPROVAL_SOURCE_PROFILE_INVALID",
        )
        if not parse_result.valid:
            return ValidationResult.fail(parse_result.failure_code, parse_result.detail)
        approval = parse_result.value

        if "approval_schema_version" not in approval or not isinstance(approval["approval_schema_version"], str):
            return ValidationResult.fail(
                "CAMPAIGN_APPROVAL_SCHEMA_INVALID",
                f"approval_schema_version is missing or not a string: {approval.get('approval_schema_version')!r}",
            )
        if approval["approval_schema_version"] != "1":
            return ValidationResult.fail(
                "CAMPAIGN_APPROVAL_SCHEMA_UNSUPPORTED",
                f"unsupported approval_schema_version: {approval['approval_schema_version']!r}",
            )

        # Marker detection MUST win before any operative-grade schema check
        # runs, and regardless of whatever else is wrong (or deliberately
        # placeholder) in the rest of the document -- a template can never
        # become operative no matter how it is otherwise malformed.
        if "marker" in approval:
            return ValidationResult.fail(
                "CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE",
                f"approval carries marker {approval.get('marker')!r} and can never be operative",
            )

        errors = schema_validation.approval_schema_errors(approval)
        if errors:
            return ValidationResult.fail(
                "CAMPAIGN_APPROVAL_SCHEMA_INVALID", "; ".join(errors[:5])
            )

        if _parse_rfc3339(approval.get("approved_at")) is None:
            return ValidationResult.fail(
                "CAMPAIGN_APPROVAL_SCHEMA_INVALID",
                f"approved_at is not a valid RFC3339 timestamp: {approval.get('approved_at')!r}",
            )

        if "approval_source" in approval:
            # Conversation-approval receipt (active_human_conversation, the
            # human's standalone 'approve' in the active conversation; the
            # conversation, not any external artifact, is the authority).
            # The receipt must bind the exact policy and never exceed its
            # envelope; there is no claimed identity -- the coding agent
            # records the human's decision, it does not identify itself.
            for field_name in ("approved_at", "reference",
                               "campaign_id", "policy_digest"):
                if _contains_placeholder(approval.get(field_name, "")):
                    return ValidationResult.fail(
                        "CAMPAIGN_APPROVAL_PLACEHOLDER_PRESENT",
                        f"field {field_name!r} contains an unfilled placeholder token",
                    )
            if (approval["campaign_id"] != policy.campaign_id
                    or approval["policy_digest"] != policy.policy_digest):
                return ValidationResult.fail(
                    "CAMPAIGN_APPROVAL_POLICY_MISMATCH",
                    "approval campaign_id/policy_digest does not match the "
                    "policy being approved",
                )
            if int(approval["maximum_attempts"]) > int(policy.raw.get("max_attempt_slots", 0)):
                return ValidationResult.fail(
                    "CAMPAIGN_APPROVAL_ENVELOPE_EXCEEDED",
                    f"approval maximum_attempts {approval['maximum_attempts']} "
                    f"exceeds the policy limit "
                    f"{policy.raw.get('max_attempt_slots')}",
                )
            if int(approval["concurrency"]) > int(policy.raw.get("concurrency_ceiling", 0)):
                return ValidationResult.fail(
                    "CAMPAIGN_APPROVAL_ENVELOPE_EXCEEDED",
                    f"approval concurrency {approval['concurrency']} exceeds "
                    f"the policy ceiling "
                    f"{policy.raw.get('concurrency_ceiling')}",
                )
            if policy.raw.get("automatic_merge_prohibited") is not True:
                return ValidationResult.fail(
                    "CAMPAIGN_APPROVAL_ENVELOPE_EXCEEDED",
                    "the approved policy does not prohibit automatic merge; "
                    "the receipt's prohibition cannot bind it",
                )
            if policy.raw.get("external_provider_api_prohibited") is not True:
                return ValidationResult.fail(
                    "CAMPAIGN_APPROVAL_ENVELOPE_EXCEEDED",
                    "the approved policy does not prohibit external provider "
                    "APIs; the receipt's prohibition cannot bind it",
                )
            if approval["classification"] != policy.raw.get("classification", ""):
                return ValidationResult.fail(
                    "CAMPAIGN_APPROVAL_ENVELOPE_EXCEEDED",
                    f"approval classification {approval['classification']!r} "
                    f"differs from the policy "
                    f"{policy.raw.get('classification')!r}",
                )
            approved_at = _parse_rfc3339(approval["approved_at"])
            window = policy.raw.get("validity_window") or {}
            not_after = _parse_rfc3339(window.get("not_after"))
            if not_after is not None and approved_at > not_after:
                return ValidationResult.fail(
                    "CAMPAIGN_APPROVAL_ENVELOPE_EXCEEDED",
                    f"approval approved_at {approval['approved_at']} is after "
                    f"the policy window end {window.get('not_after')}",
                )
        else:
            for field_name in ("claimed_approver_identity", "approval_statement",
                               "approved_at", "campaign_id", "policy_digest"):
                if _contains_placeholder(approval.get(field_name, "")):
                    return ValidationResult.fail(
                        "CAMPAIGN_APPROVAL_PLACEHOLDER_PRESENT",
                        f"field {field_name!r} contains an unfilled placeholder token",
                    )
            provenance = approval["approval_provenance"]
            mechanism = provenance.get("mechanism", "")
            reference = provenance.get("reference", "")
            if (_contains_placeholder(mechanism) or _contains_placeholder(reference)
                    or not mechanism.strip() or not reference.strip()
                    or mechanism.strip().lower() == "none"):
                return ValidationResult.fail(
                    "CAMPAIGN_APPROVAL_PROVENANCE_INVALID",
                    "approval_provenance.mechanism/reference is missing, placeholder, or 'none'",
                )

            if (approval["campaign_id"] != policy.campaign_id
                    or approval["policy_digest"] != policy.policy_digest):
                return ValidationResult.fail(
                    "CAMPAIGN_APPROVAL_POLICY_MISMATCH",
                    "approval campaign_id/policy_digest does not match the policy being approved",
                )

            if approval["claimed_approver_identity"] not in context.allowed_approver_identities:
                return ValidationResult.fail(
                    "CAMPAIGN_APPROVER_UNAUTHORIZED",
                    f"{approval['claimed_approver_identity']!r} is not an allowed approver identity",
                )

        return ValidationResult.ok(
            _create_campaign_approval(
                campaign_id=approval["campaign_id"],
                policy_digest=approval["policy_digest"],
                claimed_approver_identity=approval.get("claimed_approver_identity", ""),
                raw=freeze(approval),
            )
        )

    return _safe(_run)


# ---------------------------------------------------------------------------
# Configuration identity
# ---------------------------------------------------------------------------

def validate_configuration_identity(source_bytes: bytes,
                                     policy: CampaignPolicy) -> ValidationResult:
    """Validate a configuration-identity document against an already-validated
    ``CampaignPolicy`` and every conjunctive allowlist check independently
    (ADR 0023 section 9d / campaign-policy schema's "Conjunctive
    authorization semantics"). Passing one check never overrides another. On
    success, ``.value`` is an immutable, typed ``ConfigurationIdentity``.
    """
    def _run() -> ValidationResult:
        if not _is_genuine_campaign_policy(policy):
            return ValidationResult.fail(
                "CAMPAIGN_INTERNAL_VALIDATION_ERROR",
                "policy argument must be a genuine CampaignPolicy produced by "
                f"validate_campaign_policy(), got {type(policy).__name__}",
            )

        parse_result = _parse_document(
            source_bytes,
            missing_code="CAMPAIGN_CONFIGURATION_MISSING",
            profile_invalid_code="CAMPAIGN_CONFIGURATION_SOURCE_PROFILE_INVALID",
            open_map_root_field="execution_parameters",
        )
        if not parse_result.valid:
            return ValidationResult.fail(parse_result.failure_code, parse_result.detail)
        configuration = parse_result.value

        if ("configuration_schema_version" not in configuration
                or not isinstance(configuration["configuration_schema_version"], str)):
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_SCHEMA_INVALID",
                "configuration_schema_version is missing or not a string: "
                f"{configuration.get('configuration_schema_version')!r}",
            )
        if configuration["configuration_schema_version"] != "1":
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_SCHEMA_UNSUPPORTED",
                f"unsupported configuration_schema_version: {configuration['configuration_schema_version']!r}",
            )

        errors = schema_validation.configuration_schema_errors(configuration)
        if errors:
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_SCHEMA_INVALID", "; ".join(errors[:5])
            )

        for ref_field in (
            "framework_sha", "target_sha", "prompt_or_skill_revision", "validator_revision",
        ):
            if _looks_like_mutable_ref(configuration[ref_field]):
                return ValidationResult.fail(
                    "CAMPAIGN_CONFIGURATION_SCHEMA_INVALID",
                    f"{ref_field} is a mutable ref, not an immutable revision: {configuration[ref_field]!r}",
                )

        # configuration_id format/correctness is exclusively Python-owned
        # (the schema only requires it to be a string) -- see the
        # deterministic precedence note in this module's docstring.
        declared_id = configuration["configuration_id"]
        if not (isinstance(declared_id, str) and _SHA256_HEX_RE.match(declared_id)):
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_ID_MALFORMED",
                f"configuration_id is not a well-formed sha256 hex string: {declared_id!r}",
            )
        # Numeric-domain preflight over execution_parameters -- the only
        # place an arbitrary (open-map) numeric value can appear in a
        # configuration document. An oversized integer anywhere in it
        # (including nested mappings/sequences) is an ordinary, EXPECTED
        # invalid-document case, never CAMPAIGN_INTERNAL_VALIDATION_ERROR.
        out_of_domain_path = numeric_domain.find_out_of_domain_path(
            configuration.get("execution_parameters", {})
        )
        if out_of_domain_path is not None:
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_NUMERIC_DOMAIN_INVALID",
                f"a numeric value in execution_parameters is outside the "
                f"interoperable safe-integer domain at execution_parameters{out_of_domain_path[1:]}",
            )

        try:
            recomputed = digests.compute_configuration_id(configuration)
        except (jcs.JCSError, rfc8785.CanonicalizationError, OverflowError) as exc:
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_NUMERIC_DOMAIN_INVALID",
                f"configuration_id could not be computed: {exc}",
            )
        if recomputed != declared_id:
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_ID_MISMATCH",
                f"recomputed configuration_id {recomputed} != declared {declared_id}",
            )

        # campaign_id is deliberately EXCLUDED from the configuration_id hash
        # (ADR 0023 section 10c), precisely so the same byte-identical
        # configuration is recognizable across campaigns -- which means
        # digest/ID matching alone can never catch a configuration document
        # whose campaign_id was swapped for a different campaign's. This
        # check exists specifically because that exclusion would otherwise
        # be a binding gap.
        if configuration["campaign_id"] != policy.campaign_id:
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_CAMPAIGN_MISMATCH",
                f"configuration.campaign_id {configuration['campaign_id']!r} != "
                f"policy.campaign_id {policy.campaign_id!r}",
            )

        # Independent, conjunctive allowlist checks -- every one runs even if
        # an earlier one already failed conceptually; each has its own code,
        # and none may substitute for another.
        if declared_id not in set(policy.raw["allowed_configuration_ids"]):
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_ID_NOT_ALLOWED",
                f"{declared_id} is not a member of allowed_configuration_ids",
            )
        if configuration["framework_sha"] not in set(policy.raw["allowed_framework_shas"]):
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_FRAMEWORK_NOT_ALLOWED",
                f"{configuration['framework_sha']} is not a member of allowed_framework_shas",
            )
        target_pair = (configuration["target_repository"], configuration["target_sha"])
        allowed_targets = {(t["repository"], t["sha"]) for t in policy.raw["allowed_targets"]}
        if target_pair not in allowed_targets:
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_TARGET_NOT_ALLOWED",
                f"{target_pair} is not a member of allowed_targets",
            )
        # Model membership is the PROVIDER-API check. For
        # coding_agent_native campaigns there is no external model: the
        # configuration's model_identifier carries the execution surface,
        # which must equal the policy's declared execution_surface
        # (configuration <-> policy coherence without provider semantics).
        if policy.raw.get("execution_mode") == "coding_agent_native":
            if configuration["model_identifier"] != policy.raw.get(
                "execution_surface", ""
            ):
                return ValidationResult.fail(
                    "CAMPAIGN_CONFIGURATION_MODEL_NOT_ALLOWED",
                    "coding_agent_native: configuration model_identifier "
                    f"{configuration['model_identifier']!r} must equal the "
                    "policy execution_surface "
                    f"{policy.raw.get('execution_surface')!r} (the "
                    "execution surface is not a member of the empty "
                    "allowed_models)",
                )
        elif configuration["model_identifier"] not in set(policy.raw["allowed_models"]):
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_MODEL_NOT_ALLOWED",
                f"{configuration['model_identifier']} is not a member of allowed_models",
            )
        if configuration["artifact_type"] not in set(policy.raw["allowed_artifact_types"]):
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_ARTIFACT_TYPE_NOT_ALLOWED",
                f"{configuration['artifact_type']} is not a member of allowed_artifact_types",
            )

        return ValidationResult.ok(
            _create_configuration_identity(
                configuration_id=configuration["configuration_id"],
                campaign_id=configuration["campaign_id"],
                raw=freeze(configuration),
            )
        )

    return _safe(_run)


# ---------------------------------------------------------------------------
# Bundle (conjunction of all three)
# ---------------------------------------------------------------------------

def validate_campaign_bundle(policy_bytes: bytes, approval_bytes: bytes,
                              configuration_bytes: bytes,
                              context: ValidationContext) -> ValidationResult:
    """Validate policy + approval + configuration as one bundle.

    First-failure precedence (ADR 0023-consistent, documented in
    ``failure_codes.py``): source/profile parsing and schema/version validity
    happen inside each ``validate_*`` call before digest/identity integrity,
    approval binding, validity window, and configuration allowlists. This
    function calls them in that fixed order: policy, then approval (bound to
    the validated policy), then configuration (bound to the validated
    policy). On success, returns a ``ValidationResult`` whose ``.value`` is
    the ``ValidatedCampaignBundle`` -- inert data, never a capability. The
    bundle composes the three ALREADY-validated, already-immutable typed
    objects returned by the three single-artifact validators directly; it
    does not reconstruct new wrappers from mutable mappings.
    """
    def _run() -> ValidationResult:
        policy_result = validate_campaign_policy(policy_bytes, context)
        if not policy_result.valid:
            return policy_result
        policy = policy_result.value
        assert isinstance(policy, CampaignPolicy)

        approval_result = validate_campaign_approval(approval_bytes, policy, context)
        if not approval_result.valid:
            return approval_result
        approval = approval_result.value
        assert isinstance(approval, CampaignApproval)

        configuration_result = validate_configuration_identity(configuration_bytes, policy)
        if not configuration_result.valid:
            return configuration_result
        configuration = configuration_result.value
        assert isinstance(configuration, ConfigurationIdentity)

        bundle = ValidatedCampaignBundle(
            policy=policy,
            approval=approval,
            configuration=configuration,
        )
        return ValidationResult(valid=True, value=bundle)

    return _safe(_run)


# ---------------------------------------------------------------------------
# Filesystem / artifact-root loaders
# ---------------------------------------------------------------------------

def _load_candidates(artifact_root: str, candidate_paths: Iterable[str]) -> _InternalResult:
    """Resolve and read a set of candidate paths beneath ``artifact_root``.

    Never globs -- callers supply explicit candidate paths (ADR 0023
    section 15 / "no operative campaign-directory layout" constraint). Zero
    matches -> missing. More than one match -> ambiguous. Exactly one match
    -> its bytes. Returns a private ``_InternalResult`` (never the public
    ``ValidationResult``) -- its ``.value`` is a list of ``(path, bytes)``
    candidate tuples, a private intermediate shape that must never appear
    inside a public ``ValidationResult.value``.
    """
    found: list[tuple[str, bytes]] = []
    for candidate in candidate_paths:
        try:
            resolved = resolve_under_root(candidate, artifact_root)
            data = read_utf8_bytes(resolved)
        except ArtifactRootError as exc:
            return _InternalResult.fail(exc.code, exc.message)
        if data is not None:
            found.append((candidate, data))
    return _InternalResult.ok(found)


def load_and_validate_policy_from_root(artifact_root: str, candidate_paths: Iterable[str],
                                        context: ValidationContext) -> ValidationResult:
    load_result = _load_candidates(artifact_root, candidate_paths)
    if not load_result.valid:
        return ValidationResult.fail(load_result.failure_code, load_result.detail)
    matches = load_result.value
    if len(matches) == 0:
        return ValidationResult.fail("CAMPAIGN_POLICY_MISSING", "no policy candidate path exists")
    if len(matches) > 1:
        return ValidationResult.fail(
            "CAMPAIGN_POLICY_IDENTITY_AMBIGUOUS",
            f"{len(matches)} candidate policy paths exist: {[p for p, _ in matches]}",
        )
    _, data = matches[0]
    return validate_campaign_policy(data, context)


def load_and_validate_approval_from_root(artifact_root: str, candidate_paths: Iterable[str],
                                          policy: CampaignPolicy,
                                          context: ValidationContext) -> ValidationResult:
    load_result = _load_candidates(artifact_root, candidate_paths)
    if not load_result.valid:
        return ValidationResult.fail(load_result.failure_code, load_result.detail)
    matches = load_result.value
    if len(matches) == 0:
        return ValidationResult.fail("CAMPAIGN_APPROVAL_MISSING", "no approval candidate path exists")

    operative_matches = []
    for path, data in matches:
        result = validate_campaign_approval(data, policy, context)
        if result.valid:
            operative_matches.append((path, result))
    if len(operative_matches) > 1:
        return ValidationResult.fail(
            "CAMPAIGN_APPROVAL_AMBIGUOUS",
            f"{len(operative_matches)} candidate paths carry an operative approval "
            f"for this policy: {[p for p, _ in operative_matches]}",
        )
    if len(operative_matches) == 1:
        return operative_matches[0][1]
    # No operative match; surface the first candidate's failure for diagnosis.
    _, data = matches[0]
    return validate_campaign_approval(data, policy, context)


def load_and_validate_configuration_from_root(artifact_root: str, candidate_paths: Iterable[str],
                                               policy: CampaignPolicy) -> ValidationResult:
    load_result = _load_candidates(artifact_root, candidate_paths)
    if not load_result.valid:
        return ValidationResult.fail(load_result.failure_code, load_result.detail)
    matches = load_result.value
    if len(matches) == 0:
        return ValidationResult.fail("CAMPAIGN_CONFIGURATION_MISSING", "no configuration candidate path exists")
    if len(matches) > 1:
        return ValidationResult.fail(
            "CAMPAIGN_CONFIGURATION_IDENTITY_AMBIGUOUS",
            f"{len(matches)} candidate configuration paths exist: {[p for p, _ in matches]}",
        )
    _, data = matches[0]
    return validate_configuration_identity(data, policy)
