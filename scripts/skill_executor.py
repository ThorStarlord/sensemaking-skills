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

# SDK type imports for error classification
from claude_agent_sdk import ResultMessage, AssistantMessage

# Gate A authorization consumer. Imported by module name because scripts/ is
# already on sys.path for every consumer of this module.
from gate_a_authorization import (  # noqa: E402
    AuthorizedInvocation,
    ExecutionMode,
    GateAError,
    InvocationIdentity,
    GATE_A_AUTHORIZATION_CONSUMER_NOT_CONFIGURED,
    GATE_A_CAPABILITY_NOT_LIVE,
    GATE_A_INVOCATION_CLASSIFICATION_AMBIGUOUS,
    GATE_A_INVOCATION_IDENTITY_MISMATCH,
    GATE_A_MODEL_MISMATCH,
    CONTRACT_ARTIFACT_TYPE,
    classify_invocation,
    format_gate_a_log,
    requires_gate_a,
)


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
) -> ExecutionMode:
    """Fail closed unless a Gate-A-requiring invocation carries a live capability.

    Non-consuming. Called early so the failure happens before any prompt is
    built, any SDK object is constructed, or any provider client exists.

    Returns the derived ``ExecutionMode`` so callers can log what was decided.
    """
    mode, signals = classify_invocation(identity)
    if not requires_gate_a(mode):
        return mode
    why = ",".join(signals) or "none"
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


_EVIDENCE_DIR_RE = re.compile(
    r"experiments[\\/](?:evidence|run-control)[\\/](\d{4})-([A-Za-z0-9._-]+)"
)

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
        match = _EVIDENCE_DIR_RE.search(str(output))
        if match:
            evidence_number = evidence_number or match.group(1)
            evidence_slug = evidence_slug or f"{match.group(1)}-{match.group(2)}"

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


def build_semantic_authorities_block(repo_root: str) -> str:
    """Build the execution-instruction section that injects canonical
    semantic authorities (issue #58).

    This addresses three semantic failures observed in a live run
    (experiments/evidence/0005-runtime-skeleton-live-step1/) that passed
    structural validation but failed downstream: an invented composite
    workflow ID, a fog-type value used where a weakness-type value was
    required, and evidence citations placed only in Sections 8/13 instead of
    also in Section 7's prose.

    The lists below are generated dynamically from the authoritative files
    at call time -- they are never hardcoded here. If the registry or the
    enum file changes, the injected list changes automatically on the next
    call. Raises loudly (does not degrade silently) if either source cannot
    be loaded -- see get_allowed_workflow_ids / get_allowed_weakness_types.
    """
    workflow_ids = get_allowed_workflow_ids(repo_root)
    weakness_types = get_allowed_weakness_types(repo_root)

    workflow_list = "\n".join(f"  - {wid}" for wid in workflow_ids)
    weakness_list = "\n".join(f"  - {wt}" for wt in weakness_types)

    return (
        "## Canonical Semantic Authorities (do not deviate from these)\n\n"
        "**recommended_workflow_id**: choose exactly one ID from this list "
        "(the current top-level workflow IDs in "
        "skills/workflow-planner/references/workflow-registry.yaml):\n"
        f"{workflow_list}\n\n"
        "Never invent an ID and never use a skill ID or a step ID -- only "
        "the top-level workflow IDs above are valid. If uncertain, use the "
        "contract's escalation behavior (escalation_recommended: true) "
        "instead of guessing.\n\n"
        "**weakest_boundary.type / Section 6's 'Weakness type:' line / Section "
        "13's `weakness_type` field**: choose exactly one value from this list "
        "(the current weakness-type enum in "
        "skills/repo-sensemaker/references/weakness-types.md), or `Other` if "
        "none genuinely fit:\n"
        f"{weakness_list}\n"
        "  - Other\n\n"
        "**Structured `weakness_type` field (Section 13, required):** record "
        "the same value you stated in Section 6's `**Weakness type:**` line "
        "in the `weakness_type:` key of Section 13's machine-readable YAML "
        "block -- the two must agree. If you use `Other`, you MUST also fill "
        "`weakness_type_explanation:` with a non-empty string explaining why "
        "no registered type fits; leave it `null` for any recognized type. "
        "An unrecognized `weakness_type` value, a missing `weakness_type` "
        "field, or `Other` without an explanation are non-blocking validator "
        "warnings (they do not fail structural validation), but the brief "
        "still cannot receive final human approval until they are resolved.\n\n"
        "This is NOT the same vocabulary as primary_fog_type (Section 6.5's "
        "product_fog / ui_fog / docs_fog / architecture_fog / mixed / "
        "unknown) -- do not answer the weakness-type question with a "
        "fog-type value, and do not answer the fog-type question with a "
        "weakness-type value. These are three separate fields with three "
        "separate vocabularies: `primary_fog_type` (fog-type enum), "
        "`weakest_boundary`'s type / Section 6's weakness-type line "
        "(weakness-type enum above), and `recommended_workflow_id` "
        "(workflow-ID list above). Do not conflate them.\n\n"
        "**Section 7 (Evidence) file citations**: Section 7's prose itself "
        "must contain at least one literal file-path citation (e.g. "
        "`path/to/file.py:42` or `path/to/file.py` with a line range), even "
        "when Sections 8 and 13 already contain structured evidence "
        "citations. A citation only in Section 8's evidence_excerpts block "
        "or Section 13's evidence: list does NOT satisfy this -- Section 7's "
        "own prose is checked independently.\n\n"
        "**Section 7 logic trace (required)**: Section 7's prose must also "
        "include a paragraph that begins with the literal words `Logic "
        "trace:` and shows the diagnostic reasoning chain connecting the "
        "cited evidence to the weakest-boundary conclusion (which signal, "
        "read in which file, implies which specific failure). The validator "
        "looks for the literal substring \"logic trace\" (case-insensitive) "
        "anywhere in the artifact and fails the whole brief with "
        "NO_LOGIC_TRACE if it is absent -- do not omit this paragraph and do "
        "not paraphrase the marker words away.\n\n"
        "**Section 8 evidence_excerpts required fields**: every item in the "
        "`evidence_excerpts:` YAML list under Section 8 MUST include all "
        "four of these keys, spelled exactly this way -- `file`, `lines`, "
        "`quote`, `supports_claim`. There is no fifth acceptable key name "
        "(e.g. `citation` or `note` do NOT satisfy this -- the validator "
        "checks for `quote` and `supports_claim` literally and raises "
        "EVIDENCE_EXCERPT_FIELD once per missing key, per excerpt, if either "
        "is absent or misnamed):\n"
        "  - `file`: repo-relative path to the cited file.\n"
        "  - `lines`: a single line or range, e.g. `L18` or `L25-L30` (or "
        "bare numbers `18` / `25-30`).\n"
        "  - `quote`: the actual, verbatim text excerpt from that file/line "
        "range -- copy it, do not summarize or describe it.\n"
        "  - `supports_claim`: one sentence stating exactly which claim in "
        "this brief (e.g. which weakest-boundary or missing-piece point) "
        "this quote is evidence for.\n"
        "Example of a correctly-shaped excerpt:\n"
        "```yaml\n"
        "evidence_excerpts:\n"
        "  - file: scripts/validate-brief.py\n"
        "    lines: L312-L314\n"
        '    quote: "for field in [\\"file\\", \\"lines\\", \\"quote\\", \\"supports_claim\\"]:"\n'
        '    supports_claim: "Confirms the validator requires all four named fields per excerpt."\n'
        "```\n"
        "\n"
        f"{build_evidence_discipline_block()}"
    )


