import subprocess
from pathlib import Path

from scripts.repo_probes import churn, ci_enforcement, git_state

def _new_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"], check=True)
    return repo


def _commit(repo: Path, message: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), "-c", "commit.gpgsign=false", "commit", "-q", "-m", message],
        check=True,
    )


def _init_committed_repo(tmp_path: Path) -> Path:
    repo = _new_repo(tmp_path)
    (repo / "file.txt").write_text("one", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    _commit(repo, "initial")
    (repo / "file.txt").write_text("two", encoding="utf-8")
    (repo / "untracked.txt").write_text("u", encoding="utf-8")
    return repo


def test_git_state_reports_verified_current_state(tmp_path: Path) -> None:
    repo = _init_committed_repo(tmp_path)
    (repo / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
    (repo / "ignored.txt").write_text("ignored", encoding="utf-8")
    state = git_state(repo)
    assert state["is_git_repo"] is True
    assert state["branch"] == "main"
    assert state["head_message"] == "initial"
    assert state["tracked_file_count"] == 1
    assert state["untracked_file_count"] == 2
    assert state["dirty_file_count"] == 1
    assert state["ignored_present_entry_count"] == 1
    assert len(state["head_sha"]) >= 7


def test_git_state_reports_non_git_directory(tmp_path: Path) -> None:
    state = git_state(tmp_path)
    assert state["is_git_repo"] is False
    assert state["tracked_file_count"] == 0


def test_git_state_empty_repo(tmp_path: Path) -> None:
    repo = _new_repo(tmp_path)
    state = git_state(repo)
    assert state["is_git_repo"] is True
    assert state["tracked_file_count"] == 0


def test_git_state_detached_head(tmp_path: Path) -> None:
    repo = _new_repo(tmp_path)
    (repo / "file.txt").write_text("one", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    _commit(repo, "initial")
    subprocess.run(["git", "-C", str(repo), "checkout", "--detach", "-q"], check=True)
    state = git_state(repo)
    assert state["is_git_repo"] is True
    assert state["branch"] is None


def test_churn_reports_top_changed_files(tmp_path: Path) -> None:
    repo = _init_committed_repo(tmp_path)
    report = churn(repo, commits=10)
    assert report["commits_scanned"] == 1
    assert report["top_changed_files"] == ["file.txt"]


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


def test_verification_gap_zero_with_block_scalar_run(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / "README.md").write_text(
        "Runs `python scripts/check.py` in CI.\n",
        encoding="utf-8",
    )
    (repo / ".github" / "workflows" / "validation.yml").write_text(
        "jobs:\n  test:\n    steps:\n      - run: |\n          python scripts/check.py\n"
        "          pytest -q\n",
        encoding="utf-8",
    )
    report = ci_enforcement(repo)
    assert report["declared_in_ci"] == ["scripts/check.py"]
    assert report["vg"] == 0.0


def test_verification_gap_detects_gitlab_ci_unenforced(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("Runs `python scripts/check.py` in CI.\n", encoding="utf-8")
    (repo / ".gitlab-ci.yml").write_text(
        "test:\n  script:\n    - run: python scripts/other.py\n",
        encoding="utf-8",
    )
    report = ci_enforcement(repo)
    assert report["enforced_checks"] == ["scripts/other.py"]
    assert report["declared_in_ci"] == []
    assert report["vg"] == 1.0


def test_verification_gap_gitlab_script_key_not_scanned(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("Runs `python scripts/check.py` in CI.\n", encoding="utf-8")
    (repo / ".gitlab-ci.yml").write_text(
        "test:\n  script:\n    - python scripts/other.py\n",
        encoding="utf-8",
    )
    report = ci_enforcement(repo)
    assert report["enforced_checks"] == []
    assert report["vg"] == 1.0


def test_verification_gap_zero_with_chomped_block_scalar(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / "README.md").write_text(
        "Runs `python scripts/check.py` in CI.\n",
        encoding="utf-8",
    )
    (repo / ".github" / "workflows" / "validation.yml").write_text(
        "jobs:\n  test:\n    steps:\n      - run: |-\n          python scripts/check.py\n",
        encoding="utf-8",
    )
    report = ci_enforcement(repo)
    assert report["declared_in_ci"] == ["scripts/check.py"]
    assert report["vg"] == 0.0


def test_verification_gap_block_scalar_with_blank_line_continues(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / "README.md").write_text(
        "Runs `python scripts/check.py` and `python scripts/lint.py` in CI.\n",
        encoding="utf-8",
    )
    (repo / ".github" / "workflows" / "validation.yml").write_text(
        "jobs:\n  test:\n    steps:\n      - run: |\n          python scripts/check.py\n"
        "\n          python scripts/lint.py\n",
        encoding="utf-8",
    )
    report = ci_enforcement(repo)
    assert report["declared_in_ci"] == ["scripts/check.py", "scripts/lint.py"]
    assert report["enforced_checks"] == ["scripts/check.py", "scripts/lint.py"]
    assert report["vg"] == 0.0


from scripts.repo_probes import context_entropy, fixtures_coverage
from scripts.repo_probes import test_collection as probe_test_collection


def test_context_entropy_uses_tracked_volume_as_denominator(tmp_path: Path) -> None:
    repo = _init_committed_repo(tmp_path)  # 1 tracked, 1 untracked, 1 dirty
    report = context_entropy(repo)
    assert report["tracked_volume"] == 1
    assert report["untracked_volume"] == 1
    assert report["ce"] == 1.0


def test_context_entropy_zero_for_empty_directory(tmp_path: Path) -> None:
    report = context_entropy(tmp_path)
    assert report["ce"] == 0.0


def test_context_entropy_unmeasured_when_ignored_status_times_out(
    tmp_path: Path, monkeypatch
) -> None:
    # Issue #173 / evidence-rules Rule 9: a timed-out git status --ignored
    # must read as unmeasured (ce None), never a false clean 0.0.
    repo = _init_committed_repo(tmp_path)
    real_run = subprocess.run

    def fake_run(cmd, *args, **kwargs):
        if "--ignored" in cmd:
            raise subprocess.TimeoutExpired(cmd=cmd, timeout=30)
        return real_run(cmd, *args, **kwargs)

    monkeypatch.setattr("scripts.repo_probes.subprocess.run", fake_run)
    report = context_entropy(repo)
    assert report["ce"] is None
    assert "unmeasured" in report["notes"]
    assert report["ignored_present_volume"] == 0


def test_test_collection_counts_test_files_only(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "tests").mkdir(parents=True)
    (repo / "tests" / "test_one.py").write_text("", encoding="utf-8")
    (repo / "tests" / "test_two.py").write_text("", encoding="utf-8")
    (repo / "tests" / "test_data.csv").write_text("a,b\n", encoding="utf-8")
    (repo / ".venv" / "test_x.py").mkdir(parents=True)
    (repo / ".venv" / "test_x.py" / "test_x.py").write_text("", encoding="utf-8")
    (repo / "src.py").write_text("", encoding="utf-8")
    (repo / "pyproject.toml").write_text("[tool.pytest.ini_options]\naddopts = \"-q\"\n", encoding="utf-8")
    report = probe_test_collection(repo)
    assert report["test_file_count"] == 2
    assert report["pytest_config_present"] is True
    assert report["markers_declared"] == ""
    # Best-effort collect count: key always present; value int or None.
    assert "test_case_count" in report
    assert report["test_case_count"] is None or isinstance(report["test_case_count"], int)


def test_test_collection_reports_collected_case_count_when_pytest_available(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "tests").mkdir(parents=True)
    (repo / "tests" / "test_one.py").write_text(
        "def test_a():\n    pass\ndef test_b():\n    pass\n", encoding="utf-8"
    )
    report = probe_test_collection(repo)
    assert report["test_file_count"] == 1
    # pytest may be unavailable in minimal environments; when present the
    # count must be a positive integer matching the two collected tests.
    if report["test_case_count"] is not None:
        assert report["test_case_count"] == 2


def test_fixtures_coverage_reports_missing_fixture_dirs(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    (repo / "scripts" / "validate-demo.py").write_text("pass\n", encoding="utf-8")
    # No tests/fixtures/validate-demo directory at all.
    report = fixtures_coverage(repo)
    assert report["total_validators"] == 1
    assert report["covered_validators"] == 0
    assert report["missing_fixtures"] == ["validate-demo"]


def test_fixtures_coverage_reports_covered_and_partial(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    (repo / "scripts" / "validate-a.py").write_text("pass\n", encoding="utf-8")
    (repo / "scripts" / "validate-b.py").write_text("pass\n", encoding="utf-8")
    (repo / "tests" / "fixtures" / "validate-a" / "valid").mkdir(parents=True)
    (repo / "tests" / "fixtures" / "validate-a" / "invalid").mkdir(parents=True)
    (repo / "tests" / "fixtures" / "validate-b" / "valid").mkdir(parents=True)
    report = fixtures_coverage(repo)
    assert report["total_validators"] == 2
    assert report["covered_validators"] == 1
    assert report["missing_fixtures"] == ["validate-b"]
    assert report["coverage"] == 0.5
    assert report["valid_only"] == []


def test_fixtures_coverage_honors_documented_valid_only_convention(tmp_path: Path) -> None:
    # Issue #173: repo-wide validators cannot have a portable unsatisfiable
    # invalid/ fixture; a documented valid-only convention must be honored.
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    (repo / "scripts" / "validate-repo.py").write_text("pass\n", encoding="utf-8")
    (repo / "tests" / "fixtures" / "validate-repo" / "valid").mkdir(parents=True)
    (repo / "tests" / "fixtures" / "valid-only.txt").write_text(
        "# Repo-wide validators have no portable negative fixture\nvalidate-repo\n",
        encoding="utf-8",
    )
    report = fixtures_coverage(repo)
    assert report["total_validators"] == 1
    assert report["covered_validators"] == 1
    assert report["missing_fixtures"] == []
    assert report["coverage"] == 1.0
    assert report["valid_only"] == ["validate-repo"]


def test_fixtures_coverage_valid_only_marker_does_not_exempt_missing_valid(tmp_path: Path) -> None:
    # A validator listed as valid-only still needs its valid/ dir.
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    (repo / "scripts" / "validate-x.py").write_text("pass\n", encoding="utf-8")
    (repo / "tests" / "fixtures").mkdir(parents=True)
    (repo / "tests" / "fixtures" / "valid-only.txt").write_text("validate-x\n", encoding="utf-8")
    report = fixtures_coverage(repo)
    assert report["covered_validators"] == 0
    assert report["missing_fixtures"] == ["validate-x"]


from scripts.repo_probes import vendored_skill_drift


def _canonical_skill(root: Path, name: str, rules_text: str = "rules v1\n") -> None:
    skill = root / "skills" / name
    (skill / "references").mkdir(parents=True)
    (skill / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")
    (skill / "references" / "evidence-rules.md").write_text(rules_text, encoding="utf-8")


def test_vendored_skill_drift_no_finding_when_in_sync(tmp_path: Path) -> None:
    # Issue #170: a target whose vendored copy matches canonical is clean.
    canonical = tmp_path / "canonical"
    _canonical_skill(canonical, "repo-sensemaker")
    repo = tmp_path / "repo"
    _canonical_skill(repo, "repo-sensemaker")
    report = vendored_skill_drift(repo, canonical_skills_root=canonical / "skills")
    assert report["checked"] == ["repo-sensemaker"]
    assert report["drifted"] == []
    assert report["findings"] == []


def test_vendored_skill_drift_flags_stale_evidence_rules(tmp_path: Path) -> None:
    # The exact auteur failure: vendored evidence-rules.md predates the
    # canonical learnings (Rules 6-12), so the executor never sees them.
    canonical = tmp_path / "canonical"
    _canonical_skill(canonical, "repo-sensemaker", rules_text="rules v2 (Rules 6-12)\n")
    repo = tmp_path / "repo"
    _canonical_skill(repo, "repo-sensemaker", rules_text="rules v1 (Rules 1-5)\n")
    report = vendored_skill_drift(repo, canonical_skills_root=canonical / "skills")
    assert len(report["findings"]) == 1
    f = report["findings"][0]
    assert f["finding_type"] == "skill_distribution_drift"
    assert f["requires_semantic_review"] is False
    assert {"skills/repo-sensemaker/references/evidence-rules.md"} == {
        o["source"] for o in f["observations"]
    }


def test_vendored_skill_drift_flags_missing_evidence_rules(tmp_path: Path) -> None:
    # A vendored skill dir that is missing a compare file (evidence-rules.md)
    # is drift: the executor has no rules at all. A target with NO vendored
    # skill dir is simply not using that skill and is not flagged.
    canonical = tmp_path / "canonical"
    _canonical_skill(canonical, "repo-sensemaker")
    repo = tmp_path / "repo"
    _canonical_skill(repo, "repo-sensemaker")
    (repo / "skills" / "repo-sensemaker" / "references" / "evidence-rules.md").unlink()
    report = vendored_skill_drift(repo, canonical_skills_root=canonical / "skills")
    assert len(report["findings"]) == 1
    assert report["drifted"][0]["skill_name"] == "repo-sensemaker"
    assert report["drifted"][0]["files"][0]["drift_type"] == "missing"


def test_vendored_skill_drift_ignores_skills_not_vendored(tmp_path: Path) -> None:
    # Target with no skills/ at all: not using the framework's skills, so
    # there is nothing to drift -- clean, not a finding.
    canonical = tmp_path / "canonical"
    _canonical_skill(canonical, "repo-sensemaker")
    repo = tmp_path / "repo"
    repo.mkdir()
    report = vendored_skill_drift(repo, canonical_skills_root=canonical / "skills")
    assert report["checked"] == []
    assert report["findings"] == []


def test_vendored_skill_drift_unavailable_canonical_is_clean(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    report = vendored_skill_drift(repo, canonical_skills_root=tmp_path / "nope")
    assert report["findings"] == []
    assert report["checked"] == []
    assert "unavailable" in report["notes"]
