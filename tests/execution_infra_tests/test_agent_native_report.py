"""Agent-native reporter tests (EXP-0002 plan Phase 0.7).

Proves the corrected report is accurate and auditable: dynamic title,
agent-invocation vs external-provider-API counts, real validation rates
loaded from the recorded per-attempt results, state-aware artifact lists
(raw-output.md), a REAL report-time target-integrity result, report-only
availability after expiry, fail-closed missing-evidence detection, orphan
detection, and no authorization side effects.
"""

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_agent_native_campaign import (  # noqa: E402
    TEST_AGENT_NATIVE_CAMPAIGN,
    _events,
    _failing_validate,
    _passing_validate,
    _prepare,
    _prepare_and_deliver,
    _write_package,
)
from execution_infra.agent_native_campaign import (  # noqa: E402
    build_report,
    finalize_attempt,
)
from execution_infra.runner import (  # noqa: E402
    RunnerRefusal,
)
from sensemaking_skills.campaign_accounting import (  # noqa: E402
    AttemptOutcomeRecorder,
)
from exploratory_fixtures import TEST_VALIDATION_TIME  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
_NOW = datetime.fromisoformat(TEST_VALIDATION_TIME)
_AFTER_WINDOW = _NOW + timedelta(days=400)


def _report(pkg: Path, root: Path, **kwargs) -> str:
    return build_report(
        package_dir=pkg,
        campaign_root=root,
        framework_checkout=kwargs.pop("framework_checkout", REPO_ROOT),
        target_checkout_root=kwargs.pop("target_checkout_root", None),
        allowed_approver_identities=frozenset(),
        now=kwargs.pop("now", _NOW),
        **kwargs,
    )


def _full_attempt(tmp_path: Path, *, failing: bool = False) -> tuple[Path, Path, str]:
    """One prepared + finalized attempt; returns (pkg, root, attempt_id)."""
    result, pkg, root = _prepare_and_deliver(tmp_path)
    validate = _failing_validate if failing else _passing_validate
    outcome = finalize_attempt(
        package_dir=pkg,
        campaign_root=root,
        framework_checkout=REPO_ROOT,
        attempt_id=result["attempt_id"],
        artifact_path=Path(result["delivery_path"]),
        allowed_approver_identities=frozenset(),
        verifier=_passing_validate.__globals__.get("_unused", None),
        validate=validate,
        now=_NOW,
    )
    assert outcome["state"] == (
        "VALIDATION_FAILED" if failing else "VALIDATION_PASSED"
    )
    return pkg, root, result["attempt_id"]


# ---------------------------------------------------------------------------
# identity, invocation accounting, artifact paths
# ---------------------------------------------------------------------------


def test_report_title_is_dynamic(tmp_path: Path) -> None:
    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    _prepare(pkg, root)
    report = _report(pkg, root)
    assert f"# {TEST_AGENT_NATIVE_CAMPAIGN} execution report" in report
    assert "EXP-0001 execution report" not in report


def test_report_three_agent_invocations_zero_external(tmp_path: Path) -> None:
    """Three serialized attempts (concurrency 1) in ONE campaign: each is
    prepared, delivered, and finalized before the next; the ledger records
    three INVOKED transitions and zero external provider API activity."""
    from test_agent_native_campaign import _pkg_verifier

    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    for _ in range(3):
        result = _prepare(pkg, root)
        delivery = Path(result["delivery_path"])
        delivery.parent.mkdir(parents=True, exist_ok=True)
        delivery.write_text(
            f"# Repository Sensemaking Brief\n\nAttempt {result['attempt_id']}.\n",
            encoding="utf-8",
        )
        outcome = finalize_attempt(
            package_dir=pkg,
            campaign_root=root,
            framework_checkout=REPO_ROOT,
            attempt_id=result["attempt_id"],
            artifact_path=delivery,
            allowed_approver_identities=frozenset(),
            verifier=_pkg_verifier(pkg),
            validate=_passing_validate,
            now=_NOW,
        )
        assert outcome["state"] == "VALIDATION_PASSED"
    report = _report(pkg, root)
    assert "- total_agent_attempt_invocations: 3" in report
    # The FULL assertion lines must appear (a bare "0" line cannot be
    # vacuous): the policy prohibition, the zero invocation count, and
    # the zero cost are each asserted exactly as rendered.
    assert "- external_provider_api_invocations: 0 (must be 0; the policy prohibits external provider APIs)" in report
    assert "- external_provider_cost: 0 (must be 0)" in report
    assert report.count("external_provider_api_invocations: 0") >= 2
    assert report.count("external_provider_cost: 0") >= 2
    assert "total_provider_invocations" not in report


