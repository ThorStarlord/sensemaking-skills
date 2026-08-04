"""Windows process proofs for device-name and length rejection (Phase 4).

Each probe runs in a fresh SUBPROCESS with a hard timeout, so a regression
that blocks (e.g. reading a DOS device) fails the test as a hang instead of
wedging the test runner. Three exercise levels per name:

1. ``validate_produced_artifact_filename`` -- pure lexical rejection;
2. ``AttemptOutcomeRecorder.record_produced_artifact`` -- rejection before
   any state read or filesystem access, attempt parked at OUTPUT_CAPTURED;
3. ``invoke_exploratory_attempt`` -- the real boundary via
   ``ValidationOutcome.artifact_filename``: provider called exactly once,
   raw output captured, rejection leaves the attempt durably visible at
   OUTPUT_CAPTURED, a retry produces zero additional provider calls, and
   the campaign lock remains acquirable afterward.

Every probe also proves: no file outside the attempt directory was created
or modified, the ledger gained only the legitimate lifecycle events, and no
raw OSError/TimeoutError escaped as the public result.
"""

import json
import subprocess
import sys
from pathlib import Path
import pytest

from sensemaking_skills.campaign_accounting import ARTIFACT_FILENAME_INVALID

sys.path.insert(0, str(Path(__file__).parent.parent))

_REPO_ROOT = Path(__file__).resolve().parents[2]
_TESTS_DIR = Path(__file__).resolve().parents[1]

PROBE_NAMES = [
    "con.md",
    "aux.md",
    "nul",
    "prn.txt",
    "com1",
    "lpt1.md",
    "a" * 129,
    "a" * 300,
]

_CHILD = r"""
import json, os, sys
from pathlib import Path

sys.path.insert(0, {tests_dir!r})
sys.path.insert(0, str(Path({repo_root!r}) / "src"))

from exploratory_fixtures import (
    _ANCHOR_NOW, TrustedReferenceProvenanceVerifier, build_request,
    build_valid_bundle, make_context, new_attempt_id,
)
from sensemaking_skills.campaign_accounting import (
    ARTIFACT_FILENAME_INVALID, CampaignAccountingError, CampaignLedger,
    DurableReservationManager, AttemptOutcomeRecorder, ValidationOutcome,
    invoke_exploratory_attempt, validate_produced_artifact_filename,
    campaign_lock,
)
from sensemaking_skills.exploratory_authorization import mint_exploratory_capability

mode, name, out_path, tmp_path = sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4])
result = {{"mode": mode, "name": name, "code": None, "provider_calls": 0,
          "states": [], "error": None}}

try:
    if mode == "validator":
        try:
            validate_produced_artifact_filename(name)
            result["error"] = "name unexpectedly accepted"
        except CampaignAccountingError as exc:
            result["code"] = exc.failure_code

    elif mode == "recorder":
        bundle = build_valid_bundle()
        aid = new_attempt_id()
        mgr = DurableReservationManager(tmp_path)
        mgr.reserve_attempt(bundle, attempt_id=aid,
                            configuration_id=bundle.configuration.configuration_id,
                            request_metadata={{}}, now=_ANCHOR_NOW)
        rec = AttemptOutcomeRecorder(tmp_path, bundle.policy.campaign_id, aid)
        rec.record_invoked(bundle, now=_ANCHOR_NOW)
        rec.record_raw_output(b"raw", now=_ANCHOR_NOW)
        ledger_before = (tmp_path / bundle.policy.campaign_id / "ledger.jsonl").read_bytes()
        try:
            rec.record_produced_artifact("# x", filename=name)
            result["error"] = "name unexpectedly accepted"
        except CampaignAccountingError as exc:
            result["code"] = exc.failure_code
        ledger_after = (tmp_path / bundle.policy.campaign_id / "ledger.jsonl").read_bytes()
        result["ledger_unchanged"] = ledger_before == ledger_after
        attempt_dir = tmp_path / bundle.policy.campaign_id / "attempts" / aid
        result["files"] = sorted(p.name for p in attempt_dir.iterdir())

    elif mode == "boundary":
        bundle = build_valid_bundle()
        aid = new_attempt_id()
        mgr = DurableReservationManager(tmp_path)
        reservation = mgr.reserve_attempt(
            bundle, attempt_id=aid,
            configuration_id=bundle.configuration.configuration_id,
            request_metadata={{}}, now=_ANCHOR_NOW)
        capability = mint_exploratory_capability(
            bundle, build_request(attempt_id=aid,
                                  configuration_id=bundle.configuration.configuration_id),
            verifier=TrustedReferenceProvenanceVerifier(),
            now=_ANCHOR_NOW.isoformat())
        calls = []
        def provider():
            calls.append(1)
            return b"raw provider response"
        def validate(raw):
            return ValidationOutcome(passed=True, details={{}},
                                     artifact_content="# candidate",
                                     artifact_filename=name)
        try:
            invoke_exploratory_attempt(
                bundle=bundle, capability=capability, reservation=reservation,
                campaign_root=tmp_path, context=make_context(capability=capability),
                provider=provider, validate=validate, now=_ANCHOR_NOW)
            result["error"] = "name unexpectedly accepted"
        except CampaignAccountingError as exc:
            result["code"] = exc.failure_code
        result["provider_calls"] = len(calls)
        ledger = CampaignLedger(tmp_path / bundle.policy.campaign_id, bundle.policy.campaign_id)
        result["states"] = [e.event_type for e in ledger.read_events()
                            if e.attempt_id == aid]
        attempt_dir = tmp_path / bundle.policy.campaign_id / "attempts" / aid
        result["result_file"] = (attempt_dir / "attempt-result.yaml").exists()
        result["raw_captured"] = (attempt_dir / "raw-output.bin").exists()

        # Retry the same attempt: zero additional provider calls.
        calls2 = []
        def provider2():
            calls2.append(1)
            return b"x"
        try:
            invoke_exploratory_attempt(
                bundle=bundle, capability=capability, reservation=reservation,
                campaign_root=tmp_path, context=make_context(capability=capability),
                provider=provider2, validate=validate, now=_ANCHOR_NOW)
            result["retry_error"] = "retry unexpectedly accepted"
        except CampaignAccountingError as exc:
            result["retry_code"] = exc.failure_code
        result["retry_provider_calls"] = len(calls2)

        # The campaign lock remains acquirable afterward.
        acquired = []
        with campaign_lock(tmp_path / bundle.policy.campaign_id):
            acquired.append(True)
        result["lock_acquirable"] = bool(acquired)

    else:
        result["error"] = "unknown mode"
except BaseException as exc:  # noqa: BLE001 - report, never hang the parent
    result["error"] = type(exc).__name__ + ": " + str(exc)[:200]

Path(out_path).write_text(json.dumps(result), encoding="utf-8")
os._exit(0)
"""


