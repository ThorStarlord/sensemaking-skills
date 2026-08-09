"""
Tests for scripts/prototype_duplicate_authority_scan.py.

PROTOTYPE (prototype/repo-sensemaker-vnext) -- this test file exercises a
prototype evidence-acquisition tool, not a canonical validator. It is not
referenced by validate-repo.py or any CI job.
"""

import importlib.util
import os
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


def test_detects_same_suffix_under_two_different_top_level_prefixes(tmp_path):
    _write(str(tmp_path / "legacy" / "references" / "artifact-contracts.yaml"))
    _write(str(tmp_path / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"))

    candidates = scan.find_duplicate_authority_candidates(str(tmp_path))

    assert "references/artifact-contracts.yaml" in candidates
    assert len(candidates["references/artifact-contracts.yaml"]) == 2


def test_does_not_flag_a_uniquely_named_file(tmp_path):
    _write(str(tmp_path / "skills" / "repo-sensemaker" / "references" / "evidence-rules.md"))

    candidates = scan.find_duplicate_authority_candidates(str(tmp_path))

    assert candidates == {}


def test_does_not_flag_two_files_under_the_same_top_level_prefix(tmp_path):
    """Two sibling skills each legitimately having their own
    references/weakness-types.md-shaped file under the SAME top-level
    prefix ("skills") is not, by itself, evidence of duplicate authority --
    only a genuinely different top-level tree is."""
    _write(str(tmp_path / "skills" / "skill-a" / "references" / "notes.md"))
    _write(str(tmp_path / "skills" / "skill-b" / "references" / "notes.md"))

    candidates = scan.find_duplicate_authority_candidates(str(tmp_path))

    assert candidates == {}


def test_excludes_dot_directories_and_common_noise(tmp_path):
    _write(str(tmp_path / ".git" / "references" / "artifact-contracts.yaml"))
    _write(str(tmp_path / "skills" / "workflow-planner" / "references" / "artifact-contracts.yaml"))

    candidates = scan.find_duplicate_authority_candidates(str(tmp_path))

    assert candidates == {}


def test_against_real_repo_finds_the_known_deprecated_pair():
    """Sanity check against the actual repository: the deliberately-kept,
    deprecated workflow-orchestrator/references/artifact-contracts.yaml
    (see PR #162) should still surface as a candidate against the canonical
    skills/workflow-planner/references/artifact-contracts.yaml -- proving
    this tool would have caught the original S1-diagnosed contract fork.
    """
    candidates = scan.find_duplicate_authority_candidates(REPO_ROOT)

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
