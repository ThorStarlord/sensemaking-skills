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
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping, Optional

from . import digests, schema_validation
from .failure_codes import CAMPAIGN_FAILURE_CODES
from .fs_adapter import ArtifactRootError, read_utf8_bytes, resolve_under_root
from .models import (
    CampaignApproval,
    CampaignPolicy,
    ConfigurationIdentity,
    ValidatedCampaignBundle,
    ValidationContext,
    ValidationResult,
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
_PLACEHOLDER_MARKERS = ("<HUMAN-FILLS-IN", "TODO", "TBD", "<PLACEHOLDER>", "FIXME")
_EXAMPLE_MARKER = "EXAMPLE_ONLY_NOT_AUTHORIZATION"
_MUTABLE_REF_TOKENS = frozenset(
    {"head", "main", "master", "latest"}
)


def _parse_rfc3339(value: str) -> Optional[datetime]:
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
        # Only exact 40-char lowercase hex commit SHAs are accepted as
        # immutable framework/target refs in schema v1; anything else
        # (branch-like, remote-tracking-like) is rejected as mutable.
        return not re.match(r"^[0-9a-f]{40}$", value)
    return False


def _contains_placeholder(value: str) -> bool:
    return isinstance(value, str) and any(marker in value for marker in _PLACEHOLDER_MARKERS)


def _safe(fn):
    """Run ``fn`` and convert any unexpected exception into an internal-error result."""
    try:
        return fn()
    except (KeyError, TypeError, ValueError, ArithmeticError) as exc:
        return ValidationResult.fail(
            "CAMPAIGN_INTERNAL_VALIDATION_ERROR", f"unexpected error: {exc}"
        )


# ---------------------------------------------------------------------------
# Campaign policy
# ---------------------------------------------------------------------------

def _parse_document(source_bytes: bytes, *, missing_code: str,
                     profile_invalid_code: str,
                     open_map_root_field: Optional[str] = None) -> ValidationResult:
    if source_bytes is None:
        return ValidationResult.fail(missing_code, "document is missing")
    try:
        parsed = parse_two_lane_yaml(source_bytes, open_map_root_field=open_map_root_field)
    except TwoLaneYamlError as exc:
        return ValidationResult.fail(profile_invalid_code, f"{exc.code}: {exc.message}")
    if not isinstance(parsed, dict):
        return ValidationResult.fail(profile_invalid_code, "document did not parse to a mapping")
    return ValidationResult.ok(parsed)


def validate_campaign_policy(source_bytes: bytes,
                              context: ValidationContext) -> ValidationResult:
    """Validate a campaign policy document's source form, schema, limits,
    validity window, and digest -- everything that does not require the
    approval or configuration documents.
    """
    def _run() -> ValidationResult:
        parse_result = _parse_document(
            source_bytes,
            missing_code="CAMPAIGN_POLICY_MISSING",
            profile_invalid_code="CAMPAIGN_POLICY_SOURCE_PROFILE_INVALID",
        )
        if not parse_result.valid:
            return parse_result
        policy = parse_result.value

        version = policy.get("policy_schema_version")
        if version != "1":
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_SCHEMA_UNSUPPORTED",
                f"unsupported policy_schema_version: {version!r}",
            )

        errors = schema_validation.policy_schema_errors(policy)
        if errors:
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_SCHEMA_INVALID", "; ".join(errors[:5])
            )

        declared_digest = policy["policy_digest"]
        if not _SHA256_HEX_RE.match(declared_digest):
            return ValidationResult.fail(
                "CAMPAIGN_POLICY_DIGEST_MALFORMED",
                f"policy_digest is not a well-formed sha256 hex string: {declared_digest!r}",
            )
        recomputed = digests.compute_policy_digest(policy)
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

        return ValidationResult.ok(policy)

    return _safe(_run)


def _check_policy_limits(policy: Mapping[str, Any]) -> Optional[ValidationResult]:
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
    return None


def _check_validity_window(policy: Mapping[str, Any],
                            context: ValidationContext) -> Optional[ValidationResult]:
    window = policy["validity_window"]
    not_before = _parse_rfc3339(window.get("not_before", ""))
    not_after = _parse_rfc3339(window.get("not_after", ""))
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
    if now < not_before:
        return ValidationResult.fail("CAMPAIGN_POLICY_NOT_YET_VALID", "current time is before validity_window.not_before")
    if now >= not_after:
        return ValidationResult.fail("CAMPAIGN_POLICY_EXPIRED", "current time is at or after validity_window.not_after")
    return None


