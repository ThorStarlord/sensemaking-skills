"""Validate the small set of documents that define current release guidance."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


CURRENT_DOCS = (
    "README.md",
    "GETTING_STARTED.md",
    "INSTALLATION.md",
    "STATUS.md",
    "docs/public-surface-v1.0.md",
    "docs/maintainer-guide-v1.0.md",
    "docs/release-v1.0-checklist.md",
)


def validate_docs_currentness(repo_root: Path) -> list[str]:
    errors: list[str] = []
    for relative in CURRENT_DOCS:
        path = repo_root / relative
        if not path.is_file():
            errors.append(f"current document is missing: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        if "release-v1.0-contract.md" not in text:
            errors.append(f"current document does not link release contract: {relative}")
        if "native-harness qualification: COMPLETE" in text:
            errors.append(f"current document overclaims native qualification: {relative}")
        if "portability qualification: COMPLETE" in text:
            errors.append(f"current document overclaims portability qualification: {relative}")
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
