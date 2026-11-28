"""Mechanical source relationships for one committed Python path.

This module answers a bounded pre-change question: which tracked Python files
import the target, which tests reference it, what public symbols does it
define, and which repository files does it import? A selected symbol can also
carry a behavioral surface and direct guard-derived verification scenarios. It
reads a clean temporary checkout of one exact Git revision and parses bytes
with ``ast``.

It does not establish runtime dependency, call order, test coverage, semantic
impact or change authorization. Dynamic imports, reflection, non-Python
references and runtime-only coupling are not assessed.
"""

from __future__ import annotations

import ast
import hashlib
import re
from collections import deque
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Mapping

from .knowledge_sources import _git, _source, temporary_commit_checkout, verified_tracked_sources
from .verification_scenarios import build_guard_scenarios

_MAX_LIMIT = 250
_SYMBOL = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_LIMITS = (
    "Python AST import syntax and top-level definitions only; runtime imports, "
    "reflection and call order are NOT ASSESSED.",
    "Importer and test entries are syntactic references, not proof of runtime use "
    "or test coverage.",
    "Only tracked Python files at the exact revision are inspected; symlink "
    "sources are refused, and non-Python references and untracked bytes are not represented.",
    "A missing relationship is NOT ASSESSED, not evidence that no relationship exists.",
    "The top-level-symbol leading_underscore and in_module_all markers are syntax "
    "and name conventions only; they are not export or stable-API claims.",
    "Test references are file-level and do not show which symbol or behavior is exercised.",
    "Re-exports through a package __init__ are not resolved to the defining module.",
    "An importer line is the first matching import; evidence_refs lists the matching lines.",
)


def _safe_path(path: str) -> str:
    value = PurePosixPath(path)
    if value.is_absolute() or ".." in value.parts or not value.parts:
        raise ValueError("source relationships require a repository-relative path")
    return value.as_posix()


def _module_for_path(path: str) -> str:
    value = path.removeprefix("src/")
    if value.endswith(".py"):
        value = value[:-3]
    parts = value.split("/")
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _package_for_path(path: str) -> list[str]:
    if path.endswith("/__init__.py") or path == "__init__.py":
        return _module_for_path(path).split(".") if _module_for_path(path) else []
    return _module_for_path(path).split(".")[:-1]


def _import_from_base(path: str, node: ast.ImportFrom) -> str | None:
    """Resolve an ImportFrom base to an absolute module, or None if impossible."""

    package = _package_for_path(path)
    level = node.level or 0
    if level:
        if level - 1 > len(package):
            return None
        package = package[: len(package) - (level - 1)]
        return ".".join(filter(None, [*package, *(node.module or "").split(".")]))
    return node.module or ""


def _import_candidates(path: str, node: ast.AST) -> list[tuple[str, int, tuple[str, ...]]]:
    """Return absolute module candidates, line and imported names for an import node."""

    candidates: list[tuple[str, int, tuple[str, ...]]] = []
    if isinstance(node, ast.Import):
        for alias in node.names:
            candidates.append((alias.name, node.lineno, ()))
    elif isinstance(node, ast.ImportFrom):
        base = _import_from_base(path, node)
        if base is None:
            return []
        if not node.module:
            for alias in node.names:
                if alias.name != "*":
                    candidates.append((".".join(filter(None, [base, alias.name])), node.lineno, (alias.name,)))
            return candidates
        if base:
            candidates.append((base, node.lineno, tuple(a.name for a in node.names if a.name != "*")))
        for alias in node.names:
            if alias.name != "*":
                candidates.append((".".join(filter(None, [base, alias.name])), node.lineno, (alias.name,)))
    return candidates


def _module_index(tracked: Iterable[str]) -> dict[str, str]:
    index: dict[str, str] = {}
    for path in tracked:
        if path.endswith(".py"):
            index.setdefault(_module_for_path(path), path)
    return index


def _matches_target(module: str, target_module: str, target_is_package: bool) -> bool:
    return module == target_module or (
        target_is_package and module.startswith(target_module + ".")
    )


def _parse(
    checkout: Path, tracked: set[str], relative: str,
) -> tuple[ast.AST | None, str | None, bytes | None, str | None]:
    try:
        raw = _source(checkout, tracked, relative).read_bytes()
    except (OSError, ValueError, RuntimeError) as exc:
        return None, None, None, f"{relative}: source could not be read: {exc}"
    try:
        source = raw.decode("utf-8-sig")
    except UnicodeError as exc:
        return None, None, raw, f"{relative}: source is not UTF-8: {exc}"
    try:
        return ast.parse(source, filename=relative), source, raw, None
    except SyntaxError as exc:
        return None, source, raw, f"{relative}: Python syntax error at line {exc.lineno}"


