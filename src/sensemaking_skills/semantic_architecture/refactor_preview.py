"""Preview a fail-closed rename patch for one top-level Python symbol.

This module reads exactly one committed Git revision, computes direct syntactic
renames across tracked Python files, emits a unified patch and verifies that
patch in a disposable checkout. It never edits the active checkout and does not
establish runtime completeness: dynamic dispatch, string registries, generated
code and non-Python consumers are reported as unresolved or explicitly not
assessed.
"""

from __future__ import annotations

import ast
import copy
import difflib
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable

from .knowledge_sources import _source, temporary_commit_checkout, verified_tracked_sources
from .source_relationships import (
    _import_bindings,
    _import_from_base,
    _module_for_path,
    _parse,
    _reference_nodes,
    _safe_path,
)

_MAX_EDITS = 250
_MAX_SITES = 50
_SYMBOL = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_LIMITS = (
    "Only top-level Python functions and classes are rename targets; module-level variables, methods and nested definitions are NOT SUPPORTED.",
    "Only direct syntactic name, attribute and import references are rewritten. getattr strings, dynamic imports, generated code, inheritance, re-exports and runtime dispatch are NOT ASSESSED.",
    "Exact string constants equal to the symbol in related Python files block the patch because they may be dynamic references.",
    "Attribute access with the same name on non-module objects is listed but not rewritten; it may belong to a different symbol.",
    "Non-Python files are not modified; mentions are sampled from contained readable text files only. Symlinks, unreadable, binary and oversized files are not assessed.",
    "A READY patch is not proof of runtime correctness, test coverage, API compatibility or complete repository-wide renaming.",
)
_IGNORED_AST_FIELDS = {
    "lineno", "col_offset", "end_lineno", "end_col_offset", "type_comment",
}


def _definition_name_column(node: ast.AST) -> int:
    if isinstance(node, ast.AsyncFunctionDef):
        return node.col_offset + len("async def ")
    if isinstance(node, ast.FunctionDef):
        return node.col_offset + len("def ")
    if isinstance(node, ast.ClassDef):
        return node.col_offset + len("class ")
    raise ValueError("unsupported definition node")


def _line_span(node: ast.AST, lines: list[str]) -> tuple[int, int, int]:
    """Return (line, start, end) for the identifier this edit replaces."""

    line_number = getattr(node, "lineno", None)
    if line_number is None:
        raise ValueError("identifier edit has no source line")
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        if getattr(node, "end_lineno", None) != line_number:
            raise ValueError("identifier edit must stay on one line")
    text = lines[line_number - 1]
    if isinstance(node, ast.Name):
        start, end = node.col_offset, node.col_offset + len(node.id)
        expected = node.id
    elif isinstance(node, ast.Attribute):
        start, end = node.end_col_offset - len(node.attr), node.end_col_offset
        expected = node.attr
    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        start = _definition_name_column(node)
        end = start + len(node.name)
        expected = node.name
    elif isinstance(node, ast.alias):
        start = node.col_offset
        end = start + len(node.name)
        expected = node.name
    elif isinstance(node, ast.Constant) and isinstance(node.value, str):
        literal = text[node.col_offset:node.end_col_offset]
        offset = literal.find(node.value)
        if offset < 0:
            raise ValueError("string literal does not contain its value")
        start = node.col_offset + offset
        end = start + len(node.value)
        expected = node.value
    else:
        raise ValueError(f"unsupported edit node: {type(node).__name__}")
    if text[start:end] != expected:
        raise ValueError(
            f"source span mismatch at line {line_number}: expected {expected!r}, found {text[start:end]!r}"
        )
    return line_number, start, end


def _pair_nodes(original: ast.AST, duplicate: ast.AST, mapping: dict[int, ast.AST]) -> None:
    mapping[id(original)] = duplicate
    for left, right in zip(ast.iter_child_nodes(original), ast.iter_child_nodes(duplicate)):
        _pair_nodes(left, right, mapping)


