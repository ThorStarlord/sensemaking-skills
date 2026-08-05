"""Production signed-commit approval-provenance verifier (Phase 6, #122).

Framework-governed replacement for the Phase 6 readiness verifier. The
verifier proves a much stronger claim than "some commit is signed":

    this authorized human signed this exact approval document
    for this exact campaign
    binding this exact policy digest

The signing ceremony (constructible, no self-referential commit hashes):

1. The human approver creates the approval document whose
   ``approval_provenance.reference`` names an ANCHOR commit already on the
   governed protected branch (any commit they authored -- e.g. the current
   ``origin/main`` HEAD at ceremony time). An approval document can never
   name the commit that will contain it (a commit hash is computed from a
   tree that would have to contain that hash), so the reference is a real,
   earlier, well-formed commit -- a locator on the governed ancestry.
2. The human commits the approval document (the exact operative bytes) in
   a NEW commit and signs it with their approved key.
3. The verifier binds: the anchor reference exists on the governed
   ancestry; the SIGNED COMMIT whose tree carries the exact operative
   approval bytes is found on that same ancestry; that commit's signature
   is valid, its signer fingerprint is registered in the governed approver
   registry, and the registry maps the fingerprint to exactly the
   approval's ``claimed_approver_identity``; the commit is a descendant
   of the anchor reference; and the signed document's parsed fields agree
   with the operative document on campaign, digest, identity, and the
   human statement.

Concretely, ``verify`` fails closed unless ALL of the following hold:

1. provenance ``mechanism`` is exactly ``signed_commit`` and ``reference``
   is a 40-character lowercase hex commit SHA;
2. the verification repository's ``origin`` remote, normalized, equals the
   governed ``trusted_remote`` (a different repository cannot corroborate);
3. the anchor ``reference`` is a commit reachable from the governed
   protected branch (``refs/remotes/origin/main``) -- a local-only or
   unrelated-history locator is not corroboration;
4. some commit on the protected ancestry carries ``approval.yaml`` at the
   governed path BYTE-IDENTICAL to the operative approval-document bytes
   (``approval_bytes`` -- REQUIRED, fail closed when absent); the newest
   such commit is the corroboration target (an unrelated signed commit, a
   different approval document, or a same-named file with different bytes
   never matches);
5. the corroboration target is a descendant of the anchor reference
   (the ceremony order: anchor first, approval commit after);
6. ``git verify-commit`` succeeds for the corroboration target;
7. the signer's OpenPGP fingerprint (``%GF``) is registered in the
   governed approver registry, and the registry maps that fingerprint to
   exactly the approval's ``claimed_approver_identity`` -- a signature by
   any other key, or by a key registered to a different identity, fails;
8. the signed document's parsed ``campaign_id``, ``policy_digest``,
   ``claimed_approver_identity``, and ``approval_statement`` match the
   operative approval document's values and are non-empty (defense in
   depth on top of the byte equality; the bundle validator independently
   binds them to the policy).

The approver registry is part of the pinned framework (a governed trust
root), never the operator's local Git configuration. An empty registry
fails everything closed -- the correct posture until a human approver's
key is registered through framework governance.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import unicodedata
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

from sensemaking_skills.exploratory_authorization.models import (
    VerifiedApprovalProvenance,
)
from sensemaking_skills.exploratory_authorization.provenance import (
    ProvenanceVerificationError,
)
from .execution_identity import GOVERNED_APPROVAL_PATH, GOVERNED_PROTECTED_BRANCH

_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_FINGERPRINT_RE = re.compile(r"^[0-9a-f]{40}$|^[0-9a-f]{64}$")


def _norm_repo_url(value: str) -> str:
    """Reduce a git remote URL to ``host/owner/repo`` so aliases compare
    equal (mirrors the canonical normalizer in scripts/gate_a_authorization.py).

    ``https://github.com/O/R.git``, ``git@github.com:O/R``,
    ``ssh://git@github.com/O/R/`` all reduce to ``github.com/O/R``.
    """
    text = unicodedata.normalize("NFC", str(value or "")).strip()
    text = re.sub(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", "", text)
    text = text.replace("git@", "")
    if ":" in text and "@" not in text.split(":", 1)[0]:
        text = text.replace(":", "/", 1)
    text = text.rstrip("/")
    text = text.removesuffix(".git")
    parts = [p for p in text.split("/") if p]
    if len(parts) >= 3:
        parts = parts[-3:]
    return "/".join(parts).casefold()


class ProductionSignedCommitVerifier:
    """Corroborates a ``signed_commit`` approval reference with full
    byte- and identity-binding. Framework-governed: the trusted remote,
    the governed approval path, the protected branch, and the approver
    registry all come from the pinned framework."""

    def __init__(
        self,
        repo_root: Path,
        *,
        trusted_remote: str,
        approver_registry: Path,
        approval_path: str = GOVERNED_APPROVAL_PATH,
        protected_branch: str = GOVERNED_PROTECTED_BRANCH,
        mechanism: str = "signed_commit",
    ) -> None:
        self._repo_root = Path(repo_root)
        self._trusted_remote = trusted_remote
        self._approver_registry = Path(approver_registry)
        self._approval_path = approval_path
        self._protected_branch = protected_branch
        self._mechanism = mechanism

    # -- subprocess seam (tests stub these) --------------------------------
    def _run(self, args) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(self._repo_root)] + args,
            capture_output=True, text=True, timeout=120, check=False,
        )

    def _origin_url(self) -> str:
        result = self._run(["remote", "get-url", "origin"])
        if result.returncode != 0:
            raise ProvenanceVerificationError(
                "signed-commit verifier: verification repository has no "
                "'origin' remote; cannot prove it is the trusted repository"
            )
        return result.stdout.strip()

    def _protected_branch_sha(self) -> str:
        result = self._run(["rev-parse", "--verify", self._protected_branch])
        if result.returncode != 0:
            raise ProvenanceVerificationError(
                "signed-commit verifier: governed protected branch "
                f"{self._protected_branch!r} does not exist in the "
                "verification repository"
            )
        return result.stdout.strip()

    def _commit_exists(self, ref: str) -> bool:
        return self._run(["cat-file", "-e", f"{ref}^{{commit}}"]).returncode == 0

    def _is_ancestor_of(self, ref: str, ancestor_of: str) -> bool:
        return self._run(
            ["merge-base", "--is-ancestor", ref, ancestor_of]
        ).returncode == 0

    def _signature_verifies(self, ref: str) -> bool:
        return self._run(["verify-commit", ref]).returncode == 0

    def _signer_fingerprint(self, ref: str) -> str:
        result = self._run(["log", "-1", "--format=%GF", ref])
        if result.returncode != 0:
            raise ProvenanceVerificationError(
                f"signed-commit verifier: cannot read the signer fingerprint "
                f"of {ref}"
            )
        return result.stdout.strip()

    def _commits_touching_approval(self, branch_sha: str) -> list[str]:
        """Commits on the protected ancestry that touched the governed
        approval path, newest first."""
        result = self._run(
            ["log", "--format=%H", branch_sha, "--", self._approval_path]
        )
        if result.returncode != 0:
            return []
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]

    def _blob_bytes(self, ref: str, path: str) -> bytes:
        result = self._run(["show", f"{ref}:{path}"])
        if result.returncode != 0:
            raise ProvenanceVerificationError(
                f"signed-commit verifier: cannot read '{path}' at {ref}"
            )
        return result.stdout.encode("utf-8")

    # -- approver registry (governed trust root) ---------------------------
    def _load_approver_registry(self) -> Mapping[str, str]:
        path = self._approver_registry
        if not path.is_file():
            raise ProvenanceVerificationError(
                f"signed-commit verifier: approver registry missing at {path}"
            )
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        approvers = data.get("approvers") if isinstance(data, dict) else None
        if not isinstance(approvers, dict):
            raise ProvenanceVerificationError(
                "signed-commit verifier: approver registry is malformed "
                "(expected mapping 'approvers')"
            )
        return {str(k).casefold(): str(v) for k, v in approvers.items()}

    # -- public interface --------------------------------------------------
    def verify(
        self, approval: Any, *, approval_bytes: bytes | None = None
    ) -> VerifiedApprovalProvenance:
        raw = getattr(approval, "raw", approval) or {}
        provenance = dict(raw.get("approval_provenance") or {})
        mechanism = str(provenance.get("mechanism", ""))
        reference = str(provenance.get("reference", ""))

        if mechanism != self._mechanism:
            raise ProvenanceVerificationError(
                f"signed-commit verifier: provenance mechanism "
                f"{mechanism!r} is not {self._mechanism!r}"
            )
        if _SHA_RE.fullmatch(reference) is None:
            raise ProvenanceVerificationError(
                f"signed-commit verifier: reference {reference!r} is not a "
                "40-character lowercase hex commit SHA"
            )
        if approval_bytes is None:
            raise ProvenanceVerificationError(
                "signed-commit verifier: no operative approval bytes were "
                "supplied; byte-binding cannot be proven (fail closed)"
            )

        # 2. The verification repository must BE the trusted repository.
        if _norm_repo_url(self._origin_url()) != _norm_repo_url(
            self._trusted_remote
        ):
            raise ProvenanceVerificationError(
                "signed-commit verifier: verification repository origin "
                f"{self._origin_url()!r} is not the trusted repository "
                f"{self._trusted_remote!r}"
            )

        # 3. The anchor reference must exist on the governed protected
        # ancestry (a local-only or unrelated-history locator is refused).
        branch_sha = self._protected_branch_sha()
        if not self._commit_exists(reference):
            raise ProvenanceVerificationError(
                f"signed-commit verifier: reference {reference} is not a "
                "commit in the verification repository"
            )
        if not self._is_ancestor_of(reference, branch_sha):
            raise ProvenanceVerificationError(
                f"signed-commit verifier: reference {reference} is not an "
                f"ancestor of the governed protected branch "
                f"{self._protected_branch!r} ({branch_sha}); an unrelated "
                "or local-only commit is not approval corroboration"
            )

        # 4. Find the signed commit whose tree carries the EXACT operative
        # approval bytes on the protected ancestry (newest first). An
        # unrelated signed commit, or a commit carrying different approval
        # bytes, never matches.
        target = None
        for candidate in self._commits_touching_approval(branch_sha):
            try:
                blob = self._blob_bytes(candidate, self._approval_path)
            except ProvenanceVerificationError:
                continue
            if blob == approval_bytes:
                target = candidate
                break
        if target is None:
            raise ProvenanceVerificationError(
                "signed-commit verifier: no commit on the governed protected "
                "branch carries approval.yaml byte-identical to the "
                "operative approval document; the approved bytes were never "
                "signed into the governed ancestry"
            )

        # 5. Ceremony order: the corroboration target descends from the
        # anchor reference.
        if not self._is_ancestor_of(reference, target):
            raise ProvenanceVerificationError(
                f"signed-commit verifier: the commit carrying the operative "
                f"approval bytes ({target}) is not a descendant of the "
                f"anchor reference {reference}; the signing ceremony order "
                "is violated"
            )

        # 6-7. Signature valid AND the signer key is registered to the
        # claimed identity.
        if not self._signature_verifies(target):
            raise ProvenanceVerificationError(
                f"signed-commit verifier: the commit carrying the operative "
                f"approval bytes ({target}) does not carry a verifiable Git "
                "signature in this repository"
            )
        fingerprint = self._signer_fingerprint(target).casefold()
        if _FINGERPRINT_RE.fullmatch(fingerprint) is None:
            raise ProvenanceVerificationError(
                f"signed-commit verifier: cannot resolve a signer "
                f"fingerprint for {target} (got {fingerprint!r})"
            )
        registry = self._load_approver_registry()
        registered_identity = registry.get(fingerprint)
        if registered_identity is None:
            raise ProvenanceVerificationError(
                f"signed-commit verifier: signer fingerprint {fingerprint} "
                "is not registered in the governed approver registry; the "
                "signing key is not authorized for this campaign"
            )
        claimed_identity = str(raw.get("claimed_approver_identity", "") or "")
        if not claimed_identity:
            raise ProvenanceVerificationError(
                "signed-commit verifier: the approval document carries no "
                "claimed_approver_identity"
            )
        if registered_identity != claimed_identity:
            raise ProvenanceVerificationError(
                f"signed-commit verifier: signer fingerprint {fingerprint} "
                f"is registered to {registered_identity!r} but the approval "
                f"claims {claimed_identity!r}; the signer is not the "
                "claimed approver"
            )

        # 8. The signed document's parsed fields agree with the operative
        # document on campaign, digest, identity, and the human statement.
        try:
            signed_doc = yaml.safe_load(approval_bytes.decode("utf-8")) or {}
        except Exception as exc:  # unparseable blob fails closed
            raise ProvenanceVerificationError(
                "signed-commit verifier: the signed approval document is "
                f"not valid YAML: {exc}"
            ) from exc
        for field_name in (
            "campaign_id",
            "policy_digest",
            "claimed_approver_identity",
            "approval_statement",
        ):
            signed_value = (
                str(signed_doc.get(field_name, "") or "").strip()
                if isinstance(signed_doc, dict)
                else ""
            )
            operative_value = str(raw.get(field_name, "") or "").strip()
            if not signed_value or not operative_value or signed_value != operative_value:
                raise ProvenanceVerificationError(
                    f"signed-commit verifier: signed document field "
                    f"{field_name!r} does not match the operative approval "
                    "document (empty or divergent); the signed document is "
                    "not this campaign's approval"
                )

        return VerifiedApprovalProvenance(
            mechanism=mechanism,
            reference=target,
            signer_fingerprint=fingerprint,
            signer_identity=registered_identity,
            approval_path=self._approval_path,
            approval_sha256=hashlib.sha256(approval_bytes).hexdigest(),
            campaign_id=str(signed_doc.get("campaign_id", "")),
            policy_digest=str(signed_doc.get("policy_digest", "")),
        )
