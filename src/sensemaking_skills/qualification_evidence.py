"""Deterministic receipts for structurally valid external qualification attempts.

The external qualification verifier answers whether a frozen attempt satisfies
the repository contract. This module makes that verifier result portable by
binding the exact manifest bytes, every verified evidence file, and the declared
candidate/runtime/target identities into one content-bound receipt.

A receipt proves what the deterministic verifier checked. It does not prove
that the evidence is semantically true and cannot, by itself, attest that a
package really originated from a live coding-agent harness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import yaml

from sensemaking_skills import path_containment as pc
from sensemaking_skills.external_qualification import (
    MANIFEST_NAME,
    PROTOCOL_ID,
    QualificationResult,
    validate_attempt,
)

SCHEMA_VERSION = "1"
EVIDENCE_SCOPE = "mechanically_verified_frozen_attempt"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_RECEIPT_FIELDS = {
    "schema_version",
    "evidence_scope",
    "protocol",
    "attempt_id",
    "manifest_sha256",
    "package_sha256",
    "outcome",
    "qualified",
    "sensemaking_candidate",
    "runtime",
    "external_target",
    "campaign_id",
    "verified_evidence",
    "receipt_sha256",
}
_CANDIDATE_FIELDS = (
    "commit_sha",
    "tree_sha",
    "distribution_filename",
    "distribution_sha256",
    "version",
)
_RUNTIME_FIELDS = (
    "os",
    "python",
    "harness",
    "harness_version",
    "adapter_target",
    "adapter_scope",
)
_TARGET_FIELDS = (
    "repository",
    "branch",
    "commit_sha",
    "tree_sha",
    "engineering_goal",
)


class QualificationEvidenceError(ValueError):
    """Raised when a qualification evidence receipt cannot be trusted."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True)
class EvidenceDigest:
    path: str
    sha256: str


@dataclass(frozen=True)
class QualificationEvidenceReceipt:
    schema_version: str
    evidence_scope: str
    protocol: str
    attempt_id: str
    manifest_sha256: str
    package_sha256: str
    outcome: str
    qualified: bool
    sensemaking_candidate: Mapping[str, Any]
    runtime: Mapping[str, Any]
    external_target: Mapping[str, Any]
    campaign_id: str
    verified_evidence: tuple[EvidenceDigest, ...]
    receipt_sha256: str

    def body_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "evidence_scope": self.evidence_scope,
            "protocol": self.protocol,
            "attempt_id": self.attempt_id,
            "manifest_sha256": self.manifest_sha256,
            "package_sha256": self.package_sha256,
            "outcome": self.outcome,
            "qualified": self.qualified,
            "sensemaking_candidate": dict(self.sensemaking_candidate),
            "runtime": dict(self.runtime),
            "external_target": dict(self.external_target),
            "campaign_id": self.campaign_id,
            "verified_evidence": [asdict(item) for item in self.verified_evidence],
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self.body_dict(), "receipt_sha256": self.receipt_sha256}


def _canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_file(root: Path, relative: str, *, label: str) -> Path:
    parsed = PurePosixPath(relative.replace("\\", "/"))
    if parsed.is_absolute() or not parsed.parts or ".." in parsed.parts:
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_PATH_UNSAFE",
            f"{label} must be a safe attempt-relative path: {relative!r}",
        )
    candidate = root.joinpath(*parsed.parts)
    if not os.path.lexists(candidate):
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_FILE_MISSING",
            f"{label} does not exist: {relative}",
        )
    try:
        resolved, failure = pc.resolve_containment(candidate, root)
    except Exception as exc:  # pragma: no cover - defensive fail closed
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_CONTAINMENT_ERROR",
            f"could not establish containment for {label}: {exc}",
        ) from exc
    if failure is not None or resolved is None or not resolved.is_file():
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_PATH_UNSAFE",
            f"{label} must resolve to a regular file inside the attempt root",
        )
    return resolved


