"""Approval-provenance verification boundary (Phase 3, issue #119).

The issuer must not be the judge of its own consent: it requires an
injected ``ApprovalProvenanceVerifier`` and fails closed when none is
provided. This package ships only the interface and a fail-closed stub;
the REAL corroboration wiring -- signed-commit byte binding, trusted
signer registry, protected-branch ancestry -- lives in
``sensemaking_skills.exploratory_execution.production_verifier``
(framework-governed, pinned by ``framework_sha``).

The verifier interface receives the validated ``CampaignApproval`` AND the
exact operative approval-document bytes (the file the campaign package
carries), so a production verifier can prove that the signed commit's tree
contains those exact bytes. ``approval_bytes`` is optional for test
doubles; the production verifier refuses to corroborate without it.
"""

from __future__ import annotations

from typing import Any, Protocol

from .models import VerifiedApprovalProvenance


class ProvenanceVerificationError(Exception):
    """Raised by a verifier when it cannot corroborate the approval."""


class ApprovalProvenanceVerifier(Protocol):
    """Corroborates the provenance of a validated campaign approval.

    ``verify`` receives the validated ``CampaignApproval`` plus the exact
    operative approval-document bytes and either returns the confirmed
    ``VerifiedApprovalProvenance`` or raises ``ProvenanceVerificationError``.
    The issuer cross-checks the returned provenance against the approval
    document and fails on any mismatch.
    """

    def verify(
        self, approval: Any, *, approval_bytes: bytes | None = None
    ) -> VerifiedApprovalProvenance:  # pragma: no cover
        ...


class ProductionSignedCommitVerifier:
    """Production default: corroborates a ``signed_commit`` provenance
    reference against the local repository.

    This implementation FAILS CLOSED and never fabricates corroboration.
    The real signed-commit corroboration (exact approval-bytes binding,
    trusted signer registry, protected-branch ancestry) is implemented in
    ``exploratory_execution.production_verifier``; until the deployment
    wires that implementation, every verification attempt raises, which is
    exactly the safe default.
    """

    def __init__(self, repo_root: str) -> None:
        self._repo_root = repo_root

    def verify(
        self, approval: Any, *, approval_bytes: bytes | None = None
    ) -> VerifiedApprovalProvenance:
        raise ProvenanceVerificationError(
            "ProductionSignedCommitVerifier: real signed-commit "
            "corroboration is not wired in this stub; refusing to "
            "fabricate consent (fail closed)."
        )
