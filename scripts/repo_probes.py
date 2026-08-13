"""Deterministic repository probes for repo-sensemaker.

Pure probe functions: git subprocess reads and filesystem traversal only,
plus one best-effort read-only `pytest --collect-only` subprocess (bounded
timeout, never raising) to count collected test cases for like-for-like
"N tests" comparisons. Every function returns plain dicts safe for YAML
serialization. The only write path is sync_skills(), which copies
repo skills into an installed skills root and must be invoked explicitly.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

try:
    from probe_relationships import relationships  # scripts/ on sys.path (CLI)
except ImportError:  # imported as scripts.repo_probes from tests
    from scripts.probe_relationships import relationships


def _git(repo_root: Path, *args: str) -> str:
    """Run a read-only git command; return stdout stripped ('' on failure)."""
    proc = _git_result(repo_root, *args)
    return proc.stdout.strip() if proc is not None else ""


def _git_result(repo_root: Path, *args: str) -> "subprocess.CompletedProcess[str] | None":
    """Run a read-only git command; None on subprocess failure/timeout.

    Distinct from an empty stdout: callers that need to distinguish
    "measured clean" from "could not measure" (e.g. context_entropy, issue
    #173) must use this instead of _git(), which collapses both to ''.
    """
    try:
        return subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(repo_root),
            timeout=30,
        )
    except (subprocess.SubprocessError, OSError):
        return None


def git_state(repo_root: Path) -> Dict[str, object]:
    """Branch, head, and working-tree volume counts (verified, not documented)."""
    if _git(repo_root, "rev-parse", "--is-inside-work-tree") != "true":
        return {
            "is_git_repo": False,
            "branch": None,
            "head_sha": None,
            "head_message": None,
            "tracked_file_count": 0,
            "untracked_file_count": 0,
            "ignored_present_entry_count": 0,
            "ignored_status_measured": False,
            "dirty_file_count": 0,
        }

    branch = _git(repo_root, "symbolic-ref", "--short", "HEAD") or None
    head_sha = _git(repo_root, "rev-parse", "--short", "HEAD") or None
    head_message = _git(repo_root, "log", "-1", "--pretty=%s") or None

    tracked = _git(repo_root, "ls-files").splitlines()
    untracked = _git(repo_root, "ls-files", "--others", "--exclude-standard").splitlines()
    untracked = [f for f in untracked if not Path(f).name.startswith("probe-report")]
    # The ignored-status call is the one most likely to time out on a
    # sprawling target (auteur: ~10k ignored root JSONs). Failure here is
    # recorded explicitly so context_entropy can report "unmeasured" instead
    # of a false clean reading (issue #173 / evidence-rules Rule 9).
    ignored_proc = _git_result(repo_root, "status", "--porcelain=v1", "--ignored")
    ignored_present = ignored_proc.stdout.splitlines() if ignored_proc is not None else []
    ignored_status_measured = ignored_proc is not None
    porcelain = _git(repo_root, "status", "--porcelain=v1").splitlines()
    dirty = sum(1 for line in porcelain if not line.startswith("??"))

    return {
        "is_git_repo": True,
        "branch": branch,
        "head_sha": head_sha,
        "head_message": head_message,
        "tracked_file_count": len(tracked),
        "untracked_file_count": len(untracked),
        "ignored_present_entry_count": sum(1 for line in ignored_present if line.startswith("!!")),
        "ignored_status_measured": ignored_status_measured,
        "dirty_file_count": dirty,
    }


def churn(repo_root: Path, commits: int = 50) -> Dict[str, object]:
    """Last-N-commit change frequency: descriptive signal, not a forecast."""
    subjects = _git(repo_root, "log", f"-{commits}", "--pretty=%s").splitlines()
    if not subjects:
        return {"commits_scanned": 0, "changed_files_last_n": 0, "top_changed_files": []}

    files = _git(repo_root, "log", f"-{commits}", "--pretty=format:", "--name-only").splitlines()
    counts = Counter(f for f in files if f and not f.startswith("docs/"))
    return {
        "commits_scanned": len(subjects),
        "changed_files_last_n": len(counts),
        "top_changed_files": [name for name, _ in counts.most_common(5)],
    }


CI_FILE_CANDIDATES = (
    ".gitlab-ci.yml",
    ".circleci/config.yml",
)
CI_TOKEN_RE = re.compile(r"(?<![\w./])scripts/[\w./-]+\.py|\bpytest\b")
README_TOKEN_RE = re.compile(r"(?<![\w./])scripts/[\w./-]+\.py")


def _ci_texts(repo_root: Path) -> List[str]:
    texts: List[str] = []
    workflows_dir = repo_root / ".github" / "workflows"
    if workflows_dir.is_dir():
        for p in sorted(workflows_dir.glob("*.y*ml")):
            try:
                texts.append(p.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                pass
    for candidate in CI_FILE_CANDIDATES:
        path = repo_root / candidate
        if path.is_file():
            try:
                texts.append(path.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                pass
    return texts


def ci_enforcement(repo_root: Path) -> Dict[str, object]:
    """Compare README-declared verification entrypoints against CI run steps."""
    readme = repo_root / "README.md"
    declared: List[str] = []
    if readme.is_file():
        try:
            text = readme.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        declared = list(dict.fromkeys(README_TOKEN_RE.findall(text)))

    enforced: List[str] = []
    for ci_text in _ci_texts(repo_root):
        lines = ci_text.splitlines()
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped.lstrip("- ").startswith("run:"):
                continue
            run_line = stripped.lstrip("- ")
            payload_lines = [run_line[len("run:"):]]
            if run_line.rstrip().rstrip("+-").endswith(("|", ">")):
                base_indent = len(line) - len(line.lstrip())
                for cont in lines[i + 1 :]:
                    if not cont.strip():
                        continue
                    if len(cont) - len(cont.lstrip()) <= base_indent:
                        break
                    payload_lines.append(cont)
            for payload in payload_lines:
                enforced.extend(CI_TOKEN_RE.findall(payload))
    enforced = list(dict.fromkeys(enforced))

    declared_in_ci = [check for check in declared if check in enforced]

    if not declared:
        vg = 0.0
        notes = "no declared verification entrypoints found in README"
    elif not enforced:
        vg = 1.0
        notes = "no CI run steps found; all declared checks unenforced"
    else:
        vg = round(1 - len(declared_in_ci) / len(declared), 2)
        notes = "" if vg == 0.0 else "declared-but-unenforced checks detected"

    return {
        "declared_checks": declared,
        "enforced_checks": enforced,
        "declared_in_ci": declared_in_ci,
        "vg": vg,
        "notes": notes,
    }


_BLOAT_DIRS = {".venv", "venv", "node_modules", "build", "dist", ".git", "__pycache__", ".mypy_cache", ".pytest_cache"}


def context_entropy(repo_root: Path) -> Dict[str, object]:
    """Ratio of untracked+ignored-present volume to tracked volume.

    Failure mode (evidence-rules Rule 9 / issue #173): when the
    `git status --ignored` call fails or times out (e.g. a target with tens
    of thousands of ignored files), the metric is unmeasured -- ce is None,
    never a false clean 0.0 that would mask the sprawl the metric exists to
    detect. The report validator accepts ce: null.
    """
    state = git_state(repo_root)
    tracked = state["tracked_file_count"]
    if tracked == 0:
        return {
            "tracked_volume": 0,
            "untracked_volume": state["untracked_file_count"],
            "ignored_present_volume": state["ignored_present_entry_count"],
            "ce": 0.0,
            "notes": "no tracked files; entropy undefined",
        }
    if state.get("ignored_status_measured") is False:
        return {
            "tracked_volume": tracked,
            "untracked_volume": state["untracked_file_count"],
            "ignored_present_volume": state["ignored_present_entry_count"],
            "ce": None,
            "notes": "git status --ignored failed or timed out; context entropy unmeasured",
        }
    untracked = state["untracked_file_count"]
    ignored = state["ignored_present_entry_count"]
    ce = round((untracked + ignored) / tracked, 2)
    return {
        "tracked_volume": tracked,
        "untracked_volume": untracked,
        "ignored_present_volume": ignored,
        "ce": ce,
        "notes": f"untracked+ignored ({untracked + ignored}) / tracked ({tracked})",
    }


def _collect_test_case_count(repo_root: Path) -> Optional[int]:
    """Best-effort `pytest --collect-only -q` test case count.

    Returns the number of collected tests, or None when pytest is unavailable,
    the collection fails, or the run times out. Never raises: a probe must
    never crash on a target whose test suite does not collect cleanly
    (e.g. missing deps, import errors). The count is a like-for-like basis
    for comparing a README's "N tests" claim (see evidence-rules Rule 8).
    """
    try:
        proc = subprocess.run(
            ["python", "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    if proc.returncode != 0:
        return None
    match = re.search(r"(\d+)\s+tests?\s+collected", proc.stdout + "\n" + proc.stderr)
    return int(match.group(1)) if match else None


def test_collection(repo_root: Path) -> Dict[str, object]:
    """Count test files, best-effort collected test cases, and pytest config."""
    count = 0
    for path in repo_root.rglob("*"):
        relative_parts = list(path.relative_to(repo_root).parts)[:-1]
        if any(part in _BLOAT_DIRS for part in relative_parts):
            continue
        if path.is_file() and path.name.endswith(".py") and (path.name.startswith("test_") or path.name.endswith("_test.py")):
            count += 1
    pyproject = repo_root / "pyproject.toml"
    config_present = "[tool.pytest" in pyproject.read_text(encoding="utf-8", errors="replace") if pyproject.is_file() else False
    if not config_present:
        config_present = (repo_root / "pytest.ini").is_file() or (repo_root / "setup.cfg").is_file()
    markers = ""
    if pyproject.is_file():
        match = re.search(r"markers\s*=\s*\[([^\]]*)\]", pyproject.read_text(encoding="utf-8", errors="replace"))
        if match:
            markers = match.group(1)
    return {
        "test_file_count": count,
        "test_case_count": _collect_test_case_count(repo_root),
        "pytest_config_present": config_present,
        "markers_declared": markers.strip(),
    }


def fixtures_coverage(repo_root: Path) -> Dict[str, object]:
    """Coverage of validate-*.py scripts by tests/fixtures/<name>/{valid,invalid}.

    Valid-only convention (issue #173): a target may document that certain
    validators are valid-only -- repo-wide validators cannot have a portable
    unsatisfiable negative fixture (auteur commit 9994238). The convention is
    declared in `tests/fixtures/valid-only.txt` (one validator name per line,
    `#` comments allowed). A validator listed there is covered when its
    `valid/` dir exists, without requiring `invalid/`. Without the marker the
    metric is unchanged, so the probe never invents an exemption.
    """
    scripts_dir = repo_root / "scripts"
    validators = sorted(
        p.name[:-3]
        for p in scripts_dir.glob("validate-*.py")
        if p.name not in ("validate-and-record.py", "validate-and-report.py")
    )
    valid_only: List[str] = []
    marker = repo_root / "tests" / "fixtures" / "valid-only.txt"
    if marker.is_file():
        for raw in marker.read_text(encoding="utf-8", errors="replace").splitlines():
            name = raw.split("#", 1)[0].strip()
            if name and name in validators and name not in valid_only:
                valid_only.append(name)
    covered: List[str] = []
    missing: List[str] = []
    for name in validators:
        base = repo_root / "tests" / "fixtures" / name
        if (base / "valid").is_dir() and (base / "invalid").is_dir():
            covered.append(name)
        elif name in valid_only and (base / "valid").is_dir():
            covered.append(name)
        else:
            missing.append(name)
    total = len(validators)
    return {
        "total_validators": total,
        "covered_validators": len(covered),
        "missing_fixtures": missing,
        "coverage": round(len(covered) / total, 2) if total else 0.0,
        "valid_only": valid_only,
    }


def _read_bytes(path: Path) -> bytes | None:
    """Read raw file bytes; None on any OSError (caller decides how to treat it)."""
    try:
        return path.read_bytes()
    except OSError:
        return None


def probe_skill_distribution(
    repo_root: Path, installed_skills_root: Path | None = None
) -> Dict[str, object]:
    """Compare canonical skills/*/SKILL.md against installed copies.

    Installed copies default to ~/.agents/skills; Path.home() resolves both
    Windows (C:\\Users\\<user>\\.agents\\skills) and Unix (/home/<user>/.agents/skills)
    home locations. Pure filesystem + hashlib reads, no writes, no subprocess.

    Each skill is categorized by a drift_type:
      - "none": raw bytes identical; counted in synchronized_count, NOT listed
        in drifted_skills.
      - "line_ending_only": identical after LF normalization (CRLF vs LF only).
      - "content_drift": real content difference beyond line endings.
      - "missing_installed": installed copy missing or unreadable.
    A repo skill whose installed copy is missing or unreadable counts as
    drifted (hash_match False, installed_lines None).
    """
    if installed_skills_root is None:
        installed_skills_root = Path.home() / ".agents" / "skills"

    drifted_skills: List[Dict[str, object]] = []
    synchronized_count = 0
    line_ending_drift_count = 0
    content_drift_count = 0
    missing_installed_count = 0
    total_skills_checked = 0

    repo_skills_dir = repo_root / "skills"
    for skill_md in sorted(repo_skills_dir.glob("*/SKILL.md")):
        skill_name = skill_md.parent.name
        total_skills_checked += 1

        repo_data = _read_bytes(skill_md)
        installed_md = installed_skills_root / skill_name / "SKILL.md"
        installed_data = _read_bytes(installed_md) if installed_md.is_file() else None

        if repo_data is None:
            repo_lines: int | None = None
            repo_raw_hash: str | None = None
            repo_lf_hash: str | None = None
        else:
            repo_lines = len(repo_data.decode("utf-8", errors="replace").splitlines())
            repo_raw_hash = hashlib.sha256(repo_data).hexdigest()
            repo_lf_hash = hashlib.sha256(repo_data.replace(b"\r\n", b"\n")).hexdigest()

        if installed_data is None:
            installed_lines: int | None = None
            installed_raw_hash: str | None = None
            installed_lf_hash: str | None = None
        else:
            installed_lines = len(installed_data.decode("utf-8", errors="replace").splitlines())
            installed_raw_hash = hashlib.sha256(installed_data).hexdigest()
            installed_lf_hash = hashlib.sha256(installed_data.replace(b"\r\n", b"\n")).hexdigest()

        hash_match = (
            repo_raw_hash is not None
            and installed_raw_hash is not None
            and repo_raw_hash == installed_raw_hash
        )
        if hash_match:
            drift_type = "none"
        elif installed_raw_hash is None:
            drift_type = "missing_installed"
        elif repo_lf_hash is not None and repo_lf_hash == installed_lf_hash:
            drift_type = "line_ending_only"
        else:
            drift_type = "content_drift"

        if drift_type == "none":
            synchronized_count += 1
            continue
        if drift_type == "line_ending_only":
            line_ending_drift_count += 1
        elif drift_type == "content_drift":
            content_drift_count += 1
        else:
            missing_installed_count += 1
        drifted_skills.append(
            {
                "skill_name": skill_name,
                "repo_lines": repo_lines,
                "installed_lines": installed_lines,
                "hash_match": hash_match,
                "drift_type": drift_type,
            }
        )

    return {
        "total_skills_checked": total_skills_checked,
        "synchronized_count": synchronized_count,
        "line_ending_drift_count": line_ending_drift_count,
        "content_drift_count": content_drift_count,
        "missing_installed_count": missing_installed_count,
        "drifted_skills": drifted_skills,
    }


def sync_skills(
    repo_root: Path,
    installed_skills_root: Path | None = None,
    overwrite_content_drift: bool = True,
) -> Dict[str, object]:
    """Synchronize repo skills into the installed skills root (explicit write path).

    Uses the same drift categorization as probe_skill_distribution(): skills
    missing from the install are copied in full; content-drifted skills are
    overwritten when overwrite_content_drift is True (default). Skills that
    differ only by line endings are left untouched -- their installed copy is
    treated as equivalent. Returns a summary dict listing the synced skills.
    """
    if installed_skills_root is None:
        installed_skills_root = Path.home() / ".agents" / "skills"

    payload = probe_skill_distribution(repo_root, installed_skills_root)
    synced_skills: List[str] = []
    for entry in payload["drifted_skills"]:
        skill_name = entry["skill_name"]
        drift_type = entry["drift_type"]
        if drift_type == "missing_installed":
            shutil.copytree(
                repo_root / "skills" / skill_name,
                installed_skills_root / skill_name,
                dirs_exist_ok=True,
            )
            synced_skills.append(skill_name)
        elif drift_type == "content_drift" and overwrite_content_drift:
            shutil.copytree(
                repo_root / "skills" / skill_name,
                installed_skills_root / skill_name,
                dirs_exist_ok=True,
            )
            synced_skills.append(skill_name)

    return {
        "synced_skill_count": len(synced_skills),
        "synced_skills": synced_skills,
    }


def probe_all(repo_root: Path, churn_commits: int = 50) -> Dict[str, object]:
    """Run every probe; assemble the machine-readable report payload."""
    return {
        "schema_version": 1,
        "probe_tool": "sensemaking-skills probe-repo v1",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo_root": str(repo_root),
        "git_state": git_state(repo_root),
        "verification_gap": ci_enforcement(repo_root),
        "context_entropy": context_entropy(repo_root),
        "test_collection": test_collection(repo_root),
        "fixtures_coverage": fixtures_coverage(repo_root),
        "churn": churn(repo_root, commits=churn_commits),
        "relationships": relationships(repo_root),
    }


def append_probe_section(prompt_parts: List[str], probe_report_path: Path) -> None:
    """Append the probe-report block to an assembled prompt if the report exists."""
    if not probe_report_path.is_file():
        return
    prompt_parts.extend([
        "",
        "## Repository Probe Report",
        "The runtime pre-ran `scripts/probe-repo.py`; values below are verified "
        "current state, measured on the checked-out tree. Prefer them over "
        "documented claims (state-currency verification).",
        f"`{probe_report_path}`",
        "",
        "```yaml",
        probe_report_path.read_text(encoding="utf-8"),
        "```",
    ])
