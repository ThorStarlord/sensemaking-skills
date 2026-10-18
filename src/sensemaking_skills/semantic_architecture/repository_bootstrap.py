"""Read-only, source-pinned repository orientation and structural knowledge.

This module handles *paths and syntax*, not architecture decisions. An entry in
a Git tree does not prove that a component owns a product capability; directory
containment does not prove a runtime dependency. Callers must first validate a
clean, exact Git HEAD through verified_tracked_sources.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path

from .knowledge import KnowledgeClaim, KnowledgeRelation, stable_id

_SOURCE_ROOTS = frozenset({
    "src", "lib", "app", "apps", "packages", "backend", "frontend",
    "server", "client", "tests", "test",
})
_LANGUAGES = {
    ".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".rs": "Rust",
    ".cs": "C#", ".go": "Go", ".java": "Java", ".kt": "Kotlin",
    ".gd": "GDScript", ".sql": "SQL", ".rb": "Ruby", ".php": "PHP",
    ".cpp": "C++", ".c": "C", ".md": "Markdown",
}
_MANIFESTS = frozenset({
    "pyproject.toml", "package.json", "Cargo.toml", "go.mod",
    "pom.xml", "build.gradle", "build.gradle.kts", "requirements.txt",
    "composer.json", "Gemfile", "global.json", "CMakeLists.txt",
})
_DOCS = frozenset({
    "README.md", "STATUS.md", "CONTEXT.md", "AGENTS.md",
    "docs/product-strategy.md", "docs/persistent-semantic-stewardship-plan.md",
    ".sensemaking/intent.md", ".sensemaking/context.md",
    ".sensemaking/invariants.md",
})
_SKIP_PARTS = frozenset({
    ".git", ".venv", "venv", "node_modules", "dist", "build",
    "__pycache__", ".next", "vendor", ".tox",
})
_MAX_SOURCE_BYTES = 524288


def _candidate(path: str) -> bool:
    """Select tracked source paths without opening arbitrary files."""
    parts = Path(path).parts
    return bool(parts) and not any(p in _SKIP_PARTS for p in parts)


def _safe_file(root: Path, path: str) -> Path:
    """Reject symlinks, traversal, and oversized/unreadable evidence inputs."""
    if not path or "\\" in path or Path(path).is_absolute() or ".." in Path(path).parts:
        raise ValueError(f"unsafe tracked source path: {path}")
    node = root
    for part in Path(path).parts:
        node = node / part
        if node.is_symlink():
            raise ValueError(f"symlink source refused: {path}")
    resolved = node.resolve()
    if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
        raise ValueError(f"source missing or unsafe: {path}")
    if resolved.stat().st_size > _MAX_SOURCE_BYTES:
        raise ValueError(f"oversized bootstrap source: {path}")
    return resolved


def _rank(path: str) -> tuple[int, str]:
    if path in _DOCS or path in _MANIFESTS:
        return (0, path)
    parts = Path(path).parts
    if parts[0] in _SOURCE_ROOTS:
        return (1, path)
    if path.startswith("docs/adr/") and path.endswith(".md"):
        return (2, path)
    if Path(path).name in _MANIFESTS:
        return (3, path)
    return (4, path)


def _bounded_paths(tracked: set[str], max_files: int) -> tuple[list[str], int]:
    if not 1 <= max_files <= 20000:
        raise ValueError("max_files must be 1..20000")
    paths = sorted((p for p in tracked if _candidate(p)), key=_rank)
    return paths[:max_files], len(paths)


def orient_repository(
    root: Path, tracked: set[str], *,
    repository: str, target_ref: str,
    max_files: int = 5000, sample_limit: int = 16,
) -> dict:
    """A compact, read-only index of tracked names, never inferred product truth."""
    if not repository.strip():
        raise ValueError("explicit repository identity is required")
    if not 1 <= sample_limit <= 50:
        raise ValueError("sample_limit must be 1..50")
    paths, eligible_count = _bounded_paths(tracked, max_files)
    directories = Counter()
    languages = Counter()
    manifests: list[str] = []
    entry_docs: list[str] = []
    adr_count = 0
    source_files: list[str] = []
    test_files: list[str] = []
    for path in paths:
        parts = Path(path).parts
        directories[parts[0]] += 1
        language = _LANGUAGES.get(Path(path).suffix.lower())
        if language is not None:
            languages[language] += 1
        if Path(path).name in _MANIFESTS:
            manifests.append(path)
        if path in _DOCS:
            entry_docs.append(path)
        if path.startswith("docs/adr/") and path.endswith(".md"):
            adr_count += 1
        if parts[0] in _SOURCE_ROOTS and Path(path).suffix.lower() in _LANGUAGES:
            (test_files if parts[0] in {"test", "tests"} or Path(path).name.startswith("test_") else source_files).append(path)
    limited = len(paths) < eligible_count
    return {
        "repository": repository.strip(), "target_ref": target_ref,
        "tracked_file_count": len(tracked),
        "eligible_file_count": eligible_count,
        "inspected_file_count": len(paths),
        "path_inventory_truncated": limited,
        "top_level": [
            {"path": name, "file_count": count}
            for name, count in sorted(directories.items(), key=lambda x: (-x[1], x[0]))[:sample_limit]
        ],
        "language_file_counts": dict(sorted(languages.items())),
        "entry_documents": sorted(entry_docs),
        "manifest_examples": sorted(manifests)[:sample_limit],
        "manifest_count": len(manifests),
        "adr_path_count": adr_count,
        "source_examples": sorted(source_files)[:sample_limit],
        "test_examples": sorted(test_files)[:sample_limit],
        "source_example_count_in_scope": len(source_files),
        "test_example_count_in_scope": len(test_files),
        "source_scope": [
            "Git-tracked path names in an exact clean checkout",
            "Known document and manifest filenames; names not document contents",
            "Filename extensions and path prefixes, not compiled or executed code",
        ],
        "limits": [
            "Path inventory may be truncated; examples are not exhaustive.",
            "Unknown document layouts and unsupported languages are NOT ASSESSED.",
            "Path placement does not establish architectural responsibility, test coverage, or owner intent.",
            "Read source documents and code before relying on consequential interpretations.",
        ],
        "semantic_truth_established": False,
        "action_authorized": False,
    }


def structural_records(
    root: Path, tracked: set[str], *,
    max_structural_files: int = 600,
) -> tuple[list[KnowledgeClaim], list[KnowledgeRelation], bool]:
    """Create evidence-backed file/directory placement edges, not dependencies.

    Root/docs manifests and Python files under recognized source/test roots are
    represented. The scope is intentionally smaller than a whole-program graph.
    """
    if not 1 <= max_structural_files <= 2000:
        raise ValueError("max_structural_files must be 1..2000")
    eligible = [
        p for p in tracked if _candidate(p) and (
            p in _DOCS or Path(p).name in _MANIFESTS
            or (Path(p).parts[0] in _SOURCE_ROOTS and p.endswith(".py"))
        )
    ]
    eligible.sort(key=_rank)
    selected = eligible[:max_structural_files]
    claims: dict[str, KnowledgeClaim] = {}
    relations: dict[str, KnowledgeRelation] = {}
    for path in selected:
        source = _safe_file(root, path)
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        file_id = stable_id("file", path)
        reference = f"file:{path}"
        claims[file_id] = KnowledgeClaim(
            id=file_id, kind="source", statement=path,
            epistemic_status="observed", authority_kind="mechanical",
            authority_ref="git:tracked-file", source_ref=reference,
            evidence_refs=(reference,),
            attributes={"scope": "committed file existence, not content semantics",
                        "source_sha256": {path: digest}, "authority_verified": False},
        )
        parts = Path(path).parts
        if len(parts) < 2:
            continue
        child_id = file_id
        for depth in range(len(parts) - 1, 0, -1):
            directory = Path(*parts[:depth]).as_posix()
            directory_id = stable_id("directory", directory)
            if directory_id not in claims:
                claims[directory_id] = KnowledgeClaim(
                    id=directory_id, kind="component",
                    statement=f"Tracked directory: {directory}",
                    epistemic_status="observed", authority_kind="mechanical",
                    authority_ref="git:tracked-path",
                    source_ref=reference, evidence_refs=(reference,),
                    attributes={"scope": "path segment only; not a verified architectural component",
                                "authority_verified": False},
                )
            edge_id = stable_id("path-containment", child_id, directory_id)
            if edge_id not in relations:
                relations[edge_id] = KnowledgeRelation(
                    id=edge_id, subject=child_id, predicate="contained_in",
                    object=directory_id, epistemic_status="observed",
                    derivation="mechanical", source_ref=reference,
                    evidence_refs=(reference,),
                    attributes={"scope": "lexical tracked path placement only",
                                "source_sha256": {path: digest}},
                )
            child_id = directory_id
    return (
        [claims[k] for k in sorted(claims)],
        [relations[k] for k in sorted(relations)],
        len(eligible) > len(selected),
    )
