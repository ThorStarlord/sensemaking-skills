"""Execution report completeness tests (Phase 6 correction, Issue #122).

The report must contain EVERY field Issue #122 requires, and an
independent agent/process must be able to reconstruct the aggregate from
the ledger alone. This suite renders the report for a full test-campaign
run and audits the rendered text field by field, then rebuilds the
aggregate by reading only the append-only ledger and compares it to the
report's own numbers.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))


from execution_infra.runner import build_execution_report
from sensemaking_skills.campaign_accounting import CampaignLedger, ProviderResponse

from test_runner import (  # shared fixtures from the runner suite
    TEST_CAMPAIGN,
    SpyProvider,
    _runner,
    _write_test_package,
)


def _run_full_campaign(tmp_path):
    pkg = _write_test_package(tmp_path, campaign_id=TEST_CAMPAIGN)
    runner = _runner(tmp_path, pkg, provider=SpyProvider())
    return runner.run(), tmp_path / "root"


REQUIRED_FIELDS = [
    "total_attempts_authorized: 3",
    "total_attempts_reserved: 3",
    "total_provider_invocations: 3",
    "VALIDATION_PASSED: 3",
    "PROVIDER_FAILED: 0",
    "VALIDATION_FAILED: 0",
    "ABORTED_BEFORE_INVOCATION: 0",
    "structural pass: n/a (no checks)",
    "substantive pass: n/a (no checks)",
    "tokens_observed (post-hoc):",
    "cost_observed (post-hoc):",
    "framework_drift:",
    "target_checkout_integrity:",
    "pinned_framework_sha:",
    "EXPLORATORY_NOT_CANONICAL_EVIDENCE",
    "Nothing-omitted statement",
    "no attempt has been deleted, hidden, or selectively omitted",
]


def test_report_contains_every_issue_122_field(tmp_path) -> None:
    result, root = _run_full_campaign(tmp_path)
    report = build_execution_report(result)
    for field in REQUIRED_FIELDS:
        assert field in report, f"report is missing: {field!r}"
    # Every attempt ID and state, plus every artifact path.
    for attempt in result["summary"].attempts:
        aid = attempt["attempt_id"]
        assert f"attempt {aid}: state={attempt['state']}" in report
        assert f"raw-output.bin: experiments/campaigns/{TEST_CAMPAIGN}/attempts/{aid}/raw-output.bin" in report
        assert f"raw-request.txt: experiments/campaigns/{TEST_CAMPAIGN}/attempts/{aid}/raw-request.txt" in report
        assert f"validation-result.json: experiments/campaigns/{TEST_CAMPAIGN}/attempts/{aid}/validation-result.json" in report
    # Classification literal.
    assert report.count("EXPLORATORY_NOT_CANONICAL_EVIDENCE") >= 2


def test_independent_ledger_reconstruction_matches_report(tmp_path) -> None:
    """A different agent reading ONLY the ledger reproduces the report's
    aggregate numbers."""
    result, root = _run_full_campaign(tmp_path)
    report = build_execution_report(result)

    ledger = CampaignLedger(root / TEST_CAMPAIGN, TEST_CAMPAIGN)
    events = ledger.read_events()

    reserved = sum(1 for e in events if e.event_type == "RESERVED")
    invoked = sum(1 for e in events if e.event_type == "INVOKED")
    passed = sum(1 for e in events if e.event_type == "VALIDATION_PASSED")
    failed = sum(1 for e in events if e.event_type == "PROVIDER_FAILED")
    val_failed = sum(1 for e in events if e.event_type == "VALIDATION_FAILED")
    aborted = sum(1 for e in events if e.event_type == "ABORTED_BEFORE_INVOCATION")

    assert f"total_attempts_reserved: {reserved}" in report
    assert f"total_provider_invocations: {invoked}" in report
    assert f"VALIDATION_PASSED: {passed}" in report
    assert f"PROVIDER_FAILED: {failed}" in report
    assert f"VALIDATION_FAILED: {val_failed}" in report
    assert f"ABORTED_BEFORE_INVOCATION: {aborted}" in report
    # Ledger attempt ids == report attempt ids (no omission).
    ledger_ids = sorted(
        {e.attempt_id for e in events if e.event_type == "RESERVED"}
    )
    for aid in ledger_ids:
        assert f"attempt {aid}: " in report


def test_failure_categories_are_enumerated_in_report(tmp_path) -> None:
    """A run with failures reports every category count truthfully."""
    pkg = _write_test_package(tmp_path, campaign_id=TEST_CAMPAIGN)

    class Mixed(SpyProvider):
        def __call__(self, *, permit, context, prompt) -> ProviderResponse:
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("boom")
            return ProviderResponse(raw_output=self.raw)

    runner = _runner(tmp_path, pkg, provider=Mixed())
    result = runner.run()
    report = build_execution_report(result)
    assert "PROVIDER_FAILED: 1" in report
    assert "VALIDATION_PASSED: 2" in report
    # The provider failure is recorded in the ledger AND re-raised to the
    # runner, so it appears both as a failure category and as a runner
    # error -- never hidden.
    assert "runner-level errors (recorded, never hidden): 1" in report


def test_report_does_not_claim_structural_rates_when_none_measured(
    tmp_path,
) -> None:
    """Honest rates: the test validator reports no structural/substantive
    checks, so the report says n/a instead of inventing numbers."""
    result, _ = _run_full_campaign(tmp_path)
    report = build_execution_report(result)
    assert "n/a (no checks)" in report
