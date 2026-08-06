"""Agent-native campaign tests (two-phase prepare/finalize protocol).

EXP-0002 direction: skills are instructions for the coding agent, not
prompts forwarded to another model. The Python layer is bookkeeping only;
the coding agent performs repo-sensemaker itself. These tests prove:

* prepare creates a durable reservation + frozen instructions + durable
  INVOKED and derives remaining slots from the ledger;
* finalize preserves raw output + produced artifact, validates, and
  records the terminal state;
* the report enumerates every attempt (nothing omitted);
* the provider-loop runner refuses coding_agent_native campaigns;
* no anthropic/claude_agent_sdk import happens on the agent-native path;
* a refused approval creates NO reservation;
* real-campaign guards (injection) hold;
* mode coupling is enforced at policy validation.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from exploratory_fixtures import (  # noqa: E402
    TEST_APPROVER_IDENTITY,
    TEST_CAMPAIGN_ID,
    TEST_VALIDATION_TIME,
    build_configuration_raw,
    build_policy_raw,
    render_yaml,
)
from execution_infra.agent_native_campaign import (  # noqa: E402
    AGENT_NATIVE_REAL_CAMPAIGN_ID,
    build_report,
    finalize_attempt,
    prepare_next_attempt,
)
from execution_infra.runner import (  # noqa: E402
    GovernedCampaignRunner,
    RunnerRefusal,
)
from sensemaking_skills.campaign_accounting import (  # noqa: E402
    CampaignLedger,
)
from sensemaking_skills.campaign_validation import (  # noqa: E402
    compute_configuration_id,
    compute_policy_digest,
    validate_campaign_policy,
)
from sensemaking_skills.campaign_validation.models import (  # noqa: E402
    ValidationContext,
)
from sensemaking_skills.campaign_validation.yaml_profile import (  # noqa: E402
    dump_two_lane_yaml,
)
from sensemaking_skills.exploratory_authorization.provenance import (  # noqa: E402
    ProvenanceVerificationError,
)
from sensemaking_skills.exploratory_execution import (  # noqa: E402
    CONVERSATION_APPROVAL_FILENAME,
    ConversationApprovalVerifier,
)

TEST_AGENT_NATIVE_CAMPAIGN = "EXP-9002-agent-native-test"

_NOW = datetime.fromisoformat(TEST_VALIDATION_TIME)


def _receipt_raw(
    policy_raw: dict,
    *,
    campaign_id: str | None = None,
    policy_digest: str | None = None,
    maximum_attempts: int | None = None,
    concurrency: int | None = None,
    automatic_merge: str = "prohibited",
    classification: str | None = None,
    approved_at: str | None = None,
    reference: str = "test-session#message-42",
    status: str = "approved",
    approval_text: str = "approve",
) -> dict:
    return {
        "approval_schema_version": "1",
        "status": status,
        "campaign_id": campaign_id or policy_raw["campaign_id"],
        "policy_digest": policy_digest or policy_raw["policy_digest"],
        "approval_source": "active_human_conversation",
        "approval_text": approval_text,
        "approved_at": approved_at or _NOW.isoformat(),
        "maximum_attempts": maximum_attempts or int(policy_raw["max_attempt_slots"]),
        "concurrency": concurrency or int(policy_raw["concurrency_ceiling"]),
        "automatic_merge": automatic_merge,
        "external_provider_api_prohibited": True,
        "classification": classification or policy_raw["classification"],
        "reference": reference,
    }


def _write_receipt(pkg: Path, approval_raw: dict) -> None:
    frontmatter = dump_two_lane_yaml(approval_raw)
    body = (
        "---\n" + frontmatter + "---\n"
        "The human approved the single pending campaign presented in the "
        "active conversation.\n"
    )
    (pkg / CONVERSATION_APPROVAL_FILENAME).write_text(body, encoding="utf-8")


def _conversation_verifier(policy_raw: dict) -> ConversationApprovalVerifier:
    return ConversationApprovalVerifier(
        policy=policy_raw, clock=lambda: _NOW
    )



def _pkg_verifier(pkg: Path) -> ConversationApprovalVerifier:
    """Injected conversation verifier bound to the package's policy."""
    from sensemaking_skills.campaign_validation import parse_two_lane_yaml

    policy_raw = parse_two_lane_yaml(
        (pkg / "campaign-policy.yaml").read_bytes()
    )
    return _conversation_verifier(policy_raw)

