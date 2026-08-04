"""Production signed-commit verifier tests (Issue #122).

Every stage fails closed with ``ProvenanceVerificationError``; the success
path is only reachable when the reference commit exists, is an ancestor of
the verification repo HEAD, and carries a valid Git signature (simulated
here by stubbing the signature stage -- tests cannot fabricate a real
GPG/SSH signature, and the verifier never accepts one that does not exist).
"""

import subprocess
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from execution_infra.production_verifier import ProductionSignedCommitVerifier
from sensemaking_skills.exploratory_authorization.models import VerifiedApprovalProvenance
from sensemaking_skills.exploratory_authorization.provenance import (
    ProvenanceVerificationError,
)


def _make_approval(reference: str, mechanism: str = "signed_commit"):
    class _Approval:
        raw = {"approval_provenance": {"mechanism": mechanism, "reference": reference}}
    return _Approval()


@pytest.fixture()
def git_repo(tmp_path: Path):
    """A real git repository with one unsigned commit."""
    repo = tmp_path / "verification-repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "config", "user.email", "probe@example.invalid"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(repo), "config", "user.name", "Probe"],
        check=True,
    )
    (repo / "file.txt").write_text("content", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "file.txt"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-q", "-m", "unsigned probe commit"],
        check=True,
    )
    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return repo, head


def test_mechanism_mismatch_fails_closed(git_repo) -> None:
    repo, head = git_repo
    verifier = ProductionSignedCommitVerifier(repo)
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(_make_approval(head, mechanism="web_commit"))
    assert "mechanism" in str(exc.value)


def test_malformed_reference_fails_closed(git_repo) -> None:
    repo, _ = git_repo
    verifier = ProductionSignedCommitVerifier(repo)
    for bad in ("", "abc", "deadbeef", "ABCDEF0123456789abcdef0123456789abcdef01",
                "0" * 41):
        with pytest.raises(ProvenanceVerificationError) as exc:
            verifier.verify(_make_approval(bad))
        assert "not a 40-character lowercase hex commit SHA" in str(exc.value)


def test_missing_commit_fails_closed(git_repo) -> None:
    repo, _ = git_repo
    verifier = ProductionSignedCommitVerifier(repo)
    ghost = "0" * 40
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(_make_approval(ghost))
    assert "not a commit in the verification repository" in str(exc.value)


def test_non_ancestor_commit_fails_closed(git_repo) -> None:
    """A commit that exists but is not reachable from HEAD is rejected."""
    repo, head = git_repo
    # Create a second branch commit and move HEAD back: the first commit is
    # no longer an ancestor of HEAD.
    subprocess.run(
        ["git", "-C", str(repo), "checkout", "-q", "-b", "side", head], check=True)
    (repo / "side.txt").write_text("side", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "side.txt"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-q", "-m", "side commit"], check=True)
    side = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    subprocess.run(["git", "-C", str(repo), "checkout", "-q", head], check=True)

    verifier = ProductionSignedCommitVerifier(repo)
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(_make_approval(side))
    assert "not an ancestor" in str(exc.value)


def test_unsigned_commit_fails_closed(git_repo) -> None:
    """A real unsigned commit exists and is reachable but has no signature."""
    repo, head = git_repo
    verifier = ProductionSignedCommitVerifier(repo)
    assert verifier._commit_exists(head)
    assert verifier._is_ancestor_of_head(head)
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(_make_approval(head))
    assert "does not carry a verifiable Git signature" in str(exc.value)


def test_signature_stage_rejects_failed_verify(git_repo, monkeypatch) -> None:
    repo, head = git_repo
    verifier = ProductionSignedCommitVerifier(repo)
    monkeypatch.setattr(verifier, "_signature_verifies", lambda ref: False)
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(_make_approval(head))
    assert "does not carry a verifiable Git signature" in str(exc.value)


def test_full_corroboration_returns_exact_provenance(git_repo, monkeypatch) -> None:
    """All stages pass (signature stage simulated): the verifier returns the
    EXACT mechanism and reference from the approval document."""
    repo, head = git_repo
    verifier = ProductionSignedCommitVerifier(repo)
    monkeypatch.setattr(verifier, "_signature_verifies", lambda ref: ref == head)

    result = verifier.verify(_make_approval(head))
    assert isinstance(result, VerifiedApprovalProvenance)
    assert result.mechanism == "signed_commit"
    assert result.reference == head


def test_git_unavailable_fails_closed(tmp_path, monkeypatch) -> None:
    """A missing git binary or broken repo never yields consent."""
    verifier = ProductionSignedCommitVerifier(tmp_path)
    monkeypatch.setattr(
        verifier, "_run",
        lambda args: subprocess.CompletedProcess(args, 127, "", "git: not found"),
    )
    with pytest.raises(ProvenanceVerificationError):
        verifier.verify(_make_approval("0" * 40))
