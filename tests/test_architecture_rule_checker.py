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
                          "evidence_refs": ["file:src/lab/experiment.py"],
                          "attributes": {"owned_paths": ["src/lab/experiment.py"]}},
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
    assert "Python AST imports" in result["limits"][0]


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
             "authority_ref": "docs/arch.md", "evidence_refs": ["file:src/lab/experiment.py"],
             "attributes": {"owned_paths": ["src/lab/experiment.py"]} if version == 2 else {}},
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
    claims["component:lab"]["attributes"]["owned_paths"] = ["src/lab/__init__.py"]
    sources = {"src/core/engine.py": "from lab.deep.module import thing\n"}
    tracked = {"src/core/engine.py", "src/lab/__init__.py", "src/lab/deep/module.py"}
    result = check_rule_findings(claims, read_source=lambda p: sources.get(p, ""), tracked=tracked)
    assert [f["resolves_to"] for f in result["findings"]] == ["src/lab/deep/module.py"]

def test_relative_import_and_import_from_submodule_are_detected():
    claims = _claims()
    claims["component:lab"]["evidence_refs"] = ["file:src/pkg/lab/__init__.py"]
    claims["component:lab"]["attributes"]["owned_paths"] = ["src/pkg/lab/__init__.py"]
    claims["rule:core-no-lab"]["attributes"]["applies_to"] = ["src/pkg/core/**"]
    tracked = {"src/pkg/core/engine.py", "src/pkg/core/__init__.py",
               "src/pkg/lab/__init__.py", "src/pkg/lab/deep/module.py"}
    sources = {"src/pkg/core/engine.py": "from ..lab.deep import module\n"}
    found = check_rule_findings(claims, read_source=lambda p: sources.get(p, ""),
                                tracked=tracked)
    assert any(f["imports"] == "pkg.lab.deep.module" for f in found["findings"])


def test_parser_failure_is_reported_not_ignored():
    result = check_rule_findings(_claims(), read_source=lambda p: "def broken(:\n",
                                 tracked={"src/core/engine.py"})
    assert result["rule_assessments"][0]["assessment_status"] == "NOT_ASSESSED"
    assert any("syntax error" in note for note in result["not_assessed"])


def test_non_dependency_rules_have_explicit_assessment_records():
    claims = _claims()
    claims["rule:placement"] = {"kind": "architecture_rule", "attributes": {
        "rule_type": "placement", "severity": "warning", "applies_to": ["src/core/**"],
        "pattern": "src/core/[a-z]+\\.py"}}
    result = check_rule_findings(claims, read_source=lambda p: "pass\n",
                                 tracked={"src/core/engine.py"})
    item = next(r for r in result["rule_assessments"] if r["rule_id"] == "rule:placement")
    assert item["assessment_status"] == "NOT_ASSESSED"
    assert any("no executable checker" in s for s in item["not_assessed_reasons"])


def test_allowlist_flags_only_modeled_internal_components():
    claims = _claims()
    claims["component:core"]["attributes"] = {"owned_paths": ["src/core/engine.py"]}
    claims["component:lab"]["attributes"] = {"owned_paths": ["src/lab/experiment.py"]}
    claims["rule:core-no-lab"]["attributes"] = {
        "rule_type": "dependency_direction", "severity": "warning",
        "applies_to": ["src/core/**"], "allowed_targets": ["component:core"]
    }
    sources = {"src/core/engine.py": "import lab.experiment\n"}
    result = check_rule_findings(claims, read_source=lambda p: sources.get(p, ""),
                                 tracked={"src/core/engine.py", "src/lab/experiment.py"})
    assert len(result["findings"]) == 1
    assert "outside allowed_targets" in result["findings"][0]["note"]


def test_source_only_manifest_coverage_gap_is_explicit():
    claims = _claims()
    claims["component:lab"]["evidence_refs"] = ["file:src/lab/__init__.py"]
    claims["component:lab"]["attributes"]["owned_paths"] = ["src/lab/__init__.py"]
    files = {"release-v1.0.yaml": (
        "package_boundary:\n  source_only_modules:\n    - lab\n    - another_lab\n"
    ), "src/core/engine.py": "import lab\n"}
    tracked = set(files) | {"src/lab/__init__.py", "src/another_lab/__init__.py"}
    result = check_rule_findings(claims, read_source=lambda p: files.get(p, ""), tracked=tracked)
    assert any("every source-only package" in s for s in result["not_assessed"])

def test_evidence_only_target_is_unassessed_not_denylist_coverage():
    claims = _claims()
    claims["component:lab"]["attributes"].pop("owned_paths")
    result = check_rule_findings(claims, read_source=lambda p: "import lab.experiment\n",
                                 tracked={"src/core/engine.py", "src/lab/experiment.py"})
    assert result["findings_total"] == 0
    assert result["rule_assessments"][0]["assessment_status"] == "PARTIALLY_ASSESSED"
    assert any("no explicit owned_paths" in s for s in result["not_assessed"])