def _passing_validate(artifact_bytes: bytes) -> SimpleNamespace:
    return SimpleNamespace(passed=True, details="test validator: passed")


def _failing_validate(artifact_bytes: bytes) -> SimpleNamespace:
    return SimpleNamespace(passed=False, details="test validator: failed")


def _write_package(
    tmp_path: Path,
    *,
    campaign_id: str = TEST_AGENT_NATIVE_CAMPAIGN,
    allowed_models: list | None = None,
) -> Path:
    pkg = tmp_path / "pkg"
    pkg.mkdir(parents=True)
    policy_raw = build_policy_raw(
        campaign_id=campaign_id,
        max_attempts_per_configuration=3,
        execution_mode="coding_agent_native",
        execution_surface="current_coding_agent",
        external_provider_api_prohibited=True,
        allowed_models=allowed_models or [],
    )
    config_raw = build_configuration_raw(campaign_id=campaign_id)
    # Agent-native: the configuration's model_identifier carries the
    # execution surface (not an external model) and must equal the
    # policy's execution_surface.
    config_raw["model_identifier"] = "current_coding_agent"
    config_raw["configuration_id"] = compute_configuration_id(config_raw)
    policy_raw["allowed_configuration_ids"] = sorted(
        [config_raw["configuration_id"]]
    )
    policy_raw["policy_digest"] = compute_policy_digest(policy_raw)
    (pkg / "campaign-policy.yaml").write_bytes(render_yaml(policy_raw))
    (pkg / "configuration-identity.yaml").write_bytes(render_yaml(config_raw))
    _write_receipt(pkg, _receipt_raw(policy_raw))
    return pkg


def _prepare(
    pkg: Path,
    root: Path,
    *,
    verifier: object = None,
    campaign_id: str = TEST_AGENT_NATIVE_CAMPAIGN,
) -> dict:
    from sensemaking_skills.campaign_validation import parse_two_lane_yaml

    policy_raw = parse_two_lane_yaml(
        (pkg / "campaign-policy.yaml").read_bytes()
    )
    return prepare_next_attempt(
        package_dir=pkg,
        campaign_root=root,
        framework_checkout=Path(__file__).resolve().parents[2],
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        verifier=verifier or _conversation_verifier(policy_raw),
        now=_NOW,
    )


def _events(root: Path, campaign_id: str):
    ledger = CampaignLedger(root / campaign_id, campaign_id)
    return ledger.read_events()


def _attempt_event_types(events, attempt_id: str) -> list[str]:
    return [
        e.event_type
        for e in events
        if e.attempt_id == attempt_id and e.event_type in (
            "RESERVED", "INVOKED", "OUTPUT_CAPTURED",
            "VALIDATION_PASSED", "VALIDATION_FAILED",
            "ABORTED_BEFORE_INVOCATION", "PROVIDER_FAILED",
        )
    ]


# ---------------------------------------------------------------------------
# prepare
# ---------------------------------------------------------------------------


def test_prepare_creates_reservation_instructions_and_invoked(tmp_path: Path) -> None:
    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    result = _prepare(pkg, root)
    attempt_id = result["attempt_id"]
    assert result["remaining_slots"] == 2
    # Durable state: RESERVED then INVOKED.
    assert _attempt_event_types(_events(root, TEST_AGENT_NATIVE_CAMPAIGN), attempt_id) == [
        "RESERVED", "INVOKED",
    ]
    # Frozen instructions exist, name the delivery path, and prohibit APIs.
    instructions = Path(result["instructions_path"]).read_text(encoding="utf-8")
    assert "external_provider_api_prohibited: true" in instructions
    assert "no external model" in instructions.casefold()
    assert result["delivery_path"] in instructions
    # The attempt dir preserves the raw request.
    attempt_dir = root / TEST_AGENT_NATIVE_CAMPAIGN / "attempts" / attempt_id
    assert (attempt_dir / "raw-request.txt").is_file()


def test_prepare_derives_remaining_slots_from_ledger(tmp_path: Path) -> None:
    """The protocol is sequential: prepare -> deliver -> finalize ->
    prepare. Each prepared-but-active attempt holds the concurrency slot,
    and the ledger (not memory) counts reservations."""
    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    for expected_remaining in (2, 1, 0):
        result = _prepare(pkg, root)
        assert result["remaining_slots"] == expected_remaining
        delivery = Path(result["delivery_path"])
        delivery.parent.mkdir(parents=True, exist_ok=True)
        delivery.write_text("# Brief\n", encoding="utf-8")
        finalize_attempt(
            package_dir=pkg,
            campaign_root=root,
            framework_checkout=Path(__file__).resolve().parents[2],
            attempt_id=result["attempt_id"],
            artifact_path=result["delivery_path"],
            allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
            verifier=_pkg_verifier(pkg),
            validate=_passing_validate,
            now=_NOW,
        )
    with pytest.raises(RunnerRefusal, match="no remaining attempt slots"):
        _prepare(pkg, root)