def build_evidence_discipline_block() -> str:
    """Build the execution-instruction section requiring a contradiction
    search before any absence/negative claim (issue #74).

    Background: an independent forensic/evidence audit of a live
    repo-sensemaker run (see experiments/evidence/0011-external-repo-auteur-rerun2/
    EVIDENCE.md) found the model asserted a "ghost feature" (a capability
    with "no active diagnostic rules") based on a stale docstring comment,
    while the function body it was citing -- a few hundred lines further
    down, in the SAME function -- already implemented exactly the capability
    the model claimed was absent. The model never searched for evidence that
    would have falsified its own claim, and it treated a comment as more
    authoritative than the executable code it summarized.

    `build_semantic_authorities_block` (issue #58) already governs
    vocabulary (workflow IDs, weakness types) and evidence-excerpt shape
    (issue #71/PR #72), but said nothing about *how thoroughly* an absence
    claim must be investigated before it is written down. This block closes
    that gap. It is intentionally generic -- no repository, project, or
    symbol name is hardcoded here; it applies to any claim of this shape in
    any target repository.

    Deliberately does NOT introduce a new literal marker phrase for
    validate-brief.py (or any other validator) to scan for. PR #72 already
    caught and reverted exactly that trap once (a skeleton comment
    containing the literal "Logic trace:" phrase would have trivially
    satisfied NO_LOGIC_TRACE regardless of what the model wrote) -- adding
    another such trivially-satisfiable marker here would repeat that
    mistake. Instead this instruction is enforced only through prompt
    guidance and the mandatory independent evidence-quality audit; no new
    validator rule is added or required by this fix.
    """
    return (
        "## Evidence Discipline for Absence / Negative Claims (do not skip)\n\n"
        "This applies whenever you are about to write a claim that something "
        "is absent, unimplemented, unreachable, dead, unvalidated, unused, a "
        "\"ghost feature,\" or otherwise does not exist or does not run -- in "
        "any file, function, enum, or module of the target repository. Before "
        "writing such a claim, you must do ALL of the following:\n\n"
        "1. Search for direct implementations of the capability you are about "
        "to claim is missing (not just the one location you already looked "
        "at).\n"
        "2. Search for other usages of the relevant symbol, enum value, "
        "method, or member across the repository -- a member can be "
        "referenced, and implemented, somewhere other than where you first "
        "looked.\n"
        "3. Inspect the callees actually reachable from the entry point you "
        "are citing -- if you are citing a function that calls other "
        "functions, read what those callees do before concluding the entry "
        "point does nothing relevant. You do not need to read every line of "
        "every large file for this -- targeted searches and call-chain "
        "inspection of what is actually reachable from your cited entry "
        "point are sufficient; exhaustive line-by-line reading is not "
        "required.\n"
        "4. Deliberately search for evidence that would prove your claim "
        "wrong, not only evidence that supports it. If you cannot articulate "
        "what such falsifying evidence would look like and confirm you "
        "looked for it, you have not done this step.\n"
        "5. Apply this authority ordering when sources disagree: executable "
        "code and configuration outrank executable tests; executable tests "
        "outrank current documentation; current documentation outranks "
        "comments and docstrings; comments and docstrings outrank plans, "
        "status files, and historical/changelog notes. A comment, docstring, "
        "README line, or status document that says a capability is missing "
        "is the WEAKEST evidence available and must never be the sole basis "
        "for an absence claim.\n"
        "6. Never treat a comment or docstring as conclusive when the "
        "executable code it describes can be directly read and can confirm "
        "or contradict it. If a docstring and the function body it "
        "summarizes disagree, the function body wins.\n"
        "7. If, after reasonable-bounded searching, you cannot complete this "
        "contradiction search (e.g. the reachable call graph is too large or "
        "genuinely ambiguous), you must downgrade your conclusion to stated "
        "uncertainty (e.g. \"appears absent based on X; a full contradiction "
        "search of Y was not completed\") rather than asserting the absence "
        "as settled fact.\n"
        "8. Record what you searched for and what you did or did not find "
        "that could have falsified your claim as part of your evidence "
        "reasoning -- this disconfirmation work is part of the diagnostic "
        "reasoning chain the artifact requires, not a separate optional "
        "step.\n\n"
        "This evidence-discipline requirement does not replace or weaken the "
        "quote/supports_claim/logic-trace requirements above -- it governs "
        "the standard of care that must be met before an absence claim is "
        "written into evidence at all, whatever workflow, repository, or "
        "vocabulary is in play.\n"
    )


def build_yaml_fence_contract_block() -> str:
    """Build the execution-instruction section enforcing the exact YAML fence
    syntax for the architectural_review_recommendation artifact (issue: exact
    triple-backtick YAML fence in architectural-review recommendation).

    A live architectural-review run produced an otherwise substantive
    recommendation but fenced its authoritative machine-readable YAML block
    with `~~~yaml` instead of the required ```` ```yaml ```` triple-backtick
    fence. scripts/validate-architectural-review-recommendation.py's
    _parse_artifact_data (see that file) only recognizes the exact regex
    ``` ```yaml\\s+(.*?)\\s+``` ``` -- a tilde fence does not match, so the
    validator reports PARSING_ERROR even though the recommendation content
    itself was on-topic and substantive. This block makes the required exact
    syntax unambiguous to the model so it cannot silently substitute an
    equally-valid-looking Markdown fence style that this validator does not
    accept.

    This is a producer-side instruction only -- it does not change what the
    validator accepts.
    """
    return (
        "## Machine-readable YAML Block: Exact Fence Syntax (do not deviate)\n\n"
        "The artifact must contain EXACTLY ONE authoritative machine-readable "
        "YAML block, fenced with the EXACT syntax below:\n\n"
        "- Opening fence: exactly three backticks immediately followed by "
        "`yaml`, i.e. ` ```yaml ` (NOT `~~~yaml`, NOT `~~~`, NOT four or more "
        "backticks, NOT a language other than `yaml`).\n"
        "- Closing fence: exactly three backticks, i.e. ` ``` ` (NOT `~~~`).\n"
        "- Do NOT use tilde fences (`~~~yaml` / `~~~`) anywhere in this "
        "artifact -- the validator's parser only recognizes the triple-"
        "backtick form and treats a tilde-fenced block as if no YAML block "
        "were present at all, which fails the artifact with a parsing error.\n"
        "- Do NOT emit the machine-readable data as plain (unfenced) YAML, "
        "as JSON, or as more than one fenced machine-readable block. Exactly "
        "one ```yaml ... ``` block is required, and it is the only block "
        "the validator reads.\n\n"
        "Example of the ONLY acceptable fence syntax:\n"
        "```yaml\n"
        "decision: pursue\n"
        "confidence: high\n"
        "```\n"
    )


# ============================================================================
# Output path resolution (shared by real executors)
# ============================================================================

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
# Session-root artifact-write confinement (issue #43)
# ============================================================================
#
# create-artifact.py's own overwrite guard (PR #41 / issue #40) only stops a
# collision with an EXISTING tracked file. A fresh path outside the active
# session is not caught by anything: nothing checks WHERE expected_output_path
# is honored, only whether it exists once written. This section closes that
# gap for the Claude Agent SDK executor by making runtime artifact writes
# structurally confined, not just contract-conformant.
#
# Mechanism: a `PreToolUse` hook, not `can_use_tool`. The SDK's own contract
# (claude_agent_sdk.types.ClaudeAgentOptions.can_use_tool docstring) states
# can_use_tool is only invoked for tool calls that would otherwise prompt the
# user -- it is never invoked for a tool already permitted by allowed_tools.
# Since Write/Bash/etc. are named in allowed_tools below, can_use_tool would
# never fire for them and would be a fake gate. A PreToolUse hook with
# matcher=None is documented to observe/gate every tool call regardless of
# allowed_tools/permission_mode, which is what "structural confinement"
# requires.


def canonicalize_path(path: str) -> str:
    """Canonicalize a path for authorization comparison.

    Resolves to an absolute, symlink/junction-resolved, case-normalized form
    so that two different spellings of the same on-disk location (relative
    vs. absolute, mixed drive-letter case, a symlinked ancestor, a `..`
    traversal) compare equal, while genuinely different locations never do.

    Deliberately NOT a string-prefix check: a prefix match would treat
    "artifacts/100-run-2" as inside "artifacts/100-run" and is defeated by
    ".." components without normalization first.

    `os.path.realpath` resolves symlinks/junctions for whatever prefix of the
    path currently exists on disk; for a not-yet-created final path
    component (the common case -- the artifact doesn't exist yet) there is
    nothing to resolve for that component, so it is carried through
    unchanged. That is correct here: authorization is about *where* the
    write will land, and only existing ancestor directories can be
    symlinked into another location.
    """
    resolved = os.path.realpath(os.path.abspath(os.path.normpath(path)))
    return os.path.normcase(resolved)


