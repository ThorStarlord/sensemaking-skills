"""Installed-wheel distribution regression test (Task P1-F).

Task P1-R (CONFIRMED) proved the shipped 0.2.1 wheel could not deliver or
invoke the canonical repo-sensemaker skill: the artifact contained no
SKILL.md trees and its CLI did not expose ``setup-skills``.

This test asserts the repair holds on the ARTIFACT, not merely on source:

    build wheel
        -> fresh venv
        -> pip install wheel
        -> sensemaking-skills setup-skills --target custom <tmp dest>
        -> verify installed repo-sensemaker/SKILL.md exists
        -> verify installed canonical files match the release source
        -> verify the CLI exposes setup-skills

It also verifies drift behavior: an existing divergent copy is reported and
NOT silently overwritten; only explicit ``--force`` replaces it.

Like tests/campaign_validation/test_installed_wheel_smoke.py, this is slow
(builds a wheel + venv) and runs as part of the dedicated CI
"Phase 2 installed-wheel smoke test" job.
"""

from __future__ import annotations

import json
import subprocess
import sys
import venv
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

CANONICAL_SKILL = "skills/repo-sensemaker/SKILL.md"
CANONICAL_REFERENCES = [
    "skills/repo-sensemaker/references/evidence-rules.md",
    "skills/repo-sensemaker/references/repo-analysis-template.md",
    "skills/repo-sensemaker/references/weakness-types.md",
]
PACKAGED_SKILL = "sensemaking_skills/skill_trees/repo-sensemaker/SKILL.md"
PACKAGED_CAPABILITY_CATALOG = "sensemaking_skills/defaults/capability-registry.yaml"


def _venv_python(venv_dir: Path) -> Path:
    return venv_dir / ("Scripts/python.exe" if sys.platform.startswith("win")
                       else "bin/python")


def _venv_script(venv_dir: Path, name: str) -> Path:
    return venv_dir / ("Scripts" if sys.platform.startswith("win") else "bin") / name


