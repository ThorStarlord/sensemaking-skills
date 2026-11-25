"""Mechanical source relationships for one committed Python path.

This module answers a bounded pre-change question: which tracked Python files
import the target, which tests reference it, what public symbols does it
define, and which repository files does it import? It reads a clean temporary
checkout of one exact Git revision and parses bytes with ``ast``.

It does not establish runtime dependency, call order, test coverage, semantic
impact or change authorization. Dynamic imports, reflection, non-Python
references and runtime-only coupling are not assessed.
"""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

from .knowledge_sources import temporary_commit_checkout

_MAX_LIMIT = 250
_LIMITS = (
    "Python AST import syntax and top-level definitions only; runtime imports, "
    "reflection and call order are NOT ASSESSED.",
    "Importer and test entries are syntactic references, not proof of runtime use "
    "or test coverage.",
    "Only tracked Python files at the exact revision are inspected; non-Python "
    "references and untracked bytes are not represented.",
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


def _import_candidates(path: str, node: ast.AST) -> list[tuple[str, int, tuple[str, ...]]]:
    """Return absolute module candidates, line and imported names for an import node."""

    candidates: list[tuple[str, int, tuple[str, ...]]] = []
    if isinstance(node, ast.Import):
        for alias in node.names:
            candidates.append((alias.name, node.lineno, ()))
    elif isinstance(node, ast.ImportFrom):
        package = _package_for_path(path)
        level = node.level or 0
        if level:
            if level - 1 > len(package):
                return []
            package = package[: len(package) - (level - 1)]
            base = ".".join(filter(None, [*package, *(node.module or "").split(".")]))
        else:
            base = node.module or ""
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


def _parse(path: Path, relative: str) -> tuple[ast.AST | None, str | None, bytes | None, str | None]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
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
            package = _package_for_path(path)
            level = node.level or 0
            if level:
                if level - 1 > len(package):
                    total += 1
                    continue
                package = package[: len(package) - (level - 1)]
                base = ".".join(filter(None, [*package, *(node.module or "").split(".")]))
            else:
                base = node.module or ""
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


def build_source_relationships(
    root: str | Path, target_ref: str, path: str, *, limit: int = 50,
) -> dict[str, Any]:
    """Build a bounded source-relationship view for one committed Python file."""

    if not 1 <= limit <= _MAX_LIMIT:
        raise ValueError("source relationship limit must be 1..250")
    target_path = _safe_path(path)
    if not target_path.endswith(".py"):
        raise ValueError("source relationships currently support one tracked .py file")
    root_dir = Path(root).resolve()
    with temporary_commit_checkout(root_dir, target_ref) as checkout:
        tracked = {
            item.relative_to(checkout).as_posix()
            for item in checkout.rglob("*") if item.is_file()
        }
        if target_path not in tracked:
            raise ValueError("target path is not a tracked file at the selected revision")
        target_file = checkout / target_path
        target_tree, target_source, target_raw, target_error = _parse(target_file, target_path)
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
            tree, source, _, error = _parse(checkout / candidate, candidate)
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
        "target_parse_error": target_error,
        "parse_failures": parse_failures[:limit],
        "coverage_status": coverage_status,
        "truncated": truncated,
        "limits": list(_LIMITS),
    }
