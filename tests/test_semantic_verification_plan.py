"""Composition tests for the change-scoped verification plan consumer."""

from __future__ import annotations

from sensemaking_skills.semantic_architecture.verification_plan import (
    build_verification_plan,
)

SHA = "a" * 40
TARGET = "src/pkg/widgets.py"


def relationships(symbol_context, *, truncated: bool = False):
    return {
        "target": {"path": TARGET, "target_ref": SHA, "sha256": "b" * 64},
        "symbol_context": symbol_context,
        "truncated": truncated,
    }


def symbol_context(*, test_candidates=(), scenarios=(), defined: bool = True):
    return {
        "symbol": "build_widget",
        "defined_in_target": defined,
        "definitions": [{"line": 10}] if defined else [],
        "test_candidates": list(test_candidates),
        "verification_scenarios": {
            "scenarios": list(scenarios),
            "truncated": False,
        },
        "counts": {"parse_failures": 0},
        "truncated": False,
    }


def authored(claim_id: str, authority: str, evidence: list[str]):
    return {
        "claim_id": claim_id,
        "kind": "verification",
        "statement": "Fixture verification record.",
        "authority_kind": "test",
        "authority_ref": authority,
        "evidence_refs": evidence,
        "epistemic_status": "declared",
        "matched_by": ["relation component:widget tested_by " + claim_id],
    }


def test_plan_merges_authored_and_direct_targets_without_duplicate_entries():
    context = {
        "verification_refs": [
            authored("verification:widget-a", "tests/test_widgets.py", [
                "file:tests/test_widgets.py",
                "file:tests/test_widgets.py:line:12",
            ]),
            authored("verification:widget-b", "tests/test_widgets.py", [
                "file:tests/test_widgets.py",
            ]),
        ],
        "truncated": False,
    }
    plan = build_verification_plan(
        context,
        relationships(symbol_context(
            test_candidates=[{
                "path": "tests/test_widgets.py",
                "test_name": "test_build_widget",
                "test_kind": "FUNCTION",
                "reference_lines": [12],
                "evidence_refs": ["file:tests/test_widgets.py:line:12"],
            }],
        )),
        symbol="build_widget",
    )

    targets = [item["pytest_target"] for item in plan["pytest_candidates"]]
    assert targets == [
        "tests/test_widgets.py",
        "tests/test_widgets.py::test_build_widget",
    ]
    assert len(targets) == len(set(targets))
    file_candidate = plan["pytest_candidates"][0]
    assert file_candidate["execution_status"] == "NOT_RUN"
    assert [source["claim_id"] for source in file_candidate["sources"]] == [
        "verification:widget-a",
        "verification:widget-b",
    ]
    assert plan["counts"]["duplicate_target_merges"] == 1
    assert plan["counts"]["pytest_candidates"] == 2
    suggested = plan["suggested_pytest"]
    assert suggested["test_files"] == ["tests/test_widgets.py"]
    assert suggested["test_functions"] == []
    assert suggested["subsumed_function_candidates"] == [
        "tests/test_widgets.py::test_build_widget",
    ]
    assert suggested["argv"] == ["python", "-m", "pytest", "tests/test_widgets.py"]
    assert suggested["execution_status"] == "NOT_RUN"


def test_suggested_invocation_keeps_function_targets_without_file_coverage():
    plan = build_verification_plan(
        {"verification_refs": [], "truncated": False},
        relationships(symbol_context(test_candidates=[
            {
                "path": "tests/test_widgets.py",
                "test_name": "test_build_widget",
                "test_kind": "FUNCTION",
                "reference_lines": [12],
                "evidence_refs": ["file:tests/test_widgets.py:line:12"],
            },
            {
                "path": "tests/test_widget_helpers.py",
                "test_name": "TestWidgets::test_guard",
                "test_kind": "METHOD",
                "reference_lines": [40],
                "evidence_refs": ["file:tests/test_widget_helpers.py:line:40"],
            },
        ])),
        symbol="build_widget",
    )

    suggested = plan["suggested_pytest"]
    assert suggested["test_files"] == []
    assert suggested["test_functions"] == [
        "tests/test_widget_helpers.py::TestWidgets::test_guard",
        "tests/test_widgets.py::test_build_widget",
    ]
    assert suggested["subsumed_function_candidates"] == []
    assert suggested["argv"] == [
        "python", "-m", "pytest",
        "tests/test_widget_helpers.py::TestWidgets::test_guard",
        "tests/test_widgets.py::test_build_widget",
    ]


