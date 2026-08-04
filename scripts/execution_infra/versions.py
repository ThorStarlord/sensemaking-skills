"""Execution-infrastructure versioning (Phase 6 readiness, Issue #122).

The EXP-0001 campaign policy pins ONLY the framework code
(``framework_sha`` 4ba049e...). The provenance verifier, the provider
adapter, and the runner are INFRASTRUCTURE OUTSIDE THE CAMPAIGN
CONFIGURATION: they are injected at execution time, and their exact
versions must be preserved in the execution record so the run is
reproducible and drift-detectable.

Version identity here is content-addressed: SHA-256 over the exact source
bytes of each infrastructure module. A change to any byte produces a
different version, and the execution record captures the versions that
were actually loaded.

This module also provides the framework-drift proof: the campaign's
pinned framework SHA must still describe the framework code actually used.
Because the campaign pins ``4ba049e`` and this repository now lives past
that commit, the proof is a byte-level diff: the framework code (``src/``
and the canonical Gate A / executor scripts) at the execution checkout
must be identical to the pinned SHA. The runner refuses to run otherwise.
"""

import hashlib
import subprocess
from pathlib import Path
from typing import Dict

#: The framework code paths that define the pinned runtime. Anything
#: outside these paths is infrastructure, not framework code.
FRAMEWORK_CODE_PATHS = [
    "src/sensemaking_skills",
    "scripts/skill_executor.py",
    "scripts/gate_a_authorization.py",
]

#: Infrastructure modules whose content digests are recorded per run.
_INFRA_MODULES = [
    "versions.py",
    "production_verifier.py",
    "provider_adapter.py",
    "runner.py",
]


def module_digest(path: Path) -> str:
    """Content SHA-256 of one infrastructure module (exact source bytes)."""
    data = Path(path).read_bytes()
    return hashlib.sha256(data).hexdigest()


def adapter_versions(infra_dir: Path) -> Dict[str, str]:
    """name -> content digest for every infrastructure module."""
    versions: Dict[str, str] = {}
    for name in _INFRA_MODULES:
        path = Path(infra_dir) / name
        if path.is_file():
            versions[name] = module_digest(path)
    return versions


def framework_code_unchanged(
    pinned_sha: str, repo_root: Path, framework_paths=None
) -> bool:
    """True iff the framework code at ``repo_root`` is byte-identical to
    ``pinned_sha`` (empty diff over the framework code paths)."""
    paths = framework_paths or FRAMEWORK_CODE_PATHS
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "diff", "--quiet", pinned_sha, "HEAD", "--"]
            + paths,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0


def checkout_sha(repo_root: Path) -> str:
    """The exact HEAD commit of ``repo_root`` (for the execution record)."""
    result = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"cannot resolve checkout SHA: {result.stderr.strip()}")
    return result.stdout.strip()
