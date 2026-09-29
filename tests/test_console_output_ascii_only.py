"""Guard: print() output in src/ and scripts/ must be ASCII-only.

The codebase runs on Windows (cp1252); non-ASCII characters in stdout crash
the process (see CLAUDE.md, "Console output is ASCII-only").
"""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ("src", "scripts")


def _non_ascii_print_calls():
    offenders = []
    for scan_dir in SCAN_DIRS:
        for path in sorted((ROOT / scan_dir).rglob("*.py")):
            if "egg-info" in path.parts[-3:] or any(
                p.endswith(".egg-info") for p in path.parts
            ):
                continue
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if not (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id == "print"
                ):
                    continue
                for child in ast.walk(node):
                    if (
                        isinstance(child, ast.Constant)
                        and isinstance(child.value, str)
                        and not child.value.isascii()
                    ):
                        offenders.append(f"{path.relative_to(ROOT)}:{node.lineno}")
                        break
    return offenders


def test_print_calls_are_ascii_only():
    offenders = _non_ascii_print_calls()
    assert not offenders, (
        "Non-ASCII characters in print() calls (use ASCII, e.g. '->'): "
        + ", ".join(offenders)
    )
