"""Gate A authorization consumer for the Stage 1 controlled-run workflow.

This module is the *consumer* that the Stage 1 preparation contract
(docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md, section 2j)
specified but deliberately did not implement. Hard stop 24,
``GATE_A_AUTHORIZATION_CONSUMER_NOT_IMPLEMENTED``, existed precisely because
nothing in this repository loaded, hashed, or enforced the planned
authorization artifacts.

What this module is for
-----------------------
It sits between an *authorization record* (plus its externally stored digest
and a physically distinct owner-approval artifact) and a *model invocation*.
The core invariant is:

    No valid authorization capability, no path to the model invocation
    function.

Enforcement is by *capability*, not by flag. ``authorize()`` returns a typed
``AuthorizationDecision``; only a decision with ``authorized=True`` yields an
``AuthorizedInvocation`` capability object. The model-invoking executors in
``skill_executor.py`` require that capability object for controlled-experiment
(Stage 1) invocations and fail closed without it. There is no boolean, no
environment variable, and no module-level mutable flag that can substitute for
the capability.

What this module deliberately does NOT do
-----------------------------------------
- It never invokes a model.
- It never creates, repairs, normalizes, or rewrites authorization artifacts.
- It never writes to the target repository.
- It never mutates either checkout.
- It never authorizes a run by itself: with no real authorization record, no
  real owner approval, and no finalized execution pin, every call fails.

Implementing this consumer does not authorize Stage 1. The package remains
``PREPARED_NOT_RUN`` / ``NOT_AUTHORIZED`` / ``package_runnable: false``.

Console output is ASCII-only (this codebase runs on Windows/cp1252).
"""

from __future__ import annotations

import hashlib
import hmac
import os
import re
import secrets
import subprocess
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

try:  # pragma: no cover - exercised implicitly by every test
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


# ============================================================================
# Deterministic failure codes
# ============================================================================
#
# Independent failures get independent codes. A generic UNAUTHORIZED would
# destroy the audit value of a failed preflight: the whole point of Gate A is
# to say precisely which authority was missing or wrong.

GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED = "GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED"
GATE_A_AUTHORIZATION_RECORD_MISSING = "GATE_A_AUTHORIZATION_RECORD_MISSING"
GATE_A_AUTHORIZATION_RECORD_INVALID = "GATE_A_AUTHORIZATION_RECORD_INVALID"
GATE_A_AUTHORIZATION_RECORD_SCHEMA_UNSUPPORTED = "GATE_A_AUTHORIZATION_RECORD_SCHEMA_UNSUPPORTED"
GATE_A_AUTHORIZATION_RECORD_DUPLICATE = "GATE_A_AUTHORIZATION_RECORD_DUPLICATE"
GATE_A_AUTHORIZATION_DIGEST_MISSING = "GATE_A_AUTHORIZATION_DIGEST_MISSING"
GATE_A_AUTHORIZATION_DIGEST_INVALID = "GATE_A_AUTHORIZATION_DIGEST_INVALID"
GATE_A_AUTHORIZATION_DIGEST_MISMATCH = "GATE_A_AUTHORIZATION_DIGEST_MISMATCH"
GATE_A_OWNER_APPROVAL_MISSING = "GATE_A_OWNER_APPROVAL_MISSING"
GATE_A_OWNER_APPROVAL_INVALID = "GATE_A_OWNER_APPROVAL_INVALID"
GATE_A_OWNER_APPROVAL_DIGEST_MISMATCH = "GATE_A_OWNER_APPROVAL_DIGEST_MISMATCH"
GATE_A_OWNER_APPROVAL_CONFLICT = "GATE_A_OWNER_APPROVAL_CONFLICT"
GATE_A_OWNER_IDENTITY_MISMATCH = "GATE_A_OWNER_IDENTITY_MISMATCH"
GATE_A_OPERATOR_SELF_APPROVAL_PROHIBITED = "GATE_A_OPERATOR_SELF_APPROVAL_PROHIBITED"
GATE_A_EXECUTION_FRAMEWORK_SHA_PENDING = "GATE_A_EXECUTION_FRAMEWORK_SHA_PENDING"
GATE_A_EXECUTION_FRAMEWORK_SHA_MISMATCH = "GATE_A_EXECUTION_FRAMEWORK_SHA_MISMATCH"
GATE_A_TARGET_SHA_MISMATCH = "GATE_A_TARGET_SHA_MISMATCH"
GATE_A_TARGET_REPOSITORY_MISMATCH = "GATE_A_TARGET_REPOSITORY_MISMATCH"
GATE_A_RUN_CONTROL_COMMIT_MISMATCH = "GATE_A_RUN_CONTROL_COMMIT_MISMATCH"
GATE_A_FLOATING_REF_PROHIBITED = "GATE_A_FLOATING_REF_PROHIBITED"
GATE_A_REQUIRED_PATH_MISSING = "GATE_A_REQUIRED_PATH_MISSING"
GATE_A_PACKAGE_PATH_MISMATCH = "GATE_A_PACKAGE_PATH_MISMATCH"
GATE_A_PACKAGE_DIGEST_MISMATCH = "GATE_A_PACKAGE_DIGEST_MISMATCH"
GATE_A_CHECKLIST_PATH_MISMATCH = "GATE_A_CHECKLIST_PATH_MISMATCH"
GATE_A_CHECKLIST_DIGEST_MISMATCH = "GATE_A_CHECKLIST_DIGEST_MISMATCH"
GATE_A_MODEL_MISMATCH = "GATE_A_MODEL_MISMATCH"
GATE_A_ARTIFACT_TYPE_MISMATCH = "GATE_A_ARTIFACT_TYPE_MISMATCH"
GATE_A_EVIDENCE_IDENTITY_MISMATCH = "GATE_A_EVIDENCE_IDENTITY_MISMATCH"
GATE_A_INVOCATION_LIMIT_INVALID = "GATE_A_INVOCATION_LIMIT_INVALID"
GATE_A_FALLBACK_PROHIBITED = "GATE_A_FALLBACK_PROHIBITED"
GATE_A_RETRY_PROHIBITED = "GATE_A_RETRY_PROHIBITED"
GATE_A_MODEL_SUBSTITUTION_PROHIBITED = "GATE_A_MODEL_SUBSTITUTION_PROHIBITED"
GATE_A_ARTIFACT_REPAIR_PROHIBITED = "GATE_A_ARTIFACT_REPAIR_PROHIBITED"
GATE_A_TARGET_MUTATION_PROHIBITED = "GATE_A_TARGET_MUTATION_PROHIBITED"
GATE_A_AUTHORIZATION_STATUS_INVALID = "GATE_A_AUTHORIZATION_STATUS_INVALID"
GATE_A_AUTHORIZATION_EXPIRED = "GATE_A_AUTHORIZATION_EXPIRED"
GATE_A_ROOT_SEPARATION_FAILURE = "GATE_A_ROOT_SEPARATION_FAILURE"
GATE_A_PATH_ESCAPE_PROHIBITED = "GATE_A_PATH_ESCAPE_PROHIBITED"
GATE_A_SYMLINK_PROHIBITED = "GATE_A_SYMLINK_PROHIBITED"
GATE_A_FILESYSTEM_ERROR = "GATE_A_FILESYSTEM_ERROR"
GATE_A_EVIDENCE_OUTPUT_ALREADY_PRESENT = "GATE_A_EVIDENCE_OUTPUT_ALREADY_PRESENT"
GATE_A_CAPABILITY_ALREADY_CONSUMED = "GATE_A_CAPABILITY_ALREADY_CONSUMED"
GATE_A_CAPABILITY_CONTEXT_MISMATCH = "GATE_A_CAPABILITY_CONTEXT_MISMATCH"
GATE_A_REVALIDATION_FAILED = "GATE_A_REVALIDATION_FAILED"

# --- Remediation codes (issue #108 independent review) -----------------------
# Added after an independent review reproduced three authorization bypasses in
# the first design: a caller-controlled opt-out flag, capability cloning via
# copy/deepcopy/pickle, and a check-then-set race in consume().
GATE_A_INVOCATION_CLASSIFICATION_AMBIGUOUS = "GATE_A_INVOCATION_CLASSIFICATION_AMBIGUOUS"
GATE_A_INVOCATION_IDENTITY_MISMATCH = "GATE_A_INVOCATION_IDENTITY_MISMATCH"
GATE_A_CAPABILITY_COPY_PROHIBITED = "GATE_A_CAPABILITY_COPY_PROHIBITED"
GATE_A_CAPABILITY_SERIALIZATION_PROHIBITED = "GATE_A_CAPABILITY_SERIALIZATION_PROHIBITED"
GATE_A_CAPABILITY_NOT_LIVE = "GATE_A_CAPABILITY_NOT_LIVE"
GATE_A_CAPABILITY_CONCURRENT_CONSUMPTION = "GATE_A_CAPABILITY_CONCURRENT_CONSUMPTION"
GATE_A_CAPABILITY_CONSUMPTION_FAILED = "GATE_A_CAPABILITY_CONSUMPTION_FAILED"
GATE_A_CAPABILITY_IMMUTABLE = "GATE_A_CAPABILITY_IMMUTABLE"

