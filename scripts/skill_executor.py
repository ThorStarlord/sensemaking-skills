"""
Skill Executor — interface and implementations for invoking skills.

Defines the boundary between "the runtime prepared skill invocation" and
"the skill was actually invoked." This prevents dry-run logging from being
reported as real skill execution.

Usage:
    from skill_executor import create_executor

    executor = create_executor("dry-run", repo_root)
    result = executor.invoke_skill(skill_id, command, input_artifacts, expected_output, context)
    print(result.status)  # PREPARED, PROMPT_GENERATED, EXECUTED, FAILED, UNSUPPORTED
"""

import os
import sys
import json
import re
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from pathlib import Path

# Gate A authorization consumer. Imported by module name because scripts/ is
# already on sys.path for every consumer of this module.
from gate_a_authorization import (  # noqa: E402
    AuthorizedInvocation,
    DeclaredExploratory,
    ExecutionMode,
    GateAError,
    InvocationIdentity,
    LANE_AMBIGUOUS,
    LANE_CANONICAL,
    LANE_EXPLORATORY,
    LANE_ORDINARY,
    GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED,
    GATE_A_CAPABILITY_NOT_LIVE,
    GATE_A_INVOCATION_CLASSIFICATION_AMBIGUOUS,
    GATE_A_INVOCATION_IDENTITY_MISMATCH,
    GATE_A_MODEL_MISMATCH,
    CONTRACT_ARTIFACT_TYPE,
    classify_invocation,
    derive_authorization_lane,
    format_gate_a_log,
    parse_evidence_path,
    requires_gate_a,
)

# Phase 3 exploratory authorization (issue #119). Imported LAZILY -- see
# `_load_exploratory_authorization` below -- never at module load. The
# established minimal Gate A environment deliberately installs neither the
# Phase 2/3 package nor its declared dependencies (rfc8785, jsonschema);
# an eager import here would break every canonical executor import there.
# When the lazy import does run, it happens AFTER gate_a_authorization was
# imported: the Gate A loader pins the checkout `src/` at the front of
# sys.path and refuses an already-imported foreign package, so the
# exploratory import must never precede the gate_a import above.


# ============================================================================
# Gate A invocation binding
# ============================================================================
#
# The core invariant this enforces:
#
#     No valid authorization capability, no path to the model invocation
#     function.
#
# REMEDIATION (issue #108 independent review). The first design made this
# decision from a caller-supplied boolean, `controlled_experiment`. That was a
# reproduced bypass: the flag defaults to False, so omitting one CLI flag
# reached the provider with no authorization at all, and assigning
# `executor.controlled_experiment = False` after construction downgraded a
# gated executor while leaving its capability unspent and reusable.
#
# The boolean is no longer a security input. Whether Gate A is mandatory is
# DERIVED, at every provider boundary, from an immutable `InvocationIdentity`
# built from the actual invocation arguments -- workflow stage, artifact type,
# evidence number/slug, output destination, target pin, exact model. The
# declared flag survives only as informational metadata, and a declared
# `False` that disagrees with structural signals yields AMBIGUOUS, which is
# gated exactly like CONTROLLED_STAGE1.
#
# Ordinary (non-campaign) development invocations remain ungated only when they
# are structurally distinguishable: outside every controlled evidence
# namespace, not naming the campaign evidence identity, not targeting the
# pinned campaign repository, not requesting the exact campaign model. See
# gate_a_authorization.classify_invocation and ADR 0022.


class GateAAuthorizationRequired(ValueError):
    """Raised when a controlled invocation is attempted with no capability.

    Subclasses ValueError so the existing OrchestrationRunner/create_executor
    error handling turns it into a formatted runtime error rather than an
    unhandled crash -- while still being catchable specifically.
    """

    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


