"""Agent-native campaign execution (two-phase protocol, EXP-0002).

Skills are instructions for the coding agent, not prompts the agent
forwards to another model. For ``coding_agent_native`` campaigns the
Python layer is bookkeeping only: it prepares each attempt (durable
reservation + frozen instructions + durable INVOKED) and finalizes it
(validation + ledger recording). The reasoning itself is performed by the
coding agent reading ``repo-sensemaker/SKILL.md`` against the approved
target checkout -- no provider SDK, no external model API, no
``ANTHROPIC_API_KEY``.

Protocol per attempt::

    prepare-next-attempt          (this module, CLI)
        -> durable reservation + raw-request (frozen instructions)
        -> durable INVOKED (the attempt is spent and visible)
        -> coding agent performs repo-sensemaker against the target
        -> agent writes the brief to its delivery path
    finalize-attempt              (this module, CLI)
        -> re-verifies approval + window (live)
        -> preserves raw output + produced artifact
        -> validates via the pinned validator
        -> records the terminal state in the ledger

The real agent-native campaign (EXP-0002) refuses injected verifier or
validator callables; every execution-relevant component is constructed
from the pinned framework and the validated bundle, exactly as in the
provider-loop runner.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from execution_infra.runner import (  # noqa: E402
    ATTEMPT_ARTIFACTS,
    REAL_CAMPAIGN_ID,
    RunnerRefusal,
    build_execution_report,
    construct_production_verifier,
)
from sensemaking_skills.campaign_accounting import (  # noqa: E402
    AttemptOutcomeRecorder,
    CampaignLedger,
    DurableReservationManager,
)
from sensemaking_skills.campaign_accounting.models import (  # noqa: E402
    AttemptState,
)
from sensemaking_skills.campaign_accounting.recorder import (  # noqa: E402
    _require_state,
)
from sensemaking_skills.campaign_validation import (  # noqa: E402
    ValidationContext,
    parse_two_lane_yaml,
    validate_campaign_bundle,
)
from sensemaking_skills.exploratory_execution import (  # noqa: E402
    CONVERSATION_APPROVAL_FILENAME,
    CONVERSATION_APPROVAL_MECHANISM,
    CampaignBriefValidator,
    ConversationApprovalVerifier,
    TargetCheckout,
    execution_module_digests,
    extract_frontmatter,
    framework_tree_unchanged,
)

from sensemaking_skills.exploratory_execution.execution_identity import (  # noqa: E402
    checkout_sha,
)

#: The real agent-native campaign (parallel to runner.REAL_CAMPAIGN_ID).
AGENT_NATIVE_REAL_CAMPAIGN_ID = "EXP-0002-stage1-auteur-coding-agent-pilot"

#: Delivery scratch area (agent-owned, OUTSIDE the recorder-owned attempt
#: directory): the coding agent writes its brief here; finalize preserves
#: it into the attempt directory through the recorder.
DELIVERY_SUBDIR = ".agent-native"

_EXECUTION_PACKAGE_DIR = (
    Path(__file__).resolve().parents[2]
    / "src" / "sensemaking_skills" / "exploratory_execution"
)


# ---------------------------------------------------------------------------
# Guards (mirror the provider-loop runner's preconditions)
# ---------------------------------------------------------------------------


def _read_document(package_dir: Path, name: str) -> bytes:
    path = Path(package_dir) / name
    if not path.is_file():
        raise RunnerRefusal(f"campaign package is missing {name} at {path}")
    return path.read_bytes()


def _read_approval_document(package_dir: Path) -> bytes:
    """Read the operative approval for a coding-agent-native campaign:
    ``approval.md`` (the conversation-approval receipt). Returns the
    extracted YAML frontmatter bytes -- the machine-readable approval
    record -- and refuses when the receipt is missing or has no
    frontmatter.
    """
    path = Path(package_dir) / CONVERSATION_APPROVAL_FILENAME
    if not path.is_file():
        raise RunnerRefusal(
            f"no operative approval at {path}: the human's standalone "
            "'approve' in the active conversation is the authorization, "
            "recorded by the coding agent as approval.md (never inferred "
            "from merge, ownership, or silence)"
        )
    frontmatter = extract_frontmatter(path.read_bytes())
    if frontmatter is None:
        raise RunnerRefusal(
            f"approval.md at {path} has no well-formed YAML frontmatter; "
            "the conversation-approval receipt must carry the exact "
            "frontmatter contract"
        )
    return frontmatter


def _guard_real_campaign(
    package_dir: Path, campaign_id: str, *, verifier: Any, validate: Any
) -> None:
    if campaign_id != AGENT_NATIVE_REAL_CAMPAIGN_ID:
        return  # test campaigns may use injected doubles
    if verifier is not None or validate is not None:
        raise RunnerRefusal(
            "refusing to run the real agent-native campaign with injected "
            "execution components: the verifier and validator must be "
            "constructed from the pinned framework and the validated "
            "configuration (no caller-supplied callable may authorize the "
            "real campaign)"
        )
    _read_approval_document(package_dir)



def _guard_conversation_mechanism(bundle: Any) -> None:
    """The coding-agent-native mode uses the conversation-approval receipt
    (approval_source: active_human_conversation). The GitHub comment and
    signed-commit mechanisms were REPLACED for this mode; anything else is
    refused even if a legacy file were placed in the package."""
    raw = getattr(bundle.approval, "raw", {}) or {}
    if raw.get("approval_source") != CONVERSATION_APPROVAL_MECHANISM:
        raise RunnerRefusal(
            "coding-agent-native campaigns require the conversation-"
            "approval receipt (approval_source: active_human_conversation); "
            "the GitHub/signed-commit mechanisms were replaced for this "
            "execution mode"
        )

def _guard_window(policy_raw: dict[str, Any], now: datetime) -> None:
    window = policy_raw["validity_window"]
    not_before = datetime.fromisoformat(window["not_before"])
    not_after = datetime.fromisoformat(window["not_after"])
    if now < not_before:
        raise RunnerRefusal(
            f"validity window has not opened: now={now.isoformat()} "
            f"< not_before={window['not_before']}"
        )
    if now >= not_after:
        raise RunnerRefusal(
            f"validity window has expired: now={now.isoformat()} "
            f">= not_after={window['not_after']}"
        )


def _guard_framework_checkout(framework_checkout: Path, policy_raw: dict[str, Any]) -> None:
    pinned = policy_raw["allowed_framework_shas"][0]
    actual = checkout_sha(Path(framework_checkout))
    if actual != pinned:
        raise RunnerRefusal(
            f"framework checkout HEAD {actual} is not the pinned "
            f"framework_sha {pinned}; refusing to run with a mislabeled "
            "framework commit"
        )
    if not framework_tree_unchanged(pinned, Path(framework_checkout)):
        raise RunnerRefusal(
            f"framework tree at {actual} is not byte-identical to the "
            f"pinned {pinned}; execution would use unapproved framework "
            "bytes"
        )


def _reserved_slot_count(campaign_root: Path, campaign_id: str) -> int:
    ledger = CampaignLedger(Path(campaign_root) / campaign_id, campaign_id)
    events = ledger.read_events()
    return sum(1 for e in events if e.event_type == "RESERVED")


def _skill_text(framework_checkout: Path) -> str:
    skill = Path(framework_checkout) / "skills" / "repo-sensemaker" / "SKILL.md"
    if not skill.is_file():
        raise RunnerRefusal(
            f"pinned framework checkout has no repo-sensemaker skill at "
            f"{skill}; refusing to prepare an attempt without the pinned "
            "skill bytes"
        )
    return skill.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Attempt instructions (the frozen request)
# ---------------------------------------------------------------------------


def _build_instructions(
    skill_text: str,
    *,
    campaign_id: str,
    attempt_id: str,
    policy_digest: str,
    framework_sha: str,
    target_repository: str,
    target_sha: str,
    target_path: str,
    output_path: str,
    delivery_path: str,
    finalize_command: str,
) -> str:
    return "\n".join(
        [
            f"# {campaign_id} - attempt {attempt_id}",
            "",
            "You (the coding agent) perform this attempt directly. No",
            "external model or provider API is authorized (policy:",
            "external_provider_api_prohibited: true).",
            "",
            f"Policy digest: {policy_digest}",
            f"Framework pinned: {framework_sha}",
            f"Target repository: {target_repository}",
            f"Target SHA: {target_sha}",
            f"Target checkout (read-only): {target_path}",
            f"Expected artifact type: repository_sensemaking_brief",
            f"Expected output path: {output_path}",
            f"Delivery path (write the brief HERE): {delivery_path}",
            "",
            "## Skill: repo-sensemaker",
            "",
            skill_text,
            "",
            "## Protocol",
            "",
            "1. Analyze the target checkout at the pinned SHA per the skill.",
            "2. Produce the Repository Sensemaking Brief and write it to the",
            f"   delivery path: {delivery_path}",
            "3. Run the finalize command with the exact attempt id:",
            f"   {finalize_command}",
            "",
            "## Rules",
            "",
            "- The target checkout is READ-ONLY; never modify it.",
            "- No external model/provider API calls, ever.",
            "- No hidden retries: a failed or interrupted attempt is recorded",
            "  and reported; it is never silently repeated.",
            "- All results are EXPLORATORY_NOT_CANONICAL_EVIDENCE.",
            "",
        ]
    )


# ---------------------------------------------------------------------------
# prepare-next-attempt
# ---------------------------------------------------------------------------


def prepare_next_attempt(
    *,
    package_dir: Path,
    campaign_root: Path,
    framework_checkout: Path,
    target_checkout_root: Path | None = None,
    allowed_approver_identities: frozenset | None = None,
    verifier: Any = None,
    clock: Callable[[], datetime] | None = None,
    token: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Create the durable reservation, freeze the instructions, and record
    the durable INVOKED transition for the next attempt slot."""
    package_dir = Path(package_dir)
    campaign_root = Path(campaign_root)
    framework_checkout = Path(framework_checkout)
    allowed = (
        allowed_approver_identities
        if allowed_approver_identities is not None
        else frozenset()
    )
    clock_fn = clock or (lambda: datetime.now(UTC))
    now = now or clock_fn()

    policy_bytes = _read_document(package_dir, "campaign-policy.yaml")
    config_bytes = _read_document(package_dir, "configuration-identity.yaml")
    policy_raw = parse_two_lane_yaml(policy_bytes)
    campaign_id = policy_raw["campaign_id"]
    config_raw = parse_two_lane_yaml(config_bytes)

    if policy_raw.get("execution_mode") != "coding_agent_native":
        raise RunnerRefusal(
            "prepare-next-attempt is only valid for coding_agent_native "
            "campaigns; this policy declares "
            f"{policy_raw.get('execution_mode')!r}"
        )
    if (
        policy_raw.get("execution_mode") == "coding_agent_native"
        and policy_raw.get("external_provider_api_prohibited") is not True
    ):
        raise RunnerRefusal(
            "coding_agent_native requires external_provider_api_prohibited: "
            "true (no external model/provider API may be involved)"
        )

    _guard_real_campaign(package_dir, campaign_id, verifier=verifier, validate=None)
    _guard_window(policy_raw, now)
    if campaign_id == AGENT_NATIVE_REAL_CAMPAIGN_ID:
        _guard_framework_checkout(framework_checkout, policy_raw)

    context = ValidationContext(
        current_time=now.isoformat(),
        allowed_approver_identities=allowed,
    )
    bundle_result = validate_campaign_bundle(
        policy_bytes,
        _read_approval_document(package_dir),
        config_bytes,
        context,
    )
    if not bundle_result.valid:
        raise RunnerRefusal(
            f"bundle validation failed: {bundle_result.failure_code} "
            f"{bundle_result.detail}"
        )
    bundle = bundle_result.value
    _guard_conversation_mechanism(bundle)

    approval_bytes = _read_approval_document(package_dir)
    if campaign_id == AGENT_NATIVE_REAL_CAMPAIGN_ID:
        verifier = construct_production_verifier(framework_checkout, bundle)
    if verifier is not None:
        verifier.verify(bundle.approval, approval_bytes=approval_bytes)

    remaining = (
        int(policy_raw["max_attempt_slots"])
        - _reserved_slot_count(campaign_root, campaign_id)
    )
    if remaining <= 0:
        raise RunnerRefusal(
            "no remaining attempt slots: ledger already contains "
            f"{int(policy_raw['max_attempt_slots']) - remaining} of "
            f"{policy_raw['max_attempt_slots']} reservations"
        )

    target = None
    target_path = ""
    if campaign_id == AGENT_NATIVE_REAL_CAMPAIGN_ID:
        if target_checkout_root is None:
            raise RunnerRefusal(
                "real agent-native campaign requires --target-checkout-root"
            )
        target = TargetCheckout.prepare(
            target_repository=str(config_raw["target_repository"]),
            target_sha=str(config_raw["target_sha"]),
            work_root=Path(target_checkout_root),
        )
        target.seal_read_only()
        target_path = str(target.path)

    attempt_id = str(uuid.uuid4())
    manager = DurableReservationManager(campaign_root)
    reservation = manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=str(config_raw["configuration_id"]),
        request_metadata={
            "execution_mode": "coding_agent_native",
            "execution_surface": str(
                policy_raw.get("execution_surface", "current_coding_agent")
            ),
        },
        now=now,
    )

    recorder = AttemptOutcomeRecorder(campaign_root, campaign_id, attempt_id)
    output_path = str(
        campaign_root
        / campaign_id
        / "attempts"
        / attempt_id
        / "produced-artifact.md"
    )
    delivery_dir = (
        campaign_root / DELIVERY_SUBDIR / campaign_id / attempt_id
    )
    delivery_dir.mkdir(parents=True, exist_ok=True)
    delivery_path = str(delivery_dir / "delivery.md")

    finalize_command = (
        "python scripts/execution_infra/agent_native_campaign.py finalize "
        f"--package-dir {package_dir} --campaign-root {campaign_root} "
        f"--framework-checkout {framework_checkout} --attempt-id {attempt_id} "
        f"--artifact {delivery_path}"
    )
    instructions = _build_instructions(
        _skill_text(framework_checkout),
        campaign_id=campaign_id,
        attempt_id=attempt_id,
        policy_digest=str(policy_raw["policy_digest"]),
        framework_sha=str(config_raw["framework_sha"]),
        target_repository=str(config_raw["target_repository"]),
        target_sha=str(config_raw["target_sha"]),
        target_path=target_path or str(config_raw["target_repository"]),
        output_path=output_path,
        delivery_path=delivery_path,
        finalize_command=finalize_command,
    )

    request_ref = recorder.record_raw_request(
        instructions.encode("utf-8"), now=now
    )
    recorder.record_invoked(bundle, now=now, raw_request_reference=request_ref)

    instructions_path = delivery_dir / "attempt-instructions.md"
    instructions_path.write_text(instructions, encoding="utf-8")

    return {
        "attempt_id": attempt_id,
        "output_path": output_path,
        "delivery_path": delivery_path,
        "instructions_path": str(instructions_path),
        "target_path": target_path,
        "reservation": reservation,
        "remaining_slots": remaining - 1,
    }


