"""Stopping-state validation of the Evidence 0016 run-control artifacts.

These tests read the REAL run-control directory: the authorization record and
the stored digest file. They never write to the directory, never mint an
authorization capability, and never invoke a model or a provider of any kind.

The artifact-root topology change (PR #114, merged as main commit
``98a08d5...``) forced a regeneration of the authorization record: it now
pins the new ``execution_framework_sha``, which changes the record's bytes
and therefore its digest. The PR #113 owner approval bound the PREVIOUS
digest and cannot bind the new one, so it was renamed to
``owner-approval.SUPERSEDED-pre-artifact-root.md`` (historical record,
preserved rather than deleted; see that file's own banner) and is no longer
at the contract path. Until the repository owner approves the NEW record
digest in a fresh artifact at the exact contract path, the stopping state
holds: a well-formed record, a valid stored digest, and NO operative owner
approval. The Gate A consumer therefore denies the package at the approval
gate.

The old approval's historical existence is not asserted here; only its
absence at the stopping state, and the invariants that make the NEW digest
approvable.
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
    REQUIRED_RECORD_FIELDS,
    REQUIRED_SAFETY_BOOLEANS,
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


def test_stopping_state_has_no_operative_owner_approval():
    """The draft record exists; the operative approval does not.

    The old approval bound the previous record digest and was invalidated by
    the record regeneration. Signing a fresh approval for the new digest is an
    owner-only act that has not happened, so no owner-approval.md exists.
    """
    assert RECORD.is_file()
    assert DIGEST.is_file()
    assert TEMPLATE.is_file()
    assert not APPROVAL.exists()
    assert list(REPO_ROOT.rglob("owner-approval.md")) == []
    assert TEMPLATE.name != "owner-approval.md"


def test_only_the_exact_planned_artifact_set_exists():
    """The stopping-state allowlist: template present, operative approval absent.

    ``owner-approval.SUPERSEDED-pre-artifact-root.md`` is the historical PR
    #113 approval, relocated out of the active-approval path; it is not
    ``owner-approval.md`` and Gate A never reads it.
    """
    assert {p.name for p in RUN_CONTROL.rglob("*") if p.is_file()} == {
        ".gitattributes",
        "authorization-record.yaml",
        "authorization-record.sha256",
        "owner-approval.template.md",
        "owner-approval.SUPERSEDED-pre-artifact-root.md",
    }


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
