"""EXP-0001 governed campaign runner (Phase 6 correction, Issue #122).

Approach B: the real execution path lives INSIDE the pinned framework
(``sensemaking_skills.exploratory_execution``) and is therefore bound by
``framework_sha`` -- a normative configuration field and a policy allowlist
member -- BEFORE execution, not merely digest-recorded after it. This
module is the thin operator-facing orchestrator; it never duplicates
execution authority.

The runner REFUSES to run the real EXP-0001 campaign unless every
precondition holds:

* the operative approval file exists;
* NO execution component is injected -- the verifier, provider, and
  validator are constructed from the pinned framework and the validated
  campaign configuration (a caller-supplied verifier, provider subclass,
  or arbitrary validate callable can never authorize the real campaign);
* the framework checkout HEAD is exactly the pinned ``framework_sha`` AND
  the full tree (committed, index, working tree, untracked files) is
  byte-identical to the pin;
* the approved target repository is materialized at the exact approved
  SHA, clean, submodule-free, and re-verified before every attempt;
* the current time (re-read before EVERY attempt) is inside the policy
  validity window;
* the bundle (policy + approval + configuration) validates with exact
  digests, and the production verifier corroborates the signed approval
  with full byte/identity binding.

Lifecycle per attempt (all durable, ledger-authoritative):

1. read the real clock;
2. re-check the validity window;
3. derive remaining slots from the LEDGER (a resumed run never blindly
   begins another full loop);
4. reserve exactly one attempt;
5. mint its capability -- on mint failure the just-created reservation is
   durably terminalized as ABORTED_BEFORE_INVOCATION with the reason, and
   the run stops;
6. invoke through the Phase 4 boundary (permit-issued after INVOKED,
   request preserved, provider permit-gated);
7. re-verify framework and target integrity.

For ANY other campaign id (tests, experiments) the runner accepts injected
doubles -- the real-campaign guards are keyed on the campaign id of the
package being run, so a dry run on a test campaign can never touch the
real campaign.

The runner never fabricates approval, never calls the provider outside
the Phase 4 boundary, never hides an attempt, and never merges anything.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sensemaking_skills.campaign_accounting import (
    AttemptOutcomeRecorder,
    CampaignLedger,
    CampaignSummaryGenerator,
    DurableReservationManager,
    invoke_exploratory_attempt,
)
from sensemaking_skills.campaign_validation import (
    parse_two_lane_yaml,
    validate_campaign_bundle,
)
from sensemaking_skills.campaign_validation.models import ValidationContext
from sensemaking_skills.exploratory_authorization import mint_exploratory_capability
from sensemaking_skills.exploratory_authorization.digests import (
    compute_approval_snapshot_digest,
    compute_configuration_snapshot_digest,
)
from sensemaking_skills.exploratory_authorization.models import (
    ExploratoryAttemptRequest,
    ExploratoryInvocationContext,
)
from sensemaking_skills.exploratory_execution import (
    GOVERNED_GITHUB_REPOSITORY,
    GOVERNED_REQUIRED_APPROVER_PERMISSION,
    TRUSTED_FRAMEWORK_REMOTE,
    CampaignBriefValidator,
    ClaudeProvider,
    ConversationApprovalVerifier,
    GitHubIssueCommentApprovalVerifier,
    ProductionSignedCommitVerifier,
    TargetCheckout,
    build_exploratory_prompt,
    checkout_sha,
    execution_module_digests,
    framework_tree_unchanged,
)

REAL_CAMPAIGN_ID = "EXP-0001-stage1-auteur-autonomy-pilot"
APPROVAL_FILENAME = "approval.yaml"
LANE = "EXPLORATORY"

#: Execution-record module directory (inside the pinned framework).
_EXECUTION_PACKAGE_DIR = (
    Path(__file__).resolve().parents[2]
    / "src" / "sensemaking_skills" / "exploratory_execution"
)

#: Attempt-directory artifacts every report must name.
ATTEMPT_ARTIFACTS = (
    "reservation.yaml",
    "raw-request.txt",
    "raw-output.bin",
    "produced-artifact.md",
    "validation-result.json",
    "attempt-result.yaml",
)


class RunnerRefusal(Exception):
    """The runner refuses to execute; nothing was reserved or invoked."""


def construct_production_verifier(framework_checkout: Path, bundle: Any) -> Any:
    """Construct the verifier for the VALIDATED approval's provenance
    mechanism (never from a caller-supplied choice).

    ``active_human_conversation`` constructs the conversation-approval
    verifier (the coding-agent-native path: no network, no token -- the
    receipt's consistency with the validated policy envelope IS the
    check). ``signed_commit`` and ``github_issue_comment_approval`` are
    DEPRECATED legacy mechanisms, retained only for historical campaigns;
    any other mechanism refuses. Used by both the provider-loop runner
    and the agent-native campaign CLI, so the two execution surfaces
    share one construction.
    """
    approval_raw = bundle.approval.raw
    provenance = dict(approval_raw.get("approval_provenance") or {})
    mechanism = str(provenance.get("mechanism", ""))
    if approval_raw.get("approval_source") == "active_human_conversation":
        return ConversationApprovalVerifier(policy=bundle.policy.raw)
    if mechanism == "signed_commit":
        # DEPRECATED legacy mechanism (fingerprint registry + signed
        # commit); retained for historical campaigns only.
        return ProductionSignedCommitVerifier(
            repo_root=framework_checkout,
            trusted_remote=TRUSTED_FRAMEWORK_REMOTE,
            approver_registry=(
                framework_checkout
                / "src" / "sensemaking_skills" / "exploratory_execution"
                / "approver-registry.yaml"
            ),
            approval_path=APPROVAL_FILENAME,
        )
    if mechanism == "github_issue_comment_approval":
        # DEPRECATED legacy mechanism (GitHub issue-comment approval);
        # retained for historical campaigns only. The verifier's
        # repository is the GOVERNED constant, never the provenance-
        # supplied value: an approval naming a different repository must
        # fail inside verify(), not silently redirect the verifier to the
        # attacker's repository.
        return GitHubIssueCommentApprovalVerifier(
            repository=GOVERNED_GITHUB_REPOSITORY,
            required_permission=GOVERNED_REQUIRED_APPROVER_PERMISSION,
            policy=bundle.policy.raw,
        )
    raise RunnerRefusal(
        f"unknown approval provenance mechanism {mechanism!r}; "
        "no verifier can corroborate this approval"
    )


class GovernedCampaignRunner:
    """Run the campaign lifecycle for a campaign package."""

    def __init__(
        self,
        *,
        campaign_package_dir: Path,
        campaign_root: Path,
        framework_checkout: Path,
        target_checkout_root: Path | None = None,
        verifier: Any = None,
        provider: Any = None,
        validate: Any = None,
        allowed_approver_identities: frozenset | None = None,
        clock: Callable[[], datetime] | None = None,
        timeout_seconds: int = 1800,
    ) -> None:
        self._package_dir = Path(campaign_package_dir)
        self._campaign_root = Path(campaign_root)
        self._framework_checkout = Path(framework_checkout)
        self._target_checkout_root = Path(target_checkout_root) if target_checkout_root else None
        self._verifier = verifier
        self._provider = provider
        self._validate = validate
        # Fail closed: with an empty allowlist no approval can ever
        # validate. The operator supplies the genuine approver identity.
        self._allowed_approver_identities = (
            allowed_approver_identities if allowed_approver_identities is not None
            else frozenset()
        )
        self._clock = clock or (lambda: datetime.now(UTC))
        self._timeout_seconds = timeout_seconds

    # ------------------------------------------------------------------ #
    # Precondition guards
    # ------------------------------------------------------------------ #

    def _read_document(self, name: str) -> bytes:
        path = self._package_dir / name
        if not path.is_file():
            raise RunnerRefusal(f"campaign package is missing {name} at {path}")
        return path.read_bytes()

    def _guard_real_campaign(self, campaign_id: str) -> None:
        if campaign_id != REAL_CAMPAIGN_ID:
            return  # test campaigns may use injected doubles
        if self._verifier is not None or self._provider is not None or self._validate is not None:
            raise RunnerRefusal(
                "refusing to run the real EXP-0001 campaign with injected "
                "execution components: the verifier, provider, and validator "
                "must be constructed from the pinned framework and the "
                "validated configuration (no caller-supplied callable may "
                "authorize the real campaign)"
            )
        if not (self._package_dir / APPROVAL_FILENAME).is_file():
            # The real approval file may only exist once a human created it.
            raise RunnerRefusal(
                f"refusing to run the real campaign: no operative approval "
                f"at {self._package_dir / APPROVAL_FILENAME}; approval is a "
                "human act, never inferred from merge or ownership"
            )

    def _guard_window(self, policy_raw: dict[str, Any], now: datetime) -> None:
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

    def _guard_framework_checkout(self, policy_raw: dict[str, Any]) -> None:
        pinned = policy_raw["allowed_framework_shas"][0]
        actual = checkout_sha(self._framework_checkout)
        if actual != pinned:
            raise RunnerRefusal(
                f"framework checkout HEAD {actual} is not the pinned "
                f"framework_sha {pinned}; refusing to run with a "
                "mislabeled framework commit"
            )
        if not framework_tree_unchanged(pinned, self._framework_checkout):
            raise RunnerRefusal(
                f"framework tree at {actual} is not byte-identical to the "
                f"pinned {pinned} (committed tree, index, working tree, or "
                "untracked files differ); execution would use unapproved "
                "framework bytes"
            )

    # ------------------------------------------------------------------ #
    # Production component construction (from the pinned framework)
    # ------------------------------------------------------------------ #

    def _production_components(
        self, config_raw: dict[str, Any], target: TargetCheckout, bundle: Any
    ) -> tuple:
        """Construct the provider-loop components for the validated bundle.

        The verifier comes from ``construct_production_verifier`` (mechanism
        from the validated approval, never caller-chosen); the provider is
        the Claude SDK provider (provider_api campaigns only -- agent-native
        campaigns refuse in ``run()`` before reaching this point).
        """
        verifier = construct_production_verifier(self._framework_checkout, bundle)
        provider = ClaudeProvider(
            model=str(config_raw["model_identifier"]),
            target_repository=str(config_raw["target_repository"]),
            target_sha=str(config_raw["target_sha"]),
            framework_sha=str(config_raw["framework_sha"]),
            artifact_type=str(config_raw["artifact_type"]),
            target_checkout=target.path,
            timeout_seconds=self._timeout_seconds,
        )
        validator = CampaignBriefValidator(
            framework_checkout=self._framework_checkout,
            target_checkout=target.path,
        )
        return verifier, provider, validator

    def _skill_text(self) -> str:
        skill = (
            self._framework_checkout / "skills" / "repo-sensemaker" / "SKILL.md"
        )
        if not skill.is_file():
            raise RunnerRefusal(
                f"pinned framework checkout has no repo-sensemaker skill at "
                f"{skill}; refusing to build a prompt without the pinned "
                "skill bytes"
            )
        return skill.read_text(encoding="utf-8")

    # ------------------------------------------------------------------ #
    # Ledger-derived remaining slots
    # ------------------------------------------------------------------ #

    def _reserved_slot_count(self, campaign_id: str) -> int:
        campaign_dir = self._campaign_root / campaign_id
        ledger = CampaignLedger(campaign_dir, campaign_id)
        events = ledger.read_events()
        return sum(
            1
            for e in events
            if e.event_type == "RESERVED"
        )

    # ------------------------------------------------------------------ #
    # The lifecycle
    # ------------------------------------------------------------------ #

    def run(self) -> dict[str, Any]:
        """Validate preconditions and run every remaining attempt slot."""
        policy_bytes = self._read_document("campaign-policy.yaml")
        config_bytes = self._read_document("configuration-identity.yaml")
        policy_raw = parse_two_lane_yaml(policy_bytes)
        campaign_id = policy_raw["campaign_id"]
        config_raw = parse_two_lane_yaml(config_bytes)

        # Agent-native campaigns never enter the provider loop: the coding
        # agent performs the skill itself, so the loop (which exists to gate
        # a third-party provider) is structurally the wrong surface.
        if policy_raw.get("execution_mode") == "coding_agent_native":
            raise RunnerRefusal(
                "campaign executes in coding_agent_native mode; the "
                "provider loop cannot run it - use "
                "scripts/execution_infra/agent_native_campaign.py "
                "(prepare / finalize / report)"
            )

        # Real-campaign guards BEFORE any approval parsing or validation
        # side effects: the real campaign refuses on the first unmet
        # precondition (injection, approval file, open window, pinned
        # framework checkout).
        self._guard_real_campaign(campaign_id)
        first_now = self._clock()
        self._guard_window(policy_raw, first_now)
        if campaign_id == REAL_CAMPAIGN_ID:
            self._guard_framework_checkout(policy_raw)

        approval_bytes = self._read_document(APPROVAL_FILENAME)

        context = ValidationContext(
            current_time=first_now.isoformat(),
            allowed_approver_identities=self._allowed_approver_identities,
        )
        bundle_result = validate_campaign_bundle(
            policy_bytes, approval_bytes, config_bytes, context
        )
        if not bundle_result.valid:
            raise RunnerRefusal(
                f"campaign bundle is not genuine: {bundle_result.failure_code} "
                f"{bundle_result.detail}"
            )
        bundle = bundle_result.value

        # Target checkout: for the REAL campaign, materialize (or verify)
        # the approved target BEFORE any attempt is reserved; test
        # campaigns use injected doubles and skip the target materializer.
        target: Optional[TargetCheckout] = None
        if campaign_id == REAL_CAMPAIGN_ID:
            work_root = self._target_checkout_root or (self._campaign_root / ".targets")
            target = TargetCheckout.prepare(
                target_repository=str(config_raw["target_repository"]),
                target_sha=str(config_raw["target_sha"]),
                work_root=work_root,
            )
            target.seal_read_only()

        if campaign_id == REAL_CAMPAIGN_ID:
            verifier, provider, validate = self._production_components(
                config_raw, target, bundle  # type: ignore[arg-type]
            )
        else:
            verifier, provider, validate = (
                self._verifier, self._provider, self._validate,
            )
        if provider is None or verifier is None or validate is None:
            raise RunnerRefusal(
                "test campaign requires injected verifier, provider, and "
                "validate doubles"
            )

        # Pre-flight approval corroboration BEFORE any reservation: a
        # missing GitHub token, a deleted or edited approval comment, or an
        # expired approval must surface as a refusal instead of burning an
        # attempt slot. The per-attempt mint still re-verifies, so a comment
        # revoked mid-run stops the next attempt.
        if campaign_id == REAL_CAMPAIGN_ID:
            verifier.verify(bundle.approval, approval_bytes=approval_bytes)

        max_attempts = int(policy_raw["max_attempt_slots"])
        used = self._reserved_slot_count(campaign_id)
        remaining = max_attempts - used
        if remaining <= 0:
            raise RunnerRefusal(
                f"campaign '{campaign_id}' has no remaining attempt slots: "
                f"{used} of {max_attempts} already reserved per the ledger"
            )

        manager = DurableReservationManager(self._campaign_root)
        results: list[Any] = []
        errors: list[dict[str, Any]] = []
        prompt_cache = self._skill_text() if campaign_id == REAL_CAMPAIGN_ID else None

        for _ in range(remaining):
            # 1. Real clock, re-read before EVERY attempt.
            now = self._clock()
            # 2. Window re-check: an attempt cannot begin after expiry.
            self._guard_window(policy_raw, now)
            # 3. Re-verify the approved target is still intact.
            if target is not None:
                target.verify_integrity()

            attempt_id = str(uuid.uuid4())
            request = ExploratoryAttemptRequest(
                attempt_id=attempt_id,
                campaign_id=campaign_id,
                configuration_id=bundle.configuration.configuration_id,
                intended_model=config_raw["model_identifier"],
                framework_sha=config_raw["framework_sha"],
                target_repository=config_raw["target_repository"],
                target_sha=config_raw["target_sha"],
                artifact_type=config_raw["artifact_type"],
                output_path=str(
                    self._campaign_root / campaign_id / "attempts" / attempt_id
                    / "produced-artifact.md"
                ),
                executor_id="governed-campaign-runner",
            )
            reservation = manager.reserve_attempt(
                bundle=bundle,
                attempt_id=attempt_id,
                configuration_id=bundle.configuration.configuration_id,
                request_metadata={"campaign_id": campaign_id},
                now=now,
            )
            # 5. Mint; a mint failure after the reservation must terminalize
            # the reservation, never leave an unexplained live RESERVED.
            try:
                capability = mint_exploratory_capability(
                    bundle,
                    request,
                    verifier=verifier,
                    now=now.isoformat(),
                    approval_bytes=approval_bytes,
                )
            except Exception as exc:
                recorder = AttemptOutcomeRecorder(
                    self._campaign_root, campaign_id, attempt_id
                )
                recorder.record_pre_invocation_abort(
                    reason=f"capability mint failed: {exc}", now=now
                )
                raise RunnerRefusal(
                    f"capability mint failed for attempt '{attempt_id}'; the "
                    f"reservation was terminally recorded as "
                    "ABORTED_BEFORE_INVOCATION and the run stops: "
                    f"{type(exc).__name__}: {exc}"
                ) from exc

            invocation_context = ExploratoryInvocationContext(
                model=config_raw["model_identifier"],
                target_repository=config_raw["target_repository"],
                target_sha=config_raw["target_sha"],
                framework_sha=config_raw["framework_sha"],
                artifact_type=config_raw["artifact_type"],
                output_path=request.output_path,
                campaign_id=campaign_id,
                configuration_id=bundle.configuration.configuration_id,
                configuration_snapshot_digest=compute_configuration_snapshot_digest(
                    bundle.configuration.raw, bundle.configuration.configuration_id
                ),
                policy_digest=bundle.policy.policy_digest,
                approval_digest=compute_approval_snapshot_digest(bundle.approval.raw),
                attempt_id=attempt_id,
                lane=LANE,
                campaign_root=str(self._campaign_root),
            )
            prompt = (
                prompt_cache if prompt_cache is not None else "test prompt"
            )
            if prompt_cache is not None:
                prompt = build_exploratory_prompt(
                    skill_text=prompt_cache,
                    target_repository=config_raw["target_repository"],
                    target_sha=config_raw["target_sha"],
                    expected_output_path=request.output_path,
                    artifact_type=config_raw["artifact_type"],
                )
            try:
                result = invoke_exploratory_attempt(
                    bundle=bundle,
                    capability=capability,
                    reservation=reservation,
                    campaign_root=self._campaign_root,
                    context=invocation_context,
                    provider=provider,
                    validate=validate,
                    prompt=prompt,
                    now=now,
                )
                results.append(result)
            except Exception as exc:  # noqa: BLE001 - recorded, never hidden
                errors.append({"attempt_id": attempt_id, "error": str(exc)})

            # 7. Post-attempt integrity re-checks (framework + target).
            if campaign_id == REAL_CAMPAIGN_ID and not framework_tree_unchanged(
                policy_raw["allowed_framework_shas"][0], self._framework_checkout
            ):
                raise RunnerRefusal(
                    "framework tree drifted during execution; the run "
                    "stops and the drift is reported"
                )

        summary = CampaignSummaryGenerator(self._campaign_root).update_campaign_summary(
            bundle, now=self._clock()
        )
        drift_clean = (
            framework_tree_unchanged(
                policy_raw["allowed_framework_shas"][0], self._framework_checkout
            )
            if campaign_id == REAL_CAMPAIGN_ID
            else True
        )
        target_integrity_ok = True
        if target is not None:
            try:
                target.verify_integrity()
            except Exception:  # noqa: BLE001 - recorded as drift, never hidden
                target_integrity_ok = False
        return {
            "summary": summary,
            "attempts": results,
            "errors": errors,
            "execution_module_digests": execution_module_digests(
                _EXECUTION_PACKAGE_DIR
            ),
            "framework_checkout_sha": checkout_sha(self._framework_checkout),
            "pinned_framework_sha": policy_raw["allowed_framework_shas"][0],
            "total_attempts_authorized": max_attempts,
            "drift": {
                "pre": drift_clean,
                "post": drift_clean,
                "target_integrity_ok": target_integrity_ok,
            },
            "completed_at": self._clock().isoformat(),
        }


def build_execution_report(run_result: dict[str, Any]) -> str:
    """Render the complete execution report (nothing may be omitted).

    Counts come from the LEDGER-DERIVED summary (the append-only ledger is
    authoritative): an attempt whose provider call raised is still
    enumerated as PROVIDER_FAILED in the ledger even though no result
    object was returned to the runner. Structural/substantive pass counts
    come from the per-attempt validation outcomes (the pinned
    validator's classification).
    """
    summary = run_result["summary"]
    errors = run_result["errors"]
    summary_attempts = summary.attempts

    passed = sum(1 for a in summary_attempts if a["state"] == "VALIDATION_PASSED")
    provider_failed = sum(1 for a in summary_attempts if a["state"] == "PROVIDER_FAILED")
    validation_failed = sum(1 for a in summary_attempts if a["state"] == "VALIDATION_FAILED")
    aborted = sum(1 for a in summary_attempts if a["state"] == "ABORTED_BEFORE_INVOCATION")
    interrupted = sum(1 for a in summary_attempts if a["state"] == "INVOKED")
    captured_incomplete = sum(1 for a in summary_attempts if a["state"] == "OUTPUT_CAPTURED")

    # Structural / substantive pass counts from the recorded validation
    # outcomes (details carried by the per-attempt results).
    structural_passed = 0
    structural_total = 0
    substantive_passed = 0
    substantive_total = 0
    for attempt in run_result["attempts"]:
        outcome = getattr(attempt, "validation_outcome", None) or {}
        details = outcome.get("details") or {}
        structural = details.get("structural") or {}
        substantive = details.get("substantive") or {}
        structural_total += int(structural.get("total", 0))
        structural_passed += int(structural.get("passed", 0))
        substantive_total += int(substantive.get("total", 0))
        substantive_passed += int(substantive.get("passed", 0))

    budget = summary.remaining_budget or {}
    tokens_observed = budget.get("tokens_observed", 0)
    cost_observed = budget.get("cost_observed", 0)

    def _rate(passed_n: int, total_n: int) -> str:
        if total_n <= 0:
            return "n/a (no checks)"
        return f"{passed_n}/{total_n} ({100.0 * passed_n / total_n:.1f}%)"

    lines = [
        "# EXP-0001 execution report",
        "",
        f"- campaign_id: {summary.campaign_id}",
        f"- campaign_state: {summary.campaign_state}",
        "- classification: EXPLORATORY_NOT_CANONICAL_EVIDENCE",
        f"- completed_at: {run_result['completed_at']}",
        "",
        "## Budget and accounting (ledger-derived)",
        "",
        f"- total_attempts_authorized: {run_result['total_attempts_authorized']}",
        f"- total_attempts_reserved: {summary.reservations_issued['count']}",
        f"- total_provider_invocations: {summary.provider_invocations_made}",
        f"- VALIDATION_PASSED: {passed}",
        f"- PROVIDER_FAILED: {provider_failed}",
        f"- VALIDATION_FAILED: {validation_failed}",
        f"- ABORTED_BEFORE_INVOCATION: {aborted}",
        f"- interrupted (INVOKED, never finished): {interrupted}",
        f"- captured-but-unvalidated (OUTPUT_CAPTURED): {captured_incomplete}",
        f"- runner-level errors (recorded, never hidden): {len(errors)}",
        f"- tokens_observed (post-hoc): {tokens_observed}",
        f"- cost_observed (post-hoc): {cost_observed}",
        "",
        "## Validation rates (per-attempt, pinned validator)",
        "",
        f"- structural pass: {_rate(structural_passed, structural_total)}",
        f"- substantive pass: {_rate(substantive_passed, substantive_total)}",
        "",
        "## Framework and target integrity",
        "",
        f"- pinned_framework_sha: {run_result['pinned_framework_sha']}",
        f"- framework_checkout_sha: {run_result['framework_checkout_sha']}",
        (
            f"- framework_drift: "
            f"{'NONE' if run_result['drift']['pre'] and run_result['drift']['post'] else 'DETECTED'}"
        ),
        (
            f"- target_checkout_integrity: "
            f"{'OK' if run_result['drift']['target_integrity_ok'] else 'DRIFT DETECTED'}"
        ),
        "",
        "## Execution modules (framework-governed, bound by framework_sha)",
        "",
    ]
    for name, digest in sorted(run_result["execution_module_digests"].items()):
        lines.append(f"- {name}: {digest}")
    lines += [
        "",
        "## Attempts (every attempt, every artifact path, no omissions)",
        "",
    ]
    for entry in summary.attempts:
        attempt_id = entry["attempt_id"]
        lines.append(f"- attempt {attempt_id}: state={entry['state']}")
        for artifact in ATTEMPT_ARTIFACTS:
            lines.append(
                f"    - {artifact}: experiments/campaigns/{summary.campaign_id}/"
                f"attempts/{attempt_id}/{artifact}"
            )
    for err in errors:
        lines.append(f"- runner error for {err['attempt_id']}: {err['error']}")
    lines += [
        "",
        "## Nothing-omitted statement",
        "",
        (
            "This report enumerates every reserved attempt and every "
            "terminal state recorded in the append-only campaign ledger. "
            "Failed, validation-failed, aborted, interrupted, and "
            "captured-but-unvalidated attempts are reported identically to "
            "successful ones; no attempt has been deleted, hidden, or "
            "selectively omitted, and no best-result-only summary was "
            "produced. All results are classified "
            "EXPLORATORY_NOT_CANONICAL_EVIDENCE and may not be promoted to "
            "canonical evidence."
        ),
        "",
    ]
    return "\n".join(lines) + "\n"
