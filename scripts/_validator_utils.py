"""Shared utility functions for artifact validators.

All functions are pure (no side effects, no CLI). Importable by any validator.
"""

import os
import re
import subprocess
from datetime import datetime

import yaml


def run_subprocess(cmd: list[str], repo_root: str, *,
                   timeout: int = 120,
                   capture_output: bool = True,
                   inject_repo_root: bool = True) -> tuple[int, str, float]:
    """Run a subprocess with standardised wrapping.

    Handles template expansion (``{artifact_path}``), ``--repo-root`` injection,
    and elapsed-time tracking. Returns ``(exit_code, output, elapsed_seconds)``.

    Args:
        cmd: Command and arguments. Any ``{artifact_path}`` placeholder is
            replaced with the resolved artifact path before execution.
        repo_root: Root directory of the repository.
        timeout: Maximum execution time in seconds (default 120).
        capture_output: If True, capture stdout+stderr. If False, let them
            passthrough (for interactive commands).
        inject_repo_root: If True, append ``--repo-root <path>`` unless
            already present in cmd.

    Returns:
        Tuple of (exit_code, combined_output_string, elapsed_seconds).
    """
    resolved = [arg.replace("{artifact_path}", "") for arg in cmd]
    if inject_repo_root and "--repo-root" not in resolved:
        resolved.extend(["--repo-root", repo_root])

    start = datetime.now()
    kwargs = {"capture_output": True, "text": True, "timeout": timeout} if capture_output else {}
    result = subprocess.run(resolved, **kwargs)
    elapsed = (datetime.now() - start).total_seconds()

    if capture_output:
        output = (result.stdout + result.stderr).strip()
    else:
        output = ""
    return result.returncode, output, elapsed


def format_error(code: str, message: str, *,
                 workflow_id: str | None = None,
                 step_id: str | None = None) -> str:
    """Format a validation error as 'CODE: message', with optional context.

    When workflow_id and/or step_id are supplied the format becomes::

        CODE (workflow_id): message
        CODE (workflow_id step step_id): message

    Backward-compatible: existing callers passing ``(code, message)``
    positionally receive exactly ``CODE: message`` --- unchanged.
    """
    if workflow_id:
        context = f" ({workflow_id}"
        if step_id:
            context += f" step {step_id}"
        context += ")"
        return f"{code}{context}: {message}"
    return f"{code}: {message}"


def load_yaml(path: str) -> dict | None:
    """Load and parse a YAML file. Returns None if the file is missing."""
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_repo_root(given: str, script_dir: str) -> str:
    """Resolve --repo-root argument relative to the script directory."""
    if os.path.isabs(given):
        return given
    return os.path.normpath(os.path.join(script_dir, given))


def load_weakness_types(repo_root: str) -> list[str]:
    """Parse bolded terms from weakness-types.md reference file."""
    path = os.path.join(repo_root, "skills", "repo-sensemaker", "references", "weakness-types.md")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return re.findall(r"\*\*(.+?)\*\*", f.read())


def _registry_path(repo_root: str, filename: str) -> str:
    """Build a path to a file in the workflow-planner references directory."""
    return os.path.join(repo_root, "skills", "workflow-planner", "references", filename)


def load_workflow_registry(repo_root: str) -> dict | None:
    """Load workflow-registry.yaml from the repo."""
    return load_yaml(_registry_path(repo_root, "workflow-registry.yaml"))


def load_artifact_contracts(repo_root: str) -> dict | None:
    """Load artifact-contracts.yaml from the repo."""
    return load_yaml(_registry_path(repo_root, "artifact-contracts.yaml"))


def load_skill_registry(repo_root: str) -> dict | None:
    """Load skill-registry.yaml from the repo."""
    return load_yaml(_registry_path(repo_root, "skill-registry.yaml"))


def flatten_skill_registry(raw: dict) -> dict[str, dict]:
    """Flatten skill-registry.yaml into ``{skill_id: skill_def}`` map.

    Args:
        raw: The dict returned by ``load_skill_registry()``, with structure::

            {"ecosystems": {"ecosystem-name": {
                "skills": [{"id": "skill-name", ...}, ...]
            }}}

    Returns:
        Flat dict mapping every skill ID to its full definition dict.
        Returns empty dict if the raw registry has no ``'ecosystems'`` key.
    """
    all_skills: dict[str, dict] = {}
    for ecosystem in raw.get("ecosystems", {}).values():
        for skill in ecosystem.get("skills", []):
            all_skills[skill["id"]] = skill
    return all_skills


HEADING_RE = re.compile(r"^##\s+(?:\d+\.\s*)?(?P<name>.+?)\s*$", re.MULTILINE)


def extract_sections(text: str, normalize_hyphens: bool = True) -> dict[str, str]:
    """Split content by ## headings, returning {lowercase_name: body_text}.

    Args:
        text: The markdown content to split.
        normalize_hyphens: If True, replace hyphens with spaces in section names
            so 'machine-readable-handoff' matches 'machine readable handoff'.
    """
    sections = {}
    matches = list(HEADING_RE.finditer(text))
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        name = match.group("name").strip().lower()
        if normalize_hyphens:
            name = name.replace("-", " ")
        sections[name] = text[start:end].strip()
    return sections
