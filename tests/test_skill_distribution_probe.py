"""Unit tests for the distribution-drift probe (spike).

Covers the distribution_drift payload contract:
{ total_skills_checked, synchronized_count, line_ending_drift_count,
  content_drift_count, missing_installed_count,
  drifted_skills: [{ skill_name, repo_lines, installed_lines, hash_match, drift_type }] }
where drift_type is one of "none", "line_ending_only", "content_drift",
"missing_installed" ("none" items are counted, not listed). Also covers
sync_skills() and the CLI --sync flag.
"""

import importlib.util
import os
import sys
from pathlib import Path

from scripts.repo_probes import probe_skill_distribution, sync_skills

# Add scripts directory to sys.path so the CLI can import its sibling
# repo_probes module, then load it dynamically (scripts/ is not a package).
_scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)
_spec = importlib.util.spec_from_file_location(
    "probe_skill_distribution", os.path.join(_scripts_dir, "probe_skill_distribution.py")
)
_cli_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cli_module)
cli_main = _cli_module.main


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


def test_crlf_installed_matches_lf_repo_is_line_ending_only(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "skills" / "demo").mkdir(parents=True)
    (repo / "skills" / "demo" / "SKILL.md").write_bytes(b"# demo\nline two\n")
    installed = tmp_path / "installed"
    (installed / "demo").mkdir(parents=True)
    (installed / "demo" / "SKILL.md").write_bytes(b"# demo\r\nline two\r\n")
    payload = probe_skill_distribution(repo, installed)
    assert payload["total_skills_checked"] == 1
    assert payload["synchronized_count"] == 0
    assert payload["line_ending_drift_count"] == 1
    assert payload["content_drift_count"] == 0
    assert payload["missing_installed_count"] == 0
    entry = payload["drifted_skills"][0]
    assert entry["skill_name"] == "demo"
    assert entry["drift_type"] == "line_ending_only"
    assert entry["hash_match"] is False
    assert entry["repo_lines"] == 2
    assert entry["installed_lines"] == 2


def test_crlf_repo_matches_lf_installed_is_line_ending_only(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "skills" / "demo").mkdir(parents=True)
    (repo / "skills" / "demo" / "SKILL.md").write_bytes(b"# demo\r\nline two\r\n")
    installed = tmp_path / "installed"
    (installed / "demo").mkdir(parents=True)
    (installed / "demo" / "SKILL.md").write_bytes(b"# demo\nline two\n")
    payload = probe_skill_distribution(repo, installed)
    assert payload["drifted_skills"][0]["drift_type"] == "line_ending_only"
    assert payload["line_ending_drift_count"] == 1


def test_content_change_reports_content_drift_type(tmp_path: Path) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "# demo\nrepo version\n")
    payload = probe_skill_distribution(
        repo, _installed_with_skill(tmp_path, "demo", "# demo\ninstalled version\n")
    )
    assert payload["synchronized_count"] == 0
    assert payload["line_ending_drift_count"] == 0
    assert payload["content_drift_count"] == 1
    assert payload["missing_installed_count"] == 0
    assert payload["drifted_skills"][0]["drift_type"] == "content_drift"


def test_missing_installed_reports_missing_drift_type(tmp_path: Path) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "# demo\n")
    payload = probe_skill_distribution(repo, tmp_path / "installed")
    assert payload["content_drift_count"] == 0
    assert payload["line_ending_drift_count"] == 0
    assert payload["missing_installed_count"] == 1
    assert payload["drifted_skills"][0]["drift_type"] == "missing_installed"


def test_crlf_only_difference_does_not_change_normalized_equivalence(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "skills" / "demo").mkdir(parents=True)
    (repo / "skills" / "demo" / "SKILL.md").write_bytes(b"a\r\nb\r\nc\n")
    installed = tmp_path / "installed"
    (installed / "demo").mkdir(parents=True)
    (installed / "demo" / "SKILL.md").write_bytes(b"a\nb\nc\n")
    payload = probe_skill_distribution(repo, installed)
    assert payload["drifted_skills"][0]["drift_type"] == "line_ending_only"
    # Mixed CRLF + real content change must still be content_drift.
    (repo / "skills" / "demo" / "SKILL.md").write_bytes(b"a\r\nb\r\nc\r\n")
    (installed / "demo" / "SKILL.md").write_bytes(b"a\nb\nCHANGED\n")
    payload2 = probe_skill_distribution(repo, installed)
    assert payload2["drifted_skills"][0]["drift_type"] == "content_drift"


def test_sync_copies_missing_skill(tmp_path: Path) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "# demo\n")
    installed_root = tmp_path / "installed"
    summary = sync_skills(repo, installed_root)
    assert summary["synced_skill_count"] == 1
    assert summary["synced_skills"] == ["demo"]
    assert (installed_root / "demo" / "SKILL.md").read_text(encoding="utf-8") == "# demo\n"


def test_sync_overwrites_content_drift(tmp_path: Path) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "# demo\nrepo version\n")
    installed = _installed_with_skill(tmp_path, "demo", "# demo\ninstalled version\n")
    summary = sync_skills(repo, installed)
    assert summary["synced_skills"] == ["demo"]
    assert (installed / "demo" / "SKILL.md").read_text(encoding="utf-8") == "# demo\nrepo version\n"


def test_sync_skips_content_drift_when_overwrite_disabled(tmp_path: Path) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "# demo\nrepo version\n")
    installed = _installed_with_skill(tmp_path, "demo", "# demo\ninstalled version\n")
    summary = sync_skills(repo, installed, overwrite_content_drift=False)
    assert summary["synced_skills"] == []
    assert (installed / "demo" / "SKILL.md").read_text(encoding="utf-8") == "# demo\ninstalled version\n"


def test_sync_leaves_line_ending_only_drift_untouched(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "skills" / "demo").mkdir(parents=True)
    (repo / "skills" / "demo" / "SKILL.md").write_bytes(b"# demo\nline two\n")
    installed = tmp_path / "installed"
    (installed / "demo").mkdir(parents=True)
    (installed / "demo" / "SKILL.md").write_bytes(b"# demo\r\nline two\r\n")
    summary = sync_skills(repo, installed)
    assert summary["synced_skills"] == []
    assert (installed / "demo" / "SKILL.md").read_bytes() == b"# demo\r\nline two\r\n"


def test_sync_defaults_to_home_agents_skills(tmp_path: Path, monkeypatch) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "# demo\n")
    home = tmp_path / "home"
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    summary = sync_skills(repo)
    assert summary["synced_skills"] == ["demo"]
    assert (home / ".agents" / "skills" / "demo" / "SKILL.md").is_file()


def test_cli_sync_flag_syncs_and_reports(tmp_path: Path, capsys) -> None:
    repo = _repo_with_skill(tmp_path, "demo", "# demo\nrepo version\n")
    installed = tmp_path / "installed"
    (installed / "demo").mkdir(parents=True)
    (installed / "demo" / "SKILL.md").write_text("# demo\ninstalled version\n", encoding="utf-8")
    code = cli_main(
        [
            "--repo-root",
            str(repo),
            "--installed-dir",
            str(installed),
            "--sync",
            "--no-write",
        ]
    )
    assert code == 0
    assert (installed / "demo" / "SKILL.md").read_text(encoding="utf-8") == "# demo\nrepo version\n"
    out = capsys.readouterr().out
    assert "SYNC SUMMARY" in out
    assert "demo" in out
    assert "content drift: 0" in out
    assert "missing: 0" in out
