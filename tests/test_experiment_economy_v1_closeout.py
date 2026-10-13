"""Terminal qualification checks for Issue #438 Experiment Economy v1."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_closeout_adds_no_experiment_runtime_or_scoring_surface() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    for forbidden in (
        "ExperimentEngine",
        "ExperimentRouter",
        "EvidenceGradeSelector",
        "RigorScore",
    ):
        assert forbidden not in pyproject