class _GateAImmutableAttributes:
    """Refuses post-construction reassignment of security-relevant attributes.

    This is defense in depth, not the boundary. The boundary is that every
    provider-side authorization decision is derived from the invocation
    arguments at the moment of the call, so even a successful `__dict__` poke
    cannot downgrade the classification of what is actually being invoked.
    """

    _GATE_A_FROZEN = frozenset({
        "repo_root",
        "model",
        "authorization",
        "exploratory_capability",
        "controlled_experiment",
        "_declared_controlled_experiment",
        "_invocation_identity",
    })

    def __setattr__(self, name, value):
        if name in self._GATE_A_FROZEN and name in self.__dict__:
            raise AttributeError(
                f"{name!r} is fixed at construction on "
                f"{type(self).__name__}; Gate A classification is derived from "
                f"immutable invocation identity and cannot be reassigned."
            )
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name in self._GATE_A_FROZEN:
            raise AttributeError(
                f"{name!r} may not be deleted from {type(self).__name__}."
            )
        object.__delattr__(self, name)

    @property
    def controlled_experiment(self) -> bool:
        """Informational only. NOT an authorization switch.

        Kept because callers, logs, and the CLI still speak this word. It is
        the *declared* mode; the *effective* mode is
        ``classify_invocation(identity)`` and a declared False never overrides
        a structural controlled-Stage-1 signal.
        """
        return bool(self.__dict__.get("_declared_controlled_experiment", False))


def require_authorization_capability(
    capability: Optional[AuthorizedInvocation],
    *,
    identity: Optional[InvocationIdentity],
    model: Optional[str],
    executor_name: str,
    mode: Optional[ExecutionMode] = None,
    why: Optional[str] = None,
) -> ExecutionMode:
    """Fail closed unless a Gate-A-requiring invocation carries a live capability.

    Non-consuming. Called early so the failure happens before any prompt is
    built, any SDK object is constructed, or any provider client exists.

    Returns the derived ``ExecutionMode`` so callers can log what was decided.

    ``mode`` / ``why`` may be supplied when the caller has already derived
    the classification from a richer source than ``classify_invocation``
    alone (the four-lane dispatcher, where a declaration can make an
    identity-ordinary invocation AMBIGUOUS). When omitted, the classification
    is derived from the identity here.
    """
    if mode is None:
        mode, signals = classify_invocation(identity)
        why = why or (",".join(signals) or "none")
    if not requires_gate_a(mode):
        return mode
    why = why or ","
    if capability is None:
        raise GateAAuthorizationRequired(
            GATE_A_INVOCATION_CLASSIFICATION_AMBIGUOUS
            if mode is ExecutionMode.AMBIGUOUS
            else GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED,
            f"{executor_name} classified this invocation as {mode.value} "
            f"(signals: {why}) and refuses it with no Gate A authorization "
            f"capability. A live AuthorizedInvocation must be supplied; there "
            f"is no flag, environment variable, or override that substitutes "
            f"for it.",
        )
    if not isinstance(capability, AuthorizedInvocation):
        raise GateAAuthorizationRequired(
            GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED,
            f"{executor_name} received an object that is not an "
            f"AuthorizedInvocation capability.",
        )
    # Liveness is asked of the issuer registry, not of the object. A copy, a
    # reconstruction, or a forged ID is not live.
    if not capability.live:
        raise GateAAuthorizationRequired(
            GATE_A_CAPABILITY_NOT_LIVE,
            f"{executor_name} received a capability with no live issuance "
            f"record: it was never issued, is already spent, or is a "
            f"reconstruction of one that was.",
        )
    if not capability.decision.authorized:
        raise GateAAuthorizationRequired(
            GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED,
            f"{executor_name} received a capability whose Gate A decision is "
            f"not authorized.",
        )
    if model is not None and capability.model != model:
        raise GateAAuthorizationRequired(
            GATE_A_MODEL_MISMATCH,
            f"{executor_name} was configured for model '{model}' but the "
            f"capability authorizes '{capability.model}'.",
        )
    bound = capability.identity
    if identity is not None and bound is not None and bound.digest() != identity.digest():
        raise GateAAuthorizationRequired(
            GATE_A_INVOCATION_IDENTITY_MISMATCH,
            f"{executor_name} is performing an invocation that is not the one "
            f"this capability authorizes.",
        )
    return mode