# ---------------------------------------------------------------------------
# finalize-attempt
# ---------------------------------------------------------------------------


def finalize_attempt(
    *,
    package_dir: Path,
    campaign_root: Path,
    framework_checkout: Path,
    attempt_id: str,
    artifact_path: Path,
    target_checkout_root: Path | None = None,
    allowed_approver_identities: frozenset | None = None,
    verifier: Any = None,
    validate: Any = None,
    clock: Callable[[], datetime] | None = None,
    token: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Validate the agent's delivered artifact and record the terminal
    attempt state (re-verifying approval + window first)."""
    package_dir = Path(package_dir)
    campaign_root = Path(campaign_root)
    framework_checkout = Path(framework_checkout)
    artifact_path = Path(artifact_path)
    allowed = (
        allowed_approver_identities
        if allowed_approver_identities is not None
        else frozenset()
    )
    clock_fn = clock or (lambda: datetime.now(UTC))
    now = now or clock_fn()

    policy_bytes = _read_document(package_dir, "campaign-policy.yaml")
    config_bytes = _read_document(package_dir, "configuration-identity.yaml")
    policy_raw = parse_two_lane_yaml(policy_bytes)
    campaign_id = policy_raw["campaign_id"]
    config_raw = parse_two_lane_yaml(config_bytes)

    _guard_real_campaign(package_dir, campaign_id, verifier=verifier, validate=validate)
    _guard_window(policy_raw, now)

    context = ValidationContext(
        current_time=now.isoformat(),
        allowed_approver_identities=allowed,
    )
    bundle_result = validate_campaign_bundle(
        policy_bytes,
        _read_approval_document(package_dir),
        config_bytes,
        context,
    )
    if not bundle_result.valid:
        raise RunnerRefusal(
            f"bundle validation failed: {bundle_result.failure_code} "
            f"{bundle_result.detail}"
        )
    bundle = bundle_result.value
    _guard_conversation_mechanism(bundle)

    approval_bytes = _read_approval_document(package_dir)
    if campaign_id == AGENT_NATIVE_REAL_CAMPAIGN_ID:
        verifier = construct_production_verifier(framework_checkout, bundle)
    if verifier is not None:
        # Re-validate the conversation receipt before EVERY finalize (a
        # superseded or edited approval.md stops the attempt here).
        verifier.verify(bundle.approval, approval_bytes=approval_bytes)

    if not artifact_path.is_file():
        raise RunnerRefusal(
            f"no delivered artifact at {artifact_path}; the coding agent "
            "must write the brief to the delivery path before finalize"
        )
    recorder = AttemptOutcomeRecorder(campaign_root, campaign_id, attempt_id)
    ledger = CampaignLedger(campaign_root / campaign_id, campaign_id)
    _require_state(
        ledger.read_events(), attempt_id, AttemptState.INVOKED.value
    )
    # Path confinement: finalize only accepts the agent's delivered brief
    # inside THIS attempt's delivery directory (derived from the ledger
    # attempt id, never from the caller's claim). Any other readable file
    # on the machine is refused -- finalize records the attempt's own
    # delivery, nothing else.
    delivery_dir = (
        campaign_root / DELIVERY_SUBDIR / campaign_id / attempt_id
    ).resolve(strict=False)
    resolved_artifact = artifact_path.resolve(strict=False)
    if resolved_artifact.parent != delivery_dir:
        raise RunnerRefusal(
            f"artifact {artifact_path} resolves to "
            f"{resolved_artifact}, outside the attempt delivery directory "
            f"{delivery_dir}; finalize only records the coding agent's "
            "delivered brief"
        )
    artifact_bytes = artifact_path.read_bytes()

    raw_ref = recorder.record_raw_output(artifact_bytes, extension="md", now=now)
    artifact_ref = recorder.record_produced_artifact(
        artifact_bytes.decode("utf-8"),
        filename="produced-artifact.md",
    )

    if campaign_id == AGENT_NATIVE_REAL_CAMPAIGN_ID:
        if target_checkout_root is None:
            raise RunnerRefusal(
                "real agent-native campaign requires --target-checkout-root "
                "for the pinned validator"
            )
        target = TargetCheckout.prepare(
            target_repository=str(config_raw["target_repository"]),
            target_sha=str(config_raw["target_sha"]),
            work_root=Path(target_checkout_root),
        )
        validate = CampaignBriefValidator(
            framework_checkout=framework_checkout,
            target_checkout=target.path,
        )
    if validate is None:
        raise RunnerRefusal(
            "no validator available; test campaigns must inject one"
        )
    outcome = validate(artifact_bytes)

    result = recorder.record_validation_outcome(
        passed=bool(outcome.passed),
        details=getattr(outcome, "details", ""),
        validated_output_ref=artifact_ref,
        now=now,
    )
    return {
        "attempt_id": attempt_id,
        "state": result.state,
        "validation_passed": bool(outcome.passed),
        "validation_details": getattr(outcome, "details", ""),
        "raw_output_ref": raw_ref,
        "artifact_ref": artifact_ref,
    }


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

#: State-aware expected evidence inside attempts/<attempt-id>/ (fail-closed
#: minimum: a terminal or captured state MISSING one of these files makes
#: report generation refuse, because the record would be incomplete).
_STATE_EXPECTED_ARTIFACTS: dict[str, tuple[str, ...]] = {
    "RESERVED": ("reservation.yaml",),
    "INVOKED": ("reservation.yaml", "raw-request.txt"),
    "OUTPUT_CAPTURED": (
        "reservation.yaml", "raw-request.txt", "raw-output.md",
    ),
    "VALIDATION_PASSED": (
        "reservation.yaml", "raw-request.txt", "raw-output.md",
        "produced-artifact.md", "validation-result.json",
        "attempt-result.yaml",
    ),
    "VALIDATION_FAILED": (
        "reservation.yaml", "raw-request.txt", "raw-output.md",
        "produced-artifact.md", "validation-result.json",
        "attempt-result.yaml",
    ),
    "PROVIDER_FAILED": ("reservation.yaml", "raw-request.txt"),
    "ABORTED_BEFORE_INVOCATION": (),
}


def _attempt_report_detail(attempt_dir: Path, state: str) -> dict:
    """Load the per-attempt report detail: the recorded validation outcome
    (validation-result.json), the state-aware artifact list (only files
    that actually exist), and orphan detection. Missing expected files
    make reporting fail closed (the record would be incomplete)."""
    expected = _STATE_EXPECTED_ARTIFACTS.get(state, ())
    missing = [name for name in expected if not (attempt_dir / name).is_file()]
    if missing:
        raise RunnerRefusal(
            f"attempt record {attempt_dir.name} (state={state}) is missing "
            f"expected evidence: {', '.join(missing)}; refusing to "
            "generate an incomplete report"
        )
    existing = sorted(p.name for p in attempt_dir.iterdir() if p.is_file())
    expected_set = set(expected)
    orphans = [name for name in existing if name not in expected_set]
    detail: dict = {
        "attempt_id": attempt_dir.name,
        "state": state,
        "artifacts": list(expected),
        "orphan_artifacts": orphans,
    }
    validation_result = attempt_dir / "validation-result.json"
    if validation_result.is_file():
        try:
            detail["validation_outcome"] = json.loads(
                validation_result.read_text(encoding="utf-8")
            )
        except (ValueError, OSError) as exc:
            raise RunnerRefusal(
                f"attempt record {attempt_dir.name} has an unreadable "
                f"validation-result.json: {exc}"
            ) from exc
    return detail


def _target_integrity_check(
    target_checkout_root: Path | None,
    repository: str,
    sha: str,
) -> tuple[bool, str]:
    """Report-time target integrity under the ONE work-root contract:
    ``--target-checkout-root`` is the materialization work root everywhere
    (prepare/finalize/report), and the actual checkout lives at
    ``<target-checkout-root>/target``.

    Reporting only REOPENS and verifies that checkout -- it never calls
    ``TargetCheckout.prepare()`` and never clones, fetches, checks out,
    resets, cleans, or mutates anything. Returns ``(ok, reason)`` with the
    ACTUAL result; ``ok`` is true only when every integrity check
    (origin, exact SHA, clean index + working tree, no untracked files,
    no .gitmodules, no active submodules) succeeds."""
    if target_checkout_root is None:
        return False, "no --target-checkout-root supplied; integrity cannot be attested"
    checkout_path = Path(target_checkout_root) / "target"
    if not (checkout_path / ".git").exists():
        return (
            False,
            f"target checkout {checkout_path} is absent; nothing to attest "
            "(the staging phase materializes it; reporting never clones)",
        )
    try:
        target = TargetCheckout(
            checkout_path, target_repository=repository, target_sha=sha
        )
        target.verify_integrity()
        return True, "origin, SHA, index, working tree, untracked files, and submodules all verified clean"
    except Exception as exc:  # noqa: BLE001 - integrity is reported, never fatal
        return False, str(exc).strip() or "target integrity verification failed"


def build_report(
    *,
    package_dir: Path,
    campaign_root: Path,
    framework_checkout: Path,
    target_checkout_root: Path | None = None,
    allowed_approver_identities: frozenset | None = None,
    now: datetime | None = None,
    report_only: bool = False,
) -> str:
    """Build the complete ledger-derived execution report (same contract
    as the provider-loop runner's report), with agent-native accuracy:
    dynamic campaign title, agent-invocation vs external-provider-API
    counts, real validation rates from the recorded per-attempt results,
    state-aware artifact lists (raw-output.md for agent-native), a REAL
    report-time target-integrity check, and an optional report-only path
    that verifies without authorizing anything and without requiring the
    wall clock to sit inside the execution window."""
    from sensemaking_skills.campaign_accounting import CampaignSummaryGenerator

    package_dir = Path(package_dir)
    campaign_root = Path(campaign_root)
    framework_checkout = Path(framework_checkout)
    now = now or datetime.now(UTC)

    policy_bytes = _read_document(package_dir, "campaign-policy.yaml")
    config_bytes = _read_document(package_dir, "configuration-identity.yaml")
    policy_raw = parse_two_lane_yaml(policy_bytes)
    config_raw = parse_two_lane_yaml(config_bytes)
    allowed = (
        allowed_approver_identities
        if allowed_approver_identities is not None
        else frozenset()
    )
    context = ValidationContext(
        current_time=now.isoformat(),
        allowed_approver_identities=allowed,
        enforce_validity_window=not report_only,
    )
    bundle_result = validate_campaign_bundle(
        policy_bytes,
        _read_approval_document(package_dir),
        config_bytes,
        context,
    )
    if not bundle_result.valid:
        raise RunnerRefusal(
            f"bundle validation failed: {bundle_result.failure_code} "
            f"{bundle_result.detail}"
        )
    bundle = bundle_result.value
    _guard_conversation_mechanism(bundle)
    summary = CampaignSummaryGenerator(campaign_root).update_campaign_summary(
        bundle, now=now
    )
    attempts_dir = Path(campaign_root) / summary.campaign_id / "attempts"
    attempts_detail = []
    from sensemaking_skills.campaign_accounting import CampaignLedger

    ledger_events = CampaignLedger(
        Path(campaign_root) / summary.campaign_id,
        campaign_id=summary.campaign_id,
    ).read_events()
    # Agent invocations = INVOKED transitions in the ledger (an attempt is
    # invoked once, durably, before the coding agent begins the reasoning
    # work; final states may be terminal).
    agent_invocations = sum(
        1 for e in ledger_events if e.event_type == "INVOKED"
    )
    for entry in summary.attempts:
        state = entry["state"]
        attempt_dir = attempts_dir / entry["attempt_id"]
        if attempt_dir.is_dir():
            attempts_detail.append(
                _attempt_report_detail(attempt_dir, state)
            )
        else:
            # Ledger-only attempt (no attempt directory materialized):
            # still reported, with its state and an explicit empty
            # artifact list (never the provider-era fallback names).
            attempts_detail.append(
                {
                    "attempt_id": entry["attempt_id"],
                    "state": state,
                    "artifacts": [],
                }
            )
    try:
        drift_clean = framework_tree_unchanged(
            policy_raw["allowed_framework_shas"][0], framework_checkout
        )
    except Exception:  # noqa: BLE001 - drift is reported, never fatal
        drift_clean = False
    try:
        framework_checkout_sha = checkout_sha(framework_checkout)
    except Exception:  # noqa: BLE001 - integrity is reported, never fatal
        framework_checkout_sha = "unresolvable"
    target_integrity_ok, target_integrity_reason = _target_integrity_check(
        target_checkout_root,
        repository=str(config_raw.get("target_repository", "")),
        sha=str(config_raw.get("target_sha", "")),
    )
    return build_execution_report(
        {
            "summary": summary,
            "attempts": attempts_detail,
            "errors": [],
            "execution_module_digests": execution_module_digests(
                _EXECUTION_PACKAGE_DIR
            ),
            "framework_checkout_sha": framework_checkout_sha,
            "pinned_framework_sha": policy_raw["allowed_framework_shas"][0],
            "total_attempts_authorized": int(policy_raw["max_attempt_slots"]),
            "mode": "coding_agent_native",
            "total_agent_attempt_invocations": agent_invocations,
            "external_provider_api_prohibited": policy_raw.get(
                "external_provider_api_prohibited"
            )
            is True,
            "external_provider_api_invocations": 0,
            "external_provider_cost": 0,
            "drift": {
                "pre": drift_clean,
                "post": drift_clean,
                "target_integrity_ok": target_integrity_ok,
                "target_integrity_reason": target_integrity_reason,
            },
            "report_only": report_only,
            "completed_at": now.isoformat(),
        }
    )


# ---------------------------------------------------------------------------
# validate-approval (window-independent receipt validation)
# ---------------------------------------------------------------------------


def validate_approval(
    *,
    package_dir: Path,
    allowed_approver_identities: frozenset | None = None,
    now: datetime | None = None,
) -> dict:
    """Validate the operative conversation-approval receipt against the
    exact campaign envelope WITHOUT coupling it to the execution window.

    Proportional-approval contract: the human's standalone ``approve``
    may be given any time after the final envelope is presented and
    before it expires (``approved_at <= validity_window.not_after``).
    The receipt is recorded immediately; execution remains mechanically
    gated by ``validity_window.not_before`` (prepare/finalize always
    enforce the window -- fail closed). This command performs NO
    reservation, NO invocation, and creates NO runtime record.
    """
    package_dir = Path(package_dir)
    now = now or datetime.now(UTC)

    policy_bytes = _read_document(package_dir, "campaign-policy.yaml")
    config_bytes = _read_document(package_dir, "configuration-identity.yaml")
    allowed = (
        allowed_approver_identities
        if allowed_approver_identities is not None
        else frozenset()
    )
    context = ValidationContext(
        current_time=now.isoformat(),
        allowed_approver_identities=allowed,
        enforce_validity_window=False,
    )
    bundle_result = validate_campaign_bundle(
        policy_bytes,
        _read_approval_document(package_dir),
        config_bytes,
        context,
    )
    if not bundle_result.valid:
        raise RunnerRefusal(
            f"bundle validation failed: {bundle_result.failure_code} "
            f"{bundle_result.detail}"
        )
    bundle = bundle_result.value
    _guard_conversation_mechanism(bundle)
    approval_bytes = _read_approval_document(package_dir)
    verifier = ConversationApprovalVerifier(
        policy=bundle.policy.raw, clock=lambda: now
    )
    verified = verifier.verify(bundle.approval, approval_bytes=approval_bytes)
    return {
        "campaign_id": verified.campaign_id,
        "policy_digest": verified.policy_digest,
        "approved_at": bundle.approval.raw.get("approved_at", ""),
        "reference": verified.reference,
        "window_independent": True,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Agent-native campaign bookkeeping (prepare / finalize / "
            "report). The coding agent performs the skill itself; these "
            "commands only reserve, preserve, validate, and record."
        )
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("prepare", help="reserve + freeze instructions + INVOKED")
    p.add_argument("--package-dir", type=Path, required=True)
    p.add_argument("--campaign-root", type=Path, required=True)
    p.add_argument("--framework-checkout", type=Path, required=True)
    p.add_argument("--target-checkout-root", type=Path, default=None)
    p.add_argument("--allowed-approver", action="append", default=[])
    p.add_argument("--token", default=None)

    f = sub.add_parser("finalize", help="validate + record a delivered artifact")
    f.add_argument("--package-dir", type=Path, required=True)
    f.add_argument("--campaign-root", type=Path, required=True)
    f.add_argument("--framework-checkout", type=Path, required=True)
    f.add_argument("--attempt-id", required=True)
    f.add_argument("--artifact", type=Path, required=True)
    f.add_argument("--target-checkout-root", type=Path, default=None)
    f.add_argument("--allowed-approver", action="append", default=[])
    f.add_argument("--token", default=None)

    v = sub.add_parser(
        "validate-approval",
        help=(
            "validate the operative approval receipt against the exact "
            "envelope (window-independent: may run before the execution "
            "window opens; performs no reservation or invocation)"
        ),
    )
    v.add_argument("--package-dir", type=Path, required=True)
    v.add_argument("--allowed-approver", action="append", default=[])

    r = sub.add_parser("report", help="render the complete ledger-derived report")
    r.add_argument("--package-dir", type=Path, required=True)
    r.add_argument("--campaign-root", type=Path, required=True)
    r.add_argument("--framework-checkout", type=Path, required=True)
    r.add_argument("--target-checkout-root", type=Path, default=None)
    r.add_argument("--report-only", action="store_true")
    r.add_argument("--allowed-approver", action="append", default=[])

    args = parser.parse_args(argv)
    allowed = frozenset(args.allowed_approver)
    try:
        if args.command == "prepare":
            result = prepare_next_attempt(
                package_dir=args.package_dir,
                campaign_root=args.campaign_root,
                framework_checkout=args.framework_checkout,
                target_checkout_root=args.target_checkout_root,
                allowed_approver_identities=allowed,
                token=args.token,
            )
            print(f"ATTEMPT_PREPARED {result['attempt_id']}")
            print(f"DELIVERY_PATH {result['delivery_path']}")
            print(f"INSTRUCTIONS {result['instructions_path']}")
            print(f"REMAINING_SLOTS {result['remaining_slots']}")
            return 0
        if args.command == "finalize":
            result = finalize_attempt(
                package_dir=args.package_dir,
                campaign_root=args.campaign_root,
                framework_checkout=args.framework_checkout,
                attempt_id=args.attempt_id,
                artifact_path=args.artifact,
                target_checkout_root=args.target_checkout_root,
                allowed_approver_identities=allowed,
                token=args.token,
            )
            print(
                f"ATTEMPT_FINALIZED {result['attempt_id']} "
                f"state={result['state']} passed={result['validation_passed']}"
            )
            return 0
        if args.command == "validate-approval":
            result = validate_approval(
                package_dir=args.package_dir,
                allowed_approver_identities=frozenset(args.allowed_approver),
            )
            print(
                f"APPROVAL_VALID {result['campaign_id']} "
                f"{result['policy_digest']} window_independent=true "
                f"reference={result['reference']}"
            )
            return 0

        if args.command == "report":
            print(build_report(
                package_dir=args.package_dir,
                campaign_root=args.campaign_root,
                framework_checkout=args.framework_checkout,
                target_checkout_root=args.target_checkout_root,
                allowed_approver_identities=frozenset(args.allowed_approver),
                report_only=args.report_only,
            ))
            return 0
    except RunnerRefusal as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
