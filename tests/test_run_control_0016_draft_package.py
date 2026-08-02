"""Draft-package preflight for the Evidence 0016 run-control artifacts.

These tests read the REAL run-control directory
(``experiments/run-control/0016-stage1-auteur-post-remediation-controlled-attempt``)
but never write to it, never create ``owner-approval.md``, never mint an
authorization capability, and never invoke a model or a provider of any kind.

They assert two complementary facts:

1. **Negative (the real package as committed):** Gate A denies the package,
   and denies it *specifically* for the missing owner approval - not for a
   malformed record. Absence of ``owner-approval.md`` is the intended
   pre-approval hard stop.

2. **Positive control (temporary copy, synthetic approval):** the exact
   committed record bytes pass every other Gate A check - schema, status,
   digest, pins, provenance digests, safety booleans - when a synthetic
   approval is placed beside a temporary copy in ``tmp_path``. This is what
   proves the denial in (1) is reached at the *final* gate rather than early.
"""

from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from gate_a_authorization import (  # noqa: E402
    CONTRACT_AUTHORIZATION_STATUS,
    CONTRACT_SCHEMA_VERSION,
    GATE_A_OWNER_APPROVAL_MISSING,
    REQUIRED_RECORD_FIELDS,
    REQUIRED_SAFETY_BOOLEANS,
    AuthorizationContext,
    authorize,
    parse_record_bytes,
)

import gate_a_fixtures as fx  # noqa: E402

RUN_CONTROL = (
    REPO_ROOT
    / "experiments"
    / "run-control"
    / "0016-stage1-auteur-post-remediation-controlled-attempt"
)
RECORD = RUN_CONTROL / "authorization-record.yaml"
DIGEST = RUN_CONTROL / "authorization-record.sha256"
TEMPLATE = RUN_CONTROL / "owner-approval.template.md"
APPROVAL = RUN_CONTROL / "owner-approval.md"

EXPECTED_FRAMEWORK_SHA = "98a08d50a0a8dbca4599296e717ab60f1d567d83"
EXPECTED_TARGET_SHA = "0653defb05625f2fcde0ac32eac6e59ccf7eeb90"


def _record_bytes() -> bytes:
    return RECORD.read_bytes()


def test_draft_artifacts_present_and_approval_absent():
    assert RECORD.is_file()
    assert DIGEST.is_file()
    assert TEMPLATE.is_file()
    # The operative owner approval must NOT exist. This is the pre-approval
    # hard stop; creating it is an owner-only act.
    assert not APPROVAL.exists()


def test_only_the_exact_planned_artifact_set_exists():
    """An allowlist, not a prefix rule.

    Forbids: owner-approval.md anywhere, duplicate records, duplicate digests,
    any second run-control directory, and any Evidence 0016 output smuggled in
    under run-control.

    ``owner-approval.SUPERSEDED-pre-artifact-root.md`` is permitted: it is the
    historical PR #113 approval, renamed out of the active-approval path (see
    module docstring) after the artifact-root topology (PR #114) forced a
    record regeneration and invalidated its digest binding. Its name does not
    match ``owner-approval.md`` and Gate A never reads it.
    """
    root = RUN_CONTROL.parent
    assert sorted(p.name for p in root.iterdir() if p.is_dir()) == [
        "0016-stage1-auteur-post-remediation-controlled-attempt"
    ], "exactly one run-control directory is permitted"
    assert not [p for p in root.iterdir() if p.is_file()]
    assert {p.name for p in RUN_CONTROL.rglob("*") if p.is_file()} == {
        ".gitattributes",
        "authorization-record.yaml",
        "authorization-record.sha256",
        "owner-approval.template.md",
        "owner-approval.SUPERSEDED-pre-artifact-root.md",
    }
    assert not list(REPO_ROOT.rglob("owner-approval.md"))


def test_record_bytes_are_lf_only_and_match_digest_file():
    raw = _record_bytes()
    assert b"\r" not in raw, "record must be LF-only so its digest is byte-stable"
    computed = hashlib.sha256(raw).hexdigest()
    stored = DIGEST.read_text(encoding="utf-8").strip()
    assert stored == computed
    assert len(stored) == 64 and stored == stored.lower()


def test_record_schema_is_complete_and_pinned():
    record, code, detail = parse_record_bytes(_record_bytes())
    assert code is None, detail
    assert str(record["schema_version"]) == CONTRACT_SCHEMA_VERSION
    assert record["authorization_status"] == CONTRACT_AUTHORIZATION_STATUS
    assert not [f for f in REQUIRED_RECORD_FIELDS if f not in record]
    for field in REQUIRED_SAFETY_BOOLEANS:
        assert record[field] is True, f"{field} must be an exact boolean true"
    assert record["execution_framework_sha"] == EXPECTED_FRAMEWORK_SHA
    assert record["target_sha"] == EXPECTED_TARGET_SHA
    assert record["authorization_record_created_by"] != "ThorStarlord"