class ExploratoryAuthorizationRequired(GateAAuthorizationRequired):
    """Gate A-class denial raised on the EXPLORATORY lane (Phase 3, #119)."""


#: Stable failure code: the exploratory authorization component (or one of
#: its declared dependencies, e.g. rfc8785 or jsonschema) is unavailable in
#: this environment. Raised on the EXPLORATORY lane BEFORE any provider
#: construction or capability inspection; the invocation is never silently
#: downgraded to ORDINARY or CANONICAL, and a raw ImportError is never
#: surfaced as an authorization result. Precedence on the EXPLORATORY lane:
#: component availability precedes capability availability.
EXPLORATORY_AUTHORIZATION_COMPONENT_UNAVAILABLE = (
    "EXPLORATORY_AUTHORIZATION_COMPONENT_UNAVAILABLE"
)

_EA_MODULE = None


def _load_exploratory_authorization():
    """Import the exploratory authorization package on first EXPLORATORY use.

    Called ONLY when an actual invocation has been structurally classified
    EXPLORATORY (or its consumption/burn path genuinely needs the package).
    The successfully loaded module is cached for the process. An import
    failure -- the package itself, or one of its declared dependencies such
    as rfc8785, is unavailable -- raises the single stable configuration
    failure instead of leaking a raw ImportError as an authorization result.
    """
    global _EA_MODULE
    if _EA_MODULE is not None:
        return _EA_MODULE
    try:
        from sensemaking_skills import exploratory_authorization as _ea
    except ImportError as exc:
        raise ExploratoryAuthorizationRequired(
            EXPLORATORY_AUTHORIZATION_COMPONENT_UNAVAILABLE,
            "the exploratory authorization component is unavailable in this "
            f"environment ({exc}); the invocation is refused.",
        ) from exc
    _EA_MODULE = _ea
    return _ea


def declared_exploratory_from_context(context: Optional[dict]) -> Optional[DeclaredExploratory]:
    """The caller's declared exploratory identity, if any, from the call context.

    Fail-closed: if ANY declaration field is present, all four are treated as
    declared (missing fields become empty strings and fail the structural
    well-formedness check in ``derive_authorization_lane``). A partial or
    malformed claim therefore lands AMBIGUOUS -- never ORDINARY.
    """
    ctx = context or {}
    fields = ("campaign_id", "classification", "attempt_id", "configuration_id")
    if not any(ctx.get(name) is not None for name in fields):
        return None
    return DeclaredExploratory(
        campaign_id=str(ctx.get("campaign_id") or ""),
        classification=str(ctx.get("classification") or ""),
        attempt_id=str(ctx.get("attempt_id") or ""),
        configuration_id=str(ctx.get("configuration_id") or ""),
    )


