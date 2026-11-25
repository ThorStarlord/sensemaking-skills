"""Bounded verification scenario candidates from a Python symbol's guards.

This module turns direct ``raise`` and ``assert`` guards into reviewable
scenario candidates. It does not generate executable tests, prove reachability,
or establish coverage, correctness or expected behavior.
"""

from __future__ import annotations

import ast
from typing import Any, Iterable

_MAX_LIMIT = 50
_MAX_REQUESTED = 250
_LIMITS = (
    "Direct raise/assert guards only; helper validation, decorators, nested functions, "
    "runtime dispatch and exception behavior are NOT ASSESSED.",
    "Suggested inputs are heuristic boundary hints from literal comparisons, not proven "
    "counterexamples, test cases or reachable states.",
    "Conditions may depend on local variables, imports or state that the signature does not expose.",
    "A scenario candidate is not test coverage, pass status, semantic correctness or change authorization.",
)


def _exception_name(exc: ast.AST | None) -> str:
    if exc is None:
        return "bare raise"
    if isinstance(exc, ast.Call):
        return ast.unparse(exc.func)
    return ast.unparse(exc)


def _ancestor_conditions(
    node: ast.AST, parents: dict[ast.AST, ast.AST], root: ast.AST,
) -> list[ast.AST] | None:
    conditions: list[ast.AST] = []
    current = parents.get(node)
    while current is not None and current is not root:
        if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            return None
        if isinstance(current, ast.If):
            conditions.append(current.test)
        current = parents.get(current)
    return list(reversed(conditions))


def _boundary_hints(
    tests: Iterable[ast.AST], parameters: set[str], module_constants: dict[str, int],
) -> tuple[list[str], str]:
    hints: set[str] = set()
    for test in tests:
        for node in ast.walk(test):
            if not isinstance(node, ast.Compare):
                continue
            sides = [node.left, *node.comparators]
            names = [side.id for side in sides if isinstance(side, ast.Name) and side.id in parameters]
            constants: list[int] = []
            for side in sides:
                if isinstance(side, ast.Constant) and isinstance(side.value, int) and not isinstance(side.value, bool):
                    constants.append(side.value)
                elif isinstance(side, ast.Name) and side.id in module_constants:
                    constants.append(module_constants[side.id])
            for name in names:
                for value in constants:
                    for candidate in (value - 1, value, value + 1):
                        hints.add(f"{name}={candidate}")
    ordered = sorted(hints, key=lambda item: (item.split("=")[0], int(item.split("=")[1])))
    return ordered[:8], "BOUNDARY_CONSTANTS" if ordered else "NOT_ASSESSED"


def build_verification_scenarios(
    tree: ast.AST, source: str, path: str, symbol: str, *, limit: int = 50,
) -> dict[str, Any]:
    """Return direct guard-derived scenario candidates for one top-level symbol."""

    if not 1 <= limit <= _MAX_REQUESTED:
        raise ValueError("verification scenario limit must be 1..250")
    effective_limit = min(limit, _MAX_LIMIT)
    definitions = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and node.name == symbol
    ]
    module_constants = {
        node.targets[0].id: node.value.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, int)
        and not isinstance(node.value.value, bool)
    }
    if not definitions:
        return {
            "symbol": symbol,
            "definitions": [],
            "scenarios": [],
            "counts": {"guards": 0, "scenarios": 0, "with_input_hints": 0},
            "coverage_status": "NOT_ASSESSED",
            "truncated": False,
            "limits": list(_LIMITS),
        }
    if any(isinstance(node, ast.ClassDef) for node in definitions):
        return {
            "symbol": symbol,
            "definitions": [{"line": node.lineno, "kind": "class"} for node in definitions],
            "scenarios": [],
            "counts": {"guards": 0, "scenarios": 0, "with_input_hints": 0},
            "coverage_status": "NOT_ASSESSED",
            "truncated": False,
            "limits": [
                *_LIMITS,
                "Class definitions are not expanded into methods; select a function/method symbol.",
            ],
        }

    parents: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    scenarios: list[dict[str, Any]] = []
    guards = 0
    with_hints = 0
    for definition in definitions:
        parameters = {
            arg.arg for arg in (
                definition.args.posonlyargs + definition.args.args + definition.args.kwonlyargs
            )
        }
        for node in ast.walk(definition):
            if not isinstance(node, (ast.Raise, ast.Assert)):
                continue
            if isinstance(node, ast.Raise):
                conditions = _ancestor_conditions(node, parents, definition)
                if conditions is None:
                    continue
                expected = _exception_name(node.exc)
                kind = "RAISE"
            else:
                conditions = _ancestor_conditions(node, parents, definition)
                if conditions is None:
                    continue
                expected = "AssertionError"
                kind = "ASSERT"
            guards += 1
            hints, hint_basis = _boundary_hints(conditions, parameters, module_constants)
            if hints:
                with_hints += 1
            condition = " and ".join(ast.unparse(test) for test in conditions) or "unconditional"
            if len(scenarios) < effective_limit:
                scenarios.append({
                    "kind": kind,
                    "condition": condition[:500],
                    "expected": expected,
                    "suggested_inputs": hints,
                    "input_hint_basis": hint_basis,
                    "line": node.lineno,
                    "definition_line": definition.lineno,
                    "evidence_ref": f"file:{path}:{node.lineno}",
                })
    truncated = guards > len(scenarios)
    return {
        "symbol": symbol,
        "definitions": [
            {"line": node.lineno, "kind": "function"} for node in definitions
        ],
        "scenarios": scenarios,
        "counts": {
            "guards": guards,
            "scenarios": len(scenarios),
            "with_input_hints": with_hints,
        },
        "coverage_status": "PARTIAL" if truncated else "COMPLETE_FOR_DIRECT_GUARDS",
        "truncated": truncated,
        "limits": list(_LIMITS),
    }