def test_provenance_digests_match_the_governing_documents():
    record, code, _ = parse_record_bytes(_record_bytes())
    assert code is None
    for path_field, digest_field in (
        ("preparation_package_path", "preparation_package_sha256"),
        ("gate_d_checklist_path", "gate_d_checklist_sha256"),
    ):
        target = REPO_ROOT / record[path_field]
        assert target.is_file(), record[path_field]
        assert hashlib.sha256(target.read_bytes()).hexdigest() == record[digest_field]


def test_template_is_non_operative():
    text = TEMPLATE.read_text(encoding="utf-8")
    assert "TEMPLATE ONLY" in text
    assert "NOT AN APPROVAL" in text
    assert TEMPLATE.name != "owner-approval.md"


def _context_for(tmp_path: Path, run_control_dir: Path, *, approval_path: Path):
    framework_root = fx.make_framework_root(tmp_path)
    target_root = fx.make_target_root(tmp_path)
    return AuthorizationContext(
        framework_root=framework_root,
        target_root=target_root,
        execution_framework_sha=EXPECTED_FRAMEWORK_SHA,
        target_sha=EXPECTED_TARGET_SHA,
        evidence_number=fx.EVIDENCE_NUMBER,
        evidence_slug=fx.EVIDENCE_SLUG,
        exact_model=fx.EXACT_MODEL,
        artifact_type=fx.ARTIFACT_TYPE,
        invocation_limit=1,
        authorization_record_path=run_control_dir / "authorization-record.yaml",
        authorization_digest_path=run_control_dir / "authorization-record.sha256",
        owner_approval_path=approval_path,
        run_control_commit_sha="2" * 40,
        operator_identity="campaign-operator-agent",
        evidence_output_dir=tmp_path / "evidence-0016-absent",
    )


def test_gate_a_denies_real_package_for_missing_owner_approval(tmp_path):
    """Negative case: the committed package, exactly as it stands."""
    ctx = _context_for(tmp_path, RUN_CONTROL, approval_path=APPROVAL)

    def git_head(root: Path) -> str:
        return {
            str(ctx.framework_root): EXPECTED_FRAMEWORK_SHA,
            str(ctx.target_root): EXPECTED_TARGET_SHA,
        }.get(str(root), "")

    decision, snapshot = authorize(
        ctx, git_head=git_head,
        run_control_commit_resolver=lambda a, b: "2" * 40,
    )
    assert decision.authorized is False
    assert decision.failure_code == GATE_A_OWNER_APPROVAL_MISSING
    assert snapshot is None
    assert not APPROVAL.exists()


def test_positive_control_record_passes_every_other_gate(tmp_path):
    """The exact committed record bytes, with a SYNTHETIC approval, in tmp_path.

    Proves the record is well-formed all the way through the owner-approval
    gate, so the denial above is the final boundary and not an early reject.
    Nothing here touches the real run-control directory.
    """
    raw = _record_bytes()
    rc = tmp_path / "run-control-copy"
    rc.mkdir()
    (rc / "authorization-record.yaml").write_bytes(raw)
    (rc / "authorization-record.sha256").write_bytes(
        (hashlib.sha256(raw).hexdigest() + "\n").encode("utf-8")
    )
    approval_path = rc / "owner-approval.md"
    approval_path.write_text(
        fx.approval_text(
            hashlib.sha256(raw).hexdigest(),
            execution_framework_sha=EXPECTED_FRAMEWORK_SHA,
        ),
        encoding="utf-8",
        newline="",
    )

    ctx = _context_for(tmp_path, rc, approval_path=approval_path)
    # The framework fixture copies the real governing documents, so the
    # record's provenance digests must validate against them unchanged.
    for rel in (fx.PACKAGE_REL, fx.CHECKLIST_REL):
        shutil.copyfile(REPO_ROOT / rel, ctx.framework_root / rel)

    def git_head(root: Path) -> str:
        return {
            str(ctx.framework_root): EXPECTED_FRAMEWORK_SHA,
            str(ctx.target_root): EXPECTED_TARGET_SHA,
        }.get(str(root), "")

    decision, snapshot = authorize(
        ctx, git_head=git_head,
        run_control_commit_resolver=lambda a, b: "2" * 40,
    )
    assert decision.authorized is True, (
        f"record failed a gate other than owner approval: "
        f"{decision.failure_code} {decision.failure_detail}"
    )
    assert snapshot is not None
    # Still no real approval, and no capability was minted: authorize() is a
    # pure read-only evaluation and no provider was constructed or called.
    assert not APPROVAL.exists()
