"""Deterministic repository probes for mechanically decidable semantic facts.

Probe outputs are observations with declared scope/completeness/currentness. They
never classify architecture quality, select a responsibility, or decide what a
repository fact means for the user's goal.
"""

from __future__ import annotations

import ast
import fnmatch
import hashlib
import json
import tomllib
from pathlib import Path
from typing import Iterable

from .models import (
    Completeness,
    Currentness,
    ObservationKind,
    SemanticDiagnostic,
    SemanticObservation,
    SemanticProbeResult,
)

_SKIP_PARTS = {".git", ".hg", ".svn", "__pycache__", ".venv", "venv", "node_modules"}


def _observation_id(*parts: str) -> str:
    digest = hashlib.sha256("\0".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"OBS-{digest}"


def _iter_regular_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*"), key=lambda value: value.as_posix()):
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if any(part in _SKIP_PARTS for part in relative.parts):
            continue
        if path.is_symlink() or not path.is_file():
            continue
        yield path


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _result(
    *,
    probe_id: str,
    target_ref: str,
    scope: str,
    observations: list[SemanticObservation],
    diagnostics: list[SemanticDiagnostic],
    completeness: Completeness,
) -> SemanticProbeResult:
    return SemanticProbeResult(
        probe_id=probe_id,
        target_ref=target_ref,
        scope=scope,
        completeness=completeness,
        observations=tuple(observations),
        diagnostics=tuple(diagnostics),
    )


def probe_file_containment(repo_root: str | Path, *, target_ref: str) -> SemanticProbeResult:
    """Enumerate regular, non-symlink files and their immediate directories."""
    root = Path(repo_root).resolve()
    observations: list[SemanticObservation] = []
    for path in _iter_regular_files(root):
        rel = _relative(root, path)
        parent = Path(rel).parent.as_posix()
        if parent == ".":
            parent = "<repository-root>"
        observations.append(
            SemanticObservation(
                id=_observation_id("file_containment", rel, parent),
                kind=ObservationKind.FILE_CONTAINMENT,
                subject=rel,
                predicate="contained_by_directory",
                object=parent,
                evidence_refs=(f"file:{rel}",),
                source="filesystem_enumeration",
                scope="regular non-symlink files excluding known generated/vendor roots",
                completeness=Completeness.COMPLETE,
                currentness=Currentness.OBSERVED_CURRENT,
                target_ref=target_ref,
            )
        )
    return _result(
        probe_id="file-containment-v1",
        target_ref=target_ref,
        scope="regular non-symlink files excluding known generated/vendor roots",
        observations=observations,
        diagnostics=[],
        completeness=Completeness.COMPLETE,
    )


def probe_python_imports(repo_root: str | Path, *, target_ref: str) -> SemanticProbeResult:
    """Parse Python source files and report syntactic import statements.

    A parse failure makes the result partial. An import observation establishes
    only that the syntax is present in the inspected bytes; it does not prove a
    runtime dependency or an architectural violation.
    """
    root = Path(repo_root).resolve()
    observations: list[SemanticObservation] = []
    diagnostics: list[SemanticDiagnostic] = []
    inspected = 0
    failed = 0
    for path in _iter_regular_files(root):
        if path.suffix != ".py":
            continue
        inspected += 1
        rel = _relative(root, path)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        except (OSError, UnicodeError, SyntaxError) as exc:
            failed += 1
            diagnostics.append(
                SemanticDiagnostic(
                    "PYTHON_IMPORT_PARSE_FAILED",
                    f"could not parse {rel}: {exc}",
                    path=rel,
                )
            )
            continue
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                prefix = "." * node.level
                base = node.module or ""
                modules.append(prefix + base)
            for module in modules:
                observations.append(
                    SemanticObservation(
                        id=_observation_id("python_import", rel, module, str(getattr(node, "lineno", 0))),
                        kind=ObservationKind.PYTHON_IMPORT,
                        subject=rel,
                        predicate="contains_import_syntax",
                        object=module,
                        evidence_refs=(f"file:{rel}:line:{getattr(node, 'lineno', 0)}",),
                        source="python_ast",
                        scope="syntactically parseable Python files",
                        completeness=Completeness.COMPLETE,
                        currentness=Currentness.OBSERVED_CURRENT,
                        target_ref=target_ref,
                        metadata={"line": getattr(node, "lineno", 0)},
                    )
                )
    completeness = Completeness.PARTIAL if failed else Completeness.COMPLETE
    diagnostics.append(
        SemanticDiagnostic(
            "PYTHON_IMPORT_SCOPE",
            f"inspected {inspected} Python files; parse failures: {failed}",
        )
    )
    return _result(
        probe_id="python-imports-v1",
        target_ref=target_ref,
        scope="Python files outside excluded generated/vendor roots",
        observations=observations,
        diagnostics=diagnostics,
        completeness=completeness,
    )


def _pyproject_dependencies(path: Path) -> list[tuple[str, str]]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    project = data.get("project") if isinstance(data, dict) else None
    dependencies = project.get("dependencies", []) if isinstance(project, dict) else []
    result: list[tuple[str, str]] = []
    if isinstance(dependencies, list):
        result.extend(("project.dependencies", str(item)) for item in dependencies if str(item).strip())
    optional = project.get("optional-dependencies", {}) if isinstance(project, dict) else {}
    if isinstance(optional, dict):
        for group, values in optional.items():
            if isinstance(values, list):
                result.extend((f"project.optional-dependencies.{group}", str(item)) for item in values if str(item).strip())
    return result


def _package_json_dependencies(path: Path) -> list[tuple[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    result: list[tuple[str, str]] = []
    if not isinstance(data, dict):
        return result
    for field in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        values = data.get(field, {})
        if not isinstance(values, dict):
            continue
        for name, version in sorted(values.items()):
            result.append((field, f"{name}@{version}"))
    return result


def _requirements_dependencies(path: Path) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("-"):
            continue
        result.append(("requirements", stripped))
    return result


def probe_manifest_dependencies(repo_root: str | Path, *, target_ref: str) -> SemanticProbeResult:
    """Report dependency declarations from supported manifest formats."""
    root = Path(repo_root).resolve()
    observations: list[SemanticObservation] = []
    diagnostics: list[SemanticDiagnostic] = []
    supported = {"pyproject.toml", "package.json", "requirements.txt"}
    manifests = [path for path in _iter_regular_files(root) if path.name in supported]
    failed = 0
    for path in manifests:
        rel = _relative(root, path)
        try:
            if path.name == "pyproject.toml":
                dependencies = _pyproject_dependencies(path)
            elif path.name == "package.json":
                dependencies = _package_json_dependencies(path)
            else:
                dependencies = _requirements_dependencies(path)
        except (OSError, UnicodeError, ValueError, tomllib.TOMLDecodeError, json.JSONDecodeError) as exc:
            failed += 1
            diagnostics.append(
                SemanticDiagnostic(
                    "MANIFEST_PARSE_FAILED",
                    f"could not parse {rel}: {exc}",
                    path=rel,
                )
            )
            continue
        for field, dependency in dependencies:
            observations.append(
                SemanticObservation(
                    id=_observation_id("manifest_dependency", rel, field, dependency),
                    kind=ObservationKind.MANIFEST_DEPENDENCY,
                    subject=rel,
                    predicate="declares_dependency",
                    object=dependency,
                    evidence_refs=(f"file:{rel}",),
                    source=f"manifest_parser:{field}",
                    scope="supported dependency declaration fields",
                    completeness=Completeness.COMPLETE,
                    currentness=Currentness.OBSERVED_CURRENT,
                    target_ref=target_ref,
                    metadata={"manifest_field": field},
                )
            )
    completeness = Completeness.PARTIAL if failed else Completeness.COMPLETE
    diagnostics.append(
        SemanticDiagnostic(
            "MANIFEST_DEPENDENCY_SCOPE",
            f"supported manifests discovered: {len(manifests)}; parse failures: {failed}",
        )
    )
    return _result(
        probe_id="manifest-dependencies-v1",
        target_ref=target_ref,
        scope="pyproject.toml, package.json, and requirements.txt dependency declarations",
        observations=observations,
        diagnostics=diagnostics,
        completeness=completeness,
    )


def probe_exact_search(
    repo_root: str | Path,
    *,
    target_ref: str,
    pattern: str,
    include_glob: str = "*",
) -> SemanticProbeResult:
    """Search literal text across UTF-8 regular files in a declared scope.

    Completeness is COMPLETE only for the explicit scope: UTF-8 decodable files
    selected by the glob and excluding generated/vendor roots. The result does
    not establish absence from binary files, runtime state, generated outputs,
    external systems, or ignored roots.
    """
    if not pattern:
        raise ValueError("exact-search pattern must be non-empty")
    root = Path(repo_root).resolve()
    observations: list[SemanticObservation] = []
    diagnostics: list[SemanticDiagnostic] = []
    inspected = 0
    skipped_non_utf8 = 0
    matched_files: list[str] = []
    for path in _iter_regular_files(root):
        rel = _relative(root, path)
        if include_glob not in {"*", "**/*"} and not fnmatch.fnmatch(rel, include_glob):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            skipped_non_utf8 += 1
            continue
        inspected += 1
        for line_number, line in enumerate(text.splitlines(), start=1):
            if pattern not in line:
                continue
            matched_files.append(rel)
            observations.append(
                SemanticObservation(
                    id=_observation_id("exact_search", rel, str(line_number), pattern),
                    kind=ObservationKind.EXACT_SEARCH_MATCH,
                    subject=rel,
                    predicate="contains_literal_text",
                    object=pattern,
                    evidence_refs=(f"file:{rel}:line:{line_number}",),
                    source="literal_utf8_search",
                    scope=f"UTF-8 files matching {include_glob!r}",
                    completeness=Completeness.COMPLETE,
                    currentness=Currentness.OBSERVED_CURRENT,
                    target_ref=target_ref,
                    metadata={"line": line_number},
                )
            )
    summary_evidence = tuple(f"file:{rel}" for rel in sorted(set(matched_files)))
    observations.append(
        SemanticObservation(
            id=_observation_id("exact_search_summary", include_glob, pattern, str(len(observations))),
            kind=ObservationKind.EXACT_SEARCH_SUMMARY,
            subject="<repository-scope>",
            predicate="literal_match_count",
            object=str(len(observations)),
            evidence_refs=summary_evidence,
            source="literal_utf8_search",
            scope=f"UTF-8 files matching {include_glob!r}; generated/vendor roots excluded",
            completeness=Completeness.COMPLETE,
            currentness=Currentness.OBSERVED_CURRENT,
            target_ref=target_ref,
            metadata={
                "pattern": pattern,
                "inspected_utf8_files": inspected,
                "skipped_non_utf8_files": skipped_non_utf8,
            },
        )
    )
    diagnostics.append(
        SemanticDiagnostic(
            "EXACT_SEARCH_SCOPE",
            f"inspected {inspected} UTF-8 files; skipped non-UTF-8/unreadable files: {skipped_non_utf8}",
        )
    )
    return _result(
        probe_id="exact-search-v1",
        target_ref=target_ref,
        scope=f"UTF-8 files matching {include_glob!r}; generated/vendor roots excluded",
        observations=observations,
        diagnostics=diagnostics,
        completeness=Completeness.COMPLETE,
    )