def is_within_root(path: str, root: str) -> bool:
    """True iff canonicalized `path` is `root` itself or strictly beneath it.

    Uses os.path.commonpath on already-canonicalized inputs, not a string
    prefix check: a prefix check would treat "...\\run-1-evil" as inside
    "...\\run-1" and would not catch a symlinked/junctioned ancestor that
    canonicalizes both the "authorized" path and a rogue path to the same
    place outside the intended root (the exact gap this closes -- an
    ancestor of expected_output_path that has been redirected relocates the
    entire "authorized" destination, so equality-with-itself proves nothing;
    only independent containment in a separately-trusted root does).
    """
    try:
        return os.path.commonpath([path, root]) == root
    except ValueError:
        # Different drives on Windows, or otherwise not comparable.
        return False


# Tools this executor ever grants to the model. Anything not read-only or not
# the single artifact-writing tool is denied by the hook below, whether or
# not it is also excluded from allowed_tools -- the hook is the authority,
# allowed_tools is defense-in-depth on top of it.
_READ_ONLY_TOOLS = frozenset({"Read", "Glob", "Grep"})
_ARTIFACT_WRITE_TOOL = "Write"


def _deny(message: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": message,
        }
    }


def _allow() -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
        }
    }


def build_artifact_permission_gate(
    expected_output_path: Optional[str],
    artifact_session_dir: Optional[str] = None,
):
    """Build a PreToolUse hook callback confining writes to expected_output_path.

    Closed over two runtime-owned values for one invocation (neither ever
    supplied by the model):
      - expected_output_path: the exact file the write must target.
      - artifact_session_dir: the session root expected_output_path must be
        contained in.

    Equality with expected_output_path alone is NOT sufficient authorization:
    if an ancestor directory of expected_output_path is a symlink/junction
    that redirects outside the session root, the requested path and the
    "authorized" path canonicalize to the same (relocated) place and would
    pass an equality-only check while actually writing outside the session.
    Proving containment in an independently-trusted root closes that gap --
    the root must come from runtime state, never be inferred from
    expected_output_path itself.

    Missing/empty expected_output_path, OR missing/empty artifact_session_dir,
    OR an expected_output_path that does not canonically resolve inside the
    canonical session root, all fail closed: every mutating tool call is
    denied, since there is nothing trustworthy to authorize against.

    Returned callable matches the SDK's HookCallback signature:
    (input_data: dict, tool_use_id: str | None, context: HookContext) -> Awaitable[dict]
    """
    authorized_canonical: Optional[str] = None
    if expected_output_path and artifact_session_dir:
        expected_canonical = canonicalize_path(expected_output_path)
        root_canonical = canonicalize_path(artifact_session_dir)
        if is_within_root(expected_canonical, root_canonical):
            authorized_canonical = expected_canonical

    async def artifact_permission_gate(input_data, tool_use_id, context):
        tool_name = input_data.get("tool_name")
        tool_input = input_data.get("tool_input") or {}

        if tool_name in _READ_ONLY_TOOLS:
            return _allow()

        if tool_name == _ARTIFACT_WRITE_TOOL:
            if authorized_canonical is None:
                return _deny(
                    "No authorized artifact destination for this invocation "
                    "(expected_output_path/artifact_session_dir missing, or "
                    "expected_output_path does not resolve inside the session "
                    "root); refusing all writes (fail-closed)."
                )
            file_path = tool_input.get("file_path")
            if not isinstance(file_path, str) or not file_path.strip():
                return _deny(
                    "Write call is missing a valid file_path; refusing (fail-closed)."
                )
            if canonicalize_path(file_path) != authorized_canonical:
                return _deny(
                    f"Write to '{file_path}' is not the runtime-authorized artifact "
                    f"path. This invocation may only write to: {expected_output_path}"
                )
            return _allow()

        return _deny(
            f"Tool '{tool_name}' is not permitted during runtime-owned artifact "
            f"writes. Only {sorted(_READ_ONLY_TOOLS)} and "
            f"'{_ARTIFACT_WRITE_TOOL}' (to the authorized path) are allowed."
        )

    return artifact_permission_gate


# ============================================================================
# Tool-call trace logging (Phase 4, issue #55; extended for observability v2,
# issue tracked separately -- see docs/adr and the trace-observability issue)
# ============================================================================
#
# Live runs (like PR #54's) had no transcript to inspect after the fact --
# only the final artifact (or its absence). These hooks record every tool
# call the model makes during a skill invocation to a session-scoped JSONL
# file so a failed run can be diagnosed from evidence instead of guesswork.
#
# v1 (PR #57) recorded only: timestamp, event, tool_name, file_path,
# decision. A forensic review of PR #73's evidence
# (experiments/evidence/0011-external-repo-auteur-rerun2/EVIDENCE.md) needed
# to answer "did a write attempt targeting the target clone recur, and did
# it complete" -- v1's fields were *just* barely sufficient to answer that
# one question by manually diffing Pre/PostToolUse pairs, but could not
# answer: what Grep query was used, what Read range was requested, whether
# a result was truncated, or whether contradicting evidence was ever shown
# to the model. This section (schema_version 2) closes that gap.
#
# Deliberately NOT logged: credentials or environment-variable values,
# unrestricted model prompts, entire tool outputs by default, or full
# private repository contents. Values that look secret-like are redacted;
# everything else is bounded metadata (paths, ranges, patterns, sizes) or a
# hash, never a full file/result body.

TRACE_SCHEMA_VERSION = 2

# Bound any single string field written to the trace (query text, patterns,
# etc.) so a single call can never balloon the trace file or leak an entire
# file body through, say, an oversized Grep pattern.
_MAX_TRACE_STRING = 200

# Values that look like secrets/credentials are redacted rather than logged,
# even though tool_input in general is not logged verbatim -- this guards
# the bounded fields we DO extract (e.g. a Grep pattern) against
# accidentally containing an embedded secret-like token.
_SECRET_LIKE_RE = re.compile(
    r"(?i)(api[_-]?key|secret|token|password|bearer\s+[a-z0-9._-]+|"
    r"sk-[a-z0-9]{16,}|ghp_[a-z0-9]{20,}|aws_[a-z0-9_]{16,})"
)


def _redact(value: str) -> str:
    """Return value unchanged unless it looks secret-like, in which case
    return a fixed redaction marker instead of the raw text."""
    if _SECRET_LIKE_RE.search(value):
        return "[REDACTED:secret-like-value]"
    return value


def _bounded_str(value, max_len: int = _MAX_TRACE_STRING) -> Optional[dict]:
    """Convert an arbitrary tool_input value to a bounded, redacted,
    truncation-flagged representation safe to embed in the trace.

    Returns None for values that aren't a plain string (so callers can
    decide whether to omit the field entirely rather than log a confusing
    non-string placeholder).
    """
    if not isinstance(value, str):
        return None
    redacted = _redact(value)
    truncated = len(redacted) > max_len
    return {
        "value": redacted[:max_len],
        "truncated": truncated,
    }


def _hash_str(value: str) -> str:
    """Stable, non-reversible fingerprint for a string field, used when the
    caller wants correlation/dedup without ever writing the raw text (e.g.
    an especially sensitive-looking Grep pattern)."""
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()[:16]


