#!/usr/bin/env python3
"""Validate the mechanically decidable Level-3 strategic-state contract.

This validator is intentionally narrow. It validates repository-local
representation integrity for the current ``STATUS.md`` authority surface. It
does not establish strategy quality, currentness relative to remote systems,
frontier priority, responsibility warrant, or semantic truth.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


DEFAULT_STATUS = Path("STATUS.md")

REQUIRED_SURFACES = (
    Path("docs/product-strategy.md"),
    Path("docs/strategic-outer-loop.md"),
    Path("docs/strategic-state-contract.md"),
    Path("docs/product-thesis-revision.md"),
)

REQUIRED_HEADINGS = (
    "## Strategic Repository Evolution state — Level 3",
    "### Current product strategy",
    "### Current capability state",
    "### Material limitations and evidence ceilings",
    "### Strategic Frontier",
    "### Current highest-leverage boundary",
    "### Current decision-changing uncertainty",
    "### Current warranted repository-level responsibility",
    "### Authority / owner direction",
    "### Thesis review state",
    "## Current next step",
)

CANONICAL_POINTERS = {
    "Level-4 authority": "docs/product-strategy.md",
    "Control model": "docs/strategic-outer-loop.md",
    "Level-3 contract": "docs/strategic-state-contract.md",
    "Level-4 revision contract": "docs/product-thesis-revision.md",
}

CHECKS = (
    "required_authority_surfaces",
    "required_level3_section_anchors",
    "canonical_authority_pointers",
    "thesis_review_marker_shape",
    "strategic_frontier_identity_uniqueness",
)

_FRONTIER_ITEM_RE = re.compile(
    r"^\s*\d+\.\s+\*\*(?P<name>.+?)\s+(?:—|–|-)\s+(?P<disposition>.+?)\.\*\*",
    re.MULTILINE,
)
_THESIS_TOKEN_RE = re.compile(r"\bTHESIS_REVIEW_REQUIRED\b")
_THESIS_VALUE_RE = re.compile(
    r"^\s*`?THESIS_REVIEW_REQUIRED`?\s*:\s*"
    r"(?:\*\*)?\s*`?(?P<value>[A-Za-z0-9_-]+)`?\s*(?:\*\*)?",
    re.MULTILINE,
)


def _error(
    error_id: str,
    *,
    field: str,
    current_value: Any,
    message: str,
) -> dict[str, Any]:
    return {
        "error_id": error_id,
        "field": field,
        "current_value": current_value,
        "message": message,
    }


def _heading_level(line: str) -> int | None:
    match = re.match(r"^(#+)\s+", line)
    return len(match.group(1)) if match else None


def _extract_section(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    matches = [index for index, line in enumerate(lines) if line.strip() == heading]
    if len(matches) != 1:
        return None

    start = matches[0]
    level = _heading_level(lines[start])
    if level is None:
        return None

    end = len(lines)
    for index in range(start + 1, len(lines)):
        candidate_level = _heading_level(lines[index])
        if candidate_level is not None and candidate_level <= level:
            end = index
            break

    return "\n".join(lines[start + 1 : end])


def _normalize_frontier_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value)
    return re.sub(r"\s+", " ", normalized).strip().casefold()


def validate_strategic_state(*, repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    status_path = repo_root / DEFAULT_STATUS
    errors: list[dict[str, Any]] = []

    if not status_path.is_file():
        errors.append(
            _error(
                "STRATEGIC_STATE_STATUS_NOT_FOUND",
                field="status_file",
                current_value=str(DEFAULT_STATUS),
                message="Level-3 strategic state file STATUS.md does not exist.",
            )
        )

    for relative_path in REQUIRED_SURFACES:
        candidate = repo_root / relative_path
        if not candidate.is_file():
            errors.append(
                _error(
                    "STRATEGIC_STATE_REQUIRED_SURFACE_MISSING",
                    field="authority_surface",
                    current_value=relative_path.as_posix(),
                    message=(
                        "Required strategic authority surface does not exist: "
                        f"{relative_path.as_posix()}."
                    ),
                )
            )

    if not status_path.is_file():
        return {
            "valid": False,
            "validator": "validate-strategic-state.py",
            "status_file": DEFAULT_STATUS.as_posix(),
            "checks": list(CHECKS),
            "errors": errors,
            "semantic_truth_established": False,
        }

    text = status_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    for heading in REQUIRED_HEADINGS:
        count = sum(1 for line in lines if line.strip() == heading)
        if count == 0:
            errors.append(
                _error(
                    "STRATEGIC_STATE_SECTION_MISSING",
                    field="section",
                    current_value=heading,
                    message=f"Required Level-3 section anchor is missing: {heading}",
                )
            )
        elif count > 1:
            errors.append(
                _error(
                    "STRATEGIC_STATE_SECTION_DUPLICATE",
                    field="section",
                    current_value={"heading": heading, "count": count},
                    message=(
                        "Required Level-3 section anchor must occur exactly once: "
                        f"{heading} (found {count})."
                    ),
                )
            )

    strategy_section = _extract_section(text, "### Current product strategy")
    if strategy_section is not None:
        for label, expected_path in CANONICAL_POINTERS.items():
            pointer_re = re.compile(
                rf"^\s*-\s+\*\*{re.escape(label)}:\*\*\s+`([^`]+)`\.?\s*$",
                re.MULTILINE,
            )
            values = pointer_re.findall(strategy_section)
            if not values:
                errors.append(
                    _error(
                        "STRATEGIC_STATE_POINTER_MISSING",
                        field=label,
                        current_value=None,
                        message=(
                            f"Current product strategy must declare canonical pointer "
                            f"{label!r} -> {expected_path!r}."
                        ),
                    )
                )
                continue
            if len(values) > 1:
                errors.append(
                    _error(
                        "STRATEGIC_STATE_POINTER_DUPLICATE",
                        field=label,
                        current_value=values,
                        message=(
                            f"Canonical pointer {label!r} must occur exactly once "
                            f"(found {len(values)})."
                        ),
                    )
                )
                continue

            actual_path = values[0]
            if actual_path != expected_path:
                errors.append(
                    _error(
                        "STRATEGIC_STATE_POINTER_MISMATCH",
                        field=label,
                        current_value=actual_path,
                        message=(
                            f"Canonical pointer {label!r} must target {expected_path!r}, "
                            f"not {actual_path!r}."
                        ),
                    )
                )
                continue

            if not (repo_root / actual_path).is_file():
                errors.append(
                    _error(
                        "STRATEGIC_STATE_POINTER_BROKEN",
                        field=label,
                        current_value=actual_path,
                        message=(
                            f"Canonical pointer {label!r} targets missing repository file "
                            f"{actual_path!r}."
                        ),
                    )
                )

    thesis_section = _extract_section(text, "### Thesis review state")
    if thesis_section is not None:
        token_count = len(_THESIS_TOKEN_RE.findall(thesis_section))
        if token_count == 0:
            errors.append(
                _error(
                    "STRATEGIC_STATE_THESIS_REVIEW_MISSING",
                    field="THESIS_REVIEW_REQUIRED",
                    current_value=None,
                    message=(
                        "Thesis review state must contain exactly one "
                        "THESIS_REVIEW_REQUIRED marker."
                    ),
                )
            )
        elif token_count > 1:
            errors.append(
                _error(
                    "STRATEGIC_STATE_THESIS_REVIEW_DUPLICATE",
                    field="THESIS_REVIEW_REQUIRED",
                    current_value=token_count,
                    message=(
                        "Thesis review state contains more than one "
                        f"THESIS_REVIEW_REQUIRED marker ({token_count})."
                    ),
                )
            )
        else:
            match = _THESIS_VALUE_RE.search(thesis_section)
            value = match.group("value").upper() if match else None
            if value not in {"YES", "NO"}:
                errors.append(
                    _error(
                        "STRATEGIC_STATE_THESIS_REVIEW_INVALID",
                        field="THESIS_REVIEW_REQUIRED",
                        current_value=value,
                        message=(
                            "THESIS_REVIEW_REQUIRED must use the mechanical literal "
                            "YES or NO."
                        ),
                    )
                )

    frontier_section = _extract_section(text, "### Strategic Frontier")
    if frontier_section is not None:
        seen: dict[str, tuple[str, str]] = {}
        for match in _FRONTIER_ITEM_RE.finditer(frontier_section):
            name = match.group("name").strip()
            disposition = match.group("disposition").strip()
            normalized = _normalize_frontier_name(name)
            if normalized in seen:
                prior_name, prior_disposition = seen[normalized]
                errors.append(
                    _error(
                        "STRATEGIC_STATE_FRONTIER_DUPLICATE_ITEM",
                        field="Strategic Frontier",
                        current_value={
                            "name": name,
                            "dispositions": [prior_disposition, disposition],
                        },
                        message=(
                            "Strategic Frontier declares the same normalized item more "
                            f"than once: {prior_name!r} / {name!r}."
                        ),
                    )
                )
            else:
                seen[normalized] = (name, disposition)

    return {
        "valid": not errors,
        "validator": "validate-strategic-state.py",
        "status_file": DEFAULT_STATUS.as_posix(),
        "checks": list(CHECKS),
        "errors": errors,
        "semantic_truth_established": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the repository-local mechanical representation contract of "
            "the Level-3 strategic state."
        )
    )
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    args = parser.parse_args()

    result = validate_strategic_state(repo_root=Path(args.repo_root))

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    elif result["valid"]:
        print("STRATEGIC_STATE_VALID")
    else:
        for error in result["errors"]:
            print(f"ERROR {error['error_id']}: {error['message']}")

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
