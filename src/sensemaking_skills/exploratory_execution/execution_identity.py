"""Execution identity and framework-drift proof (Phase 6 correction, #122).

The campaign configuration (ADR 0023 §5/§10) is the frozen, hashable set
of every execution-relevant input. The execution machinery in this package
-- verifier, provider, prompt builder, artifact validator, target
materializer -- is FRAMEWORK-GOVERNED: its bytes ship inside the pinned
framework and are therefore bound by ``framework_sha`` (a normative
configuration field and a policy allowlist member) BEFORE execution, not
merely recorded after it. No module here is treated as incidental
infrastructure outside the configuration.

This module provides the drift proof: the execution checkout must be
byte-identical to the pinned framework commit across ALL of:

* the committed tree (``git diff <pin> HEAD`` empty);
* the index and working tree (``git diff <pin>`` empty);
* untracked files (``git status --porcelain --untracked-files=all`` empty,
  which also covers symlink/path substitutions the index cannot see);
* the resolved HEAD (``rev-parse HEAD`` == pin).

There is deliberately NO path carve-out: every file that can influence
execution -- skills, skeletons, registries, schemas, validators,
``scripts/``, ``src/`` -- is protected by the full-tree proof.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

#: The governed identity of the framework repository whose signed commits
#: and pinned tree are trusted for campaign execution. The runner supplies
#: this to the production verifier and the checkout guard.
TRUSTED_FRAMEWORK_REMOTE = "https://github.com/ThorStarlord/sensemaking-skills.git"

#: The governed GitHub repository for Lane A beta campaign approvals
#: (issue-comment mechanism). Approval provenance must name exactly this
#: repository; the comment verifier refuses anything else.
GOVERNED_GITHUB_REPOSITORY = "ThorStarlord/sensemaking-skills"

#: The minimum GitHub collaborator permission an approval-comment author
#: must hold on the governed repository (admin = repository owner for
#: EXP-0001's designated approver).
GOVERNED_REQUIRED_APPROVER_PERMISSION = "admin"

#: The governed path of the approval document inside signed commits.
GOVERNED_APPROVAL_PATH = "approval.yaml"

#: The governed protected branch (remote-tracking) that signed approval
#: commits must be reachable from.
GOVERNED_PROTECTED_BRANCH = "refs/remotes/origin/main"

#: Modules whose content digests are recorded in the execution record for
#: auditability (the AUTHORIZATION is the framework pin; the digests make
#: the record byte-exact).
_EXECUTION_MODULES: list[str] = [
    "execution_identity.py",
    "production_verifier.py",
    "github_approval.py",
    "target_checkout.py",
    "prompt_builder.py",
    "claude_provider.py",
    "artifact_validator.py",
    "approver-registry.yaml",
]


def checkout_sha(repo_root: Path) -> str:
    """The exact HEAD commit of ``repo_root`` (for the execution record)."""
    result = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        capture_output=True, text=True, timeout=60, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"cannot resolve checkout SHA: {result.stderr.strip()}")
    return result.stdout.strip()


def _git_ok(repo_root: Path, args: list[str]) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root)] + args,
            capture_output=True, text=True, timeout=120, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0


def framework_tree_unchanged(pinned_sha: str, repo_root: Path) -> bool:
    """True iff ``repo_root`` is byte-identical to ``pinned_sha``.

    Proves all four conditions: HEAD resolves to the pin, the committed
    tree matches the pin, index+working tree match the pin, and there are
    no untracked files (which would silently introduce bytes the pin never
    contained). ``git status --porcelain --untracked-files=all`` exits 0
    even when untracked files exist, so its OUTPUT must be empty -- the
    return code alone is not proof. Fails closed on any git error.
    """
    repo_root = Path(repo_root)
    if checkout_sha(repo_root) != pinned_sha:
        return False
    if not _git_ok(repo_root, ["diff", "--quiet", pinned_sha, "HEAD"]):
        return False
    if not _git_ok(repo_root, ["diff", "--quiet", pinned_sha]):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--porcelain",
             "--untracked-files=all"],
            capture_output=True, text=True, timeout=120, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0 and result.stdout.strip() == ""


def module_digest(path: Path) -> str:
    """Content SHA-256 of one execution module (exact source bytes)."""
    data = Path(path).read_bytes()
    return hashlib.sha256(data).hexdigest()


def execution_module_digests(package_dir: Path) -> dict[str, str]:
    """name -> content digest for every framework execution module.

    Fails if any expected module is missing: the execution record must
    never silently omit a module that shaped the run.
    """
    package_dir = Path(package_dir)
    digests: dict[str, str] = {}
    missing = []
    for name in _EXECUTION_MODULES:
        path = package_dir / name
        if not path.is_file():
            missing.append(name)
            continue
        digests[name] = module_digest(path)
    if missing:
        raise RuntimeError(
            f"execution modules missing from framework package: {sorted(missing)}"
        )
    return digests