def _binding_sites(tree: ast.AST, name: str, *, module_level_only: bool = False) -> list[tuple[int, int, str]]:
    """Return syntactic binding sites for one name."""

    sites: list[tuple[int, int, str]] = []
    nodes: Iterable[ast.AST]
    if module_level_only:
        nodes = _module_scope_nodes(tree)
    else:
        nodes = ast.walk(tree)
    for node in nodes:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name == name:
                sites.append((node.lineno, _definition_name_column(node), "definition"))
        elif isinstance(node, ast.arg) and node.arg == name:
            sites.append((node.lineno, node.col_offset, "parameter"))
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                if alias.name == "*":
                    continue
                bound = alias.asname or (
                    alias.name.split(".")[0] if isinstance(node, ast.Import) else alias.name
                )
                if bound == name:
                    sites.append((alias.lineno or node.lineno, alias.col_offset or 0, "import"))
        elif isinstance(node, ast.Name) and node.id == name and isinstance(node.ctx, (ast.Store, ast.Del)):
            sites.append((node.lineno, node.col_offset, "assignment"))
        elif isinstance(node, ast.ExceptHandler) and node.name == name:
            sites.append((node.lineno, node.col_offset, "except"))
        elif isinstance(node, (ast.Global, ast.Nonlocal)) and name in node.names:
            sites.append((node.lineno, node.col_offset, "declaration"))
    return sites


def _module_scope_nodes(tree: ast.AST) -> Iterable[ast.AST]:
    """Walk module-level control flow without entering functions or classes."""

    stack = list(ast.iter_child_nodes(tree))
    while stack:
        child = stack.pop()
        yield child
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            continue
        stack.extend(ast.iter_child_nodes(child))


def _docstring_ids(tree: ast.AST) -> set[int]:
    ids: set[int] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if not node.body:
            continue
        first = node.body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
            ids.add(id(first.value))
    return ids


def _module_all_nodes(tree: ast.AST, symbol: str) -> list[ast.Constant]:
    found: list[ast.Constant] = []
    for node in tree.body:
        value: ast.AST | None = None
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
                value = node.value
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                value = node.value
        if value is None:
            continue
        if not isinstance(value, (ast.List, ast.Tuple, ast.Set)):
            continue
        for element in value.elts:
            if isinstance(element, ast.Constant) and element.value == symbol:
                found.append(element)
    return found


def _dynamic_all(tree: ast.AST) -> int | None:
    for node in tree.body:
        value: ast.AST | None = None
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
                value = node.value
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                value = node.value
        if value is not None and not isinstance(value, (ast.List, ast.Tuple, ast.Set)):
            return node.lineno
    return None


