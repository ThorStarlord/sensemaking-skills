"""Stopping-state validation of the Evidence 0016 run-control artifacts.

These tests read the REAL run-control directory: the authorization record and
the stored digest file. They never write to the directory, never mint an
authorization capability, and never invoke a model or a provider of any kind.

The remediation of PR #113 removed the operative ``owner-approval.md``: the
approval it contained bound a PREVIOUS record digest (the old preparation
package was corrected, so the record had to be regenerated, so the old
approval no longer bound anything). The repository owner has since approved
the new record digest (``bf31c7b6...``) in a fresh, human-authored artifact
at the exact contract path. The current state is: a well-formed record, a
valid stored digest, and exactly one operative owner approval binding that
exact digest.

The two invalidated digests (``ccd25fac...``, ``9cf76a34...``) are not
asserted here; only the current approved digest, and the invariants that
keep it approvable and untransferable.
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
    CONTRACT_AUTHORIZATION_STATUS,
    CONTRACT_APPROVING_AUTHORITIES,
    REQUIRED_APPROVAL_FIELDS,
    REQUIRED_RECORD_FIELDS,
    REQUIRED_SAFETY_BOOLEANS,
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
TEMPLATE = RUN_CONTROL / "owner-approval.template.md"


def test_owner_approval_is_present_and_binds_the_current_record_digest():
    """The repository owner approved this record's digest (PR #113, 2026-08-01).

    The approval must exist at the exact contract path, parse successfully
    with the real consumer, name an approving identity in
    CONTRACT_APPROVING_AUTHORITIES that differs from the record's author, and
    bind exactly the digest the record's own bytes recompute to -- never an
    inferred or transferred digest.
    """
    assert RECORD.is_file()
    assert DIGEST.is_file()
    assert TEMPLATE.is_file()
    assert APPROVAL.is_file()
    assert TEMPLATE.name != "owner-approval.md"

    record, record_code, record_detail = parse_record_bytes(RECORD.read_bytes())
    assert record_code is None, record_detail
    computed_record_sha = hashlib.sha256(RECORD.read_bytes()).hexdigest()

    fields, code, detail = parse_approval_bytes(APPROVAL.read_bytes())
    assert code is None, detail
    missing = [f for f in REQUIRED_APPROVAL_FIELDS if not fields.get(f, "").strip()]
    assert not missing, f"approval missing required fields: {missing}"
    assert fields["authorization_record_sha256"] == computed_record_sha, (
        "approval does not bind the exact current record digest"
    )
    assert fields["approver_github_identity"] in CONTRACT_APPROVING_AUTHORITIES
    assert fields["approver_github_identity"] != record["authorization_record_created_by"]


def test_only_the_exact_planned_artifact_set_exists():
    """The approval-present allowlist: template and operative approval both
    present, exactly once each, nowhere else in the repository."""
    assert {p.name for p in RUN_CONTROL.rglob("*") if p.is_file()} == {
        ".gitattributes",
        "authorization-record.yaml",
        "authorization-record.sha256",
        "owner-approval.template.md",
        "owner-approval.md",
    }
    assert [
        str(p.relative_to(REPO_ROOT)).replace("\\", "/")
        for p in REPO_ROOT.rglob("owner-approval.md")
        if ".git" not in p.parts
    ] == [str(APPROVAL.relative_to(REPO_ROOT)).replace("\\", "/")], (
        "owner-approval.md must exist exactly once, at the contract path"
    )


def test_record_digest_recomputes_and_matches_the_stored_digest():
    raw = RECORD.read_bytes()
    assert b"\r" not in raw, "record must be LF-only so its digest is byte-stable"
    computed = hashlib.sha256(raw).hexdigest()
    stored = DIGEST.read_text(encoding="utf-8").strip()
    assert computed == stored
    assert len(computed) == 64 and computed == computed.lower()


def test_record_parses_and_is_well_formed():
    record, code, detail = parse_record_bytes(RECORD.read_bytes())
    assert code is None, detail
    assert record is not None
    missing = [f for f in REQUIRED_RECORD_FIELDS if not str(record.get(f, "")).strip()]
    assert not missing, f"record missing required fields: {missing}"
    for field in REQUIRED_SAFETY_BOOLEANS:
        assert record[field] is True, f"{field} must be an exact boolean true"
    assert record["authorization_status"] == CONTRACT_AUTHORIZATION_STATUS
    assert record["authorization_record_created_by"] != "ThorStarlord"


def test_record_pins_the_new_preparation_package_digest():
    """The regenerated record must bind the CURRENT package bytes.

    This is the whole point of the remediation: the old record pinned the
    uncorrected preparation package, so the corrected package forced a record
    regeneration, which in turn invalidated the old approval. The new record
    pins the corrected package, making it the approvable target.
    """
    record, code, detail = parse_record_bytes(RECORD.read_bytes())
    assert code is None, detail
    package_path = REPO_ROOT / record["preparation_package_path"]
    assert package_path.is_file(), record["preparation_package_path"]
    assert (
        hashlib.sha256(package_path.read_bytes()).hexdigest()
        == record["preparation_package_sha256"]
    ), "record pins a stale preparation-package digest"


def test_provenance_digests_match_the_governing_documents():
    record, code, _ = parse_record_bytes(RECORD.read_bytes())
    assert code is None
    for path_field, digest_field in (
        ("preparation_package_path", "preparation_package_sha256"),
        ("gate_d_checklist_path", "gate_d_checklist_sha256"),
    ):
        target = REPO_ROOT / record[path_field]
        assert target.is_file(), record[path_field]
        assert hashlib.sha256(target.read_bytes()).hexdigest() == record[digest_field]


def test_approval_template_remains_the_future_shape():
    text = TEMPLATE.read_text(encoding="utf-8")
    assert "TEMPLATE ONLY" in text
    assert "NOT AN APPROVAL" in text