def _result_metadata(tool_response) -> dict:
    """Derive bounded, safe metadata about a tool's result for PostToolUse --
    never the full result content itself.

    Handles the SDK's tool_response shapes defensively: a plain string, a
    dict with a "content" key (text or list-of-blocks), or anything else
    (falls back to a type name only).
    """
    text: Optional[str] = None
    if isinstance(tool_response, str):
        text = tool_response
    elif isinstance(tool_response, dict):
        content = tool_response.get("content")
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            parts = []
            for block in content:
                if isinstance(block, dict) and isinstance(block.get("text"), str):
                    parts.append(block["text"])
            if parts:
                text = "\n".join(parts)
        is_error = tool_response.get("is_error")
        if is_error:
            return {"result_status": "error", "result_size": 0, "result_truncated": False}

    if text is None:
        return {"result_status": "unknown", "result_size": None, "result_truncated": False}

    return {
        "result_status": "ok",
        "result_size": len(text),
        "result_line_count": text.count("\n") + 1 if text else 0,
        # A heuristic, not a guarantee: the SDK/CLI truncates some tool
        # outputs and commonly signals it with a trailing marker string;
        # absence of the marker does not prove the result is complete, but
        # presence is a strong positive signal worth recording.
        "result_truncated": "..." in text[-40:] or "[truncated]" in text.lower(),
    }


def _tool_metadata(tool_name: Optional[str], tool_input: dict) -> dict:
    """Extract bounded, tool-specific structured metadata for the trace.

    Only ever derives metadata (paths, ranges, patterns, bounded/redacted
    strings) -- never logs a full file body or full tool output.
    """
    meta: dict = {}
    file_path = tool_input.get("file_path") if isinstance(tool_input, dict) else None
    if isinstance(file_path, str) and file_path:
        meta["target_path"] = os.path.normcase(os.path.normpath(file_path))

    if tool_name == "Read":
        offset = tool_input.get("offset")
        limit = tool_input.get("limit")
        if offset is not None:
            meta["read_offset"] = offset
        if limit is not None:
            meta["read_limit"] = limit

    elif tool_name == "Grep":
        pattern = tool_input.get("pattern")
        if isinstance(pattern, str):
            bounded = _bounded_str(pattern)
            if bounded is not None:
                meta["grep_pattern"] = bounded["value"]
                meta["grep_pattern_truncated"] = bounded["truncated"]
                meta["grep_pattern_hash"] = _hash_str(pattern)
        glob_filter = tool_input.get("glob")
        if isinstance(glob_filter, str):
            meta["grep_glob_filter"] = glob_filter[:_MAX_TRACE_STRING]

    elif tool_name == "Glob":
        pattern = tool_input.get("pattern")
        if isinstance(pattern, str):
            meta["glob_pattern"] = pattern[:_MAX_TRACE_STRING]

    elif tool_name == "Write":
        # target_path (above) already captures the destination; nothing
        # additional to add here beyond what every event gets.
        pass

    return meta


def _trace_event(
    event: str,
    tool_name: Optional[str],
    file_path: Optional[str],
    decision: str,
    invocation_id: Optional[str] = None,
    extra: Optional[dict] = None,
) -> dict:
    entry = {
        "schema_version": TRACE_SCHEMA_VERSION,
        "timestamp": datetime.now().isoformat(),
        "event": event,  # PreToolUse | PostToolUse
        "tool_name": tool_name,
        "file_path": file_path,
        "decision": decision,  # observed | allow | deny | completed | error
        "invocation_id": invocation_id,  # correlates a PreToolUse with its PostToolUse
    }
    if extra:
        entry.update(extra)
    return entry


def build_tool_trace_hooks(trace_log: list, expected_output_path: Optional[str] = None):
    """Build PreToolUse/PostToolUse hook callbacks that append to `trace_log`.

    `trace_log` is a plain list the caller owns and writes to disk after the
    invocation completes -- these hooks never touch disk themselves so a
    crash mid-run still leaves the caller with whatever was appended so far.

    Each PreToolUse/PostToolUse pair for the same tool call shares
    `invocation_id` (the SDK-provided `tool_use_id`), so a consumer can
    reconstruct exactly which PostToolUse (if any) completed a given
    PreToolUse -- and, just as importantly, detect when a PreToolUse has NO
    matching PostToolUse at all (the exact PR #73 near-miss shape: a
    target-directed Write observed at PreToolUse with nothing completing
    it).
    """

    async def pre_trace(input_data, tool_use_id, context):
        tool_name = input_data.get("tool_name")
        tool_input = input_data.get("tool_input") or {}
        file_path = tool_input.get("file_path") if isinstance(tool_input, dict) else None
        is_expected_write = bool(
            expected_output_path and file_path and tool_name in ("Write", "Edit")
            and os.path.abspath(file_path) == os.path.abspath(expected_output_path)
        )
        extra = dict(_tool_metadata(tool_name, tool_input if isinstance(tool_input, dict) else {}))
        if file_path:
            extra["targets_expected_artifact"] = is_expected_write
        trace_log.append(_trace_event(
            "PreToolUse", tool_name, file_path, "observed",
            invocation_id=tool_use_id,
            extra=extra or None,
        ))
        # This hook only observes; build_artifact_permission_gate is the
        # authoritative allow/deny decision. Returning {} lets that other
        # PreToolUse hook (registered alongside this one) make the call.
        return {}

    async def post_trace(input_data, tool_use_id, context):
        tool_name = input_data.get("tool_name")
        tool_input = input_data.get("tool_input") or {}
        file_path = tool_input.get("file_path") if isinstance(tool_input, dict) else None
        tool_response = input_data.get("tool_response")
        extra = dict(_tool_metadata(tool_name, tool_input if isinstance(tool_input, dict) else {}))
        extra.update(_result_metadata(tool_response))
        trace_log.append(_trace_event(
            "PostToolUse", tool_name, file_path, "completed",
            invocation_id=tool_use_id,
            extra=extra or None,
        ))
        return {}

    return pre_trace, post_trace


def find_unpaired_pretooluse_events(trace_log: list) -> list[dict]:
    """Return every PreToolUse event in trace_log that has no matching
    PostToolUse event with the same invocation_id.

    This is the detector for exactly the PR #73 near-miss shape: a
    target-directed Write (or any tool) observed at PreToolUse with no
    completion recorded anywhere in the trace, whether because it was
    denied, because the process crashed mid-call, or for any other reason.
    Falls back to matching by (tool_name, file_path) when invocation_id is
    absent (e.g. hand-authored/older-schema fixtures), since schema_version
    1 traces predate invocation_id and may still need auditing.
    """
    posts_by_id = set()
    posts_by_shape = set()
    for entry in trace_log:
        if entry.get("event") == "PostToolUse":
            inv_id = entry.get("invocation_id")
            if inv_id:
                posts_by_id.add(inv_id)
            posts_by_shape.add((entry.get("tool_name"), entry.get("file_path")))

    unpaired = []
    for entry in trace_log:
        if entry.get("event") != "PreToolUse":
            continue
        inv_id = entry.get("invocation_id")
        if inv_id:
            if inv_id not in posts_by_id:
                unpaired.append(entry)
        else:
            if (entry.get("tool_name"), entry.get("file_path")) not in posts_by_shape:
                unpaired.append(entry)
    return unpaired


def write_tool_trace(trace_log: list, session_dir: Optional[str], repo_root: str) -> Optional[str]:
    """Write the accumulated trace to a session-scoped JSONL file. Returns the path written, or None."""
    if not trace_log:
        return None
    target_dir = session_dir or os.path.join(repo_root, "artifacts")
    try:
        os.makedirs(target_dir, exist_ok=True)
        trace_path = os.path.join(target_dir, "tool-call-trace.jsonl")
        with open(trace_path, "a", encoding="utf-8") as f:
            for entry in trace_log:
                f.write(json.dumps(entry, default=str) + "\n")
        return trace_path
    except OSError:
        return None


# ============================================================================
# Status Enum
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

