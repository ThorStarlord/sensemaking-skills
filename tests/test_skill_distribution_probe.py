"""Unit tests for the distribution-drift probe (spike).

Covers the distribution_drift payload contract:
{ total_skills_checked, synchronized_count, drifted_skills: [{ skill_name, repo_lines, installed_lines, hash_match }] }
"""

from pathlib import Path

from scripts.repo_probes import probe_skill_distribution


def _repo_with_skill(tmp_path: Path, name: str, content: str) -> Path:
    repo = tmp_path / "repo"
    (repo / "skills" / name).mkdir(parents=True)
    (repo / "skills" / name / "SKILL.md").write_text(content, encoding="utf-8")
    return repo


def _installed_with_skill(tmp_path: Path, name: str, content: str) -> Path:
    root = tmp_path / "installed"
    (root / name).mkdir(parents=True)
    (root / name / "SKILL.md").write_text(content, encoding="utf-8")
    return root


def test_identical_skills_are_synchronized(tmp_path: Path) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "# demo\nline two\n")
    payload = probe_skill_distribution(repo, _installed_with_skill(tmp_path, "demo", "# demo\nline two\n"))
    assert payload["total_skills_checked"] == 1
    assert payload["synchronized_count"] == 1
    assert payload["drifted_skills"] == []


def test_content_change_is_drift(tmp_path: Path) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "# demo\nrepo version\n")
    payload = probe_skill_distribution(repo, _installed_with_skill(tmp_path, "demo", "# demo\ninstalled version\n"))
    assert payload["synchronized_count"] == 0
    assert len(payload["drifted_skills"]) == 1
    entry = payload["drifted_skills"][0]
    assert entry["skill_name"] == "demo"
    assert entry["repo_lines"] == 2
    assert entry["installed_lines"] == 2
    assert entry["hash_match"] is False


def test_missing_installed_skill_counts_as_drift(tmp_path: Path) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "# demo\n")
    payload = probe_skill_distribution(repo, tmp_path / "installed")
    assert payload["total_skills_checked"] == 1
    assert payload["synchronized_count"] == 0
    entry = payload["drifted_skills"][0]
    assert entry["skill_name"] == "demo"
    assert entry["installed_lines"] is None
    assert entry["hash_match"] is False


def test_differing_line_counts_reported(tmp_path: Path) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "a\nb\nc\n")
    payload = probe_skill_distribution(repo, _installed_with_skill(tmp_path, "demo", "a\nb\n"))
    entry = payload["drifted_skills"][0]
    assert entry["repo_lines"] == 3
    assert entry["installed_lines"] == 2


def test_default_installed_root_is_home_agents_skills(tmp_path: Path, monkeypatch) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "# demo\n")
    home = tmp_path / "home"
    (home / ".agents" / "skills" / "demo").mkdir(parents=True)
    (home / ".agents" / "skills" / "demo" / "SKILL.md").write_text("# demo\n", encoding="utf-8")
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    payload = probe_skill_distribution(repo)
    assert payload["total_skills_checked"] == 1
    assert payload["synchronized_count"] == 1


def test_non_skill_markdown_files_ignored(tmp_path: Path) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "# demo\n")
    (repo / "skills" / "demo" / "README.md").write_text("readme content\n", encoding="utf-8")
    payload = probe_skill_distribution(repo, _installed_with_skill(tmp_path, "demo", "# demo\n"))
    assert payload["total_skills_checked"] == 1
    assert payload["synchronized_count"] == 1


def test_empty_skills_dir_yields_zero_payload(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "skills").mkdir(parents=True)
    payload = probe_skill_distribution(repo, _installed_with_skill(tmp_path, "unrelated", "x\n"))
    assert payload["total_skills_checked"] == 0
    assert payload["synchronized_count"] == 0
    assert payload["drifted_skills"] == []


def test_multiple_skills_mixed_sync_and_drift(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    for name, content in (("alpha", "a\n"), ("beta", "b\n")):
        (repo / "skills" / name).mkdir(parents=True)
        (repo / "skills" / name / "SKILL.md").write_text(content, encoding="utf-8")
    installed = _installed_with_skill(tmp_path, "alpha", "a\n")
    (installed / "beta").mkdir()
    (installed / "beta" / "SKILL.md").write_text("B changed\n", encoding="utf-8")
    payload = probe_skill_distribution(repo, installed)
    assert payload["total_skills_checked"] == 2
    assert payload["synchronized_count"] == 1
    assert [entry["skill_name"] for entry in payload["drifted_skills"]] == ["beta"]