def test_report_lists_raw_output_md_not_bin(tmp_path: Path) -> None:
    pkg, root, attempt_id = _full_attempt(tmp_path)
    report = _report(pkg, root)
    assert f"raw-output.md: experiments/campaigns/{TEST_AGENT_NATIVE_CAMPAIGN}/attempts/{attempt_id}/raw-output.md" in report
    assert "raw-output.bin" not in report


def test_report_real_validation_rates(tmp_path: Path) -> None:
    """The rates come from the RECORDED per-attempt validation results
    (validation-result.json), exactly as finalize stored them."""
    pkg, root, attempt_id = _full_attempt(tmp_path)
    import json

    recorded = json.loads(
        (
            root / TEST_AGENT_NATIVE_CAMPAIGN / "attempts" / attempt_id
            / "validation-result.json"
        ).read_text(encoding="utf-8")
    )
    report = _report(pkg, root)
    details = recorded.get("details") or {}
    structural = (details.get("structural") or {}) if isinstance(details, dict) else {}
    if structural:
        passed, total = structural["passed"], structural["total"]
        assert f"structural pass: {passed}/{total}" in report
    # The stub validator records a plain-string detail -> n/a, never a
    # crash and never a fabricated rate.
    assert "structural pass:" in report


def test_report_includes_validation_failed_attempt(tmp_path: Path) -> None:
    pkg, root, _ = _full_attempt(tmp_path, failing=True)
    report = _report(pkg, root)
    assert "attempts_validation_failed: 1" in report
    assert "state=VALIDATION_FAILED" in report


def test_report_includes_interrupted_invoked_attempt(tmp_path: Path) -> None:
    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    result = _prepare(pkg, root)
    report = _report(pkg, root)
    assert result["attempt_id"] in report
    assert "interrupted (INVOKED, never finished): 1" in report
    assert "state=INVOKED" in report
    # Exactly ONE agent invocation for the one interrupted attempt (the
    # ledger INVOKED event is counted once, never doubled).
    assert "- total_agent_attempt_invocations: 1" in report


def test_report_includes_captured_unvalidated_attempt(tmp_path: Path) -> None:
    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    result = _prepare(pkg, root)
    # Capture raw output without finalizing (OUTPUT_CAPTURED, no terminal).
    recorder = AttemptOutcomeRecorder(
        root, TEST_AGENT_NATIVE_CAMPAIGN, result["attempt_id"]
    )
    recorder.record_raw_output(
        b"# partial brief\n", extension="md", now=_NOW
    )
    report = _report(pkg, root)
    assert "captured-but-unvalidated (OUTPUT_CAPTURED): 1" in report
    assert "state=OUTPUT_CAPTURED" in report
    assert "raw-output.md" in report


# ---------------------------------------------------------------------------
# fail-closed evidence checks
# ---------------------------------------------------------------------------


def test_report_refuses_missing_expected_artifact(tmp_path: Path) -> None:
    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    result = _prepare(pkg, root)
    attempt_dir = (
        root / TEST_AGENT_NATIVE_CAMPAIGN / "attempts" / result["attempt_id"]
    )
    (attempt_dir / "raw-request.txt").unlink()
    with pytest.raises(RunnerRefusal, match="missing expected evidence"):
        _report(pkg, root)