class ClaudeAgentSdkSkillExecutor(_GateAImmutableAttributes, SkillExecutor):
    """Invoke skills via Claude Agent SDK.

    Uses the Claude Agent SDK's query() API to invoke skills with autonomous
    tool use. The SDK handles skill discovery from filesystem, tool loops,
    file management, and permissions.

    The executor bridges the synchronous SkillExecutor interface to the
    async Claude Agent SDK using anyio.run().
    """

    supports_real_execution: bool = True

    def __init__(
        self,
        repo_root: str,
        model: Optional[str] = None,
        controlled_experiment: bool = False,
        authorization: Optional[AuthorizedInvocation] = None,
        invocation_identity: Optional[InvocationIdentity] = None,
    ):
        """
        Args:
            repo_root: Repository root path.
            authorization: Gate A capability. REQUIRED when
                controlled_experiment is True -- the constructor refuses to
                build an executor that could reach query() without one, and
                invoke_skill/_invoke_skill_async re-check and consume it at
                the provider boundary.
            model: Explicit model identifier passed straight through as
                ClaudeAgentOptions(model=...) (issue #86). None preserves
                today's ambient/default-model behavior.
            controlled_experiment: When True, `model` is required -- this
                constructor raises ValueError immediately (before any SDK
                call, before even a query() is built) if model is missing.
                This is the innermost enforcement layer; workflow-runtime.py
                also checks this before constructing the executor at all.
        """
        self.repo_root = repo_root
        self._check_dependencies()

        if controlled_experiment and not model:
            raise ValueError(
                "controlled_experiment=True requires an explicit model "
                "identifier (issue #86): no model was supplied. Refusing to "
                "construct an executor that could invoke the SDK with an "
                "ambient/default model in a controlled-experiment run."
            )
        if model is not None:
            validate_model_identifier(model)

        self.model = model
        # Declared mode is informational metadata only. See
        # _GateAImmutableAttributes.controlled_experiment.
        self._declared_controlled_experiment = bool(controlled_experiment)
        self._invocation_identity = invocation_identity or build_invocation_identity(
            repo_root=repo_root,
            executor_id="claude-code",
            model=model,
            declared_controlled_mode=(True if controlled_experiment else None),
        )

        # Gate A, outermost layer: refuse to even construct an executor that
        # could reach the SDK without a live capability, when the identity
        # known at construction already requires one.
        require_authorization_capability(
            authorization,
            identity=self._invocation_identity,
            model=model,
            executor_name="ClaudeAgentSdkSkillExecutor",
        )
        self.authorization = authorization

    def _actual_identity(self, skill_id, expected_output_artifact,
                         context) -> InvocationIdentity:
        """Identity of the invocation being performed right now.

        Built from the call arguments every time. Deliberately does NOT trust
        stored executor state for the classification-bearing fields, so
        mutating the executor after construction cannot change what Gate A
        thinks is happening.
        """
        return build_invocation_identity(
            repo_root=self.repo_root,
            executor_id="claude-code",
            skill_id=skill_id,
            expected_output_artifact=expected_output_artifact,
            context=context,
            model=self.model,
            declared_controlled_mode=(
                True if self.__dict__.get("_declared_controlled_experiment")
                else None
            ),
        )

    def _check_dependencies(self) -> tuple[bool, str]:
        """Check if required dependencies are installed."""
        missing = []
        try:
            import anyio
        except ImportError:
            missing.append("anyio")

        try:
            from claude_agent_sdk import query, ClaudeAgentOptions
        except ImportError:
            missing.append("claude-agent-sdk")

        return len(missing) == 0, missing

    def build_skeleton_prompt(
        self, skill_id: str, input_section: str, relative_output_path: str
    ) -> str:
        """Build the execution instruction sent to the model for the
        runtime-owned-skeleton path (repository_sensemaking_brief only).

        Extracted to its own method so tests can inspect the exact prompt
        string this executor constructs (including the dynamically-injected
        semantic-authorities block, issue #58) without invoking the async
        Claude Agent SDK call. This proves what is BUILT, not that it was
        DELIVERED over the wire to the SDK -- the actual query() call is
        exercised only by the live Step 1 rerun, tracked separately.
        """
        semantic_authorities_block = build_semantic_authorities_block(self.repo_root)
        return (
            f"You are executing the '{skill_id}' skill as part of a structured workflow.\n\n"
            f"{input_section}"
            f"## Your Task\n"
            f"A runtime-owned artifact skeleton already exists at:\n"
            f"```\n{relative_output_path}\n```\n\n"
            f"Read it first. It already contains the required headings and the "
            f"machine-readable YAML fence with runtime-owned fields "
            f"(artifact_id, schema_version, source_intent_ref, created_at, "
            f"immutable) filled in -- do NOT try to recreate or reorder those.\n\n"
            f"## Your only job\n"
            f"Fill in the content between each `<!-- MODEL_SECTION:<name>:BEGIN -->` "
            f"/ `<!-- MODEL_SECTION:<name>:END -->` marker pair with your analysis, "
            f"and fill in the placeholder YAML fields in Section 13 "
            f"(user_implied_fog_type, primary_fog_type, diagnosis_conflict, "
            f"escalation_recommended, evidence, recommended_workflow_id, "
            f"recommended_execution_mode, weakest_boundary) and the "
            f"evidence_excerpts YAML block under Section 8.\n\n"
            f"{semantic_authorities_block}\n"
            f"Use the Write tool, writing the FULL file content back to the exact "
            f"path above (with your filled-in sections/fields, keeping the marker "
            f"comments and the existing headings/fence in place). Do not invent a "
            f"different structure. Do not stop until you have written that file."
        )

    def invoke_skill(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        """Invoke a skill via Claude Agent SDK.

        Returns EXECUTED only if the expected artifact file exists after execution.
        Returns UNSUPPORTED if dependencies are missing.
        """
        # Gate A, fail-fast layer. Non-consuming: the capability is spent at
        # the provider boundary in _invoke_skill_async, immediately before
        # query(). This check exists so a controlled invocation with no
        # capability dies before any prompt is built or SDK object exists.
        try:
            require_authorization_capability(
                self.authorization,
                identity=self._actual_identity(
                    skill_id, expected_output_artifact, context
                ),
                model=self.model,
                executor_name="ClaudeAgentSdkSkillExecutor.invoke_skill",
            )
        except GateAAuthorizationRequired as gate_error:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.FAILED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                requested_model=self.model,
                error=f"{gate_error.code}: {gate_error.detail}",
                message="Gate A denied: no model invocation was attempted.",
            )

        deps_ok, missing_deps = self._check_dependencies()
        if not deps_ok:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.UNSUPPORTED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"Missing dependencies: {', '.join(missing_deps)}. "
                      f"Install with: pip install {' '.join(missing_deps)}",
            )

        # Bridge to async SDK using anyio
        try:
            import anyio
            result = anyio.run(
                self._invoke_skill_async,
                skill_id,
                invocation_command,
                input_artifacts,
                expected_output_artifact,
                context,
            )
            return result
        except Exception as e:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.FAILED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"Skill execution failed: {str(e)}",
            )

    async def _invoke_skill_async(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        """Async implementation of skill invocation via Claude Agent SDK."""
        from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

        # Build prompt that instructs Claude to run the skill
        resolved_inputs = context.get("resolved_inputs", {})

        # Format input information for the prompt
        input_section = ""
        if resolved_inputs:
            input_section = "## Input Data\n"
            for input_name, input_data in resolved_inputs.items():
                if input_data["type"] == "external_context":
                    input_section += f"\n**{input_name}:**\n```\n{input_data['data']}\n```\n"
                elif input_data["type"] == "artifact_path":
                    input_section += f"\n**{input_name}** (artifact file):\n{input_data['path']}\n"
                elif input_data["type"] == "repository_state":
                    input_section += f"\n**{input_name}:**\nRepository root: {input_data['data'].get('path', '.')}\n"
            input_section += "\n"

        # Expected output path — use the runtime-resolved (session-scoped) path so
        # the artifact lands where the runtime will look for it.
        expected_output_path = resolve_output_path(self.repo_root, expected_output_artifact, context)
        relative_output_path = os.path.relpath(expected_output_path, self.repo_root)

        # Session root the expected_output_path must be contained in (issue #43
        # follow-up): equality with expected_output_path alone doesn't prove the
        # write lands inside the session, because a symlinked/junctioned ancestor
        # of expected_output_path could redirect the "authorized" path itself
        # outside the session root -- both the requested and authorized paths
        # would then canonicalize equal to each other while landing elsewhere.
        # artifact_session_dir is runtime-owned state (OrchestrationRunner sets
        # it, never the model); when the runtime is not driving this invocation
        # (e.g. standalone/manual executor use with no session), fall back to
        # this executor's own repo_root/artifacts, which is likewise never
        # model-supplied.
        artifact_session_dir = context.get("artifact_session_dir") or os.path.join(
            self.repo_root, "artifacts"
        )

        # --- Runtime-owned skeleton (issue #55) ---------------------------------
        # For repository_sensemaking_brief specifically, the runtime pre-creates
        # the canonical artifact envelope at expected_output_path *before* the
        # model ever runs, and reconciles whatever the model produced back into
        # that envelope afterward. See scripts/brief_skeleton.py for why: PR #54
        # showed a free-form model cannot reliably reproduce deterministic
        # artifact grammar (the YAML fence was omitted entirely in that run).
        # Other artifact types are unaffected -- this is scoped to the one
        # artifact issue #55 targets, not a general renderer (Architecture 3).
        uses_runtime_skeleton = expected_output_artifact == brief_skeleton.ARTIFACT_ID
        skeleton_ctx = None
        if uses_runtime_skeleton:
            skeleton_ctx = brief_skeleton.SkeletonContext(
                source_intent_ref=context.get("source_intent_ref", brief_skeleton.SkeletonContext().source_intent_ref),
            )
            os.makedirs(os.path.dirname(expected_output_path), exist_ok=True)
            with open(expected_output_path, "w", encoding="utf-8") as f:
                f.write(brief_skeleton.build_skeleton(skeleton_ctx))

        if uses_runtime_skeleton:
            prompt = self.build_skeleton_prompt(skill_id, input_section, relative_output_path)
        else:
            # architectural-review's authoritative output (architectural_review_
            # recommendation) is validated by
            # scripts/validate-architectural-review-recommendation.py, which
            # requires an exact triple-backtick ```yaml fence (see
            # build_yaml_fence_contract_block's docstring for the live-run
            # failure this addresses). Inject that exact-syntax requirement
            # for this skill specifically, the same pattern
            # build_semantic_authorities_block uses for repo-sensemaker.
            fence_contract_block = ""
            if skill_id == "architectural-review":
                fence_contract_block = "\n" + build_yaml_fence_contract_block() + "\n"

            prompt = (
                f"You are executing the '{skill_id}' skill as part of a structured workflow.\n\n"
                f"{input_section}"
                f"## Your Task\n"
                f"Use the/{skill_id} slash command or the skill definition to produce the required output.\n\n"
                f"## Output Artifact (REQUIRED)\n"
                f"You MUST write the final artifact to this exact path:\n"
                f"```\n{relative_output_path}\n```\n\n"
                f"Use the Write tool to create this file. The artifact must be markdown format (.md) "
                f"and must match the expected output format for this skill.\n"
                f"{fence_contract_block}"
                f"\nDo not stop until the artifact file exists at the specified path."
            )

        # Capture SDK result and error info for diagnostic classification
        sdk_last_result_info: str | None = None

        # Model-enforcement evidence (issue #86): every distinct
        # AssistantMessage.model value observed during this invocation, in
        # first-seen order. Populated regardless of whether a model was
        # requested, so ambient/default runs also get a durable record of
        # what actually ran.
        reported_models: list[str] = []

        # Runtime artifact-write confinement (issue #43): the PreToolUse hook below
        # is the authoritative enforcement point (see build_artifact_permission_gate).
        # allowed_tools is narrowed too, as defense-in-depth on top of the hook, not
        # as the enforcement mechanism itself -- can_use_tool would have been a fake
        # gate here since Write/Bash would already be pre-permitted by allowed_tools.
        artifact_permission_gate = build_artifact_permission_gate(
            expected_output_path, artifact_session_dir
        )

        # Tool-call trace (Phase 4, issue #55): observes every tool call this
        # invocation makes without changing any allow/deny decision.
        trace_log: list = []
        pre_trace, post_trace = build_tool_trace_hooks(trace_log, expected_output_path)
        trace_log.append(_trace_event(
            "SkillInvocation", skill_id, expected_output_path, "started",
            extra={"uses_runtime_skeleton": uses_runtime_skeleton},
        ))

        # ------------------------------------------------------------------
        # Gate A, binding layer. This is the narrowest boundary: the last
        # statement before the provider call itself. consume() re-reads the
        # authorization record, digest file, owner approval, package and
        # checklist bytes, and both repository HEADs, and compares them to the
        # snapshot taken at validation time (TOCTOU). It raises -- it does not
        # return a value an intermediate caller could discard -- and it marks
        # the capability spent so no second invocation is possible.
        # ------------------------------------------------------------------
        actual_identity = self._actual_identity(
            skill_id, expected_output_path, context
        )
        gate_a_mode = require_authorization_capability(
            self.authorization,
            identity=actual_identity,
            model=self.model,
            executor_name="ClaudeAgentSdkSkillExecutor._invoke_skill_async",
        )
        if requires_gate_a(gate_a_mode):
            gate_a_decision = self.authorization.consume(
                model=self.model,
                artifact_type=self.authorization.artifact_type,
                actual_identity=actual_identity,
            )
            trace_log.append(_trace_event(
                "GateAAuthorization", skill_id, expected_output_path, "consumed",
                extra={
                    "gate_a": format_gate_a_log(gate_a_decision),
                    "execution_mode": gate_a_mode.value,
                },
            ))

        try:
            # Query the Claude Agent SDK
            async for message in query(
                prompt=prompt,
                options=ClaudeAgentOptions(
                    cwd=self.repo_root,
                    setting_sources=["project", "user"],
                    skills=[skill_id],
                    allowed_tools=["Read", "Write", "Glob", "Grep"],
                    # Explicit model pin (issue #86). None (the default)
                    # preserves today's ambient/default-model behavior --
                    # this is never a hidden global default, only whatever
                    # the caller explicitly supplied. fallback_model is
                    # deliberately never set anywhere in this executor: no
                    # fallback, retry, or escalation is introduced.
                    model=self.model,
                    hooks={
                        "PreToolUse": [
                            HookMatcher(matcher=None, hooks=[artifact_permission_gate, pre_trace]),
                        ],
                        "PostToolUse": [
                            HookMatcher(matcher=None, hooks=[post_trace]),
                        ],
                    },
                ),
            ):
                # Capture ResultMessage error info for classification
                if isinstance(message, ResultMessage):
                    if message.is_error:
                        errors_text = "; ".join(str(e) for e in (message.errors or []))
                        sdk_last_result_info = errors_text or str(message.subtype)

                # Record every AssistantMessage.model value observed (issue
                # #86 requirement 7): this is the SDK's only per-message
                # report of which model actually ran (ClaudeAgentOptions and
                # ResultMessage do not carry a single "the model used" field).
                if isinstance(message, AssistantMessage):
                    reported_model = getattr(message, "model", None)
                    trace_log.append(_trace_event(
                        "AssistantMessage", None, None, "observed",
                        extra={"reported_model": reported_model},
                    ))
                    if reported_model:
                        reported_models.append(reported_model)

            # For the runtime-skeleton path, reconcile whatever the model wrote
            # (if anything) back into the canonical envelope. This is the
            # enforcement point described in brief_skeleton.reconcile(): the
            # envelope survives even if the model wrote nothing, malformed
            # content, or attempted a full-file replacement.
            handoff_yaml_valid = True
            handoff_yaml_invalid_reason: Optional[str] = None
            if uses_runtime_skeleton:
                model_raw = ""
                if os.path.exists(expected_output_path):
                    with open(expected_output_path, encoding="utf-8") as f:
                        model_raw = f.read()
                target_repo_root = context.get("target_repo") or self.repo_root
                reconciled = brief_skeleton.reconcile(
                    model_raw,
                    skeleton_ctx,
                    target_root=target_repo_root,
                    framework_root=self.repo_root,
                )
                with open(expected_output_path, "w", encoding="utf-8") as f:
                    f.write(reconciled)
                # `integrity_ok` here is a structural check ONLY (markers,
                # headings, artifact_id present as text) -- see
                # brief_skeleton.skeleton_integrity_ok's docstring. It does
                # NOT prove Section 13's YAML is parseable, which is exactly
                # how Evidence 0014 shipped a HANDOFF_YAML_PARSE_ERROR
                # artifact alongside `integrity_ok: true`. The separate
                # `handoff_yaml_valid` field is the actual round-trip
                # parseability guarantee and is what gates artifact
                # acceptance below.
                handoff_yaml_valid, handoff_yaml_invalid_reason = brief_skeleton.handoff_yaml_round_trips(reconciled)
                trace_log.append(_trace_event(
                    "Reconciliation", "brief_skeleton.reconcile", expected_output_path,
                    "ok" if handoff_yaml_valid else "hard_stop",
                    extra={
                        "integrity_ok": brief_skeleton.skeleton_integrity_ok(reconciled),
                        "handoff_yaml_valid": handoff_yaml_valid,
                        "handoff_yaml_invalid_reason": handoff_yaml_invalid_reason,
                    },
                ))

            # Model-enforcement decision (issue #86). Computed unconditionally
            # so ambient (model=None) runs still get reported_models recorded,
            # but the hard-stop only applies when a model was requested --
            # there is nothing to "match" for an ambient run.
            distinct_reported = list(dict.fromkeys(reported_models))  # de-dup, preserve order
            model_match: Optional[bool] = None
            model_enforcement_detail = ""
            if self.model:
                if not distinct_reported:
                    model_match = False
                    model_enforcement_detail = (
                        "no AssistantMessage.model was observed; cannot confirm the "
                        "requested model was honored"
                    )
                elif len(distinct_reported) > 1:
                    model_match = False
                    model_enforcement_detail = (
                        f"multiple distinct reported models: {distinct_reported}"
                    )
                elif distinct_reported[0] != self.model:
                    model_match = False
                    model_enforcement_detail = (
                        f"reported model '{distinct_reported[0]}' != "
                        f"requested model '{self.model}'"
                    )
                else:
                    model_match = True

            trace_log.append(_trace_event(
                "ModelEnforcement", None, None,
                "hard_stop" if model_match is False else "ok" if model_match else "not_applicable",
                extra={
                    "requested_model": self.model,
                    "reported_models": distinct_reported,
                    "model_match": model_match,
                },
            ))

            trace_path = write_tool_trace(trace_log, artifact_session_dir, self.repo_root)

            # Hard-stop takes precedence over artifact success (issue #86,
            # requirements 8-9): a produced artifact does not excuse a model
            # mismatch or an unobservable model in a run that required one.
            # No fallback, no retry -- return control to the caller.
            if self.model and model_match is False:
                return SkillExecutionResult(
                    skill_id=skill_id,
                    status=SkillExecutionStatus.FAILED,
                    command=invocation_command,
                    output_artifact=expected_output_artifact,
                    error=f"[model_mismatch] {model_enforcement_detail}. "
                          f"requested_model={self.model} reported_models={distinct_reported}",
                    requested_model=self.model,
                    reported_models=distinct_reported,
                    model_match=False,
                )

            # Runtime-skeleton hard-stop (companion to the model-enforcement
            # hard-stop above): if reconciliation produced an authoritative
            # handoff whose Section 13 YAML cannot be parsed, this is a
            # runtime serialization defect, not a model content problem --
            # validate-brief.py's HANDOFF_YAML_PARSE_ERROR would reject it
            # anyway, but the runtime must not silently report artifact
            # success (or a misleadingly-true integrity_ok) on top of a
            # handoff it already knows cannot parse.
            if uses_runtime_skeleton and not handoff_yaml_valid:
                return SkillExecutionResult(
                    skill_id=skill_id,
                    status=SkillExecutionStatus.FAILED,
                    command=invocation_command,
                    output_artifact=expected_output_artifact,
                    error=f"[handoff_yaml_invalid] Section 13 machine-readable handoff did not "
                          f"produce parseable YAML after reconciliation: {handoff_yaml_invalid_reason}",
                    requested_model=self.model,
                    reported_models=distinct_reported,
                    model_match=model_match,
                )

            # Check if the expected artifact was produced
            if os.path.exists(expected_output_path):
                return SkillExecutionResult(
                    skill_id=skill_id,
                    status=SkillExecutionStatus.EXECUTED,
                    command=invocation_command,
                    output_artifact=expected_output_artifact,
                    message=f"Artifact produced at {expected_output_path}"
                            + (f" (tool trace: {trace_path})" if trace_path else ""),
                    requested_model=self.model,
                    reported_models=distinct_reported,
                    model_match=model_match,
                )
            else:
                # Build categorized error: include SDK error info if available
                category = "sdk_result_error" if sdk_last_result_info else "no_artifact"
                detail = ""
                if sdk_last_result_info:
                    detail = f" SDK reported: {sdk_last_result_info}."
                return SkillExecutionResult(
                    skill_id=skill_id,
                    status=SkillExecutionStatus.FAILED,
                    command=invocation_command,
                    output_artifact=expected_output_artifact,
                    error=f"[{category}] Expected artifact '{expected_output_artifact}' not produced.{detail} "
                          f"Artifact not found at {expected_output_path}",
                    requested_model=self.model,
                    reported_models=distinct_reported,
                    model_match=model_match,
                )

        except Exception as e:
            write_tool_trace(trace_log, artifact_session_dir, self.repo_root)
            detail = ""
            if sdk_last_result_info:
                detail = f" SDK result: {sdk_last_result_info}."
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.FAILED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"SDK execution failed: {e}.{detail}",
                requested_model=self.model,
                reported_models=list(dict.fromkeys(reported_models)),
            )

