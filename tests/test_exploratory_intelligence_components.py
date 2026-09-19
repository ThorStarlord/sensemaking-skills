"""Contract tests for Experimental Intelligence Components v0.

These tests protect the experiment/product boundary. They do not evaluate the
semantic quality of StrategicPlanner output.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "intelligence-components-v0" / "strategic_planner_v0.py"
CASES_PATH = ROOT / "experiments" / "intelligence-components-v0" / "cases-v0.yaml"
SIMULATED_CASES_PATH = (
    ROOT
    / "experiments"
    / "intelligence-components-v0"
    / "simulated-e2e-v0"
    / "case-v0.yaml"
)

SPEC = importlib.util.spec_from_file_location("strategic_planner_v0", MODULE_PATH)
assert SPEC and SPEC.loader
planner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(planner)


def _normalized(value: str) -> str:
    return " ".join(value.split())


def test_frozen_cases_are_explicitly_retrospective_and_loadable() -> None:
    cases = planner.load_cases(CASES_PATH)

    assert len(cases) == 4
    assert {case["id"] for case in cases} == {
        "release-identity-drift",
        "stale-authority-reference",
        "goal-a-environment-blocker",
        "execution-interface-boundary",
    }


def test_constructed_smoke_case_is_supported_without_historical_outcome() -> None:
    cases = planner.load_cases(SIMULATED_CASES_PATH)

    assert len(cases) == 1
    assert cases[0]["id"] == "quartz-cli-dry-run-contract"
    assert "historical_outcome" not in cases[0]


def test_constructed_case_must_not_claim_hindsight_contamination(tmp_path: Path) -> None:
    raw = SIMULATED_CASES_PATH.read_text(encoding="utf-8")
    bad = raw.replace("hindsight_contaminated: false", "hindsight_contaminated: true")
    path = tmp_path / "bad-simulated.yaml"
    path.write_text(bad, encoding="utf-8")

    with pytest.raises(planner.ExperimentContractError):
        planner.load_cases(path)


@pytest.mark.parametrize("arm", ["baseline", "treatment"])
def test_packet_rendering_is_deterministic(arm: str) -> None:
    case = planner.load_cases(CASES_PATH)[0]

    first = planner.render_packet(case, arm)
    second = planner.render_packet(dict(case), arm)

    assert first == second


def test_baseline_preserves_current_semantic_selection() -> None:
    case = planner.load_cases(CASES_PATH)[0]
    packet = planner.render_baseline_packet(case)
    normalized = _normalized(packet)

    assert "select one warranted repository-level responsibility" in normalized
    assert "STRATEGICPLANNER V0" not in packet
    assert "generate 2–4" not in packet


def test_treatment_generates_candidates_without_claiming_decision_authority() -> None:
    case = planner.load_cases(CASES_PATH)[0]
    packet = planner.render_treatment_packet(case)
    normalized = _normalized(packet)

    assert "generate 2–4" in normalized
    assert "Do not rank the candidates." in normalized
    assert "Do not choose a winner." in normalized
    assert "Do not execute anything." in normalized
    assert "Do not split a contingent substep or diagnostic branch" in normalized
    assert "candidate generation != strategic decision" in packet
    assert "planner output != implementation plan" in packet


def test_case_contract_rejects_preselected_or_authorized_action() -> None:
    case = dict(planner.load_cases(CASES_PATH)[0])
    case["selected_responsibility"] = "secretly-decided"

    with pytest.raises(planner.ExperimentContractError):
        planner.validate_case(case)


def test_case_contract_rejects_numeric_priority_score() -> None:
    case = dict(planner.load_cases(CASES_PATH)[0])
    case["priority_score"] = 99

    with pytest.raises(planner.ExperimentContractError):
        planner.validate_case(case)


def test_experiment_is_not_imported_as_a_shipped_product_module() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert "experiments/intelligence-components-v0" not in pyproject
    assert "strategic_planner_v0" not in pyproject
