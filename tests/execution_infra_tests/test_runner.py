"""GovernedCampaignRunner tests (Phase 6 correction, Issue #122).

The runner must refuse the REAL campaign unless every precondition holds
(no injected components, approval file present, pinned+clean framework
checkout, open window, verified target), and must run the full lifecycle
for test campaigns with injected doubles -- proving the lifecycle without
ever touching the real campaign, a real provider, or a real approval.

Lifecycle proofs:

* ledger-derived remaining slots (a resumed run never re-attempts used
  slots);
* mint failure after reservation -> durable ABORTED_BEFORE_INVOCATION and
  the run stops;
* the clock is re-read before EVERY attempt (an attempt cannot begin
  after expiry);
* every reserved attempt is enumerated in the ledger and the report.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from execution_infra.runner import (
    APPROVAL_FILENAME,
    REAL_CAMPAIGN_ID,
    GovernedCampaignRunner,
    RunnerRefusal,
    build_execution_report,
)
from exploratory_fixtures import (
    _ANCHOR_NOW,
    TEST_APPROVER_IDENTITY,
    TrustedReferenceProvenanceVerifier,
    build_approval_raw,
    build_configuration_raw,
    build_policy_raw,
    render_yaml,
)

from sensemaking_skills.campaign_accounting import (
    AttemptState,
    CampaignLedger,
    ProviderResponse,
    ValidationOutcome,
)

NOT_BEFORE = (_ANCHOR_NOW - timedelta(days=1)).isoformat()
NOT_AFTER = (_ANCHOR_NOW + timedelta(days=30)).isoformat()
TEST_CAMPAIGN = "EXP-9001-infra-test"
FRAMEWORK_PIN = "4ba049e04e74699a009147df112baed3f7536343"


class SpyProvider:
    def __init__(self, raw: bytes = b"raw provider output"):
        self.raw = raw
        self.calls = 0

    def __call__(self, *, permit, context, prompt) -> ProviderResponse:
        self.calls += 1
        return ProviderResponse(raw_output=self.raw)


def _write_test_package(tmp_path: Path, *, campaign_id: str) -> Path:
    """Write a genuine fixture-based campaign package into a temp dir."""
    policy_raw = build_policy_raw(
        campaign_id=campaign_id,
        max_attempts_per_configuration=3,
        validity_window={"not_before": NOT_BEFORE, "not_after": NOT_AFTER},
    )
    config_raw = build_configuration_raw(campaign_id=campaign_id)
    policy_raw["allowed_configuration_ids"] = sorted([config_raw["configuration_id"]])
    from sensemaking_skills.campaign_validation import compute_policy_digest
    policy_raw["policy_digest"] = compute_policy_digest(policy_raw)
    approval_raw = build_approval_raw(
        campaign_id=campaign_id,
        policy_digest=policy_raw["policy_digest"],
        mechanism="signed_commit",
    )

    pkg = tmp_path / "package"
    pkg.mkdir(parents=True)
    (pkg / "campaign-policy.yaml").write_bytes(render_yaml(policy_raw))
    (pkg / "configuration-identity.yaml").write_bytes(render_yaml(config_raw))
    (pkg / APPROVAL_FILENAME).write_bytes(render_yaml(approval_raw))
    return pkg


def _passing_validate(raw: bytes) -> ValidationOutcome:
    return ValidationOutcome(passed=True, details={}, artifact_content="# ok")


def _runner(tmp_path, pkg, *, verifier=None, provider=None, validate=None,
            clock=None, campaign_root=None):
    return GovernedCampaignRunner(
        campaign_package_dir=pkg,
        campaign_root=campaign_root or (tmp_path / "root"),
        framework_checkout=Path(__file__).resolve().parents[2],
        verifier=verifier if verifier is not None else TrustedReferenceProvenanceVerifier(),
        provider=provider if provider is not None else SpyProvider(),
        validate=validate if validate is not None else _passing_validate,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        clock=clock,
    )


# ---------------------------------------------------------------------------
# Real-campaign guards (refusal paths only -- acceptance needs human approval)
# ---------------------------------------------------------------------------


def test_real_campaign_refuses_injected_components(tmp_path: Path) -> None:
    """The real campaign accepts NO caller-supplied execution component:
    injection itself is the refusal reason."""
    pkg = _write_test_package(tmp_path, campaign_id=REAL_CAMPAIGN_ID)
    (pkg / APPROVAL_FILENAME).write_bytes(b"placeholder: existence is checked first")
    runner = _runner(tmp_path, pkg, verifier=TrustedReferenceProvenanceVerifier())
    with pytest.raises(RunnerRefusal) as exc:
        runner.run()
    assert "injected execution components" in str(exc.value)


def test_real_campaign_refuses_without_approval_file(tmp_path: Path) -> None:
    pkg = _write_test_package(tmp_path, campaign_id=REAL_CAMPAIGN_ID)
    (pkg / APPROVAL_FILENAME).unlink()  # no operative approval
    # No injected components: the approval-file guard must fire.
    runner = GovernedCampaignRunner(
        campaign_package_dir=pkg,
        campaign_root=tmp_path / "root",
        framework_checkout=Path(__file__).resolve().parents[2],
        verifier=None,
        provider=None,
        validate=None,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
    )
    with pytest.raises(RunnerRefusal) as exc:
        runner.run()
    assert "no operative approval" in str(exc.value)


def test_real_campaign_refuses_closed_window(tmp_path: Path) -> None:
    """The REAL package's frozen window starts 2026-08-07; an earlier now
    must refuse. Use a temp copy of the real package plus an approval
    file so the window guard (not the approval guard) fires."""
    import shutil
    real_pkg = (
        Path(__file__).resolve().parents[2]
        / "experiments" / "campaigns" / REAL_CAMPAIGN_ID
    )
    pkg = tmp_path / "real-pkg"
    shutil.copytree(real_pkg, pkg)
    (pkg / APPROVAL_FILENAME).write_bytes(b"placeholder: existence is checked first")
    runner = GovernedCampaignRunner(
        campaign_package_dir=pkg,
        campaign_root=tmp_path / "root",
        framework_checkout=Path(__file__).resolve().parents[2],
        verifier=None,
        provider=None,
        validate=None,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        clock=lambda: datetime.fromisoformat("2026-08-06T00:00:00+00:00"),
    )
    with pytest.raises(RunnerRefusal) as exc:
        runner.run()
    assert "has not opened" in str(exc.value)


def test_real_campaign_refuses_unpinned_framework_checkout(tmp_path: Path) -> None:
    pkg = _write_test_package(tmp_path, campaign_id=REAL_CAMPAIGN_ID)
    (pkg / APPROVAL_FILENAME).write_bytes(b"placeholder")
    runner = GovernedCampaignRunner(
        campaign_package_dir=pkg,
        campaign_root=tmp_path / "root",
        framework_checkout=Path(__file__).resolve().parents[2],  # HEAD != pin
        verifier=None,
        provider=None,
        validate=None,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        clock=lambda: datetime.fromisoformat("2026-08-08T00:00:00+00:00"),
    )
    with pytest.raises(RunnerRefusal) as exc:
        runner.run()
    assert "not the pinned" in str(exc.value)


# ---------------------------------------------------------------------------
# Test-campaign dry run: the full lifecycle with injected doubles
# ---------------------------------------------------------------------------


def test_test_campaign_full_lifecycle(tmp_path: Path) -> None:
    pkg = _write_test_package(tmp_path, campaign_id=TEST_CAMPAIGN)
    campaign_root = tmp_path / "root"
    provider = SpyProvider()
    runner = _runner(tmp_path, pkg, provider=provider, campaign_root=campaign_root)

    result = runner.run()

    summary = result["summary"]
    assert summary.campaign_id == TEST_CAMPAIGN
    assert summary.reservations_issued["count"] == 3
    assert summary.provider_invocations_made == 3
    assert len(summary.attempts) == 3
    assert all(a["state"] == AttemptState.VALIDATION_PASSED.value
               for a in summary.attempts)
    ids = {a["attempt_id"] for a in summary.attempts}
    assert len(ids) == 3
    assert provider.calls == 3

    assert result["errors"] == []
    assert result["total_attempts_authorized"] == 3
    assert result["drift"]["pre"] is True
    assert result["drift"]["post"] is True
    assert "claude_provider.py" in result["execution_module_digests"]

    # No runtime state leaks outside the test campaign root.
    assert not (tmp_path / "root" / REAL_CAMPAIGN_ID).exists()


def test_resume_derives_remaining_slots_from_ledger(tmp_path: Path) -> None:
    """A prior partial run already consumed slots; a resumed run must NOT
    blindly begin another three-attempt loop."""
    pkg = _write_test_package(tmp_path, campaign_id=TEST_CAMPAIGN)
    campaign_root = tmp_path / "root"

    class FailingFirst(SpyProvider):
        def __call__(self, *, permit, context, prompt) -> ProviderResponse:
            self.calls += 1
            raise RuntimeError("provider exploded")

    first = FailingFirst()
    runner1 = _runner(tmp_path, pkg, provider=first, campaign_root=campaign_root)
    result1 = runner1.run()
    assert result1["summary"].reservations_issued["count"] == 3
    assert result1["summary"].provider_invocations_made == 3

    # Now resume: the ledger shows 3 reservations already -> zero remaining.
    provider2 = SpyProvider()
    runner2 = _runner(tmp_path, pkg, provider=provider2, campaign_root=campaign_root)
    with pytest.raises(RunnerRefusal) as exc:
        runner2.run()
    assert "no remaining attempt slots" in str(exc.value)
    assert provider2.calls == 0

    # A HALF-consumed campaign: 1 reservation pre-existing -> 2 remaining.
    pkg3 = _write_test_package(tmp_path / "pkg3", campaign_id=TEST_CAMPAIGN)
    root3 = tmp_path / "root3"
    # Manually consume ONE slot so the ledger has 1 reservation.
    from exploratory_fixtures import build_request

    from sensemaking_skills.campaign_accounting import DurableReservationManager
    from sensemaking_skills.campaign_validation import parse_two_lane_yaml
    from sensemaking_skills.exploratory_authorization import mint_exploratory_capability
    policy_bytes = (pkg3 / "campaign-policy.yaml").read_bytes()
    config_bytes = (pkg3 / "configuration-identity.yaml").read_bytes()
    approval_bytes = (pkg3 / APPROVAL_FILENAME).read_bytes()
    from sensemaking_skills.campaign_validation import validate_campaign_bundle
    from sensemaking_skills.campaign_validation.models import ValidationContext
    ctx = ValidationContext(
        current_time=_ANCHOR_NOW.isoformat(),
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
    )
    bundle = validate_campaign_bundle(policy_bytes, approval_bytes, config_bytes, ctx).value
    config_raw = parse_two_lane_yaml(config_bytes)
    import uuid as _uuid
    aid = str(_uuid.uuid4())
    manager = DurableReservationManager(root3)
    manager.reserve_attempt(
        bundle=bundle, attempt_id=aid,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": TEST_CAMPAIGN}, now=_ANCHOR_NOW,
    )
    mint_exploratory_capability(
        bundle,
        build_request(attempt_id=aid, campaign_id=TEST_CAMPAIGN,
                      configuration_id=bundle.configuration.configuration_id),
        verifier=TrustedReferenceProvenanceVerifier(), now=_ANCHOR_NOW.isoformat(),
    )
    # The reserved-but-never-invoked attempt is terminalized by recovery
    # on the next run? No: the runner derives remaining slots from the
    # ledger; the reservation consumes a slot either way.
    from sensemaking_skills.campaign_accounting import AttemptRecovery
    AttemptRecovery(root3).recover_uninvoked_reservations(TEST_CAMPAIGN, now=_ANCHOR_NOW)

    runner4 = GovernedCampaignRunner(
        campaign_package_dir=pkg3,
        campaign_root=root3,
        framework_checkout=Path(__file__).resolve().parents[2],
        verifier=TrustedReferenceProvenanceVerifier(),
        provider=SpyProvider(),
        validate=_passing_validate,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
    )
    result4 = runner4.run()
    assert result4["summary"].reservations_issued["count"] == 3  # 1 + 2
    assert result4["summary"].provider_invocations_made == 2


def test_mint_failure_records_abort_and_stops(tmp_path: Path) -> None:
    """A capability mint failure after the reservation must terminalize the
    reservation as ABORTED_BEFORE_INVOCATION and stop the run -- never
    leave an unexplained live RESERVED attempt."""
    pkg = _write_test_package(tmp_path, campaign_id=TEST_CAMPAIGN)
    campaign_root = tmp_path / "root"

    class ExplodingVerifier:
        def verify(self, approval, *, approval_bytes=None):
            from sensemaking_skills.exploratory_authorization.provenance import (
                ProvenanceVerificationError,
            )
            raise ProvenanceVerificationError("verifier exploded at mint")

    runner = _runner(tmp_path, pkg, verifier=ExplodingVerifier(),
                     campaign_root=campaign_root)
    with pytest.raises(RunnerRefusal) as exc:
        runner.run()
    assert "capability mint failed" in str(exc.value)

    ledger = CampaignLedger(campaign_root / TEST_CAMPAIGN, TEST_CAMPAIGN)
    states = [e.event_type for e in ledger.read_events()]
    assert states == ["RESERVED", "ABORTED_BEFORE_INVOCATION"]
    # The provider was never entered.
    assert "INVOKED" not in states


def test_clock_is_reread_before_every_attempt(tmp_path: Path) -> None:
    """The window is checked against the CURRENT time before EVERY attempt:
    a frozen start-time cannot authorize an attempt after expiry."""
    pkg = _write_test_package(tmp_path, campaign_id=TEST_CAMPAIGN)
    campaign_root = tmp_path / "root"
    times = iter(
        [
            _ANCHOR_NOW,                                   # pre-run guard: open
            _ANCHOR_NOW,                                   # attempt 1: open
            _ANCHOR_NOW + timedelta(days=31),              # attempt 2: EXPIRED
        ]
    )

    def fake_clock():
        return next(times)

    runner = _runner(tmp_path, pkg, clock=fake_clock, campaign_root=campaign_root)
    with pytest.raises(RunnerRefusal) as exc:
        runner.run()
    assert "window has expired" in str(exc.value)

    ledger = CampaignLedger(campaign_root / TEST_CAMPAIGN, TEST_CAMPAIGN)
    states = [e.event_type for e in ledger.read_events()]
    # Exactly ONE attempt was reserved before the expiry refusal.
    assert states.count("RESERVED") == 1
    assert states.count("INVOKED") == 1


def test_failed_attempts_are_reported_not_hidden(tmp_path: Path) -> None:
    """A failing attempt is recorded and reported, never concealed."""
    pkg = _write_test_package(tmp_path, campaign_id=TEST_CAMPAIGN)

    class FailingProvider(SpyProvider):
        def __call__(self, *, permit, context, prompt) -> ProviderResponse:
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("provider exploded")
            return ProviderResponse(raw_output=self.raw)

    failing = FailingProvider()
    runner = _runner(tmp_path, pkg, provider=failing)
    result = runner.run()

    summary = result["summary"]
    states = {a["state"] for a in summary.attempts}
    assert AttemptState.PROVIDER_FAILED.value in states
    assert AttemptState.VALIDATION_PASSED.value in states
    assert len(summary.attempts) == 3
    assert summary.reservations_issued["count"] == 3

    report = build_execution_report(result)
    assert "PROVIDER_FAILED: 1" in report or "PROVIDER_FAILED: 2" in report