def test_plan_keeps_guard_scenarios_non_executable_and_names_the_gap():
    scenario = {
        "kind": "RAISE",
        "condition": "not 1 <= limit <= 10",
        "expected": "ValueError",
        "suggested_inputs": ["limit=0", "limit=11"],
        "input_hint_basis": "BOUNDARY_CONSTANTS",
        "line": 42,
        "definition_line": 10,
        "evidence_ref": f"file:{TARGET}:42",
    }
    plan = build_verification_plan(
        {"verification_refs": [], "truncated": False},
        relationships(symbol_context(scenarios=[scenario])),
        symbol="build_widget",
    )

    candidate = plan["scenario_candidates"][0]
    assert candidate["pytest_target"] is None
    assert candidate["execution_status"] == "NOT_RUN"
    assert candidate["test_mapping"] == "NOT_ASSESSED"
    assert candidate["suggested_inputs"] == ["limit=0", "limit=11"]
    gap = next(item for item in plan["gaps"] if item["status"] == "NO_EXECUTABLE_TEST")
    assert gap["count"] == 1
    assert gap["lines"] == [42]


def test_plan_reports_unmapped_authored_records_and_absent_direct_tests():
    plan = build_verification_plan(
        {
            "verification_refs": [
                authored("verification:docs", "docs/test-plan.md", ["file:docs/test-plan.md"]),
            ],
            "truncated": False,
        },
        relationships(symbol_context()),
        symbol="build_widget",
    )

    assert plan["pytest_candidates"] == []
    assert plan["suggested_pytest"]["argv"] is None
    assert plan["suggested_pytest"]["test_files"] == []
    assert plan["unmapped_authored_verification"] == [{
        "claim_id": "verification:docs",
        "authority_ref": "docs/test-plan.md",
        "evidence_refs": ["file:docs/test-plan.md"],
        "reason": "NO_TEST_FILE_REFERENCE",
    }]
    statuses = {item["status"] for item in plan["gaps"]}
    assert {"NO_TEST_FILE", "NONE_OBSERVED"} <= statuses


def test_plan_states_that_execution_analysis_coverage_and_authority_are_absent():
    plan = build_verification_plan(
        {"verification_refs": [], "truncated": False},
        relationships(symbol_context()),
        symbol="build_widget",
    )

    assert plan["tests_executed"] is False
    assert plan["test_analysis_established"] is False
    assert plan["test_results_established"] is False
    assert plan["coverage_established"] is False
    assert plan["semantic_truth_established"] is False
    assert plan["action_authorized"] is False
    assert any("No test was executed" in limit for limit in plan["limits"])
    gaps = {item["status"] for item in plan["gaps"]}
    assert {"NOT_RUN", "NOT_ASSESSED"} <= gaps


def test_plan_keeps_authored_evidence_when_symbol_context_is_unassessed():
    plan = build_verification_plan(
        {
            "verification_refs": [
                authored("verification:widget", "tests/test_widgets.py", [
                    "file:tests/test_widgets.py",
                ]),
            ],
            "truncated": False,
        },
        relationships(None),
        symbol="build_widget",
    )

    assert plan["target"]["symbol"] == "build_widget"
    assert plan["target"]["symbol_defined"] is None
    assert [item["pytest_target"] for item in plan["pytest_candidates"]] == [
        "tests/test_widgets.py",
    ]
    assert plan["scenario_candidates"] == []
    gap = next(item for item in plan["gaps"] if item["category"] == "symbol_context")
    assert gap["status"] == "NOT_ASSESSED"


def test_plan_reports_a_symbol_that_is_not_defined_in_the_target():
    plan = build_verification_plan(
        {"verification_refs": [], "truncated": False},
        relationships(symbol_context(defined=False)),
        symbol="build_widget",
    )

    assert plan["target"]["symbol_defined"] is False
    assert plan["pytest_candidates"] == []
    assert plan["scenario_candidates"] == []
    gap = next(item for item in plan["gaps"] if item["category"] == "symbol")
    assert gap["status"] == "NOT_DEFINED"