def _dynamic_references(
    tree: ast.AST, symbol: str, target_module: str, module_aliases: set[str],
) -> list[tuple[int, str, str]]:
    """Return call sites that could reference the symbol dynamically."""

    found: list[tuple[int, str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = ast.unparse(node.func)
            if name in {"getattr", "setattr", "delattr", "hasattr"} and len(node.args) >= 2:
                attribute = node.args[1]
                if isinstance(attribute, ast.Constant) and attribute.value == symbol:
                    found.append((node.lineno, "DYNAMIC_ATTRIBUTE", f"{name}(..., {symbol!r})"))
                elif (
                    not isinstance(attribute, ast.Constant)
                    and isinstance(node.args[0], ast.Name)
                    and node.args[0].id in module_aliases
                ):
                    found.append((node.lineno, "DYNAMIC_ATTRIBUTE", f"{name}(module_alias, <computed>)"))
            if name == "__import__" or name.endswith(".import_module"):
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    imported = node.args[0].value
                    if imported == target_module or imported.startswith(target_module + "."):
                        found.append((node.lineno, "DYNAMIC_IMPORT", f"{name}({imported!r})"))
        elif isinstance(node, ast.Subscript):
            if (
                isinstance(node.value, ast.Attribute)
                and node.value.attr == "modules"
                and isinstance(node.slice, ast.Constant)
                and isinstance(node.slice.value, str)
                and (node.slice.value == target_module or node.slice.value.startswith(target_module + "."))
            ):
                found.append((node.lineno, "DYNAMIC_IMPORT", f"sys.modules[{node.slice.value!r}]"))
    return found


def _ast_delta_allowed(before: ast.AST, after: ast.AST, symbol: str, new: str) -> bool:
    """True when the two trees differ only in the intended identifiers/strings."""

    if type(before) is not type(after):
        return False
    for field in before._fields:
        if field in _IGNORED_AST_FIELDS:
            continue
        left = getattr(before, field)
        right = getattr(after, field)
        if isinstance(left, list) and isinstance(right, list):
            if len(left) != len(right):
                return False
            for left_item, right_item in zip(left, right):
                if isinstance(left_item, ast.AST) and isinstance(right_item, ast.AST):
                    if not _ast_delta_allowed(left_item, right_item, symbol, new):
                        return False
                elif left_item != right_item:
                    return False
            continue
        if isinstance(left, ast.AST) and isinstance(right, ast.AST):
            if not _ast_delta_allowed(left, right, symbol, new):
                return False
            continue
        if left == right:
            continue
        if left == symbol and right == new:
            continue
        if isinstance(left, str) and isinstance(right, str) and left == symbol and right == new:
            continue
        return False
    return True


def _plan_file(
    path: str,
    tree: ast.AST,
    source: str,
    target_path: str,
    target_module: str,
    symbol: str,
    new: str,
    is_target: bool,
    definition_line: int | None,
) -> dict[str, Any]:
    """Compute bounded edits for one file, mutating a duplicate AST in parallel."""

    lines = source.splitlines(keepends=True)
    duplicate = copy.deepcopy(tree)
    mapping: dict[int, ast.AST] = {}
    _pair_nodes(tree, duplicate, mapping)
    edits: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    not_rewritten: list[dict[str, Any]] = []

    def record(
        node: ast.AST, kind: str, new_text: str, *, replace: bool = True,
    ) -> None:
        line, start, end = _line_span(node, lines)
        if replace:
            clone = mapping[id(node)]
            if kind == "NAME":
                clone.id = new_text  # type: ignore[attr-defined]
            elif kind == "ATTRIBUTE":
                clone.attr = new_text  # type: ignore[attr-defined]
            elif kind == "DEFINITION":
                clone.name = new_text  # type: ignore[attr-defined]
            elif kind == "IMPORT":
                clone.name = new_text  # type: ignore[attr-defined]
            elif kind == "EXPORT":
                clone.value = new_text  # type: ignore[attr-defined]
            else:
                raise ValueError(f"unsupported edit kind: {kind}")
        edits.append({
            "path": path,
            "line": line,
            "column": start,
            "kind": kind,
            "before": lines[line - 1][start:end],
            "after": new_text,
            "evidence_ref": f"file:{path}:line:{line}",
        })

    def flag(line: int, reason: str, detail: str) -> None:
        unresolved.append({
            "path": path,
            "line": line,
            "reason": reason,
            "detail": detail[:300],
            "evidence_ref": f"file:{path}:line:{line}",
        })

    if source and not source.endswith("\n"):
        flag(len(lines) or 1, "NO_TRAILING_NEWLINE", "file does not end with a newline; a safe patch cannot be guaranteed")

    if is_target:
        if definition_line is None:
            flag(1, "SYMBOL_NOT_FOUND", f"{symbol!r} is not defined in the target file")
        target_defs = [
            node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and node.name == symbol
        ]
        if len(target_defs) != 1:
            flag(
                target_defs[0].lineno if target_defs else 1,
                "SYMBOL_AMBIGUOUS",
                f"expected exactly one top-level function/class named {symbol!r}; found {len(target_defs)}",
            )
        else:
            definition = target_defs[0]
            record(definition, "DEFINITION", new)
            allowed = {(definition.lineno, _definition_name_column(definition))}
            extras = [
                site for site in _binding_sites(tree, symbol)
                if (site[0], site[1]) not in allowed
            ]
            if extras:
                flag(extras[0][0], "SYMBOL_ALSO_BOUND", f"{symbol!r} is also bound as {extras[0][2]}")
            collisions = _binding_sites(tree, new, module_level_only=True)
            if collisions:
                flag(collisions[0][0], "NEW_NAME_ALREADY_BOUND", f"{new!r} is already a module-level binding")
        dynamic_all_line = _dynamic_all(tree)
        if dynamic_all_line is not None:
            flag(dynamic_all_line, "DYNAMIC_ALL", "__all__ is dynamically constructed; exported names cannot be resolved")
        for constant in _module_all_nodes(tree, symbol):
            record(constant, "EXPORT", new)

    symbol_aliases, module_aliases, star_import = _import_bindings(
        path, tree, target_module, symbol,
    )
    imported_unaliased = symbol in symbol_aliases
    imported_aliased = any(alias != symbol for alias in symbol_aliases)

    if star_import:
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and any(alias.name == "*" for alias in node.names):
                if _import_from_base(path, node) == target_module:
                    flag(node.lineno, "STAR_IMPORT", f"from {target_module} import *")
                    break

    import_sites: set[tuple[int, int]] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        if _import_from_base(path, node) != target_module:
            continue
        for alias in node.names:
            if alias.name != symbol:
                continue
            import_sites.add((alias.lineno or node.lineno, alias.col_offset or 0))
            record(alias, "IMPORT", new)

    if imported_unaliased or imported_aliased:
        dynamic_all_line = _dynamic_all(tree)
        if dynamic_all_line is not None:
            flag(dynamic_all_line, "DYNAMIC_ALL", "__all__ is dynamically constructed in a file that imports the symbol")

    if imported_unaliased and not is_target:
        extras = [
            site for site in _binding_sites(tree, symbol)
            if (site[0], site[1]) not in import_sites
        ]
        if extras:
            flag(extras[0][0], "SYMBOL_ALSO_BOUND", f"{symbol!r} is also bound as {extras[0][2]}")
        collisions = _binding_sites(tree, new, module_level_only=True)
        if collisions:
            flag(collisions[0][0], "NEW_NAME_ALREADY_BOUND", f"{new!r} is already a module-level binding")
        for constant in _module_all_nodes(tree, symbol):
            record(constant, "EXPORT", new)

    if imported_unaliased or is_target:
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == symbol and isinstance(node.ctx, ast.Load):
                record(node, "NAME", new)

    for alias in sorted(module_aliases):
        extras = [
            site for site in _binding_sites(tree, alias)
            if site[2] != "import"
        ]
        if extras:
            flag(extras[0][0], "MODULE_ALIAS_REBOUND", f"module alias {alias!r} is rebound as {extras[0][2]}")
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and node.attr == symbol
                and isinstance(node.ctx, ast.Load)
                and isinstance(node.value, ast.Name)
                and node.value.id == alias
            ):
                record(node, "ATTRIBUTE", new)

    if not is_target and not symbol_aliases and not module_aliases and not star_import:
        return {
            "edits": edits,
            "unresolved": unresolved,
            "not_rewritten": not_rewritten,
            "original_tree": tree,
            "expected_tree": duplicate,
        }

    docstrings = _docstring_ids(tree)
    export_nodes = {id(node) for node in _module_all_nodes(tree, symbol)}
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and node.value == symbol
            and id(node) not in docstrings
            and id(node) not in export_nodes
        ):
            flag(node.lineno, "STRING_CONSTANT", "exact symbol string may be a dynamic reference")

    for line, reason, detail in _dynamic_references(tree, symbol, target_module, module_aliases):
        flag(line, reason, detail)

    if not is_target:
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and node.attr == symbol
                and isinstance(node.ctx, ast.Load)
                and not (
                    isinstance(node.value, ast.Name)
                    and node.value.id in module_aliases
                )
            ):
                not_rewritten.append({
                    "path": path,
                    "line": node.lineno,
                    "reason": "NON_MODULE_ATTRIBUTE",
                    "detail": ast.unparse(node)[:200],
                    "evidence_ref": f"file:{path}:line:{node.lineno}",
                })

    return {
        "edits": edits,
        "unresolved": unresolved,
        "not_rewritten": not_rewritten,
        "original_tree": tree,
        "expected_tree": duplicate,
    }


