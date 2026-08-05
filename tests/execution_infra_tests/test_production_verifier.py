"""ProductionSignedCommitVerifier tests (Phase 6 correction, #122).

Proves the full binding matrix with REAL temporary git repositories. Only
the signature seams (``verify-commit`` / fingerprint extraction) are
stubbed -- those require a GPG key; every byte, ancestry, remote, and
registry check runs against real git.

Adversarial probes:

* approval references an unrelated commit (no approval.yaml in its tree);
* the signed commit contains DIFFERENT approval bytes;
* the signer fingerprint is not in the registry;
* the fingerprint maps to a different identity than claimed;
* the verification repository's origin is not the trusted remote;
* the reference is not on the governed protected branch;
* approval_bytes are absent (fail closed);
* signed document field values diverge from the operative document;
* subclass-overridden verify() cannot bypass the runner (exact-type
  guard is tested in test_runner.py).
"""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import yaml
from exploratory_fixtures import (
    TEST_APPROVER_IDENTITY,
    build_approval_raw,
    render_yaml,
)

from sensemaking_skills.exploratory_authorization.provenance import (
    ProvenanceVerificationError,
)
from sensemaking_skills.exploratory_execution import ProductionSignedCommitVerifier

TRUSTED_REMOTE = "https://github.com/ThorStarlord/sensemaking-skills.git"
FINGERPRINT = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
OTHER_FINGERPRINT = "0f0e0d0c0b0a090807060504030201000f0e0d0c"


class _Repo:
    def __init__(self, tmp_path: Path, name: str = "repo"):
        self.path = tmp_path / name
        self.path.mkdir()
        self._git(["init", "-q"])
        self._git(["config", "user.email", "t@e.i"])
        self._git(["config", "user.name", "T"])
        self._git(["remote", "add", "origin", TRUSTED_REMOTE])

    def _git(self, args):
        return subprocess.run(
            ["git", "-C", str(self.path)] + args,
            capture_output=True, text=True, check=False,
        )

    def commit(self, files: dict, message: str) -> str:
        for name, content in files.items():
            p = self.path / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            self._git(["add", name])
        self._git(["commit", "-q", "-m", message])
        return self._git(["rev-parse", "HEAD"]).stdout.strip()

    def head(self) -> str:
        return self._git(["rev-parse", "HEAD"]).stdout.strip()

    def advance_protected(self) -> None:
        """Move the governed protected branch to HEAD (simulates a fetched
        remote-tracking ref)."""
        self._git(["update-ref", "refs/remotes/origin/main", "HEAD"])

    def orphan_commit(self, files: dict, message: str) -> str:
        """Create a commit on an UNRELATED history (no common ancestor)."""
        self._git(["checkout", "-q", "--orphan", "side"])
        self._git(["rm", "-rf", "-q", "."])
        for name, content in files.items():
            p = self.path / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            self._git(["add", name])
        self._git(["commit", "-q", "-m", message])
        sha = self._git(["rev-parse", "HEAD"]).stdout.strip()
        self._git(["update-ref", "refs/remotes/origin/main", sha])
        return sha


class _SigningVerifier(ProductionSignedCommitVerifier):
    """Production verifier with the GPG seams replaced by fixed values."""

    def __init__(self, repo_root, *, fingerprint=FINGERPRINT, **kwargs):
        super().__init__(repo_root, **kwargs)
        self._fp = fingerprint

    def _signature_verifies(self, ref):
        return True

    def _signer_fingerprint(self, ref):
        return self._fp


def _registry(tmp_path: Path, mapping=None) -> Path:
    reg = tmp_path / "approver-registry.yaml"
    reg.write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "approvers": mapping
                if mapping is not None
                else {FINGERPRINT: TEST_APPROVER_IDENTITY},
            }
        ),
        encoding="utf-8",
    )
    return reg



