"""Approval-provenance verification boundary (Phase 3, issue #119).

The issuer must not be the judge of its own consent: it requires an
injected ``ApprovalProvenanceVerifier`` and fails closed when none is
provided. The production default is a verifier that corroborates a signed
commit reference against the repository; this package ships only the
interface. The tests inject a test double.
"""

from __future__ import annotations

from typing import Any, Protocol

from .models import VerifiedApprovalProvenance


class ProvenanceVerificationError(Exception):
    """Raised by a verifier when it cannot corroborate the approval."""


class ApprovalProvenanceVerifier(Protocol):
    """Corroborates the provenance of a validated campaign approval.

    ``verify`` receives the validated ``CampaignApproval`` and either
    returns the confirmed ``VerifiedApprovalProvenance`` or raises
    ``ProvenanceVerificationError``. The issuer cross-checks the returned
    provenance against the approval document and fails on any mismatch.
    """

    def verify(self, approval: Any) -> VerifiedApprovalProvenance:  # pragma: no cover
        ...


class ProductionSignedCommitVerifier:
    """Production default: corroborates a ``signed_commit`` provenance
    reference against the local repository.

    This implementation FAILS CLOSED and never fabricates corroboration:
    it only accepts a reference that exists as a reachable commit in the
    framework checkout. Deployment wiring (which checkout, which remote)
    is Phase 4; until then every verification attempt raises, which is
    exactly the safe default.
    """

    def __init__(self, repo_root: str) -> None:
        self._repo_root = repo_root

    def verify(self, approval: Any) -> VerifiedApprovalProvenance:
        raise ProvenanceVerificationError(
            "ProductionSignedCommitVerifier: real signed-commit "
            "corroboration is not wired until Phase 4; refusing to "
            "fabricate consent (fail closed)."
        )
