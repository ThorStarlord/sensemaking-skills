"""Append-only narrative verification receipts for durable Campaign state.

Narrative verification is deliberately mechanical. The active coding agent
supplies claim/evidence bindings. This module checks only that each claim is an
exact member of the current durable Campaign narrative, that every referenced
evidence item already satisfies the Campaign evidence contract, and that the
exact evidence bytes remain unchanged.

A verification receipt therefore means:

    claim existed in the bound Campaign state
    + cited durable evidence existed with these exact bytes

It does *not* mean that the evidence proves the claim, that the claim is true,
or that any semantic transition is warranted.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

import yaml

from sensemaking_skills import path_containment as pc
from sensemaking_skills.campaign_semantics import (
    CampaignState,
    ClaimEvidence,
    canonicalize,
)

from .admission import sha256_file
from .errors import (
    CampaignIntegrityError,
    CampaignTransactionError,
    CampaignWorkspaceError,
)
from .target_snapshot import CampaignService


_SCHEMA_VERSION = "1"
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_RECEIPT_NAME_RE = re.compile(
    r"^(?P<receipt_id>[A-Za-z0-9][A-Za-z0-9._-]*)--(?P<digest>[0-9a-f]{64})\.yaml$"
)
_SCOPES = {"current_state", "established_fact", "resolved_question"}
_CLAIM_FIELDS = {
    "claim",
    "scope",
    "method",
    "coverage",
    "claim_strength",
    "evidence",
}
_RECEIPT_FIELDS = {
    "campaign_id",
    "receipt_id",
    "state_sha256",
    "claims",
    "evidence_sha256",
    "schema_version",
}


class CampaignNarrativeContractError(ValueError):
    """Raised when narrative-verification data is structurally ambiguous."""


@dataclass(frozen=True)
class NarrativeVerificationReceipt:
    campaign_id: str
    receipt_id: str
    state_sha256: str
    claims: tuple[ClaimEvidence, ...]
    evidence_sha256: Mapping[str, str]
    schema_version: str = _SCHEMA_VERSION


@dataclass(frozen=True)
class NarrativeVerificationResult:
    receipt: NarrativeVerificationReceipt
    receipt_ref: str
    receipt_sha256: str


@dataclass(frozen=True)
class NarrativeVerificationStatus:
    receipt_id: str
    receipt_ref: str
    receipt_sha256: str
    state_sha256: str
    current_state_match: bool
    claim_count: int
    evidence_refs: tuple[str, ...]


def _canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _state_sha256(state: CampaignState) -> str:
    return _canonical_digest(canonicalize(state))


def _claim_payload(claim: ClaimEvidence) -> dict[str, Any]:
    return {
        "claim": claim.claim,
        "scope": claim.scope,
        "method": claim.method,
        "coverage": list(claim.coverage),
        "claim_strength": claim.claim_strength,
        "evidence": list(claim.evidence),
    }


def _receipt_payload(receipt: NarrativeVerificationReceipt) -> dict[str, Any]:
    return {
        "campaign_id": receipt.campaign_id,
        "receipt_id": receipt.receipt_id,
        "state_sha256": receipt.state_sha256,
        "claims": [_claim_payload(claim) for claim in receipt.claims],
        "evidence_sha256": dict(sorted(receipt.evidence_sha256.items())),
        "schema_version": receipt.schema_version,
    }


def dump_narrative_verification_receipt(
    receipt: NarrativeVerificationReceipt,
) -> dict[str, Any]:
    if not isinstance(receipt, NarrativeVerificationReceipt):
        raise CampaignNarrativeContractError(
            "dump_narrative_verification_receipt expects NarrativeVerificationReceipt"
        )
    return _receipt_payload(receipt)


def _require_text(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise CampaignNarrativeContractError(f"{field} must be a non-empty string")
    return value


def _text_tuple(value: Any, *, field: str) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or isinstance(value, (str, bytes)):
        raise CampaignNarrativeContractError(f"{field} must be a list")
    result: list[str] = []
    for index, item in enumerate(value):
        result.append(_require_text(item, field=f"{field}[{index}]"))
    return tuple(result)


def _load_claim(value: Any, *, path: str) -> ClaimEvidence:
    if isinstance(value, ClaimEvidence):
        claim = value
    else:
        if not isinstance(value, Mapping):
            raise CampaignNarrativeContractError(f"{path} must be a mapping")
        data = dict(value)
        unknown = sorted(set(data) - _CLAIM_FIELDS)
        missing = sorted(_CLAIM_FIELDS - set(data))
        if unknown or missing:
            raise CampaignNarrativeContractError(
                f"{path} fields invalid: unknown={unknown} missing={missing}"
            )
        claim = ClaimEvidence(
            claim=_require_text(data["claim"], field=f"{path}.claim"),
            scope=_require_text(data["scope"], field=f"{path}.scope"),
            method=_require_text(data["method"], field=f"{path}.method"),
            coverage=_text_tuple(data["coverage"], field=f"{path}.coverage"),
            claim_strength=_require_text(
                data["claim_strength"], field=f"{path}.claim_strength"
            ),
            evidence=_text_tuple(data["evidence"], field=f"{path}.evidence"),
        )

    _require_text(claim.claim, field=f"{path}.claim")
    _require_text(claim.scope, field=f"{path}.scope")
    _require_text(claim.method, field=f"{path}.method")
    _require_text(claim.claim_strength, field=f"{path}.claim_strength")
    _text_tuple(claim.coverage, field=f"{path}.coverage")
    evidence = _text_tuple(claim.evidence, field=f"{path}.evidence")
    if claim.scope not in _SCOPES:
        raise CampaignNarrativeContractError(
            f"{path}.scope must be one of {sorted(_SCOPES)}"
        )
    if not evidence:
        raise CampaignNarrativeContractError(
            f"{path}.evidence must cite at least one durable evidence ref"
        )
    return claim


def load_narrative_claims(value: Any) -> tuple[ClaimEvidence, ...]:
    """Load strict claim bindings from a mapping/list or YAML path.

    Supported document shape::

        claims:
          - claim: "..."
            scope: established_fact
            method: agent_cross_check
            coverage: ["artifact section 3"]
            claim_strength: supported
            evidence: ["evidence/review.txt"]
    """
    if isinstance(value, (str, Path)):
        with Path(value).open("r", encoding="utf-8") as handle:
            value = yaml.safe_load(handle)
    if isinstance(value, Mapping):
        data = dict(value)
        unknown = sorted(set(data) - {"claims"})
        if unknown or "claims" not in data:
            raise CampaignNarrativeContractError(
                f"narrative claim document fields invalid: unknown={unknown}"
            )
        value = data["claims"]
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise CampaignNarrativeContractError("narrative claims must be a list")
    claims = tuple(
        _load_claim(item, path=f"claims[{index}]")
        for index, item in enumerate(value)
    )
    if not claims:
        raise CampaignNarrativeContractError("at least one narrative claim is required")
    keys = [(claim.scope, claim.claim) for claim in claims]
    if len(keys) != len(set(keys)):
        raise CampaignNarrativeContractError(
            "duplicate narrative claim/scope bindings are not allowed"
        )
    return claims


def load_narrative_verification_receipt(value: Any) -> NarrativeVerificationReceipt:
    if isinstance(value, (str, Path)):
        with Path(value).open("r", encoding="utf-8") as handle:
            value = yaml.safe_load(handle)
    if not isinstance(value, Mapping):
        raise CampaignNarrativeContractError("narrative verification receipt must be a mapping")
    data = dict(value)
    unknown = sorted(set(data) - _RECEIPT_FIELDS)
    missing = sorted(_RECEIPT_FIELDS - set(data))
    if unknown or missing:
        raise CampaignNarrativeContractError(
            f"narrative verification receipt fields invalid: unknown={unknown} missing={missing}"
        )
    if data["schema_version"] != _SCHEMA_VERSION:
        raise CampaignNarrativeContractError(
            f"unsupported narrative verification schema_version: {data['schema_version']!r}"
        )
    campaign_id = _require_text(data["campaign_id"], field="campaign_id")
    receipt_id = _require_text(data["receipt_id"], field="receipt_id")
    if not _SAFE_ID.fullmatch(receipt_id):
        raise CampaignNarrativeContractError("receipt_id contains unsafe characters")
    state_digest = _require_text(data["state_sha256"], field="state_sha256")
    if not _SHA256_RE.fullmatch(state_digest):
        raise CampaignNarrativeContractError("state_sha256 must be lowercase SHA-256")
    claims = load_narrative_claims(data["claims"])
    evidence_sha256 = data["evidence_sha256"]
    if not isinstance(evidence_sha256, Mapping):
        raise CampaignNarrativeContractError("evidence_sha256 must be a mapping")
    normalized_digests: dict[str, str] = {}
    for ref, digest in evidence_sha256.items():
        ref_text = _require_text(ref, field="evidence_sha256 key")
        digest_text = _require_text(digest, field=f"evidence_sha256[{ref_text!r}]")
        if not _SHA256_RE.fullmatch(digest_text):
            raise CampaignNarrativeContractError(
                f"evidence_sha256[{ref_text!r}] must be lowercase SHA-256"
            )
        normalized_digests[ref_text] = digest_text
    cited = {ref for claim in claims for ref in claim.evidence}
    if set(normalized_digests) != cited:
        raise CampaignNarrativeContractError(
            "evidence_sha256 keys must exactly equal the evidence refs cited by claims"
        )
    return NarrativeVerificationReceipt(
        campaign_id=campaign_id,
        receipt_id=receipt_id,
        state_sha256=state_digest,
        claims=claims,
        evidence_sha256=normalized_digests,
    )


def _assert_physically_contained(path: Path, root: Path) -> None:
    try:
        resolved, failure = pc.resolve_containment(path, root)
    except Exception as exc:  # pragma: no cover - defensive fail-closed guard
        raise CampaignWorkspaceError(
            f"could not establish narrative verification path containment for {path}: {exc}"
        ) from exc
    if failure is not None or resolved is None:
        raise CampaignWorkspaceError(
            "narrative verification path is not physically contained: "
            f"path={path} root={root} failure={failure}"
        )
    try:
        resolved_root = root.resolve(strict=False)
    except OSError as exc:
        raise CampaignWorkspaceError(
            f"could not resolve narrative verification root {root}: {exc}"
        ) from exc
    if (
        pc.canonicalize_path(resolved).relative_to_root(
            pc.canonicalize_path(resolved_root)
        )
        is None
    ):
        raise CampaignWorkspaceError(
            f"narrative verification path escapes its physical root: {path}"
        )


def _safe_workspace_ref(ref: str) -> PurePosixPath:
    parsed = PurePosixPath(ref)
    if (
        not ref
        or parsed.is_absolute()
        or ".." in parsed.parts
        or "." in parsed.parts
    ):
        raise CampaignNarrativeContractError(
            f"evidence ref must be a safe workspace-relative path: {ref!r}"
        )
    return parsed


def _evidence_path(root: Path, ref: str) -> Path:
    parsed = _safe_workspace_ref(ref)
    path = root.joinpath(*parsed.parts)
    _assert_physically_contained(path, root)
    if not path.is_file():
        raise CampaignIntegrityError(
            f"narrative verification evidence is missing: {ref}",
            diagnostic_codes=("NARRATIVE_VERIFICATION_EVIDENCE_MISSING",),
        )
    return path


def _receipt_directory(root: Path, *, create: bool) -> Path | None:
    directory = root / "narrative-verifications"
    if os.path.lexists(directory):
        if directory.is_symlink() or not directory.is_dir():
            raise CampaignIntegrityError(
                "narrative verification path must be a real directory",
                diagnostic_codes=("NARRATIVE_VERIFICATION_DIRECTORY_INVALID",),
            )
        _assert_physically_contained(directory, root)
        return directory
    if not create:
        return None
    try:
        directory.mkdir()
    except OSError as exc:
        raise CampaignWorkspaceError(
            f"could not create narrative verification directory: {exc}"
        ) from exc
    _assert_physically_contained(directory, root)
    return directory


def _exclusive_write(path: Path, payload: Mapping[str, Any]) -> None:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError as exc:
        raise CampaignTransactionError(
            f"narrative verification receipt already exists: {path.name}"
        ) from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            yaml.safe_dump(dict(payload), handle, sort_keys=False, allow_unicode=True)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        if path.exists():
            path.unlink()
        raise


class CampaignNarrativeVerificationService:
    """Persist and inspect mechanical claim/evidence bindings for Campaign state."""

    def __init__(self, workspace: str | Path) -> None:
        self.workspace = Path(workspace)

    def _snapshot(self):
        return CampaignService(self.workspace).resume()

    @staticmethod
    def _claim_matches_state(claim: ClaimEvidence, state: CampaignState) -> bool:
        if claim.scope == "current_state":
            return claim.claim == state.current_state
        if claim.scope == "established_fact":
            return claim.claim in state.established_facts
        if claim.scope == "resolved_question":
            return claim.claim in state.resolved_questions
        return False

    def verify(
        self,
        *,
        receipt_id: str,
        claims: Sequence[ClaimEvidence] | Mapping[str, Any] | str | Path,
    ) -> NarrativeVerificationResult:
        """Bind exact current narrative claims to exact durable evidence bytes."""
        if not isinstance(receipt_id, str) or not _SAFE_ID.fullmatch(receipt_id):
            raise CampaignTransactionError(
                "narrative verification receipt id must use only letters, numbers, '.', '_' or '-'"
            )
        normalized = load_narrative_claims(claims)
        snapshot = self._snapshot()

        for claim in normalized:
            if not self._claim_matches_state(claim, snapshot.state):
                raise CampaignTransactionError(
                    "narrative claim is not an exact member of the current Campaign state: "
                    f"scope={claim.scope!r} claim={claim.claim!r}"
                )

        available = set(snapshot.evidence_refs)
        cited = sorted({ref for claim in normalized for ref in claim.evidence})
        missing = sorted(set(cited) - available)
        if missing:
            raise CampaignTransactionError(
                "narrative verification references non-durable evidence: "
                + ", ".join(missing)
            )

        root = CampaignService(self.workspace).store.root
        evidence_digests = {
            ref: sha256_file(_evidence_path(root, ref))
            for ref in cited
        }
        receipt = NarrativeVerificationReceipt(
            campaign_id=snapshot.state.campaign_id,
            receipt_id=receipt_id,
            state_sha256=_state_sha256(snapshot.state),
            claims=normalized,
            evidence_sha256=evidence_digests,
        )
        payload = _receipt_payload(receipt)
        digest = _canonical_digest(payload)

        existing = self.history()
        if any(item.receipt_id == receipt_id for item in existing):
            raise CampaignTransactionError(
                f"narrative verification receipt id already exists: {receipt_id}"
            )

        directory = _receipt_directory(root, create=True)
        assert directory is not None
        path = directory / f"{receipt_id}--{digest}.yaml"
        _assert_physically_contained(path, directory)
        _exclusive_write(path, payload)
        return NarrativeVerificationResult(
            receipt=receipt,
            receipt_ref=path.relative_to(root).as_posix(),
            receipt_sha256=digest,
        )

    def history(self) -> tuple[NarrativeVerificationStatus, ...]:
        """Validate all receipts and report whether each binds the current state."""
        snapshot = self._snapshot()
        root = CampaignService(self.workspace).store.root
        directory = _receipt_directory(root, create=False)
        if directory is None:
            return ()

        current_state_digest = _state_sha256(snapshot.state)
        available = set(snapshot.evidence_refs)
        statuses: list[NarrativeVerificationStatus] = []
        seen_ids: set[str] = set()

        for path in sorted(directory.iterdir()):
            _assert_physically_contained(path, directory)
            match = _RECEIPT_NAME_RE.fullmatch(path.name)
            if path.is_symlink() or not path.is_file() or match is None:
                raise CampaignIntegrityError(
                    "narrative verification directory contains an invalid entry",
                    diagnostic_codes=("INVALID_NARRATIVE_VERIFICATION_RECEIPT",),
                )
            try:
                receipt = load_narrative_verification_receipt(path)
            except (CampaignNarrativeContractError, OSError, yaml.YAMLError) as exc:
                raise CampaignIntegrityError(
                    f"narrative verification receipt is invalid: {path.name}",
                    diagnostic_codes=("INVALID_NARRATIVE_VERIFICATION_RECEIPT",),
                ) from exc

            if receipt.receipt_id != match.group("receipt_id"):
                raise CampaignIntegrityError(
                    "narrative verification receipt id does not match its filename",
                    diagnostic_codes=("INVALID_NARRATIVE_VERIFICATION_RECEIPT",),
                )
            if receipt.receipt_id in seen_ids:
                raise CampaignIntegrityError(
                    f"duplicate narrative verification receipt id: {receipt.receipt_id}",
                    diagnostic_codes=("DUPLICATE_NARRATIVE_VERIFICATION_RECEIPT",),
                )
            seen_ids.add(receipt.receipt_id)
            if receipt.campaign_id != snapshot.state.campaign_id:
                raise CampaignIntegrityError(
                    "narrative verification receipt belongs to a different Campaign",
                    diagnostic_codes=("NARRATIVE_VERIFICATION_CAMPAIGN_ID_MISMATCH",),
                )

            payload_digest = _canonical_digest(_receipt_payload(receipt))
            if payload_digest != match.group("digest"):
                raise CampaignIntegrityError(
                    f"narrative verification receipt digest mismatch: {path.name}",
                    diagnostic_codes=("NARRATIVE_VERIFICATION_DIGEST_MISMATCH",),
                )

            cited = set(receipt.evidence_sha256)
            missing = sorted(cited - available)
            if missing:
                raise CampaignIntegrityError(
                    "narrative verification evidence is no longer durable: "
                    + ", ".join(missing),
                    diagnostic_codes=("NARRATIVE_VERIFICATION_EVIDENCE_MISSING",),
                )
            for ref, expected_digest in receipt.evidence_sha256.items():
                actual_digest = sha256_file(_evidence_path(root, ref))
                if actual_digest != expected_digest:
                    raise CampaignIntegrityError(
                        f"narrative verification evidence bytes changed: {ref}",
                        diagnostic_codes=(
                            "NARRATIVE_VERIFICATION_EVIDENCE_DIGEST_MISMATCH",
                        ),
                    )

            statuses.append(
                NarrativeVerificationStatus(
                    receipt_id=receipt.receipt_id,
                    receipt_ref=path.relative_to(root).as_posix(),
                    receipt_sha256=payload_digest,
                    state_sha256=receipt.state_sha256,
                    current_state_match=(receipt.state_sha256 == current_state_digest),
                    claim_count=len(receipt.claims),
                    evidence_refs=tuple(sorted(cited)),
                )
            )
        return tuple(statuses)