def require_invocation_authorization(
    authorization: Optional[AuthorizedInvocation],
    exploratory_capability,
    *,
    identity: Optional[InvocationIdentity],
    model: Optional[str],
    executor_name: str,
    declared: Optional[DeclaredExploratory] = None,
) -> tuple[str, ExecutionMode]:
    """The four-lane dispatcher every provider-boundary entry point calls.

    Derives the lane from the ACTUAL invocation (identity + declared
    exploratory values) and demands the right capability:

    * EXPLORATORY -> the exploratory capability must exist, be the right
      type, and be live (fail-fast, non-consuming); the consumption itself
      happens at the narrowest point, immediately before the provider call.
    * CANONICAL / AMBIGUOUS -> the existing Gate A check (verbatim):
      ``require_authorization_capability``.
    * ORDINARY -> no authorization is consulted at all.

    Returns ``(lane, mode)`` so the caller can log what was decided and
    choose the correct consuming path.
    """
    lane, signals = derive_authorization_lane(identity, declared)
    if lane == LANE_EXPLORATORY:
        why = ",".join(signals) or "none"
        _ea = _load_exploratory_authorization()
        failure = _ea.exploratory_capability_availability(exploratory_capability)
        if failure is not None:
            raise ExploratoryAuthorizationRequired(
                failure,
                f"{executor_name} classified this invocation as {lane} "
                f"(signals: {why}) and refuses it: no usable exploratory "
                f"capability ({failure}).",
            )
        return lane, ExecutionMode.AMBIGUOUS
    if lane == LANE_ORDINARY:
        # No authorization is consulted for ordinary development. This branch
        # is taken BEFORE re-classification so a declaration-induced AMBIGUOUS
        # lane can never fall through to ordinary (fail closed).
        return lane, ExecutionMode.ORDINARY_DEVELOPMENT
    # CANONICAL / AMBIGUOUS: the identical Gate A demand. The mode is forced
    # from the lane, never re-derived from the identity alone -- an
    # identity-ordinary invocation carrying an exploratory claim is AMBIGUOUS
    # and must demand the canonical capability exactly like any other
    # ambiguous invocation.
    forced_mode = (
        ExecutionMode.CONTROLLED_STAGE1 if lane == LANE_CANONICAL
        else ExecutionMode.AMBIGUOUS
    )
    mode = require_authorization_capability(
        authorization,
        identity=identity,
        model=model,
        executor_name=executor_name,
        mode=forced_mode,
        why=",".join(signals) or "none",
    )
    return lane, mode


def _exploratory_invocation_context(executor, context, output_path):
    """The consumption context, built from the CALL (never from the capability).

    Every field is the value actually being invoked right now: model from the
    executor configuration, the rest from the invocation context. Absent
    fields become empty strings, which fail closed against any non-empty
    binding.
    """
    _ea = _load_exploratory_authorization()
    return _ea.ExploratoryInvocationContext(
        model=executor.model or "",
        target_repository=str(context.get("target_repository") or ""),
        target_sha=str(context.get("target_sha") or ""),
        framework_sha=str(context.get("execution_framework_sha") or ""),
        artifact_type=str(context.get("artifact_type") or ""),
        output_path=output_path,
        campaign_id=str(context.get("campaign_id") or ""),
        configuration_id=str(context.get("configuration_id") or ""),
        configuration_snapshot_digest=str(
            context.get("configuration_snapshot_digest") or ""),
        policy_digest=str(context.get("policy_digest") or ""),
        approval_digest=str(context.get("approval_digest") or ""),
        attempt_id=str(context.get("attempt_id") or ""),
        lane=_ea.EXPLORATORY_LANE,
    )


# NOTE (issue #108, second independent review):
# There used to be an `_EVIDENCE_DIR_RE` here -- a SECOND, independently
# maintained evidence-path regex that ran over the raw output string. It was
# weak in the same way the classifier's substring test was weak, so the two
# checks failed together on `experiments/./evidence/0016-...` and
# `experiments//evidence//0016-...`, both of which reached a provider with no
# authorization at all. It has been deleted, not fixed: the runtime now
# consumes `gate_a_authorization.parse_evidence_path`, the single shared
# parser the classifier consumes. Do not reintroduce a local regex here; the
# runtime/classifier agreement invariant test will fail if you do.

#: Skill ids that ARE Stage 1 repository sensemaking.
_STAGE_1_SKILLS = ("repo-sensemaker",)


