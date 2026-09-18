from __future__ import annotations

import json
import subprocess
from pathlib import Path

import yaml
from click.testing import CliRunner

from sensemaking_skills.cli import cli
from sensemaking_skills.release_authority import audit_release_authority


def _fixture_repo(tmp_path: Path, *, source: str = "1.0.0rc3.dev0", target: str = "1.0.0rc3", status: str = "development") -> Path:
    root = tmp_path / "repo"
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / "docs").mkdir()
    (root / "pyproject.toml").write_text(
        f'[project]\nname = "sensemaking-skills"\nversion = "{source}"\n',
        encoding="utf-8",
    )
    (root / "release-v1.0.yaml").write_text(
        yaml.safe_dump({"release": {"version": target, "status": status}}, sort_keys=False),
        encoding="utf-8",
    )
    for relative in (
        "README.md",
        "STATUS.md",
        "docs/PUBLISHING.md",
        "docs/release-v1.0-contract.md",
    ):
        (root / relative).write_text(
            f"source {source}\ntarget {target}\n",
            encoding="utf-8",
        )
    (root / ".github" / "workflows" / "release-candidate.yml").write_text(
        """on:\n  push:\n    branches: [main]\nsource_version=\ntarget_version=\nrelease_status=\n"
        "github.event.pull_request.head.sha || github.sha\n""",
        encoding="utf-8",
    )
    subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "tests@example.com"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Sensemaking Tests"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-m", "fixture"], check=True, capture_output=True)
    return root


def test_release_authority_audit_accepts_relational_development_identity(tmp_path: Path) -> None:
    root = _fixture_repo(tmp_path)
    result = audit_release_authority(root)

    assert result.ok
    assert result.source_version == "1.0.0rc3.dev0"
    assert result.target_version == "1.0.0rc3"
    assert result.release_status == "development"
    assert result.git_head
    assert result.git_tree
    assert result.git_dirty is False
    assert result.qualification_established is False


def test_release_authority_audit_fails_closed_on_identity_mismatch(tmp_path: Path) -> None:
    root = _fixture_repo(tmp_path, source="1.0.0rc3", status="development")
    result = audit_release_authority(root)

    assert not result.ok
    assert any(item.code == "RELEASE_IDENTITY_RELATION_INVALID" for item in result.findings)


def test_release_audit_cli_exposes_claim_boundary() -> None:
    result = CliRunner().invoke(cli, ["release", "audit", "--repo-root", ".", "--json"])

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["ok"] is True
    assert payload["qualification_established"] is False
    assert payload["publication_established"] is False
    assert payload["semantic_truth_established"] is False