def _module_all(tree: ast.AST) -> set[str] | None:
    """Return a literal module-level __all__ set, or None when absent/dynamic."""

    for node in tree.body:
        value = None
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        ):
            value = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "__all__":
            value = node.value
        if value is None:
            continue
        if isinstance(value, (ast.List, ast.Tuple, ast.Set)):
            names = {
                element.value for element in value.elts
                if isinstance(element, ast.Constant) and isinstance(element.value, str)
            }
            if len(names) == len(value.elts):
                return names
        return None
    return None


def _top_level_symbols(
    tree: ast.AST, limit: int, exported: set[str] | None,
) -> tuple[list[dict[str, Any]], int]:
    symbols: list[dict[str, Any]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            symbols.append({
                "name": node.name,
                "kind": "class" if isinstance(node, ast.ClassDef) else "function",
                "line": node.lineno,
                "leading_underscore": node.name.startswith("_"),
                "in_module_all": (
                    node.name in exported if exported is not None else None
                ),
            })
    return symbols[:limit], len(symbols)


def _direct_imports(
    tree: ast.AST, path: str, module_paths: Mapping[str, str], limit: int,
) -> tuple[list[dict[str, Any]], int]:
    items: list[dict[str, Any]] = []
    total = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                total += 1
                if len(items) < limit:
                    resolved = module_paths.get(alias.name)
                    items.append({
                        "module": alias.name,
                        "line": node.lineno,
                        "resolved_path": resolved,
                        "resolution": "TRACKED" if resolved else "EXTERNAL_OR_UNRESOLVED",
                        "imported_names": [],
                        "evidence_ref": f"file:{path}:line:{node.lineno}",
                    })
        elif isinstance(node, ast.ImportFrom):
            base = _import_from_base(path, node)
            if base is None:
                total += 1
                continue
            total += 1
            if len(items) < limit:
                resolved = module_paths.get(base)
                items.append({
                    "module": base,
                    "line": node.lineno,
                    "resolved_path": resolved,
                    "resolution": "TRACKED" if resolved else "EXTERNAL_OR_UNRESOLVED",
                    "imported_names": [a.name for a in node.names if a.name != "*"],
                    "evidence_ref": f"file:{path}:line:{node.lineno}",
                })
    return items, total


def _import_bindings(
    path: str, tree: ast.AST, target_module: str, symbol: str,
) -> tuple[set[str], set[str], bool]:
    """Return local symbol aliases, local module aliases and star-import status."""

    symbol_aliases: set[str] = set()
    module_aliases: set[str] = set()
    star_import = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name != target_module:
                    continue
                if alias.asname:
                    module_aliases.add(alias.asname)
                elif "." not in alias.name:
                    module_aliases.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            base = _import_from_base(path, node)
            if base is None:
                continue
            if base == target_module:
                for alias in node.names:
                    if alias.name == "*":
                        star_import = True
                    elif alias.name == symbol:
                        symbol_aliases.add(alias.asname or alias.name)
            else:
                for alias in node.names:
                    if alias.name == "*":
                        continue
                    candidate = f"{base}.{alias.name}" if base else alias.name
                    if candidate == target_module:
                        module_aliases.add(alias.asname or alias.name)
    return symbol_aliases, module_aliases, star_import


def _reference_nodes(
    tree: ast.AST, symbol: str, symbol_aliases: set[str], module_aliases: set[str],
) -> list[tuple[int, int, str]]:
    parents: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    references: list[tuple[int, int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in symbol_aliases and isinstance(node.ctx, ast.Load):
            parent = parents.get(node)
            kind = "CALL" if isinstance(parent, ast.Call) and parent.func is node else "NAME"
            references.append((node.lineno, node.col_offset, kind))
        elif (
            isinstance(node, ast.Attribute) and node.attr == symbol
            and isinstance(node.ctx, ast.Load)
            and isinstance(node.value, ast.Name) and node.value.id in module_aliases
        ):
            parent = parents.get(node)
            kind = "CALL" if isinstance(parent, ast.Call) and parent.func is node else "ATTRIBUTE"
            references.append((node.lineno, node.col_offset, kind))
    return references


def _test_scopes(tree: ast.AST) -> list[tuple[str, str, int, int]]:
    scopes: list[tuple[str, str, int, int]] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            scopes.append(("FUNCTION", node.name, node.lineno, node.end_lineno or node.lineno))
        elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name.startswith("test_"):
                    scopes.append((
                        "METHOD", f"{node.name}::{child.name}",
                        child.lineno, child.end_lineno or child.lineno,
                    ))
    return scopes


def _direct_behavior_nodes(node: ast.AST) -> Iterable[ast.AST]:
    """Yield nodes inside one definition without entering nested functions/classes."""

    stack = list(ast.iter_child_nodes(node))
    while stack:
        child = stack.pop()
        yield child
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            continue
        stack.extend(ast.iter_child_nodes(child))


def _signature(node: ast.AST) -> str:
    if isinstance(node, ast.ClassDef):
        parts = [ast.unparse(base) for base in node.bases]
        parts.extend(f"{keyword.arg}={ast.unparse(keyword.value)}" for keyword in node.keywords)
        return "class " + node.name + "(" + ", ".join(parts) + ")"
    prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
    result = prefix + "(" + ast.unparse(node.args) + ")"
    if getattr(node, "returns", None) is not None:
        result += " -> " + ast.unparse(node.returns)
    return result


def _behavior_surface(
    node: ast.AST, source: str, path: str, limit: int,
) -> dict[str, Any]:
    """Return a source-level behavioral surface for one definition.

    This is a bounded reading aid: signature, decorators, docstring summary,
    direct raise/assert statements and an exact source-body hash. It is not a
    semantic behavior model or a runtime contract.
    """

    docstring = ast.get_docstring(node, clean=True) if isinstance(
        node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    ) else None
    summary = None
    if docstring:
        summary = " ".join(docstring.strip().split("\n\n", 1)[0].split())
        summary = summary[:400]
    raises: list[dict[str, Any]] = []
    assertions: list[dict[str, Any]] = []
    raises_total = 0
    assertions_total = 0
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        for child in _direct_behavior_nodes(node):
            if isinstance(child, ast.Raise):
                raises_total += 1
                if len(raises) < limit:
                    if child.exc is None:
                        name = "bare raise"
                    elif isinstance(child.exc, ast.Call):
                        name = ast.unparse(child.exc.func)
                    else:
                        name = ast.unparse(child.exc)
                    raises.append({"type": name, "line": child.lineno})
            elif isinstance(child, ast.Assert):
                assertions_total += 1
                if len(assertions) < limit:
                    assertions.append({"test": ast.unparse(child.test)[:240], "line": child.lineno})
    segment = ast.get_source_segment(source, node)
    if segment is None:
        segment = ast.unparse(node)
    return {
        "kind": (
            "class" if isinstance(node, ast.ClassDef)
            else "async_function" if isinstance(node, ast.AsyncFunctionDef)
            else "function"
        ),
        "signature": _signature(node),
        "decorators": [ast.unparse(item) for item in node.decorator_list][:limit],
        "docstring_summary": summary,
        "docstring_sha256": hashlib.sha256(docstring.encode("utf-8")).hexdigest() if docstring else None,
        "raises": raises,
        "assertions": assertions,
        "source_sha256": hashlib.sha256(segment.encode("utf-8")).hexdigest(),
        "line": node.lineno,
        "end_line": node.end_lineno or node.lineno,
        "path": path,
        "truncated": (
            raises_total > len(raises)
            or assertions_total > len(assertions)
            or len(node.decorator_list) > limit
        ),
    }


def _symbol_context(
    target_path: str, target_tree: ast.AST, target_source: str, target_module: str,
    target_exported: set[str] | None, tracked: set[str], checkout: Path,
    symbol: str, limit: int,
) -> dict[str, Any]:
    definitions: list[dict[str, Any]] = []
    definitions_total = 0
    for node in target_tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if node.name != symbol:
            continue
        definitions_total += 1
        if len(definitions) < limit:
            definitions.append({
                "path": target_path,
                "line": node.lineno,
                "kind": "class" if isinstance(node, ast.ClassDef) else "function",
                "leading_underscore": node.name.startswith("_"),
                "in_module_all": node.name in target_exported if target_exported is not None else None,
                "evidence_ref": f"file:{target_path}:line:{node.lineno}",
                "behavior": _behavior_surface(node, target_source, target_path, limit),
            })

    direct_references: list[dict[str, Any]] = []
    test_candidates: list[dict[str, Any]] = []
    direct_total = 0
    test_total = 0
    star_import = False
    parse_failures: list[str] = []

    target_refs = _reference_nodes(target_tree, symbol, {symbol}, set())
    for line, column, kind in target_refs:
        direct_total += 1
        if len(direct_references) < limit:
            direct_references.append({
                "path": target_path,
                "line": line,
                "column": column,
                "kind": kind,
                "is_target_file": True,
                "evidence_ref": f"file:{target_path}:line:{line}",
            })

    for candidate in sorted(tracked):
        if not candidate.endswith(".py") or candidate == target_path:
            continue
        tree, _, _, error = _parse(checkout, tracked, candidate)
        if error or tree is None:
            parse_failures.append(error or f"{candidate}: source could not be parsed")
            continue
        symbol_aliases, module_aliases, candidate_star = _import_bindings(
            candidate, tree, target_module, symbol,
        )
        star_import = star_import or candidate_star
        references = _reference_nodes(tree, symbol, symbol_aliases, module_aliases)
        if not references:
            continue
        if candidate.startswith("tests/"):
            scopes = _test_scopes(tree)
            by_scope: dict[str, dict[str, Any]] = {}
            for line, column, kind in references:
                containing = [
                    scope for scope in scopes if scope[2] <= line <= scope[3]
                ]
                if not containing:
                    continue
                scope = min(containing, key=lambda item: item[3] - item[2])
                key = scope[1]
                item = by_scope.setdefault(key, {
                    "path": candidate,
                    "test_name": scope[1],
                    "test_kind": scope[0],
                    "line": scope[2],
                    "reference_lines": [],
                    "kinds": [],
                    "evidence_refs": [],
                })
                if line not in item["reference_lines"]:
                    item["reference_lines"].append(line)
                if kind not in item["kinds"]:
                    item["kinds"].append(kind)
                item["evidence_refs"].append(f"file:{candidate}:line:{line}")
            for item in by_scope.values():
                test_total += 1
                if len(test_candidates) < limit:
                    test_candidates.append(item)
        else:
            for line, column, kind in references:
                direct_total += 1
                if len(direct_references) < limit:
                    direct_references.append({
                        "path": candidate,
                        "line": line,
                        "column": column,
                        "kind": kind,
                        "is_target_file": False,
                        "evidence_ref": f"file:{candidate}:line:{line}",
                    })

    behavior_truncated = any(
        item["behavior"].get("truncated") for item in definitions
    )
    scenario_context = build_guard_scenarios(
        target_tree, target_source, target_path, symbol, limit=limit,
    )
    truncated = (
        definitions_total > len(definitions)
        or direct_total > len(direct_references)
        or test_total > len(test_candidates)
        or behavior_truncated
        or scenario_context["truncated"]
    )
    return {
        "symbol": symbol,
        "defined_in_target": definitions_total > 0,
        "definitions": definitions,
        "direct_references": direct_references,
        "test_candidates": test_candidates,
        "counts": {
            "definitions": definitions_total,
            "direct_references": direct_total,
            "test_candidates": test_total,
            "parse_failures": len(parse_failures),
            "behavior_truncated": behavior_truncated,
            "verification_scenarios": scenario_context["counts"]["scenarios"],
        },
        "star_import_observed": star_import,
        "test_candidate_scope": "TEST_FUNCTION_LEVEL",
        "verification_scenarios": scenario_context,
        "truncated": truncated,
        "limits": [
            *scenario_context["limits"],
            "Symbol references are direct syntactic names/attributes only; dotted import chains without an alias, star imports, dynamic dispatch, inheritance and runtime calls are NOT ASSESSED.",
            "Test candidates are test functions/methods that directly mention the symbol in their own body; fixture, helper and indirect coverage is NOT ASSESSED.",
            "Aliases are collected across each file; lexical scope and rebinding are NOT ASSESSED.",
            "A reference is not proof of execution, and a test candidate is not proof that the test covers the symbol.",
            "No transitive closure or impact verdict is produced.",
        ],
    }


def build_source_relationships(
    root: str | Path, target_ref: str, path: str, *, limit: int = 50,
    symbol: str | None = None,
) -> dict[str, Any]:
    """Build a bounded source-relationship view for one committed Python file."""

    if not 1 <= limit <= _MAX_LIMIT:
        raise ValueError("source relationship limit must be 1..250")
    if symbol is not None and not _SYMBOL.fullmatch(symbol):
        raise ValueError("--symbol must be one Python identifier")
    target_path = _safe_path(path)
    if not target_path.endswith(".py"):
        raise ValueError("source relationships currently support one tracked .py file")
    root_dir = Path(root).resolve()
    with temporary_commit_checkout(root_dir, target_ref) as checkout:
        checkout, tracked = verified_tracked_sources(checkout, target_ref)
        if target_path not in tracked:
            raise ValueError("target path is not a tracked file at the selected revision")
        target_tree, target_source, target_raw, target_error = _parse(checkout, tracked, target_path)
        if target_raw is None:
            raise ValueError(f"target source could not be read: {target_error or target_path}")
        module_paths = _module_index(tracked)
        target_module = _module_for_path(target_path)
        target_is_package = target_path.endswith("/__init__.py") or target_path == "__init__.py"
        target_sha256 = hashlib.sha256(target_raw).hexdigest()
        exported = _module_all(target_tree) if target_tree is not None else None

        if target_tree is None:
            direct_imports: list[dict[str, Any]] = []
            direct_imports_total = 0
            top_level_symbols: list[dict[str, Any]] = []
            top_level_symbols_total = 0
        else:
            direct_imports, direct_imports_total = _direct_imports(
                target_tree, target_path, module_paths, limit,
            )
            top_level_symbols, top_level_symbols_total = _top_level_symbols(
                target_tree, limit, exported,
            )

        symbol_context = None
        # A malformed target must not suppress authored context or imply that
        # the requested symbol is absent. Preserve the target parse disclosure.
        if symbol is not None and target_tree is not None:
            symbol_context = _symbol_context(
                target_path, target_tree, target_source or "", target_module,
                exported, tracked, checkout, symbol, limit,
            )

        importers: list[dict[str, Any]] = []
        test_references: list[dict[str, Any]] = []
        leading_underscore_imports: list[dict[str, Any]] = []
        parse_failures: list[str] = []
        importers_total = 0
        tests_total = 0
        leading_underscore_imports_total = 0
        for candidate in sorted(tracked):
            if not candidate.endswith(".py") or candidate == target_path:
                continue
            tree, source, _, error = _parse(checkout, tracked, candidate)
            if error or tree is None or source is None:
                parse_failures.append(error or f"{candidate}: source could not be parsed")
                continue
            matches: list[tuple[str, int, tuple[str, ...]]] = []
            for node in ast.walk(tree):
                if not isinstance(node, (ast.Import, ast.ImportFrom)):
                    continue
                for module, line, names in _import_candidates(candidate, node):
                    if _matches_target(module, target_module, target_is_package):
                        matches.append((module, line, names))
            is_test = candidate.startswith("tests/")
            if matches:
                first = matches[0]
                name_lines: dict[str, int] = {}
                for _, line, names in matches:
                    for name in names:
                        if name.startswith("_"):
                            name_lines.setdefault(name, line)
                for name, line in sorted(name_lines.items()):
                    leading_underscore_imports_total += 1
                    if len(leading_underscore_imports) < limit:
                        leading_underscore_imports.append({
                            "name": name,
                            "importer": candidate,
                            "line": line,
                            "is_test": is_test,
                            "evidence_ref": f"file:{candidate}:line:{line}",
                        })
                item = {
                    "path": candidate,
                    "line": first[1],
                    "derivations": ["IMPORT"],
                    "imported_names": sorted({name for _, _, names in matches for name in names}),
                    "evidence_refs": [f"file:{candidate}:line:{line}" for _, line, _ in matches[:limit]],
                }
                if is_test:
                    tests_total += 1
                    if len(test_references) < limit:
                        test_references.append(item)
                else:
                    importers_total += 1
                    if len(importers) < limit:
                        importers.append(item)
                continue
            if is_test and (target_path in source or target_module in source):
                tests_total += 1
                if len(test_references) < limit:
                    line = 1
                    for number, text in enumerate(source.splitlines(), 1):
                        if target_path in text or target_module in text:
                            line = number
                            break
                    test_references.append({
                        "path": candidate,
                        "line": line,
                        "derivations": ["PATH_MENTION"],
                        "imported_names": [],
                        "evidence_refs": [f"file:{candidate}:line:{line}"],
                    })

    truncated = (
        direct_imports_total > len(direct_imports)
        or top_level_symbols_total > len(top_level_symbols)
        or importers_total > len(importers) or tests_total > len(test_references)
        or leading_underscore_imports_total > len(leading_underscore_imports)
        or (symbol_context is not None and symbol_context["truncated"])
    )
    coverage_status = (
        "PARTIAL" if parse_failures or truncated or target_error
        else "COMPLETE_FOR_PYTHON_AST"
    )
    return {
        "target": {
            "path": target_path,
            "target_ref": target_ref,
            "sha256": target_sha256,
        },
        "counts": {
            "direct_imports": direct_imports_total,
            "direct_importers": importers_total,
            "test_references": tests_total,
            "top_level_symbols": top_level_symbols_total,
            "leading_underscore_imports": leading_underscore_imports_total,
            "parse_failures": len(parse_failures),
        },
        "direct_imports": direct_imports,
        "direct_importers": importers,
        "test_references": test_references,
        "test_reference_scope": "FILE_LEVEL",
        "top_level_symbols": top_level_symbols,
        "leading_underscore_imports": leading_underscore_imports,
        "symbol_context": symbol_context,
        "target_parse_error": target_error,
        "parse_failures": parse_failures[:limit],
        "coverage_status": coverage_status,
        "truncated": truncated,
        "limits": list(_LIMITS),
    }


def _review_side(
    root: Path, ref: str, path: str, limit: int, symbol: str | None,
) -> dict[str, Any]:
    """Classify the exact committed tree entry before inspecting its source."""

    entry = _git(root, "--literal-pathspecs", "ls-tree", "-z", "--full-tree", ref, "--", path)
    if not entry:
        return {"ref": ref, "status": "ABSENT_FROM_TREE", "relationships": None}
    metadata, separator, name = entry.rstrip("\0").partition("\t")
    if not separator or name != path or len(metadata.split()) != 3:
        raise ValueError("cannot establish the exact committed source review entry")
    mode, kind, _ = metadata.split()
    if kind != "blob" or mode not in {"100644", "100755"}:
        return {"ref": ref, "status": "NOT_REGULAR_FILE", "relationships": None}
    return {
        "ref": ref, "status": "REGULAR_FILE",
        "relationships": build_source_relationships(
            root, ref, path, limit=limit, symbol=symbol,
        ),
    }


def _compare_identities(
    base: Mapping[str, Any], target: Mapping[str, Any], field: str,
    identity: Callable[[Mapping[str, Any]], str], *,
    base_parsed: bool, target_parsed: bool,
) -> dict[str, Any]:
    """Compare only identities returned by the bounded syntactic consumer."""

    base_rows, target_rows = base[field], target[field]
    left = {identity(row) for row in base_rows}
    right = {identity(row) for row in target_rows}
    base_complete = base_parsed and base["counts"][field] == len(base_rows)
    target_complete = target_parsed and target["counts"][field] == len(target_rows)
    return {
        "base_only": sorted(left - right),
        "target_only": sorted(right - left),
        "both": sorted(left & right),
        "base_list_complete": base_complete,
        "target_list_complete": target_complete,
        "comparison_status": (
            "COMPLETE_FOR_REPORTED_IDENTITIES" if base_complete and target_complete
            else "VISIBLE_ONLY"
        ),
    }


def _behavior_comparison(
    base_symbol: Mapping[str, Any] | None,
    target_symbol: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Compare reported behavioral surfaces for one selected symbol."""

    if base_symbol is None or target_symbol is None:
        return {
            "comparison_status": "NOT_COMPARABLE",
            "reason": "SYMBOL_CONTEXT_UNAVAILABLE",
            "presence": "UNKNOWN",
            "changed_fields": [],
            "source_changed": None,
            "base": None,
            "target": None,
        }
    base_definitions = [
        item for item in base_symbol.get("definitions", []) if item.get("behavior")
    ]
    target_definitions = [
        item for item in target_symbol.get("definitions", []) if item.get("behavior")
    ]
    if len(base_definitions) != 1 or len(target_definitions) != 1:
        return {
            "comparison_status": "NOT_COMPARABLE",
            "reason": "EXPECTED_ONE_DEFINITION_WITH_BEHAVIOR",
            "presence": (
                "BOTH" if base_definitions and target_definitions
                else "BASE_ONLY" if base_definitions
                else "TARGET_ONLY" if target_definitions
                else "NEITHER"
            ),
            "changed_fields": [],
            "source_changed": None,
            "base": base_definitions[0]["behavior"] if len(base_definitions) == 1 else None,
            "target": target_definitions[0]["behavior"] if len(target_definitions) == 1 else None,
        }
    base, target = base_definitions[0]["behavior"], target_definitions[0]["behavior"]
    checks = (
        ("kind", base["kind"], target["kind"]),
        ("signature", base["signature"], target["signature"]),
        ("decorators", base["decorators"], target["decorators"]),
        ("docstring_summary", base["docstring_summary"], target["docstring_summary"]),
        ("docstring_sha256", base["docstring_sha256"], target["docstring_sha256"]),
        (
            "raises",
            sorted(item["type"] for item in base["raises"]),
            sorted(item["type"] for item in target["raises"]),
        ),
        (
            "assertions",
            sorted(item["test"] for item in base["assertions"]),
            sorted(item["test"] for item in target["assertions"]),
        ),
        ("source_sha256", base["source_sha256"], target["source_sha256"]),
    )
    changed = [name for name, left, right in checks if left != right]
    truncated = bool(
        base_symbol.get("truncated") or target_symbol.get("truncated")
        or base.get("truncated") or target.get("truncated")
    )
    return {
        "comparison_status": (
            "PARTIAL" if truncated else "COMPLETE_FOR_REPORTED_BEHAVIOR"
        ),
        "reason": None,
        "presence": "BOTH",
        "changed_fields": changed,
        "source_changed": base["source_sha256"] != target["source_sha256"],
        "base": base,
        "target": target,
    }


def build_source_review_comparison(
    root: Path, base_ref: str, target_ref: str, path: str, *,
    limit: int = 25, symbol: str | None = None,
) -> dict[str, Any]:
    """Pair existing exact-commit source views for one focal review path.

    Identity membership is not behavioral equivalence. When a symbol is
    selected, an additional source-level behavior surface may be compared;
    semantic behavior, runtime execution and test coverage are still not
    inferred. Missing or non-regular entries never become invented empty
    source inventories.
    """

    if not 1 <= limit <= _MAX_LIMIT:
        raise ValueError("source relationship limit must be 1..250")
    if any(not re.fullmatch(r"[0-9a-f]{40}", ref) for ref in (base_ref, target_ref)):
        raise ValueError("source review requires two full 40-character Git SHAs")
    if symbol is not None and not _SYMBOL.fullmatch(symbol):
        raise ValueError("--source-symbol must be one Python identifier")
    path = _safe_path(path)
    if not path.endswith(".py"):
        raise ValueError("--source-path requires a repository-relative .py file")
    base_side = _review_side(root, base_ref, path, limit, symbol)
    target_side = (
        base_side if target_ref == base_ref
        else _review_side(root, target_ref, path, limit, symbol)
    )
    base, target = base_side["relationships"], target_side["relationships"]
    comparisons: dict[str, Any] = {}
    behavior_comparison = None
    if base is not None and target is not None:
        base_target_parsed = base["target_parse_error"] is None
        target_target_parsed = target["target_parse_error"] is None
        base_repo_parsed = base_target_parsed and base["counts"]["parse_failures"] == 0
        target_repo_parsed = target_target_parsed and target["counts"]["parse_failures"] == 0
        for field, identity, entire_repo in (
            ("direct_imports", lambda row: row["module"], False),
            ("direct_importers", lambda row: row["path"], True),
            ("test_references", lambda row: row["path"], True),
            ("top_level_symbols", lambda row: f'{row["kind"]}:{row["name"]}', False),
        ):
            comparisons[field] = _compare_identities(
                base, target, field, identity,
                base_parsed=base_repo_parsed if entire_repo else base_target_parsed,
                target_parsed=target_repo_parsed if entire_repo else target_target_parsed,
            )
        base_symbol, target_symbol = base["symbol_context"], target["symbol_context"]
        if base_symbol is not None and target_symbol is not None:
            for field, identity in (
                ("direct_references", lambda row: row["path"]),
                ("test_candidates", lambda row: f'{row["path"]}::{row["test_name"]}'),
            ):
                comparisons[f"symbol_{field}"] = _compare_identities(
                    base_symbol, target_symbol, field, identity,
                    base_parsed=base_symbol["counts"]["parse_failures"] == 0,
                    target_parsed=target_symbol["counts"]["parse_failures"] == 0,
                )
            if symbol is not None:
                behavior_comparison = _behavior_comparison(base_symbol, target_symbol)
    return {
        "path": path, "symbol": symbol, "base": base_side, "target": target_side,
        "identity_comparisons": comparisons,
        "symbol_behavior_comparison": behavior_comparison,
        "truncated": (
            any(side is not None and side["truncated"] for side in (base, target))
            or (
                behavior_comparison is not None
                and behavior_comparison["comparison_status"] == "PARTIAL"
            )
        ),
        "limits": [
            "Only this focal path receives paired committed source context. Other paths are not compared.",
            "Membership compares returned module, file, kind:name or test identities, not line positions, signatures or full source bodies.",
            "Both means visible at both revisions, not unchanged behavior or identical source.",
            "VISIBLE_ONLY differences are returned-list differences, not established additions or removals.",
            "Even complete identity lists are limited to the underlying syntactic scanner; missing runtime or semantic relationships are NOT ASSESSED.",
            "Absent or non-regular tree entries and unavailable symbol contexts are not compared as empty inventories.",
            "Symbol behavior compares source-level signature, decorators, docstring summary/hash, direct raises/asserts and exact definition source hash; semantic or runtime behavioral equivalence is NOT ASSESSED.",
            "A source-hash difference can be formatting, comments or any body edit; inspect the reported fields and original source.",
            "No uncommitted bytes, test coverage, change safety, transitive impact or authorization are established.",
        ],
    }


_ROUTE_MAX_SOURCE_BYTES = 512 * 1024
_ROUTE_DETAIL_LIMIT = 20
_ROUTE_LIMITS = (
    "Each edge is a Python AST import module-name candidate mapped to exactly one tracked path, not a verified import or runtime dependency.",
    "Module names use the existing root/src and relative-import conventions; package-member candidates may be attributes or re-exports rather than modules actually imported.",
    "The search follows outgoing import candidates only. Conditional, local and type-checking imports are included; dynamic imports, package initialization, reflection and external resolution are NOT ASSESSED.",
    "The first witnessed path is a shortest-hop path in the explored candidate graph, not necessarily a globally shortest or unique dependency path.",
    "A negative or partial result is not proof of independence, absence of cycles, architectural conformance or semantic impact.",
    "No target code or tests are executed, no semantic knowledge is promoted, and no change is authorized.",
)


def _route_path(path: str) -> str:
    """Require an explicit normalized repository-relative Python path."""
    normalized = _safe_path(path)
    if (normalized != path or not path.endswith(".py")
            or "\\" in path or ":" in path or path.startswith("-")
            or any(ord(c) < 32 or ord(c) == 127 for c in path)):
        raise ValueError("source route requires normalized repository-relative .py paths")
    return normalized


def build_source_route(
    root: str | Path, target_ref: str, from_path: str, to_path: str, *,
    max_hops: int = 6, max_files: int = 80,
) -> dict[str, Any]:
    """Find one bounded directed witness in exact-source Python import syntax."""
    if not re.fullmatch(r"[0-9a-f]{40}", target_ref):
        raise ValueError("source route requires a full 40-character Git SHA")
    if not 1 <= max_hops <= 6 or not 1 <= max_files <= 250:
        raise ValueError("source route requires max_hops 1..6 and max_files 1..250")
    start, destination = _route_path(from_path), _route_path(to_path)
    if start == destination:
        raise ValueError("source route requires two distinct source paths")
    with temporary_commit_checkout(Path(root).resolve(), target_ref) as checkout:
        checkout, tracked = verified_tracked_sources(checkout, target_ref)
        for path in (start, destination):
            _source(checkout, tracked, path)
        modules: dict[str, list[str]] = {}
        for path in sorted(tracked):
            if path.endswith(".py"):
                modules.setdefault(_module_for_path(path), []).append(path)
        queue = deque([(start, 0)])
        discovered = {start}
        parent: dict[str, dict[str, Any]] = {}
        failures: list[dict[str, str]] = []
        ambiguities: list[dict[str, Any]] = []
        inspected = 0
        unresolved = 0
        ambiguous_total = 0
        hop_frontier = 0
        found = False
        while queue and inspected < max_files and not found:
            current, depth = queue.popleft()
            inspected += 1
            try:
                if _source(checkout, tracked, current).stat().st_size > _ROUTE_MAX_SOURCE_BYTES:
                    raise ValueError("source exceeds 512 KiB parse budget")
                tree, _, raw, error = _parse(checkout, tracked, current)
            except (OSError, ValueError, RuntimeError, RecursionError) as exc:
                failures.append({"path": current, "reason": str(exc)[:300]})
                continue
            if tree is None or raw is None or error is not None:
                failures.append({"path": current, "reason": (error or "parse unavailable")[:300]})
                continue
            fingerprint = hashlib.sha256(raw).hexdigest()
            # Deterministic source-order candidate expansion. Retain the first
            # witnessed edge to each path; BFS never revisits a discovered path.
            candidates = sorted(
                (line, module, names, type(node).__name__)
                for node in ast.walk(tree)
                if isinstance(node, (ast.Import, ast.ImportFrom))
                for module, line, names in _import_candidates(current, node)
            )
            for line, module, names, syntax_kind in candidates:
                matches = modules.get(module, [])
                if not matches:
                    unresolved += 1
                    continue
                if len(matches) != 1:
                    ambiguous_total += 1
                    if len(ambiguities) < _ROUTE_DETAIL_LIMIT:
                        ambiguities.append({
                            "from_path": current, "line": line, "module_candidate": module,
                            "candidate_path_count": len(matches), "candidate_paths": matches[:_ROUTE_DETAIL_LIMIT],
                        })
                    continue
                next_path = matches[0]
                if next_path in discovered:
                    continue
                discovered.add(next_path)
                parent[next_path] = {
                    "from_path": current, "to_path": next_path, "module_candidate": module,
                    "line": line, "imported_names": list(names), "syntax_kind": syntax_kind,
                    "source_sha256": fingerprint, "evidence_ref": f"file:{current}:line:{line}",
                    "basis": "UNIQUE_TRACKED_MODULE_NAME_CANDIDATE",
                }
                if next_path == destination:
                    found = True
                    break
                if depth + 1 < max_hops:
                    queue.append((next_path, depth + 1))
                else:
                    hop_frontier += 1
        route: list[dict[str, Any]] = []
        if found:
            current = destination
            while current != start:
                edge = parent[current]
                route.append(edge)
                current = edge["from_path"]
            route.reverse()
        budget_exhausted = bool(queue and not found and inspected >= max_files)
        incomplete = bool(failures or ambiguous_total or budget_exhausted)
        return {
            "code": "SEMANTIC_SOURCE_ROUTE",
            "target_ref": target_ref, "from_path": start, "to_path": destination,
            "status": ("FOUND" if found else "NOT_ASSESSED" if incomplete
                       else "NO_ROUTE_FOUND_WITHIN_BOUNDS"),
            "route": route, "hop_count": len(route) if found else None,
            "search": {
                "max_hops": max_hops, "max_files": max_files,
                "source_file_byte_limit": _ROUTE_MAX_SOURCE_BYTES,
                "inspected_files": inspected, "discovered_paths": len(discovered),
                "queued_uninspected_paths": len(queue),
                "hop_frontier_paths": hop_frontier,
                "file_budget_exhausted": budget_exhausted,
                "parse_or_read_failure_total": len(failures),
                "parse_or_read_failures": failures[:_ROUTE_DETAIL_LIMIT],
                "ambiguous_candidate_total": ambiguous_total,
                "ambiguous_candidates": ambiguities,
                "unresolved_candidate_total": unresolved,
                "search_partial": incomplete,
                "detail_limit": _ROUTE_DETAIL_LIMIT,
                "detail_truncated": (len(failures) > _ROUTE_DETAIL_LIMIT
                                     or ambiguous_total > len(ambiguities)
                                     or any(x["candidate_path_count"] > len(x["candidate_paths"])
                                            for x in ambiguities)),
            },
            "runtime_dependency_established": False, "semantic_impact_established": False,
            "tests_executed": False, "action_authorized": False,
            "explicit_limits": list(_ROUTE_LIMITS),
        }