def build_invocation_identity(
    *,
    repo_root: str,
    executor_id: str,
    skill_id: str = "",
    expected_output_artifact: str = "",
    context: Optional[dict] = None,
    model: Optional[str] = None,
    declared_controlled_mode: Optional[bool] = None,
) -> InvocationIdentity:
    """Build the immutable identity of the invocation actually being performed.

    Everything here comes from the CALL, not from mutable executor state that
    an attacker could have poked after construction. That is what makes the
    post-construction-downgrade bypass structurally impossible rather than
    merely tested against.
    """
    ctx = context or {}

    # `expected_output_artifact` is the artifact TYPE at the invoke_skill
    # layer and a resolved PATH at the async provider layer. Both layers must
    # derive the SAME identity or the fail-fast check and the consuming check
    # would disagree, so normalize here rather than at the call sites.
    looks_like_path = bool(expected_output_artifact) and (
        "/" in expected_output_artifact or "\\" in expected_output_artifact
    )
    output = str(ctx.get("expected_output_path", "") or "")
    if not output and looks_like_path:
        output = expected_output_artifact

    artifact_type = str(ctx.get("artifact_type", "") or "")
    if not artifact_type and expected_output_artifact and not looks_like_path:
        artifact_type = expected_output_artifact
    if not artifact_type and skill_id in _STAGE_1_SKILLS:
        artifact_type = CONTRACT_ARTIFACT_TYPE

    workflow_stage = str(ctx.get("workflow_stage", "") or "")
    if not workflow_stage and skill_id in _STAGE_1_SKILLS:
        workflow_stage = "stage-1"

    evidence_number = ctx.get("evidence_number")
    evidence_slug = ctx.get("evidence_slug")
    if not (evidence_number and evidence_slug):
        # ONE parser, shared with the classifier. See parse_evidence_path.
        # `repo_root` is passed as the authoritative anchor: without it a
        # relative output path would be interpreted against process CWD and an
        # aliased campaign path would yield no evidence identity at all.
        ident = parse_evidence_path(output, repo_root)
        if ident.evidence_number:
            evidence_number = evidence_number or ident.evidence_number
            evidence_slug = evidence_slug or ident.evidence_slug

    return InvocationIdentity.build(
        workflow_id=str(ctx.get("workflow_id", "") or skill_id),
        workflow_stage=workflow_stage,
        artifact_type=artifact_type,
        evidence_number=evidence_number,
        evidence_slug=evidence_slug,
        output_path=output,
        framework_root=repo_root,
        target_root=str(ctx.get("target_root", "") or ""),
        target_repository=str(ctx.get("target_repository", "") or ""),
        target_sha=str(ctx.get("target_sha", "") or ""),
        requested_model=model or "",
        executor_id=executor_id,
        invocation_limit=int(ctx.get("invocation_limit", 1) or 1),
        execution_framework_sha=ctx.get("execution_framework_sha"),
        declared_controlled_mode=declared_controlled_mode,
    )


def display_relative_path(path: str, root: str) -> str:
    """`os.path.relpath` that survives a cross-drive pair.

    On Windows `os.path.relpath("C:/tmp/x", "H:/repo")` raises ValueError
    ("path is on mount 'C:', start on mount 'H:'"). This is used only to render
    a prompt-facing path, but the raised ValueError propagated out of prompt
    construction and aborted the invocation BEFORE the Gate A boundary --
    turning specific Gate A error codes into a generic
    "Skill execution failed: path is on mount ..." and, worse, breaking the
    positive exactly-one-invocation proof. When the two paths share no mount
    there is no relative form; the absolute path is the honest answer.

    This is presentation only. It is never used for a security decision --
    containment is decided by `gate_a_authorization.resolve_containment`.
    """
    try:
        return os.path.relpath(path, root)
    except ValueError:
        return os.path.abspath(path)


def validate_model_identifier(model: str) -> None:
    """Validate an explicitly-supplied model identifier before it can reach
    ClaudeAgentOptions/the SDK (issue #86).

    Rules (deliberately minimal -- this is generic controlled-run
    infrastructure, not a hardcoded allowlist):
      - must not be empty
      - must not have surrounding whitespace

    Does NOT restrict the value to any specific model name. Stage 1's
    documented command and tests are expected to always pass exactly
    "claude-sonnet-5", but that is an experiment-configuration convention
    enforced by the caller/tests, not a runtime restriction -- this function
    must not silently normalize or reject a different owner-approved model
    string for some other controlled run.

    Raises:
        ValueError: if model is empty or has leading/trailing whitespace.
    """
    if model == "":
        raise ValueError("Explicit model identifier must not be empty.")
    if model != model.strip():
        raise ValueError(
            f"Explicit model identifier must not have surrounding whitespace: {model!r}"
        )