def _load_manifest(root: Path) -> dict[str, Any]:
    path = _safe_file(root, MANIFEST_NAME, label="attempt manifest")
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_MANIFEST_READ_ERROR",
            f"could not read attempt manifest: {exc}",
        ) from exc
    if not isinstance(value, Mapping):
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_MANIFEST_INVALID",
            "attempt manifest must be a mapping",
        )
    return dict(value)


def _copy_fields(value: Any, fields: tuple[str, ...], *, label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_MANIFEST_INVALID",
            f"{label} must be a mapping",
        )
    missing = [field for field in fields if field not in value]
    if missing:
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_MANIFEST_INVALID",
            f"{label} missing field(s): {missing}",
        )
    return {field: value[field] for field in fields}


def _require_valid_result(result: QualificationResult) -> None:
    if result.package_valid:
        return
    detail = "; ".join(
        f"{item.code}: {item.message}" for item in result.diagnostics
    ) or "external qualification verifier rejected the attempt"
    raise QualificationEvidenceError(
        "QUALIFICATION_ATTEMPT_NOT_STRUCTURALLY_VALID",
        detail,
    )


def build_qualification_evidence(
    attempt_dir: str | Path,
) -> QualificationEvidenceReceipt:
    """Build a deterministic receipt for one structurally valid frozen attempt."""
    result = validate_attempt(attempt_dir)
    _require_valid_result(result)
    if result.attempt_id is None or result.manifest_sha256 is None or result.outcome is None:
        raise QualificationEvidenceError(
            "QUALIFICATION_RESULT_INCOMPLETE",
            "structurally valid attempt returned incomplete verifier identity",
        )

    root = Path(attempt_dir).resolve(strict=True)
    manifest_path = _safe_file(root, MANIFEST_NAME, label="attempt manifest")
    manifest = _load_manifest(root)
    candidate = _copy_fields(
        manifest.get("sensemaking_candidate"), _CANDIDATE_FIELDS, label="sensemaking_candidate"
    )
    runtime = _copy_fields(manifest.get("runtime"), _RUNTIME_FIELDS, label="runtime")
    target = _copy_fields(
        manifest.get("external_target"), _TARGET_FIELDS, label="external_target"
    )
    campaign = manifest.get("campaign")
    if not isinstance(campaign, Mapping) or not isinstance(campaign.get("campaign_id"), str):
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_MANIFEST_INVALID",
            "campaign.campaign_id must be present",
        )

    evidence = tuple(
        EvidenceDigest(
            path=relative,
            sha256=_file_sha256(_safe_file(root, relative, label=f"verified evidence {relative}")),
        )
        for relative in sorted(result.verified_evidence)
    )
    actual_manifest_sha256 = _file_sha256(manifest_path)
    if actual_manifest_sha256 != result.manifest_sha256:
        raise QualificationEvidenceError(
            "QUALIFICATION_MANIFEST_DIGEST_DRIFT",
            "attempt manifest changed between verification and receipt construction",
        )

    package_sha256 = _canonical_sha256(
        {
            "manifest_sha256": actual_manifest_sha256,
            "verified_evidence": [asdict(item) for item in evidence],
        }
    )
    provisional = QualificationEvidenceReceipt(
        schema_version=SCHEMA_VERSION,
        evidence_scope=EVIDENCE_SCOPE,
        protocol=PROTOCOL_ID,
        attempt_id=result.attempt_id,
        manifest_sha256=actual_manifest_sha256,
        package_sha256=package_sha256,
        outcome=result.outcome,
        qualified=result.qualified,
        sensemaking_candidate=candidate,
        runtime=runtime,
        external_target=target,
        campaign_id=campaign["campaign_id"],
        verified_evidence=evidence,
        receipt_sha256="0" * 64,
    )
    receipt_sha256 = _canonical_sha256(provisional.body_dict())
    return QualificationEvidenceReceipt(
        **{key: value for key, value in provisional.__dict__.items() if key != "receipt_sha256"},
        receipt_sha256=receipt_sha256,
    )