def test_prepare_refuses_when_verifier_refuses(tmp_path: Path) -> None:
    class RefusingVerifier:
        def verify(self, approval, *, approval_bytes=None):
            raise ProvenanceVerificationError("test: approval refused")

    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    with pytest.raises(ProvenanceVerificationError, match="refused"):
        _prepare(pkg, root, verifier=RefusingVerifier())
    assert _events(root, TEST_AGENT_NATIVE_CAMPAIGN) == []
    # Nothing was delivered or reserved.
    assert not (root / ".agent-native").exists()


def test_prepare_refuses_provider_api_campaign(tmp_path: Path) -> None:
    pkg = _write_package(tmp_path, campaign_id=TEST_CAMPAIGN_ID)
    pkg2 = tmp_path / "pkg2"
    pkg2.mkdir()
    # Overwrite with a provider_api policy (no mode fields).
    policy_raw = build_policy_raw(campaign_id=TEST_CAMPAIGN_ID)
    config_raw = build_configuration_raw(campaign_id=TEST_CAMPAIGN_ID)
    policy_raw["allowed_configuration_ids"] = sorted([config_raw["configuration_id"]])
    policy_raw["policy_digest"] = compute_policy_digest(policy_raw)
    from exploratory_fixtures import build_approval_raw
    approval_raw = build_approval_raw(campaign_id=TEST_CAMPAIGN_ID)
    approval_raw["policy_digest"] = policy_raw["policy_digest"]
    (pkg2 / "campaign-policy.yaml").write_bytes(render_yaml(policy_raw))
    (pkg2 / "configuration-identity.yaml").write_bytes(render_yaml(config_raw))
    (pkg2 / "approval.yaml").write_bytes(render_yaml(approval_raw))
    with pytest.raises(RunnerRefusal, match="coding_agent_native"):
        _prepare(pkg2, tmp_path / "root2", campaign_id=TEST_CAMPAIGN_ID)


def test_prepare_refuses_legacy_approval_in_agent_native_mode(
    tmp_path: Path,
) -> None:
    """A valid legacy (github) approval placed as approval.md is refused:
    the conversation mechanism was REPLACED for coding-agent-native
    campaigns; nothing else may authorize them."""
    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    from sensemaking_skills.campaign_validation import parse_two_lane_yaml

    policy_raw = parse_two_lane_yaml(
        (pkg / "campaign-policy.yaml").read_bytes()
    )
    legacy = {
        "approval_schema_version": "1",
        "campaign_id": TEST_AGENT_NATIVE_CAMPAIGN,
        "policy_digest": policy_raw["policy_digest"],
        "claimed_approver_identity": TEST_APPROVER_IDENTITY,
        "approval_provenance": {
            "mechanism": "github_issue_comment_approval",
            "reference": (
                "https://github.com/ThorStarlord/sensemaking-skills/"
                "issues/122#issuecomment-1"
            ),
            "repository": "ThorStarlord/sensemaking-skills",
            "issue_number": "122",
            "comment_id": "1",
            "comment_body_sha256": "a" * 64,
        },
        "approval_statement": "I authorize this campaign.",
        "approved_at": "2026-01-02T00:00:00Z",
    }
    from sensemaking_skills.campaign_validation.yaml_profile import (
        dump_two_lane_yaml,
    )

    md = "---\n" + dump_two_lane_yaml(legacy) + "---\nlegacy prose\n"
    (pkg / CONVERSATION_APPROVAL_FILENAME).write_text(md, encoding="utf-8")
    with pytest.raises(RunnerRefusal, match="active_human_conversation"):
        _prepare(pkg, root)
    assert _events(root, TEST_AGENT_NATIVE_CAMPAIGN) == []