# ---------------------------------------------------------------------------
# Campaign approval
# ---------------------------------------------------------------------------

def validate_campaign_approval(source_bytes: bytes, policy: Mapping[str, Any],
                                context: ValidationContext) -> ValidationResult:
    """Validate a campaign approval document against an already-validated policy.

    Never infers approval from merge state, write access, branch ownership,
    PR authorship, or silence -- only from the explicit fields on the
    approval document, checked against ``context.allowed_approver_identities``.
    """
    def _run() -> ValidationResult:
        parse_result = _parse_document(
            source_bytes,
            missing_code="CAMPAIGN_APPROVAL_MISSING",
            profile_invalid_code="CAMPAIGN_APPROVAL_SOURCE_PROFILE_INVALID",
        )
        if not parse_result.valid:
            return parse_result
        approval = parse_result.value

        version = approval.get("approval_schema_version")
        if version != "1":
            return ValidationResult.fail(
                "CAMPAIGN_APPROVAL_SCHEMA_UNSUPPORTED",
                f"unsupported approval_schema_version: {version!r}",
            )

        errors = schema_validation.approval_schema_errors(approval)
        if errors:
            return ValidationResult.fail(
                "CAMPAIGN_APPROVAL_SCHEMA_INVALID", "; ".join(errors[:5])
            )

        if "marker" in approval:
            return ValidationResult.fail(
                "CAMPAIGN_APPROVAL_EXAMPLE_TEMPLATE_NON_OPERATIVE",
                f"approval carries marker {approval['marker']!r} and can never be operative",
            )

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

        if (approval["campaign_id"] != policy["campaign_id"]
                or approval["policy_digest"] != policy["policy_digest"]):
            return ValidationResult.fail(
                "CAMPAIGN_APPROVAL_POLICY_MISMATCH",
                "approval campaign_id/policy_digest does not match the policy being approved",
            )

        if approval["claimed_approver_identity"] not in context.allowed_approver_identities:
            return ValidationResult.fail(
                "CAMPAIGN_APPROVER_UNAUTHORIZED",
                f"{approval['claimed_approver_identity']!r} is not an allowed approver identity",
            )

        return ValidationResult.ok(approval)

    return _safe(_run)


# ---------------------------------------------------------------------------
# Configuration identity
# ---------------------------------------------------------------------------

