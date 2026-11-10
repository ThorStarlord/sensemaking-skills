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
are never silently overwritten. Only ``--force`` replaces them, except that
``--update`` replaces a copy that still matches the tree this installer
recorded writing (or verifying) there, or (from a Git checkout, with no record)
a tree committed in the checkout's history, because such a copy holds no local
change that replacing it would lose.

Install record: each destination root gets one ``.sensemaking-skills-install.json``
file beside the Skill directories. It maps a Skill name to the digest of the
tree setup-skills last wrote or verified there, with the package version and
source kind. The Skill trees themselves stay byte-identical to the packaged
ones. The record lets a later run tell a copy that is merely outdated from one
that changed after installation. It is setup-skills' own bookkeeping: it does
not show what a host loaded, and copies written by any other tool are not
recorded.

Committed history: when the Skill source is a Git checkout, a divergent copy
with no record is compared with every version of ``skills/<name>`` committed on
the checkout's branches, tags and remote-tracking refs. A copy whose tree equals
one of them (byte for byte, or after converting CRLF line endings to LF, which
is what a Windows checkout writes) is ``historical``: its exact content is
still in Git, so ``--update`` may replace it. This covers roots installed
before install records existed. Only read-only Git commands are run.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Mapping, Sequence, Tuple

import yaml

from . import __version__
from .harness_adapters import (
    HarnessAdapterError,
    resolve_harness_destinations,
)
from .workflow_availability import (
    installed_skill_ids,
    summarize_availability,
    workflow_availability,
)

__all__ = [
    "SkillsSetupError",
    "copy_skill",
    "find_skills_in_package",
    "get_agents_skills_dir",
    "get_claude_code_skills_dir",
    "get_claude_personal_skills_dir",
    "get_codex_skills_dir",
    "get_opencode_skills_dir",
    "get_package_skills_dir",
    "setup_skills",
    "skill_state",
]
# ``__all__`` and the signatures of the names in it are frozen by
# docs/public-api-v1.0.yaml (tests/test_public_api_contract.py). The install
# record helpers below are deliberately not exported.

INSTALL_RECORD_NAME = ".sensemaking-skills-install.json"
"""File name of the per-root install record (see the module docstring)."""

INSTALL_RECORD_ARTIFACT_ID = "sensemaking_skills_install_record"
INSTALL_RECORD_SCHEMA_VERSION = 1


class SkillsSetupError(Exception):
    """Raised when skill setup fails."""


def get_package_skills_dir() -> Path:
    """Get the Skill source directory without assuming a source checkout."""
    try:
        from importlib.resources import files

        packaged = files("sensemaking_skills") / "skill_trees"
        if packaged.is_dir():
            return Path(str(packaged))
    except (ImportError, ModuleNotFoundError, OSError):
        # A source checkout may not have importlib resource metadata. Other
        # failures indicate a broken packaged-resource boundary and must be
        # visible instead of silently selecting a different source tree.
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
    """Return the declared Codex personal Skill discovery root."""
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