def test_prepare_refuses_before_window_opens(tmp_path: Path) -> None:
    """The mechanical execution gate: a valid receipt does NOT make
    prepare run early. Before validity_window.not_before, prepare refuses
    and creates no reservation, no ledger event, and no attempt."""
    from execution_infra.agent_native_campaign import prepare_next_attempt

    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    from sensemaking_skills.campaign_validation import parse_two_lane_yaml

    policy_raw = parse_two_lane_yaml(
        (pkg / "campaign-policy.yaml").read_bytes()
    )
    # A time before the fixture window opens (not_before = anchor - 30d).
    before_window = _NOW - timedelta(days=60)
    # The receipt's approved_at must be the approval moment (not in the
    # future relative to the validation clock).
    _write_receipt(
        pkg, _receipt_raw(policy_raw, approved_at=before_window.isoformat())
    )
    with pytest.raises(RunnerRefusal, match="validity window has not opened"):
        prepare_next_attempt(
            package_dir=pkg,
            campaign_root=root,
            framework_checkout=Path(__file__).resolve().parents[2],
            allowed_approver_identities=frozenset(),
            verifier=_conversation_verifier(policy_raw),
            now=before_window,
        )
    assert _events(root, TEST_AGENT_NATIVE_CAMPAIGN) == []
    assert not (root / TEST_AGENT_NATIVE_CAMPAIGN / "attempts").exists()


def test_validate_approval_succeeds_before_window(tmp_path: Path) -> None:
    """Approval validity is window-INDEPENDENT: the receipt validates any
    time after presentation and before expiry, even before the execution
    window opens."""
    from execution_infra.agent_native_campaign import validate_approval

    pkg = _write_package(tmp_path)
    from sensemaking_skills.campaign_validation import parse_two_lane_yaml

    policy_raw = parse_two_lane_yaml(
        (pkg / "campaign-policy.yaml").read_bytes()
    )
    before_window = _NOW - timedelta(days=60)
    _write_receipt(
        pkg, _receipt_raw(policy_raw, approved_at=before_window.isoformat())
    )
    result = validate_approval(
        package_dir=pkg,
        allowed_approver_identities=frozenset(),
        now=before_window,
    )
    assert result["campaign_id"] == TEST_AGENT_NATIVE_CAMPAIGN
    assert result["policy_digest"] == policy_raw["policy_digest"]
    assert result["window_independent"] is True
    assert result["reference"] == "test-session#message-42"


def test_validate_approval_creates_no_residue(tmp_path: Path) -> None:
    """validate-approval performs NO reservation, NO invocation, and
    creates no ledger event or attempt directory."""
    from execution_infra.agent_native_campaign import validate_approval

    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    validate_approval(
        package_dir=pkg,
        allowed_approver_identities=frozenset(),
        now=_NOW,
    )
    assert _events(root, TEST_AGENT_NATIVE_CAMPAIGN) == []
    assert not (root / TEST_AGENT_NATIVE_CAMPAIGN).exists()
    assert not (pkg / "ledger.jsonl").exists()


def test_validate_approval_refuses_bad_receipt(tmp_path: Path) -> None:
    """A receipt that does not bind the exact envelope is refused even
    window-independently."""
    from execution_infra.agent_native_campaign import validate_approval

    pkg = _write_package(tmp_path)
    (pkg / "approval.md").write_text(
        (pkg / "approval.md").read_text(encoding="utf-8").replace(
            '"approve"', '"denied"'
        ),
        encoding="utf-8",
    )
    with pytest.raises(RunnerRefusal):
        validate_approval(
            package_dir=pkg,
            allowed_approver_identities=frozenset(),
            now=_NOW,
        )


def test_prepare_real_campaign_refuses_injection(tmp_path: Path) -> None:
    pkg = _write_package(tmp_path, campaign_id=AGENT_NATIVE_REAL_CAMPAIGN_ID)
    with pytest.raises(RunnerRefusal, match="injected execution components"):
        _prepare(pkg, tmp_path / "root", campaign_id=AGENT_NATIVE_REAL_CAMPAIGN_ID)


# ---------------------------------------------------------------------------
# finalize
# ---------------------------------------------------------------------------


def _prepare_and_deliver(
    tmp_path: Path, *, validate=None
) -> tuple[dict, Path, Path]:
    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    result = _prepare(pkg, root)
    delivery = Path(result["delivery_path"])
    delivery.parent.mkdir(parents=True, exist_ok=True)
    delivery.write_text("# Repository Sensemaking Brief\n\nTest brief bytes.\n", encoding="utf-8")
    return result, pkg, root


