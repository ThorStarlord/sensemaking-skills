"""Path-confinement adversarial tests (Phase 4, #120 merge blocker).

``record_produced_artifact`` and ``record_raw_output`` accept
caller-supplied names. These tests prove the frozen lowercase ASCII
leaf-name grammar closes every escape vector -- traversal, separators,
drive/UNC qualification, ADS/colon syntax, trailing-dot/space aliasing,
hidden and empty names -- and that rejected names cause NO file creation
or modification outside the exact attempt directory, leave the ledger
byte-identical, leave other attempt directories untouched, and yield the
exact deterministic failure code. The same vectors are exercised through
the real ``invoke_exploratory_attempt`` boundary, proving the provider is
never called again and the attempt stays durably visible.
"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from exploratory_fixtures import (
    _ANCHOR_NOW,
    TrustedReferenceProvenanceVerifier,
    build_request,
    build_valid_bundle,
    make_context,
    new_attempt_id,
)

from sensemaking_skills.campaign_accounting import (
    ARTIFACT_ALREADY_EXISTS,
    ARTIFACT_FILENAME_INVALID,
    ATTEMPT_STATE_INVALID_TRANSITION,
    AttemptState,
    CampaignAccountingError,
    CampaignLedger,
    DurableReservationManager,
    AttemptOutcomeRecorder,
    ValidationOutcome,
    invoke_exploratory_attempt,
    RAW_OUTPUT_EXTENSION_INVALID,
)
from sensemaking_skills.exploratory_authorization import mint_exploratory_capability


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _reserve(tmp_path: Path, bundle, attempt_id=None):
    attempt_id = attempt_id or new_attempt_id()
    manager = DurableReservationManager(tmp_path)
    manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=_ANCHOR_NOW,
    )
    return AttemptOutcomeRecorder(tmp_path, bundle.policy.campaign_id, attempt_id)


def _reach_captured(tmp_path: Path, bundle, attempt_id=None) -> AttemptOutcomeRecorder:
    """Reserve + invoke + raw capture: ledger state OUTPUT_CAPTURED."""
    recorder = _reserve(tmp_path, bundle, attempt_id)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)
    recorder.record_raw_output(b"raw bytes", now=_ANCHOR_NOW)
    return recorder


def _snapshot(root: Path) -> dict:
    """path (POSIX-normalized) -> bytes for every file under ``root``."""
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[p.relative_to(root).as_posix()] = p.read_bytes()
    return out


def _setup_with_second_attempt(tmp_path: Path, bundle):
    """Return (campaign_root, second_attempt_dir).

    The second attempt is reserved and immediately aborted (terminal) so
    it does not occupy the v1 concurrency slot.
    """
    campaign_root = tmp_path / bundle.policy.campaign_id
    second = _reserve(tmp_path, bundle)
    second.record_pre_invocation_abort("second attempt for confinement tests", now=_ANCHOR_NOW)
    second_dir = campaign_root / "attempts" / second.attempt_id
    return campaign_root, second_dir


# ---------------------------------------------------------------------------
# Produced-artifact filename rejection matrix (public recorder)
# ---------------------------------------------------------------------------

INVALID_FILENAMES = [
    "../../../escaped.md",            # traversal above the campaign root
    "../../ledger.jsonl",             # traversal onto the ledger itself
    "../other-attempt/reservation.yaml",  # traversal into another attempt
    "/tmp/absolute-posix.md",         # absolute POSIX path
    "C:/windows-drive.md",            # Windows drive-qualified (slash)
    "C:\\windows-drive.md",           # Windows drive-qualified (backslash)
    "\\\\server\\share\\evil.md",     # UNC path
    "..\\..\\backslash-traversal.md", # backslash traversal
    "evil.md:ads",                    # Windows ADS/colon syntax
    "evil.md.",                       # trailing-dot alias
    "evil.md ",                       # trailing-space alias
    "",                               # empty name
    ".hidden",                        # leading dot (hidden)
    "Uppercase.md",                   # outside lowercase grammar
    "..",                             # parent alias
    ".",                              # self alias
    "a..b.md",                        # interior double-dot sequence
]


@pytest.mark.parametrize("bad", INVALID_FILENAMES)
def test_produced_artifact_rejects_unsafe_name(tmp_path: Path, bad: str) -> None:
    bundle = build_valid_bundle()
    campaign_root, second_dir = _setup_with_second_attempt(tmp_path, bundle)
    recorder = _reach_captured(tmp_path, bundle)

    before_tree = _snapshot(campaign_root)
    before_ledger = (campaign_root / "ledger.jsonl").read_bytes()
    before_tmp = _snapshot(tmp_path)

    with pytest.raises(CampaignAccountingError) as exc_info:
        recorder.record_produced_artifact("# x", filename=bad)
    assert exc_info.value.failure_code == ARTIFACT_FILENAME_INVALID

    # No file created or modified anywhere in the campaign tree.
    assert _snapshot(campaign_root) == before_tree
    # The ledger is byte-identical.
    assert (campaign_root / "ledger.jsonl").read_bytes() == before_ledger
    # No file created above the campaign root.
    assert _snapshot(tmp_path) == before_tmp
    # The other attempt's directory is untouched.
    assert _snapshot(second_dir) == _snapshot(second_dir)


# ---------------------------------------------------------------------------
# Valid produced-artifact names
# ---------------------------------------------------------------------------

VALID_FILENAMES = [
    "produced-artifact.md",
    "artifact.v1.0-final.md",
    "notes_2026.md",
]


@pytest.mark.parametrize("good", VALID_FILENAMES)
def test_produced_artifact_accepts_safe_name(tmp_path: Path, good: str) -> None:
    bundle = build_valid_bundle()
    recorder = _reach_captured(tmp_path, bundle)

    ref = recorder.record_produced_artifact("# content", filename=good)

    assert ref == (
        f"experiments/campaigns/{bundle.policy.campaign_id}/attempts/"
        f"{recorder.attempt_id}/{good}"
    )
    target = (
        tmp_path / bundle.policy.campaign_id / "attempts" / recorder.attempt_id / good
    )
    assert target.read_bytes() == "# content".encode("utf-8")


# ---------------------------------------------------------------------------
# Overwrite resistance and deterministic crash-resume
# ---------------------------------------------------------------------------


def test_produced_artifact_rejects_different_existing_artifact(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    recorder = _reach_captured(tmp_path, bundle)
    recorder.record_produced_artifact("version-A", filename="produced-artifact.md")

    with pytest.raises(CampaignAccountingError) as exc_info:
        recorder.record_produced_artifact("version-B", filename="produced-artifact.md")
    assert exc_info.value.failure_code == ARTIFACT_ALREADY_EXISTS

    target = (
        tmp_path / bundle.policy.campaign_id / "attempts" / recorder.attempt_id
        / "produced-artifact.md"
    )
    # The original artifact is never overwritten.
    assert target.read_bytes() == b"version-A"


def test_produced_artifact_identical_repeat_is_resume(tmp_path: Path) -> None:
    """Repeated identical write = deterministic crash-resume, not an error."""
    bundle = build_valid_bundle()
    recorder = _reach_captured(tmp_path, bundle)
    recorder.record_produced_artifact("# same", filename="produced-artifact.md")

    ref = recorder.record_produced_artifact("# same", filename="produced-artifact.md")
    assert ref.endswith("produced-artifact.md")

    target = (
        tmp_path / bundle.policy.campaign_id / "attempts" / recorder.attempt_id
        / "produced-artifact.md"
    )
    assert target.read_bytes() == b"# same"


def test_produced_artifact_crash_resume_from_preserved_file(tmp_path: Path) -> None:
    """A file preserved by a crashed run (identical bytes) resumes cleanly."""
    bundle = build_valid_bundle()
    recorder = _reach_captured(tmp_path, bundle)
    target = (
        tmp_path / bundle.policy.campaign_id / "attempts" / recorder.attempt_id
        / "produced-artifact.md"
    )
    # Simulate the crash window: the artifact was atomically renamed but the
    # process died before the terminal ledger event.
    target.write_bytes(b"# preserved")

    ref = recorder.record_produced_artifact("# preserved", filename="produced-artifact.md")
    assert ref.endswith("produced-artifact.md")
    assert target.read_bytes() == b"# preserved"

    # A different artifact in that window is still rejected.
    with pytest.raises(CampaignAccountingError) as exc_info:
        recorder.record_produced_artifact("# different", filename="produced-artifact.md")
    assert exc_info.value.failure_code == ARTIFACT_ALREADY_EXISTS
    assert target.read_bytes() == b"# preserved"


# ---------------------------------------------------------------------------
# State gate: artifact preservation requires OUTPUT_CAPTURED
# ---------------------------------------------------------------------------


def test_produced_artifact_requires_output_captured(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    recorder = _reserve(tmp_path, bundle)  # RESERVED only

    with pytest.raises(CampaignAccountingError) as exc_info:
        recorder.record_produced_artifact("# x", filename="produced-artifact.md")
    assert exc_info.value.failure_code == ATTEMPT_STATE_INVALID_TRANSITION

    attempt_dir = tmp_path / bundle.policy.campaign_id / "attempts" / recorder.attempt_id
    assert not (attempt_dir / "produced-artifact.md").exists()


def test_produced_artifact_requires_raw_output_first(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    recorder = _reserve(tmp_path, bundle)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)  # INVOKED, not captured

    with pytest.raises(CampaignAccountingError) as exc_info:
        recorder.record_produced_artifact("# x", filename="produced-artifact.md")
    assert exc_info.value.failure_code == ATTEMPT_STATE_INVALID_TRANSITION


# ---------------------------------------------------------------------------
# Raw-output extension rejection matrix (public recorder)
# ---------------------------------------------------------------------------

INVALID_EXTENSIONS = [
    "../escaped",
    "..\\escaped",
    "../../x",
    "x/y",
    "evil:stream",
    "bin.",
    "bin ",
    "",
    ".bin",
    "BIN",
    "..",
    ".",
    "a..b",
]


@pytest.mark.parametrize("bad", INVALID_EXTENSIONS)
def test_raw_output_rejects_unsafe_extension(tmp_path: Path, bad: str) -> None:
    bundle = build_valid_bundle()
    campaign_root = tmp_path / bundle.policy.campaign_id
    recorder = _reserve(tmp_path, bundle)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)

    before_tree = _snapshot(campaign_root)
    before_ledger = (campaign_root / "ledger.jsonl").read_bytes()

    with pytest.raises(CampaignAccountingError) as exc_info:
        recorder.record_raw_output(b"x", extension=bad, now=_ANCHOR_NOW)
    assert exc_info.value.failure_code == RAW_OUTPUT_EXTENSION_INVALID

    assert _snapshot(campaign_root) == before_tree
    assert (campaign_root / "ledger.jsonl").read_bytes() == before_ledger


@pytest.mark.parametrize("good", ["bin", "txt.gz", "json", "md"])
def test_raw_output_accepts_safe_extension(tmp_path: Path, good: str) -> None:
    bundle = build_valid_bundle()
    recorder = _reserve(tmp_path, bundle)
    recorder.record_invoked(bundle, now=_ANCHOR_NOW)

    ref = recorder.record_raw_output(b"payload", extension=good, now=_ANCHOR_NOW)
    target = (
        tmp_path / bundle.policy.campaign_id / "attempts" / recorder.attempt_id
        / f"raw-output.{good}"
    )
    assert target.read_bytes() == b"payload"
    assert ref.endswith(f"raw-output.{good}")


# ---------------------------------------------------------------------------
# Real boundary (invoke_exploratory_attempt) vectors
# ---------------------------------------------------------------------------


def _mint(bundle, attempt_id):
    return mint_exploratory_capability(
        bundle,
        build_request(
            attempt_id=attempt_id,
            configuration_id=bundle.configuration.configuration_id,
        ),
        verifier=TrustedReferenceProvenanceVerifier(),
        now=_ANCHOR_NOW.isoformat(),
    )


class CountingProvider:
    def __init__(self):
        self.calls = 0

    def __call__(self) -> bytes:
        self.calls += 1
        return b"raw provider response"


def _invoke(tmp_path, bundle, capability, reservation, provider, validate):
    return invoke_exploratory_attempt(
        bundle=bundle,
        capability=capability,
        reservation=reservation,
        campaign_root=tmp_path,
        context=make_context(capability=capability),
        provider=provider,
        validate=validate,
        now=_ANCHOR_NOW,
    )


def test_boundary_rejects_traversal_artifact_filename(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = CountingProvider()
    manager = DurableReservationManager(tmp_path)
    reservation = manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=_ANCHOR_NOW,
    )
    before_tree = _snapshot(tmp_path / bundle.policy.campaign_id)

    def validate(raw):
        return ValidationOutcome(
            passed=True,
            details={},
            artifact_content="# candidate",
            artifact_filename="../../../escaped.md",
        )

    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, reservation, provider, validate)
    assert exc_info.value.failure_code == ARTIFACT_FILENAME_INVALID

    # The provider was reached exactly once (raw capture precedes the
    # artifact step) and is NEVER called again.
    assert provider.calls == 1

    # The attempt stays durably visible: RESERVED -> INVOKED -> OUTPUT_CAPTURED.
    ledger = CampaignLedger(tmp_path / bundle.policy.campaign_id, bundle.policy.campaign_id)
    states = [e.event_type for e in ledger.read_events() if e.attempt_id == attempt_id]
    assert states == [
        AttemptState.RESERVED.value,
        AttemptState.INVOKED.value,
        AttemptState.OUTPUT_CAPTURED.value,
    ]

    # No file was created or modified outside the attempt directory: the
    # only delta vs the pre-invoke tree is raw-output.bin plus the ledger's
    # two legitimate lifecycle events.
    after_tree = _snapshot(tmp_path / bundle.policy.campaign_id)
    delta = set(after_tree) - set(before_tree)
    assert delta == {
        f"attempts/{attempt_id}/raw-output.bin",
    }, delta
    assert not (tmp_path / "escaped.md").exists()
    assert not (tmp_path / bundle.policy.campaign_id / "escaped.md").exists()
    # No terminal result was fabricated.
    assert not (
        tmp_path / bundle.policy.campaign_id / "attempts" / attempt_id
        / "attempt-result.yaml"
    ).exists()

    # The spent capability cannot retry the attempt; the provider is not
    # called again.
    provider2 = CountingProvider()
    with pytest.raises(CampaignAccountingError) as exc_info2:
        _invoke(tmp_path, bundle, capability, reservation, provider2, validate)
    assert exc_info2.value.failure_code == "RESERVATION_NOT_LIVE"
    assert provider2.calls == 0
    assert provider.calls == 1


def test_boundary_ledger_jsonl_target_rejected(tmp_path: Path) -> None:
    """'../../ledger.jsonl' from the attempt dir must never touch the ledger."""
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = CountingProvider()
    manager = DurableReservationManager(tmp_path)
    reservation = manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=_ANCHOR_NOW,
    )

    def validate(raw):
        return ValidationOutcome(
            passed=True, details={}, artifact_content="# x",
            artifact_filename="../../ledger.jsonl",
        )

    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, reservation, provider, validate)
    assert exc_info.value.failure_code == ARTIFACT_FILENAME_INVALID
    assert provider.calls == 1

    # The ledger is intact: the full hash chain still validates and carries
    # exactly the three legitimate lifecycle events.
    ledger = CampaignLedger(tmp_path / bundle.policy.campaign_id, bundle.policy.campaign_id)
    events = ledger.read_events()
    assert [e.event_type for e in events if e.attempt_id == attempt_id] == [
        AttemptState.RESERVED.value,
        AttemptState.INVOKED.value,
        AttemptState.OUTPUT_CAPTURED.value,
    ]
    # The produced artifact was never written anywhere.
    assert not (tmp_path / bundle.policy.campaign_id / "ledger.jsonl.bak").exists()


def test_boundary_other_attempt_reservation_target_rejected(tmp_path: Path) -> None:
    """'../other-attempt/reservation.yaml' must never reach another attempt."""
    bundle = build_valid_bundle()
    other_recorder = _reserve(tmp_path, bundle)  # a second, unrelated attempt
    # Terminal so it does not occupy the v1 concurrency slot.
    other_recorder.record_pre_invocation_abort("second attempt", now=_ANCHOR_NOW)
    other_dir = (
        tmp_path / bundle.policy.campaign_id / "attempts" / other_recorder.attempt_id
    )
    other_reservation_bytes = (other_dir / "reservation.yaml").read_bytes()

    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = CountingProvider()
    manager = DurableReservationManager(tmp_path)
    reservation = manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=_ANCHOR_NOW,
    )

    def validate(raw):
        return ValidationOutcome(
            passed=True, details={}, artifact_content="# x",
            artifact_filename="../other-attempt/reservation.yaml",
        )

    with pytest.raises(CampaignAccountingError) as exc_info:
        _invoke(tmp_path, bundle, capability, reservation, provider, validate)
    assert exc_info.value.failure_code == ARTIFACT_FILENAME_INVALID
    assert provider.calls == 1
    # The other attempt's durable data is byte-identical.
    assert (other_dir / "reservation.yaml").read_bytes() == other_reservation_bytes


def test_boundary_valid_artifact_filename_succeeds(tmp_path: Path) -> None:
    bundle = build_valid_bundle()
    attempt_id = new_attempt_id()
    capability = _mint(bundle, attempt_id)
    provider = CountingProvider()
    manager = DurableReservationManager(tmp_path)
    reservation = manager.reserve_attempt(
        bundle=bundle,
        attempt_id=attempt_id,
        configuration_id=bundle.configuration.configuration_id,
        request_metadata={"campaign_id": bundle.policy.campaign_id},
        now=_ANCHOR_NOW,
    )

    def validate(raw):
        assert raw == b"raw provider response"
        return ValidationOutcome(
            passed=True, details={"ok": True}, artifact_content="# candidate",
            artifact_filename="produced-artifact.md",
        )

    result = _invoke(tmp_path, bundle, capability, reservation, provider, validate)
    assert result.state == AttemptState.VALIDATION_PASSED.value
    assert provider.calls == 1
    attempt_dir = tmp_path / bundle.policy.campaign_id / "attempts" / attempt_id
    assert (attempt_dir / "produced-artifact.md").read_bytes() == b"# candidate"
