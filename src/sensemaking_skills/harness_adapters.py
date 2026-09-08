"""P10 explicit harness adapter registry for Agent Skills installation.

Harness adapters are setup metadata only. They map an explicitly selected
coding-agent environment and scope to a filesystem Skill discovery root.
They never inspect which agent is running, choose a Skill, grant execution
authority, or alter Campaign semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class HarnessAdapterError(ValueError):
    """Raised when an explicit harness-adapter request is invalid."""


@dataclass(frozen=True)
class HarnessAdapter:
    """Declared Skill discovery roots for one coding-agent harness."""

    id: str
    label: str
    user_relative: tuple[str, ...]
    project_relative: tuple[str, ...]
    notes: str

    def user_skills_dir(self, *, home: Path | None = None) -> Path:
        root = Path.home() if home is None else Path(home)
        return root.joinpath(*self.user_relative)

    def project_skills_dir(self, project_root: Path) -> Path:
        return Path(project_root).joinpath(*self.project_relative)


@dataclass(frozen=True)
class HarnessDestination:
    """One unique filesystem destination for one or more declared adapters."""

    adapter_ids: tuple[str, ...]
    scope: str
    path: Path

    @property
    def label(self) -> str:
        return "+".join(self.adapter_ids)


# P10 deliberately encodes only documented Skill discovery roots. These paths
# are versioned product metadata, not runtime detection. If a harness changes
# its discovery contract, this registry and its qualification tests must change
# explicitly rather than silently probing or guessing.
HARNESS_ADAPTERS: dict[str, HarnessAdapter] = {
    "generic": HarnessAdapter(
        id="generic",
        label="Portable Agent Skills",
        user_relative=(".agents", "skills"),
        project_relative=(".agents", "skills"),
        notes="Portable Agent Skills filesystem root.",
    ),
    "claude": HarnessAdapter(
        id="claude",
        label="Claude Code",
        user_relative=(".claude", "skills"),
        project_relative=(".claude", "skills"),
        notes="Claude Code personal/project custom Skill roots.",
    ),
    "codex": HarnessAdapter(
        id="codex",
        label="Codex",
        user_relative=(".agents", "skills"),
        project_relative=(".agents", "skills"),
        notes="Codex Agent Skills user/project discovery roots.",
    ),
    "opencode": HarnessAdapter(
        id="opencode",
        label="OpenCode",
        user_relative=(".config", "opencode", "skills"),
        project_relative=(".opencode", "skills"),
        notes="OpenCode native global/project Skill roots.",
    ),
}

# Preserve the existing public target name while making the canonical product
# concept explicit. `agents` and `generic` resolve to the same adapter.
HARNESS_ALIASES: dict[str, str] = {
    "agents": "generic",
}

CANONICAL_HARNESS_TARGETS: tuple[str, ...] = tuple(HARNESS_ADAPTERS)
ALL_HARNESS_TARGETS: tuple[str, ...] = (
    "generic",
    "claude",
    "codex",
    "opencode",
)


def canonical_harness_id(target: str) -> str:
    """Return the canonical explicit adapter id or fail closed."""
    canonical = HARNESS_ALIASES.get(target, target)
    if canonical not in HARNESS_ADAPTERS:
        raise HarnessAdapterError(f"Unknown harness target: {target}")
    return canonical


def get_harness_adapter(target: str) -> HarnessAdapter:
    """Return one declared adapter; no runtime harness detection is performed."""
    return HARNESS_ADAPTERS[canonical_harness_id(target)]


def resolve_harness_destinations(
    target: str,
    *,
    scope: str = "user",
    project_root: Path | None = None,
    home: Path | None = None,
) -> tuple[HarnessDestination, ...]:
    """Resolve explicit harness/scope metadata to unique filesystem roots.

    `target="all"` expands the canonical adapter set and deduplicates shared
    physical roots. Codex and the portable generic adapter intentionally share
    `.agents/skills`, so `all` writes that location once while preserving both
    logical adapter ids in the returned metadata.
    """
    if scope not in {"user", "project"}:
        raise HarnessAdapterError(f"Unknown harness scope: {scope}")

    if scope == "project":
        if project_root is None:
            raise HarnessAdapterError(
                "--project-root is required when --scope=project"
            )
        root = Path(project_root).expanduser()
        if not root.exists() or not root.is_dir():
            raise HarnessAdapterError(
                f"Project root does not exist or is not a directory: {root}"
            )
    else:
        root = None

    target_ids = ALL_HARNESS_TARGETS if target == "all" else (target,)

    ordered_paths: list[Path] = []
    ids_by_path: dict[Path, list[str]] = {}
    for target_id in target_ids:
        adapter = get_harness_adapter(target_id)
        path = (
            adapter.user_skills_dir(home=home)
            if scope == "user"
            else adapter.project_skills_dir(root)  # type: ignore[arg-type]
        )
        # Lexical absolute paths are sufficient here; setup is explicitly
        # user-directed and must not silently dereference/create through a
        # different harness root merely because aliases or symlinks exist.
        path = path.expanduser().absolute()
        if path not in ids_by_path:
            ordered_paths.append(path)
            ids_by_path[path] = []
        canonical = adapter.id
        if canonical not in ids_by_path[path]:
            ids_by_path[path].append(canonical)

    return tuple(
        HarnessDestination(
            adapter_ids=tuple(ids_by_path[path]),
            scope=scope,
            path=path,
        )
        for path in ordered_paths
    )