# Keep old name as alias for backwards compatibility
ClaudeCodeSkillExecutor = ClaudeAgentSdkSkillExecutor


class ApiSkillExecutor(_GateAImmutableAttributes, SkillExecutor):
    """Invoke skills by calling Claude API directly with skill instructions.

    Loads the skill definition from SKILL.md, builds a prompt with input artifacts,
    calls Claude API, and saves the output to the expected artifact path.

    Requires ANTHROPIC_API_KEY environment variable.
    """

    supports_real_execution: bool = True

    #: The model this executor hardcodes. Named as a constant so the Gate A
    #: check and the SDK call can never drift apart.
    API_MODEL: str = "claude-opus-4-7"

    def __init__(self, repo_root: str, controlled_experiment: bool = False,
                 authorization: Optional[AuthorizedInvocation] = None,
                 invocation_identity: Optional[InvocationIdentity] = None):
        self.repo_root = repo_root
        self.model = self.API_MODEL
        self._declared_controlled_experiment = bool(controlled_experiment)
        self._invocation_identity = invocation_identity or build_invocation_identity(
            repo_root=repo_root,
            executor_id="api",
            model=self.API_MODEL,
            declared_controlled_mode=(True if controlled_experiment else None),
        )
        # Same constructor-level Gate A layer as the Agent SDK executor, so
        # neither production provider path can even be built for a
        # Gate-A-requiring invocation without a live capability.
        require_authorization_capability(
            authorization,
            identity=self._invocation_identity,
            model=None,
            executor_name="ApiSkillExecutor",
        )
        self.authorization = authorization
        self._check_dependencies()

    def _actual_identity(self, skill_id, expected_output_artifact,
                         context) -> InvocationIdentity:
        return build_invocation_identity(
            repo_root=self.repo_root,
            executor_id="api",
            skill_id=skill_id,
            expected_output_artifact=expected_output_artifact,
            context=context,
            model=self.API_MODEL,
            declared_controlled_mode=(
                True if self.__dict__.get("_declared_controlled_experiment")
                else None
            ),
        )

    def _check_dependencies(self) -> tuple[bool, list[str]]:
        """Check if required dependencies are installed."""
        missing = []
        try:
            import anthropic
        except ImportError:
            missing.append("anthropic")

        import os
        if not os.environ.get("ANTHROPIC_API_KEY"):
            missing.append("ANTHROPIC_API_KEY environment variable")

        return len(missing) == 0, missing

    def _load_skill_content(self, skill_id: str) -> str | None:
        """Load skill definition from SKILL.md."""
        skill_path = os.path.join(self.repo_root, "skills", skill_id, "SKILL.md")
        if not os.path.exists(skill_path):
            return None
        try:
            with open(skill_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    def _read_artifact_content(self, artifact_path: str) -> str | None:
        """Read artifact content if it exists."""
        if not artifact_path or not os.path.exists(artifact_path):
            return None
        try:
            with open(artifact_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    def invoke_skill(
        self,
        skill_id: str,
        invocation_command: str,
        input_artifacts: list[str],
        expected_output_artifact: str,
        context: dict,
    ) -> SkillExecutionResult:
        """Invoke a skill via Claude API.

        Returns EXECUTED if artifact is produced and saved.
        Returns FAILED if API call fails or artifact not produced.
        Returns UNSUPPORTED if dependencies missing.

        Gate A: this executor is a second, independent production path to a
        model SDK call (`anthropic.Anthropic().messages.create`). Gating only
        the Claude Agent SDK executor would leave a real bypass, so the same
        capability requirement applies here. This executor additionally
        hardcodes a model that is NOT the contractually authorized Stage 1
        model, so a controlled invocation through it is always refused.
        """
        try:
            api_identity = self._actual_identity(
                skill_id, expected_output_artifact, context
            )
            api_mode = require_authorization_capability(
                self.authorization,
                identity=api_identity,
                model=None,
                executor_name="ApiSkillExecutor.invoke_skill",
            )
            if requires_gate_a(api_mode):
                # Hardcoded API model can never equal the authorized model,
                # so this always fails closed rather than substituting.
                raise GateAAuthorizationRequired(
                    GATE_A_MODEL_MISMATCH,
                    f"ApiSkillExecutor invokes a hardcoded model "
                    f"('{self.API_MODEL}') which is not the authorized Stage 1 "
                    f"model. Controlled invocations must not use this path.",
                )
        except GateAAuthorizationRequired as gate_error:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.FAILED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"{gate_error.code}: {gate_error.detail}",
                message="Gate A denied: no model invocation was attempted.",
            )

        deps_ok, missing = self._check_dependencies()
        if not deps_ok:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.UNSUPPORTED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"Missing dependencies: {', '.join(missing)}. "
                      f"Install with: pip install anthropic",
            )

        # Load skill definition
        skill_content = self._load_skill_content(skill_id)
        if not skill_content:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.FAILED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"Skill '{skill_id}' not found in skills/{skill_id}/SKILL.md",
            )

        # Build prompt with skill definition and context
        prompt_parts = [
            f"You are executing the '{skill_id}' skill as part of a structured workflow.",
            "",
            "## Skill Definition",
            skill_content,
            "",
        ]

        # Add input context if available
        resolved_inputs = context.get("resolved_inputs", {})
        if resolved_inputs:
            prompt_parts.append("## Input Context")
            for input_name, input_data in resolved_inputs.items():
                if input_data.get("type") == "artifact_content":
                    prompt_parts.append(f"\n### {input_name}")
                    prompt_parts.append(f"```\n{input_data.get('content', '')}\n```")

        # Add output instruction — use the runtime-resolved (session-scoped) path.
        expected_path = resolve_output_path(self.repo_root, expected_output_artifact, context)
        relative_expected_path = os.path.relpath(expected_path, self.repo_root).replace("\\", "/")
        prompt_parts.extend([
            "",
            "## Required Output",
            f"Write the final artifact to this path (relative to repo root):",
            f"`{relative_expected_path}`",
            "",
            "Produce valid markdown that matches the expected artifact format. "
            "Include all required sections and machine-readable fields.",
        ])

        prompt = "\n".join(prompt_parts)

        try:
            from anthropic import Anthropic

            client = Anthropic()

            # Call Claude API
            message = client.messages.create(
                model=self.API_MODEL,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )

            artifact_content = message.content[0].text if message.content else ""

            # Try to extract markdown artifact from response
            # Claude might wrap it in code blocks or explain it
            import re
            match = re.search(r"^#\s+", artifact_content, re.MULTILINE)
            if match:
                # Response starts with markdown heading, use as-is
                artifact_text = artifact_content
            elif "```markdown" in artifact_content:
                # Response has code block, extract it
                m = re.search(r"```markdown\n(.*?)\n```", artifact_content, re.DOTALL)
                artifact_text = m.group(1) if m else artifact_content
            else:
                artifact_text = artifact_content

            # Create artifacts directory if needed
            os.makedirs(os.path.dirname(expected_path), exist_ok=True)

            # Write artifact to expected path
            with open(expected_path, "w", encoding="utf-8") as f:
                f.write(artifact_text)

            # Verify artifact was created
            if os.path.exists(expected_path):
                return SkillExecutionResult(
                    skill_id=skill_id,
                    status=SkillExecutionStatus.EXECUTED,
                    command=invocation_command,
                    output_artifact=expected_output_artifact,
                    message=f"Artifact produced at {expected_path} via Claude API",
                )
            else:
                return SkillExecutionResult(
                    skill_id=skill_id,
                    status=SkillExecutionStatus.FAILED,
                    command=invocation_command,
                    output_artifact=expected_output_artifact,
                    error=f"Artifact file not created at {expected_path}",
                )

        except Exception as e:
            return SkillExecutionResult(
                skill_id=skill_id,
                status=SkillExecutionStatus.FAILED,
                command=invocation_command,
                output_artifact=expected_output_artifact,
                error=f"API execution failed: {str(e)}",
            )


