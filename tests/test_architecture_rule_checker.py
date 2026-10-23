"""Warning-only dependency-rule checker and its CLI (ADR 0033, Phase 3)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from sensemaking_skills.semantic_architecture.knowledge_architecture import (
    _module_file, check_rule_findings,
)

ROOT = Path(__file__).resolve().parents[1]


def _claims():
    return {
        "component:core": {"id": "component:core", "kind": "component", "statement": "core",
                           "evidence_refs": ["file:src/core/engine.py"], "attributes": {}},
        "component:lab": {"id": "component:lab", "kind": "component", "statement": "lab",
                          "evidence_refs": ["file:src/lab/experiment.py"], "attributes": {}},
        "rule:core-no-lab": {"id": "rule:core-no-lab", "kind": "architecture_rule",
                             "statement": "Core must not import lab.", "evidence_refs": ["file:src/core/engine.py"],
                             "attributes": {"rule_type": "dependency_direction", "severity": "error",
                                            "applies_to": ["src/core/**"], "forbidden_targets": ["component:lab"]}},
    }


def test_module_resolution_prefers_src_and_packages():
    tracked = {"src/core/engine.py", "src/lab/__init__.py"}
    assert _module_file("core.engine", tracked) == "src/core/engine.py"
    assert _module_file("lab", tracked) == "src/lab/__init__.py"
    assert _module_file("os.path", tracked) is None


def test_forbidden_import_is_reported_as_warning_only_finding():
    sources = {"src/core/engine.py": "import lab.experiment\nfrom core import util\n"}
    tracked = {"src/core/engine.py", "src/lab/experiment.py", "src/core/util.py"}
    result = check_rule_findings(_claims(), read_source=lambda p: sources.get(p, ""), tracked=tracked)
    assert result["warning_only"] is True
    assert [f["rule_id"] for f in result["findings"]] == ["rule:core-no-lab"]
    finding = result["findings"][0]
    assert finding["imports"] == "lab.experiment"
    assert finding["resolves_to"] == "src/lab/experiment.py"
    assert "import syntax only" in result["limits"][0]


def test_clean_scope_produces_no_findings():
    sources = {"src/core/engine.py": "from core import util\n"}
    tracked = {"src/core/engine.py", "src/lab/experiment.py", "src/core/util.py"}
    result = check_rule_findings(_claims(), read_source=lambda p: sources.get(p, ""), tracked=tracked)
    assert result["findings"] == []
    assert result["findings_total"] == 0


def test_rule_with_no_matching_python_files_is_not_assessed():
    result = check_rule_findings(_claims(), read_source=lambda p: "", tracked={"docs/readme.md"})
    assert any("no tracked Python file matches" in note for note in result["not_assessed"])


def test_syntax_errors_and_unknown_targets_are_surfaced_not_crashing():
    claims = _claims()
    claims["rule:core-no-lab"]["attributes"]["forbidden_targets"] = ["component:ghost"]
    result = check_rule_findings(claims, read_source=lambda p: "def broken(:\n",
                                 tracked={"src/core/engine.py"})
    assert any("component:ghost is not a claim" in note for note in result["not_assessed"])
    assert result["findings"] == []


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True,
                   env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


def _committed_repo(tmp_path: Path, files: dict[str, str]) -> tuple[Path, str]:
    _git(tmp_path, "init", "-q")
    for rel, text in files.items():
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "fixture")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True, text=True,
                          check=True).stdout.strip()
    return tmp_path, head


def _authored(version: int) -> str:
    return json.dumps({
        "schema_version": version,
        "claims": [
            {"id": "component:core", "kind": "component", "statement": "Core engine.",
             "epistemic_status": "declared", "authority_kind": "document",
             "authority_ref": "docs/arch.md", "evidence_refs": ["file:src/core/engine.py"]},
            {"id": "component:lab", "kind": "component", "statement": "Lab package.",
             "epistemic_status": "declared", "authority_kind": "document",
             "authority_ref": "docs/arch.md", "evidence_refs": ["file:src/lab/experiment.py"]},
            {"id": "rule:core-no-lab", "kind": "architecture_rule", "statement": "Core must not import lab.",
             "epistemic_status": "declared", "authority_kind": "document",
             "authority_ref": "docs/arch.md", "evidence_refs": ["file:docs/arch.md"],
             "attributes": {"rule_type": "dependency_direction", "severity": "error",
                            "applies_to": ["src/core/**"], "forbidden_targets": ["component:lab"]}},
        ],
        "relations": [],
    }, indent=2)


def _cli(repo: Path, head: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    return subprocess.run(
        [sys.executable, "-m", "sensemaking_skills.cli", "semantic", "knowledge-check-rules",
         "--repo", str(repo), "--target-ref", head, "--json"],
        capture_output=True, text=True, cwd=ROOT, env=env, check=False,
    )


def test_cli_reports_committed_violation_and_never_fails(tmp_path):
    repo, head = _committed_repo(tmp_path, {
        ".sensemaking/knowledge/arch.json": _authored(2),
        "docs/arch.md": "# Architecture\n",
        "src/core/engine.py": "import lab.experiment\n",
        "src/lab/experiment.py": "X = 1\n",
    })
    result = _cli(repo, head)
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["warning_only"] is True
    assert payload["findings"][0]["rule_id"] == "rule:core-no-lab"
    assert payload["action_authorized"] is False
    assert payload["semantic_truth_established"] is False


def test_cli_refuses_dirty_worktree(tmp_path):
    repo, head = _committed_repo(tmp_path, {
        ".sensemaking/knowledge/arch.json": _authored(2),
        "docs/arch.md": "# Architecture\n",
        "src/core/engine.py": "X = 1\n",
        "src/lab/experiment.py": "X = 1\n",
    })
    (repo / "scratch.txt").write_text("uncommitted\n", encoding="utf-8")
    result = _cli(repo, head)
    assert result.returncode != 0
    assert "dirty or untracked" in result.stderr


def test_cli_rejects_version_two_constructs_in_version_one_document(tmp_path):
    repo, head = _committed_repo(tmp_path, {
        ".sensemaking/knowledge/arch.json": _authored(1),
        "docs/arch.md": "# Architecture\n",
        "src/core/engine.py": "X = 1\n",
        "src/lab/experiment.py": "X = 1\n",
    })
    result = _cli(repo, head)
    assert result.returncode != 0
    assert "requires schema_version 2" in result.stderr


def test_package_init_claim_covers_the_whole_package():
    claims = _claims()
    claims["component:lab"]["evidence_refs"] = ["file:src/lab/__init__.py"]
    sources = {"src/core/engine.py": "from lab.deep.module import thing\n"}
    tracked = {"src/core/engine.py", "src/lab/__init__.py", "src/lab/deep/module.py"}
    result = check_rule_findings(claims, read_source=lambda p: sources.get(p, ""), tracked=tracked)
    assert [f["resolves_to"] for f in result["findings"]] == ["src/lab/deep/module.py"]