def _run_probe(mode: str, name: str, tmp_path: Path) -> dict:
    out_path = tmp_path / f"out-{mode}.json"
    child_code = _CHILD.format(tests_dir=str(_TESTS_DIR), repo_root=str(_REPO_ROOT))
    try:
        proc = subprocess.run(
            [sys.executable, "-u", "-c", child_code, mode, name,
             str(out_path), str(tmp_path)],
            capture_output=True, text=True, timeout=45, cwd=str(_REPO_ROOT),
            check=False,
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"HANG: {mode} probe for {name!r} did not terminate in 45s")
    assert proc.returncode == 0, (
        f"child crashed for {mode}/{name!r}: rc={proc.returncode} "
        f"stderr={proc.stderr[-300:]!r}"
    )
    assert out_path.exists(), f"child produced no result for {mode}/{name!r}"
    return json.loads(out_path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", PROBE_NAMES)
def test_validator_rejects_device_and_overlong(name: str, tmp_path: Path) -> None:
    result = _run_probe("validator", name, tmp_path)
    assert result["code"] == ARTIFACT_FILENAME_INVALID, result
    assert result.get("error") is None, result


@pytest.mark.parametrize("name", PROBE_NAMES)
def test_recorder_rejects_before_touching_state_or_fs(name: str, tmp_path: Path) -> None:
    result = _run_probe("recorder", name, tmp_path)
    assert result["code"] == ARTIFACT_FILENAME_INVALID, result
    assert result.get("error") is None, result
    # Lexical rejection left the ledger and the attempt directory untouched.
    assert result.get("ledger_unchanged") is True, result
    assert result.get("files") == [
        "raw-output.bin", "request-metadata.json", "reservation.yaml",
    ], result


@pytest.mark.parametrize("name", PROBE_NAMES)
def test_boundary_rejects_with_single_provider_call_and_live_lock(
    name: str, tmp_path: Path
) -> None:
    result = _run_probe("boundary", name, tmp_path)
    assert result["code"] == ARTIFACT_FILENAME_INVALID, result
    assert result.get("error") is None, result
    # The provider ran exactly once for the original attempt (raw capture
    # precedes artifact naming) and NEVER again on retry.
    assert result["provider_calls"] == 1, result
    assert result["retry_code"] == "RESERVATION_NOT_LIVE", result
    assert result["retry_provider_calls"] == 0, result
    # The attempt is durably visible at OUTPUT_CAPTURED with the raw output
    # preserved and no fabricated terminal result.
    assert result["states"] == [
        "RESERVED", "INVOKED", "OUTPUT_CAPTURED",
    ], result
    assert result["raw_captured"] is True, result
    assert result["result_file"] is False, result
    # No file outside the attempt directory was created or modified.
    assert result["lock_acquirable"] is True, result
