r"""
Setup command to install sensemaking-skills SKILL.md files to explicit
agent-discoverable locations.

P10 adds first-class filesystem adapters for:
- portable Agent Skills / generic agents;
- Claude Code;
- Codex;
- OpenCode;
- explicit custom directories.

The setup layer never auto-detects the active harness. The caller chooses the
harness and user/project scope explicitly; deterministic code only maps that
choice to a declared filesystem discovery root and copies exact packaged Skill
trees there.

Source resolution:
1. Packaged skill trees (``sensemaking_skills/skill_trees``) -- the
   wheel-installed case.
2. Repository-root ``skills/`` -- editable/source-checkout development.

Drift detection remains fail closed: existing divergent copies are reported and
are never silently overwritten. Only ``--force`` replaces them.
"""

from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path
from typing import List, Tuple

from .harness_adapters import (
    HarnessAdapterError,
    resolve_harness_destinations,
)


class SkillsSetupError(Exception):
    """Raised when skill setup fails."""


def get_package_skills_dir() -> Path:
    """Get the Skill source directory without assuming a source checkout."""
    try:
        from importlib.resources import files

        packaged = files("sensemaking_skills") / "skill_trees"
        if packaged.is_dir():
            return Path(str(packaged))
    except Exception:
        pass

    package_dir = Path(__file__).parent.parent.parent
    skills_dir = package_dir / "skills"
    if not skills_dir.exists():
        raise SkillsSetupError(
            f"Skills directory not found at {skills_dir}. "
            "This may indicate an incomplete installation."
        )
    return skills_dir


def get_agents_skills_dir() -> Path:
    """Backward-compatible portable Agent Skills user directory."""
    destination = resolve_harness_destinations("generic", scope="user")[0]
    return destination.path


def get_claude_personal_skills_dir() -> Path:
    """Return the declared Claude Code personal Skill discovery root."""
    return resolve_harness_destinations("claude", scope="user")[0].path


def get_codex_skills_dir() -> Path:
    """Return the declared Codex user Skill discovery root."""
    return resolve_harness_destinations("codex", scope="user")[0].path


def get_opencode_skills_dir() -> Path:
    """Return the declared OpenCode native global Skill discovery root."""
    return resolve_harness_destinations("opencode", scope="user")[0].path


def get_claude_code_skills_dir() -> Path:
    """Backward-compatible legacy Claude/Superpowers plugin-cache target.

    This is intentionally *not* the P10 Claude Code adapter. The first-class
    Claude adapter uses ``~/.claude/skills``. This function remains only so the
    pre-P10 ``claude-superpowers`` target keeps its old behavior.
    """
    home = Path.home()
    return (
        home
        / ".claude"
        / "plugins"
        / "cache"
        / "claude-plugins-official"
        / "superpowers"
        / "5.1.0"
        / "skills"
    )


def find_skills_in_package(skills_dir: Path) -> List[str]:
    """Find Skill folders in deterministic name order."""
    if not skills_dir.exists():
        return []
    skill_names = []
    for item in skills_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skill_names.append(item.name)
    return sorted(skill_names)