def _apply_edits(source: str, edits: list[dict[str, Any]], path: str) -> str:
    lines = source.splitlines(keepends=True)
    ordered = sorted(edits, key=lambda item: (item["line"], item["column"]), reverse=True)
    previous: tuple[int, int] | None = None
    for edit in ordered:
        line = edit["line"]
        start = edit["column"]
        end = start + len(edit["before"])
        if previous is not None and (line, start) >= previous:
            raise ValueError(f"overlapping edits in {path}")
        previous = (line, start)
        text = lines[line - 1]
        if text[start:end] != edit["before"]:
            raise ValueError(
                f"edit does not match source in {path}:{line}: expected {edit['before']!r}, "
                f"found {text[start:end]!r}"
            )
        lines[line - 1] = text[:start] + edit["after"] + text[end:]
    return "".join(lines)


def _unified_patch(path: str, before: str, after: str) -> str:
    diff = "".join(difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=f"a/{path}",
        tofile=f"b/{path}",
        n=3,
    ))
    if not diff:
        return ""
    return f"diff --git a/{path} b/{path}\n{diff}"


def _non_python_mentions(
    checkout: Path, tracked: set[str], symbol: str, rewritten: set[str], limit: int,
) -> tuple[list[dict[str, Any]], int]:
    pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(symbol)}(?![A-Za-z0-9_])")
    found: list[dict[str, Any]] = []
    total = 0
    for relative in sorted(tracked):
        if relative.endswith(".py") or relative in rewritten:
            continue
        try:
            # Use the same tracked, contained, non-symlink source boundary as
            # Python parsing. Non-Python mention disclosure must not follow a
            # repository link into unrelated files in the agent's environment.
            candidate = _source(checkout, tracked, relative)
            if candidate.stat().st_size > 200_000:
                continue
            raw = candidate.read_bytes()
        except (OSError, ValueError, RuntimeError):
            continue
        if b"\0" in raw:
            continue
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                total += 1
                if len(found) < limit:
                    found.append({
                        "path": relative,
                        "line": line_number,
                        "reason": "NON_PYTHON_MENTION",
                        "detail": line.strip()[:200],
                        "evidence_ref": f"file:{relative}:line:{line_number}",
                    })
                break
    return found, total


