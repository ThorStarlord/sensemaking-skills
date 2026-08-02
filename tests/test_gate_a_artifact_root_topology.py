"""Tests for the artifact-root Gate A topology.

Provenance contract under test: ``artifact_snapshot_sha`` (carried in
``AuthorizationContext.run_control_commit_sha`` when ``artifact_root`` is set)
means the exact commit from which every runtime authorization artifact
(record, digest, approval) is read. ``artifact_root`` must be checked out
exactly at that commit's HEAD, all three artifact paths must be physically
contained within it, and the bytes on disk must exactly match the git object
bytes at that revision. ``framework_root`` and ``target_root`` remain
independently pinned and verified exactly as before -- this topology only
changes how run-control-artifact provenance is proven, not how the framework
or target revisions are checked.

These tests build REAL git repositories (unlike the synthetic-callable
fixtures in ``gate_a_fixtures.py``), because the entire point of this
topology is exercising the real ``git rev-parse`` / ``git cat-file`` /
``git show`` provenance chain, not an injected fake.

Nothing here writes to the real repository. Every repo is a throwaway git
init inside ``tmp_path``. No model or provider is invoked.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gate_a_authorization as ga  # noqa: E402
from gate_a_fixtures import (  # noqa: E402
    ARTIFACT_TYPE,
    EVIDENCE_NUMBER,
    EVIDENCE_SLUG,
    EXACT_MODEL,
    FRAMEWORK_SHA,
    TARGET_SHA,
    approval_text,
    dump_record,
    make_framework_root,
    make_target_root,
    record_mapping,
    sha256_bytes,
)


def _git(*args, cwd):
    out = subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, check=False,
    )
    assert out.returncode == 0, f"git {args} failed: {out.stderr}"
    return out.stdout.strip()


def _init_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    _git("init", "-q", cwd=root)
    _git("config", "user.email", "test@example.invalid", cwd=root)
    _git("config", "user.name", "Test", cwd=root)


def make_artifact_root(tmp_path: Path, framework_root: Path, *,
                       record_overrides=None, approval_overrides=None,
                       digest=None) -> tuple[Path, str, dict]:
    """A real git repo containing the three committed run-control artifacts.

    Returns (artifact_root, commit_sha, paths) where paths maps
    'record'/'digest'/'approval' to their absolute Path inside the repo.
    """
    root = tmp_path / "artifact-root"
    _init_repo(root)

    record = record_mapping(framework_root, **(record_overrides or {}))
    raw = dump_record(record)
    approval = approval_text(sha256_bytes(raw), **(approval_overrides or {}))
    digest_text = (digest if digest is not None else sha256_bytes(raw)) + "\n"

    rc = root / "run-control" / EVIDENCE_SLUG
    rc.mkdir(parents=True)
    record_path = rc / "authorization-record.yaml"
    digest_path = rc / "authorization-record.sha256"
    approval_path = rc / "owner-approval.md"
    record_path.write_bytes(raw)
    digest_path.write_text(digest_text, encoding="utf-8", newline="")
    approval_path.write_text(approval, encoding="utf-8", newline="")

    _git("add", "-A", cwd=root)
    _git("commit", "-q", "-m", "artifact snapshot", cwd=root)
    sha = _git("rev-parse", "HEAD", cwd=root)

    return root, sha, {
        "record": record_path, "digest": digest_path, "approval": approval_path,
    }


def build_artifact_root_case(tmp_path: Path, **kwargs):
    """Full valid case using the new artifact_root topology."""
    framework_root = make_framework_root(tmp_path)
    target_root = make_target_root(tmp_path)
    artifact_root, snapshot_sha, paths = make_artifact_root(
        tmp_path, framework_root, **kwargs
    )

    context = ga.AuthorizationContext(
        framework_root=framework_root,
        target_root=target_root,
        artifact_root=artifact_root,
        execution_framework_sha=FRAMEWORK_SHA,
        target_sha=TARGET_SHA,
        evidence_number=EVIDENCE_NUMBER,
        evidence_slug=EVIDENCE_SLUG,
        exact_model=EXACT_MODEL,
        artifact_type=ARTIFACT_TYPE,
        invocation_limit=1,
        authorization_record_path=paths["record"],
        authorization_digest_path=paths["digest"],
        owner_approval_path=paths["approval"],
        run_control_commit_sha=snapshot_sha,
        operator_identity="operator-not-the-owner",
        evidence_output_dir=tmp_path / "evidence-0016",
    )

    heads = {str(framework_root): FRAMEWORK_SHA, str(target_root): TARGET_SHA,
             str(artifact_root): snapshot_sha}

    def git_head(root: Path) -> str:
        return heads.get(str(root), ga.read_git_head(root))

    return context, git_head, artifact_root, snapshot_sha, paths


# ---------------------------------------------------------------------------
# Positive case
# ---------------------------------------------------------------------------


def test_pinned_framework_plus_separate_artifact_checkout_succeeds(tmp_path):
    context, git_head, *_ = build_artifact_root_case(tmp_path)
    decision, snapshot = ga.authorize(context, git_head=git_head)
    assert decision.authorized is True, decision.failure_detail
    assert snapshot is not None
    assert "artifact_root_head_matches_pin" in decision.checks_passed
    assert "artifact_snapshot_bytes_verified" in decision.checks_passed


def test_consumer_never_mutates_artifact_root_inputs(tmp_path):
    context, git_head, artifact_root, snapshot_sha, paths = build_artifact_root_case(tmp_path)
    before = {p: p.read_bytes() for p in paths.values()}
    ga.authorize(context, git_head=git_head)
    for p, content in before.items():
        assert p.read_bytes() == content
    assert ga.read_git_head(artifact_root) == snapshot_sha, "authorize() must not commit"


def test_no_evidence_output_created(tmp_path):
    context, git_head, *_ = build_artifact_root_case(tmp_path)
    ga.authorize(context, git_head=git_head)
    assert not context.evidence_output_dir.exists()


# ---------------------------------------------------------------------------
# Framework / target revisions still independently enforced
# ---------------------------------------------------------------------------


def test_framework_head_mismatch_still_fails(tmp_path):
    context, git_head, *_ = build_artifact_root_case(tmp_path)
    wrong_head = {**{k: v for k, v in
                      {str(context.framework_root): "9" * 40}.items()}}

    def bad_git_head(root: Path) -> str:
        if str(root) == str(context.framework_root):
            return "9" * 40
        return git_head(root)

    decision, snapshot = ga.authorize(context, git_head=bad_git_head)
    assert decision.authorized is False
    assert decision.failure_code == ga.GATE_A_EXECUTION_FRAMEWORK_SHA_MISMATCH
    assert snapshot is None


def test_target_head_mismatch_still_fails(tmp_path):
    context, git_head, *_ = build_artifact_root_case(tmp_path)

    def bad_git_head(root: Path) -> str:
        if str(root) == str(context.target_root):
            return "9" * 40
        return git_head(root)

    decision, snapshot = ga.authorize(context, git_head=bad_git_head)
    assert decision.authorized is False
    assert decision.failure_code == ga.GATE_A_TARGET_SHA_MISMATCH
    assert snapshot is None


# ---------------------------------------------------------------------------
# Artifact-root containment
# ---------------------------------------------------------------------------


def test_artifact_path_outside_artifact_root_fails(tmp_path):
    context, git_head, *_ = build_artifact_root_case(tmp_path)
    outside = tmp_path / "outside-approval.md"
    outside.write_text(context.owner_approval_path.read_text(encoding="utf-8"),
                       encoding="utf-8")
    import dataclasses
    context = dataclasses.replace(context, owner_approval_path=outside)
    decision, snapshot = ga.authorize(context, git_head=git_head)
    assert decision.authorized is False
    assert decision.failure_code == ga.GATE_A_PATH_ESCAPE_PROHIBITED
    assert snapshot is None


@pytest.mark.skipif(sys.platform != "win32", reason="symlink privilege behavior is platform-specific")
def test_symlink_escape_fails(tmp_path):
    context, git_head, artifact_root, snapshot_sha, paths = build_artifact_root_case(tmp_path)
    link = artifact_root / "run-control" / EVIDENCE_SLUG / "owner-approval-link.md"
    try:
        link.symlink_to(paths["approval"])
    except OSError:
        pytest.skip("no symlink privilege available in this environment")
    import dataclasses
    context = dataclasses.replace(context, owner_approval_path=link)
    decision, snapshot = ga.authorize(context, git_head=git_head)
    assert decision.authorized is False
    assert decision.failure_code == ga.GATE_A_SYMLINK_PROHIBITED
    assert snapshot is None


# ---------------------------------------------------------------------------
# Artifact-root revision and byte provenance
# ---------------------------------------------------------------------------


def test_artifact_root_head_mismatch_fails(tmp_path):
    context, git_head, artifact_root, snapshot_sha, paths = build_artifact_root_case(tmp_path)
    # Advance artifact_root's real HEAD past the pinned snapshot.
    (artifact_root / "unrelated.txt").write_text("noise\n", encoding="utf-8")
    _git("add", "-A", cwd=artifact_root)
    _git("commit", "-q", "-m", "unrelated change", cwd=artifact_root)

    def real_artifact_head(root: Path) -> str:
        if str(root) == str(artifact_root):
            return ga.read_git_head(root)  # the real, now-advanced HEAD
        return git_head(root)

    decision, snapshot = ga.authorize(context, git_head=real_artifact_head)
    assert decision.authorized is False
    assert decision.failure_code == ga.GATE_A_ARTIFACT_ROOT_HEAD_MISMATCH
    assert snapshot is None


def test_dirty_artifact_bytes_fail(tmp_path):
    context, git_head, artifact_root, snapshot_sha, paths = build_artifact_root_case(tmp_path)
    # Modify the approval file on disk without committing -- HEAD is unchanged,
    # but the bytes Gate A would read no longer match the pinned revision.
    paths["approval"].write_text(
        paths["approval"].read_text(encoding="utf-8") + "\ntampered: true\n",
        encoding="utf-8",
    )
    decision, snapshot = ga.authorize(context, git_head=git_head)
    assert decision.authorized is False
    assert decision.failure_code == ga.GATE_A_ARTIFACT_SNAPSHOT_BYTES_MISMATCH
    assert snapshot is None


def test_untracked_replacement_fails(tmp_path):
    context, git_head, artifact_root, snapshot_sha, paths = build_artifact_root_case(tmp_path)
    import dataclasses
    untracked = artifact_root / "run-control" / EVIDENCE_SLUG / "untracked-approval.md"
    untracked.write_text(paths["approval"].read_text(encoding="utf-8"), encoding="utf-8")
    # Never `git add`/committed -- absent from the pinned revision's tree.
    context = dataclasses.replace(context, owner_approval_path=untracked)
    decision, snapshot = ga.authorize(context, git_head=git_head)
    assert decision.authorized is False
    assert decision.failure_code == ga.GATE_A_ARTIFACT_SNAPSHOT_BYTES_MISMATCH
    assert snapshot is None


def test_cross_drive_topology_does_not_use_relpath_between_roots(tmp_path, monkeypatch):
    """framework_root and artifact_root must never be relpath'd against each
    other -- only paths *within* artifact_root are relpath'd, against
    artifact_root itself. Proven by making relpath raise for any other pair.
    """
    import os as _os
    real_relpath = _os.path.relpath

    def guarded_relpath(path, start=None):
        if start is not None and "artifact-root" not in str(start):
            # framework_root/target_root must never be the `start` of a
            # relpath call in this code path.
            raise AssertionError(
                f"unexpected relpath(start={start!r}); framework/target roots "
                "must not be relpath'd"
            )
        return real_relpath(path, start) if start is not None else real_relpath(path)

    context, git_head, *_ = build_artifact_root_case(tmp_path)
    monkeypatch.setattr(ga.os.path, "relpath", guarded_relpath)
    decision, snapshot = ga.authorize(context, git_head=git_head)
    assert decision.authorized is True, decision.failure_detail


# ---------------------------------------------------------------------------
# Backward compatibility: existing single-root behavior is untouched
# ---------------------------------------------------------------------------


def test_existing_single_root_fixture_still_authorizes(tmp_path):
    from gate_a_fixtures import build_valid_case
    ctx, head, resolver, _ = build_valid_case(tmp_path)
    assert ctx.artifact_root is None
    decision, snapshot = ga.authorize(ctx, git_head=head, run_control_commit_resolver=resolver)
    assert decision.authorized is True, decision.failure_detail
    assert snapshot is not None
