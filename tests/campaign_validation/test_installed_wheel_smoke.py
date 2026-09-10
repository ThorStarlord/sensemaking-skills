"""Installed-wheel product-boundary smoke test.

Build the real wheel, prove source-only lab packages and their dependencies are
absent, then exercise an ordinary Campaign plus the shipped semantic/portability
substrate from an isolated installed venv.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
import venv
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LAB_PREFIXES = (
    "sensemaking_skills/campaign_accounting/",
    "sensemaking_skills/campaign_validation/",
    "sensemaking_skills/exploratory_authorization/",
    "sensemaking_skills/exploratory_execution/",
)

_SMOKE_SCRIPT = textwrap.dedent(
    r'''
    import importlib
    import os
    import tempfile
    from pathlib import Path

    assert not os.path.isdir("docs")
    assert not os.path.isdir("scripts")

    import sensemaking_skills
    from sensemaking_skills.campaign_semantics import CampaignState
    from sensemaking_skills.campaigns import CampaignBundleService, CampaignService
    from sensemaking_skills.semantic_architecture import (
        build_repository_semantic_map,
        probe_exact_search,
    )

    assert sensemaking_skills.__version__ != "0+unknown"

    workspace = Path(tempfile.mkdtemp()) / "CMP-WHEEL"
    service = CampaignService(workspace)
    snapshot = service.initialize(
        CampaignState(
            campaign_id="CMP-WHEEL",
            mission="prove shipped core Campaign works",
            status="active",
            current_state="initialized",
        )
    )
    assert snapshot.state.campaign_id == "CMP-WHEEL"
    assert snapshot.state.schema_version == "2"
    assert service.resume().state.current_state == "initialized"

    semantic_target = workspace.parent / "semantic-target"
    semantic_target.mkdir()
    (semantic_target / "note.txt").write_text("needle\n", encoding="utf-8")
    probe = probe_exact_search(
        semantic_target,
        target_ref="sha:wheel",
        pattern="needle",
    )
    assert probe.semantic_truth_established is False
    semantic_map = build_repository_semantic_map(
        map_id="MAP-WHEEL",
        target_ref="sha:wheel",
        observations=probe.observations,
    )
    assert semantic_map.relations
    assert semantic_map.semantic_truth_established is False

    bundle_path = workspace.parent / "campaign.zip"
    CampaignBundleService(workspace).export(bundle_path)
    bundle_result = CampaignBundleService.verify(bundle_path)
    assert bundle_result.valid
    assert bundle_result.semantic_truth_established is False

    for module_name in (
        "sensemaking_skills.campaign_accounting",
        "sensemaking_skills.campaign_validation",
        "sensemaking_skills.exploratory_authorization",
        "sensemaking_skills.exploratory_execution",
    ):
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError:
            pass
        else:
            raise AssertionError(f"source-only lab package leaked into wheel: {module_name}")

    print("CORE_WHEEL_SMOKE_OK")
    '''
)


def test_installed_wheel_contains_product_but_not_source_only_lab(tmp_path):
    wheel_dir = tmp_path / "wheel"
    venv_dir = tmp_path / "venv"
    work_dir = tmp_path / "work"
    work_dir.mkdir()

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
        timeout=300,
    )
    assert build.returncode == 0, build.stdout + build.stderr

    wheels = list(wheel_dir.glob("*.whl"))
    assert len(wheels) == 1, f"expected exactly one wheel, got {wheels}"
    wheel = wheels[0]

    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        for prefix in LAB_PREFIXES:
            assert not any(name.startswith(prefix) for name in names), prefix
        assert any(
            name.endswith("sensemaking_skills/semantic_architecture/__init__.py")
            for name in names
        )
        assert any(
            name.endswith("sensemaking_skills/campaigns/bundle.py")
            for name in names
        )
        metadata_names = [name for name in names if name.endswith(".dist-info/METADATA")]
        assert len(metadata_names) == 1
        metadata = archive.read(metadata_names[0]).decode("utf-8").lower()
        assert "requires-dist: jsonschema" not in metadata
        assert "requires-dist: rfc8785" not in metadata
        assert "requires-dist: click" in metadata
        assert "requires-dist: pyyaml" in metadata

    venv.create(venv_dir, with_pip=True)
    venv_python = venv_dir / (
        "Scripts/python.exe" if sys.platform.startswith("win") else "bin/python"
    )
    install = subprocess.run(
        [str(venv_python), "-m", "pip", "install", str(wheel)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert install.returncode == 0, install.stdout + install.stderr

    run = subprocess.run(
        [str(venv_python), "-c", _SMOKE_SCRIPT],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=str(work_dir),
    )
    assert run.returncode == 0, run.stdout + run.stderr
    assert "CORE_WHEEL_SMOKE_OK" in run.stdout
