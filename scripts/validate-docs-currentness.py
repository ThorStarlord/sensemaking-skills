"""Validate the small set of documents that define current release guidance."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

import yaml


CURRENT_DOCS = (
    "README.md",
    "GETTING_STARTED.md",
    "INSTALLATION.md",
    "STATUS.md",
    "docs/operations-runbook.md",
    "docs/PUBLISHING.md",
    "docs/public-surface-v1.0.md",
    "docs/maintainer-guide-v1.0.md",
    "docs/release-v1.0-contract.md",
    "docs/release-v1.0-checklist.md",
)

SOURCE_IDENTITY_DOCS = (
    "README.md",
    "GETTING_STARTED.md",
    "INSTALLATION.md",
    "STATUS.md",
    "docs/operations-runbook.md",
    "docs/maintainer-guide-v1.0.md",
)

TARGET_IDENTITY_DOCS = (
    "README.md",
    "STATUS.md",
    "docs/PUBLISHING.md",
    "docs/public-surface-v1.0.md",
    "docs/maintainer-guide-v1.0.md",
    "docs/release-v1.0-contract.md",
    "docs/release-v1.0-checklist.md",
)

STALE_CURRENT_PHRASES = (
    "sensemaking-skills==0.3.0",
    "Current package version: `0.3.0`",
    "**Version:** 1.0.0rc1",
    "Getting Started with Sensemaking Skills v0.3.0",
    "Publishing Sensemaking Skills v0.3.0",
    "installed v0.3 package",
)


def _release_identity(repo_root: Path) -> tuple[str, str, str]:
    pyproject = tomllib.loads(
        (repo_root / "pyproject.toml").read_text(encoding="utf-8")
    )
    contract = yaml.safe_load(
        (repo_root / "release-v1.0.yaml").read_text(encoding="utf-8")
    )
    source_version = pyproject["project"]["version"]
    target_version = contract["release"]["version"]
    status = contract["release"]["status"]
    return source_version, target_version, status


def validate_docs_currentness(repo_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        source_version, target_version, status = _release_identity(repo_root)
    except (
        OSError,
        KeyError,
        TypeError,
        tomllib.TOMLDecodeError,
        yaml.YAMLError,
    ) as exc:
        return [f"cannot resolve release identity: {exc}"]

    texts: dict[str, str] = {}
    for relative in CURRENT_DOCS:
        path = repo_root / relative
        if not path.is_file():
            errors.append(f"current document is missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        texts[relative] = text
        if "release-v1.0-contract.md" not in text and relative != "docs/release-v1.0-contract.md":
            errors.append(f"current document does not link release contract: {relative}")
        if "native-harness qualification: COMPLETE" in text:
            errors.append(f"current document overclaims native qualification: {relative}")
        if "portability qualification: COMPLETE" in text:
            errors.append(f"current document overclaims portability qualification: {relative}")
        for stale in STALE_CURRENT_PHRASES:
            if stale in text:
                errors.append(
                    f"current document contains stale release identity {stale!r}: {relative}"
                )

    for relative in SOURCE_IDENTITY_DOCS:
        text = texts.get(relative)
        if text is not None and source_version not in text:
            errors.append(
                f"current document omits source version {source_version}: {relative}"
            )

    for relative in TARGET_IDENTITY_DOCS:
        text = texts.get(relative)
        if text is not None and target_version not in text:
            errors.append(
                f"current document omits release target {target_version}: {relative}"
            )

    if status == "development":
        frozen_claim = f"**Version:** {target_version} (reduced-scope release candidate)"
        for relative, text in texts.items():
            if frozen_claim in text:
                errors.append(
                    f"development source is presented as frozen candidate in {relative}"
                )

    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate_docs_currentness(args.repo_root.resolve())
    if errors:
        print(f"FAIL: {len(errors)} documentation-currentness error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"current documents validated: {len(CURRENT_DOCS)}")
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
