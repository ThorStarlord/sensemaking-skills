"""Shared utility functions for artifact validators.

All functions are pure (no side effects, no CLI). Importable by any validator.
"""

import os
import re
import subprocess
from datetime import datetime

import yaml

import workflow_liveness


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
        Tuple of (exit_code, combined_output_string, elapsed_seconds)
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


def load_workflow_liveness(repo_root: str) -> dict:
    """Load the ADR-0027 workflow-liveness overlay.

    Missing overlays default to ``active`` for backward compatibility with
    external/custom registries that predate the liveness contract.
    """
    return workflow_liveness.load_liveness_file(
        _registry_path(repo_root, "workflow-liveness.yaml")
    )


def load_workflow_catalog(repo_root: str) -> dict | None:
    """Load the complete workflow catalog, annotated with effective liveness.

    This is the provenance/structural view. Compatibility-only workflow IDs
    remain present with their historical definitions.
    """
    raw = load_yaml(_registry_path(repo_root, "workflow-registry.yaml"))
    if raw is None:
        return None
    return workflow_liveness.annotate_catalog(raw, load_workflow_liveness(repo_root))


def load_workflow_registry(repo_root: str) -> dict | None:
    """Load the CURRENT operational workflow view.

    Only workflows whose effective liveness is ``active`` are returned.
    Compatibility-only identities and historical definitions remain available
    through :func:`load_workflow_catalog`.
    """
    raw = load_yaml(_registry_path(repo_root, "workflow-registry.yaml"))
    if raw is None:
        return None
    return workflow_liveness.operationalize_catalog(
        raw, load_workflow_liveness(repo_root)
    )


def load_artifact_contracts(repo_root: str) -> dict | None:
    """Load artifact-contracts.yaml from the repo."""
    return load_yaml(_registry_path(repo_root, "artifact-contracts.yaml"))


def load_skill_registry(repo_root: str) -> dict | None:
    """Load skill-registry.yaml from the repo."""
    return load_yaml(_registry_path(repo_root, "skill-registry.yaml"))


def load_canonical_vocabulary(repo_root: str) -> dict | None:
    """Load canonical-vocabulary.yaml from the repo.

    The canonical vocabulary defines authoritative enumerated values used
    throughout the system: fog_types, routing_fields, gates, execution_modes,
    artifact_ids, and workflow_ids.

    Returns:
        Dict with keys: fog_types, routing_fields, gates, execution_modes,
        artifact_ids, workflow_ids, or None if file not found.
    """
    path = os.path.join(repo_root, "docs", "canonical-vocabulary.yaml")
    return load_yaml(path)


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


def validator_cli(
    validate_fn,
    *,
    description: str = "",
    error_codes: dict[str, str] | list[str] | None = None,
    success_msg: str = "Validation passed!",
    needs_artifact: bool = True,
    repo_root_default: str = ".",
    argv: list[str] | None = None,
) -> int:
    """Standard CLI entry point for artifact validators.

    Handles argparse setup, --list-codes, --repo-root, and error printing,
    and exit code logic. Reduces each validator's ``main()`` from ~30
    lines to ~3.

    Args:
        validate_fn: Callable ``(artifact_path, repo_root) -> list[str]``.
            The list contains error messages (empty = pass).
        description: Shown in ``--help``.
        error_codes: Dict ``{code: description}`` or list of code strings.
            If given, ``--list-codes`` prints them.
        success_msg: Printed when validation passes.
        needs_artifact: If True, requires ``artifact_path`` positional arg.
            If False, only accepts ``--repo-root``.
        repo_root_default: Default value for ``--repo-root``.
        argv: Command-line arguments to parse. If None, uses sys.argv[1:].

    Returns:
        Exit code (0 = pass, 1 = fail).
    """
    import argparse

    parser = argparse.ArgumentParser(description=description)
    if needs_artifact:
        parser.add_argument("artifact_path", nargs="?", help="Path to the artifact markdown file")
    parser.add_argument("--repo-root", default=repo_root_default, help="Root directory of the repository")
    parser.add_argument("--list-codes", action="store_true", help="List all error codes and exit")
    args = parser.parse_args(argv)

    if args.list_codes and error_codes is not None:
        list_error_codes(error_codes)
        return 0

    if needs_artifact and not args.artifact_path:
        parser.print_usage()
        return 1

    errs = validate_fn(getattr(args, "artifact_path", None), args.repo_root)
    if errs:
        for e in errs:
            print(f"ERROR {e}")
        return 1
    print(success_msg)
    return 0


def list_error_codes(codes: dict[str, str] | list[str], *, prefix: str = "") -> None:
    """Print error codes in the standard format.

    Args:
        codes: Either a dict of ``{code: description}`` or a list of code strings.
        prefix: Optional heading line printed before the codes.
    """
    if prefix:
        print(prefix)
    if isinstance(codes, dict):
        for code, desc in sorted(codes.items()):
            print(f"  {code}: {desc}")
    else:
        for code in codes:
            print(code)


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


def build_fog_type_normalizer(vocab: dict) -> dict[str, str]:
    """Build a fog type alias->canonical mapping from the vocabulary.

    Args:
        vocab: The canonical vocabulary dict from load_canonical_vocabulary().

    Returns:
        Dict mapping {alias: canonical_id} including canonical forms themselves
        (e.g., {"product_fog": "product_fog", "product": "product_fog", ...}).
    """
    mapping = {}
    if not vocab or "fog_types" not in vocab:
        return mapping

    for fog_type in vocab["fog_types"]:
        canonical = fog_type["id"]
        # Map canonical form to itself
        mapping[canonical] = canonical
        # Map all aliases to canonical form
        for alias in fog_type.get("aliases", []):
            mapping[alias] = canonical

    return mapping


def normalize_fog_type(value: str, mapping: dict[str, str]) -> str:
    """Normalize a fog type to canonical form using the mapping.

    Args:
        value: The fog type value (may be canonical or alias).
        mapping: The mapping returned by build_fog_type_normalizer().

    Returns:
        The canonical fog type form.

    Raises:
        ValueError: If the value is not recognized.
    """
    normalized = mapping.get(value.lower() if isinstance(value, str) else value)
    if not normalized:
        available = ", ".join(sorted(set(mapping.values())))
        raise ValueError(f"Unknown fog type: {value!r}. Valid values: {available}")
    return normalized