ALL_FAILURE_CODES = tuple(
    sorted(
        name
        for name in list(globals())
        if name.startswith("GATE_A_") and name != "GATE_A_AUTHORIZATION_CONSUMER_NOT_IMPLEMENTED"
    )
)


# ============================================================================
# Contract constants (from the merged preparation package, section 2c/2g)
# ============================================================================

CONTRACT_SCHEMA_VERSION = "1"
CONTRACT_AUTHORIZATION_STATUS = "AUTHORIZED_FOR_ONE_CONTROLLED_INVOCATION"
CONTRACT_EVIDENCE_NUMBER = "0016"
CONTRACT_EVIDENCE_SLUG = "0016-stage1-auteur-post-remediation-controlled-attempt"
CONTRACT_EXACT_MODEL = "claude-sonnet-5"
CONTRACT_ARTIFACT_TYPE = "repository_sensemaking_brief"
CONTRACT_TARGET_REPOSITORY = "https://github.com/ThorStarlord/auteur.git"
CONTRACT_INVOCATION_LIMIT = 1

CONTRACT_RUN_CONTROL_DIR = (
    "experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt"
)
CONTRACT_RECORD_FILENAME = "authorization-record.yaml"
CONTRACT_DIGEST_FILENAME = "authorization-record.sha256"
CONTRACT_APPROVAL_FILENAME = "owner-approval.md"

CONTRACT_PACKAGE_PATH = "docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md"
CONTRACT_CHECKLIST_PATH = "docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md"

# Authoring identity is NOT approving authority. Only these identities may
# approve, per section 2e (repository owner, or an explicitly delegated
# campaign owner named by the owner).
CONTRACT_APPROVING_AUTHORITIES = ("ThorStarlord",)

# The 24-field record schema of section 2g.
REQUIRED_RECORD_FIELDS = (
    "schema_version",
    "authorization_status",
    "authorization_scope",
    "evidence_number",
    "evidence_slug",
    "execution_framework_sha",
    "target_repository",
    "target_sha",
    "exact_model",
    "artifact_type",
    "preparation_package_path",
    "preparation_package_sha256",
    "gate_d_checklist_path",
    "gate_d_checklist_sha256",
    "authorization_record_created_at",
    "authorization_record_created_by",
    "owner_approval_reference",
    "one_invocation_only",
    "no_retry",
    "no_fallback",
    "no_model_substitution",
    "no_artifact_repair",
    "no_target_mutation",
    "stop_on_first_failed_gate",
)

REQUIRED_SAFETY_BOOLEANS = (
    "one_invocation_only",
    "no_retry",
    "no_fallback",
    "no_model_substitution",
    "no_artifact_repair",
    "no_target_mutation",
    "stop_on_first_failed_gate",
)

REQUIRED_APPROVAL_FIELDS = (
    "approver_github_identity",
    "approval_timestamp",
    "authorization_record_sha256",
    "execution_framework_sha",
    "target_sha",
    "evidence_number",
    "evidence_slug",
    "exact_model",
    "authorization_decision",
    "no_retry_statement",
    "owner_decision_reference",
)

# Sentinels the merged preparation package uses to mark values that do not
# exist yet. They are never valid authoritative values.
SENTINEL_VALUES = frozenset(
    {
        "PENDING_POST_MERGE_PIN_FINALIZATION",
        "PENDING_AUTHORIZATION_RECORD_CREATION",
        "PENDING_OWNER_APPROVAL",
        "TBD",
        "TODO",
        "PENDING",
        "NONE",
        "N/A",
        "XXX",
        "CHANGEME",
        "PLACEHOLDER",
    }
)

FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EVIDENCE_NUMBER_RE = re.compile(r"^[0-9]{4}$")

# Anything that is not a full 40-hex SHA but looks like a git revision the
# resolver would follow at execution time is a floating ref.
FLOATING_REF_TOKENS = (
    "HEAD",
    "main",
    "master",
    "origin/",
    "refs/",
    "@{",
    "latest",
    "develop",
)


class GateAError(Exception):
    """Raised when a caller misuses the consumer API itself."""


# ============================================================================
# Typed interface
# ============================================================================


@dataclass(frozen=True)
class AuthorizationContext:
    """Immutable, fully-resolved inputs to a Gate A decision.

    Every value is a resolved absolute path or a full 40-character SHA. No
    floating ref is accepted, because a ref resolved at execution time is a
    different value from the one the owner approved.
    """

    framework_root: Path
    target_root: Path
    execution_framework_sha: str
    target_sha: str
    evidence_number: str
    evidence_slug: str
    exact_model: str
    artifact_type: str
    invocation_limit: int
    authorization_record_path: Path
    authorization_digest_path: Path
    owner_approval_path: Path
    run_control_commit_sha: str
    operator_identity: Optional[str] = None
    expected_target_repository: str = CONTRACT_TARGET_REPOSITORY
    required_framework_paths: tuple = (CONTRACT_PACKAGE_PATH, CONTRACT_CHECKLIST_PATH)
    required_target_paths: tuple = ()
    evidence_output_dir: Optional[Path] = None


@dataclass(frozen=True)
class AuthorizationDecision:
    """The typed result of a Gate A evaluation.

    ``authorized`` is only ever True when every check passed. ``failure_code``
    is a stable, specific code from this module -- never a generic
    ``UNAUTHORIZED``.
    """

    authorized: bool
    failure_code: Optional[str] = None
    failure_detail: str = ""
    validated_record_sha256: Optional[str] = None
    validated_owner_identity: Optional[str] = None
    validated_framework_sha: Optional[str] = None
    validated_target_sha: Optional[str] = None
    validated_run_control_commit_sha: Optional[str] = None
    validated_model: Optional[str] = None
    validated_invocation_limit: Optional[int] = None
    checks_passed: tuple = ()

    def to_log_dict(self) -> dict:
        """Log-safe projection.

        Emits the decision, the failure code, digests, and revisions. Never
        emits record bodies, approval prose, tokens, or credentials.
        """
        return {
            "gate": "A",
            "authorized": self.authorized,
            "failure_code": self.failure_code,
            "failure_detail": self.failure_detail,
            "evidence_number": CONTRACT_EVIDENCE_NUMBER,
            "authorization_record_sha256": self.validated_record_sha256,
            "owner_identity": self.validated_owner_identity,
            "framework_sha": self.validated_framework_sha,
            "target_sha": self.validated_target_sha,
            "run_control_commit_sha": self.validated_run_control_commit_sha,
            "model": self.validated_model,
            "invocation_limit": self.validated_invocation_limit,
            "checks_passed": list(self.checks_passed),
        }


@dataclass
class _ValidatedSnapshot:
    """Byte-level and revision-level snapshot taken at validation time.

    This is the anchor for TOCTOU resistance: the capability revalidates
    against exactly these digests immediately before the provider call.
    """

    record_sha256: str
    digest_file_sha256: str
    approval_sha256: str
    package_sha256: str
    checklist_sha256: str
    framework_head: str
    target_head: str


# ============================================================================
# Immutable invocation identity
# ============================================================================
#
# The security decision "is this a controlled Stage 1 invocation?" must not be
# a caller-supplied boolean. It is derived from *what is actually being
# invoked*: the workflow stage, the artifact type, the evidence namespace the
# output lands in, the pinned target, and the exact model. Those values are
# captured here in a frozen object, bound into the capability at issuance, and
# re-checked at consumption.


