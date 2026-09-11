#!/usr/bin/env python3
"""Validate mechanical authority markers for strategic candidate directions.

This validator checks only representation boundaries that keep the idea reservoir
non-authoritative. It does not judge candidate quality, priority, evidence, or
whether any idea should enter the Strategic Frontier.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CANDIDATE_PATH = Path("docs/strategic-candidate-directions.md")
REQUIRED_MARKERS = (
    "**Status:** exploratory / non-authoritative idea reservoir",
    "**Authority:** none; candidate ideas do not constitute Strategic Frontier membership",
    "**Current strategy authority:** [`product-strategy.md`](product-strategy.md)",
    "**Current Level-3 state:** [`../STATUS.md`](../STATUS.md)",
    "**Control model:** [`strategic-outer-loop.md`](strategic-outer-loop.md)",
    "possible direction\n!= Strategic Frontier item\n!= warranted repository responsibility\n!= authorized Campaign/work package\n!= implementation commitment",
    "## 13. Current priority statement",
    "This document intentionally declares **no current implementation priority**.",
    "Use this reservoir to remember possibilities. Use Level 3 to decide whether any possibility has become consequential enough to act on.",
)


def validate_candidate_directions(repo_root: Path) -> list[dict[str, str]]:
    path = repo_root / CANDIDATE_PATH
    diagnostics: list[dict[str, str]] = []
    if not path.is_file():
        return [
            {
                "code": "CANDIDATE_DIRECTIONS_MISSING",
                "detail": str(CANDIDATE_PATH),
            }
        ]
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [
            {
                "code": "CANDIDATE_DIRECTIONS_READ_FAILED",
                "detail": str(exc),
            }
        ]
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            diagnostics.append(
                {
                    "code": "CANDIDATE_DIRECTIONS_AUTHORITY_MARKER_MISSING",
                    "detail": marker.splitlines()[0],
                }
            )
    return diagnostics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    diagnostics = validate_candidate_directions(root)
    payload = {
        "ok": not diagnostics,
        "code": (
            "CANDIDATE_DIRECTIONS_CONTRACT_VALID"
            if not diagnostics
            else "CANDIDATE_DIRECTIONS_CONTRACT_INVALID"
        ),
        "path": str(CANDIDATE_PATH),
        "diagnostics": diagnostics,
        "semantic_priority_established": False,
        "implementation_authority_established": False,
    }
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        print(payload["code"])
        for diagnostic in diagnostics:
            print(f"{diagnostic['code']}: {diagnostic['detail']}")
    return 0 if not diagnostics else 3


if __name__ == "__main__":
    raise SystemExit(main())
