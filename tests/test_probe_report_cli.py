import subprocess
import sys
from pathlib import Path

import yaml

PROBE_SCRIPT = str(Path(__file__).resolve().parents[1] / "scripts" / "probe-repo.py")


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
        [sys.executable, PROBE_SCRIPT, "--repo-root", str(repo), "--output", str(out)],
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