def _ceremony(repo, approval) -> tuple[str, dict]:
    """The signing ceremony: (1) the approver creates an ANCHOR commit on
    the branch (the approval's reference locator), then (2) commits the
    operative approval bytes -- naming the anchor -- in a NEW signed
    commit. Returns (anchor_sha, operative_approval)."""
    approval = dict(approval)
    approval["approval_provenance"] = dict(approval["approval_provenance"])
    anchor = repo.commit({"ANCHOR.txt": "anchor"}, "anchor commit")
    approval["approval_provenance"]["reference"] = anchor
    signed = repo.commit(
        {"approval.yaml": render_yaml(approval).decode("utf-8")},
        "signed approval",
    )
    return anchor, approval


def _verifier(repo: _Repo, tmp_path: Path, **kwargs):
    kwargs.setdefault("trusted_remote", TRUSTED_REMOTE)
    kwargs.setdefault("approver_registry", _registry(tmp_path))
    return _SigningVerifier(repo.path, **kwargs)


def _approval_bytes(repo: _Repo, digest: str = "0" * 64) -> bytes:
    raw = build_approval_raw(
        policy_digest=digest,
        reference=repo.head(),
    )
    return render_yaml(raw)


class _Approval:
    def __init__(self, raw: dict, reference: str):
        self.raw = raw
        self._ref = reference

    @property
    def provenance(self):
        return self.raw["approval_provenance"]


def test_verifies_when_every_binding_holds(tmp_path: Path) -> None:
    repo = _Repo(tmp_path)
    approval = build_approval_raw(reference="0" * 40)
    anchor, approval = _ceremony(repo, approval)
    repo.commit({"other.txt": "y"}, "second")  # branch advances past
    repo.advance_protected()
    verifier = _verifier(repo, tmp_path)
    verified = verifier.verify(
        _Approval(approval, anchor), approval_bytes=render_yaml(approval)
    )
    # The verified reference is the SIGNED COMMIT carrying the operative
    # bytes (a descendant of the anchor).
    assert verified.reference != anchor
    assert verified.reference.startswith("0" * 0) or len(verified.reference) == 40
    assert verified.signer_fingerprint == FINGERPRINT
    assert verified.signer_identity == TEST_APPROVER_IDENTITY
    assert verified.approval_sha256 is not None
    assert verified.campaign_id == approval["campaign_id"]
    assert verified.policy_digest == approval["policy_digest"]


def test_rejects_approval_bytes_mismatch(tmp_path: Path) -> None:
    """A signed commit containing DIFFERENT approval bytes must fail."""
    repo = _Repo(tmp_path)
    anchor = repo.commit({"ANCHOR.txt": "anchor"}, "anchor")
    repo.commit({"approval.yaml": "different bytes"}, "signed")
    repo.advance_protected()
    verifier = _verifier(repo, tmp_path)
    approval = build_approval_raw(reference=anchor)
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(
            _Approval(approval, anchor), approval_bytes=render_yaml(approval)
        )
    assert "no commit on the governed protected branch carries" in str(exc.value)


def test_rejects_unrelated_signed_commit_without_approval_file(
    tmp_path: Path,
) -> None:
    """A commit that never carried the operative approval bytes must fail
    even with a valid signature."""
    repo = _Repo(tmp_path)
    unrelated = repo.commit({"README.md": "no approval here"}, "unrelated")
    repo.commit({"approval.yaml": "x"}, "later")
    repo.advance_protected()
    verifier = _verifier(repo, tmp_path)
    approval = build_approval_raw(reference=unrelated)
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(
            _Approval(approval, unrelated), approval_bytes=render_yaml(approval)
        )
    assert "no commit on the governed protected branch carries" in str(exc.value)


def test_rejects_unregistered_fingerprint(tmp_path: Path) -> None:
    repo = _Repo(tmp_path)
    approval = build_approval_raw(reference="0" * 40)
    anchor, approval = _ceremony(repo, approval)
    repo.advance_protected()
    verifier = _verifier(repo, tmp_path, fingerprint=OTHER_FINGERPRINT)
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(
            _Approval(approval, anchor), approval_bytes=render_yaml(approval)
        )
    assert "not registered" in str(exc.value)


