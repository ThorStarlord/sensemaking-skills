"""Terminal qualification checks for Issue #432 Decision Journey Productization v1."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_closeout_adds_no_strategic_planner_runtime() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "StrategicPlanner" not in pyproject
    assert "OuterLoopEngine" not in pyproject
