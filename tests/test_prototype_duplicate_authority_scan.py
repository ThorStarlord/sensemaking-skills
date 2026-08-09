"""
Tests for scripts/prototype_duplicate_authority_scan.py.

PROTOTYPE (prototype/repo-sensemaker-vnext) -- this test file exercises a
prototype evidence-acquisition tool, not a canonical validator. It is not
referenced by validate-repo.py or any CI job.
"""

import importlib.util
import os
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

_spec = importlib.util.spec_from_file_location(
    "prototype_duplicate_authority_scan",
    os.path.join(SCRIPTS_DIR, "prototype_duplicate_authority_scan.py"),
)
scan = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(scan)


def _write(path, content="x"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _init_git_repo_with_files(tmp_path, files):
    """Create a real git repo at tmp_path, write and commit `files`
    (list of relative paths), and leave one extra UNTRACKED file so tests
    can prove tracked-vs-workspace filtering actually happens."""
    subprocess.run(["git", "init", "-q"], cwd=str(tmp_path), check=True)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=str(tmp_path), check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=str(tmp_path), check=True)
    for f in files:
        _write(str(tmp_path / f))
    subprocess.run(["git", "add", "-A"], cwd=str(tmp_path), check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=str(tmp_path), check=True)


def test_detects_same_suffix_under_two_different_top_level_prefixes(tmp_path):
    _write(str(tmp_path / "legacy" / "references" / "artifact-contracts.yaml"))
    _write(str(tmp_path / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"))

    candidates, _provenance = scan.find_duplicate_authority_candidates(str(tmp_path))

    assert "references/artifact-contracts.yaml" in candidates
    assert len(candidates["references/artifact-contracts.yaml"]) == 2


def test_does_not_flag_a_uniquely_named_file(tmp_path):
    _write(str(tmp_path / "skills" / "repo-sensemaker" / "references" / "evidence-rules.md"))

    candidates, _provenance = scan.find_duplicate_authority_candidates(str(tmp_path))

    assert candidates == {}


def test_does_not_flag_two_files_under_the_same_top_level_prefix(tmp_path):
    """Two sibling skills each legitimately having their own
    references/weakness-types.md-shaped file under the SAME top-level
    prefix ("skills") is not, by itself, evidence of duplicate authority --
    only a genuinely different top-level tree is."""
    _write(str(tmp_path / "skills" / "skill-a" / "references" / "notes.md"))
    _write(str(tmp_path / "skills" / "skill-b" / "references" / "notes.md"))

    candidates, _provenance = scan.find_duplicate_authority_candidates(str(tmp_path))

    assert candidates == {}


def test_excludes_dot_directories_and_common_noise(tmp_path):
    _write(str(tmp_path / ".git" / "references" / "artifact-contracts.yaml"))
    _write(str(tmp_path / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"))

    candidates, _provenance = scan.find_duplicate_authority_candidates(str(tmp_path))

    assert candidates == {}


def test_against_real_repo_finds_the_known_deprecated_pair():
    """Sanity check against the actual repository: the deliberately-kept,
    deprecated workflow-orchestrator/references/artifact-contracts.yaml
    (see PR #162) should still surface as a candidate against the canonical
    skills/workflow-planner/references/artifact-contracts.yaml -- proving
    this tool would have caught the original S1-diagnosed contract fork.
    """
    candidates, provenance = scan.find_duplicate_authority_candidates(REPO_ROOT)

    assert provenance == "git_tracked"
    assert "references/artifact-contracts.yaml" in candidates
    paths = candidates["references/artifact-contracts.yaml"]
    assert any(p.startswith("workflow-orchestrator/") for p in paths)
    assert any(p.startswith("skills/") for p in paths)


def test_main_runs_and_reports_candidates(tmp_path, capsys):
    _write(str(tmp_path / "legacy" / "references" / "x.md"))
    _write(str(tmp_path / "skills" / "y" / "references" / "x.md"))

    code = scan.main(["--repo-root", str(tmp_path)])
    out = capsys.readouterr().out

    assert code == 0
    assert "references/x.md" in out
    assert "filesystem walk" in out


def test_uses_git_tracked_files_when_repo_root_is_a_git_repo(tmp_path):
    """The P4-lesson fix: prefer `git ls-files` over a raw filesystem walk
    so workspace/untracked noise (the .venv-class problem) is excluded and
    the result's provenance is reported."""
    _init_git_repo_with_files(tmp_path, [
        "legacy/references/artifact-contracts.yaml",
        "skills/workflow-planner/references/artifact-contracts.yaml",
    ])
    # Untracked file that would ALSO collide on suffix if the scanner used
    # a raw filesystem walk instead of git ls-files.
    _write(str(tmp_path / "untracked_copy" / "references" / "artifact-contracts.yaml"))

    candidates, provenance = scan.find_duplicate_authority_candidates(str(tmp_path))

    assert provenance == "git_tracked"
    paths = candidates["references/artifact-contracts.yaml"]
    assert "untracked_copy/references/artifact-contracts.yaml" not in paths
    assert len(paths) == 2


def test_falls_back_to_filesystem_walk_outside_a_git_repo(tmp_path):
    """Not a git repo at all (no .git/) -- must not crash, must fall back,
    and must report the weaker provenance so a reader knows the results may
    include workspace-only files."""
    _write(str(tmp_path / "legacy" / "references" / "x.md"))
    _write(str(tmp_path / "skills" / "y" / "references" / "x.md"))

    candidates, provenance = scan.find_duplicate_authority_candidates(str(tmp_path))

    assert provenance == "filesystem_fallback"
    assert "references/x.md" in candidates
