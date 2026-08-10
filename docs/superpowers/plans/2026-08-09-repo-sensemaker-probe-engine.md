# Repo-Sensemaker Probe Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give `repo-sensemaker` a deterministic probe engine (`scripts/probe-repo.py` + `scripts/repo_probes.py`) that pre-computes verified-current-state metrics — git state, verification gap $V_g$, context entropy $C_e$, test collection, validator-fixture coverage, and change churn — into a machine-readable `probe-report.yaml`, and wire that report into the SKILL.md probe rules and the runtime prompt assembly.

**Architecture:** Three layers. (1) `scripts/repo_probes.py` — pure, testable probe functions (git subprocess + filesystem reads only; no pytest subprocess, no network). (2) `scripts/probe-repo.py` — thin CLI that runs every probe, writes `probe-report.yaml`, prints a 6-line summary, exits 0. (3) Consumers: a new `scripts/validate-probe-report.py` in the existing validator harness (with valid/invalid fixtures), a "Probe Engine" section in `skills/repo-sensemaker/SKILL.md`, and a prompt-injection helper used by `scripts/skill_executor.py`. This implements Research Path 3 (quantified fog metrics) fully, the probe half of Path 1 (empirical instead of derived evidence), and a bounded slice of Path 4 (churn as a scored input).

**Tech Stack:** Python 3.11+ (stdlib + `PyYAML` only), git CLI via `subprocess`, pytest with `tmp_path` for real-git fixtures, the existing `scripts/test-validators.py` harness conventions (frontmatter `validator_case` / `expected_error_contains`).

---

## Out of scope (explicit)

- **Path 2 (semantic knowledge graphs)** and **Path 5 (closed-loop eval feedback)** — shelved by design decision; no code.
- **Auteur repo remediation** — separate plan (its brief recommends `architecture-implementation-workflow`).
- **`src/sensemaking_skills/skills/repo_sensemaker.py`** — legacy trivial Python implementation, superseded by SKILL.md + runtime envelope path. Left untouched; flag as a separate cleanup ticket, do not modify here.
- **`src/sensemaking_skills/exploratory_execution/prompt_builder.py`** — exploratory campaign prompt construction; the mainline `skill_executor.py` assembly is the only injection point in this plan.

---

## File Structure

| File | Role |
| :--- | :--- |
| `scripts/repo_probes.py` (create) | Pure probe library: `git_state`, `ci_enforcement`, `context_entropy`, `test_collection`, `fixtures_coverage`, `churn`, plus `probe_all` and `append_probe_section`. No side effects except git subprocess reads. |
| `scripts/probe-repo.py` (create) | CLI: `--repo-root`, `--output`, `--churn-commits`; writes `probe-report.yaml`; prints summary; exit 0 on success, 2 on unreachable repo. |
| `scripts/validate-probe-report.py` (create) | Validator for `probe-report.yaml` (schema_version, required keys, Vg range, Ce non-negative). Follows the harness contract (argparse `--repo-root`, exit 1, error codes as printed substrings). |
| `tests/test_repo_probes.py` (create) | Unit tests for every probe function using `git init`'d `tmp_path` repos. |
| `tests/test_probe_report_cli.py` (create) | CLI golden tests: writes report, exit codes, output filename honoring `--output`. |
| `tests/test_probe_prompt_injection.py` (create) | Unit test for `append_probe_section`. |
| `tests/fixtures/validate-probe-report/valid/sample.yaml` (create) | Positive fixture (frontmatter-less; body is a complete valid report). |
| `tests/fixtures/validate-probe-report/invalid/missing_key.yaml` (create) | Negative fixture: `context_entropy` key removed; `expected_error_contains: PROBE_REPORT_MISSING_KEY`. |
| `tests/fixtures/validate-probe-report/invalid/vg_out_of_range.yaml` (create) | Negative fixture: `vg: 1.5`; `expected_error_contains: PROBE_REPORT_VG_RANGE`. |
| `skills/repo-sensemaker/SKILL.md` (modify) | New "Probe Engine" section (evidence hierarchy, mandatory probe step, fallback labeling). |
| `scripts/skill_executor.py` (modify, ~line 2331) | Call `append_probe_section` when `context["probe_report_path"]` exists. |
| `README.md` (modify) | "Probe Engine" section under a new "Tooling" heading. |
| `CONTEXT.md` (modify) | Vocabulary entries for `probe-report`, `Vg`, `Ce` in a new "Probe Engine" subsection. |

---

## Task 1: git state + churn probes (`scripts/repo_probes.py`)

**Files:**
- Create: `scripts/repo_probes.py`
- Test: `tests/test_repo_probes.py`

- [ ] **Step 1: Write the failing test**