# Runtime-owned skeleton for repository_sensemaking_brief (issue #55).
import brief_skeleton

# Canonical semantic authorities (issue #58): the workflow-ID registry and the
# weakness-type enum are parsed with the SAME loader functions the validator
# itself uses (_validator_utils.load_workflow_registry /
# load_weakness_types), so the list injected into the model's execution
# instruction can never drift from what scripts/validate-brief.py actually
# checks. Do not re-parse these files independently.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _validator_utils import load_workflow_registry, load_weakness_types  # noqa: E402
from repo_probes import append_probe_section  # noqa: E402


# ============================================================================
# Semantic authorities (issue #58)
# ============================================================================

def get_allowed_workflow_ids(repo_root: str) -> list[str]:
    """Return the current top-level workflow IDs from workflow-registry.yaml.

    Uses the same loader (_validator_utils.load_workflow_registry) that
    scripts/validate-brief.py uses to validate recommended_workflow_id, so
    this list cannot drift from what the validator actually accepts. These
    are top-level `workflows: - id:` entries only -- NOT skill IDs and NOT
    step IDs (both of which also appear as `id:` keys elsewhere in the same
    YAML file, but are not valid values for recommended_workflow_id).

    Raises RuntimeError (fails loudly, no silent empty/stale fallback) if the
    registry file is missing, unparseable, or has no workflows.
    """
    registry = load_workflow_registry(repo_root)
    if registry is None:
        raise RuntimeError(
            "Cannot build execution instruction: workflow-registry.yaml could not "
            "be loaded (missing or invalid YAML) at "
            "skills/workflow-planner/references/workflow-registry.yaml. "
            "Refusing to fall back to an empty/stale workflow-ID list."
        )
    workflows = registry.get("workflows")
    if not workflows:
        raise RuntimeError(
            "Cannot build execution instruction: workflow-registry.yaml parsed "
            "but contains no top-level 'workflows' entries."
        )
    ids = [w["id"] for w in workflows if isinstance(w, dict) and "id" in w]
    if not ids:
        raise RuntimeError(
            "Cannot build execution instruction: workflow-registry.yaml has a "
            "'workflows' list but no entries with an 'id' field."
        )
    return ids


def get_allowed_weakness_types(repo_root: str) -> list[str]:
    """Return the current weakness-type enum from weakness-types.md.

    Uses the same loader (_validator_utils.load_weakness_types) that
    scripts/validate-brief.py uses to validate the Weakest boundary section,
    so this list cannot drift from what the validator actually accepts.

    Raises RuntimeError (fails loudly, no silent empty/stale fallback) if the
    reference file is missing or yields no types.
    """
    types = load_weakness_types(repo_root)
    if not types:
        raise RuntimeError(
            "Cannot build execution instruction: weakness-types.md could not be "
            "loaded or parsed (expected 7 bolded terms) at "
            "skills/repo-sensemaker/references/weakness-types.md. Refusing to "
            "fall back to an empty/stale weakness-type list."
        )
    return types


def resolve_output_path(repo_root: str, expected_output_artifact: str, context: Optional[dict]) -> str:
    """Resolve the absolute path where a skill's output artifact must be written.

    The runtime owns artifact path resolution (contracts + session scoping via
    OrchestrationRunner._resolve_artifact_path). When it invokes a skill it passes
    the already-resolved, session-scoped path as context['expected_output_path'].
    Executors MUST honor that path so the producer (executor) and consumer
    (runtime) agree on where the artifact lives.

    Only when no path is provided (e.g. an executor used standalone, outside the
    runtime) do we fall back to the flat artifacts/<id>.md path.
    """
    provided = (context or {}).get("expected_output_path")
    if provided:
        return provided
    return os.path.join(repo_root, "artifacts", expected_output_artifact + ".md")