# ============================================================================
# Factory
# ============================================================================

EXECUTOR_REGISTRY = {
    "dry-run": DryRunSkillExecutor,
    "prompt-chain": PromptChainSkillExecutor,
    "claude-code": ClaudeCodeSkillExecutor,
    "api": ApiSkillExecutor,
}


def create_executor(
    executor_id: str,
    repo_root: str,
    prompt_output_dir: Optional[str] = None,
    model: Optional[str] = None,
    controlled_experiment: bool = False,
    authorization: Optional[AuthorizedInvocation] = None,
    invocation_identity: Optional[InvocationIdentity] = None,
) -> SkillExecutor:
    """Create a SkillExecutor instance by id.

    Gate A: `authorization` is the typed capability minted by
    `gate_a_authorization.authorize_invocation()`. It is REQUIRED whenever
    `controlled_experiment` is True, for every executor id. There is no
    executor id that performs a controlled Stage 1 invocation without it.

    Args:
        executor_id: One of "dry-run", "prompt-chain", "claude-code", "api".
        repo_root: Repository root path.
        prompt_output_dir: Directory for prompt files (prompt-chain only).
        model: Explicit model identifier (issue #86). Only meaningful for
            "claude-code" -- threaded into ClaudeAgentSdkSkillExecutor, which
            passes it to ClaudeAgentOptions(model=...). Ignored for other
            executor ids (dry-run/prompt-chain never invoke the SDK; "api"
            uses its own separate Anthropic-client model configuration, out
            of scope for this issue).
        controlled_experiment: When True and executor_id == "claude-code",
            requires `model` to be set -- raises ValueError otherwise, before
            any SDK object is constructed.

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

    if executor_id == "claude-code":
        return executor_cls(
            repo_root=repo_root, model=model,
            controlled_experiment=controlled_experiment,
            authorization=authorization,
            invocation_identity=invocation_identity,
        )

    if executor_id == "api":
        return executor_cls(
            repo_root=repo_root,
            controlled_experiment=controlled_experiment,
            authorization=authorization,
            invocation_identity=invocation_identity,
        )


    return executor_cls()
