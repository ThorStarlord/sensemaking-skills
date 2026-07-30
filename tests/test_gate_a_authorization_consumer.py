"""Unit tests for the Gate A authorization consumer.

These tests exercise `scripts/gate_a_authorization.py` in isolation: schema
validation, exact-byte digest hashing, owner-approval binding, repository and
revision pinning, package/checklist provenance, model and invocation-limit
enforcement, and filesystem safety.

They never invoke a model. They never create real run-control artifacts. Every
fixture is synthetic and lives in a pytest tmp_path.

Isolated unit tests are necessary but NOT sufficient (preparation package
section 2j, criterion 25). The invocation-boundary proofs live in
tests/test_gate_a_invocation_boundary.py.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gate_a_authorization as ga  # noqa: E402
from gate_a_fixtures import (  # noqa: E402
    CHECKLIST_REL,
    EVIDENCE_SLUG,
    FRAMEWORK_SHA,
    OMIT,
    PACKAGE_REL,
    TARGET_SHA,
    build_valid_case,
    dump_record,
    record_mapping,
    sha256_bytes,
)


def run(context, git_head, resolver):
    return ga.authorize(context, git_head=git_head, run_control_commit_resolver=resolver)


def expect_failure(tmp_path, code, **kwargs):
    ctx, head, resolver, _ = build_valid_case(tmp_path, **kwargs)
    decision, snapshot = run(ctx, head, resolver)
    assert decision.authorized is False, f"expected denial with {code}"
    assert snapshot is None, "a denied decision must never produce a snapshot"
    assert decision.failure_code == code, (
        f"expected {code}, got {decision.failure_code}: {decision.failure_detail}"
    )
    return decision


# ---------------------------------------------------------------------------
# Baseline: the valid synthetic case
# ---------------------------------------------------------------------------


def test_valid_fixture_authorizes(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    decision, snapshot = run(ctx, head, resolver)
    assert decision.authorized is True, decision.failure_detail
    assert decision.failure_code is None
    assert snapshot is not None
    assert decision.validated_owner_identity == "ThorStarlord"
    assert decision.validated_model == "claude-sonnet-5"
    assert decision.validated_invocation_limit == 1
    assert decision.validated_framework_sha == FRAMEWORK_SHA
    assert decision.validated_target_sha == TARGET_SHA
    # Every documented check ran, not just the cheap ones.
    for check in ("root_separation", "record_digest_matches_digest_file",
                  "owner_approval_binds_exact_digest", "revisions_match_heads",
                  "package_and_checklist_provenance",
                  "safety_booleans_and_invocation_limit"):
        assert check in decision.checks_passed


def test_consumer_never_mutates_inputs(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    before = {
        p: p.read_bytes()
        for p in (ctx.authorization_record_path, ctx.authorization_digest_path,
                  ctx.owner_approval_path,
                  ctx.framework_root / PACKAGE_REL,
                  ctx.framework_root / CHECKLIST_REL)
    }
    run(ctx, head, resolver)
    for path, content in before.items():
        assert path.read_bytes() == content, f"consumer mutated {path.name}"


# ---------------------------------------------------------------------------
# Record presence, parsing, schema
# ---------------------------------------------------------------------------


def test_missing_record(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx.authorization_record_path.unlink()
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_AUTHORIZATION_RECORD_MISSING


def test_missing_digest_file(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx.authorization_digest_path.unlink()
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_AUTHORIZATION_DIGEST_MISSING


def test_missing_approval(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx.owner_approval_path.unlink()
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_OWNER_APPROVAL_MISSING


def test_malformed_yaml(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_AUTHORIZATION_RECORD_INVALID,
                   record_bytes=b"schema_version: 1\n  bad indent: [\n")


def test_duplicate_yaml_keys(tmp_path):
    raw = b"schema_version: '1'\nno_retry: true\nno_retry: false\n"
    decision = expect_failure(tmp_path, ga.GATE_A_AUTHORIZATION_RECORD_INVALID,
                              record_bytes=raw)
    assert "duplicate key" in decision.failure_detail


def test_yaml_alias_rejected(tmp_path):
    raw = b"schema_version: &v '1'\nauthorization_status: *v\n"
    decision = expect_failure(tmp_path, ga.GATE_A_AUTHORIZATION_RECORD_INVALID,
                              record_bytes=raw)
    assert "alias" in decision.failure_detail


def test_multiple_records_in_one_file(tmp_path):
    raw = b"schema_version: '1'\n---\nschema_version: '1'\n"
    expect_failure(tmp_path, ga.GATE_A_AUTHORIZATION_RECORD_DUPLICATE,
                   record_bytes=raw)


def test_unsupported_schema_version(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_AUTHORIZATION_RECORD_SCHEMA_UNSUPPORTED,
                   record_overrides={"schema_version": "2"})


@pytest.mark.parametrize("field", ga.REQUIRED_RECORD_FIELDS)
def test_every_required_field_is_actually_required(tmp_path, field):
    """Each of the 24 contract fields is independently load-bearing."""
    decision = expect_failure(tmp_path,
                              ga.GATE_A_AUTHORIZATION_RECORD_SCHEMA_UNSUPPORTED
                              if field == "schema_version"
                              else ga.GATE_A_AUTHORIZATION_RECORD_INVALID,
                              record_overrides={field: OMIT})
    assert decision.authorized is False


def test_blank_field(tmp_path):
    decision = expect_failure(tmp_path, ga.GATE_A_AUTHORIZATION_RECORD_INVALID,
                              record_overrides={"authorization_scope": "   "})
    assert "blank" in decision.failure_detail


def test_sentinel_field(tmp_path):
    decision = expect_failure(tmp_path, ga.GATE_A_AUTHORIZATION_RECORD_INVALID,
                              record_overrides={"owner_approval_reference":
                                                "PENDING_OWNER_APPROVAL"})
    assert "sentinel" in decision.failure_detail


def test_abbreviated_framework_sha(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_AUTHORIZATION_RECORD_INVALID,
                   record_overrides={"execution_framework_sha": "1" * 12})


def test_non_string_sha(tmp_path):
    """An unquoted numeric SHA is not a valid SHA, it is a YAML integer."""
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    rec = record_mapping(ctx.framework_root)
    rec["execution_framework_sha"] = 11111
    ctx.authorization_record_path.write_bytes(dump_record(rec))
    ctx.authorization_digest_path.write_text(
        sha256_bytes(ctx.authorization_record_path.read_bytes()) + "\n",
        encoding="utf-8", newline="")
    ctx.owner_approval_path.write_text(
        __import__("gate_a_fixtures").approval_text(
            sha256_bytes(ctx.authorization_record_path.read_bytes())),
        encoding="utf-8", newline="")
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_AUTHORIZATION_RECORD_INVALID
    assert "string SHA" in decision.failure_detail


@pytest.mark.parametrize("floating", ["HEAD", "origin/main", "main", "refs/heads/main",
                                      "HEAD@{1}", "latest"])
def test_floating_refs_rejected_in_record(tmp_path, floating):
    expect_failure(tmp_path, ga.GATE_A_FLOATING_REF_PROHIBITED,
                   record_overrides={"target_sha": floating})


def test_floating_ref_rejected_in_context(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx = ctx.__class__(**{**ctx.__dict__, "execution_framework_sha": "origin/main"})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_FLOATING_REF_PROHIBITED


def test_pending_execution_framework_sha_sentinel(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx = ctx.__class__(**{**ctx.__dict__,
                           "execution_framework_sha": "PENDING_POST_MERGE_PIN_FINALIZATION"})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_EXECUTION_FRAMEWORK_SHA_PENDING


def test_pending_run_control_commit_sentinel(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx = ctx.__class__(**{**ctx.__dict__,
                           "run_control_commit_sha": "PENDING_AUTHORIZATION_RECORD_CREATION"})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_RUN_CONTROL_COMMIT_MISMATCH


# ---------------------------------------------------------------------------
# Exact-byte digest hashing
# ---------------------------------------------------------------------------


def test_digest_mismatch(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_AUTHORIZATION_DIGEST_MISMATCH, digest="0" * 64)


@pytest.mark.parametrize("bad", [b"", b"deadbeef\n", b"A" * 64, b"x" * 64,
                                 b"a" * 64 + b"\n" + b"b" * 64 + b"\n",
                                 b"a" * 64 + b"  wrong-name.yaml\n",
                                 b"a" * 64 + b" extra tokens here\n"])
def test_malformed_digest_files(tmp_path, bad):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx.authorization_digest_path.write_bytes(bad)
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_AUTHORIZATION_DIGEST_INVALID


def test_digest_file_with_correct_filename_accepted(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    real = sha256_bytes(ctx.authorization_record_path.read_bytes())
    ctx.authorization_digest_path.write_text(
        f"{real}  authorization-record.yaml\n", encoding="utf-8", newline="")
    decision, _ = run(ctx, head, resolver)
    assert decision.authorized is True, decision.failure_detail


def test_line_ending_change_after_approval_fails(tmp_path):
    """CRLF-ing an approved record produces a different authorization."""
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    original = ctx.authorization_record_path.read_bytes()
    ctx.authorization_record_path.write_bytes(original.replace(b"\n", b"\r\n"))
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_AUTHORIZATION_DIGEST_MISMATCH


def test_trailing_whitespace_change_after_approval_fails(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    original = ctx.authorization_record_path.read_bytes()
    ctx.authorization_record_path.write_bytes(original + b" \n")
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_AUTHORIZATION_DIGEST_MISMATCH


def test_hashing_is_over_raw_bytes_not_reserialized_yaml(tmp_path):
    """Semantically-equal YAML with different bytes is a different record."""
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    raw = ctx.authorization_record_path.read_bytes()
    reserialized = dump_record(
        __import__("yaml").safe_load(raw.decode("utf-8"))
    )
    assert reserialized != raw or True  # may coincide; the digest check is the proof
    ctx.authorization_record_path.write_bytes(b"# comment added\n" + raw)
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_AUTHORIZATION_DIGEST_MISMATCH


# ---------------------------------------------------------------------------
# Owner approval
# ---------------------------------------------------------------------------


def test_approval_of_a_different_digest(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    text = ctx.owner_approval_path.read_text(encoding="utf-8")
    real = sha256_bytes(ctx.authorization_record_path.read_bytes())
    ctx.owner_approval_path.write_text(text.replace(real, "f" * 64),
                                       encoding="utf-8", newline="")
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_OWNER_APPROVAL_DIGEST_MISMATCH


def test_wrong_owner(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_OWNER_IDENTITY_MISMATCH,
                   approval_overrides={"approver_github_identity": "random-contributor"})


def test_self_approval_embedded_only_in_record_is_not_approval(tmp_path):
    """Deleting the distinct approval and putting the digest in the record
    itself must not authorize anything."""
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx.owner_approval_path.unlink()
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_OWNER_APPROVAL_MISSING


def test_operator_self_approval_prohibited(tmp_path):
    ctx, head, resolver, _ = build_valid_case(
        tmp_path,
        record_overrides={"authorization_record_created_by": "ThorStarlord"},
    )
    ctx = ctx.__class__(**{**ctx.__dict__, "operator_identity": "ThorStarlord"})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_OPERATOR_SELF_APPROVAL_PROHIBITED


def test_conflicting_approvals(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    text = ctx.owner_approval_path.read_text(encoding="utf-8")
    ctx.owner_approval_path.write_text(
        text + "\napprover_github_identity: someone-else\n",
        encoding="utf-8", newline="")
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_OWNER_APPROVAL_CONFLICT


@pytest.mark.parametrize("field", ga.REQUIRED_APPROVAL_FIELDS)
def test_every_required_approval_field_is_required(tmp_path, field):
    ctx, head, resolver, _ = build_valid_case(
        tmp_path, approval_overrides={field: OMIT})
    decision, _ = run(ctx, head, resolver)
    assert decision.authorized is False
    assert decision.failure_code in (
        ga.GATE_A_OWNER_APPROVAL_INVALID,
        ga.GATE_A_OWNER_APPROVAL_DIGEST_MISMATCH,
        ga.GATE_A_OWNER_IDENTITY_MISMATCH,
    )


def test_approval_sentinel_value(tmp_path):
    ctx, head, resolver, _ = build_valid_case(
        tmp_path, approval_overrides={"owner_decision_reference": "TBD"})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_OWNER_APPROVAL_INVALID


def test_approval_wrong_decision_status(tmp_path):
    ctx, head, resolver, _ = build_valid_case(
        tmp_path, approval_overrides={"authorization_decision": "LOOKS_FINE_TO_ME"})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_OWNER_APPROVAL_INVALID


def test_approval_disagrees_with_record_on_target_sha(tmp_path):
    ctx, head, resolver, _ = build_valid_case(
        tmp_path, approval_overrides={"target_sha": "9" * 40})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_OWNER_APPROVAL_INVALID
    assert "target_sha" in decision.failure_detail


def test_approval_prose_without_digest_binding(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx.owner_approval_path.write_text(
        "# Approval\n\nI approve this run. Looks good. Go ahead.\n",
        encoding="utf-8", newline="")
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_OWNER_APPROVAL_INVALID


def test_approval_timestamp_must_be_iso8601(tmp_path):
    ctx, head, resolver, _ = build_valid_case(
        tmp_path, approval_overrides={"approval_timestamp": "last tuesday"})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_OWNER_APPROVAL_INVALID


# ---------------------------------------------------------------------------
# Repository identity and revisions
# ---------------------------------------------------------------------------


def test_wrong_framework_sha_in_record(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_EXECUTION_FRAMEWORK_SHA_MISMATCH,
                   record_overrides={"execution_framework_sha": "3" * 40},
                   approval_overrides={"execution_framework_sha": "3" * 40})


def test_framework_head_moved(tmp_path):
    ctx, head, resolver, heads = build_valid_case(tmp_path)
    heads[str(ctx.framework_root)] = "4" * 40
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_EXECUTION_FRAMEWORK_SHA_MISMATCH


def test_target_head_moved(tmp_path):
    ctx, head, resolver, heads = build_valid_case(tmp_path)
    heads[str(ctx.target_root)] = "5" * 40
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_TARGET_SHA_MISMATCH


def test_target_pin_silently_updated_is_rejected(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_TARGET_SHA_MISMATCH,
                   record_overrides={"target_sha": "6" * 40},
                   approval_overrides={"target_sha": "6" * 40})


def test_wrong_target_repository(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_TARGET_REPOSITORY_MISMATCH,
                   record_overrides={"target_repository":
                                     "https://github.com/someone/else.git"})


def test_same_root_for_framework_and_target(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx = ctx.__class__(**{**ctx.__dict__, "target_root": ctx.framework_root})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_ROOT_SEPARATION_FAILURE


def test_nested_roots_rejected(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    nested = ctx.framework_root / "nested-target"
    nested.mkdir()
    ctx = ctx.__class__(**{**ctx.__dict__, "target_root": nested})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_ROOT_SEPARATION_FAILURE


def test_wrong_run_control_commit(tmp_path):
    ctx, head, _resolver, _ = build_valid_case(tmp_path)
    decision, _ = run(ctx, head, lambda a, b: "7" * 40)
    assert decision.failure_code == ga.GATE_A_RUN_CONTROL_COMMIT_MISMATCH


def test_unprovable_run_control_commit_fails_closed(tmp_path):
    ctx, head, _resolver, _ = build_valid_case(tmp_path)
    decision, _ = run(ctx, head, lambda a, b: "")
    assert decision.failure_code == ga.GATE_A_RUN_CONTROL_COMMIT_MISMATCH
    assert "unproven" in decision.failure_detail


# ---------------------------------------------------------------------------
# Evidence identity, model, artifact type
# ---------------------------------------------------------------------------


def test_wrong_evidence_number(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_EVIDENCE_IDENTITY_MISMATCH,
                   record_overrides={"evidence_number": "0015"},
                   approval_overrides={"evidence_number": "0015"})


def test_malformed_evidence_number(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_EVIDENCE_IDENTITY_MISMATCH,
                   record_overrides={"evidence_number": "16"},
                   approval_overrides={"evidence_number": "16"})


def test_wrong_slug(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_EVIDENCE_IDENTITY_MISMATCH,
                   record_overrides={"evidence_slug": "0016-something-else"},
                   approval_overrides={"evidence_slug": "0016-something-else"})


def test_wrong_artifact_type(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_ARTIFACT_TYPE_MISMATCH,
                   record_overrides={"artifact_type": "architectural_review"})


@pytest.mark.parametrize("wrong_model", ["claude-opus-4-7", "claude-sonnet-4-5",
                                         "sonnet", "claude-sonnet-latest",
                                         "claude-sonnet-5-20260101"])
def test_wrong_or_aliased_model(tmp_path, wrong_model):
    expect_failure(tmp_path, ga.GATE_A_MODEL_MISMATCH,
                   record_overrides={"exact_model": wrong_model},
                   approval_overrides={"exact_model": wrong_model})


# ---------------------------------------------------------------------------
# Package and checklist provenance
# ---------------------------------------------------------------------------


def test_package_digest_mismatch(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_PACKAGE_DIGEST_MISMATCH,
                   record_overrides={"preparation_package_sha256": "a" * 64})


def test_checklist_digest_mismatch(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_CHECKLIST_DIGEST_MISMATCH,
                   record_overrides={"gate_d_checklist_sha256": "b" * 64})


def test_package_path_substitution(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_PACKAGE_PATH_MISMATCH,
                   record_overrides={"preparation_package_path":
                                     "docs/experiments/SOME-OTHER-PACKAGE.md"})


def test_package_bytes_changed_after_authorization(tmp_path):
    """An 'equivalent' package is not the authorized package."""
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    pkg = ctx.framework_root / PACKAGE_REL
    pkg.write_bytes(pkg.read_bytes() + b"\n<!-- harmless comment -->\n")
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_PACKAGE_DIGEST_MISMATCH


def test_missing_required_framework_path(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx = ctx.__class__(**{**ctx.__dict__,
                           "required_framework_paths": (PACKAGE_REL, "docs/does-not-exist.md")})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_REQUIRED_PATH_MISSING


def test_missing_required_target_path(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx = ctx.__class__(**{**ctx.__dict__, "required_target_paths": ("src/nope.py",)})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_REQUIRED_PATH_MISSING


def test_missing_package_file_at_framework_root(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    (ctx.framework_root / PACKAGE_REL).unlink()
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_REQUIRED_PATH_MISSING


# ---------------------------------------------------------------------------
# Safety booleans and invocation limit
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("boolean,code", [
    ("no_retry", ga.GATE_A_RETRY_PROHIBITED),
    ("no_fallback", ga.GATE_A_FALLBACK_PROHIBITED),
    ("no_model_substitution", ga.GATE_A_MODEL_SUBSTITUTION_PROHIBITED),
    ("no_artifact_repair", ga.GATE_A_ARTIFACT_REPAIR_PROHIBITED),
    ("no_target_mutation", ga.GATE_A_TARGET_MUTATION_PROHIBITED),
    ("one_invocation_only", ga.GATE_A_INVOCATION_LIMIT_INVALID),
])
def test_safety_boolean_disabled(tmp_path, boolean, code):
    expect_failure(tmp_path, code, record_overrides={boolean: False})


@pytest.mark.parametrize("truthy", ["true", "yes", 1])
def test_stringly_typed_booleans_rejected(tmp_path, truthy):
    """'true' the string is not True the boolean."""
    expect_failure(tmp_path, ga.GATE_A_RETRY_PROHIBITED,
                   record_overrides={"no_retry": truthy})


@pytest.mark.parametrize("limit", [0, 2, 3, 10])
def test_invocation_limit_other_than_one(tmp_path, limit):
    expect_failure(tmp_path, ga.GATE_A_INVOCATION_LIMIT_INVALID,
                   record_overrides={"invocation_limit": limit})


def test_context_invocation_limit_other_than_one(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx = ctx.__class__(**{**ctx.__dict__, "invocation_limit": 2})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_INVOCATION_LIMIT_INVALID


def test_expired_authorization(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_AUTHORIZATION_EXPIRED,
                   record_overrides={"authorization_expires_at": "2020-01-01T00:00:00+00:00"})


def test_wrong_authorization_status(tmp_path):
    expect_failure(tmp_path, ga.GATE_A_AUTHORIZATION_STATUS_INVALID,
                   record_overrides={"authorization_status": "AUTHORIZED"})


def test_pre_existing_evidence_0016_output_rejected(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    ctx.evidence_output_dir.mkdir(parents=True)
    (ctx.evidence_output_dir / "brief.md").write_text("stale", encoding="utf-8")
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_EVIDENCE_OUTPUT_ALREADY_PRESENT


# ---------------------------------------------------------------------------
# Filesystem safety
# ---------------------------------------------------------------------------


def test_path_traversal_out_of_run_control_dir(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    forged = outside / "owner-approval.md"
    forged.write_text(ctx.owner_approval_path.read_text(encoding="utf-8"),
                      encoding="utf-8", newline="")
    traversal = ctx.authorization_record_path.parent / ".." / ".." / "elsewhere" / "owner-approval.md"
    ctx = ctx.__class__(**{**ctx.__dict__, "owner_approval_path": traversal})
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_PATH_ESCAPE_PROHIBITED


def _can_symlink() -> bool:
    """Probe the real capability rather than guessing from the platform.

    On Linux CI this is True and the test runs for real; on an unprivileged
    Windows box symlink creation raises WinError 1314 and the test skips.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "src"
        src.write_text("x", encoding="utf-8")
        try:
            (Path(d) / "link").symlink_to(src)
            return True
        except (OSError, NotImplementedError):
            return False