# ============================================================================
class SkillExecutionStatus(Enum):
    """Honest status values that distinguish preparation from real execution."""
    PREPARED = "prepared"          # dry-run: invocation was prepared/logged
    PROMPT_GENERATED = "prompt_generated"  # prompt-chain: human/agent prompt created
    EXECUTED = "executed"          # real skill execution happened
    FAILED = "failed"              # attempted and failed
    UNSUPPORTED = "unsupported"    # selected executor is not implemented


# ============================================================================
# Result Object
# ============================================================================

@dataclass
class SkillExecutionResult:
    """Result of a single skill invocation attempt."""
    skill_id: str
    status: SkillExecutionStatus
    command: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    output_artifact: Optional[str] = None
    message: str = ""
    error: str = ""
    validator_results: Optional[list] = None
    validation_passed: Optional[bool] = None
    # Model-enforcement evidence (issue #86). requested_model is the model
    # explicitly supplied to the executor (None for ambient/default runs).
    # reported_models is every distinct AssistantMessage.model value observed
    # from the SDK during this invocation. model_match is True/False when
    # requested_model was set (None when no model was requested, since there
    # is nothing to match against).
    requested_model: Optional[str] = None
    reported_models: Optional[list] = None
    model_match: Optional[bool] = None

    def to_dict(self) -> dict:
        return {
            "skill_id": self.skill_id,
            "status": self.status.value,
            "command": self.command,
            "timestamp": self.timestamp,
            "output_artifact": self.output_artifact,
            "message": self.message,
            "error": self.error,
            "validator_results": self.validator_results,
            "validation_passed": self.validation_passed,
            "requested_model": self.requested_model,
            "reported_models": self.reported_models,
            "model_match": self.model_match,
        }


# ============================================================================
# Abstract Base Class
# ============================================================================

