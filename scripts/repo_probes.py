"""Deterministic repository probes for repo-sensemaker.

Pure probe functions: git subprocess reads and filesystem traversal only.
No pytest subprocess, no network, no writes. Every function returns plain
dicts safe for YAML serialization.
"""

from __future__ import annotations

import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def _git(repo_root: Path, *args: str) -> str:
    """Run a read-only git command; return stdout stripped ('' on failure)."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(repo_root),
            timeout=30,
        )
    except (subprocess.SubprocessError, OSError):
        return ""
    return proc.stdout.strip()


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
            "dirty_file_count": 0,
        }

    branch = _git(repo_root, "symbolic-ref", "--short", "HEAD") or None
    head_sha = _git(repo_root, "rev-parse", "--short", "HEAD") or None
    head_message = _git(repo_root, "log", "-1", "--pretty=%s") or None

    tracked = _git(repo_root, "ls-files").splitlines()
    untracked = _git(repo_root, "ls-files", "--others", "--exclude-standard").splitlines()
    ignored_present = _git(repo_root, "status", "--porcelain=v1", "--ignored").splitlines()
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
    """Ratio of untracked+ignored-present volume to tracked volume."""
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


def test_collection(repo_root: Path) -> Dict[str, object]:
    """Count test files and detect pytest configuration (no pytest subprocess)."""
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
        "pytest_config_present": config_present,
        "markers_declared": markers.strip(),
    }


def fixtures_coverage(repo_root: Path) -> Dict[str, object]:
    """Coverage of validate-*.py scripts by tests/fixtures/<name>/{valid,invalid}."""
    scripts_dir = repo_root / "scripts"
    validators = sorted(
        p.name[:-3]
        for p in scripts_dir.glob("validate-*.py")
        if p.name not in ("validate-and-record.py", "validate-and-report.py")
    )
    covered: List[str] = []
    missing: List[str] = []
    for name in validators:
        base = repo_root / "tests" / "fixtures" / name
        if (base / "valid").is_dir() and (base / "invalid").is_dir():
            covered.append(name)
        else:
            missing.append(name)
    total = len(validators)
    return {
        "total_validators": total,
        "covered_validators": len(covered),
        "missing_fixtures": missing,
        "coverage": round(len(covered) / total, 2) if total else 0.0,
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
