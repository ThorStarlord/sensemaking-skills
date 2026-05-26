r"""
Setup command to install sensemaking-skills SKILL.md files to agent-discoverable locations.

This module handles copying SKILL.md files from the package to:
- ~/.agents/skills (or C:\Users\*\.agents\skills on Windows)
- Claude Code/Superpowers plugin cache (optional)

Skills are copied with their original folder names:
- using-sensemaking/SKILL.md
- repo-sensemaker/SKILL.md
- workflow-planner/SKILL.md
"""

import sys
import shutil
from pathlib import Path
from typing import List, Tuple


class SkillsSetupError(Exception):
    """Raised when skill setup fails."""
    pass


def get_package_skills_dir() -> Path:
    """Get the path to skills directory in the installed package."""
    # The skills are in the repo root, not in the package directory
    # We need to find them relative to this file
    package_dir = Path(__file__).parent.parent.parent  # Go up from src/sensemaking_skills/
    skills_dir = package_dir / "skills"

    if not skills_dir.exists():
        raise SkillsSetupError(
            f"Skills directory not found at {skills_dir}. "
            "This may indicate an incomplete installation."
        )

    return skills_dir


def get_agents_skills_dir() -> Path:
    """Get the default .agents/skills directory for the current platform."""
    home = Path.home()
    agents_skills = home / ".agents" / "skills"
    return agents_skills


def get_claude_code_skills_dir() -> Path:
    """Get the Claude Code / Superpowers plugin skills directory."""
    # This is the Superpowers plugin cache path
    home = Path.home()

    if sys.platform == "win32":
        # Windows path
        claude_path = (
            home / ".claude" / "plugins" / "cache" / "claude-plugins-official"
            / "superpowers" / "5.1.0" / "skills"
        )
    else:
        # macOS/Linux path
        claude_path = (
            home / ".claude" / "plugins" / "cache" / "claude-plugins-official"
            / "superpowers" / "5.1.0" / "skills"
        )

    return claude_path


def find_skills_in_package(skills_dir: Path) -> List[str]:
    """Find all skill folders in the package skills directory."""
    if not skills_dir.exists():
        return []

    skill_names = []
    for item in skills_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skill_names.append(item.name)

    return sorted(skill_names)


def copy_skill(
    src_skill_dir: Path,
    dest_skills_dir: Path,
    skill_name: str,
    dry_run: bool = False,
    force: bool = False
) -> Tuple[bool, str]:
    """
    Copy a single skill to the destination directory.

    Returns: (success, message)
    """
    src_skill = src_skill_dir / skill_name
    dest_skill = dest_skills_dir / skill_name

    if not (src_skill / "SKILL.md").exists():
        return False, f"Source SKILL.md not found: {src_skill / 'SKILL.md'}"

    if dest_skill.exists() and not force:
        return False, f"Destination already exists: {dest_skill} (use --force to overwrite)"

    if dry_run:
        return True, f"[DRY-RUN] Would copy {src_skill} -> {dest_skill}"

    try:
        if dest_skill.exists():
            shutil.rmtree(dest_skill)
        shutil.copytree(src_skill, dest_skill)
        return True, f"Copied {skill_name} -> {dest_skill}"
    except Exception as e:
        return False, f"Failed to copy {skill_name}: {e}"


def setup_skills(
    target: str = "agents",
    skills_dir: str = None,
    dry_run: bool = False,
    force: bool = False,
    verbose: bool = False
) -> bool:
    """
    Install sensemaking-skills SKILL.md files to agent-discoverable locations.

    Args:
        target: Which location(s) to install to:
            - "agents" (default): ~/.agents/skills
            - "claude-superpowers": Claude Code Superpowers cache
            - "all": Both locations
            - "custom": Use --skills-dir path
        skills_dir: Custom destination directory (if target="custom")
        dry_run: Show what would be done without actually doing it
        force: Overwrite existing skills
        verbose: Print detailed output

    Returns: True if successful, False otherwise
    """

    try:
        # Get source skills directory
        package_skills_dir = get_package_skills_dir()
        skill_names = find_skills_in_package(package_skills_dir)

        if not skill_names:
            raise SkillsSetupError(f"No skills found in {package_skills_dir}")

        if verbose:
            print(f"Found {len(skill_names)} skills: {', '.join(skill_names)}")

        # Determine destination directories
        destinations = []

        if target in ("agents", "all"):
            destinations.append(("agents", get_agents_skills_dir()))

        if target in ("claude-superpowers", "all"):
            destinations.append(("claude-superpowers", get_claude_code_skills_dir()))

        if target == "custom":
            if not skills_dir:
                raise SkillsSetupError("--skills-dir required when using custom target")
            destinations.append(("custom", Path(skills_dir)))

        if not destinations:
            raise SkillsSetupError(f"Unknown target: {target}")

        # Install to each destination
        all_success = True

        for dest_name, dest_dir in destinations:
            print(f"\n{'='*60}")
            print(f"Installing to: {dest_name}")
            print(f"Directory: {dest_dir}")
            print(f"{'='*60}")

            # Create directory if needed
            if not dry_run and not dest_dir.exists():
                dest_dir.mkdir(parents=True, exist_ok=True)
                if verbose:
                    print(f"Created directory: {dest_dir}")

            # Copy each skill
            for skill_name in skill_names:
                success, message = copy_skill(
                    package_skills_dir,
                    dest_dir,
                    skill_name,
                    dry_run=dry_run,
                    force=force
                )

                status = "OK" if success else "FAIL"
                symbol = "+" if success else "x"
                print(f"  [{symbol}] {message}")

                if not success:
                    all_success = False

        # Print summary
        print(f"\n{'='*60}")
        print("Summary")
        print(f"{'='*60}")

        if dry_run:
            print("[DRY-RUN MODE] No files were actually installed.")

        print(f"Skills to install: {', '.join(skill_names)}")
        print(f"Target locations: {len(destinations)}")

        if all_success:
            print("\nStatus: SUCCESS")
            print("\nYou can now invoke skills from your agents:")
            for skill_name in skill_names:
                print(f"  /skill {skill_name}")
            print("\nNote: Agents also need sensemaking-skills Python package installed:")
            print("  pip install sensemaking-skills")
        else:
            print("\nStatus: PARTIAL FAILURE - Some installations failed")

        return all_success

    except SkillsSetupError as e:
        print(f"Error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False