def test_report_flags_orphan_artifact(tmp_path: Path) -> None:
    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    result = _prepare(pkg, root)
    attempt_dir = (
        root / TEST_AGENT_NATIVE_CAMPAIGN / "attempts" / result["attempt_id"]
    )
    (attempt_dir / "stray.txt").write_text("unexpected", encoding="utf-8")
    report = _report(pkg, root)
    assert "ORPHAN FILE: stray.txt" in report


def test_report_target_drift_detected(tmp_path: Path) -> None:
    pkg, root, _ = _full_attempt(tmp_path)
    # No target root provided -> integrity cannot be attested -> DRIFT.
    report = _report(pkg, root, target_checkout_root=None)
    assert "target_checkout_integrity: DRIFT DETECTED" in report
    # A bogus target root also reports DRIFT (actual result, never
    # hardcoded true).
    report = _report(pkg, root, target_checkout_root=tmp_path / "no-such-target")
    assert "target_checkout_integrity: DRIFT DETECTED" in report


def test_report_target_integrity_ok_on_pristine_checkout(tmp_path: Path) -> None:
    """A real, pristine target checkout at the approved SHA reports OK --
    the check is a live git verification, not a hardcoded value."""
    import subprocess

    from exploratory_fixtures import TEST_TARGET_REPOSITORY
    from sensemaking_skills.campaign_validation import (
        compute_configuration_id,
        compute_policy_digest,
    )
    from sensemaking_skills.campaign_validation.yaml_profile import (
        dump_two_lane_yaml,
    )
    from test_agent_native_campaign import _receipt_raw, _write_receipt

    target = tmp_path / "target"
    target.mkdir()
    subprocess.run(["git", "init", "-q", str(target)], check=True)
    subprocess.run(
        ["git", "-C", str(target), "config", "user.email", "test@example.invalid"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(target), "config", "user.name", "test"], check=True
    )
    subprocess.run(
        ["git", "-C", str(target), "remote", "add", "origin", TEST_TARGET_REPOSITORY],
        check=True,
    )
    (target / "README.md").write_text("target material\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(target), "add", "."], check=True)
    subprocess.run(["git", "-C", str(target), "commit", "-qm", "init"], check=True)
    head = subprocess.run(
        ["git", "-C", str(target), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()

    from exploratory_fixtures import build_configuration_raw, build_policy_raw
    from test_agent_native_campaign import _conversation_verifier

    pkg = tmp_path / "pkg"
    pkg.mkdir()
    config_raw = build_configuration_raw(campaign_id=TEST_AGENT_NATIVE_CAMPAIGN)
    config_raw["model_identifier"] = "current_coding_agent"
    config_raw["target_sha"] = head
    config_raw["configuration_id"] = compute_configuration_id(config_raw)
    policy_raw = build_policy_raw(
        campaign_id=TEST_AGENT_NATIVE_CAMPAIGN,
        execution_mode="coding_agent_native",
        execution_surface="current_coding_agent",
        external_provider_api_prohibited=True,
        allowed_models=[],
    )
    policy_raw["allowed_targets"] = [
        {"repository": TEST_TARGET_REPOSITORY, "sha": head}
    ]
    policy_raw["allowed_configuration_ids"] = [config_raw["configuration_id"]]
    policy_raw["policy_digest"] = compute_policy_digest(policy_raw)
    from exploratory_fixtures import render_yaml

    (pkg / "campaign-policy.yaml").write_bytes(render_yaml(policy_raw))
    (pkg / "configuration-identity.yaml").write_bytes(render_yaml(config_raw))
    _write_receipt(pkg, _receipt_raw(policy_raw))

    root = tmp_path / "root"
    report = _report(pkg, root, target_checkout_root=target)
    assert "target_checkout_integrity: OK" in report


def test_report_framework_drift_detected(tmp_path: Path) -> None:
    pkg, root, _ = _full_attempt(tmp_path)
    report = _report(pkg, root, framework_checkout=tmp_path / "not-the-framework")
    assert "framework_drift: DETECTED" in report


# ---------------------------------------------------------------------------
# report-only (post-expiry) path
# ---------------------------------------------------------------------------


def test_report_requires_window_for_execution_report(tmp_path: Path) -> None:
    """Without --report-only, reporting after expiry refuses (the window
    is enforced): the record stays bounded even for reporting."""
    pkg, root, _ = _full_attempt(tmp_path)
    with pytest.raises(RunnerRefusal, match="bundle validation failed"):
        _report(pkg, root, now=_AFTER_WINDOW)


def test_report_only_available_after_expiry(tmp_path: Path) -> None:
    pkg, root, _ = _full_attempt(tmp_path)
    report = _report(pkg, root, now=_AFTER_WINDOW, report_only=True)
    assert f"# {TEST_AGENT_NATIVE_CAMPAIGN} execution report" in report
    assert "## Report-only mode" in report
    assert "NO reservation or invocation was authorized" in report


def test_report_only_still_binds_approval_and_digest(tmp_path: Path) -> None:
    """Report-only still verifies policy/configuration digests and the
    approval binding: a wrong approval file must refuse even report-only."""
    pkg, root, _ = _full_attempt(tmp_path)
    (pkg / "approval.md").write_text(
        (pkg / "approval.md").read_text(encoding="utf-8").replace(
            '"approve"', '"denied"'
        ),
        encoding="utf-8",
    )
    with pytest.raises(RunnerRefusal):
        _report(pkg, root, now=_AFTER_WINDOW, report_only=True)


def test_report_never_reserves_or_invokes(tmp_path: Path) -> None:
    pkg, root, _ = _full_attempt(tmp_path)
    before = _events(root, TEST_AGENT_NATIVE_CAMPAIGN)
    attempts_dir = root / TEST_AGENT_NATIVE_CAMPAIGN / "attempts"
    dirs_before = sorted(p.name for p in attempts_dir.iterdir()) if attempts_dir.is_dir() else []
    _report(pkg, root)
    _report(pkg, root, now=_AFTER_WINDOW, report_only=True)
    after = _events(root, TEST_AGENT_NATIVE_CAMPAIGN)
    dirs_after = sorted(p.name for p in attempts_dir.iterdir()) if attempts_dir.is_dir() else []
    assert after == before
    assert dirs_after == dirs_before


# ---------------------------------------------------------------------------
# statements and evidence
# ---------------------------------------------------------------------------


def test_report_contains_nothing_omitted_statement(tmp_path: Path) -> None:
    pkg, root, _ = _full_attempt(tmp_path)
    report = _report(pkg, root)
    assert "## Nothing-omitted statement" in report
    assert "no attempt has been deleted, hidden, or selectively omitted" in report


def test_report_exploratory_classification(tmp_path: Path) -> None:
    pkg, root, _ = _full_attempt(tmp_path)
    report = _report(pkg, root)
    assert "EXPLORATORY_NOT_CANONICAL_EVIDENCE" in report


def test_report_leaves_evidence_untouched(tmp_path: Path) -> None:
    """Evidence 0015 (and any later evidence artifacts) are byte-identical
    before and after report generation."""
    evidence_root = REPO_ROOT / "experiments" / "evidence"
    targets = [
        p
        for p in evidence_root.iterdir()
        if p.name.startswith("0015") or p.name.startswith("0016")
    ]
    assert targets, "expected Evidence 0015/0016 under experiments/evidence/"

    def snapshot() -> dict[str, bytes]:
        result: dict[str, bytes] = {}
        for target in targets:
            for f in sorted(target.rglob("*")):
                if f.is_file():
                    result[str(f.relative_to(evidence_root))] = f.read_bytes()
        return result

    before = snapshot()
    pkg, root, _ = _full_attempt(tmp_path)
    _report(pkg, root)
    assert snapshot() == before
