#!/usr/bin/env python3
"""Validate mechanically decidable Skill-registry liveness contradictions.

This validator is intentionally narrow. It compares explicit registry liveness
claims with the existence of canonical ``skills/<id>/SKILL.md`` trees. It does
not establish semantic correctness, qualification maturity, or harness support.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


DEFAULT_REGISTRY = Path("skills/workflow-planner/references/skill-registry.yaml")

_NO_IMPLEMENTATION_PATTERNS = (
    re.compile(r"\bno\s+current\s+implementation(?:\s+yet)?\b", re.IGNORECASE),
    re.compile(r"\bno\s+current\s+skill\s+implementation(?:\s+yet)?\b", re.IGNORECASE),
    re.compile(
        r"\bno\s+implementation\s+under\s+[`'\"]?skills/?[`'\"]?",
        re.IGNORECASE,
    ),
)
_CURRENT_PATH_RE = re.compile(
    r"current\s+canonical\s+implementation\s+lives\s+under\s+"
    r"[`'\"]?(skills/[A-Za-z0-9_.-]+/)",
    re.IGNORECASE,
)


def _error(
    error_id: str,
    *,
    skill_id: str | None,
    field: str,
    current_value: Any,
    message: str,
) -> dict[str, Any]:
    return {
        "error_id": error_id,
        "skill_id": skill_id,
        "field": field,
        "current_value": current_value,
        "message": message,
    }


def _load_registry(path: Path) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    if not path.is_file():
        return None, [
            _error(
                "SKILL_REGISTRY_NOT_FOUND",
                skill_id=None,
                field="registry",
                current_value=str(path),
                message="Skill registry file does not exist.",
            )
        ]

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - exact parser wording is dependency-specific
        return None, [
            _error(
                "SKILL_REGISTRY_INVALID_YAML",
                skill_id=None,
                field="registry",
                current_value=str(path),
                message=f"Skill registry YAML could not be parsed: {exc}",
            )
        ]

    if not isinstance(raw, dict) or not isinstance(raw.get("ecosystems"), dict):
        return None, [
            _error(
                "SKILL_REGISTRY_INVALID_SHAPE",
                skill_id=None,
                field="ecosystems",
                current_value=None if not isinstance(raw, dict) else raw.get("ecosystems"),
                message="Skill registry must contain an ecosystems mapping.",
            )
        ]

    return raw, []


def validate_skill_registry_liveness(
    *, repo_root: Path, registry_path: Path
) -> dict[str, Any]:
    registry, errors = _load_registry(registry_path)
    if registry is None:
        return {
            "valid": False,
            "validator": "validate-skill-registry-liveness.py",
            "registry": str(registry_path),
            "checks": ["canonical_skill_tree_vs_registry_liveness_claim"],
            "errors": errors,
            "semantic_truth_established": False,
        }

    seen_ids: set[str] = set()

    for ecosystem_id, ecosystem in registry["ecosystems"].items():
        if not isinstance(ecosystem, dict):
            errors.append(
                _error(
                    "SKILL_REGISTRY_INVALID_ECOSYSTEM",
                    skill_id=None,
                    field=f"ecosystems.{ecosystem_id}",
                    current_value=ecosystem,
                    message="Ecosystem entry must be a mapping.",
                )
            )
            continue

        skills = ecosystem.get("skills", [])
        if not isinstance(skills, list):
            errors.append(
                _error(
                    "SKILL_REGISTRY_INVALID_SKILLS_LIST",
                    skill_id=None,
                    field=f"ecosystems.{ecosystem_id}.skills",
                    current_value=skills,
                    message="Ecosystem skills must be a list.",
                )
            )
            continue

        for index, skill in enumerate(skills):
            if not isinstance(skill, dict):
                errors.append(
                    _error(
                        "SKILL_REGISTRY_INVALID_SKILL_ENTRY",
                        skill_id=None,
                        field=f"ecosystems.{ecosystem_id}.skills[{index}]",
                        current_value=skill,
                        message="Skill entry must be a mapping.",
                    )
                )
                continue

            skill_id = skill.get("id")
            if not isinstance(skill_id, str) or not skill_id.strip():
                errors.append(
                    _error(
                        "SKILL_REGISTRY_MISSING_ID",
                        skill_id=None,
                        field=f"ecosystems.{ecosystem_id}.skills[{index}].id",
                        current_value=skill_id,
                        message="Skill entry must declare a non-empty string id.",
                    )
                )
                continue
            skill_id = skill_id.strip()

            if skill_id in seen_ids:
                errors.append(
                    _error(
                        "SKILL_REGISTRY_DUPLICATE_ID",
                        skill_id=skill_id,
                        field="id",
                        current_value=skill_id,
                        message="Skill id appears more than once in the registry.",
                    )
                )
            seen_ids.add(skill_id)

            canonical_skill = repo_root / "skills" / skill_id / "SKILL.md"
            canonical_exists = canonical_skill.is_file()
            status = skill.get("status")
            status_note = skill.get("status_note", "")

            if status_note is None:
                status_note = ""
            if not isinstance(status_note, str):
                errors.append(
                    _error(
                        "SKILL_REGISTRY_INVALID_STATUS_NOTE",
                        skill_id=skill_id,
                        field="status_note",
                        current_value=status_note,
                        message="status_note must be text when present.",
                    )
                )
                continue

            if status == "proposed" and canonical_exists:
                errors.append(
                    _error(
                        "SKILL_REGISTRY_STALE_PROPOSED_STATUS",
                        skill_id=skill_id,
                        field="status",
                        current_value=status,
                        message=(
                            f"Registry marks {skill_id!r} proposed while canonical "
                            f"{canonical_skill.relative_to(repo_root)} exists."
                        ),
                    )
                )

            if canonical_exists and any(
                pattern.search(status_note) for pattern in _NO_IMPLEMENTATION_PATTERNS
            ):
                errors.append(
                    _error(
                        "SKILL_REGISTRY_STALE_ABSENCE_NOTE",
                        skill_id=skill_id,
                        field="status_note",
                        current_value=status_note,
                        message=(
                            f"Registry note claims no current implementation for {skill_id!r} "
                            f"while {canonical_skill.relative_to(repo_root)} exists."
                        ),
                    )
                )

            for referenced_path in _CURRENT_PATH_RE.findall(status_note):
                expected_path = f"skills/{skill_id}/"
                if referenced_path != expected_path:
                    errors.append(
                        _error(
                            "SKILL_REGISTRY_MISMATCHED_CURRENT_PATH",
                            skill_id=skill_id,
                            field="status_note",
                            current_value=referenced_path,
                            message=(
                                f"Registry note for {skill_id!r} points to {referenced_path!r} "
                                f"instead of {expected_path!r}."
                            ),
                        )
                    )

                referenced_skill = repo_root / referenced_path / "SKILL.md"
                if not referenced_skill.is_file():
                    errors.append(
                        _error(
                            "SKILL_REGISTRY_BROKEN_CURRENT_PATH",
                            skill_id=skill_id,
                            field="status_note",
                            current_value=referenced_path,
                            message=(
                                f"Registry note identifies {referenced_path!r} as the current "
                                "canonical implementation, but its SKILL.md is missing."
                            ),
                        )
                    )

    return {
        "valid": not errors,
        "validator": "validate-skill-registry-liveness.py",
        "registry": str(registry_path),
        "checks": ["canonical_skill_tree_vs_registry_liveness_claim"],
        "errors": errors,
        "semantic_truth_established": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reject mechanically contradictory Skill-registry liveness claims."
    )
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument(
        "--registry",
        default=str(DEFAULT_REGISTRY),
        help="Registry path, absolute or relative to --repo-root",
    )
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    registry_arg = Path(args.registry)
    registry_path = (
        registry_arg.resolve()
        if registry_arg.is_absolute()
        else (repo_root / registry_arg).resolve()
    )

    result = validate_skill_registry_liveness(
        repo_root=repo_root, registry_path=registry_path
    )

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    elif result["valid"]:
        print("SKILL_REGISTRY_LIVENESS_VALID")
    else:
        for error in result["errors"]:
            print(f"ERROR {error['error_id']}: {error['message']}")

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