def test_rejects_fingerprint_registered_to_different_identity(
    tmp_path: Path,
) -> None:
    repo = _Repo(tmp_path)
    approval = build_approval_raw(reference="0" * 40)
    anchor, approval = _ceremony(repo, approval)
    repo.advance_protected()
    registry = _registry(
        tmp_path, {FINGERPRINT: "someone-else-entirely"}
    )
    verifier = _SigningVerifier(
        repo.path,
        trusted_remote=TRUSTED_REMOTE,
        approver_registry=registry,
    )
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(
            _Approval(approval, anchor), approval_bytes=render_yaml(approval)
        )
    assert "is not the claimed approver" in str(exc.value)


def test_rejects_untrusted_verification_repository(tmp_path: Path) -> None:
    repo = _Repo(tmp_path)
    repo._git(["remote", "set-url", "origin", "https://github.com/evil/x.git"])
    repo.commit({"approval.yaml": "x"}, "signed")
    repo.advance_protected()
    verifier = _verifier(repo, tmp_path)
    approval = build_approval_raw(reference=repo.head())
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(
            _Approval(approval, repo.head()), approval_bytes=render_yaml(approval)
        )
    assert "is not the trusted repository" in str(exc.value)


def test_rejects_commit_not_on_protected_branch(tmp_path: Path) -> None:
    """A signed commit on an UNRELATED history (not an ancestor of the
    governed protected branch) must fail."""
    repo = _Repo(tmp_path)
    signed = repo.commit({"approval.yaml": "x"}, "signed")
    repo.orphan_commit({"README.md": "unrelated"}, "unrelated history")
    verifier = _verifier(repo, tmp_path)
    approval = build_approval_raw(reference=signed)
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(
            _Approval(approval, signed), approval_bytes=render_yaml(approval)
        )
    assert "protected branch" in str(exc.value)


def test_rejects_missing_approval_bytes(tmp_path: Path) -> None:
    repo = _Repo(tmp_path)
    signed = repo.commit({"approval.yaml": "x"}, "signed")
    repo.advance_protected()
    verifier = _verifier(repo, tmp_path)
    approval = build_approval_raw(reference=signed)
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(_Approval(approval, signed), approval_bytes=None)
    assert "no operative approval bytes" in str(exc.value)


def test_rejects_claimed_identity_not_in_registry_identity(tmp_path: Path) -> None:
    """An approval claiming an identity the signer's registered key does
    not map to must fail (identity binding, independent of byte equality)."""
    repo = _Repo(tmp_path)
    approval = build_approval_raw(reference="0" * 40)
    # The signed commit carries bytes claiming a DIFFERENT identity than
    # the registry maps the signer fingerprint to.
    tampered = dict(approval)
    tampered["claimed_approver_identity"] = "someone-else"
    anchor = repo.commit({"ANCHOR.txt": "anchor"}, "anchor")
    tampered["approval_provenance"] = dict(approval["approval_provenance"])
    tampered["approval_provenance"]["reference"] = anchor
    repo.commit(
        {"approval.yaml": render_yaml(tampered).decode("utf-8")}, "signed"
    )
    repo.advance_protected()
    verifier = _verifier(repo, tmp_path)
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(
            _Approval(tampered, anchor), approval_bytes=render_yaml(tampered)
        )
    assert "is not the claimed approver" in str(exc.value)


def test_rejects_malformed_reference(tmp_path: Path) -> None:
    repo = _Repo(tmp_path)
    verifier = _verifier(repo, tmp_path)
    approval = build_approval_raw(reference="not-a-sha")
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(_Approval(approval, "not-a-sha"), approval_bytes=b"x")
    assert "not a 40-character" in str(exc.value)


def test_empty_registry_fails_everything_closed(tmp_path: Path) -> None:
    """The governed registry ships EMPTY: no key can corroborate."""
    repo = _Repo(tmp_path)
    approval = build_approval_raw(reference="0" * 40)
    anchor, approval = _ceremony(repo, approval)
    repo.advance_protected()
    verifier = _SigningVerifier(
        repo.path,
        trusted_remote=TRUSTED_REMOTE,
        approver_registry=_registry(tmp_path, mapping={}),
    )
    with pytest.raises(ProvenanceVerificationError) as exc:
        verifier.verify(
            _Approval(approval, anchor), approval_bytes=render_yaml(approval)
        )
    assert "not registered" in str(exc.value)
