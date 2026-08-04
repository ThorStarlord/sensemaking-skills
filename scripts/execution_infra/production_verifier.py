"""Production signed-commit approval-provenance verifier (Issue #122).

The campaign framework (``src/sensemaking_skills/exploratory_authorization``)
ships the verifier interface and a fail-closed stub that refuses to
fabricate consent. This module is the REAL corroboration wiring: it verifies
that the approval's ``signed_commit`` provenance reference is a commit in
the verification repository, is reachable from the repository's current
HEAD, and carries a valid Git signature per ``git verify-commit``.

Corroboration stages, in order, each fail-closed:

1. mechanism must be exactly ``signed_commit``;
2. reference must be a 40-character lowercase hex commit SHA;
3. the commit must exist in the repository
   (``git cat-file -e <ref>^{commit}``);
4. the commit must be reachable from the repository HEAD
   (``git merge-base --is-ancestor <ref> HEAD``) -- a local-only forged
   commit is not corroboration;
5. the commit signature must verify
   (``git verify-commit <ref>``) against the repository's trusted keys.

Any failure raises ``ProvenanceVerificationError`` with the failing stage;
nothing is ever accepted on partial evidence. This verifier never invents
an approver identity or a consent statement -- it only corroborates what
the approval document already claims.
"""

import re
import subprocess
from pathlib import Path
from typing import Any

from sensemaking_skills.exploratory_authorization.models import (
    VerifiedApprovalProvenance,
)
from sensemaking_skills.exploratory_authorization.provenance import (
    ProvenanceVerificationError,
)

_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class ProductionSignedCommitVerifier:
    """Corroborates a ``signed_commit`` approval-provenance reference.

    ``repo_root`` is the verification repository (normally the framework
    checkout the campaign runs against). The reference commit must exist,
    be reachable from that repository's HEAD, and carry a valid Git
    signature.
    """

    def __init__(self, repo_root: Path, mechanism: str = "signed_commit") -> None:
        self._repo_root = Path(repo_root)
        self._mechanism = mechanism

    # -- subprocess seam (tests stub these) --------------------------------
    def _run(self, args) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(self._repo_root)] + args,
            capture_output=True, text=True, timeout=120, check=False,
        )

    def _commit_exists(self, ref: str) -> bool:
        return self._run(["cat-file", "-e", f"{ref}^{{commit}}"]).returncode == 0

    def _is_ancestor_of_head(self, ref: str) -> bool:
        return self._run(["merge-base", "--is-ancestor", ref, "HEAD"]).returncode == 0

    def _signature_verifies(self, ref: str) -> bool:
        return self._run(["verify-commit", ref]).returncode == 0

    # -- public interface --------------------------------------------------
    def verify(self, approval: Any) -> VerifiedApprovalProvenance:
        provenance = getattr(approval, "raw", approval).get("approval_provenance") or {}
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
        if not self._commit_exists(reference):
            raise ProvenanceVerificationError(
                f"signed-commit verifier: reference {reference} is not a "
                "commit in the verification repository"
            )
        if not self._is_ancestor_of_head(reference):
            raise ProvenanceVerificationError(
                f"signed-commit verifier: reference {reference} is not an "
                "ancestor of the verification repository HEAD (local-only "
                "commits are not corroboration)"
            )
        if not self._signature_verifies(reference):
            raise ProvenanceVerificationError(
                f"signed-commit verifier: reference {reference} does not "
                "carry a verifiable Git signature in this repository"
            )
        return VerifiedApprovalProvenance(mechanism=mechanism, reference=reference)