@dataclass(frozen=True)
class InvocationIdentity:
    """What is actually being invoked. Immutable, hashable, digestible.

    Every field is a plain string (paths are normalized to POSIX-style strings)
    so the digest is stable across platforms and across process boundaries.
    Construct with :meth:`build`, which does the normalization.
    """

    workflow_id: str
    workflow_stage: str
    artifact_type: str
    evidence_number: Optional[str]
    evidence_slug: Optional[str]
    output_path: str
    framework_root: str
    target_root: str
    target_repository: str
    target_sha: str
    requested_model: str
    executor_id: str
    invocation_limit: int = 1
    execution_framework_sha: Optional[str] = None
    #: Informational only. Recorded for the audit log and for conflict
    #: detection. It is NEVER sufficient to make Gate A optional -- see
    #: ``classify_invocation``.
    declared_controlled_mode: Optional[bool] = None

    @staticmethod
    def _norm_path(value) -> str:
        if value is None:
            return ""
        return str(value).replace("\\", "/").rstrip("/")

    @classmethod
    def build(cls, *, workflow_id="", workflow_stage="", artifact_type="",
              evidence_number=None, evidence_slug=None, output_path="",
              framework_root="", target_root="", target_repository="",
              target_sha="", requested_model="", executor_id="",
              invocation_limit=1, execution_framework_sha=None,
              declared_controlled_mode=None) -> "InvocationIdentity":
        return cls(
            workflow_id=str(workflow_id or ""),
            workflow_stage=str(workflow_stage or ""),
            artifact_type=str(artifact_type or ""),
            evidence_number=(str(evidence_number) if evidence_number else None),
            evidence_slug=(str(evidence_slug) if evidence_slug else None),
            output_path=cls._norm_path(output_path),
            framework_root=cls._norm_path(framework_root),
            target_root=cls._norm_path(target_root),
            target_repository=str(target_repository or ""),
            target_sha=str(target_sha or ""),
            requested_model=str(requested_model or ""),
            executor_id=str(executor_id or ""),
            invocation_limit=int(invocation_limit),
            execution_framework_sha=(str(execution_framework_sha)
                                     if execution_framework_sha else None),
            declared_controlled_mode=(None if declared_controlled_mode is None
                                      else bool(declared_controlled_mode)),
        )

    def digest(self) -> str:
        """Deterministic digest over every field except the informational flag.

        ``declared_controlled_mode`` is excluded on purpose: it is metadata,
        not identity. Two invocations that differ only in that flag are the
        SAME invocation and must not be able to obtain different treatment by
        binding to different capabilities.
        """
        payload = "\x1f".join(
            (
                self.workflow_id, self.workflow_stage, self.artifact_type,
                self.evidence_number or "", self.evidence_slug or "",
                self.output_path, self.framework_root, self.target_root,
                self.target_repository, self.target_sha, self.requested_model,
                self.executor_id, str(self.invocation_limit),
                self.execution_framework_sha or "",
            )
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class ExecutionMode(Enum):
    """Typed classification of an invocation. Not a boolean."""

    ORDINARY_DEVELOPMENT = "ORDINARY_DEVELOPMENT"
    CONTROLLED_STAGE1 = "CONTROLLED_STAGE1"
    AMBIGUOUS = "AMBIGUOUS"


#: Any output landing under one of these path segments is inside a controlled
#: evidence namespace, regardless of what mode the caller declared.
CONTROLLED_NAMESPACE_SEGMENTS = ("experiments/evidence/", "experiments/run-control/")

#: Skills / workflow stages that constitute Stage 1 repository sensemaking.
STAGE_1_STAGE_TOKENS = ("stage-1", "stage1", "stage_1", "1")
STAGE_1_SKILL_IDS = ("repo-sensemaker",)

_EVIDENCE_PATH_RE = re.compile(
    r"experiments/(?:evidence|run-control)/(\d{4})-([A-Za-z0-9._-]+)"
)


def _is_stage_1(identity: "InvocationIdentity") -> bool:
    stage = identity.workflow_stage.strip().lower()
    if stage in STAGE_1_STAGE_TOKENS:
        return True
    wid = identity.workflow_id.strip().lower()
    return any(tok in wid for tok in ("stage-1", "stage1")) or wid in STAGE_1_SKILL_IDS


def _in_controlled_namespace(identity: "InvocationIdentity") -> bool:
    out = identity.output_path.lower()
    return any(seg in out for seg in CONTROLLED_NAMESPACE_SEGMENTS)


def classify_invocation(identity: Optional["InvocationIdentity"]
                        ) -> tuple[ExecutionMode, tuple[str, ...]]:
    """Derive the execution mode from immutable invocation properties.

    Returns ``(mode, signals)`` where ``signals`` names every structural
    controlled-Stage-1 signal that fired. Fails closed: anything that looks
    partially like the controlled campaign is AMBIGUOUS, and AMBIGUOUS
    requires Gate A exactly as CONTROLLED_STAGE1 does.

    The ordinary-development boundary is deliberately narrow and structural:
    an invocation is ordinary only when it lands OUTSIDE every controlled
    evidence namespace, does NOT name the campaign evidence number or slug,
    does NOT target the pinned campaign repository, does NOT request the exact
    campaign model, and does NOT declare controlled mode. Running
    repo-sensemaker locally into ``artifacts/`` therefore stays ungated;
    running it into ``experiments/evidence/`` never does.
    """
    if identity is None:
        # No identity at all at a provider boundary is not "ordinary" -- it is
        # an absence of the evidence needed to say so.
        return ExecutionMode.AMBIGUOUS, ("identity_missing",)

    signals: list[str] = []
    if identity.artifact_type == CONTRACT_ARTIFACT_TYPE:
        signals.append("artifact_type_is_stage1_brief")
    stage_1 = _is_stage_1(identity)
    if stage_1:
        signals.append("workflow_stage_is_stage_1")
    if identity.evidence_number == CONTRACT_EVIDENCE_NUMBER:
        signals.append("evidence_number_is_campaign")
    if identity.evidence_slug == CONTRACT_EVIDENCE_SLUG:
        signals.append("evidence_slug_is_campaign")
    ns = _in_controlled_namespace(identity)
    if ns:
        signals.append("output_in_controlled_evidence_namespace")
    if identity.evidence_number or identity.evidence_slug:
        signals.append("evidence_identity_present")
    if identity.target_repository == CONTRACT_TARGET_REPOSITORY:
        signals.append("target_repository_is_campaign_pin")
    if identity.requested_model == CONTRACT_EXACT_MODEL:
        signals.append("requested_model_is_campaign_model")
    if identity.declared_controlled_mode is True:
        signals.append("declared_controlled_mode")

    frozen_signals = tuple(signals)

    strong = (
        "evidence_number_is_campaign" in signals
        or "evidence_slug_is_campaign" in signals
        or "output_in_controlled_evidence_namespace" in signals
        or "evidence_identity_present" in signals
    )
    weak = (
        "target_repository_is_campaign_pin" in signals
        or "requested_model_is_campaign_model" in signals
    )
    brief = "artifact_type_is_stage1_brief" in signals

    # A caller who declares controlled mode gets controlled mode. A caller who
    # declares NOT-controlled while structural signals say otherwise gets
    # AMBIGUOUS -- never ordinary. `False` can never override structure.
    if identity.declared_controlled_mode is True:
        return ExecutionMode.CONTROLLED_STAGE1, frozen_signals
    if identity.declared_controlled_mode is False and (strong or weak):
        return ExecutionMode.AMBIGUOUS, frozen_signals + ("declared_mode_conflict",)

    if strong and brief:
        return ExecutionMode.CONTROLLED_STAGE1, frozen_signals
    if strong:
        return ExecutionMode.AMBIGUOUS, frozen_signals
    if weak and brief and stage_1:
        return ExecutionMode.CONTROLLED_STAGE1, frozen_signals
    if weak and (brief or stage_1):
        return ExecutionMode.AMBIGUOUS, frozen_signals
    return ExecutionMode.ORDINARY_DEVELOPMENT, frozen_signals


def requires_gate_a(mode: ExecutionMode) -> bool:
    """Gate A is mandatory for controlled Stage 1 AND for ambiguity."""
    return mode is not ExecutionMode.ORDINARY_DEVELOPMENT


# ============================================================================
# Issuer-backed capability registry
# ============================================================================
#
# The capability OBJECT is not authorization. The authorization lives in this
# process-local registry, keyed by a cryptographically random capability ID.
# A copied, pickled, reconstructed, or hand-built object either carries no ID
# that the registry knows, or carries an ID that maps to the SAME single
# registry entry -- so duplicates compete for one atomic consumption and at
# most one wins. Python attribute privacy is NOT the security boundary.

_CAPABILITY_STATE_ISSUED = "ISSUED"
_CAPABILITY_STATE_CONSUMING = "CONSUMING"
_CAPABILITY_STATE_CONSUMED = "CONSUMED"
_CAPABILITY_STATE_FAILED = "FAILED"


class _CapabilityEntry:
    """Registry-side authoritative state. Never handed to callers."""

    __slots__ = ("capability_id", "decision", "context", "snapshot", "identity",
                 "identity_digest", "state", "issued_at", "remaining")

    def __init__(self, capability_id, decision, context, snapshot, identity):
        self.capability_id = capability_id
        self.decision = decision
        self.context = context
        self.snapshot = snapshot
        self.identity = identity
        self.identity_digest = identity.digest() if identity is not None else None
        self.state = _CAPABILITY_STATE_ISSUED
        self.issued_at = datetime.now(timezone.utc)
        self.remaining = int(context.invocation_limit)


class _CapabilityRegistry:
    """Process-local, lock-protected issuance ledger."""

    def __init__(self):
        self._lock = threading.Lock()
        self._entries: dict = {}

    # -- issuance -----------------------------------------------------------

    def issue(self, decision, context, snapshot, identity) -> "AuthorizedInvocation":
        capability_id = secrets.token_hex(32)
        entry = _CapabilityEntry(capability_id, decision, context, snapshot, identity)
        with self._lock:
            self._entries[capability_id] = entry
        return AuthorizedInvocation(_CAPABILITY_TOKEN, capability_id)

    # -- read (non-authoritative; never used to decide) ---------------------

    def peek(self, capability_id):
        with self._lock:
            return self._entries.get(capability_id)

    def is_live(self, capability_id) -> bool:
        with self._lock:
            entry = self._entries.get(capability_id)
            return entry is not None and entry.state == _CAPABILITY_STATE_ISSUED

    def live_count(self) -> int:
        with self._lock:
            return sum(1 for e in self._entries.values()
                       if e.state == _CAPABILITY_STATE_ISSUED)

    # -- atomic consumption -------------------------------------------------

    def begin_consumption(self, capability_id) -> _CapabilityEntry:
        """ISSUED -> CONSUMING, atomically. At most one caller can win.

        The transition happens BEFORE any expensive revalidation, so the race
        window is the width of a dict lookup under a lock, not the width of
        five file hashes and two git invocations.
        """
        with self._lock:
            entry = self._entries.get(capability_id)
            if entry is None:
                raise GateAError(
                    f"{GATE_A_CAPABILITY_NOT_LIVE}: no live issuance exists for "
                    f"this capability. It was never issued by this process, or "
                    f"it is a copy/reconstruction of one that was."
                )
            if entry.state == _CAPABILITY_STATE_CONSUMING:
                raise GateAError(
                    f"{GATE_A_CAPABILITY_CONCURRENT_CONSUMPTION}: another caller "
                    f"is already consuming this authorization. Exactly one "
                    f"invocation is permitted."
                )
            if entry.state == _CAPABILITY_STATE_CONSUMED:
                raise GateAError(
                    f"{GATE_A_CAPABILITY_ALREADY_CONSUMED}: this authorization "
                    f"permits exactly {entry.context.invocation_limit} invocation "
                    f"and has already been spent. No retry, no rerun, no repair."
                )
            if entry.state == _CAPABILITY_STATE_FAILED:
                raise GateAError(
                    f"{GATE_A_CAPABILITY_CONSUMPTION_FAILED}: a previous "
                    f"consumption attempt burned this authorization. This "
                    f"campaign permits no retry."
                )
            if entry.remaining <= 0:
                raise GateAError(
                    f"{GATE_A_CAPABILITY_ALREADY_CONSUMED}: no invocations remain."
                )
            entry.state = _CAPABILITY_STATE_CONSUMING
            return entry

    def fail_consumption(self, capability_id) -> None:
        """Burn the capability. It never returns to ISSUED."""
        with self._lock:
            entry = self._entries.get(capability_id)
            if entry is not None and entry.state == _CAPABILITY_STATE_CONSUMING:
                entry.state = _CAPABILITY_STATE_FAILED
                entry.remaining = 0

    def complete_consumption(self, capability_id) -> None:
        with self._lock:
            entry = self._entries.get(capability_id)
            if entry is None or entry.state != _CAPABILITY_STATE_CONSUMING:
                raise GateAError(
                    f"{GATE_A_CAPABILITY_CONSUMPTION_FAILED}: capability state "
                    f"changed underneath an in-flight consumption."
                )
            entry.state = _CAPABILITY_STATE_CONSUMED
            entry.remaining = 0


_REGISTRY = _CapabilityRegistry()


class AuthorizedInvocation:
    """Opaque handle to a single live issuance in the capability registry.

    The object holds ONE thing: a cryptographically random capability ID. It
    carries no authorization of its own. Every question ("is this authorized?",
    "may this be consumed?") is answered by the registry, live, under a lock.

    Consequences that matter:

    - A copy, deepcopy, pickle, or hand-reconstruction of this object cannot
      create a second authorization. Copying is explicitly refused; and even if
      an attacker rebuilds an object carrying the same ID by reflection, that
      object points at the SAME registry entry, which permits exactly one
      atomic consumption.
    - A forged ID is simply absent from the registry
      (``GATE_A_CAPABILITY_NOT_LIVE``).
    - The object is immutable: attribute assignment and deletion are refused,
      and ``__slots__`` prevents adding new state.
    """

    __slots__ = ("_capability_id",)

    def __init_subclass__(cls, **kwargs):  # pragma: no cover - defensive
        raise TypeError(
            f"{GATE_A_CAPABILITY_COPY_PROHIBITED}: AuthorizedInvocation may not "
            f"be subclassed; a subclass would be a second capability type."
        )

    def __init__(self, token, capability_id: str):
        if token is not _CAPABILITY_TOKEN:
            raise GateAError(
                "AuthorizedInvocation cannot be constructed directly. It is "
                "minted only by authorize_invocation() after a successful "
                "Gate A evaluation. Note that constructing one is not the "
                "security boundary -- the issuer registry is."
            )
        object.__setattr__(self, "_capability_id", capability_id)

    # -- immutability --------------------------------------------------------

    def __setattr__(self, name, value):
        raise AttributeError(
            f"{GATE_A_CAPABILITY_IMMUTABLE}: AuthorizedInvocation is immutable; "
            f"refusing to set {name!r}."
        )

    def __delattr__(self, name):
        raise AttributeError(
            f"{GATE_A_CAPABILITY_IMMUTABLE}: AuthorizedInvocation is immutable; "
            f"refusing to delete {name!r}."
        )

    # -- duplication prohibitions -------------------------------------------

    def __copy__(self):
        raise TypeError(
            f"{GATE_A_CAPABILITY_COPY_PROHIBITED}: an authorization capability "
            f"may not be copied."
        )

    def __deepcopy__(self, memo):
        raise TypeError(
            f"{GATE_A_CAPABILITY_COPY_PROHIBITED}: an authorization capability "
            f"may not be deep-copied."
        )

    def __reduce__(self):
        raise TypeError(
            f"{GATE_A_CAPABILITY_SERIALIZATION_PROHIBITED}: an authorization "
            f"capability may not be serialized."
        )

    def __reduce_ex__(self, protocol):
        raise TypeError(
            f"{GATE_A_CAPABILITY_SERIALIZATION_PROHIBITED}: an authorization "
            f"capability may not be serialized (protocol {protocol})."
        )

    def __getstate__(self):
        raise TypeError(
            f"{GATE_A_CAPABILITY_SERIALIZATION_PROHIBITED}: an authorization "
            f"capability exposes no serializable state."
        )

    def __setstate__(self, state):
        raise TypeError(
            f"{GATE_A_CAPABILITY_SERIALIZATION_PROHIBITED}: an authorization "
            f"capability cannot be reconstructed from state."
        )

    def __repr__(self):
        return f"<AuthorizedInvocation live={self.live}>"

    # -- registry-backed accessors ------------------------------------------

    @property
    def capability_id(self) -> str:
        """Opaque handle. Knowing it is useless without a live registry entry."""
        return object.__getattribute__(self, "_capability_id")

    def _live_entry(self) -> _CapabilityEntry:
        entry = _REGISTRY.peek(self.capability_id)
        if entry is None:
            raise GateAError(
                f"{GATE_A_CAPABILITY_NOT_LIVE}: this capability has no issuance "
                f"record. It was not minted by authorize_invocation()."
            )
        return entry

    @property
    def live(self) -> bool:
        return _REGISTRY.is_live(self.capability_id)

    @property
    def decision(self) -> AuthorizationDecision:
        return self._live_entry().decision

    @property
    def identity(self) -> Optional[InvocationIdentity]:
        return self._live_entry().identity

    @property
    def model(self) -> str:
        """The exact authorized model. Passed to the provider unchanged."""
        return self._live_entry().context.exact_model

    @property
    def evidence_number(self) -> str:
        return self._live_entry().context.evidence_number

    @property
    def artifact_type(self) -> str:
        return self._live_entry().context.artifact_type

    @property
    def consumed(self) -> bool:
        return self._live_entry().state != _CAPABILITY_STATE_ISSUED

    @property
    def remaining_invocations(self) -> int:
        return self._live_entry().remaining

    # -- fail-closed guarantees ---------------------------------------------

    def revalidate(self, git_head: Optional[Callable[[Path], str]] = None
                   ) -> AuthorizationDecision:
        """Re-read every authoritative byte and revision and compare to the
        snapshot taken at validation time.

        This is the TOCTOU boundary. It runs immediately before the provider
        call, inside the invocation function -- not in the caller -- so a
        change made between preflight and invocation fails closed.
        """
        entry = self._live_entry()
        return _revalidate_entry(entry, git_head)

    def consume(self, *, model: str, artifact_type: str,
                git_head: Optional[Callable[[Path], str]] = None,
                actual_identity: Optional[InvocationIdentity] = None,
                _before_revalidation: Optional[Callable[[], None]] = None,
                ) -> AuthorizationDecision:
        """Atomically spend the single issuance backing this capability.

        Sequence (see ADR 0022): take the registry lock, verify the issuance is
        ISSUED, move it to CONSUMING, release. Only then perform identity
        comparison and byte/revision revalidation. Any failure moves the
        issuance to FAILED -- it never returns to ISSUED. Once a consumption
        attempt begins, the capability is irreversibly spent; this campaign
        permits no retry.

        ``_before_revalidation`` is a test-only hook for deterministic race
        construction. It has no effect on the security decision.
        """
        capability_id = self.capability_id
        entry = _REGISTRY.begin_consumption(capability_id)
        try:
            if _before_revalidation is not None:
                _before_revalidation()

            if model != entry.context.exact_model:
                raise GateAError(
                    f"{GATE_A_MODEL_MISMATCH}: capability authorizes model "
                    f"'{entry.context.exact_model}', invocation requested "
                    f"'{model}'."
                )
            if artifact_type != entry.context.artifact_type:
                raise GateAError(
                    f"{GATE_A_CAPABILITY_CONTEXT_MISMATCH}: capability authorizes "
                    f"artifact type '{entry.context.artifact_type}', invocation "
                    f"requested '{artifact_type}'."
                )
            if actual_identity is not None:
                if entry.identity_digest is None:
                    raise GateAError(
                        f"{GATE_A_INVOCATION_IDENTITY_MISMATCH}: capability was "
                        f"issued without a bound invocation identity."
                    )
                if not _digests_equal(actual_identity.digest(), entry.identity_digest):
                    raise GateAError(
                        f"{GATE_A_INVOCATION_IDENTITY_MISMATCH}: the invocation "
                        f"being performed is not the invocation that was "
                        f"authorized."
                    )

            revalidated = _revalidate_entry(entry, git_head)
            if not revalidated.authorized:
                raise GateAError(
                    f"{revalidated.failure_code}: {revalidated.failure_detail}"
                )
        except BaseException:
            # Includes GeneratorExit/CancelledError/KeyboardInterrupt: a
            # cancelled or interrupted consumption burns the capability.
            _REGISTRY.fail_consumption(capability_id)
            raise

        _REGISTRY.complete_consumption(capability_id)
        return revalidated


def _revalidate_entry(entry: _CapabilityEntry,
                      git_head: Optional[Callable[[Path], str]] = None
                      ) -> AuthorizationDecision:
    head_fn = git_head or read_git_head
    ctx = entry.context
    snapshot = entry.snapshot
    try:
        checks = (
            ("record", ctx.authorization_record_path, snapshot.record_sha256),
            ("digest", ctx.authorization_digest_path, snapshot.digest_file_sha256),
            ("approval", ctx.owner_approval_path, snapshot.approval_sha256),
            ("package", ctx.framework_root / CONTRACT_PACKAGE_PATH,
             snapshot.package_sha256),
            ("checklist", ctx.framework_root / CONTRACT_CHECKLIST_PATH,
             snapshot.checklist_sha256),
        )
        for label, path, expected in checks:
            current = sha256_file(path)
            if current is None:
                return _fail(
                    GATE_A_REVALIDATION_FAILED,
                    f"{label} disappeared between validation and invocation",
                )
            if not _digests_equal(current, expected):
                return _fail(
                    GATE_A_REVALIDATION_FAILED,
                    f"{label} bytes changed between validation and invocation",
                )

        framework_head = head_fn(ctx.framework_root)
        if framework_head != snapshot.framework_head:
            return _fail(
                GATE_A_REVALIDATION_FAILED,
                "framework HEAD moved between validation and invocation",
            )
        target_head = head_fn(ctx.target_root)
        if target_head != snapshot.target_head:
            return _fail(
                GATE_A_REVALIDATION_FAILED,
                "target HEAD moved between validation and invocation",
            )
    except OSError as exc:
        return _fail(GATE_A_FILESYSTEM_ERROR, f"revalidation IO failure: {exc.strerror}")
    return entry.decision


_CAPABILITY_TOKEN = object()


def _fail(code: str, detail: str = "") -> AuthorizationDecision:
    return AuthorizationDecision(authorized=False, failure_code=code, failure_detail=detail)


# ============================================================================
# Canonical byte hashing
# ============================================================================


def sha256_bytes(data: bytes) -> str:
    """SHA-256 of exact bytes, lowercase hex."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> Optional[str]:
    """SHA-256 over the exact bytes on disk.

    Deliberately reads in binary and hashes what is there. It does NOT parse
    and reserialize YAML, normalize line endings, strip whitespace, or
    reconstruct a dictionary -- a CRLF/LF change or a trailing space is a
    different authorization record and must fail.
    """
    try:
        with open(path, "rb") as fh:
            return sha256_bytes(fh.read())
    except (OSError, ValueError):
        return None


def _digests_equal(a: str, b: str) -> bool:
    """Constant-time digest comparison."""
    return hmac.compare_digest(a.encode("ascii", "ignore"), b.encode("ascii", "ignore"))


def parse_digest_file(raw: bytes) -> tuple[Optional[str], Optional[str]]:
    """Parse an externally stored SHA-256 file.

    Accepts exactly one digest, optionally in ``<digest>  <filename>`` form
    with the contract filename. Returns ``(digest, None)`` or
    ``(None, failure_code)``.
    """
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, GATE_A_AUTHORIZATION_DIGEST_INVALID

    lines = [ln for ln in text.splitlines() if ln.strip()]
    if len(lines) != 1:
        # Zero digests, or multiple digests -> ambiguous authority.
        return None, GATE_A_AUTHORIZATION_DIGEST_INVALID

    tokens = lines[0].split()
    if len(tokens) == 1:
        digest = tokens[0]
    elif len(tokens) == 2:
        digest, name = tokens
        # `sha256sum` writes "*name" for binary mode.
        if name.lstrip("*") != CONTRACT_RECORD_FILENAME:
            return None, GATE_A_AUTHORIZATION_DIGEST_INVALID
    else:
        return None, GATE_A_AUTHORIZATION_DIGEST_INVALID

    if not SHA256_RE.match(digest):
        # Rejects uppercase, abbreviated, and non-hex digests. The contract
        # specifies "64 lowercase hex"; normalizing case here would let an
        # approval and a record disagree on their exact approved string.
        return None, GATE_A_AUTHORIZATION_DIGEST_INVALID
    return digest, None


# ============================================================================
# Filesystem safety
# ============================================================================


def _is_within(path: Path, root: Path) -> bool:
    try:
        Path(os.path.realpath(path)).relative_to(Path(os.path.realpath(root)))
        return True
    except (ValueError, OSError):
        return False


def check_run_control_path(path: Path, run_control_root: Path) -> Optional[str]:
    """Reject symlinks and any path escaping the run-control directory."""
    try:
        if not path.exists():
            return GATE_A_REQUIRED_PATH_MISSING
        if path.is_symlink():
            return GATE_A_SYMLINK_PROHIBITED
        # Any symlinked ancestor inside the run-control root is also a redirect.
        probe = path.parent
        root_real = Path(os.path.realpath(run_control_root))
        while True:
            if probe.is_symlink():
                return GATE_A_SYMLINK_PROHIBITED
            if Path(os.path.realpath(probe)) == root_real or probe == probe.parent:
                break
            probe = probe.parent
        if not _is_within(path, run_control_root):
            return GATE_A_PATH_ESCAPE_PROHIBITED
    except OSError:
        return GATE_A_FILESYSTEM_ERROR
    return None


# ============================================================================
# Git helpers (read-only)
# ============================================================================


def read_git_head(root: Path) -> str:
    """Read HEAD of a checkout. Never mutates or cleans it."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def resolve_run_control_commit(framework_root: Path, artifact_path: Path) -> str:
    """Return the commit that last touched the run-control artifact.

    Read-only. Returns "" when it cannot be demonstrated, which the consumer
    treats as a failure (immutability unproven), never as a pass.
    """
    try:
        rel = os.path.relpath(artifact_path, framework_root).replace("\\", "/")
        out = subprocess.run(
            ["git", "-C", str(framework_root), "log", "-1", "--format=%H", "--", rel],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, ValueError, subprocess.SubprocessError):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


# ============================================================================
# Value validation helpers
# ============================================================================


def _blank(value) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def _is_sentinel(value) -> bool:
    return isinstance(value, str) and value.strip().upper() in SENTINEL_VALUES


def _is_floating_ref(value) -> bool:
    if not isinstance(value, str):
        return False
    v = value.strip()
    if FULL_SHA_RE.match(v):
        return False
    return any(tok.lower() in v.lower() for tok in FLOATING_REF_TOKENS)


if yaml is not None:

    class _StrictLoader(yaml.SafeLoader):
        """SafeLoader that refuses duplicate keys and YAML aliases.

        A duplicate key silently keeps the last value, which would let a
        record declare ``no_retry: true`` and then ``no_retry: false``. An
        alias can make an authoritative value point somewhere non-obvious.
        Both are rejected rather than resolved -- the consumer must never
        normalize an ambiguous record into a valid one.
        """

        def compose_node(self, parent, index):
            if self.check_event(yaml.events.AliasEvent):
                event = self.peek_event()
                raise yaml.constructor.ConstructorError(
                    None, None,
                    "YAML aliases are not permitted in an authorization record",
                    event.start_mark,
                )
            return super().compose_node(parent, index)

        def construct_mapping(self, node, deep=False):
            mapping = {}
            for key_node, value_node in node.value:
                key = self.construct_object(key_node, deep=deep)
                if key in mapping:
                    raise yaml.constructor.ConstructorError(
                        None, None,
                        f"duplicate key in authorization record: {key!r}",
                        key_node.start_mark,
                    )
                mapping[key] = self.construct_object(value_node, deep=deep)
            return mapping

else:  # pragma: no cover
    _StrictLoader = None  # type: ignore[assignment]


def parse_record_bytes(raw: bytes) -> tuple[Optional[dict], Optional[str], str]:
    """Parse authorization-record bytes strictly.

    Returns ``(mapping, failure_code, detail)``. Never repairs or normalizes.
    """
    if yaml is None:  # pragma: no cover
        return None, GATE_A_AUTHORIZATION_RECORD_INVALID, "pyyaml unavailable"
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, GATE_A_AUTHORIZATION_RECORD_INVALID, "record is not valid UTF-8"
    try:
        docs = list(yaml.load_all(text, Loader=_StrictLoader))
    except yaml.YAMLError as exc:
        reason = "duplicate key" if "duplicate key" in str(exc) else (
            "alias" if "alias" in str(exc) else "malformed YAML"
        )
        return None, GATE_A_AUTHORIZATION_RECORD_INVALID, reason
    if len(docs) != 1:
        return None, GATE_A_AUTHORIZATION_RECORD_DUPLICATE, (
            f"expected exactly one authorization record document, found {len(docs)}"
        )
    doc = docs[0]
    if not isinstance(doc, dict):
        return None, GATE_A_AUTHORIZATION_RECORD_INVALID, "record is not a mapping"
    return doc, None, ""


def parse_approval_bytes(raw: bytes) -> tuple[Optional[dict], Optional[str], str]:
    """Parse the owner-approval artifact.

    The approval is a markdown document carrying a ``key: value`` block. Each
    required field must appear exactly once; a second, contradictory
    declaration is a conflict, not an override.
    """
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, GATE_A_OWNER_APPROVAL_INVALID, "approval is not valid UTF-8"

    fields: dict = {}
    seen_twice: set = set()
    for line in text.splitlines():
        stripped = line.strip().lstrip("-*").strip()
        stripped = stripped.replace("**", "")
        m = re.match(r"^([a-z0-9_]+)\s*:\s*(.*)$", stripped)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip().strip("`").strip()
        if key not in REQUIRED_APPROVAL_FIELDS:
            continue
        if key in fields and fields[key] != value:
            seen_twice.add(key)
        fields.setdefault(key, value)
    if seen_twice:
        return None, GATE_A_OWNER_APPROVAL_CONFLICT, (
            f"contradictory approval fields: {sorted(seen_twice)}"
        )
    return fields, None, ""


# ============================================================================
# The consumer
# ============================================================================


def authorize(context: AuthorizationContext, *,
              git_head: Optional[Callable[[Path], str]] = None,
              run_control_commit_resolver: Optional[Callable[[Path, Path], str]] = None,
              now: Optional[datetime] = None
              ) -> tuple[AuthorizationDecision, Optional[_ValidatedSnapshot]]:
    """Evaluate Gate A. Pure read-only. Never invokes a model.

    Validation order follows section 2j of the merged preparation package:
    artifacts exist -> exact-byte digest recomputed -> owner approval binds to
    that digest -> approval identity -> status -> record fields -> revisions ->
    evidence identity -> model -> package/checklist provenance -> safety
    booleans -> no pre-existing Evidence 0016 output.

    Fails on the FIRST failing check (``stop_on_first_failed_gate``).
    """
    head_fn = git_head or read_git_head
    now = now or datetime.now(timezone.utc)
    passed: list = []

    # ---- 0. Root separation and identity ---------------------------------
    fr = Path(os.path.realpath(context.framework_root))
    tr = Path(os.path.realpath(context.target_root))
    if fr == tr or _is_within(tr, fr) or _is_within(fr, tr):
        return _fail(
            GATE_A_ROOT_SEPARATION_FAILURE,
            "framework root and target root must be separate repositories",
        ), None
    passed.append("root_separation")

    # ---- 0b. No floating refs anywhere in the pinned context -------------
    for label, value in (
        ("execution_framework_sha", context.execution_framework_sha),
        ("target_sha", context.target_sha),
        ("run_control_commit_sha", context.run_control_commit_sha),
    ):
        if _blank(value):
            return _fail(GATE_A_AUTHORIZATION_RECORD_INVALID, f"{label} is blank"), None
        if _is_sentinel(value):
            code = (GATE_A_EXECUTION_FRAMEWORK_SHA_PENDING
                    if label == "execution_framework_sha" else
                    GATE_A_RUN_CONTROL_COMMIT_MISMATCH
                    if label == "run_control_commit_sha" else
                    GATE_A_AUTHORIZATION_RECORD_INVALID)
            return _fail(code, f"{label} is still the sentinel value"), None
        if _is_floating_ref(value):
            return _fail(GATE_A_FLOATING_REF_PROHIBITED,
                         f"{label} is a floating ref, not an immutable revision"), None
        if not FULL_SHA_RE.match(str(value).strip()):
            return _fail(GATE_A_AUTHORIZATION_RECORD_INVALID,
                         f"{label} is not a full 40-character lowercase SHA"), None
    passed.append("pins_immutable")

    # ---- 1. Run-control artifacts exist at the exact planned paths -------
    run_control_root = context.authorization_record_path.parent
    for path, missing_code in (
        (context.authorization_record_path, GATE_A_AUTHORIZATION_RECORD_MISSING),
        (context.authorization_digest_path, GATE_A_AUTHORIZATION_DIGEST_MISSING),
        (context.owner_approval_path, GATE_A_OWNER_APPROVAL_MISSING),
    ):
        code = check_run_control_path(path, run_control_root)
        if code == GATE_A_REQUIRED_PATH_MISSING:
            return _fail(missing_code, f"missing: {path.name}"), None
        if code:
            return _fail(code, f"unsafe run-control path: {path.name}"), None
    passed.append("run_control_artifacts_present")

    try:
        record_raw = context.authorization_record_path.read_bytes()
        digest_raw = context.authorization_digest_path.read_bytes()
        approval_raw = context.owner_approval_path.read_bytes()
    except OSError as exc:
        # Permission errors fail closed, they never fall through to success.
        return _fail(GATE_A_FILESYSTEM_ERROR, f"cannot read run-control artifact: {exc.strerror}"), None

    # ---- 2/3. Recompute the record digest over EXACT bytes ---------------
    computed_record_sha = sha256_bytes(record_raw)
    stored_digest, digest_code = parse_digest_file(digest_raw)
    if digest_code:
        return _fail(digest_code, "digest file is not exactly one 64-char lowercase hex digest"), None
    if not _digests_equal(computed_record_sha, stored_digest):
        return _fail(GATE_A_AUTHORIZATION_DIGEST_MISMATCH,
                     "recomputed record digest does not match the stored digest file"), None
    passed.append("record_digest_matches_digest_file")

    # ---- 4. Parse the record --------------------------------------------
    record, rec_code, rec_detail = parse_record_bytes(record_raw)
    if rec_code:
        return _fail(rec_code, rec_detail), None

    schema_version = record.get("schema_version")
    if _blank(schema_version) or str(schema_version).strip() != CONTRACT_SCHEMA_VERSION:
        return _fail(GATE_A_AUTHORIZATION_RECORD_SCHEMA_UNSUPPORTED,
                     f"unsupported schema_version (expected {CONTRACT_SCHEMA_VERSION})"), None

    missing = [f for f in REQUIRED_RECORD_FIELDS if f not in record]
    if missing:
        return _fail(GATE_A_AUTHORIZATION_RECORD_INVALID,
                     f"missing required fields: {sorted(missing)}"), None
    blank = [f for f in REQUIRED_RECORD_FIELDS if _blank(record.get(f))]
    if blank:
        return _fail(GATE_A_AUTHORIZATION_RECORD_INVALID,
                     f"blank required fields: {sorted(blank)}"), None
    sentinel = [f for f in REQUIRED_RECORD_FIELDS if _is_sentinel(record.get(f))]
    if sentinel:
        return _fail(GATE_A_AUTHORIZATION_RECORD_INVALID,
                     f"sentinel values in required fields: {sorted(sentinel)}"), None
    passed.append("record_fields_complete")

    for sha_field in ("execution_framework_sha", "target_sha"):
        value = record.get(sha_field)
        if not isinstance(value, str):
            return _fail(GATE_A_AUTHORIZATION_RECORD_INVALID,
                         f"{sha_field} must be a string SHA, not {type(value).__name__}"), None
        if _is_floating_ref(value):
            return _fail(GATE_A_FLOATING_REF_PROHIBITED, f"{sha_field} is a floating ref"), None
        if not FULL_SHA_RE.match(value.strip()):
            return _fail(GATE_A_AUTHORIZATION_RECORD_INVALID,
                         f"{sha_field} is not a full 40-character lowercase SHA"), None
    for d_field in ("preparation_package_sha256", "gate_d_checklist_sha256"):
        value = record.get(d_field)
        if not isinstance(value, str) or not SHA256_RE.match(value.strip()):
            return _fail(GATE_A_AUTHORIZATION_RECORD_INVALID,
                         f"{d_field} is not 64 lowercase hex characters"), None
    passed.append("record_sha_shapes_valid")

    # ---- 5. Authorization status ----------------------------------------
    if str(record.get("authorization_status")).strip() != CONTRACT_AUTHORIZATION_STATUS:
        return _fail(GATE_A_AUTHORIZATION_STATUS_INVALID,
                     "authorization_status is not the single-controlled-invocation status"), None
    passed.append("authorization_status")

    # ---- 5b. Expiry, if the record declares one --------------------------
    expires = record.get("authorization_expires_at")
    if expires is not None and not _blank(expires):
        try:
            exp_dt = datetime.fromisoformat(str(expires).replace("Z", "+00:00"))
            if exp_dt.tzinfo is None:
                exp_dt = exp_dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return _fail(GATE_A_AUTHORIZATION_RECORD_INVALID,
                         "authorization_expires_at is not ISO-8601"), None
        if now >= exp_dt:
            return _fail(GATE_A_AUTHORIZATION_EXPIRED, "authorization window has closed"), None
    passed.append("authorization_not_expired")

    # ---- 6. Owner approval: distinct artifact binding the exact digest ---
    approval, ap_code, ap_detail = parse_approval_bytes(approval_raw)
    if ap_code:
        return _fail(ap_code, ap_detail), None
    missing_ap = [f for f in REQUIRED_APPROVAL_FIELDS if _blank(approval.get(f))]
    if missing_ap:
        return _fail(GATE_A_OWNER_APPROVAL_INVALID,
                     f"approval missing required fields: {sorted(missing_ap)}"), None
    sentinel_ap = [f for f in REQUIRED_APPROVAL_FIELDS if _is_sentinel(approval.get(f))]
    if sentinel_ap:
        return _fail(GATE_A_OWNER_APPROVAL_INVALID,
                     f"approval contains sentinel values: {sorted(sentinel_ap)}"), None

    approved_digest = str(approval.get("authorization_record_sha256", "")).strip()
    if not SHA256_RE.match(approved_digest):
        return _fail(GATE_A_OWNER_APPROVAL_INVALID,
                     "approval digest is not 64 lowercase hex characters"), None
    # Step 4 of section 2j: the approved digest is taken from the APPROVAL,
    # never from the record itself. A record that approves itself is not an
    # approval.
    if not _digests_equal(approved_digest, computed_record_sha):
        return _fail(GATE_A_OWNER_APPROVAL_DIGEST_MISMATCH,
                     "owner approved a different authorization-record revision"), None
    passed.append("owner_approval_binds_exact_digest")

    if str(approval.get("authorization_decision")).strip() != CONTRACT_AUTHORIZATION_STATUS:
        return _fail(GATE_A_OWNER_APPROVAL_INVALID,
                     "approval decision is not the single-controlled-invocation decision"), None

    approver = str(approval.get("approver_github_identity", "")).strip()
    if approver not in CONTRACT_APPROVING_AUTHORITIES:
        return _fail(GATE_A_OWNER_IDENTITY_MISMATCH,
                     "approver is not the repository owner or a named delegate"), None
    if context.operator_identity and context.operator_identity.strip() == \
            str(record.get("authorization_record_created_by", "")).strip() == approver:
        # Author == approver == operator is self-approval
        # (operator_self_approval_allowed: false).
        return _fail(GATE_A_OPERATOR_SELF_APPROVAL_PROHIBITED,
                     "operator, record author, and approver are the same identity"), None
    passed.append("approval_identity")

    try:
        datetime.fromisoformat(str(approval.get("approval_timestamp")).replace("Z", "+00:00"))
    except ValueError:
        return _fail(GATE_A_OWNER_APPROVAL_INVALID,
                     "approval_timestamp is not ISO-8601"), None

    # The approval must agree with the record on every pinned value; an
    # approval that names different revisions approves a different run.
    for ap_field, rec_field in (
        ("execution_framework_sha", "execution_framework_sha"),
        ("target_sha", "target_sha"),
        ("evidence_number", "evidence_number"),
        ("evidence_slug", "evidence_slug"),
        ("exact_model", "exact_model"),
    ):
        if str(approval.get(ap_field, "")).strip() != str(record.get(rec_field, "")).strip():
            return _fail(GATE_A_OWNER_APPROVAL_INVALID,
                         f"approval and record disagree on {ap_field}"), None
    passed.append("approval_agrees_with_record")

    # ---- 7/8. Framework and target revisions -----------------------------
    record_fw = str(record.get("execution_framework_sha")).strip()
    record_tgt = str(record.get("target_sha")).strip()

    if record_fw != context.execution_framework_sha.strip():
        return _fail(GATE_A_EXECUTION_FRAMEWORK_SHA_MISMATCH,
                     "record framework SHA does not match the resolved execution pin"), None
    if record_tgt != context.target_sha.strip():
        return _fail(GATE_A_TARGET_SHA_MISMATCH,
                     "record target SHA does not match the resolved target pin"), None

    framework_head = head_fn(context.framework_root)
    if framework_head != record_fw:
        return _fail(GATE_A_EXECUTION_FRAMEWORK_SHA_MISMATCH,
                     f"framework HEAD {framework_head[:12] or '<unknown>'} != "
                     f"authorized {record_fw[:12]}"), None
    target_head = head_fn(context.target_root)
    if target_head != record_tgt:
        return _fail(GATE_A_TARGET_SHA_MISMATCH,
                     f"target HEAD {target_head[:12] or '<unknown>'} != "
                     f"authorized {record_tgt[:12]}"), None
    passed.append("revisions_match_heads")

    if str(record.get("target_repository")).strip() != context.expected_target_repository:
        return _fail(GATE_A_TARGET_REPOSITORY_MISMATCH,
                     "authorization record was created for a different repository"), None
    passed.append("target_repository_identity")

    # ---- 9. Run-control commit -------------------------------------------
    # "Immutable run-control location" is a *commit* property, not a
    # filesystem convention (section 2f). The artifacts on disk must be the
    # ones introduced by the authorized run-control commit. This fails closed:
    # a resolver that cannot demonstrate the commit is a failure, not a skip.
    resolve_rc = run_control_commit_resolver or resolve_run_control_commit
    observed_rc = resolve_rc(context.framework_root, context.authorization_record_path)
    if not observed_rc:
        return _fail(GATE_A_RUN_CONTROL_COMMIT_MISMATCH,
                     "cannot demonstrate which commit introduced the run-control "
                     "artifacts; immutability is unproven"), None
    if observed_rc.strip() != context.run_control_commit_sha.strip():
        return _fail(GATE_A_RUN_CONTROL_COMMIT_MISMATCH,
                     "run-control artifacts do not come from the authorized "
                     "immutable run-control commit"), None
    passed.append("run_control_commit")

    # ---- 10. Evidence identity and artifact type -------------------------
    if not EVIDENCE_NUMBER_RE.match(str(record.get("evidence_number")).strip()):
        return _fail(GATE_A_EVIDENCE_IDENTITY_MISMATCH, "malformed evidence number"), None
    # Each authoritative value must equal BOTH the resolved context value and
    # the contract constant. Written as explicit `and`, never as a chained
    # comparison (which would silently compare the wrong pair).
    rec_evidence_number = str(record.get("evidence_number")).strip()
    if not (rec_evidence_number == context.evidence_number.strip()
            and rec_evidence_number == CONTRACT_EVIDENCE_NUMBER):
        return _fail(GATE_A_EVIDENCE_IDENTITY_MISMATCH, "evidence number mismatch"), None
    rec_slug = str(record.get("evidence_slug")).strip()
    if not (rec_slug == context.evidence_slug.strip() and rec_slug == CONTRACT_EVIDENCE_SLUG):
        return _fail(GATE_A_EVIDENCE_IDENTITY_MISMATCH, "evidence slug mismatch"), None
    rec_artifact_type = str(record.get("artifact_type")).strip()
    if not (rec_artifact_type == context.artifact_type.strip()
            and rec_artifact_type == CONTRACT_ARTIFACT_TYPE):
        return _fail(GATE_A_ARTIFACT_TYPE_MISMATCH, "artifact type mismatch"), None
    passed.append("evidence_identity")

    # ---- 11. Exact model --------------------------------------------------
    record_model = str(record.get("exact_model")).strip()
    if not (record_model == CONTRACT_EXACT_MODEL
            and record_model == context.exact_model.strip()):
        return _fail(GATE_A_MODEL_MISMATCH,
                     f"authorized model must be exactly {CONTRACT_EXACT_MODEL}"), None
    passed.append("exact_model")

    # ---- 12/13. Package and checklist provenance -------------------------
    for path_field, digest_field, canonical, path_code, digest_code_ in (
        ("preparation_package_path", "preparation_package_sha256", CONTRACT_PACKAGE_PATH,
         GATE_A_PACKAGE_PATH_MISMATCH, GATE_A_PACKAGE_DIGEST_MISMATCH),
        ("gate_d_checklist_path", "gate_d_checklist_sha256", CONTRACT_CHECKLIST_PATH,
         GATE_A_CHECKLIST_PATH_MISMATCH, GATE_A_CHECKLIST_DIGEST_MISMATCH),
    ):
        declared = str(record.get(path_field)).strip().replace("\\", "/")
        if declared != canonical:
            return _fail(path_code, f"{path_field} is not the canonical path"), None
        resolved = context.framework_root / canonical
        if not _is_within(resolved, context.framework_root):
            return _fail(GATE_A_PATH_ESCAPE_PROHIBITED, f"{path_field} escapes framework root"), None
        if resolved.is_symlink():
            return _fail(GATE_A_SYMLINK_PROHIBITED, f"{path_field} is a symlink"), None
        actual = sha256_file(resolved)
        if actual is None:
            return _fail(GATE_A_REQUIRED_PATH_MISSING,
                         f"{path_field} does not exist at the framework root"), None
        if not _digests_equal(actual, str(record.get(digest_field)).strip()):
            return _fail(digest_code_,
                         f"{path_field} bytes differ from the authorized digest"), None
    passed.append("package_and_checklist_provenance")

    # ---- 14. Safety booleans and invocation limit ------------------------
    bool_codes = {
        "no_retry": GATE_A_RETRY_PROHIBITED,
        "no_fallback": GATE_A_FALLBACK_PROHIBITED,
        "no_model_substitution": GATE_A_MODEL_SUBSTITUTION_PROHIBITED,
        "no_artifact_repair": GATE_A_ARTIFACT_REPAIR_PROHIBITED,
        "no_target_mutation": GATE_A_TARGET_MUTATION_PROHIBITED,
        "one_invocation_only": GATE_A_INVOCATION_LIMIT_INVALID,
        "stop_on_first_failed_gate": GATE_A_AUTHORIZATION_RECORD_INVALID,
    }
    for boolean in REQUIRED_SAFETY_BOOLEANS:
        value = record.get(boolean)
        # Strictly `True`. The string "true" or 1 is not a validated boolean.
        if value is not True:
            return _fail(bool_codes[boolean],
                         f"{boolean} must be exactly true in the authorization record"), None
    if int(context.invocation_limit) != CONTRACT_INVOCATION_LIMIT:
        return _fail(GATE_A_INVOCATION_LIMIT_INVALID,
                     f"invocation limit must be exactly {CONTRACT_INVOCATION_LIMIT}"), None
    declared_limit = record.get("invocation_limit", CONTRACT_INVOCATION_LIMIT)
    if int(declared_limit) != CONTRACT_INVOCATION_LIMIT:
        return _fail(GATE_A_INVOCATION_LIMIT_INVALID,
                     f"invocation limit must be exactly {CONTRACT_INVOCATION_LIMIT}"), None
    passed.append("safety_booleans_and_invocation_limit")

    # ---- 15. Required paths, and no pre-existing Evidence 0016 output ----
    for rel in context.required_framework_paths:
        if not (context.framework_root / rel).exists():
            return _fail(GATE_A_REQUIRED_PATH_MISSING,
                         f"required framework path missing: {rel}"), None
    for rel in context.required_target_paths:
        if not (context.target_root / rel).exists():
            return _fail(GATE_A_REQUIRED_PATH_MISSING,
                         f"required target path missing: {rel}"), None
    evidence_dir = context.evidence_output_dir or (
        context.framework_root / "experiments" / "evidence" / CONTRACT_EVIDENCE_SLUG
    )
    if evidence_dir.exists() and any(evidence_dir.iterdir()):
        return _fail(GATE_A_EVIDENCE_OUTPUT_ALREADY_PRESENT,
                     "Evidence 0016 output already exists; refusing to accept it as fresh"), None
    passed.append("required_paths_and_no_stale_output")

    snapshot = _ValidatedSnapshot(
        record_sha256=computed_record_sha,
        digest_file_sha256=sha256_bytes(digest_raw),
        approval_sha256=sha256_bytes(approval_raw),
        package_sha256=sha256_file(context.framework_root / CONTRACT_PACKAGE_PATH) or "",
        checklist_sha256=sha256_file(context.framework_root / CONTRACT_CHECKLIST_PATH) or "",
        framework_head=framework_head,
        target_head=target_head,
    )
    decision = AuthorizationDecision(
        authorized=True,
        failure_code=None,
        validated_record_sha256=computed_record_sha,
        validated_owner_identity=approver,
        validated_framework_sha=record_fw,
        validated_target_sha=record_tgt,
        validated_run_control_commit_sha=context.run_control_commit_sha.strip(),
        validated_model=record_model,
        validated_invocation_limit=CONTRACT_INVOCATION_LIMIT,
        checks_passed=tuple(passed),
    )
    return decision, snapshot


def identity_for_context(context: AuthorizationContext, *,
                         workflow_id: str = "repo-sensemaker",
                         workflow_stage: str = "stage-1",
                         executor_id: str = "claude-code",
                         output_path=None) -> InvocationIdentity:
    """Derive the invocation identity a capability for ``context`` authorizes.

    The output path defaults to the contract's evidence-output destination, so
    the bound identity is the campaign invocation, not "anything at all".
    """
    if output_path is None:
        output_path = (context.evidence_output_dir
                       if context.evidence_output_dir is not None
                       else Path("experiments/evidence") / context.evidence_slug)
    return InvocationIdentity.build(
        workflow_id=workflow_id,
        workflow_stage=workflow_stage,
        artifact_type=context.artifact_type,
        evidence_number=context.evidence_number,
        evidence_slug=context.evidence_slug,
        output_path=output_path,
        framework_root=context.framework_root,
        target_root=context.target_root,
        target_repository=context.expected_target_repository,
        target_sha=context.target_sha,
        requested_model=context.exact_model,
        executor_id=executor_id,
        invocation_limit=context.invocation_limit,
        execution_framework_sha=context.execution_framework_sha,
        declared_controlled_mode=True,
    )


def authorize_invocation(context: AuthorizationContext, *,
                         git_head: Optional[Callable[[Path], str]] = None,
                         run_control_commit_resolver: Optional[Callable[[Path, Path], str]] = None,
                         now: Optional[datetime] = None,
                         invocation_identity: Optional[InvocationIdentity] = None
                         ) -> tuple[AuthorizationDecision, Optional[AuthorizedInvocation]]:
    """Evaluate Gate A and, only on success, issue the single-use capability.

    This is the only function in the codebase that can produce an
    ``AuthorizedInvocation``. On any failure it returns ``(decision, None)`` --
    there is no partial capability.

    The capability is issued *by the registry*: what is returned is an opaque
    handle to one live issuance record bound to ``invocation_identity``.
    Possessing the object is not authorization; being live in the registry is.
    """
    decision, snapshot = authorize(
        context, git_head=git_head,
        run_control_commit_resolver=run_control_commit_resolver, now=now,
    )
    if not decision.authorized or snapshot is None:
        return decision, None
    identity = invocation_identity or identity_for_context(context)
    return decision, _REGISTRY.issue(decision, context, snapshot, identity)


def format_gate_a_log(decision: AuthorizationDecision) -> str:
    """ASCII-only, secret-free single-line log record."""
    d = decision.to_log_dict()
    parts = [f"GATE_A decision={'AUTHORIZED' if d['authorized'] else 'DENIED'}"]
    if d["failure_code"]:
        parts.append(f"code={d['failure_code']}")
        if d["failure_detail"]:
            parts.append(f"detail={d['failure_detail']}")
    parts.append(f"evidence={d['evidence_number']}")
    if d["authorization_record_sha256"]:
        parts.append(f"record_sha256={d['authorization_record_sha256'][:16]}...")
    if d["framework_sha"]:
        parts.append(f"framework_sha={d['framework_sha'][:12]}")
    if d["target_sha"]:
        parts.append(f"target_sha={d['target_sha'][:12]}")
    if d["model"]:
        parts.append(f"model={d['model']}")
    return " ".join(parts)
