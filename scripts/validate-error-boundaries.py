"""Reject silent broad exception handlers in the shipped product surface."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


PRODUCT_ROOTS = (
    "campaign_semantics",
    "campaigns",
    "commands",
    "defaults",
    "reasoning",
    "semantic_architecture",
    "skills",
)


def validate(repo_root: Path) -> list[str]:
    """Return diagnostics for bare or silently swallowed product exceptions."""
    errors: list[str] = []
    source_root = repo_root / "src" / "sensemaking_skills"
    paths = [source_root / "cli.py", source_root / "setup_skills.py"]
    for name in PRODUCT_ROOTS:
        paths.extend(source_root.joinpath(name).rglob("*.py"))
    for path in paths:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, SyntaxError) as exc:
            errors.append(f"cannot inspect {path}: {exc}")
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ExceptHandler):
                continue
            is_broad = node.type is None or (
                isinstance(node.type, ast.Name) and node.type.id == "Exception"
            )
            if not is_broad:
                continue
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                errors.append(f"silent broad exception handler: {path}:{node.lineno}")
    return sorted(set(errors))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("ERROR_BOUNDARIES_VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())