class SkillExecutor(ABC):
    """Interface for skill invocation.

    Each executor implementation determines how a skill is actually invoked.
    The runtime selects an executor based on the execution mode and passes
    it to the skill-execution-agent.
    """

    supports_real_execution: bool = False
    """Whether this executor actually runs skills (not just dry-run/prompt)."""

    @abstractmethod
    def invoke_skill(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        ...

    def validate_mode(self, mode: str) -> Optional[str]:
        """Return an error message if this executor cannot honestly run in the given mode."""
        if mode in ("autonomous_execution", "yolo_execution") and not self.supports_real_execution:
            return (
                f"{mode} requires a real SkillExecutor with supports_real_execution=True.\n"
                f"Current executor: {self.__class__.__name__} "
                f"(supports_real_execution={self.supports_real_execution}).\n"
                f"This mode cannot honestly execute skills yet."
            )
        return None


# ============================================================================
# Dry-Run Executor
# ============================================================================

class DryRunSkillExecutor(SkillExecutor):
    """Validates that a skill exists in the registry and logs the intended invocation.

    This is the current behavior — the skill is never actually invoked.
    The result status is PREPARED, not EXECUTED.
    """

    supports_real_execution: bool = False

    def invoke_skill(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        return SkillExecutionResult(
            skill_id=skill_id,
            status=SkillExecutionStatus.PREPARED,
            command=invocation_command,
            output_artifact=expected_output_artifact,
            message=f"Dry run: invocation of '{invocation_command}' prepared. "
                    f"Skill was NOT actually invoked.",
        )


# ============================================================================
# Prompt Chain Executor
# ============================================================================

class PromptChainSkillExecutor(SkillExecutor):
    """Generates copy-paste prompts for manual or coding-agent skill execution.

    The prompts are written to a file and returned. No actual skill invocation
    happens — the output is intended for a human or coding agent to run.
    """

    supports_real_execution: bool = False

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def invoke_skill(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        # Build a prompt for the skill
        prompt_lines = [
            f"# Skill: {skill_id}",
            f"## Command: {invocation_command}",
            f"## Expected Output: {expected_output_artifact}",
            "",
            "### Input Context",
        ]
        for artifact in input_artifacts:
            prompt_lines.append(f"- {artifact}")
        prompt_lines.extend([
            "",
            "### Instructions",
            f"Run {invocation_command} with the context above.",
            f"Produce the output artifact at: {expected_output_artifact}",
            "",
            "---",
            f"Prompt generated by PromptChainSkillExecutor at {datetime.now().isoformat()}",
        ])
        prompt_text = "\n".join(prompt_lines)

        # Write prompt to file
        os.makedirs(self.output_dir, exist_ok=True)
        prompt_path = os.path.join(self.output_dir, f"prompt_{skill_id}.md")
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(prompt_text)

        return SkillExecutionResult(
            skill_id=skill_id,
            status=SkillExecutionStatus.PROMPT_GENERATED,
            command=invocation_command,
            output_artifact=expected_output_artifact,
            message=f"Prompt chain: prompt for '{invocation_command}' written to {prompt_path}. "
                    f"Skill was NOT actually invoked.",
        )


# ============================================================================
# Unsupported / Future Executors
# ============================================================================

# Factory
# ============================================================================

EXECUTOR_REGISTRY = {
    "dry-run": DryRunSkillExecutor,
    "prompt-chain": PromptChainSkillExecutor,
}


def create_executor(
    executor_id: str,
    repo_root: str,
    prompt_output_dir: Optional[str] = None,
    model: Optional[str] = None,
    controlled_experiment: bool = False,
    authorization: Optional[AuthorizedInvocation] = None,
    exploratory_capability=None,
    invocation_identity: Optional[InvocationIdentity] = None,
) -> SkillExecutor:
    """Create a SkillExecutor instance by id.

    Gate A: `authorization` is the typed capability minted by
    `gate_a_authorization.authorize_invocation()`. It is REQUIRED whenever
    `controlled_experiment` is True, for every executor id. There is no
    executor id that performs a controlled Stage 1 invocation without it.

    Phase 3 (issue #119): `exploratory_capability` is the exploratory-lane
    capability, threaded to the claude-code and api executors. It is never
    required at construction; the EXPLORATORY lane demands it at invocation
    time, when the lane is derived from the actual call.

    Args:
        executor_id: One of "dry-run", "prompt-chain", "claude-code", "api".
        repo_root: Repository root path.
        prompt_output_dir: Directory for prompt files (prompt-chain only).
        model: Explicit model identifier (issue #86). Only meaningful for
            controlled experiments; dry-run/prompt-chain never invoke a model.
        controlled_experiment: When True, requires `model` to be set for
            execution-mode runs -- raises ValueError otherwise.

    Returns:
        A SkillExecutor instance.

    Raises:
        ValueError: If executor_id is unknown, or if controlled_experiment
            is set for "claude-code" with no model.
    """
    if executor_id not in EXECUTOR_REGISTRY:
        known = ", ".join(EXECUTOR_REGISTRY.keys())
        raise ValueError(f"Unknown executor '{executor_id}'. Known: {known}")

    executor_cls = EXECUTOR_REGISTRY[executor_id]

    # Gate A applies to EVERY executor id, and it is evaluated first. The
    # early returns below would otherwise let "prompt-chain" and "dry-run"
    # slip past the check -- a controlled Stage 1 run must not silently
    # downgrade to a non-executing path either.
    if controlled_experiment and executor_id in ("dry-run", "prompt-chain"):
        raise GateAAuthorizationRequired(
            GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED,
            f"executor '{executor_id}' cannot perform a controlled Stage 1 "
            f"invocation; it never invokes a model.",
        )

    if executor_id == "prompt-chain":
        output_dir = prompt_output_dir or os.path.join(repo_root, "prompts")
        return executor_cls(output_dir=output_dir)

    return executor_cls()
