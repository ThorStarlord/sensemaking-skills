"""Synthetic, temporary fixtures for Gate A authorization-consumer tests.

Every artifact these helpers build lives in a pytest ``tmp_path``. Nothing here
creates the real run-control directory
(``experiments/run-control/0016-...``), a real authorization record, a real
owner approval, or any Evidence 0016 artifact. The real paths are never
written and never touched.

The framework fixture copies only the two governing documents whose digests
the contract requires the consumer to verify; it does not copy or execute the
repository.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

PACKAGE_REL = "docs/experiments/STAGE-1-AUTEUR-POST-REMEDIATION-PREPARATION.md"
CHECKLIST_REL = "docs/experiments/GATE-D-STALE-DIAGNOSIS-CHECKLIST.md"

FRAMEWORK_SHA = "1" * 40
TARGET_SHA = "0653defb05625f2fcde0ac32eac6e59ccf7eeb90"
RUN_CONTROL_SHA = "2" * 40
OWNER = "ThorStarlord"
AUTHOR = "campaign-operator-bot"
EVIDENCE_NUMBER = "0016"
EVIDENCE_SLUG = "0016-stage1-auteur-post-remediation-controlled-attempt"
EXACT_MODEL = "claude-sonnet-5"
ARTIFACT_TYPE = "repository_sensemaking_brief"
TARGET_REPOSITORY = "https://github.com/ThorStarlord/auteur.git"
AUTHORIZATION_STATUS = "AUTHORIZED_FOR_ONE_CONTROLLED_INVOCATION"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def make_framework_root(tmp_path: Path) -> Path:
    """A stand-in framework checkout carrying the two governing documents."""
    root = tmp_path / "framework"
    (root / "docs" / "experiments").mkdir(parents=True)
    shutil.copyfile(REPO_ROOT / PACKAGE_REL, root / PACKAGE_REL)
    shutil.copyfile(REPO_ROOT / CHECKLIST_REL, root / CHECKLIST_REL)
    return root


def make_target_root(tmp_path: Path) -> Path:
    """A stand-in target checkout. Never the real Auteur repository."""
    root = tmp_path / "target"
    root.mkdir(parents=True)
    (root / "README.md").write_text("synthetic target fixture\n", encoding="utf-8")
    return root


def record_mapping(framework_root: Path, **overrides) -> dict:
    record = {
        "schema_version": "1",
        "authorization_status": AUTHORIZATION_STATUS,
        "authorization_scope": "single controlled Stage 1 invocation, Evidence 0016",
        "evidence_number": EVIDENCE_NUMBER,
        "evidence_slug": EVIDENCE_SLUG,
        "execution_framework_sha": FRAMEWORK_SHA,
        "target_repository": TARGET_REPOSITORY,
        "target_sha": TARGET_SHA,
        "exact_model": EXACT_MODEL,
        "artifact_type": ARTIFACT_TYPE,
        "preparation_package_path": PACKAGE_REL,
        "preparation_package_sha256": sha256_path(framework_root / PACKAGE_REL),
        "gate_d_checklist_path": CHECKLIST_REL,
        "gate_d_checklist_sha256": sha256_path(framework_root / CHECKLIST_REL),
        "authorization_record_created_at": "2026-07-30T12:00:00+00:00",
        "authorization_record_created_by": AUTHOR,
        "owner_approval_reference": "owner-approval.md",
        "one_invocation_only": True,
        "no_retry": True,
        "no_fallback": True,
        "no_model_substitution": True,
        "no_artifact_repair": True,
        "no_target_mutation": True,
        "stop_on_first_failed_gate": True,
    }
    record.update(overrides)
    return {k: v for k, v in record.items() if v is not _OMIT}


class _Omit:
    def __repr__(self):  # pragma: no cover
        return "<omit>"


_OMIT = _Omit()
OMIT = _OMIT


def approval_text(record_sha256: str, **overrides) -> str:
    fields = {
        "approver_github_identity": OWNER,
        "approval_timestamp": "2026-07-30T12:30:00+00:00",
        "authorization_record_sha256": record_sha256,
        "execution_framework_sha": FRAMEWORK_SHA,
        "target_sha": TARGET_SHA,
        "evidence_number": EVIDENCE_NUMBER,
        "evidence_slug": EVIDENCE_SLUG,
        "exact_model": EXACT_MODEL,
        "authorization_decision": AUTHORIZATION_STATUS,
        "no_retry_statement": "No retry, no rerun, no repair. Exactly one invocation.",
        "owner_decision_reference": "owner decision on the run-control PR",
    }
    fields.update(overrides)
    lines = [
        "# Owner approval - Evidence 0016 (SYNTHETIC TEST FIXTURE)",
        "",
        "This is a temporary test fixture. It is not an approval of anything.",
        "",
    ]
    for key, value in fields.items():
        if value is _OMIT:
            continue
        lines.append(f"{key}: {value}")
    extra = overrides.get("_extra_lines")
    if extra:
        lines.extend(extra)
    return "\n".join(lines) + "\n"


def make_run_control(tmp_path: Path, record_bytes: bytes, approval: str,
                     digest: str | None = None) -> tuple[Path, Path, Path]:
    """Write the three run-control artifacts into a TEMPORARY directory."""
    rc = tmp_path / "run-control" / EVIDENCE_SLUG
    rc.mkdir(parents=True, exist_ok=True)
    record_path = rc / "authorization-record.yaml"
    digest_path = rc / "authorization-record.sha256"
    approval_path = rc / "owner-approval.md"
    record_path.write_bytes(record_bytes)
    digest_path.write_text(
        (digest if digest is not None else sha256_bytes(record_bytes)) + "\n",
        encoding="utf-8", newline="",
    )
    approval_path.write_text(approval, encoding="utf-8", newline="")
    return record_path, digest_path, approval_path


def dump_record(record: dict) -> bytes:
    return yaml.safe_dump(record, sort_keys=False, allow_unicode=True).encode("utf-8")


def build_valid_case(tmp_path: Path, *, record_overrides=None, approval_overrides=None,
                     digest=None, record_bytes=None):
    """Build a fully valid synthetic Gate A case.

    Returns ``(context, heads, resolver)`` ready to pass to ``authorize``.
    """
    import sys

    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    from gate_a_authorization import AuthorizationContext

    framework_root = make_framework_root(tmp_path)
    target_root = make_target_root(tmp_path)

    record = record_mapping(framework_root, **(record_overrides or {}))
    raw = record_bytes if record_bytes is not None else dump_record(record)
    approval = approval_text(sha256_bytes(raw), **(approval_overrides or {}))
    record_path, digest_path, approval_path = make_run_control(
        tmp_path, raw, approval, digest=digest
    )

    context = AuthorizationContext(
        framework_root=framework_root,
        target_root=target_root,
        execution_framework_sha=FRAMEWORK_SHA,
        target_sha=TARGET_SHA,
        evidence_number=EVIDENCE_NUMBER,
        evidence_slug=EVIDENCE_SLUG,
        exact_model=EXACT_MODEL,
        artifact_type=ARTIFACT_TYPE,
        invocation_limit=1,
        authorization_record_path=record_path,
        authorization_digest_path=digest_path,
        owner_approval_path=approval_path,
        run_control_commit_sha=RUN_CONTROL_SHA,
        operator_identity="operator-not-the-owner",
        evidence_output_dir=tmp_path / "evidence-0016",
    )

    heads = {str(framework_root): FRAMEWORK_SHA, str(target_root): TARGET_SHA}

    def git_head(root: Path) -> str:
        return heads.get(str(root), "")

    def resolver(framework_root_, artifact_path_) -> str:
        return RUN_CONTROL_SHA

    return context, git_head, resolver, heads