```python
import subprocess
from pathlib import Path

import pytest

from scripts.repo_probes import git_state, churn


def _init_committed_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"], check=True)
    (repo / "file.txt").write_text("one", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "initial"], check=True)
    (repo / "file.txt").write_text("two", encoding="utf-8")
    (repo / "untracked.txt").write_text("u", encoding="utf-8")
    return repo


def test_git_state_reports_verified_current_state(tmp_path: Path) -> None:
    repo = _init_committed_repo(tmp_path)
    state = git_state(repo)
    assert state["is_git_repo"] is True
    assert state["branch"] == "main"
    assert state["head_message"] == "initial"
    assert state["tracked_file_count"] == 1
    assert state["untracked_file_count"] == 1
    assert state["dirty_file_count"] == 1
    assert len(state["head_sha"]) >= 7


def test_git_state_reports_non_git_directory(tmp_path: Path) -> None:
    state = git_state(tmp_path)
    assert state["is_git_repo"] is False
    assert state["tracked_file_count"] == 0


def test_churn_reports_top_changed_files(tmp_path: Path) -> None:
    repo = _init_committed_repo(tmp_path)
    report = churn(repo, commits=10)
    assert report["commits_scanned"] == 1
    assert report["top_changed_files"] == ["file.txt"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_repo_probes.py -v --tb=short`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.repo_probes'` (and `scripts/__init__.py` missing if needed; create an empty `scripts/__init__.py` only if the import error says so).

- [ ] **Step 3: Implement `git_state` and `churn`**

Add to `scripts/repo_probes.py` (new file, full contents below; a stub `probe_all` will be replaced in later tasks):

