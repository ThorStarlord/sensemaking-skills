"""EXP-0001 execution runner (Phase 6 readiness, Issue #122).

Composes the frozen framework (Phase 2 validation + Phase 3 capability +
Phase 4 durable boundary) with the injected execution infrastructure
(production verifier + real provider adapter). The runner executes the
campaign lifecycle -- reserve, mint, invoke, preserve, validate -- for
every attempt slot in the policy, with the durable Phase 4 ledger as the
authority, and produces the complete execution report (every attempt,
every terminal state, raw references, pass rate, failure categories,
observed cost/tokens, drift status, and an explicit nothing-omitted
statement).

The runner REFUSES to run the real EXP-0001 campaign unless every
precondition holds:

* the operative approval file exists and the bundle validates (policy +
  approval + configuration, exact digests);
* the injected verifier is the production signed-commit verifier (a test
  verifier can never authorize the real campaign);
* the injected provider is the real ClaudeProviderAdapter;
* the framework checkout HEAD is exactly the pinned ``framework_sha``;
* the current time is inside the policy validity window.

For any OTHER campaign id (tests, experiments), the runner accepts
injected doubles -- the real-campaign guards are keyed on the campaign id
of the package being run, so a dry run on a test campaign can never touch
the real campaign.

The runner never fabricates approval, never calls the provider outside
the Phase 4 boundary, and never hides an attempt.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

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
from sensemaking_skills.campaign_accounting import (
    CampaignSummaryGenerator,
    DurableReservationManager,
    invoke_exploratory_attempt,
)

from execution_infra.production_verifier import ProductionSignedCommitVerifier
from execution_infra.provider_adapter import ClaudeProviderAdapter
from execution_infra.versions import adapter_versions, checkout_sha, framework_code_unchanged

REAL_CAMPAIGN_ID = "EXP-0001-stage1-auteur-autonomy-pilot"
APPROVAL_FILENAME = "approval.yaml"
LANE = "EXPLORATORY"


class RunnerRefusal(Exception):
    """The runner refuses to execute; nothing was reserved or invoked."""


class Exp0001Runner:
    """Run the campaign lifecycle for a campaign package."""

    def __init__(
        self,
        *,
        campaign_package_dir: Path,
        campaign_root: Path,
        framework_checkout: Path,
        verifier: Any,
        provider: Callable[[], bytes],
        validate: Callable[[bytes], Any],
        allowed_approver_identities: Optional[frozenset] = None,
        now: Optional[datetime] = None,
    ) -> None:
        self._package_dir = Path(campaign_package_dir)
        self._campaign_root = Path(campaign_root)
        self._framework_checkout = Path(framework_checkout)
        self._verifier = verifier
        self._provider = provider
        self._validate = validate
        # Fail closed: with an empty allowlist no approval can ever
        # validate. The operator supplies the genuine approver identity.
        self._allowed_approver_identities = (
            allowed_approver_identities if allowed_approver_identities is not None
            else frozenset()
        )
        self._now = now or datetime.now(timezone.utc)

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
        if not (self._package_dir / APPROVAL_FILENAME).is_file():
            # The real approval file may only exist once a human created it.
            raise RunnerRefusal(
                f"refusing to run the real campaign: no operative approval "
                f"at {self._package_dir / APPROVAL_FILENAME}; approval is a "
                "human act, never inferred from merge or ownership"
            )
        if not isinstance(self._verifier, ProductionSignedCommitVerifier):
            raise RunnerRefusal(
                "refusing to run the real EXP-0001 campaign with a "
                "non-production verifier"
            )
        if not isinstance(self._provider, ClaudeProviderAdapter):
            raise RunnerRefusal(
                "refusing to run the real EXP-0001 campaign with a "
                "non-production provider adapter"
            )

    def _guard_window(self, policy_raw: Dict[str, Any]) -> None:
        window = policy_raw["validity_window"]
        not_before = datetime.fromisoformat(window["not_before"])
        not_after = datetime.fromisoformat(window["not_after"])
        if self._now < not_before:
            raise RunnerRefusal(
                f"validity window has not opened: now={self._now.isoformat()} "
                f"< not_before={window['not_before']}"
            )
        if self._now >= not_after:
            raise RunnerRefusal(
                f"validity window has expired: now={self._now.isoformat()} "
                f">= not_after={window['not_after']}"
            )

    def _guard_framework_checkout(self, policy_raw: Dict[str, Any]) -> None:
        pinned = policy_raw["allowed_framework_shas"][0]
        actual = checkout_sha(self._framework_checkout)
        if actual != pinned:
            raise RunnerRefusal(
                f"framework checkout HEAD {actual} is not the pinned "
                f"framework_sha {pinned}; refusing to run with a "
                "mislabeled framework commit"
            )
        if not framework_code_unchanged(pinned, self._framework_checkout):
            raise RunnerRefusal(
                f"framework code at {actual} differs from the pinned "
                f"{pinned}; execution would use unapproved framework bytes"
            )

    # ------------------------------------------------------------------ #
    # The lifecycle
    # ------------------------------------------------------------------ #

    def run(self) -> Dict[str, Any]:
        """Validate preconditions and run every attempt slot."""
        policy_bytes = self._read_document("campaign-policy.yaml")
        config_bytes = self._read_document("configuration-identity.yaml")
        policy_raw = parse_two_lane_yaml(policy_bytes)
        campaign_id = policy_raw["campaign_id"]
        config_raw = parse_two_lane_yaml(config_bytes)

        # Real-campaign guards BEFORE any approval parsing or validation
        # side effects: the real campaign refuses on the first unmet
        # precondition (approval file, production verifier, production
        # provider, open window, pinned framework checkout).
        self._guard_real_campaign(campaign_id)
        self._guard_window(policy_raw)
        if campaign_id == REAL_CAMPAIGN_ID:
            self._guard_framework_checkout(policy_raw)

        approval_bytes = self._read_document(APPROVAL_FILENAME)

        context = ValidationContext(
            current_time=self._now.isoformat(),
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

        max_attempts = int(policy_raw["max_attempt_slots"])
        manager = DurableReservationManager(self._campaign_root)
        results: List[Any] = []
        errors: List[Dict[str, Any]] = []

        for _ in range(max_attempts):
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
                executor_id="exp0001-runner",
            )
            reservation = manager.reserve_attempt(
                bundle=bundle,
                attempt_id=attempt_id,
                configuration_id=bundle.configuration.configuration_id,
                request_metadata={"campaign_id": campaign_id},
                now=self._now,
            )
            capability = mint_exploratory_capability(
                bundle, request, verifier=self._verifier, now=self._now.isoformat()
            )
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
            )
            try:
                result = invoke_exploratory_attempt(
                    bundle=bundle,
                    capability=capability,
                    reservation=reservation,
                    campaign_root=self._campaign_root,
                    context=invocation_context,
                    provider=self._provider,
                    validate=self._validate,
                    now=self._now,
                )
                results.append(result)
            except Exception as exc:  # noqa: BLE001 - recorded, never hidden
                errors.append({"attempt_id": attempt_id, "error": str(exc)})

        summary = CampaignSummaryGenerator(self._campaign_root).update_campaign_summary(
            bundle, now=self._now
        )
        return {
            "summary": summary,
            "attempts": results,
            "errors": errors,
            "infra_versions": adapter_versions(Path(__file__).parent),
            "framework_checkout_sha": checkout_sha(self._framework_checkout),
            "pinned_framework_sha": policy_raw["allowed_framework_shas"][0],
            "completed_at": self._now.isoformat(),
        }


def build_execution_report(run_result: Dict[str, Any]) -> str:
    """Render the complete execution report (nothing may be omitted).

    Counts come from the LEDGER-DERIVED summary (the append-only ledger is
    authoritative): an attempt whose provider call raised is still
    enumerated as PROVIDER_FAILED in the ledger even though no result
    object was returned to the runner.
    """
    summary = run_result["summary"]
    errors = run_result["errors"]
    summary_attempts = summary.attempts

    passed = sum(1 for a in summary_attempts if a["state"] == "VALIDATION_PASSED")
    provider_failed = sum(1 for a in summary_attempts if a["state"] == "PROVIDER_FAILED")
    validation_failed = sum(1 for a in summary_attempts if a["state"] == "VALIDATION_FAILED")
    aborted = sum(1 for a in summary_attempts if a["state"] == "ABORTED_BEFORE_INVOCATION")

    lines = [
        "# EXP-0001 execution report",
        "",
        f"- campaign_id: {summary.campaign_id}",
        f"- campaign_state: {summary.campaign_state}",
        f"- completed_at: {run_result['completed_at']}",
        f"- pinned_framework_sha: {run_result['pinned_framework_sha']}",
        f"- framework_checkout_sha: {run_result['framework_checkout_sha']}",
        (
            f"- framework_drift: "
            f"{'NONE (checkout matches pin)' if run_result['framework_checkout_sha'] == run_result['pinned_framework_sha'] else 'DETECTED'}"
        ),
        "",
        "## Infrastructure versions (outside campaign configuration)",
        "",
    ]

    for name, digest in sorted(run_result["infra_versions"].items()):
        lines.append(f"- {name}: {digest}")
    lines += [
        "",
        "## Attempts (every attempt, no omissions)",
        "",
        f"- reservations_issued: {summary.reservations_issued['count']}",
        f"- provider_invocations_made: {summary.provider_invocations_made}",
        f"- VALIDATION_PASSED: {passed}",
        f"- PROVIDER_FAILED: {provider_failed}",
        f"- VALIDATION_FAILED: {validation_failed}",
        f"- ABORTED_BEFORE_INVOCATION: {aborted}",
        f"- runner-level errors (recorded, never hidden): {len(errors)}",
        "",
    ]
    for entry in summary.attempts:
        lines.append(
            f"- attempt {entry['attempt_id']}: state={entry['state']} "
            f"configuration={entry['configuration_id'][:12]}..."
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
            "Failed, validation-failed, and aborted attempts are reported "
            "identically to successful ones; no attempt has been deleted, "
            "hidden, or selectively omitted, and no best-result-only "
            "summary was produced."
        ),
        "",
    ]
    return "\n".join(lines) + "\n"