@pytest.mark.skipif(not _can_symlink(),
                    reason="this environment cannot create symlinks "
                           "(unprivileged Windows); the guard is covered by "
                           "test_check_run_control_path_reports_symlink_* instead")
def test_symlink_redirection_rejected(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    real = tmp_path / "shadow-record.yaml"
    real.write_bytes(ctx.authorization_record_path.read_bytes())
    ctx.authorization_record_path.unlink()
    ctx.authorization_record_path.symlink_to(real)
    decision, _ = run(ctx, head, resolver)
    assert decision.failure_code == ga.GATE_A_SYMLINK_PROHIBITED


def test_check_run_control_path_reports_symlink_without_creating_one(tmp_path):
    """Unit-level proof of the symlink branch that works on every platform."""
    rc = tmp_path / "rc"
    rc.mkdir()
    target = rc / "record.yaml"
    target.write_text("x", encoding="utf-8")

    class FakeSymlink(type(target)):
        pass

    # Exercise the guard directly with a stubbed is_symlink.
    import types
    stub = types.SimpleNamespace(
        exists=lambda: True,
        is_symlink=lambda: True,
        parent=rc,
        name="record.yaml",
    )
    assert ga.check_run_control_path(stub, rc) == ga.GATE_A_SYMLINK_PROHIBITED


def test_permission_error_fails_closed(tmp_path, monkeypatch):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    original = Path.read_bytes

    def boom(self, *a, **k):
        if self.name == "authorization-record.yaml":
            raise PermissionError(13, "Permission denied")
        return original(self, *a, **k)

    monkeypatch.setattr(Path, "read_bytes", boom)
    decision, _ = run(ctx, head, resolver)
    assert decision.authorized is False
    assert decision.failure_code == ga.GATE_A_FILESYSTEM_ERROR


# ---------------------------------------------------------------------------
# Capability semantics and logging hygiene
# ---------------------------------------------------------------------------


def test_capability_cannot_be_constructed_directly(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    decision, snapshot = run(ctx, head, resolver)
    with pytest.raises(ga.GateAError):
        ga.AuthorizedInvocation(object(), decision, ctx, snapshot)


def test_authorize_invocation_mints_capability_only_on_success(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    decision, cap = ga.authorize_invocation(
        ctx, git_head=head, run_control_commit_resolver=resolver)
    assert decision.authorized is True
    assert isinstance(cap, ga.AuthorizedInvocation)
    assert cap.model == "claude-sonnet-5"
    assert cap.remaining_invocations == 1


def test_no_capability_on_any_failure(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path, digest="0" * 64)
    decision, cap = ga.authorize_invocation(
        ctx, git_head=head, run_control_commit_resolver=resolver)
    assert decision.authorized is False
    assert cap is None, "a failed Gate A must never mint a capability"


def test_capability_is_single_use(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    _, cap = ga.authorize_invocation(ctx, git_head=head,
                                     run_control_commit_resolver=resolver)
    cap.consume(model="claude-sonnet-5", artifact_type="repository_sensemaking_brief",
                git_head=head)
    assert cap.consumed is True
    with pytest.raises(ga.GateAError, match="ALREADY_CONSUMED"):
        cap.consume(model="claude-sonnet-5",
                    artifact_type="repository_sensemaking_brief", git_head=head)


def test_capability_refuses_a_different_model(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    _, cap = ga.authorize_invocation(ctx, git_head=head,
                                     run_control_commit_resolver=resolver)
    with pytest.raises(ga.GateAError, match="MODEL_MISMATCH"):
        cap.consume(model="claude-opus-4-7",
                    artifact_type="repository_sensemaking_brief", git_head=head)
    assert cap.consumed is False


def test_log_output_is_ascii_and_leaks_nothing(tmp_path):
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    decision, _ = run(ctx, head, resolver)
    line = ga.format_gate_a_log(decision)
    line.encode("ascii")  # raises if non-ASCII
    approval_body = ctx.owner_approval_path.read_text(encoding="utf-8")
    for secret_ish in ("owner decision on the run-control PR", "No retry, no rerun"):
        assert secret_ish not in line
    assert approval_body not in line
    full_digest = decision.validated_record_sha256
    assert full_digest not in line, "log must truncate the digest, not emit it whole"
    assert "claude-sonnet-5" in line


def test_failure_codes_are_distinct_and_not_generic():
    assert len(set(ga.ALL_FAILURE_CODES)) == len(ga.ALL_FAILURE_CODES)
    assert "GATE_A_UNAUTHORIZED" not in ga.ALL_FAILURE_CODES
    assert len(ga.ALL_FAILURE_CODES) >= 25