def validate_configuration_identity(source_bytes: bytes,
                                     policy: Mapping[str, Any]) -> ValidationResult:
    """Validate a configuration-identity document and every conjunctive
    allowlist check independently (ADR 0023 section 9d / campaign-policy
    schema's "Conjunctive authorization semantics"). Passing one check never
    overrides another.
    """
    def _run() -> ValidationResult:
        parse_result = _parse_document(
            source_bytes,
            missing_code="CAMPAIGN_CONFIGURATION_MISSING",
            profile_invalid_code="CAMPAIGN_CONFIGURATION_SCHEMA_INVALID",
            open_map_root_field="execution_parameters",
        )
        if not parse_result.valid:
            return parse_result
        configuration = parse_result.value

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

        declared_id = configuration["configuration_id"]
        if not _SHA256_HEX_RE.match(declared_id):
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_ID_MALFORMED",
                f"configuration_id is not a well-formed sha256 hex string: {declared_id!r}",
            )
        recomputed = digests.compute_configuration_id(configuration)
        if recomputed != declared_id:
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_ID_MISMATCH",
                f"recomputed configuration_id {recomputed} != declared {declared_id}",
            )

        # Independent, conjunctive allowlist checks -- every one runs even if
        # an earlier one already failed conceptually; each has its own code,
        # and none may substitute for another.
        if declared_id not in set(policy["allowed_configuration_ids"]):
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_ID_NOT_ALLOWED",
                f"{declared_id} is not a member of allowed_configuration_ids",
            )
        if configuration["framework_sha"] not in set(policy["allowed_framework_shas"]):
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_FRAMEWORK_NOT_ALLOWED",
                f"{configuration['framework_sha']} is not a member of allowed_framework_shas",
            )
        target_pair = (configuration["target_repository"], configuration["target_sha"])
        allowed_targets = {(t["repository"], t["sha"]) for t in policy["allowed_targets"]}
        if target_pair not in allowed_targets:
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_TARGET_NOT_ALLOWED",
                f"{target_pair} is not a member of allowed_targets",
            )
        if configuration["model_identifier"] not in set(policy["allowed_models"]):
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_MODEL_NOT_ALLOWED",
                f"{configuration['model_identifier']} is not a member of allowed_models",
            )
        if configuration["artifact_type"] not in set(policy["allowed_artifact_types"]):
            return ValidationResult.fail(
                "CAMPAIGN_CONFIGURATION_ARTIFACT_TYPE_NOT_ALLOWED",
                f"{configuration['artifact_type']} is not a member of allowed_artifact_types",
            )

        return ValidationResult.ok(configuration)

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
    the ``ValidatedCampaignBundle`` -- inert data, never a capability.
    """
    def _run() -> ValidationResult:
        policy_result = validate_campaign_policy(policy_bytes, context)
        if not policy_result.valid:
            return policy_result
        policy = policy_result.value

        approval_result = validate_campaign_approval(approval_bytes, policy, context)
        if not approval_result.valid:
            return approval_result
        approval = approval_result.value

        configuration_result = validate_configuration_identity(configuration_bytes, policy)
        if not configuration_result.valid:
            return configuration_result
        configuration = configuration_result.value

        bundle = ValidatedCampaignBundle(
            policy=CampaignPolicy(
                campaign_id=policy["campaign_id"],
                policy_digest=policy["policy_digest"],
                raw=policy,
            ),
            approval=CampaignApproval(
                campaign_id=approval["campaign_id"],
                policy_digest=approval["policy_digest"],
                claimed_approver_identity=approval["claimed_approver_identity"],
                raw=approval,
            ),
            configuration=ConfigurationIdentity(
                configuration_id=configuration["configuration_id"],
                campaign_id=configuration["campaign_id"],
                raw=configuration,
            ),
        )
        return ValidationResult(valid=True, value=bundle)

    return _safe(_run)


# ---------------------------------------------------------------------------
# Filesystem / artifact-root loaders
# ---------------------------------------------------------------------------

def _load_candidates(artifact_root: str, candidate_paths: Iterable[str]) -> ValidationResult:
    """Resolve and read a set of candidate paths beneath ``artifact_root``.

    Never globs -- callers supply explicit candidate paths (ADR 0023
    section 15 / "no operative campaign-directory layout" constraint). Zero
    matches -> missing. More than one match -> ambiguous. Exactly one match
    -> its bytes.
    """
    found: list[tuple[str, bytes]] = []
    for candidate in candidate_paths:
        try:
            resolved = resolve_under_root(candidate, artifact_root)
        except ArtifactRootError as exc:
            return ValidationResult.fail(exc.code, exc.message, path=candidate)
        data = read_utf8_bytes(resolved)
        if data is not None:
            found.append((candidate, data))
    return ValidationResult.ok({"matches": found})  # internal helper shape


def load_and_validate_policy_from_root(artifact_root: str, candidate_paths: Iterable[str],
                                        context: ValidationContext) -> ValidationResult:
    load_result = _load_candidates(artifact_root, candidate_paths)
    if not load_result.valid:
        return load_result
    matches = load_result.value["matches"]
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
                                          policy: Mapping[str, Any],
                                          context: ValidationContext) -> ValidationResult:
    load_result = _load_candidates(artifact_root, candidate_paths)
    if not load_result.valid:
        return load_result
    matches = load_result.value["matches"]
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
                                               policy: Mapping[str, Any]) -> ValidationResult:
    load_result = _load_candidates(artifact_root, candidate_paths)
    if not load_result.valid:
        return load_result
    matches = load_result.value["matches"]
    if len(matches) == 0:
        return ValidationResult.fail("CAMPAIGN_CONFIGURATION_MISSING", "no configuration candidate path exists")
    if len(matches) > 1:
        return ValidationResult.fail(
            "CAMPAIGN_POLICY_IDENTITY_AMBIGUOUS",
            f"{len(matches)} candidate configuration paths exist: {[p for p, _ in matches]}",
        )
    _, data = matches[0]
    return validate_configuration_identity(data, policy)
