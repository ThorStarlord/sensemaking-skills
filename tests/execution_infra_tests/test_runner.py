"""Exp0001Runner tests (Issue #122).

The runner must refuse the REAL campaign unless every Phase 6 precondition
holds (approval file, production verifier, production provider, pinned
framework checkout, open window), and must run the full lifecycle only for
test campaigns with injected doubles -- proving the lifecycle without ever
touching the real campaign, a real provider, or a real approval.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from exploratory_fixtures import (
    TEST_APPROVER_IDENTITY,
    TEST_FRAMEWORK_SHA,
    TrustedReferenceProvenanceVerifier,
    build_approval_raw,
    build_configuration_raw,
    build_policy_raw,
    render_yaml,
)

from execution_infra.production_verifier import ProductionSignedCommitVerifier
from execution_infra.provider_adapter import ClaudeProviderAdapter
from execution_infra.runner import APPROVAL_FILENAME, REAL_CAMPAIGN_ID, Exp0001Runner, RunnerRefusal

from sensemaking_skills.campaign_accounting import (
    AttemptState,
    ValidationOutcome,
)

# Window for the test campaign: anchored to the fixture anchor, always open.
from exploratory_fixtures import _ANCHOR_NOW

NOT_BEFORE = (_ANCHOR_NOW - timedelta(days=1)).isoformat()
NOT_AFTER = (_ANCHOR_NOW + timedelta(days=30)).isoformat()
TEST_CAMPAIGN = "EXP-9001-infra-test"
FRAMEWORK_PIN = "4ba049e04e74699a009147df112baed3f7536343"


class SpyProvider:
    def __init__(self, raw: bytes = b"raw provider output"):
        self.raw = raw
        self.calls = 0

    def __call__(self) -> bytes:
        self.calls += 1
        return self.raw


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
    pkg.mkdir()
    (pkg / "campaign-policy.yaml").write_bytes(render_yaml(policy_raw))
    (pkg / "configuration-identity.yaml").write_bytes(render_yaml(config_raw))
    (pkg / APPROVAL_FILENAME).write_bytes(render_yaml(approval_raw))
    return pkg


def _passing_validate(raw: bytes) -> ValidationOutcome:
    return ValidationOutcome(passed=True, details={}, artifact_content="# ok")


# ---------------------------------------------------------------------------
# Real-campaign guards (refusal paths only -- acceptance needs human approval)
# ---------------------------------------------------------------------------


def test_real_campaign_refuses_without_approval_file(tmp_path: Path) -> None:
    pkg = _write_test_package(tmp_path, campaign_id=REAL_CAMPAIGN_ID)
    (pkg / APPROVAL_FILENAME).unlink()  # no operative approval
    adapter = ClaudeProviderAdapter(
        framework_checkout=Path(__file__).resolve().parents[2],
        target_repository="https://github.com/ThorStarlord/auteur.git",
        target_sha="0" * 40,
    )
    runner = Exp0001Runner(
        campaign_package_dir=pkg,
        campaign_root=tmp_path / "root",
        framework_checkout=Path(__file__).resolve().parents[2],
        verifier=ProductionSignedCommitVerifier(tmp_path),
        provider=adapter,
        validate=_passing_validate,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        now=_ANCHOR_NOW,
    )
    with pytest.raises(RunnerRefusal) as exc:
        runner.run()
    assert "no operative approval" in str(exc.value)


def test_real_campaign_refuses_test_verifier(tmp_path: Path) -> None:
    pkg = _write_test_package(tmp_path, campaign_id=REAL_CAMPAIGN_ID)
    runner = Exp0001Runner(
        campaign_package_dir=pkg,
        campaign_root=tmp_path / "root",
        framework_checkout=Path(__file__).resolve().parents[2],
        verifier=TrustedReferenceProvenanceVerifier(),
        provider=SpyProvider(),
        validate=_passing_validate,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        now=_ANCHOR_NOW,
    )
    with pytest.raises(RunnerRefusal) as exc:
        runner.run()
    assert "non-production verifier" in str(exc.value)


def test_real_campaign_refuses_test_provider(tmp_path: Path) -> None:
    pkg = _write_test_package(tmp_path, campaign_id=REAL_CAMPAIGN_ID)
    runner = Exp0001Runner(
        campaign_package_dir=pkg,
        campaign_root=tmp_path / "root",
        framework_checkout=Path(__file__).resolve().parents[2],
        verifier=ProductionSignedCommitVerifier(tmp_path),
        provider=SpyProvider(),
        validate=_passing_validate,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        now=_ANCHOR_NOW,
    )
    with pytest.raises(RunnerRefusal) as exc:
        runner.run()
    assert "non-production provider adapter" in str(exc.value)


def test_real_campaign_refuses_closed_window(tmp_path: Path) -> None:
    # The REAL package's frozen window starts 2026-08-07; any earlier now
    # must refuse. Use a temp copy of the real package plus an approval
    # file so the window guard (not the approval guard) fires.
    import shutil
    real_pkg = (
        Path(__file__).resolve().parents[2]
        / "experiments" / "campaigns" / REAL_CAMPAIGN_ID
    )
    pkg = tmp_path / "real-pkg"
    shutil.copytree(real_pkg, pkg)
    (pkg / APPROVAL_FILENAME).write_bytes(b"placeholder: existence is checked first")
    adapter = ClaudeProviderAdapter(
        framework_checkout=Path(__file__).resolve().parents[2],
        target_repository="https://github.com/ThorStarlord/auteur.git",
        target_sha="0" * 40,
    )
    runner = Exp0001Runner(
        campaign_package_dir=pkg,
        campaign_root=tmp_path / "root",
        framework_checkout=Path(__file__).resolve().parents[2],
        verifier=ProductionSignedCommitVerifier(tmp_path),
        provider=adapter,
        validate=_passing_validate,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        now=datetime.fromisoformat("2026-08-06T00:00:00+00:00"),  # before not_before
    )
    with pytest.raises(RunnerRefusal) as exc:
        runner.run()
    assert "has not opened" in str(exc.value)


def test_real_campaign_refuses_unpinned_framework_checkout(tmp_path: Path) -> None:
    pkg = _write_test_package(tmp_path, campaign_id=REAL_CAMPAIGN_ID)
    adapter = ClaudeProviderAdapter(
        framework_checkout=Path(__file__).resolve().parents[2],
        target_repository="https://github.com/ThorStarlord/auteur.git",
        target_sha="0" * 40,
    )
    runner = Exp0001Runner(
        campaign_package_dir=pkg,
        campaign_root=tmp_path / "root",
        framework_checkout=Path(__file__).resolve().parents[2],  # HEAD != pin
        verifier=ProductionSignedCommitVerifier(tmp_path),
        provider=adapter,
        validate=_passing_validate,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        now=datetime.fromisoformat("2026-08-08T00:00:00+00:00"),
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
    runner = Exp0001Runner(
        campaign_package_dir=pkg,
        campaign_root=campaign_root,
        framework_checkout=Path(__file__).resolve().parents[2],
        verifier=TrustedReferenceProvenanceVerifier(),
        provider=provider,
        validate=_passing_validate,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        now=_ANCHOR_NOW,
    )

    result = runner.run()

    summary = result["summary"]
    assert summary.campaign_id == TEST_CAMPAIGN
    assert summary.reservations_issued["count"] == 3
    assert summary.provider_invocations_made == 3
    assert len(summary.attempts) == 3
    assert all(a["state"] == AttemptState.VALIDATION_PASSED.value
               for a in summary.attempts)
    # Three DISTINCT attempt IDs -- three independent observations.
    ids = {a["attempt_id"] for a in summary.attempts}
    assert len(ids) == 3
    assert provider.calls == 3

    # Execution record: infra versions + framework identity + no errors.
    # The test campaign pins the fixture framework SHA (not the real pin).
    assert result["errors"] == []
    assert result["pinned_framework_sha"] == TEST_FRAMEWORK_SHA
    assert "runner.py" in result["infra_versions"]
    assert len(result["infra_versions"]["runner.py"]) == 64

    # No runtime state leaks outside the test campaign root.
    assert not (tmp_path / "root" / REAL_CAMPAIGN_ID).exists()


def test_execution_report_enumerates_every_attempt(tmp_path: Path) -> None:
    pkg = _write_test_package(tmp_path, campaign_id=TEST_CAMPAIGN)
    provider = SpyProvider()
    runner = Exp0001Runner(
        campaign_package_dir=pkg,
        campaign_root=tmp_path / "root",
        framework_checkout=Path(__file__).resolve().parents[2],
        verifier=TrustedReferenceProvenanceVerifier(),
        provider=provider,
        validate=_passing_validate,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        now=_ANCHOR_NOW,
    )
    result = runner.run()

    from execution_infra.runner import build_execution_report
    report = build_execution_report(result)
    assert "## Attempts (every attempt, no omissions)" in report
    assert "## Nothing-omitted statement" in report
    assert "reservations_issued: 3" in report
    for a in result["summary"].attempts:
        assert a["attempt_id"] in report
    assert "framework_drift:" in report
    # Failed attempts would be enumerated identically (no success-only mode).
    assert "PROVIDER_FAILED: 0" in report


def test_failed_attempts_are_reported_not_hidden(tmp_path: Path) -> None:
    """A failing attempt is recorded and reported, never concealed."""
    pkg = _write_test_package(tmp_path, campaign_id=TEST_CAMPAIGN)
    class FailingProvider(SpyProvider):
        """Fails exactly once, then succeeds: a real provider failure."""
        def __init__(self):
            super().__init__()
            self._failures_left = 1

        def __call__(self) -> bytes:
            self.calls += 1
            if self._failures_left > 0:
                self._failures_left -= 1
                raise RuntimeError("provider exploded")
            return self.raw

    failing = FailingProvider()
    runner = Exp0001Runner(
        campaign_package_dir=pkg,
        campaign_root=tmp_path / "root",
        framework_checkout=Path(__file__).resolve().parents[2],
        verifier=TrustedReferenceProvenanceVerifier(),
        provider=failing,
        validate=_passing_validate,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        now=_ANCHOR_NOW,
    )
    result = runner.run()
    summary = result["summary"]
    states = {a["state"] for a in summary.attempts}
    assert AttemptState.PROVIDER_FAILED.value in states
    assert AttemptState.VALIDATION_PASSED.value in states
    assert len(summary.attempts) == 3
    # The failed attempts consumed their slots: no hidden fourth attempt.
    assert summary.reservations_issued["count"] == 3

    from execution_infra.runner import build_execution_report
    report = build_execution_report(result)
    assert "PROVIDER_FAILED: 1" in report or "PROVIDER_FAILED: 2" in report
