"""Fresh-installed-wheel proof for P10 coding-agent harness adapters."""

from __future__ import annotations

import subprocess
import sys
import venv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def _venv_python(venv_dir: Path) -> Path:
    return venv_dir / (
        "Scripts/python.exe" if sys.platform.startswith("win") else "bin/python"
    )


def _venv_script(venv_dir: Path, name: str) -> Path:
    return (
        venv_dir
        / ("Scripts" if sys.platform.startswith("win") else "bin")
        / name
    )


def _build_and_install_wheel(tmp_path: Path) -> tuple[Path, Path]:
    wheel_dir = tmp_path / "wheel"
    venv_dir = tmp_path / "venv"

    build = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            str(REPO_ROOT),
            "--no-deps",
            "--wheel-dir",
            str(wheel_dir),
        ],
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    wheels = list(wheel_dir.glob("*.whl"))
    assert len(wheels) == 1, wheels

    venv.create(venv_dir, with_pip=True)
    install = subprocess.run(
        [str(_venv_python(venv_dir)), "-m", "pip", "install", str(wheels[0])],
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert install.returncode == 0, install.stdout + install.stderr
    return wheels[0], venv_dir


def _run(cli: str, work_dir: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [cli, *args],
        capture_output=True,
        text=True,
        timeout=180,
        cwd=str(work_dir),
    )


def test_installed_wheel_exposes_explicit_p10_harness_adapters(tmp_path: Path):
    _wheel, venv_dir = _build_and_install_wheel(tmp_path)
    work_dir = tmp_path / "outside-source-checkout"
    work_dir.mkdir()
    cli = str(_venv_script(venv_dir, "sensemaking-skills"))

    help_run = _run(cli, work_dir, "setup-skills", "--help")
    assert help_run.returncode == 0, help_run.stdout + help_run.stderr
    for token in (
        "generic",
        "claude",
        "codex",
        "opencode",
        "claude-superpowers",
        "--scope",
        "--project-root",
    ):
        assert token in help_run.stdout

    cases = {
        "claude": Path(".claude/skills"),
        "codex": Path(".agents/skills"),
        "opencode": Path(".opencode/skills"),
    }
    for target, relative_root in cases.items():
        project = work_dir / f"{target}-project"
        project.mkdir()
        result = _run(
            cli,
            work_dir,
            "setup-skills",
            "--target",
            target,
            "--scope",
            "project",
            "--project-root",
            str(project),
        )
        assert result.returncode == 0, result.stdout + result.stderr
        assert f"Requested adapter target: {target}" in result.stdout
        assert "Requested scope: project" in result.stdout

        installed = relative_root / "repo-sensemaker" / "SKILL.md"
        installed_path = project / installed
        assert installed_path.is_file(), installed_path
        assert installed_path.read_bytes() == (
            REPO_ROOT / "skills" / "repo-sensemaker" / "SKILL.md"
        ).read_bytes()

        # A harness adapter is setup metadata only; installation must not create
        # Campaign state or pretend that any Skill was selected/executed.
        assert not (project / "campaign-state.yaml").exists()
        lowered = result.stdout.lower()
        assert "selected skill" not in lowered
        assert "execution authorized" not in lowered

    all_project = work_dir / "all-project"
    all_project.mkdir()
    all_result = _run(
        cli,
        work_dir,
        "setup-skills",
        "--target",
        "all",
        "--scope",
        "project",
        "--project-root",
        str(all_project),
    )
    assert all_result.returncode == 0, all_result.stdout + all_result.stderr
    assert "Target locations: 3" in all_result.stdout
    for relative_root in (
        Path(".agents/skills"),
        Path(".claude/skills"),
        Path(".opencode/skills"),
    ):
        assert (relative_root if relative_root.is_absolute() else all_project / relative_root)
        assert (all_project / relative_root / "using-sensemaking" / "SKILL.md").is_file()

    # Existing fail-closed drift behavior applies equally to a P10 harness root.
    claude_project = work_dir / "claude-project"
    installed = claude_project / ".claude" / "skills" / "repo-sensemaker" / "SKILL.md"
    canonical = installed.read_bytes()
    installed.write_bytes(b"# divergent installed copy\n")

    rejected = _run(
        cli,
        work_dir,
        "setup-skills",
        "--target",
        "claude",
        "--scope",
        "project",
        "--project-root",
        str(claude_project),
    )
    assert rejected.returncode != 0
    assert "Different from packaged version" in rejected.stdout
    assert installed.read_bytes() == b"# divergent installed copy\n"

    forced = _run(
        cli,
        work_dir,
        "setup-skills",
        "--target",
        "claude",
        "--scope",
        "project",
        "--project-root",
        str(claude_project),
        "--force",
    )
    assert forced.returncode == 0, forced.stdout + forced.stderr
    assert installed.read_bytes() == canonical