def _build_and_install_wheel(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Build the wheel, install it into a fresh venv; return (wheel, venv, work)."""
    wheel_dir = tmp_path / "wheel"
    venv_dir = tmp_path / "venv"
    work_dir = tmp_path / "work"
    work_dir.mkdir()

    build = subprocess.run(
        [sys.executable, "-m", "pip", "wheel", str(REPO_ROOT), "--no-deps",
         "--wheel-dir", str(wheel_dir)],
        capture_output=True, text=True, timeout=600,
    )
    assert build.returncode == 0, build.stdout + build.stderr

    wheels = list(wheel_dir.glob("*.whl"))
    assert len(wheels) == 1, f"expected exactly one wheel, got {wheels}"

    venv.create(venv_dir, with_pip=True)
    install = subprocess.run(
        [str(_venv_python(venv_dir)), "-m", "pip", "install", str(wheels[0])],
        capture_output=True, text=True, timeout=600,
    )
    assert install.returncode == 0, install.stdout + install.stderr

    return wheels[0], venv_dir, work_dir


def test_wheel_contains_skill_trees(tmp_path):
    """The built wheel must actually contain the canonical skill trees."""
    wheel_dir = tmp_path / "wheel"
    build = subprocess.run(
        [sys.executable, "-m", "pip", "wheel", str(REPO_ROOT),
         "--no-deps", "--wheel-dir", str(wheel_dir)],
        capture_output=True, text=True, timeout=600,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    wheel = next(wheel_dir.glob("*.whl"))

    with zipfile.ZipFile(wheel) as z:
        names = z.namelist()
        assert any("SKILL.md" in n for n in names), (
            f"wheel {wheel.name} ships no SKILL.md files")
        assert PACKAGED_SKILL in names, (
            f"wheel {wheel.name} missing {PACKAGED_SKILL}")


def test_installed_wheel_setup_skills_delivers_canonical_skill(tmp_path):
    wheel, venv_dir, work_dir = _build_and_install_wheel(tmp_path)

    # The CLI must expose setup-skills.
    help_run = subprocess.run(
        [str(_venv_script(venv_dir, "sensemaking-skills")), "--help"],
        capture_output=True, text=True, timeout=60, cwd=str(work_dir),
    )
    assert help_run.returncode == 0, help_run.stdout + help_run.stderr
    assert "setup-skills" in help_run.stdout, (
        f"CLI does not expose setup-skills:\n{help_run.stdout}")

    # Run the documented setup path into a fresh custom destination.
    dest = tmp_path / "agent-skills"
    setup = subprocess.run(
        [str(_venv_script(venv_dir, "sensemaking-skills")), "setup-skills",
         "--target", "custom", "--skills-dir", str(dest)],
        capture_output=True, text=True, timeout=120, cwd=str(work_dir),
    )
    assert setup.returncode == 0, setup.stdout + setup.stderr

    # The canonical skill tree must be installed at the destination.
    installed = dest / "repo-sensemaker" / "SKILL.md"
    assert installed.is_file(), f"repo-sensemaker/SKILL.md not installed at {dest}"

    # Installed canonical files must match the release source byte-for-byte.
    for rel in [CANONICAL_SKILL] + CANONICAL_REFERENCES:
        src = (REPO_ROOT / rel).read_bytes()
        dst = dest / rel.removeprefix("skills/")
        assert dst.is_file(), f"installed asset missing: {dst}"
        assert dst.read_bytes() == src, f"installed asset differs from source: {rel}"

    # All canonical skills shipped in the repo root are installed.
    repo_skills = sorted(p.name for p in (REPO_ROOT / "skills").iterdir()
                         if (p / "SKILL.md").is_file())
    for name in repo_skills:
        assert (dest / name / "SKILL.md").is_file(), f"skill not installed: {name}"


def test_setup_skills_reports_drift_and_requires_force(tmp_path):
    """A divergent installed copy is reported, not silently overwritten."""
    wheel, venv_dir, work_dir = _build_and_install_wheel(tmp_path)
    dest = tmp_path / "agent-skills"

    setup = subprocess.run(
        [str(_venv_script(venv_dir, "sensemaking-skills")), "setup-skills",
         "--target", "custom", "--skills-dir", str(dest)],
        capture_output=True, text=True, timeout=120, cwd=str(work_dir),
    )
    assert setup.returncode == 0, setup.stdout + setup.stderr

    # Simulate a stale/divergent installed copy (like the pre-repair 178d5f0
    # 2026-05-22 global install that P1-R observed).
    installed = dest / "repo-sensemaker" / "SKILL.md"
    original = installed.read_bytes()
    installed.write_bytes(b"# stale divergent copy\n")

    # Re-running WITHOUT --force must report the drift and leave the file.
    rerun = subprocess.run(
        [str(_venv_script(venv_dir, "sensemaking-skills")), "setup-skills",
         "--target", "custom", "--skills-dir", str(dest)],
        capture_output=True, text=True, timeout=120, cwd=str(work_dir),
    )
    assert rerun.returncode != 0, (
        "setup-skills must fail when a divergent copy exists without --force:\n"
        + rerun.stdout + rerun.stderr)
    assert "Different from packaged version" in rerun.stdout, rerun.stdout
    assert installed.read_bytes() == b"# stale divergent copy\n", (
        "divergent copy must NOT be silently overwritten without --force")

    # WITH --force the divergent copy is deliberately replaced.
    forced = subprocess.run(
        [str(_venv_script(venv_dir, "sensemaking-skills")), "setup-skills",
         "--target", "custom", "--skills-dir", str(dest), "--force"],
        capture_output=True, text=True, timeout=120, cwd=str(work_dir),
    )
    assert forced.returncode == 0, forced.stdout + forced.stderr
    assert installed.read_bytes() == original, (
        "--force must replace the divergent copy with the canonical one")


def test_installed_wheel_supports_p6_capability_inspection_without_source_checkout(tmp_path):
    wheel, venv_dir, work_dir = _build_and_install_wheel(tmp_path)

    with zipfile.ZipFile(wheel) as z:
        assert PACKAGED_CAPABILITY_CATALOG in z.namelist(), (
            f"wheel {wheel.name} missing {PACKAGED_CAPABILITY_CATALOG}"
        )

    cli_path = str(_venv_script(venv_dir, "sensemaking-skills"))
    workspace = work_dir / "CMP-P6-WHEEL"

    initialized = subprocess.run(
        [
            cli_path, "campaign", "init",
            "--workspace", str(workspace),
            "--campaign-id", "CMP-P6-WHEEL",
            "--mission", "prove packaged P6 capability inspection",
            "--json",
        ],
        capture_output=True, text=True, timeout=120, cwd=str(work_dir),
    )
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr

    advanced = subprocess.run(
        [
            cli_path, "campaign", "advance",
            "--workspace", str(workspace),
            "--transition-id", "TR-P6-WHEEL",
            "--to-state", "architecture_review_needed",
            "--decision", "the agent explicitly authored an architecture review responsibility",
            "--responsibility-id", "R-P6-WHEEL",
            "--responsibility-statement", "inspect architecture-review capabilities",
            "--decision-blocked", "which capability, if any, the agent should select",
            "--scope", "installed-wheel P6 proof",
            "--authority", "authorized_autonomously",
            "--success-condition", "capability metadata is inspectable from the wheel",
            "--json",
        ],
        capture_output=True, text=True, timeout=120, cwd=str(work_dir),
    )
    assert advanced.returncode == 0, advanced.stdout + advanced.stderr

    inspected = subprocess.run(
        [
            cli_path, "campaign", "capabilities",
            "--workspace", str(workspace),
            "--responsibility-type", "architecture_review",
            "--json",
        ],
        capture_output=True, text=True, timeout=120, cwd=str(work_dir),
    )
    assert inspected.returncode == 0, inspected.stdout + inspected.stderr
    payload = json.loads(inspected.stdout)
    assert payload["code"] == "CAMPAIGN_CAPABILITIES"
    assert payload["candidate_count"] == 1
    assert payload["candidates"][0]["id"] == "architectural-review"
    assert payload["candidates"][0]["availability"] == "external"
    encoded = json.dumps(payload).lower()
    assert "recommended_capability" not in encoded
    assert "rank" not in encoded


def test_installed_wheel_supports_p7_handoff_and_fresh_resume_without_source_checkout(tmp_path):
    wheel, venv_dir, work_dir = _build_and_install_wheel(tmp_path)
    cli_path = str(_venv_script(venv_dir, "sensemaking-skills"))
    workspace = work_dir / "CMP-P7-WHEEL"

    campaign_help = subprocess.run(
        [cli_path, "campaign", "--help"],
        capture_output=True, text=True, timeout=60, cwd=str(work_dir),
    )
    assert campaign_help.returncode == 0, campaign_help.stdout + campaign_help.stderr
    assert "handoff" in campaign_help.stdout
    assert "resume" in campaign_help.stdout

    initialized = subprocess.run(
        [
            cli_path, "campaign", "init",
            "--workspace", str(workspace),
            "--campaign-id", "CMP-P7-WHEEL",
            "--mission", "prove packaged P7 fresh-context reconstruction",
            "--json",
        ],
        capture_output=True, text=True, timeout=120, cwd=str(work_dir),
    )
    assert initialized.returncode == 0, initialized.stdout + initialized.stderr

    advanced = subprocess.run(
        [
            cli_path, "campaign", "advance",
            "--workspace", str(workspace),
            "--transition-id", "TR-P7-WHEEL",
            "--to-state", "handoff_ready",
            "--decision", "the agent explicitly authored the responsibility before handoff",
            "--responsibility-id", "R-P7-WHEEL",
            "--responsibility-statement", "continue from durable campaign context",
            "--decision-blocked", "what the fresh agent should decide next",
            "--scope", "installed-wheel P7 proof",
            "--authority", "authorized_autonomously",
            "--success-condition", "fresh process reconstructs the exact durable context",
            "--json",
        ],
        capture_output=True, text=True, timeout=120, cwd=str(work_dir),
    )
    assert advanced.returncode == 0, advanced.stdout + advanced.stderr

    handed_off = subprocess.run(
        [
            cli_path, "campaign", "handoff",
            "--workspace", str(workspace),
            "--allowed-next-action", "fresh_agent_decides",
            "--json",
        ],
        capture_output=True, text=True, timeout=120, cwd=str(work_dir),
    )
    assert handed_off.returncode == 0, handed_off.stdout + handed_off.stderr
    handoff_payload = json.loads(handed_off.stdout)
    assert handoff_payload["code"] == "CAMPAIGN_HANDOFF_WRITTEN"
    assert len(handoff_payload["reconstruction_sha256"]) == 64

    resumed = subprocess.run(
        [
            cli_path, "campaign", "resume",
            "--workspace", str(workspace),
            "--json",
        ],
        capture_output=True, text=True, timeout=120, cwd=str(work_dir),
    )
    assert resumed.returncode == 0, resumed.stdout + resumed.stderr
    payload = json.loads(resumed.stdout)
    assert payload["code"] == "CAMPAIGN_RESUMED"
    assert payload["campaign_id"] == "CMP-P7-WHEEL"
    assert payload["state"]["current_state"] == "handoff_ready"
    assert payload["state"]["active_responsibility"]["id"] == "R-P7-WHEEL"
    assert payload["handoff"]["allowed_next_actions"] == ["fresh_agent_decides"]
    assert payload["reconstruction_sha256"] == handoff_payload["reconstruction_sha256"]