def load_qualification_evidence(path: str | Path) -> dict[str, Any]:
    """Load a receipt with strict top-level shape and digest checks."""
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_RECEIPT_READ_ERROR",
            f"could not read qualification evidence receipt: {exc}",
        ) from exc
    if not isinstance(value, Mapping):
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_RECEIPT_INVALID",
            "qualification evidence receipt must be a JSON object",
        )
    data = dict(value)
    unknown = sorted(set(data) - _RECEIPT_FIELDS)
    missing = sorted(_RECEIPT_FIELDS - set(data))
    if unknown or missing:
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_RECEIPT_INVALID",
            f"receipt fields invalid: unknown={unknown} missing={missing}",
        )
    if data["schema_version"] != SCHEMA_VERSION:
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_SCHEMA_UNSUPPORTED",
            f"unsupported receipt schema: {data['schema_version']!r}",
        )
    if data["evidence_scope"] != EVIDENCE_SCOPE:
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_SCOPE_MISMATCH",
            f"receipt evidence_scope must be {EVIDENCE_SCOPE!r}",
        )
    if data["protocol"] != PROTOCOL_ID:
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_PROTOCOL_MISMATCH",
            f"receipt protocol must be {PROTOCOL_ID!r}",
        )
    for field in ("manifest_sha256", "package_sha256", "receipt_sha256"):
        if not isinstance(data[field], str) or not _SHA256.fullmatch(data[field]):
            raise QualificationEvidenceError(
                "QUALIFICATION_EVIDENCE_RECEIPT_INVALID",
                f"{field} must be lowercase SHA-256",
            )
    body = {key: data[key] for key in data if key != "receipt_sha256"}
    if _canonical_sha256(body) != data["receipt_sha256"]:
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_RECEIPT_DIGEST_MISMATCH",
            "receipt payload no longer matches receipt_sha256",
        )
    return data


def write_qualification_evidence(
    attempt_dir: str | Path,
    destination: str | Path,
) -> QualificationEvidenceReceipt:
    """Create one receipt without overwriting an existing evidence artifact."""
    receipt = build_qualification_evidence(attempt_dir)
    path = Path(destination)
    parent = path.parent
    if not parent.exists() or not parent.is_dir():
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_OUTPUT_PARENT_MISSING",
            f"receipt parent directory does not exist: {parent}",
        )
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(
                receipt.to_dict(),
                handle,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            )
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_OUTPUT_EXISTS",
            f"refusing to overwrite existing receipt: {path}",
        ) from exc
    return receipt


def verify_qualification_evidence(
    attempt_dir: str | Path,
    receipt_path: str | Path,
) -> QualificationEvidenceReceipt:
    """Rebuild the expected receipt and require exact equality."""
    expected = build_qualification_evidence(attempt_dir)
    actual = load_qualification_evidence(receipt_path)
    if actual != expected.to_dict():
        raise QualificationEvidenceError(
            "QUALIFICATION_EVIDENCE_ATTEMPT_MISMATCH",
            "receipt does not match the exact supplied attempt package",
        )
    return expected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create or verify deterministic external qualification evidence receipts."
    )
    parser.add_argument("attempt_dir")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--output", type=Path)
    mode.add_argument("--verify", type=Path)
    args = parser.parse_args(argv)

    try:
        if args.output is not None:
            receipt = write_qualification_evidence(args.attempt_dir, args.output)
            print("QUALIFICATION_EVIDENCE_RECEIPT_WRITTEN")
            print(f"attempt_id={receipt.attempt_id}")
            print(f"outcome={receipt.outcome}")
            print(f"qualified={str(receipt.qualified).lower()}")
            print(f"package_sha256={receipt.package_sha256}")
            print(f"receipt_sha256={receipt.receipt_sha256}")
            return 0

        receipt = verify_qualification_evidence(args.attempt_dir, args.verify)
        print("QUALIFICATION_EVIDENCE_RECEIPT_VALID")
        print(f"attempt_id={receipt.attempt_id}")
        print(f"receipt_sha256={receipt.receipt_sha256}")
        return 0
    except QualificationEvidenceError as exc:
        print("QUALIFICATION_EVIDENCE_RECEIPT_INVALID")
        print(f"{exc.code}: {exc.message}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