```python
"""Deterministic repository probes for repo-sensemaker.

Pure probe functions: git subprocess reads and filesystem traversal only.
No pytest subprocess, no network, no writes. Every function returns plain
dicts safe for YAML serialization.
"""

from __future__ import annotations

import subprocess
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional


def _git(repo_root: Path, *args: str) -> str:
    """Run a read-only git command; return stdout stripped ('' on failure)."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True,
            text=True,
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
    ignored_present = _git(repo_root, "status", "--porcelain=v1", "-uno", "--ignored").splitlines()
    porcelain = _git(repo_root, "status", "--porcelain=v1").splitlines()
    dirty = sum(1 for line in porcelain if not line.startswith("??"))

    return {
        "is_git_repo": True,
        "branch": branch,
        "head_sha": head_sha,
        "head_message": head_message,
        "tracked_file_count": len(tracked),
        "untracked_file_count": len(untracked),
        "ignored_present_entry_count": len(ignored_present),
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_repo_probes.py -v --tb=short`
Expected: 3 PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/repo_probes.py tests/test_repo_probes.py
git commit -m "feat(probes): git state + churn probes with tmp-git-repo tests"
```

---

## Task 2: verification-gap probe ($V_g$)

**Files:**
- Modify: `scripts/repo_probes.py`
- Test: `tests/test_repo_probes.py`

$V_g = 1 - \frac{|declared\_checks \cap enforced\_checks|}{|declared\_checks|}$, computed from README declarations vs. CI workflow `run:` steps. Deterministic rules:

- `declared_checks`: every `scripts/<name>.py` path mentioned in `README.md` (regex `scripts/[\w./-]+\.py`). The literal `pytest` token in README does **not** declare a check — the executable fixtures define this semantics (resolution of an internal plan contradiction, user-approved 2026-08-10).
- `enforced_checks`: from `.github/workflows/*.{yml,yaml}` (and `.gitlab-ci.yml`, `.circleci/config.yml` if present), every token matching `scripts/[\w./-]+\.py` or the literal `pytest` in any `run:` step (YAML list items `- run: ...` included; strip leading `- ` before matching).
- `vg`: `1.0` when there are declared checks but zero CI files or zero enforced checks (Contract-Mismatch signal); `0.0` when no checks are declared at all; otherwise `1 - matched/declared`, rounded to 2 decimals.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_repo_probes.py`:

```python
from scripts.repo_probes import ci_enforcement


def _repo_with_readme_and_ci(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / "README.md").write_text(
        "## Verification\nCI runs the same entrypoint: `python scripts/check.py` and pytest.\n",
        encoding="utf-8",
    )
    (repo / ".github" / "workflows" / "validation.yml").write_text(
        "jobs:\n  test:\n    steps:\n      - run: pytest -q\n",
        encoding="utf-8",
    )
    return repo


def test_verification_gap_detects_unenforced_ci_claim(tmp_path: Path) -> None:
    report = ci_enforcement(_repo_with_readme_and_ci(tmp_path))
    assert report["declared_checks"] == ["scripts/check.py"]
    assert report["enforced_checks"] == ["pytest"]
    assert report["declared_in_ci"] == []
    assert report["vg"] == 1.0


def test_verification_gap_zero_when_fully_enforced(tmp_path: Path) -> None:
    repo = _repo_with_readme_and_ci(tmp_path)
    (repo / ".github" / "workflows" / "validation.yml").write_text(
        "jobs:\n  test:\n    steps:\n      - run: python scripts/check.py\n",
        encoding="utf-8",
    )
    report = ci_enforcement(repo)
    assert report["declared_in_ci"] == ["scripts/check.py"]
    assert report["vg"] == 0.0


def test_verification_gap_zero_when_no_checks_declared(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("Nothing about verification here.\n", encoding="utf-8")
    report = ci_enforcement(repo)
    assert report["declared_checks"] == []
    assert report["vg"] == 0.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_repo_probes.py -v --tb=short`
Expected: FAIL — `ImportError: cannot import name 'ci_enforcement'`.

- [ ] **Step 3: Implement `ci_enforcement`**

Append to `scripts/repo_probes.py`:

```python
import re

CI_FILE_CANDIDATES = (
    ".gitlab-ci.yml",
    ".circleci/config.yml",
)
CI_TOKEN_RE = re.compile(r"scripts/[\w./-]+\.py|\bpytest\b")
README_TOKEN_RE = re.compile(r"scripts/[\w./-]+\.py")


def _ci_texts(repo_root: Path) -> List[str]:
    texts: List[str] = []
    workflows_dir = repo_root / ".github" / "workflows"
    if workflows_dir.is_dir():
        texts.extend(
            p.read_text(encoding="utf-8", errors="replace")
            for p in sorted(workflows_dir.glob("*.y*ml"))
        )
    for candidate in CI_FILE_CANDIDATES:
        path = repo_root / candidate
        if path.is_file():
            texts.append(path.read_text(encoding="utf-8", errors="replace"))
    return texts


def ci_enforcement(repo_root: Path) -> Dict[str, object]:
    """Compare README-declared verification entrypoints against CI run steps."""
    readme = repo_root / "README.md"
    declared: List[str] = []
    if readme.is_file():
        text = readme.read_text(encoding="utf-8", errors="replace")
        declared = list(dict.fromkeys(CI_TOKEN_RE.findall(text)))

    enforced: List[str] = []
    for ci_text in _ci_texts(repo_root):
        for line in ci_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("run:"):
                enforced.extend(CI_TOKEN_RE.findall(stripped))
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_repo_probes.py -v --tb=short`
Expected: 6 PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/repo_probes.py tests/test_repo_probes.py
git commit -m "feat(probes): verification-gap probe (Vg) from README vs CI run steps"
```

---

## Task 3: context-entropy, test-collection, fixtures-coverage probes

**Files:**
- Modify: `scripts/repo_probes.py`
- Test: `tests/test_repo_probes.py`

$C_e = \frac{untracked\_volume + ignored\_present\_volume}{tracked\_volume}$ — bounded, cheap, deterministic (git status output only; no deep ignored walks).

- [ ] **Step 1: Write the failing test**

Append to `tests/test_repo_probes.py`:

```python
from scripts.repo_probes import context_entropy, fixtures_coverage, test_collection


def test_context_entropy_uses_tracked_volume_as_denominator(tmp_path: Path) -> None:
    repo = _init_committed_repo(tmp_path)  # 1 tracked, 1 untracked, 1 dirty
    report = context_entropy(repo)
    assert report["tracked_volume"] == 1
    assert report["untracked_volume"] == 1
    assert report["ce"] == 1.0


def test_context_entropy_zero_for_empty_directory(tmp_path: Path) -> None:
    report = context_entropy(tmp_path)
    assert report["ce"] == 0.0


def test_test_collection_counts_test_files_only(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "tests").mkdir(parents=True)
    (repo / "tests" / "test_one.py").write_text("", encoding="utf-8")
    (repo / "tests" / "test_two.py").write_text("", encoding="utf-8")
    (repo / "src.py").write_text("", encoding="utf-8")
    (repo / "pyproject.toml").write_text("[tool.pytest.ini_options]\naddopts = \"-q\"\n", encoding="utf-8")
    report = test_collection(repo)
    assert report["test_file_count"] == 2
    assert report["pytest_config_present"] is True


def test_fixtures_coverage_reports_missing_fixture_dirs(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    (repo / "scripts" / "validate-demo.py").write_text("pass\n", encoding="utf-8")
    # No tests/fixtures/validate-demo directory at all.
    report = fixtures_coverage(repo)
    assert report["total_validators"] == 1
    assert report["covered_validators"] == 0
    assert report["missing_fixtures"] == ["validate-demo"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_repo_probes.py -v --tb=short`
Expected: FAIL — `ImportError: cannot import name 'context_entropy'`.

- [ ] **Step 3: Implement the three probes**

Append to `scripts/repo_probes.py`:

```python
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
        if path.is_file() and (path.name.startswith("test_") or path.name.endswith("_test.py")):
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_repo_probes.py -v --tb=short`
Expected: 10 PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/repo_probes.py tests/test_repo_probes.py
git commit -m "feat(probes): context-entropy, test-collection, fixture-coverage probes"
```

---

## Task 4: probe CLI (`scripts/probe-repo.py`) and `probe_all`

**Files:**
- Modify: `scripts/repo_probes.py` (add `probe_all`, `append_probe_section`)
- Create: `scripts/probe-repo.py`
- Test: `tests/test_probe_report_cli.py`, `tests/test_probe_prompt_injection.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_probe_report_cli.py`:

```python
import subprocess
import sys
from pathlib import Path

import yaml


def _committed_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"], check=True)
    (repo / "README.md").write_text("## Verification\nCI runs `python scripts/check.py`.\n", encoding="utf-8")
    (repo / "scripts").mkdir()
    (repo / "scripts" / "check.py").write_text("pass\n", encoding="utf-8")
    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / ".github" / "workflows" / "ci.yml").write_text(
        "jobs:\n  t:\n    steps:\n      - run: python scripts/check.py\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "initial"], check=True)
    return repo


def test_cli_writes_report_and_exits_zero(tmp_path: Path) -> None:
    repo = _committed_repo(tmp_path)
    out = tmp_path / "report.yaml"
    proc = subprocess.run(
        [sys.executable, "scripts/probe-repo.py", "--repo-root", str(repo), "--output", str(out)],
        capture_output=True, text=True, cwd=repo,
    )
    assert proc.returncode == 0, proc.stderr
    assert out.is_file()
    data = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert data["schema_version"] == 1
    assert data["git_state"]["is_git_repo"] is True
    assert data["verification_gap"]["vg"] == 0.0
    assert data["fixtures_coverage"]["total_validators"] == 0
    summary = proc.stdout
    assert "REPO PROBE SUMMARY" in summary
    assert "Vg" in summary and "Ce" in summary
```

Create `tests/test_probe_prompt_injection.py`:

```python
from pathlib import Path
from scripts.repo_probes import append_probe_section


def test_append_probe_section_adds_report(tmp_path: Path) -> None:
    report = tmp_path / "probe-report.yaml"
    report.write_text("schema_version: 1\n", encoding="utf-8")
    parts: list[str] = ["## Skill Definition", "body"]
    append_probe_section(parts, report)
    joined = "\n".join(parts)
    assert "## Repository Probe Report" in joined
    assert "schema_version: 1" in joined


def test_append_probe_section_skips_missing_report(tmp_path: Path) -> None:
    parts: list[str] = ["## Skill Definition", "body"]
    append_probe_section(parts, tmp_path / "missing.yaml")
    assert len(parts) == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_probe_report_cli.py tests/test_probe_prompt_injection.py -v --tb=short`
Expected: FAIL — `FileNotFoundError` / import errors (`probe-repo` script absent, `append_probe_section` undefined).

- [ ] **Step 3: Implement `probe_all`, `append_probe_section`, and the CLI**

Append to `scripts/repo_probes.py`:

```python
from datetime import datetime, timezone


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
```

Create `scripts/probe-repo.py`:

```python
"""Probe engine CLI for repo-sensemaker.

Usage:
    python scripts/probe-repo.py [--repo-root PATH] [--output PATH] [--churn-commits N]

Writes probe-report.yaml (default), prints a bounded summary to stdout, exits 0.
Exit 2: --repo-root does not exist or is not a directory.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from repo_probes import probe_all

SUMMARY_LINES = 6


def _summary(report: dict, output: Path) -> str:
    git = report["git_state"]
    vg = report["verification_gap"]
    ce = report["context_entropy"]
    coll = report["test_collection"]
    fx = report["fixtures_coverage"]
    ch = report["churn"]
    head = git.get("head_sha") or "no-commits"
    lines = [
        "REPO PROBE SUMMARY%s" % (f" -> {output}" if output else ""),
        f"  git: {git.get('branch') or '-'} @ {head} | "
        f"tracked={git['tracked_file_count']} untracked={git['untracked_file_count']} dirty={git['dirty_file_count']}",
        f"  Vg (verification gap): {vg['vg']} | declared={vg['declared_checks']} enforced={vg['enforced_checks']}",
        f"  Ce (context entropy): {ce['ce']} | {ce['notes']}",
        f"  tests: {coll['test_file_count']} files | pytest-config={coll['pytest_config_present']}",
        f"  fixture coverage: {fx['covered_validators']}/{fx['total_validators']} "
        f"({fx['coverage']}) missing={fx['missing_fixtures']}",
        f"  churn: {ch['commits_scanned']} commits, {ch['changed_files_last_n']} files; top: {ch['top_changed_files']}",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic repository probes.")
    parser.add_argument("--repo-root", default=".", help="Repository to probe (default: current dir)")
    parser.add_argument("--output", default="probe-report.yaml", help="Report output path")
    parser.add_argument("--churn-commits", type=int, default=50, help="Commits to scan for churn")
    parser.add_argument("--no-write", action="store_true", help="Print summary only")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    if not repo_root.is_dir():
        print(f"[probe] ERROR: repo-root is not a directory: {repo_root}", file=sys.stderr)
        return 2

    report = probe_all(repo_root, churn_commits=args.churn_commits)

    output: Path | None = None
    if not args.no_write:
        output = Path(args.output).resolve()
        output.write_text(yaml.safe_dump(report, sort_keys=False), encoding="utf-8")

    print(_summary(report, output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

Note: `scripts/probe-repo.py` imports `repo_probes` by name because `scripts/` is on `sys.path` when run as `python scripts/probe-repo.py` (same convention as `validate-brief.py` importing `_validator_utils`).

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_probe_report_cli.py tests/test_probe_prompt_injection.py -v --tb=short`
Expected: 3 PASS.

- [ ] **Step 5: Manual smoke on a real repo**

Run: `python scripts/probe-repo.py --repo-root . --output .\tmp-probe-smoke.yaml --no-write`
Expected: prints the 7-line `REPO PROBE SUMMARY` block; exit 0. Delete `.tmp-probe-smoke.yaml` if created without `--no-write`.

- [ ] **Step 6: Commit**

```bash
git add scripts/repo_probes.py scripts/probe-repo.py tests/test_probe_report_cli.py tests/test_probe_prompt_injection.py
git commit -m "feat(probes): probe-repo CLI writing probe-report.yaml with summary"
```

---

## Task 5: report validator (`scripts/validate-probe-report.py`) + fixtures

**Files:**
- Create: `scripts/validate-probe-report.py`
- Create: `tests/fixtures/validate-probe-report/valid/sample.yaml`
- Create: `tests/fixtures/validate-probe-report/invalid/missing_key.yaml`
- Create: `tests/fixtures/validate-probe-report/invalid/vg_out_of_range.yaml`
- Test: (harness) `python scripts/test-validators.py` — must include `validate-probe-report`

- [ ] **Step 1: Write the failing fixtures**

Create `tests/fixtures/validate-probe-report/valid/sample.yaml`:

```yaml
schema_version: 1
probe_tool: sensemaking-skills probe-repo v1
generated_at: "2026-08-09T12:00:00Z"
repo_root: .
git_state:
  is_git_repo: true
  branch: main
  head_sha: abc1234
  head_message: initial
  tracked_file_count: 10
  untracked_file_count: 5
  ignored_present_entry_count: 2
  dirty_file_count: 1
verification_gap:
  declared_checks: [scripts/check.py]
  enforced_checks: [scripts/check.py]
  declared_in_ci: [scripts/check.py]
  vg: 0.0
  notes: ""
context_entropy:
  tracked_volume: 10
  untracked_volume: 5
  ignored_present_volume: 2
  ce: 0.7
  notes: "untracked+ignored (7) / tracked (10)"
test_collection:
  test_file_count: 3
  pytest_config_present: true
  markers_declared: ""
fixtures_coverage:
  total_validators: 2
  covered_validators: 2
  missing_fixtures: []
  coverage: 1.0
churn:
  commits_scanned: 50
  changed_files_last_n: 40
  top_changed_files: [identity.py, validate-identity.py]
```

Create `tests/fixtures/validate-probe-report/invalid/missing_key.yaml`:

```yaml
---
validator_case: negative
expected_error_contains: PROBE_REPORT_MISSING_KEY
---
schema_version: 1
probe_tool: sensemaking-skills probe-repo v1
generated_at: "2026-08-09T12:00:00Z"
repo_root: .
git_state:
  is_git_repo: true
  branch: main
  head_sha: abc1234
  head_message: initial
  tracked_file_count: 1
  untracked_file_count: 0
  ignored_present_entry_count: 0
  dirty_file_count: 0
verification_gap:
  declared_checks: []
  enforced_checks: []
  declared_in_ci: []
  vg: 0.0
  notes: ""
churn:
  commits_scanned: 0
  changed_files_last_n: 0
  top_changed_files: []
```

Create `tests/fixtures/validate-probe-report/invalid/vg_out_of_range.yaml`:

```yaml
---
validator_case: negative
expected_error_contains: PROBE_REPORT_VG_RANGE
---
schema_version: 1
probe_tool: sensemaking-skills probe-repo v1
generated_at: "2026-08-09T12:00:00Z"
repo_root: .
git_state:
  is_git_repo: false
  branch: null
  head_sha: null
  head_message: null
  tracked_file_count: 0
  untracked_file_count: 0
  ignored_present_entry_count: 0
  dirty_file_count: 0
verification_gap:
  declared_checks: []
  enforced_checks: []
  declared_in_ci: []
  vg: 1.5
  notes: ""
context_entropy:
  tracked_volume: 0
  untracked_volume: 0
  ignored_present_volume: 0
  ce: 0.0
  notes: "no tracked files; entropy undefined"
test_collection:
  test_file_count: 0
  pytest_config_present: false
  markers_declared: ""
fixtures_coverage:
  total_validators: 0
  covered_validators: 0
  missing_fixtures: []
  coverage: 0.0
churn:
  commits_scanned: 0
  changed_files_last_n: 0
  top_changed_files: []
```

- [ ] **Step 2: Run harness to verify negative fixtures fail now**

Run: `python scripts/test-validators.py`
Expected: FAIL list includes `validate-probe-report` (`FileNotFoundError` — validator script does not exist yet). This is the red state; Task 5 continues immediately to green.

- [ ] **Step 3: Implement the validator**

Create `scripts/validate-probe-report.py`:

```python
"""Validator for probe-report.yaml produced by scripts/probe-repo.py.

Error codes (substrings matched by tests/fixtures/validate-probe-report/):
  PROBE_REPORT_NOT_FOUND
  PROBE_REPORT_PARSE_ERROR
  PROBE_REPORT_SCHEMA_VERSION
  PROBE_REPORT_MISSING_KEY
  PROBE_REPORT_VG_RANGE
  PROBE_REPORT_CE_NEGATIVE
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

import yaml

REQUIRED_KEYS = (
    "schema_version",
    "probe_tool",
    "generated_at",
    "repo_root",
    "git_state",
    "verification_gap",
    "context_entropy",
    "test_collection",
    "fixtures_coverage",
    "churn",
)

FRONTMATTER_RE = re.compile(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n", re.DOTALL)


def load_report(path: Path) -> Optional[dict]:
    """Load a probe report, tolerating the harness's frontmatter convention."""
    if not path.is_file():
        print("[PROBE_REPORT_NOT_FOUND] report file not found: " + str(path))
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"[PROBE_REPORT_PARSE_ERROR] unreadable: {exc}")
        return None
    body = FRONTMATTER_RE.sub("", text, count=1)
    try:
        data = yaml.safe_load(body)
    except yaml.YAMLError as exc:
        print(f"[PROBE_REPORT_PARSE_ERROR] invalid YAML: {exc}")
        return None
    if not isinstance(data, dict):
        print("[PROBE_REPORT_PARSE_ERROR] report is not a mapping")
        return None
    return data


def validate_report(data: dict) -> bool:
    ok = True

    if data.get("schema_version") != 1:
        print("[PROBE_REPORT_SCHEMA_VERSION] expected schema_version 1")
        ok = False

    for key in REQUIRED_KEYS:
        if key not in data:
            print(f"[PROBE_REPORT_MISSING_KEY] missing required key: {key}")
            ok = False

    vg = (data.get("verification_gap") or {}).get("vg")
    if vg is not None and not isinstance(vg, (int, float)):
        print("[PROBE_REPORT_VG_RANGE] vg must be numeric")
        ok = False
    elif vg is not None and not (0.0 <= float(vg) <= 1.0):
        print(f"[PROBE_REPORT_VG_RANGE] vg out of range [0,1]: {vg}")
        ok = False

    ce = (data.get("context_entropy") or {}).get("ce")
    if ce is not None and isinstance(ce, (int, float)) and float(ce) < 0.0:
        print(f"[PROBE_REPORT_CE_NEGATIVE] ce must be >= 0: {ce}")
        ok = False

    return ok


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate a probe-report.yaml")
    parser.add_argument("report_path", help="Path to the probe report (or negative fixture)")
    parser.add_argument("--repo-root", default=".", help="Unused by this validator; harness contract")
    args = parser.parse_args(argv)

    data = load_report(Path(args.report_path))
    if data is None:
        return 1
    return 0 if validate_report(data) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run harness to verify all three cases pass**

Run: `python scripts/test-validators.py`
Expected: the harness reports `validate-probe-report` PASS for valid + both invalid cases (error substrings matched); entire harness exits 0.

- [ ] **Step 5: Commit**

```bash
git add scripts/validate-probe-report.py tests/fixtures/validate-probe-report
git commit -m "feat(probes): validate-probe-report validator + valid/invalid fixtures"
```

---

## Task 6: SKILL.md Probe Engine integration

**Files:**
- Modify: `skills/repo-sensemaker/SKILL.md`

- [ ] **Step 1: Add the Probe Engine section**

Insert a new section after `## Evidence Rules`'s standard-workflow item and before `## Output Format`. Concretely, insert the following block right before the `## Output Format` heading (line 94):

````markdown
## Probe Engine (verified current state, mandatory before synthesis)

Deterministic probes replace *derived* evidence (text inspection) with *measured*
current-state evidence. Before writing Sections 3–9, run the probe engine against
the target repository:

```powershell
python scripts/probe-repo.py --repo-root <target-repo> [--output <path>/probe-report.yaml]
```

Then:

1. **Read `probe-report.yaml`.** Its values are verified current state, measured
   on the checked-out tree — prefer them over any documented claim (state-currency
   verification, per Standard Workflow item 4).
2. **Surface the numbers in your prose.** The report's `verification_gap.vg`,
   `context_entropy.ce`, `fixtures_coverage.coverage`, and `churn` fields feed
   directly into the missing-pieces, weakest-boundary, and evidence sections.
   A `vg > 0` with declared-but-unenforced checks is a `Contract Mismatch` signal;
   `vg == 1.0` means every declared check is unenforced (or CI is absent).
   `ce >= 5` triggers a hygiene warning about untracked/ignored artifact sprawl.
   A non-empty `missing_fixtures` list signals validator orphans (Zero Validation
   or Orphaned Examples candidates).
3. **Cite the probe in Section 8.** Every excerpt that rests on a measured value
   must reference the probe that produced it (e.g.
   `probe-report.yaml:verification_gap.vg`), plus the usual `file:lines`.
4. **Probe failure fallback.** If the probe exits nonzero or the target is not a
   git repository (`is_git_repo: false`), the probe still reports directory-level
   facts; any claim you cannot measure must be labeled
   "documented but not independently verified" (per Standard Workflow item 4 and
   Section 8). Never skip the probe because a repo "looks simple" — a
   non-git repo is itself a finding.
````

- [ ] **Step 2: Update the evidence-authority hierarchy**

In the "Evidence-authority hierarchy and grammar" paragraph of the runtime-owned-section (around line 153), replace the sentence

`prefer direct code/config over comments over external docs when they conflict`

with

`probe-report.yaml (measured current state) sits above direct code/config; prefer probes over code/config over comments over external docs when they conflict`

- [ ] **Step 3: Verify skill renders**

Run: `python -m pytest tests/test_brief_skeleton.py -q --tb=short`
Expected: PASS (skeleton tests are independent of SKILL.md prose; this guards against accidental structural breakage).

- [ ] **Step 4: Commit**

```bash
git add skills/repo-sensemaker/SKILL.md
git commit -m "feat(probes): SKILL.md probe engine rules and evidence hierarchy"
```

---

## Task 7: runtime prompt injection (`scripts/skill_executor.py`)

**Files:**
- Modify: `scripts/skill_executor.py:2331` (insert between the Input Context block and the Required Output block)

- [ ] **Step 1: Write the failing test**

Append to `tests/test_probe_prompt_injection.py`:

```python
def test_append_probe_section_guards_missing_file_and_readable_error(tmp_path: Path) -> None:
    parts: list[str] = ["pre"]
    broken = tmp_path / "report.yaml"
    broken.write_text("{not yaml", encoding="utf-8")  # path exists -> appended as-is
    append_probe_section(parts, broken)
    assert "Repository Probe Report" in "\n".join(parts)
```

(Guards against a future change that would silently skip existing-but-broken reports.)

- [ ] **Step 2: Implement the executor call site**

In `scripts/skill_executor.py`, directly after the Input Context block (after line 2329 `prompt_parts.append(f"\n### {input_name}")` / the `if resolved_inputs:` block closes), insert:

```python
        # Add pre-computed repository probes when the runtime supplied a report
        probe_report_path = context.get("probe_report_path")
        if probe_report_path:
            append_probe_section(
                prompt_parts,
                Path(probe_report_path) if Path(probe_report_path).is_absolute()
                else Path(self.repo_root) / probe_report_path,
            )
```

Add the import at the top of `scripts/skill_executor.py` (with the other local imports):

```python
from repo_probes import append_probe_section
```

If `repo_probes` is not resolvable from the executor's module context, add the same directory to `sys.path` before the import (mirror the existing pattern used for `_validator_utils` elsewhere in the file).

- [ ] **Step 3: Verify executor still imports and tests pass**

Run: `python -c "import scripts.skill_executor"` — Expected: no ImportError.
Run: `python -m pytest tests/test_probe_prompt_injection.py -q --tb=short` — Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add scripts/skill_executor.py tests/test_probe_prompt_injection.py
git commit -m "feat(probes): inject probe report into runtime prompt assembly"
```

---

## Task 8: documentation (README + CONTEXT.md)

**Files:**
- Modify: `README.md`
- Modify: `CONTEXT.md`

- [ ] **Step 1: README tooling section**

Insert under a new `## Tooling` heading (before the `## Tests` heading, or after the skills section if present):

```markdown
## Tooling

### Probe Engine

Deterministic repository probes for verified current state. `repo-sensemaker`
consumes the report it produces; you can also run it standalone on any repo:

```powershell
python scripts/probe-repo.py --repo-root <path> [--output probe-report.yaml]
```

The report (`probe-report.yaml`) contains git state, the verification-gap metric
`Vg` (declared vs CI-enforced checks, from README + `.github/workflows`), the
context-entropy metric `Ce` (untracked+ignored volume / tracked volume), test
collection stats, validator fixture coverage, and change churn. Validate a
report with `python scripts/validate-probe-report.py <report.yaml>`.
```

- [ ] **Step 2: CONTEXT.md vocabulary**

Add a `## Probe Engine` subsection near the glossary/vocabulary area of `CONTEXT.md`:

```markdown
## Probe Engine

- **probe-report**: machine-readable YAML produced by `scripts/probe-repo.py`
  capturing measured current state (git, CI enforcement, artifact volume, tests,
  fixtures, churn). Canonical input to `repo-sensemaker` state-currency
  verification; distinct from documented claims.
- **Vg (verification gap)**: `1 - |declared ∩ enforced| / |declared|` over
  verification entrypoints declared in README vs. steps executed in CI configs.
  `Vg > 0` is a Contract-Mismatch signal; `Vg == 1.0` means no declared check is
  enforced (or no CI exists).
- **Ce (context entropy)**: `(untracked + ignored-present volume) / tracked
  volume`. `Ce >= 5` is a hygiene/sprawl warning threshold.
- **fixtures-coverage**: share of `scripts/validate-*.py` validators that have
  `tests/fixtures/<name>/{valid,invalid}`; a gap is an Orphaned-Examples /
  Zero-Validation candidate.
```

- [ ] **Step 3: Verify no stale references**

Run: `python scripts/validate-repo.py`
Expected: exit 0 (repo-wide structural checks).

- [ ] **Step 4: Commit**

```bash
git add README.md CONTEXT.md
git commit -m "docs(probes): README tooling section and CONTEXT vocabulary"
```

---

## Full verification (final gate)

Before declaring completion:

- [ ] `python -m pytest tests -q --tb=short` — full suite green (242 existing + new probe tests).
- [ ] `python scripts/test-validators.py` — harness green (includes `validate-probe-report`).
- [ ] `python scripts/validate-repo.py` — repo structural checks green.
- [ ] `python scripts/probe-repo.py --repo-root . --no-write` — self-probe prints a sane summary on this repo (expected: `Vg` reflects this repo's own CI/README state; `Ce` modest; fixture coverage high).
- [ ] `git status --short` — only intended files changed.

## Self-review notes

- **Spec coverage:** Path 3 (Vg/Ce deterministic metrics) → Tasks 2–3; probe engine replacing derived evidence (Path 1 probe half) → Tasks 1, 4, 6, 7; Path 4 churn-as-scored-input (bounded) → Task 1; harness wiring → Task 5; docs → Task 8. Excluded paths (2, 5) plus legacy `repo_sensemaker.py` are called out in Out of scope with reasons.
- **Placeholder scan:** every code step carries complete code and exact expected output; no "add validation later" or "similar to Task N" patterns. The one conditional (import resolution of `repo_probes` inside `skill_executor.py`) specifies both branches explicitly.
- **Type consistency:** `probe_all` returns the same dict keys the CLI validator and SKILL.md consume (`schema_version`, `git_state`, `verification_gap.vg`, `context_entropy.ce`, `fixtures_coverage.{covered_validators,total_validators,coverage,missing_fixtures}`, `churn.{commits_scanned,changed_files_last_n,top_changed_files}`, `test_collection.{test_file_count,pytest_config_present,markers_declared}`); fixture YAML uses identical names; `append_probe_section(prompt_parts, path)` signature consistent between unit test, function, and executor call site.