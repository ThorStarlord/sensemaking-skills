"""Evaluate whether the repository may be called a final Version 1.0 release.

The gate consumes repository-owned release metadata plus provenance-bound release
sidecars. The sidecars are deliberately outside tracked source identity so
recording CI results, artifact hashes, or owner authorization does not mutate the
exact source bytes those facts attest.

Mechanical validation of a sidecar establishes only that the recorded evidence
is internally consistent with the current exact head. It does not independently
query GitHub, make an owner decision, or establish semantic product usefulness.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

import yaml


DEFAULT_CI_EVIDENCE = Path(".release-evidence") / "ci.yaml"
DEFAULT_OWNER_AUTHORIZATION = Path(".release-evidence") / "owner-authorization.yaml"
DEFAULT_ARTIFACT_DIGESTS = Path("dist") / "SHA256SUMS"

_REQUIRED_CI_CHECKS = {
    "product_validation": "Product Validation",
    "release_candidate_distribution": "Release Candidate Distribution",
}


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


def _resolve_path(repo_root: Path, value: str | Path | None, default: Path) -> Path:
    if value is None:
        return (repo_root / default).resolve()
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def _load_yaml(path: Path, label: str, diagnostics: list[str]) -> dict[str, Any] | None:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        diagnostics.append(f"{label} is missing or unreadable: {exc}")
        return None
    except yaml.YAMLError as exc:
        diagnostics.append(f"{label} is invalid YAML: {exc}")
        return None
    if not isinstance(value, dict):
        diagnostics.append(f"{label} must be a YAML mapping")
        return None
    return value


def _validate_ci_evidence(
    path: Path,
    *,
    target: str | None,
    git_head: str | None,
    diagnostics: list[str],
) -> None:
    evidence = _load_yaml(path, "exact release head CI evidence", diagnostics)
    if evidence is None:
        return

    if evidence.get("schema_version") != 1:
        diagnostics.append("exact release head CI evidence schema_version must be 1")
    if target and evidence.get("release_version") != target:
        diagnostics.append(
            "exact release head CI evidence release_version does not match release target"
        )
    if git_head and evidence.get("source_sha") != git_head:
        diagnostics.append(
            "exact release head CI evidence source_sha does not match current Git HEAD"
        )

    for key, workflow_name in _REQUIRED_CI_CHECKS.items():
        item = evidence.get(key)
        if not isinstance(item, dict):
            diagnostics.append(f"exact release head CI evidence is missing {key}")
            continue
        if item.get("workflow") != workflow_name:
            diagnostics.append(
                f"exact release head CI evidence {key}.workflow must be {workflow_name!r}"
            )
        run_id = item.get("run_id")
        if isinstance(run_id, bool) or not isinstance(run_id, int) or run_id <= 0:
            diagnostics.append(
                f"exact release head CI evidence {key}.run_id must be a positive integer"
            )
        if item.get("conclusion") != "success":
            diagnostics.append(
                f"exact release head CI evidence {key}.conclusion must be 'success'"
            )


def _validate_owner_authorization(
    path: Path,
    *,
    target: str | None,
    git_head: str | None,
    diagnostics: list[str],
) -> None:
    evidence = _load_yaml(path, "release-owner authorization", diagnostics)
    if evidence is None:
        return

    if evidence.get("schema_version") != 1:
        diagnostics.append("release-owner authorization schema_version must be 1")
    if evidence.get("decision") != "AUTHORIZE_FINAL_1_0_PUBLICATION":
        diagnostics.append(
            "release-owner authorization decision must be AUTHORIZE_FINAL_1_0_PUBLICATION"
        )
    if target and evidence.get("release_version") != target:
        diagnostics.append(
            "release-owner authorization release_version does not match release target"
        )
    if git_head and evidence.get("source_sha") != git_head:
        diagnostics.append(
            "release-owner authorization source_sha does not match current Git HEAD"
        )
    for field in ("authorized_by", "authorized_at"):
        value = evidence.get(field)
        if not isinstance(value, str) or not value.strip():
            diagnostics.append(f"release-owner authorization {field} must be non-empty")


def _validate_artifact_digests(
    path: Path,
    *,
    source_version: str | None,
    diagnostics: list[str],
) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        diagnostics.append(f"artifact SHA-256 digest record is missing or unreadable: {exc}")
        return

    records: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-fA-F]{64})\s+\*?(.+)", line)
        if match is None:
            diagnostics.append("artifact SHA-256 digest record contains an invalid line")
            continue
        records[Path(match.group(2)).name] = match.group(1).lower()

    if source_version:
        expected = {
            f"sensemaking_skills-{source_version}-py3-none-any.whl",
            f"sensemaking_skills-{source_version}.tar.gz",
        }
        missing = sorted(expected - set(records))
        if missing:
            diagnostics.append(
                "artifact SHA-256 digest record is missing expected artifacts: "
                + ", ".join(missing)
            )


def readiness_diagnostics(
    repo_root: Path,
    *,
    ci_evidence_path: str | Path | None = None,
    owner_authorization_path: str | Path | None = None,
    artifact_digests_path: str | Path | None = None,
) -> list[str]:
    """Return deterministic blockers; never convert missing evidence to PASS."""

    repo_root = repo_root.resolve()
    diagnostics: list[str] = []
    contract_path = repo_root / "release-v1.0.yaml"
    try:
        contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"cannot read release contract: {exc}"]

    release = contract.get("release", {}) if isinstance(contract, dict) else {}
    target = release.get("version")
    status = release.get("status")
    if target != "1.0.0":
        diagnostics.append(f"release target is {target or 'missing'}, not final 1.0.0")
    if status != "ready":
        diagnostics.append(f"release status is {status or 'missing'}")

    pyproject_path = repo_root / "pyproject.toml"
    source_version: str | None = None
    try:
        pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        diagnostics.append(f"project metadata is unreadable: {exc}")
    else:
        project = pyproject.get("project", {})
        source_version = project.get("version")
        classifiers = project.get("classifiers", [])
        if status == "ready" and source_version != target:
            diagnostics.append(
                f"ready source version {source_version} does not match release target {target}"
            )
        if status != "ready" and (
            "Development Status :: 5 - Production/Stable" in classifiers
            or "Development Status :: 4 - Beta" not in classifiers
        ):
            diagnostics.append(
                "project metadata does not classify the pre-release/development source as Beta"
            )
        if status == "ready" and (
            "Development Status :: 5 - Production/Stable" not in classifiers
            or "Development Status :: 4 - Beta" in classifiers
        ):
            diagnostics.append(
                "ready project metadata must classify the source as Production/Stable and not Beta"
            )

    evidence_status = repo_root / "qualification-evidence" / "STATUS.md"
    try:
        evidence_text = evidence_status.read_text(encoding="utf-8")
    except OSError as exc:
        diagnostics.append(f"qualification evidence status is unreadable: {exc}")
    else:
        support = contract.get("support", {}) if isinstance(contract, dict) else {}
        release_scope = release.get("scope_classification")
        requires_external = release_scope == "full" or bool(support.get("native_harnesses"))
        if requires_external and (
            "Checked-in real-harness attempts:** 0" in evidence_text
            or "Current empirical PASS:** NONE" in evidence_text
        ):
            diagnostics.append("real external harness evidence is not frozen")

    claims = contract.get("claims", []) if isinstance(contract, dict) else []
    deferred = [
        str(item.get("id"))
        for item in claims
        if item.get("support_required") is True
        and item.get("status") in {"deferred", "not-yet-qualified"}
    ]
    if deferred:
        diagnostics.append("unqualified release claims remain: " + ", ".join(deferred))

    git_head = _git(repo_root, "rev-parse", "HEAD")
    porcelain = _git(repo_root, "status", "--porcelain")
    if git_head is None or porcelain is None:
        diagnostics.append("exact release head cannot be inspected")
    elif porcelain:
        diagnostics.append("exact release head is not clean")

    ci_path = _resolve_path(repo_root, ci_evidence_path, DEFAULT_CI_EVIDENCE)
    owner_path = _resolve_path(
        repo_root, owner_authorization_path, DEFAULT_OWNER_AUTHORIZATION
    )
    digest_path = _resolve_path(
        repo_root, artifact_digests_path, DEFAULT_ARTIFACT_DIGESTS
    )

    _validate_ci_evidence(
        ci_path,
        target=target if isinstance(target, str) else None,
        git_head=git_head,
        diagnostics=diagnostics,
    )
    _validate_owner_authorization(
        owner_path,
        target=target if isinstance(target, str) else None,
        git_head=git_head,
        diagnostics=diagnostics,
    )
    _validate_artifact_digests(
        digest_path,
        source_version=source_version if isinstance(source_version, str) else None,
        diagnostics=diagnostics,
    )

    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument(
        "--ci-evidence",
        type=Path,
        help=(
            "Path to provenance-bound exact-head CI evidence. Defaults to "
            ".release-evidence/ci.yaml below the repository root."
        ),
    )
    parser.add_argument(
        "--owner-authorization",
        type=Path,
        help=(
            "Path to explicit release-owner authorization. Defaults to "
            ".release-evidence/owner-authorization.yaml below the repository root."
        ),
    )
    parser.add_argument(
        "--artifact-digests",
        type=Path,
        help=(
            "Path to SHA-256 records for the final wheel/sdist. Defaults to "
            "dist/SHA256SUMS below the repository root."
        ),
    )
    args = parser.parse_args()

    diagnostics = readiness_diagnostics(
        args.repo_root,
        ci_evidence_path=args.ci_evidence,
        owner_authorization_path=args.owner_authorization,
        artifact_digests_path=args.artifact_digests,
    )
    if diagnostics:
        for item in diagnostics:
            print(f"BLOCKED: {item}")
        return 1
    print("READY: Version 1.0 release gates are complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
