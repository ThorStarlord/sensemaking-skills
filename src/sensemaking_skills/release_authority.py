"""Deterministic local release-authority audit.

The auditor reconciles repository-owned release identities and mechanically
inspectable Git/document/workflow state. It deliberately does not infer CI
qualification, publication state, semantic correctness, or release-owner
authorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import tomllib
from typing import Any

import yaml


CURRENT_IDENTITY_DOCS = (
    "README.md",
    "STATUS.md",
    "docs/PUBLISHING.md",
    "docs/release-v1.0-contract.md",
)


@dataclass(frozen=True)
class ReleaseAuthorityFinding:
    code: str
    detail: str
    severity: str = "error"


@dataclass(frozen=True)
class ReleaseAuthorityAudit:
    repo_root: str
    source_version: str | None
    target_version: str | None
    release_status: str | None
    git_head: str | None
    git_tree: str | None
    git_dirty: bool | None
    expected_artifacts: tuple[str, ...]
    findings: tuple[ReleaseAuthorityFinding, ...]
    qualification_established: bool = False
    publication_established: bool = False
    semantic_truth_established: bool = False

    @property
    def ok(self) -> bool:
        return not any(item.severity == "error" for item in self.findings)


def _git(repo_root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _release_metadata(repo_root: Path) -> tuple[str, str, str]:
    pyproject = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
    contract = yaml.safe_load((repo_root / "release-v1.0.yaml").read_text(encoding="utf-8"))
    source = pyproject["project"]["version"]
    release = contract["release"]
    target = release["version"]
    status = release["status"]
    if not all(isinstance(item, str) and item for item in (source, target, status)):
        raise ValueError("release source, target, and status must be non-empty strings")
    return source, target, status


def _artifact_names(source_version: str | None) -> tuple[str, ...]:
    if not source_version:
        return ()
    return (
        f"sensemaking_skills-{source_version}-py3-none-any.whl",
        f"sensemaking_skills-{source_version}.tar.gz",
    )


def audit_release_authority(repo_root: str | Path) -> ReleaseAuthorityAudit:
    root = Path(repo_root).resolve()
    findings: list[ReleaseAuthorityFinding] = []
    source: str | None = None
    target: str | None = None
    status: str | None = None

    try:
        source, target, status = _release_metadata(root)
    except (OSError, KeyError, TypeError, ValueError, tomllib.TOMLDecodeError, yaml.YAMLError) as exc:
        findings.append(
            ReleaseAuthorityFinding(
                "RELEASE_METADATA_UNREADABLE",
                f"cannot resolve repository-owned release identity: {exc}",
            )
        )

    if source and target and status:
        if status == "development":
            expected = f"{target}.dev0"
            if source != expected:
                findings.append(
                    ReleaseAuthorityFinding(
                        "RELEASE_IDENTITY_RELATION_INVALID",
                        f"development source must be {expected}, got {source}",
                    )
                )
        elif status in {"candidate", "ready"}:
            if source != target:
                findings.append(
                    ReleaseAuthorityFinding(
                        "RELEASE_IDENTITY_RELATION_INVALID",
                        f"{status} source must equal target {target}, got {source}",
                    )
                )
        else:
            findings.append(
                ReleaseAuthorityFinding(
                    "RELEASE_STATUS_INVALID",
                    f"unsupported release status: {status}",
                )
            )

        for relative in CURRENT_IDENTITY_DOCS:
            path = root / relative
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                findings.append(
                    ReleaseAuthorityFinding(
                        "RELEASE_AUTHORITY_DOCUMENT_MISSING",
                        f"{relative}: {exc}",
                    )
                )
                continue
            if source not in text:
                findings.append(
                    ReleaseAuthorityFinding(
                        "RELEASE_SOURCE_NOT_PROJECTED",
                        f"{relative} does not contain current source version {source}",
                    )
                )
            if target not in text:
                findings.append(
                    ReleaseAuthorityFinding(
                        "RELEASE_TARGET_NOT_PROJECTED",
                        f"{relative} does not contain current target version {target}",
                    )
                )

    workflow_path = root / ".github" / "workflows" / "release-candidate.yml"
    try:
        workflow = workflow_path.read_text(encoding="utf-8")
    except OSError as exc:
        findings.append(
            ReleaseAuthorityFinding(
                "RELEASE_DISTRIBUTION_WORKFLOW_MISSING",
                str(exc),
            )
        )
    else:
        required_fragments = (
            "source_version=",
            "target_version=",
            "release_status=",
            "github.event.pull_request.head.sha || github.sha",
            "push:",
        )
        for fragment in required_fragments:
            if fragment not in workflow:
                findings.append(
                    ReleaseAuthorityFinding(
                        "RELEASE_WORKFLOW_IDENTITY_BOUNDARY_MISSING",
                        f"release workflow is missing {fragment!r}",
                    )
                )
        if "sensemaking_skills-1.0.0rc1" in workflow:
            findings.append(
                ReleaseAuthorityFinding(
                    "RELEASE_WORKFLOW_HISTORICAL_IDENTITY_HARDCODED",
                    "release workflow still hardcodes historical RC1 artifact identity",
                )
            )

    git_head = _git(root, "rev-parse", "HEAD")
    git_tree = _git(root, "rev-parse", "HEAD^{tree}")
    porcelain = _git(root, "status", "--porcelain")
    git_dirty = None if porcelain is None else bool(porcelain)
    if git_head is None or git_tree is None or git_dirty is None:
        findings.append(
            ReleaseAuthorityFinding(
                "RELEASE_GIT_IDENTITY_UNAVAILABLE",
                "Git HEAD/tree/working-state identity could not be resolved",
            )
        )
    elif status in {"candidate", "ready"} and git_dirty:
        findings.append(
            ReleaseAuthorityFinding(
                "RELEASE_FROZEN_SOURCE_DIRTY",
                "candidate/ready source has uncommitted working-tree changes",
            )
        )

    return ReleaseAuthorityAudit(
        repo_root=str(root),
        source_version=source,
        target_version=target,
        release_status=status,
        git_head=git_head,
        git_tree=git_tree,
        git_dirty=git_dirty,
        expected_artifacts=_artifact_names(source),
        findings=tuple(findings),
    )


def release_authority_payload(value: ReleaseAuthorityAudit) -> dict[str, Any]:
    return {
        "ok": value.ok,
        "code": "RELEASE_AUTHORITY_VALID" if value.ok else "RELEASE_AUTHORITY_INVALID",
        "repo_root": value.repo_root,
        "source_version": value.source_version,
        "target_version": value.target_version,
        "release_status": value.release_status,
        "git": {
            "head": value.git_head,
            "tree": value.git_tree,
            "dirty": value.git_dirty,
        },
        "expected_artifacts": list(value.expected_artifacts),
        "findings": [
            {"code": item.code, "detail": item.detail, "severity": item.severity}
            for item in value.findings
        ],
        "qualification_established": False,
        "publication_established": False,
        "semantic_truth_established": False,
        "explicit_limit": (
            "Local release-authority audit reconciles repository-owned identity, "
            "Git state, current documents, and workflow mechanics. It does not "
            "establish CI qualification, public publication state, semantic truth, "
            "or release-owner authorization."
        ),
    }
