"""Evaluate whether the repository may be called a final Version 1.0 release."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tomllib
from pathlib import Path

import yaml


def readiness_diagnostics(repo_root: Path) -> list[str]:
    """Return deterministic blockers; never convert missing evidence to PASS."""
    diagnostics: list[str] = []
    contract_path = repo_root / "release-v1.0.yaml"
    try:
        contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"cannot read release contract: {exc}"]

    release = contract.get("release", {}) if isinstance(contract, dict) else {}
    if release.get("version") != "1.0.0":
        diagnostics.append("release version is not 1.0.0")
    if release.get("status") != "ready":
        diagnostics.append(f"release status is {release.get('status', 'missing')}")

    pyproject_path = repo_root / "pyproject.toml"
    try:
        pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        diagnostics.append(f"project metadata is unreadable: {exc}")
    else:
        project = pyproject.get("project", {})
        classifiers = project.get("classifiers", [])
        if release.get("version") == "1.0.0" and (
            "Development Status :: 4 - Beta" in classifiers
            or "Development Status :: 5 - Production/Stable" not in classifiers
        ):
            diagnostics.append("project metadata still classifies 1.0.0 as non-stable")

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

    if not (repo_root / "release-owner-authorization.yaml").is_file():
        diagnostics.append("release-owner authorization is missing")
    if not any((repo_root / name).is_file() for name in ("SHA256SUMS", "dist/SHA256SUMS", "artifacts/SHA256SUMS")):
        diagnostics.append("artifact SHA-256 digest record is missing")

    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        diagnostics.append(f"exact release head cannot be inspected: {exc}")
    else:
        if result.returncode != 0 or result.stdout.strip():
            diagnostics.append("exact release head is not clean")

    diagnostics.append("exact release head CI evidence is not recorded")
    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    diagnostics = readiness_diagnostics(args.repo_root.resolve())
    if diagnostics:
        for item in diagnostics:
            print(f"BLOCKED: {item}")
        return 1
    print("READY: Version 1.0 release gates are complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