def _skill_tree_fingerprint(skill_dir: Path) -> dict[str, str]:
    """Map every regular file in a Skill tree to its SHA-256 digest."""
    fingerprint: dict[str, str] = {}
    if not skill_dir.is_dir():
        return fingerprint
    for path in sorted(skill_dir.rglob("*")):
        if path.is_file():
            rel = path.relative_to(skill_dir).as_posix()
            fingerprint[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return fingerprint


def skill_state(src_skill: Path, dest_skill: Path) -> str:
    """Classify destination as ``missing``, ``current``, or ``different``."""
    if not dest_skill.exists():
        return "missing"
    if _skill_tree_fingerprint(src_skill) == _skill_tree_fingerprint(dest_skill):
        return "current"
    return "different"


def copy_skill(
    src_skill_dir: Path,
    dest_skills_dir: Path,
    skill_name: str,
    dry_run: bool = False,
    force: bool = False,
) -> Tuple[bool, str]:
    """Copy one Skill tree with explicit drift handling."""
    src_skill = src_skill_dir / skill_name
    dest_skill = dest_skills_dir / skill_name

    if not (src_skill / "SKILL.md").exists():
        return False, f"Source SKILL.md not found: {src_skill / 'SKILL.md'}"

    state = skill_state(src_skill, dest_skill)
    if state == "current":
        return True, f"Current (already matches packaged version): {skill_name}"

    if state == "different" and not force:
        return (
            False,
            f"Different from packaged version: {skill_name} "
            "(installed copy diverged; use --force to overwrite)",
        )

    if dest_skill.exists() and not force:
        return False, f"Destination already exists: {dest_skill} (use --force to overwrite)"

    if dry_run:
        action = "Would replace" if dest_skill.exists() else "Would copy"
        return True, f"[DRY-RUN] {action} {src_skill} -> {dest_skill}"

    try:
        if dest_skill.exists():
            shutil.rmtree(dest_skill)
        shutil.copytree(src_skill, dest_skill)
        return True, f"Copied {skill_name} -> {dest_skill}"
    except Exception as exc:
        return False, f"Failed to copy {skill_name}: {exc}"


def _resolve_destinations(
    *,
    target: str,
    scope: str,
    skills_dir: str | None,
    project_root: str | Path | None,
) -> list[tuple[str, Path]]:
    """Resolve the explicit setup request; infer no harness from the machine."""
    if target == "custom":
        if scope != "user":
            raise SkillsSetupError(
                "--scope applies to harness adapters; use --target=custom "
                "with the exact --skills-dir instead"
            )
        if project_root is not None:
            raise SkillsSetupError(
                "--project-root is not valid with --target=custom"
            )
        if not skills_dir:
            raise SkillsSetupError("--skills-dir required when using custom target")
        return [("custom", Path(skills_dir).expanduser().absolute())]

    if skills_dir is not None:
        raise SkillsSetupError("--skills-dir is only valid with --target=custom")

    if target == "claude-superpowers":
        if scope != "user" or project_root is not None:
            raise SkillsSetupError(
                "legacy claude-superpowers target supports user scope only"
            )
        return [("claude-superpowers-legacy", get_claude_code_skills_dir())]

    try:
        resolved = resolve_harness_destinations(
            target,
            scope=scope,
            project_root=(Path(project_root) if project_root is not None else None),
        )
    except HarnessAdapterError as exc:
        raise SkillsSetupError(str(exc)) from exc

    destinations = [(item.label, item.path) for item in resolved]

    # Preserve the old `--target all` behavior as a compatibility superset:
    # user-scope `all` still includes the historical Superpowers cache while
    # also adding the first-class Claude/Codex/OpenCode roots. Project-scope
    # `all` contains only project-native P10 adapters.
    if target == "all" and scope == "user":
        legacy = get_claude_code_skills_dir().expanduser().absolute()
        if all(path != legacy for _, path in destinations):
            destinations.append(("claude-superpowers-legacy", legacy))

    return destinations


def setup_skills(
    target: str = "agents",
    skills_dir: str | None = None,
    dry_run: bool = False,
    force: bool = False,
    verbose: bool = False,
    scope: str = "user",
    project_root: str | Path | None = None,
) -> bool:
    """Install packaged Skill trees to explicitly selected discovery roots.

    Canonical P10 targets:
    - ``generic`` / compatibility alias ``agents``: ``.agents/skills``;
    - ``claude``: ``.claude/skills``;
    - ``codex``: ``.agents/skills``;
    - ``opencode``: native OpenCode Skill root;
    - ``all``: all unique canonical roots (plus the legacy Superpowers cache
      for user scope to preserve pre-P10 behavior);
    - ``custom``: exact caller-supplied directory.

    ``scope=user`` selects user/global roots. ``scope=project`` requires an
    explicit project root and selects project-local discovery roots. No active
    harness is detected automatically.
    """
    try:
        package_skills_dir = get_package_skills_dir()
        skill_names = find_skills_in_package(package_skills_dir)
        if not skill_names:
            raise SkillsSetupError(f"No skills found in {package_skills_dir}")

        destinations = _resolve_destinations(
            target=target,
            scope=scope,
            skills_dir=skills_dir,
            project_root=project_root,
        )
        if not destinations:
            raise SkillsSetupError(f"No destination resolved for target: {target}")

        if verbose:
            print(f"Found {len(skill_names)} skills: {', '.join(skill_names)}")
            print(f"Explicit target: {target}")
            print(f"Scope: {scope}")

        all_success = True
        for dest_name, dest_dir in destinations:
            print(f"\n{'=' * 60}")
            print(f"Installing to: {dest_name}")
            print(f"Scope: {scope}")
            print(f"Directory: {dest_dir}")
            print(f"{'=' * 60}")

            if not dry_run and not dest_dir.exists():
                dest_dir.mkdir(parents=True, exist_ok=True)
                if verbose:
                    print(f"Created directory: {dest_dir}")

            for skill_name in skill_names:
                success, message = copy_skill(
                    package_skills_dir,
                    dest_dir,
                    skill_name,
                    dry_run=dry_run,
                    force=force,
                )
                symbol = "+" if success else "x"
                print(f"  [{symbol}] {message}")
                if not success:
                    all_success = False

        print(f"\n{'=' * 60}")
        print("Summary")
        print(f"{'=' * 60}")
        if dry_run:
            print("[DRY-RUN MODE] No files were actually installed.")
        print(f"Skills to install: {', '.join(skill_names)}")
        print(f"Target locations: {len(destinations)}")
        print(f"Requested adapter target: {target}")
        print(f"Requested scope: {scope}")

        if all_success:
            print("\nStatus: SUCCESS")
            print(
                "\nReload/restart the selected harness if needed; use its "
                "normal Skill discovery/invocation surface."
            )
            print("The setup command does not select or invoke any Skill.")
            print("\nThe Python package is still required for Skill helper commands:")
            print("  pip install sensemaking-skills")
        else:
            print("\nStatus: PARTIAL FAILURE - Some installations failed")
            print("Existing divergent Skill copies are reported above and are")
            print("NOT overwritten. Use --force to deliberately replace them.")

        return all_success

    except SkillsSetupError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return False
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return False