def _tree_digest(fingerprint: Mapping[str, str]) -> str:
    """Digest a tree fingerprint (relative path -> file SHA-256), order-independent."""
    hasher = hashlib.sha256()
    for rel in sorted(fingerprint):
        hasher.update(rel.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(fingerprint[rel].encode("ascii"))
        hasher.update(b"\n")
    return hasher.hexdigest()


def _skill_source_kind(package_skills_dir: Path) -> str:
    """Name the kind of Skill source resolved by :func:`get_package_skills_dir`."""
    return "packaged" if package_skills_dir.name == "skill_trees" else "source_checkout"


def _valid_record_entry(entry: object) -> bool:
    if not isinstance(entry, dict):
        return False
    digest = entry.get("tree_sha256")
    return (
        isinstance(digest, str)
        and len(digest) == 64
        and all(char in "0123456789abcdef" for char in digest)
    )


def _recorded_version(entry: Mapping | None) -> str:
    """Return the recorded package version as short printable ASCII."""
    version = entry.get("package_version") if isinstance(entry, Mapping) else None
    if not isinstance(version, str) or not version:
        return "an earlier run"
    cleaned = "".join(char for char in version[:40] if " " <= char <= "~")
    return cleaned or "an earlier run"


def load_install_record(dest_skills_dir: Path) -> Tuple[dict, str | None]:
    """Read a destination root's install record.

    Returns ``(entries_by_skill_name, problem)``. A root without a record gives
    ``({}, None)``. A record that is not a regular file, cannot be parsed, or has
    an unknown format gives ``({}, problem)``: every divergent copy is then
    treated as unrecorded, as before install records existed, and the file is
    left unchanged. Entries without a well-formed ``tree_sha256`` are skipped.
    """
    path = dest_skills_dir / INSTALL_RECORD_NAME
    if not path.exists() and not path.is_symlink():
        return {}, None
    if path.is_symlink() or not path.is_file():
        return {}, "install record is not a regular file"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        return {}, f"install record could not be read ({type(exc).__name__})"
    if (
        not isinstance(data, dict)
        or data.get("artifact_id") != INSTALL_RECORD_ARTIFACT_ID
        or data.get("schema_version") != INSTALL_RECORD_SCHEMA_VERSION
        or not isinstance(data.get("skills"), dict)
    ):
        return {}, "install record has an unknown format"
    entries = {
        name: dict(entry)
        for name, entry in data["skills"].items()
        if isinstance(name, str) and _valid_record_entry(entry)
    }
    return entries, None


def _write_install_record(dest_skills_dir: Path, entries: Mapping[str, Mapping]) -> None:
    """Write the install record atomically (temporary file, then replace)."""
    payload = {
        "artifact_id": INSTALL_RECORD_ARTIFACT_ID,
        "schema_version": INSTALL_RECORD_SCHEMA_VERSION,
        "note": (
            "Written by sensemaking-skills setup-skills: the Skill trees it last "
            "wrote or verified in this directory. It does not show what a host "
            "loaded, and it is not a Skill."
        ),
        "skills": {name: dict(entries[name]) for name in sorted(entries)},
    }
    path = dest_skills_dir / INSTALL_RECORD_NAME
    # mkstemp creates a new file exclusively, so a planted link at a fixed
    # temporary name cannot redirect the write outside the root.
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=INSTALL_RECORD_NAME + ".", suffix=".tmp", dir=dest_skills_dir
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(
                json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
            )
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _is_link_like(path: Path) -> bool:
    """True for a symlink or (Windows, Python 3.12+) a directory junction."""
    if path.is_symlink():
        return True
    is_junction = getattr(os.path, "isjunction", None)
    return bool(is_junction and is_junction(path))


def install_state(
    src_skill: Path, dest_skill: Path, recorded: Mapping | None = None
) -> str:
    """Classify a destination against its packaged source and its install record.

    ``missing`` and ``current`` mean what they mean for :func:`skill_state`. A
    copy that differs from the packaged tree is:

    - ``outdated`` when its tree still has the digest setup-skills recorded
      writing or verifying there, so nothing has changed it since;
    - ``changed`` when a record exists but the tree no longer matches it
      (edited locally, or rewritten by another tool);
    - ``unrecorded`` when there is no usable record for it, or when the
      destination is a symlink or junction (its bytes live elsewhere, so a
      record cannot vouch for them).
    """
    if not dest_skill.exists():
        return "missing"
    dest_fingerprint = _skill_tree_fingerprint(dest_skill)
    if _skill_tree_fingerprint(src_skill) == dest_fingerprint:
        return "current"
    if _is_link_like(dest_skill) or not _valid_record_entry(recorded):
        return "unrecorded"
    if _tree_digest(dest_fingerprint) == recorded["tree_sha256"]:
        return "outdated"
    return "changed"


_GIT_TIMEOUT_SECONDS = 120


def _git_object_id(hash_name: str, kind: bytes, body: bytes) -> str:
    return hashlib.new(hash_name, kind + b" %d\0" % len(body) + body).hexdigest()


def _git_tree_id(directory: Path, hash_name: str, *, lf_only: bool) -> str | None:
    """Compute the Git tree id ``directory`` would have if committed as is.

    Every file is taken as a regular non-executable file (mode 100644), which
    is how every committed Skill file is stored. With ``lf_only``, CRLF line
    endings in files without NUL bytes are converted to LF first, which undoes
    a Windows checkout's conversion. Returns ``None`` when the tree holds a
    symlink, junction or anything that is neither a file nor a directory, so
    such a copy never matches. Empty directories, which Git cannot hold, are
    skipped.
    """
    entries: list[tuple[bytes, bytes, str]] = []
    for child in directory.iterdir():
        if _is_link_like(child):
            return None
        name = child.name.encode("utf-8")
        if child.is_dir():
            subtree = _git_tree_id(child, hash_name, lf_only=lf_only)
            if subtree is None:
                return None
            if subtree != _git_object_id(hash_name, b"tree", b""):
                entries.append((b"40000", name, subtree))
        elif child.is_file():
            data = child.read_bytes()
            if lf_only and b"\0" not in data:
                data = data.replace(b"\r\n", b"\n")
            entries.append((b"100644", name, _git_object_id(hash_name, b"blob", data)))
        else:
            return None
    # Git orders tree entries by name, comparing a directory as "name/".
    entries.sort(key=lambda entry: entry[1] + (b"/" if entry[0] == b"40000" else b""))
    body = b"".join(
        mode + b" " + name + b"\0" + bytes.fromhex(object_id)
        for mode, name, object_id in entries
    )
    return _git_object_id(hash_name, b"tree", body)


class _CommittedSkillHistory:
    """Look up installed Skill trees among versions committed in a checkout.

    Only constructed for a ``source_checkout`` source whose parent directory is
    the top level of a Git work tree. Any Git failure makes a lookup return
    ``None``, so a copy without a match stays ``unrecorded``.
    """

    def __init__(self, repo_root: Path, hash_name: str) -> None:
        self.repo_root = repo_root
        self.hash_name = hash_name

    @classmethod
    def for_source(cls, package_skills_dir: Path) -> "_CommittedSkillHistory | None":
        if _skill_source_kind(package_skills_dir) != "source_checkout":
            return None
        repo_root = package_skills_dir.parent
        output = cls._git(repo_root, "rev-parse", "--show-toplevel", "--show-object-format")
        lines = output.splitlines() if output else []
        if len(lines) != 2 or lines[1] not in ("sha1", "sha256"):
            return None
        try:
            if Path(lines[0]).resolve() != repo_root.resolve():
                return None
        except OSError:
            return None
        return cls(repo_root, lines[1])

    @staticmethod
    def _git(repo_root: Path, *args: str, stdin: str | None = None) -> str | None:
        try:
            completed = subprocess.run(
                ["git", "-C", str(repo_root), *args],
                input=stdin,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=_GIT_TIMEOUT_SECONDS,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return None
        if completed.returncode != 0:
            return None
        return completed.stdout

    def find(self, skill_name: str, dest_skill: Path) -> dict | None:
        """Return the newest commit whose ``skills/<name>`` tree equals ``dest_skill``.

        The result has ``commit``, ``date`` and ``line_endings_only`` (True
        when only CRLF line endings differ). ``None`` when nothing matches.
        """
        if _is_link_like(dest_skill) or not dest_skill.is_dir():
            return None
        try:
            exact = _git_tree_id(dest_skill, self.hash_name, lf_only=False)
            lf_only = _git_tree_id(dest_skill, self.hash_name, lf_only=True)
        except OSError:
            return None
        if exact is None:
            return None
        log = self._git(
            self.repo_root,
            "log",
            "--format=%H %cs",
            "--branches",
            "--tags",
            "--remotes",
            "HEAD",
            "--",
            f"skills/{skill_name}",
        )
        commits = [line.split(" ", 1) for line in (log or "").splitlines() if " " in line]
        if not commits:
            return None
        batch = self._git(
            self.repo_root,
            "cat-file",
            "--batch-check",
            stdin="".join(f"{commit}:skills/{skill_name}\n" for commit, _ in commits),
        )
        answers = (batch or "").splitlines()
        if len(answers) != len(commits):
            return None
        for (commit, date), answer in zip(commits, answers):
            fields = answer.split()
            if len(fields) != 3 or fields[1] != "tree":
                continue
            if fields[0] in (exact, lf_only):
                return {
                    "commit": commit,
                    "date": date,
                    "line_endings_only": fields[0] != exact,
                }
        return None


def _describe_commit(skill_name: str, match: Mapping) -> str:
    text = f"skills/{skill_name} in commit {match['commit'][:10]} ({match['date']})"
    if match.get("line_endings_only"):
        text += ", apart from CRLF line endings"
    return text


def copy_skill(
    src_skill_dir: Path,
    dest_skills_dir: Path,
    skill_name: str,
    dry_run: bool = False,
    force: bool = False,
) -> Tuple[bool, str]:
    """Copy one Skill tree with explicit drift handling (no install record)."""
    return _copy_skill_tree(
        src_skill_dir, dest_skills_dir, skill_name, dry_run=dry_run, force=force
    )


_REPLACEABLE_BY_UPDATE = ("outdated", "historical")
"""States whose copy holds nothing that replacing it would lose."""


def _classify_install(
    src_skill: Path,
    dest_skill: Path,
    recorded: Mapping | None,
    history: _CommittedSkillHistory | None,
) -> Tuple[str, dict | None]:
    """:func:`install_state`, refined by committed history for unrecorded copies.

    Returns ``(state, match)``. An ``unrecorded`` copy whose tree equals a
    committed version of its Skill becomes ``historical`` and ``match`` names
    that commit; every other state is returned unchanged with ``None``.
    """
    state = install_state(src_skill, dest_skill, recorded)
    if state == "unrecorded" and history is not None:
        match = history.find(src_skill.name, dest_skill)
        if match is not None:
            return "historical", match
    return state, None


def _copy_skill_tree(
    src_skill_dir: Path,
    dest_skills_dir: Path,
    skill_name: str,
    *,
    dry_run: bool = False,
    force: bool = False,
    update: bool = False,
    recorded: Mapping | None = None,
    classified: Tuple[str, Mapping | None] | None = None,
    history_checked: bool = False,
) -> Tuple[bool, str]:
    """Copy one Skill tree, classifying a divergent copy against its record.

    ``recorded`` is this Skill's install-record entry, if any. ``classified``
    is a ``(state, match)`` pair from :func:`_classify_install`; without it the
    state comes from :func:`install_state` and committed history is not used.
    ``history_checked`` says whether committed history was searched, which only
    changes the wording for an ``unrecorded`` copy. ``update`` replaces only an
    ``outdated`` or ``historical`` copy; ``force`` replaces any divergent copy.
    Without a record or classification this is :func:`copy_skill`.
    """
    src_skill = src_skill_dir / skill_name
    dest_skill = dest_skills_dir / skill_name

    if not (src_skill / "SKILL.md").exists():
        return False, f"Source SKILL.md not found: {src_skill / 'SKILL.md'}"

    if classified is None:
        state, match = install_state(src_skill, dest_skill, recorded), None
    else:
        state, match = classified
    if state == "current":
        return True, f"Current (already matches packaged version): {skill_name}"

    version = _recorded_version(recorded)
    if state == "outdated" and not (force or update):
        return (
            False,
            f"Different from packaged version: {skill_name} "
            f"(unchanged since setup-skills {version} recorded it; "
            "use --update to replace it)",
        )
    if state == "historical" and not (force or update):
        return (
            False,
            f"Different from packaged version: {skill_name} "
            f"(no install record, but identical to {_describe_commit(skill_name, match)}; "
            "use --update to replace it)",
        )
    if state == "changed" and not force:
        return (
            False,
            f"Different from packaged version: {skill_name} "
            f"(changed since setup-skills {version} recorded it; "
            "--force overwrites those changes)",
        )
    if state == "unrecorded" and not force:
        if history_checked and not _is_link_like(dest_skill):
            return (
                False,
                f"Different from packaged version: {skill_name} "
                "(installed copy diverged; no install record, and no version "
                "committed in this checkout matches it; inspect it, then use "
                "--force to overwrite)",
            )
        return (
            False,
            f"Different from packaged version: {skill_name} "
            "(installed copy diverged; use --force to overwrite)",
        )

    replace_allowed = force or (update and state in _REPLACEABLE_BY_UPDATE)
    if dest_skill.exists() and not replace_allowed:
        return False, f"Destination already exists: {dest_skill} (use --force to overwrite)"

    if dry_run:
        action = "Would replace" if dest_skill.exists() else "Would copy"
        return True, f"[DRY-RUN] {action} {src_skill} -> {dest_skill}"

    try:
        if dest_skill.exists():
            shutil.rmtree(dest_skill)
        shutil.copytree(src_skill, dest_skill)
        if state == "outdated":
            return True, (
                f"Updated {skill_name} -> {dest_skill} "
                f"(was unchanged since setup-skills {version} recorded it)"
            )
        if state == "historical":
            return True, (
                f"Updated {skill_name} -> {dest_skill} "
                f"(was identical to {_describe_commit(skill_name, match)})"
            )
        return True, f"Copied {skill_name} -> {dest_skill}"
    except Exception as exc:
        return False, f"Failed to copy {skill_name}: {exc}"


def _refresh_record_entry(
    entries: dict,
    skill_name: str,
    src_skill: Path,
    dest_skill: Path,
    *,
    action: str,
    source_kind: str,
) -> bool:
    """Record a destination tree that now equals its packaged source.

    Returns True when the entry changed. Nothing is recorded unless the copy is
    byte-identical to the source tree, so a record never vouches for bytes that
    setup-skills did not ship. ``action`` says how the recorded digest was
    established (``installed``, ``replaced`` or ``verified`` for a copy that
    already matched); an entry whose digest, version and source are unchanged
    is left as it was, so ``action`` and ``recorded_at`` keep their first values.
    """
    if _is_link_like(dest_skill):
        return False
    dest_fingerprint = _skill_tree_fingerprint(dest_skill)
    if not dest_fingerprint or dest_fingerprint != _skill_tree_fingerprint(src_skill):
        return False
    digest = _tree_digest(dest_fingerprint)
    previous = entries.get(skill_name)
    if (
        previous
        and previous.get("tree_sha256") == digest
        and previous.get("package_version") == __version__
        and previous.get("source") == source_kind
    ):
        return False
    entries[skill_name] = {
        "tree_sha256": digest,
        "package_version": __version__,
        "source": source_kind,
        "action": action,
        "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    return True


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

    if scope == "user" and project_root is not None:
        raise SkillsSetupError(
            "--project-root is only valid when --scope=project"
        )

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


NO_FLAG_PROFILE = "full"
"""Profile used when no ``--profile`` flag is given.

It stays ``full`` in M3, so the installed set is unchanged. Changing it is a
separate release decision (M4), not part of profile selection.
"""


def _load_install_profiles() -> Tuple[dict, dict]:
    """Return (profiles, add_ons) from the packaged install-profile catalogue."""
    from importlib.resources import files

    text = files("sensemaking_skills.defaults").joinpath("install-profiles.yaml").read_text(
        encoding="utf-8"
    )
    data = yaml.safe_load(text) or {}
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise SkillsSetupError("packaged install-profiles.yaml must be a schema_version 1 mapping")
    profiles = data.get("profiles")
    add_ons = data.get("add_ons") or {}
    if not isinstance(profiles, dict) or not isinstance(add_ons, dict):
        raise SkillsSetupError(
            "packaged install-profiles.yaml must define 'profiles' and 'add_ons' mappings"
        )
    for group in (profiles, add_ons):
        for name, spec in group.items():
            if not isinstance(spec, dict):
                raise SkillsSetupError(f"install profile {name!r} must be a mapping")
            if spec.get("all_packaged") is not True and not isinstance(spec.get("skills"), list):
                raise SkillsSetupError(
                    f"install profile {name!r} must list 'skills' or set all_packaged"
                )
    return profiles, add_ons


def _select_skill_names(
    packaged: List[str],
    *,
    profile: str | None,
    include: Sequence[str],
) -> Tuple[str, List[str], List[str]]:
    """Resolve a profile and add-ons to the exact Skill names to copy.

    Fails closed: an unknown profile or add-on, or a profile member that is not
    packaged, raises before anything is copied.
    """
    profiles, add_ons = _load_install_profiles()
    name = NO_FLAG_PROFILE if profile is None else profile
    if name not in profiles:
        raise SkillsSetupError(
            f"unknown profile {name!r}; choose one of: {', '.join(sorted(profiles))}"
        )
    spec = profiles[name]
    chosen = set(packaged) if spec.get("all_packaged") is True else set(spec["skills"])
    selected_add_ons: List[str] = []
    for add_on in include:
        if add_on not in add_ons:
            raise SkillsSetupError(
                f"unknown add-on {add_on!r}; choose from: {', '.join(sorted(add_ons))}"
            )
        if add_on not in selected_add_ons:
            selected_add_ons.append(add_on)
            chosen.update(add_ons[add_on]["skills"])
    missing = sorted(chosen - set(packaged))
    if missing:
        raise SkillsSetupError("profile names Skills that are not packaged: " + ", ".join(missing))
    return name, selected_add_ons, sorted(chosen)


def _report_workflow_availability(
    dest_dir: Path,
    *,
    dry_run: bool,
    planned: frozenset[str],
) -> None:
    """Print installation availability of active workflows for one destination.

    This is installation availability only. It does not change liveness and does
    not authorize execution. Workflows missing required Skills are listed as not
    available rather than presented as executable.
    """
    present = installed_skill_ids(dest_dir)
    label = "planned" if dry_run else "installed"
    installed = (present | planned) if dry_run else present
    try:
        rows = workflow_availability(installed)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(
            f"  Workflow installation availability: not evaluated ({exc}); "
            "no workflow is presented as available."
        )
        return
    print(f"  Workflow installation availability ({label} Skill set):")
    for line in summarize_availability(rows):
        print(f"    {line}")


def setup_skill_profile(
    target: str = "agents",
    skills_dir: str | None = None,
    dry_run: bool = False,
    force: bool = False,
    verbose: bool = False,
    scope: str = "user",
    project_root: str | Path | None = None,
    profile: str | None = None,
    include: Sequence[str] = (),
    update: bool = False,
) -> bool:
    """Install packaged Skill trees to explicitly selected discovery roots.

    Canonical P10 targets:
    - ``generic`` / compatibility alias ``agents``: user/project
      ``.agents/skills``;
    - ``claude``: user/project ``.claude/skills``;
    - ``codex``: personal ``$CODEX_HOME/skills`` (default ``~/.codex/skills``)
      and project ``.agents/skills``;
    - ``opencode``: native OpenCode Skill roots;
    - ``all``: all unique canonical roots (plus the legacy Superpowers cache
      for user scope to preserve pre-P10 behavior);
    - ``custom``: exact caller-supplied directory.

    ``scope=user`` selects user/global roots. ``scope=project`` requires an
    explicit project root and selects project-local discovery roots. No active
    harness is detected automatically.

    ``profile`` selects a dependency-closed installation profile (``entrypoint``
    or ``full``); ``include`` adds named add-ons (for example
    ``product-management``). Omitting both installs every packaged Skill, which
    is the current default. Profiles never change workflow liveness.

    ``update`` replaces copies that are unchanged since setup-skills recorded
    them in the destination's install record and, from a Git checkout, copies
    without a record that equal a committed version of their Skill; changed or
    other unrecorded copies still need ``force``. Outside dry-run, each root's
    install record is refreshed for every selected Skill that ends identical
    to its source.
    """
    try:
        package_skills_dir = get_package_skills_dir()
        skill_names = find_skills_in_package(package_skills_dir)
        if not skill_names:
            raise SkillsSetupError(f"No skills found in {package_skills_dir}")
        profile_name, add_on_names, selected = _select_skill_names(
            skill_names, profile=profile, include=include
        )

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
            print(
                f"Profile: {profile_name}; add-ons: {', '.join(add_on_names) or 'none'}; "
                f"{len(selected)} of {len(skill_names)} Skills selected"
            )
            print(f"Explicit target: {target}")
            print(f"Scope: {scope}")

        all_success = True
        source_kind = _skill_source_kind(package_skills_dir)
        history = _CommittedSkillHistory.for_source(package_skills_dir)
        if verbose:
            print(
                "Committed history for unrecorded copies: "
                + (str(history.repo_root) if history else "not available")
            )
        refused: dict[str, int] = {
            "outdated": 0,
            "historical": 0,
            "changed": 0,
            "unrecorded": 0,
        }
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

            records, record_problem = load_install_record(dest_dir)
            if record_problem:
                print(
                    f"  [!] {record_problem}: {dest_dir / INSTALL_RECORD_NAME} "
                    "is ignored and left unchanged; divergent copies count as "
                    "unrecorded. Remove it to start a new record."
                )
            record_changed = False

            for skill_name in selected:
                src_skill = package_skills_dir / skill_name
                dest_skill = dest_dir / skill_name
                recorded = records.get(skill_name)
                before, match = _classify_install(
                    src_skill, dest_skill, recorded, history
                )
                success, message = _copy_skill_tree(
                    package_skills_dir,
                    dest_dir,
                    skill_name,
                    dry_run=dry_run,
                    force=force,
                    update=update,
                    recorded=recorded,
                    classified=(before, match),
                    history_checked=history is not None,
                )
                symbol = "+" if success else "x"
                print(f"  [{symbol}] {message}")
                if not success:
                    all_success = False
                    # Count policy refusals only; a copy that was allowed but
                    # failed (for example rmtree on a link) is not a refusal.
                    allowed = force or (update and before in _REPLACEABLE_BY_UPDATE)
                    if before in refused and not allowed:
                        refused[before] += 1
                elif not dry_run and record_problem is None:
                    action = {"missing": "installed", "current": "verified"}.get(
                        before, "replaced"
                    )
                    if _refresh_record_entry(
                        records,
                        skill_name,
                        src_skill,
                        dest_skill,
                        action=action,
                        source_kind=source_kind,
                    ):
                        record_changed = True

            if record_changed:
                try:
                    _write_install_record(dest_dir, records)
                except OSError as exc:
                    print(
                        f"  [!] Install record not updated ({type(exc).__name__}: {exc}); "
                        "any earlier record is unchanged, and this run's copies are "
                        "not recorded."
                    )
                else:
                    if verbose:
                        print(f"  Install record: {dest_dir / INSTALL_RECORD_NAME}")

            _report_workflow_availability(
                dest_dir,
                dry_run=dry_run,
                planned=frozenset(selected),
            )

        print(f"\n{'=' * 60}")
        print("Summary")
        print(f"{'=' * 60}")
        if dry_run:
            print("[DRY-RUN MODE] No files were actually installed.")
        print(f"Profile: {profile_name}")
        print(f"Add-ons: {', '.join(add_on_names) or 'none'}")
        print(f"Skills to install: {', '.join(selected)}")
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
            print(
                "\nSkill helper commands (for example `semantic`) need a "
                "sensemaking-skills CLI from the same source as these Skills."
            )
            print(f"These Skills came from sensemaking-skills {__version__}.")
            print("Confirm a CLI before relying on it:")
            print("  sensemaking-skills --version")
            print("  sensemaking-skills semantic --help")
            print(
                "The published PyPI distribution may lag this source and lack "
                "these commands; see INSTALLATION.md for pinned installs."
            )
        else:
            print("\nStatus: PARTIAL FAILURE - Some installations failed")
            if any(refused.values()):
                print("Divergent Skill copies refused above were NOT overwritten.")
                print("Use --force to deliberately replace them.")
            replaceable = []
            if refused["outdated"]:
                replaceable.append(f"Unchanged since recorded: {refused['outdated']}")
            if refused["historical"]:
                replaceable.append(
                    "no install record but identical to a committed version: "
                    f"{refused['historical']}"
                )
            if replaceable:
                replaceable[0] = replaceable[0][0].upper() + replaceable[0][1:]
                print("; ".join(replaceable) + "; --update replaces only these.")
            if refused["changed"] or refused["unrecorded"]:
                unrecorded = (
                    "not matched to an install record or a commit"
                    if history is not None
                    else "no install record"
                )
                print(
                    f"Changed since recorded: {refused['changed']}; "
                    f"{unrecorded}: {refused['unrecorded']}. --update never "
                    "replaces these; inspect them before using --force."
                )

        return all_success

    except SkillsSetupError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return False
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return False


def setup_skills(
    target: str = "agents",
    skills_dir: str | None = None,
    dry_run: bool = False,
    force: bool = False,
    verbose: bool = False,
    scope: str = "user",
    project_root: str | Path | None = None,
) -> bool:
    """Install every packaged Skill tree to explicitly selected discovery roots.

    This is the frozen public entry point. Profile selection is available through
    ``setup_skill_profile`` and the ``setup-skills`` command.
    """
    return setup_skill_profile(
        target=target,
        skills_dir=skills_dir,
        dry_run=dry_run,
        force=force,
        verbose=verbose,
        scope=scope,
        project_root=project_root,
    )