def _residual_references(checkout: Path, tracked: set[str], target_module: str, symbol: str) -> list[dict[str, Any]]:
    residue: list[dict[str, Any]] = []
    for candidate in sorted(tracked):
        if not candidate.endswith(".py"):
            continue
        tree, _, _, error = _parse(checkout, tracked, candidate)
        if error or tree is None:
            residue.append({
                "path": candidate,
                "line": 0,
                "reason": "PARSE_FAILURE",
                "detail": error or "parse failed",
            })
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and _import_from_base(candidate, node) == target_module:
                for alias in node.names:
                    if alias.name == symbol:
                        residue.append({
                            "path": candidate,
                            "line": node.lineno,
                            "reason": "IMPORT",
                            "detail": f"from {target_module} import {symbol}",
                        })
        aliases, modules, _ = _import_bindings(candidate, tree, target_module, symbol)
        for line, _, kind in _reference_nodes(tree, symbol, aliases, modules):
            residue.append({
                "path": candidate,
                "line": line,
                "reason": kind,
                "detail": "direct old-name reference remains",
            })
    return residue


def build_refactor_rename_preview(
    root: str | Path, target_ref: str, path: str, symbol: str, new: str,
) -> dict[str, Any]:
    """Build and verify a patch-only rename preview for one committed symbol."""

    if not _SYMBOL.fullmatch(symbol):
        raise ValueError("--symbol must be one Python identifier")
    if not _SYMBOL.fullmatch(new):
        raise ValueError("--to must be one Python identifier")
    if symbol == new:
        raise ValueError("--symbol and --to must differ")
    target_path = _safe_path(path)
    if not target_path.endswith(".py"):
        raise ValueError("refactor rename currently supports one tracked .py file")
    root_dir = Path(root).resolve()
    with temporary_commit_checkout(root_dir, target_ref) as checkout:
        checkout, tracked = verified_tracked_sources(checkout, target_ref)
        if target_path not in tracked:
            raise ValueError("target path is not a tracked file at the selected revision")
        target_tree, target_source, _, target_error = _parse(checkout, tracked, target_path)
        if target_tree is None or target_source is None:
            raise ValueError(f"target source could not be parsed: {target_error or target_path}")
        target_module = _module_for_path(target_path)
        definitions = [
            node for node in target_tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and node.name == symbol
        ]
        if not definitions:
            raise ValueError(f"{symbol!r} is not a top-level function or class in {target_path}")
        if len(definitions) != 1:
            raise ValueError(f"{symbol!r} is defined {len(definitions)} times; exactly one definition is required")

        plans: dict[str, dict[str, Any]] = {}
        planned_sources: dict[str, str] = {}
        unresolved: list[dict[str, Any]] = []
        not_rewritten: list[dict[str, Any]] = []
        edits_total = 0
        for candidate in sorted(tracked):
            if not candidate.endswith(".py"):
                continue
            tree, source, _, error = _parse(checkout, tracked, candidate)
            if tree is None or source is None:
                unresolved.append({
                    "path": candidate,
                    "line": 0,
                    "reason": "PARSE_FAILURE",
                    "detail": error or "parse failed",
                    "evidence_ref": f"file:{candidate}",
                })
                continue
            if candidate != target_path:
                aliases, modules, star = _import_bindings(candidate, tree, target_module, symbol)
                if not aliases and not modules and not star:
                    continue
            plan = _plan_file(
                candidate, tree, source, target_path, target_module, symbol, new,
                candidate == target_path, definitions[0].lineno,
            )
            if plan["edits"] or plan["unresolved"] or plan["not_rewritten"]:
                plans[candidate] = plan
            edits_total += len(plan["edits"])
            unresolved.extend(plan["unresolved"])
            not_rewritten.extend(plan["not_rewritten"])
            if plan["edits"]:
                planned_sources[candidate] = _apply_edits(source, plan["edits"], candidate)

        patch_parts: list[str] = []
        for candidate in sorted(planned_sources):
            tree, source, _, _ = _parse(checkout, tracked, candidate)
            if tree is None or source is None:
                raise ValueError(f"source became unreadable: {candidate}")
            patch_parts.append(_unified_patch(candidate, source, planned_sources[candidate]))
        patch = "".join(patch_parts)

        non_python, non_python_total = _non_python_mentions(
            checkout, tracked, symbol, set(planned_sources), _MAX_SITES,
        )

        status = "READY"
        coverage = "COMPLETE_FOR_DIRECT_PYTHON_REFERENCES"
        application: dict[str, Any] = {
            "applied_in_temporary_checkout": False,
            "git_apply_check": "NOT_RUN",
            "files_parse": "NOT_RUN",
            "ast_delta": "NOT_RUN",
            "old_reference_residue": None,
            "failure": None,
        }
        if unresolved:
            status = "BLOCKED"
            coverage = "BLOCKED"
            application["failure"] = "unresolved sites block the patch"
        if not patch:
            status = "BLOCKED"
            coverage = "BLOCKED"
            application["failure"] = "no changes were computed"
        if status == "READY":
            try:
                check = subprocess.run(
                    ["git", "-c", "core.fsmonitor=false", "apply", "--check", "-"],
                    cwd=checkout, input=patch.encode("utf-8"), text=False,
                    capture_output=True, timeout=120, check=False,
                )
                application["git_apply_check"] = "PASS" if check.returncode == 0 else "FAIL"
                if check.returncode != 0:
                    detail = check.stderr.decode("utf-8", "replace").strip()[:300]
                    raise ValueError(f"git apply --check failed: {detail}")
                apply = subprocess.run(
                    ["git", "-c", "core.fsmonitor=false", "apply", "-"],
                    cwd=checkout, input=patch.encode("utf-8"), text=False,
                    capture_output=True, timeout=120, check=False,
                )
                if apply.returncode != 0:
                    detail = apply.stderr.decode("utf-8", "replace").strip()[:300]
                    raise ValueError(f"git apply failed: {detail}")
                application["applied_in_temporary_checkout"] = True
                for candidate in sorted(planned_sources):
                    after_tree, _, _, error = _parse(checkout, tracked, candidate)
                    if after_tree is None:
                        raise ValueError(f"patched source does not parse: {candidate}: {error}")
                    original = plans[candidate].get("original_tree")
                    expected = plans[candidate].get("expected_tree")
                    if original is None or expected is None:
                        raise ValueError(f"missing planned tree for {candidate}")
                    if not _ast_delta_allowed(original, after_tree, symbol, new):
                        raise ValueError(f"AST delta outside identifiers in {candidate}")
                    if ast.dump(expected, include_attributes=False) != ast.dump(after_tree, include_attributes=False):
                        raise ValueError(f"patched AST differs from the planned identifier edits in {candidate}")
                application["files_parse"] = "PASS"
                application["ast_delta"] = "IDENTIFIERS_ONLY"
                residue = _residual_references(checkout, tracked, target_module, symbol)
                application["old_reference_residue"] = len(residue)
                if residue:
                    raise ValueError(f"old-name residue remains in {len(residue)} site(s)")
            except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
                status = "BLOCKED"
                coverage = "BLOCKED"
                application["failure"] = str(exc)
        proposed_patch = patch if status == "BLOCKED" else ""
        if status == "BLOCKED":
            patch = ""

        if non_python or not_rewritten:
            if coverage.startswith("COMPLETE"):
                coverage = "COMPLETE_FOR_DIRECT_PYTHON_REFERENCES_WITH_LISTED_NON_PYTHON_OR_ATTRIBUTE_MENTIONS"

        reported_edits: list[dict[str, Any]] = []
        for candidate in sorted(plans):
            reported_edits.extend(plans[candidate]["edits"])
        truncated = len(reported_edits) > _MAX_EDITS or len(unresolved) > _MAX_SITES
        reported_edits = reported_edits[:_MAX_EDITS]
        reported_unresolved = unresolved[:_MAX_SITES]
        reported_not_rewritten = (not_rewritten + non_python)[:_MAX_SITES]

        return {
            "artifact": "refactor_rename_preview",
            "status": status,
            "base_ref": target_ref,
            "path": target_path,
            "symbol": symbol,
            "to": new,
            "definition": {
                "line": definitions[0].lineno,
                "kind": "class" if isinstance(definitions[0], ast.ClassDef) else "function",
                "module": target_module,
            },
            "changes": reported_edits,
            "counts": {
                "files_changed": len(planned_sources),
                "edits": edits_total,
                "imports": sum(1 for edit in reported_edits if edit["kind"] == "IMPORT"),
                "exports": sum(1 for edit in reported_edits if edit["kind"] == "EXPORT"),
                "unresolved_sites": len(unresolved),
                "not_rewritten_sites": len(not_rewritten) + non_python_total,
            },
            "unresolved_sites": reported_unresolved,
            "not_rewritten": reported_not_rewritten,
            "non_python_mentions_total": non_python_total,
            "patch": patch or None,
            "proposed_patch": proposed_patch if status == "BLOCKED" else None,
            "application": application,
            "coverage_status": coverage,
            "truncated": truncated,
            "limits": list(_LIMITS),
        }
