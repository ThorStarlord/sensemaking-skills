"""Validation of the real owner-approval artifact and its exact-digest binding.

These tests read the REAL run-control directory: the authorization record,
the stored digest file, and the owner-approval artifact. They never write to
the directory, never mint an authorization capability, and never invoke a
model or a provider of any kind.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from gate_a_authorization import (  # noqa: E402
    CONTRACT_APPROVING_AUTHORITIES,
    CONTRACT_AUTHORIZATION_STATUS,
    REQUIRED_APPROVAL_FIELDS,
    SENTINEL_VALUES,
    parse_approval_bytes,
    parse_record_bytes,
)

RUN_CONTROL = (
    REPO_ROOT
    / "experiments"
    / "run-control"
    / "0016-stage1-auteur-post-remediation-controlled-attempt"
)
RECORD = RUN_CONTROL / "authorization-record.yaml"
DIGEST = RUN_CONTROL / "authorization-record.sha256"
APPROVAL = RUN_CONTROL / "owner-approval.md"

APPROVED_DIGEST = "ccd25facdf8c01d9b0e95ba3ae2d724c7a29ee1aca57d0ac2a77ce496e65d9e1"

OWNER_STATEMENTS = (
    "supplied directly by the repository owner in this prompt",
    "did not infer, delegate, or manufacture",
    "does not itself authorize live model invocation",
    "remain separate controlled steps",
    "invalidates this approval",
)


def test_approval_artifact_exists_only_at_the_contract_path():
    assert APPROVAL.is_file()
    assert list(REPO_ROOT.rglob("owner-approval.md")) == [APPROVAL]


def test_record_digest_recomputes_to_the_approved_digest():
    computed = hashlib.sha256(RECORD.read_bytes()).hexdigest()
    stored = DIGEST.read_text(encoding="utf-8").strip()
    assert computed == APPROVED_DIGEST
    assert stored == APPROVED_DIGEST


def test_record_bytes_are_lf_only():
    assert b"\r" not in RECORD.read_bytes()


def test_approval_parses_with_the_real_consumer_parser():
    approval, code, detail = parse_approval_bytes(APPROVAL.read_bytes())
    assert code is None, detail
    assert approval is not None


def test_approval_carries_every_required_field_exactly_once():
    text = APPROVAL.read_text(encoding="utf-8")
    for field in REQUIRED_APPROVAL_FIELDS:
        assert text.count(f"{field}:") == 1, field
    approval, code, detail = parse_approval_bytes(APPROVAL.read_bytes())
    assert code is None, detail
    missing = [f for f in REQUIRED_APPROVAL_FIELDS
               if not str(approval.get(f, "")).strip()]
    assert not missing
    sentinel = [f for f in REQUIRED_APPROVAL_FIELDS
                if str(approval.get(f, "")).strip().upper() in SENTINEL_VALUES]
    assert not sentinel


def test_approval_binds_the_exact_recomputed_digest():
    computed = hashlib.sha256(RECORD.read_bytes()).hexdigest()
    approval, _, _ = parse_approval_bytes(APPROVAL.read_bytes())
    assert approval["authorization_record_sha256"] == computed == APPROVED_DIGEST


def test_approval_decision_and_identity():
    approval, _, _ = parse_approval_bytes(APPROVAL.read_bytes())
    assert approval["authorization_decision"] == CONTRACT_AUTHORIZATION_STATUS
    approver = approval["approver_github_identity"]
    assert approver in CONTRACT_APPROVING_AUTHORITIES
    record, rec_code, _ = parse_record_bytes(RECORD.read_bytes())
    assert rec_code is None
    assert record["authorization_record_created_by"] != approver


def test_approval_agrees_with_the_record_on_every_pinned_value():
    approval, _, _ = parse_approval_bytes(APPROVAL.read_bytes())
    record, rec_code, _ = parse_record_bytes(RECORD.read_bytes())
    assert rec_code is None
    for ap_field, rec_field in (
        ("execution_framework_sha", "execution_framework_sha"),
        ("target_sha", "target_sha"),
        ("evidence_number", "evidence_number"),
        ("evidence_slug", "evidence_slug"),
        ("exact_model", "exact_model"),
    ):
        assert approval[ap_field] == record[rec_field], ap_field


def test_approval_carries_the_owner_required_statements():
    text = " ".join(APPROVAL.read_text(encoding="utf-8").split())
    for statement in OWNER_STATEMENTS:
        assert statement in text