def test_finalize_records_terminal_state(tmp_path: Path) -> None:
    result, pkg, root = _prepare_and_deliver(tmp_path)
    outcome = finalize_attempt(
        package_dir=pkg,
        campaign_root=root,
        framework_checkout=Path(__file__).resolve().parents[2],
        attempt_id=result["attempt_id"],
        artifact_path=result["delivery_path"],
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        verifier=_pkg_verifier(pkg),
        validate=_passing_validate,
        now=_NOW,
    )
    assert outcome["validation_passed"] is True
    events = _attempt_event_types(_events(root, TEST_AGENT_NATIVE_CAMPAIGN), result["attempt_id"])
    assert events == ["RESERVED", "INVOKED", "OUTPUT_CAPTURED", "VALIDATION_PASSED"]
    attempt_dir = root / TEST_AGENT_NATIVE_CAMPAIGN / "attempts" / result["attempt_id"]
    for name in ("raw-output.md", "produced-artifact.md", "validation-result.json", "attempt-result.yaml"):
        assert (attempt_dir / name).is_file(), name


def test_finalize_records_validation_failure(tmp_path: Path) -> None:
    result, pkg, root = _prepare_and_deliver(tmp_path)
    outcome = finalize_attempt(
        package_dir=pkg,
        campaign_root=root,
        framework_checkout=Path(__file__).resolve().parents[2],
        attempt_id=result["attempt_id"],
        artifact_path=result["delivery_path"],
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        verifier=_pkg_verifier(pkg),
        validate=_failing_validate,
        now=_NOW,
    )
    assert outcome["validation_passed"] is False
    events = _attempt_event_types(_events(root, TEST_AGENT_NATIVE_CAMPAIGN), result["attempt_id"])
    assert events[-1] == "VALIDATION_FAILED"


def test_finalize_refuses_missing_artifact(tmp_path: Path) -> None:
    result, pkg, root = _prepare_and_deliver(tmp_path)
    with pytest.raises(RunnerRefusal, match="no delivered artifact"):
        finalize_attempt(
            package_dir=pkg,
            campaign_root=root,
            framework_checkout=Path(__file__).resolve().parents[2],
            attempt_id=result["attempt_id"],
            artifact_path=tmp_path / "does-not-exist.md",
            allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
            verifier=_pkg_verifier(pkg),
            validate=_passing_validate,
            now=_NOW,
        )


def test_finalize_refuses_non_invoked_attempt(tmp_path: Path) -> None:
    pkg = _write_package(tmp_path)
    root = tmp_path / "root"
    from sensemaking_skills.campaign_accounting import CampaignAccountingError

    # Prepare one attempt so the ledger exists, then finalize a DIFFERENT
    # (never-reserved) attempt id: it is not in the INVOKED state.
    result = _prepare(pkg, root)
    artifact = tmp_path / "artifact.md"
    artifact.write_text("# Brief\n", encoding="utf-8")
    with pytest.raises(CampaignAccountingError):
        finalize_attempt(
            package_dir=pkg,
            campaign_root=root,
            framework_checkout=Path(__file__).resolve().parents[2],
            attempt_id="00000000-0000-0000-0000-000000000000",
            artifact_path=artifact,
            allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
            verifier=_pkg_verifier(pkg),
            validate=_passing_validate,
            now=_NOW,
        )


def test_finalize_refuses_artifact_outside_delivery_dir(tmp_path: Path) -> None:
    """finalize only records the agent's brief inside the attempt's own
    delivery directory; any other readable file is refused."""
    result, pkg, root = _prepare_and_deliver(tmp_path)
    elsewhere = tmp_path / "unrelated.md"
    elsewhere.write_text("# Not the delivery\n", encoding="utf-8")
    with pytest.raises(RunnerRefusal, match="outside the attempt delivery"):
        finalize_attempt(
            package_dir=pkg,
            campaign_root=root,
            framework_checkout=Path(__file__).resolve().parents[2],
            attempt_id=result["attempt_id"],
            artifact_path=elsewhere,
            allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
            verifier=_pkg_verifier(pkg),
            validate=_passing_validate,
            now=_NOW,
        )
    # Nothing was recorded for the attempt beyond prepare's INVOKED.
    events = _attempt_event_types(_events(root, TEST_AGENT_NATIVE_CAMPAIGN), result["attempt_id"])
    assert events == ["RESERVED", "INVOKED"]


def test_finalize_reenforces_approval(tmp_path: Path) -> None:
    """The approval is re-verified at finalize: a revoked approval stops
    the attempt before anything is recorded."""
    class RefusingVerifier:
        def verify(self, approval, *, approval_bytes=None):
            raise ProvenanceVerificationError("test: approval revoked")

    result, pkg, root = _prepare_and_deliver(tmp_path)
    with pytest.raises(ProvenanceVerificationError, match="revoked"):
        finalize_attempt(
            package_dir=pkg,
            campaign_root=root,
            framework_checkout=Path(__file__).resolve().parents[2],
            attempt_id=result["attempt_id"],
            artifact_path=result["delivery_path"],
            allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
            verifier=RefusingVerifier(),
            validate=_passing_validate,
            now=_NOW,
        )
    events = _attempt_event_types(_events(root, TEST_AGENT_NATIVE_CAMPAIGN), result["attempt_id"])
    assert events == ["RESERVED", "INVOKED"], "no terminal state may be recorded"


# ---------------------------------------------------------------------------
# report + runner refusal + no SDK import
# ---------------------------------------------------------------------------


def test_report_enumerates_every_attempt(tmp_path: Path) -> None:
    result, pkg, root = _prepare_and_deliver(tmp_path)
    finalize_attempt(
        package_dir=pkg,
        campaign_root=root,
        framework_checkout=Path(__file__).resolve().parents[2],
        attempt_id=result["attempt_id"],
        artifact_path=result["delivery_path"],
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        verifier=_pkg_verifier(pkg),
        validate=_passing_validate,
        now=_NOW,
    )
    report = build_report(
        package_dir=pkg,
        campaign_root=root,
        framework_checkout=Path(__file__).resolve().parents[2],
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
        now=_NOW,
    )
    assert result["attempt_id"] in report
    assert "VALIDATION_PASSED" in report
    assert "nothing-omitted" in report.casefold()
    assert "EXPLORATORY_NOT_CANONICAL_EVIDENCE" in report


def test_provider_loop_runner_refuses_agent_native(tmp_path: Path) -> None:
    pkg = _write_package(tmp_path)
    runner = GovernedCampaignRunner(
        campaign_package_dir=pkg,
        campaign_root=tmp_path / "root",
        framework_checkout=Path(__file__).resolve().parents[2],
        verifier=_pkg_verifier(pkg),
        provider=lambda **kwargs: None,
        validate=_passing_validate,
        allowed_approver_identities=frozenset({TEST_APPROVER_IDENTITY}),
    )
    with pytest.raises(RunnerRefusal, match="coding_agent_native"):
        runner.run()


def test_agent_native_path_never_imports_provider_sdk() -> None:
    assert "claude_agent_sdk" not in sys.modules
    from execution_infra import agent_native_campaign  # noqa: F401
    assert "claude_agent_sdk" not in sys.modules
    assert "anthropic" not in sys.modules


# ---------------------------------------------------------------------------
# policy-mode coupling (framework-level)
# ---------------------------------------------------------------------------


def test_policy_mode_coupling_enforced() -> None:
    ctx = ValidationContext(
        current_time=TEST_VALIDATION_TIME,
        allowed_approver_identities=frozenset(),
    )
    raw = build_policy_raw(
        execution_mode="coding_agent_native",
        execution_surface="current_coding_agent",
        external_provider_api_prohibited=True,
        allowed_models=[],
    )
    raw["policy_digest"] = compute_policy_digest(raw)
    assert validate_campaign_policy(render_yaml(raw), ctx).valid

    # Non-empty allowed_models fails for the native mode.
    raw2 = dict(raw)
    raw2["allowed_models"] = ["claude-sonnet-5"]
    raw2["policy_digest"] = compute_policy_digest(raw2)
    assert not validate_campaign_policy(render_yaml(raw2), ctx).valid

    # prohibited: true without the native mode fails.
    raw3 = build_policy_raw(external_provider_api_prohibited=True)
    raw3["policy_digest"] = compute_policy_digest(raw3)
    assert not validate_campaign_policy(render_yaml(raw3), ctx).valid

    # Unknown mode value fails.
    raw4 = dict(raw)
    raw4["execution_mode"] = "telepathy"
    raw4["policy_digest"] = compute_policy_digest(raw4)
    assert not validate_campaign_policy(render_yaml(raw4), ctx).valid

    # Legacy provider_api policy (fields absent) still validates.
    legacy = build_policy_raw()
    legacy["policy_digest"] = compute_policy_digest(legacy)
    assert validate_campaign_policy(render_yaml(legacy), ctx).valid
