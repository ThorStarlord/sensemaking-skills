"""Compose one change-scoped verification plan from existing query evidence.

The plan is a mechanical projection over already-returned surfaces:

- authored verification records from ``context.verification_refs``;
- direct test-function candidates from ``symbol_context.test_candidates``;
- separate explicit package re-export test candidates;
- guard-derived scenario candidates from
  ``symbol_context.verification_scenarios``.

Authored and syntactic test candidates merge into a deduplicated set of pytest target candidates.
Authored workflow file pointers and guard scenarios stay separate from pytest
candidates; neither is dispatched or executed. Explicit
gaps disclose what the composition did not establish.

It does not execute tests, generate test code, infer coverage, establish a
pass/fail status or authorize a change.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

_MAX_LIMIT = 250

_LIMITS = (
    "Candidates only. No test was executed; no pass/fail, failure, coverage, "
    "sufficiency or change-safety status is established.",
    "Authored verification records are file-level unless the record names an explicit "
    "test node; they do not prove that a specific test exercises this symbol.",
    "Direct test candidates are test functions/methods whose own body syntactically "
    "mentions the symbol; fixture, helper, parameterized and indirect coverage is "
    "NOT ASSESSED.",
    "One-hop explicit package re-export test candidates retain their import-syntax "
    "provenance; no runtime binding, indirect coverage or test result is established.",
    "Guard scenarios are source-level candidates from direct raise/assert guards. No "
    "executable test is generated or mapped; suggested inputs are heuristic hints.",
    "Authored GitHub workflow file references are manual inspection candidates only; "
    "workflow availability, job applicability, dispatch, and execution are NOT ASSESSED.",
    "A pytest target is an invocation candidate; pytest collection, execution, pass "
    "status and correctness are NOT ASSESSED.",
    "Only tracked Python source at the selected committed revision is inspected; "
    "uncommitted bytes and runtime-only relationships are not part of the plan.",
    "Verification records come from context.verification_refs. For an owned file they "
    "can include records linked from the owning component or an applicable rule, not "
    "necessarily tests of this symbol.",
)


def _reference_parts(reference: Any) -> tuple[str, str | None] | None:
    """Return a supported test path and optional node path, or None.

    Accepted forms are the same bounded strings the authored-record surfaces use:
    ``tests/example.py``, ``file:tests/example.py``,
    ``file:tests/example.py:line:42`` and ``file:tests/example.py#fragment``.
    An explicit ``::test`` segment is preserved as a node target. Fragments are
    not converted into test nodes because the authored record does not establish
    that meaning.
    """

    if not isinstance(reference, str):
        return None
    text = reference.strip()
    if text.startswith("file:"):
        text = text[5:]
    if not text:
        return None
    if "#" in text:
        text = text.split("#", 1)[0]
    if ":line:" in text:
        text = text.split(":line:", 1)[0]
    node = None
    if "::" in text:
        text, node = text.split("::", 1)
    if not text.startswith("tests/") or not text.endswith(".py"):
        return None
    if node and not all(part.isidentifier() for part in node.split("::")):
        node = None
    return text, node


def _test_target(reference: Any) -> str | None:
    parts = _reference_parts(reference)
    if parts is None:
        return None
    path, node = parts
    return f"{path}::{node}" if node else path


def _workflow_path(reference: Any) -> str | None:
    """Recognize an explicit authored GitHub workflow file pointer, not a job."""
    if not isinstance(reference, str):
        return None
    text = reference.strip()
    if text.startswith("file:"):
        text = text[5:]
    text = text.split("#", 1)[0].split(":line:", 1)[0]
    if re.fullmatch(r"\.github/workflows/[A-Za-z0-9_.-]+\.ya?ml", text):
        return text
    return None


def _string_list(value: Any) -> list[str]:
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def _record_references(record: Mapping[str, Any]) -> list[str]:
    references: list[str] = []
    authority = record.get("authority_ref")
    if isinstance(authority, str):
        references.append(authority)
    references.extend(_string_list(record.get("evidence_refs")))
    return list(dict.fromkeys(references))


def _authored_source(record: Mapping[str, Any]) -> dict[str, Any]:
    source = {
        "kind": "AUTHORED_VERIFICATION",
        "claim_id": record.get("claim_id"),
        "statement": record.get("statement"),
        "authority_kind": record.get("authority_kind"),
        "authority_ref": record.get("authority_ref"),
        "epistemic_status": record.get("epistemic_status"),
        "matched_by": _string_list(record.get("matched_by")),
    }
    conditions = record.get("recorded_conditions")
    if conditions:
        source["recorded_conditions"] = conditions
    return source


def _direct_source(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "kind": "DIRECT_TEST_FUNCTION",
        "test_kind": candidate.get("test_kind"),
        "test_name": candidate.get("test_name"),
        "reference_lines": [
            line for line in (candidate.get("reference_lines") or [])
            if isinstance(line, int)
        ],
    }


def _scenario_candidate(
    path: str | None, scenario: Mapping[str, Any],
) -> dict[str, Any]:
    line = scenario.get("line")
    return {
        "scenario_id": f"{path}:guard:{line}" if path else f"guard:{line}",
        "kind": scenario.get("kind"),
        "condition": scenario.get("condition"),
        "expected": scenario.get("expected"),
        "suggested_inputs": [
            item for item in (scenario.get("suggested_inputs") or [])
            if isinstance(item, str)
        ],
        "input_hint_basis": scenario.get("input_hint_basis"),
        "line": line,
        "definition_line": scenario.get("definition_line"),
        "evidence_ref": scenario.get("evidence_ref"),
        "pytest_target": None,
        "execution_status": "NOT_RUN",
        "test_mapping": "NOT_ASSESSED",
    }


def build_verification_plan(
    context: Mapping[str, Any],
    source_relationships: Mapping[str, Any],
    *,
    symbol: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    """Compose existing verification evidence into one bounded candidate plan."""

    if not 1 <= limit <= _MAX_LIMIT:
        raise ValueError("verification plan limit must be 1..250")

    target_meta = source_relationships.get("target")
    target_meta = target_meta if isinstance(target_meta, Mapping) else {}
    target_path = target_meta.get("path")
    symbol_context = source_relationships.get("symbol_context")
    symbol_context = symbol_context if isinstance(symbol_context, Mapping) else None
    plan_symbol = symbol if symbol is not None else (
        symbol_context.get("symbol") if symbol_context is not None else None
    )
    definitions = [
        item for item in (symbol_context.get("definitions") or [])
        if isinstance(item, Mapping)
    ] if symbol_context is not None else []
    symbol_defined = (
        bool(symbol_context.get("defined_in_target"))
        if symbol_context is not None else None
    )

    verification_records = [
        item for item in (context.get("verification_refs") or [])
        if isinstance(item, Mapping)
    ]

    candidates: dict[str, dict[str, Any]] = {}
    duplicate_target_merges = 0

    def add_candidate(
        target: str, source: Mapping[str, Any], evidence_refs: list[str],
    ) -> None:
        nonlocal duplicate_target_merges
        if target in candidates:
            duplicate_target_merges += 1
        candidate = candidates.setdefault(target, {
            "pytest_target": target,
            "scope": "TEST_FUNCTION" if "::" in target else "FILE",
            "sources": [],
            "evidence_refs": [],
            "execution_status": "NOT_RUN",
        })
        if source not in candidate["sources"]:
            candidate["sources"].append(dict(source))
        for reference in evidence_refs:
            if reference not in candidate["evidence_refs"]:
                candidate["evidence_refs"].append(reference)

    workflow_candidates: dict[str, dict[str, Any]] = {}
    workflow_mapped_authored = 0
    mapped_authored = 0
    file_scope_claim_ids: list[str] = []
    unmapped_authored: list[dict[str, Any]] = []
    for record in verification_records:
        references = _record_references(record)
        targets: list[str] = []
        for reference in references:
            target = _test_target(reference)
            if target is not None and target not in targets:
                targets.append(target)
        claim_id = record.get("claim_id")
        workflow_refs: dict[str, list[str]] = {}
        for reference in references:
            workflow_path = _workflow_path(reference)
            if workflow_path is not None:
                workflow_refs.setdefault(workflow_path, []).append(reference)
        if workflow_refs:
            workflow_mapped_authored += 1
        source = _authored_source(record)
        for workflow_path, matched_refs in workflow_refs.items():
            workflow = workflow_candidates.setdefault(workflow_path, {
                "path": workflow_path,
                "scope": "WORKFLOW_FILE",
                "sources": [],
                "evidence_refs": [],
                "inspection_status": "NOT_ASSESSED",
                "execution_status": "NOT_RUN",
            })
            if source not in workflow["sources"]:
                workflow["sources"].append(source)
            for reference in matched_refs:
                if reference not in workflow["evidence_refs"]:
                    workflow["evidence_refs"].append(reference)
        if not targets:
            unmapped_authored.append({
                "claim_id": claim_id,
                "authority_ref": record.get("authority_ref"),
                "evidence_refs": _string_list(record.get("evidence_refs")),
                "reason": "NO_TEST_FILE_REFERENCE",
            })
            continue
        mapped_authored += 1
        if isinstance(claim_id, str) and all("::" not in target for target in targets):
            file_scope_claim_ids.append(claim_id)
        for target in targets:
            add_candidate(target, source, references)

    direct_candidates = [
        item for item in (
            (symbol_context.get("test_candidates") or [])
            if symbol_context is not None else []
        )
        if isinstance(item, Mapping)
    ]
    for candidate in direct_candidates:
        path, name = candidate.get("path"), candidate.get("test_name")
        if not isinstance(path, str) or not isinstance(name, str):
            continue
        evidence_refs = _string_list(candidate.get("evidence_refs"))
        add_candidate(
            f"{path}::{name}", _direct_source(candidate), evidence_refs,
        )

    reexport_context = (
        symbol_context.get("package_reexport_context") if symbol_context is not None else None
    )
    reexport_context = reexport_context if isinstance(reexport_context, Mapping) else {}
    reexport_candidates = [
        item for item in (reexport_context.get("test_candidates") or [])
        if isinstance(item, Mapping)
    ]
    for candidate in reexport_candidates:
        path, name = candidate.get("path"), candidate.get("test_name")
        if not isinstance(path, str) or not isinstance(name, str):
            continue
        source = _direct_source(candidate)
        source.update({
            "kind": "PACKAGE_REEXPORT_TEST_FUNCTION",
            "package_reexport": candidate.get("package_reexport"),
            "consumer_import_lines": candidate.get("consumer_import_lines"),
            "consumer_import_line_total": candidate.get("consumer_import_line_total"),
        })
        add_candidate(f"{path}::{name}", source, _string_list(candidate.get("evidence_refs")))

    scenario_context = (
        symbol_context.get("verification_scenarios")
        if symbol_context is not None else None
    )
    scenario_context = scenario_context if isinstance(scenario_context, Mapping) else {}
    scenario_candidates = [
        _scenario_candidate(target_path, item)
        for item in (scenario_context.get("scenarios") or [])
        if isinstance(item, Mapping)
    ]
    scenario_candidates.sort(key=lambda item: (item["line"] or 0, item["expected"] or ""))

    pytest_candidates = sorted(
        candidates.values(),
        key=lambda item: (0 if item["scope"] == "FILE" else 1, item["pytest_target"]),
    )
    file_targets = sorted(
        item["pytest_target"] for item in pytest_candidates if item["scope"] == "FILE"
    )
    file_target_set = set(file_targets)
    function_targets = sorted(
        item["pytest_target"] for item in pytest_candidates
        if item["scope"] == "TEST_FUNCTION"
    )
    suggested_function_targets = [
        target for target in function_targets
        if target.split("::", 1)[0] not in file_target_set
    ]
    suggested_targets = [*file_targets, *suggested_function_targets]
    subsumed_function_targets = [
        target for target in function_targets if target not in suggested_function_targets
    ]
    counts = {
        "authored_verification_records": len(verification_records),
        "authored_verification_mapped_to_pytest": mapped_authored,
        "authored_verification_unmapped": len(unmapped_authored),
        "authored_verification_mapped_to_workflow": workflow_mapped_authored,
        "workflow_candidates": len(workflow_candidates),
        "authored_verification_file_scope": len(file_scope_claim_ids),
        "direct_test_functions": len(direct_candidates),
        "package_reexport_test_candidates": len(reexport_candidates),
        "guard_scenarios": len(scenario_candidates),
        "pytest_candidates": len(pytest_candidates),
        "pytest_file_candidates": sum(
            1 for item in pytest_candidates if item["scope"] == "FILE"
        ),
        "pytest_function_candidates": sum(
            1 for item in pytest_candidates if item["scope"] == "TEST_FUNCTION"
        ),
        "suggested_pytest_targets": len(suggested_targets),
        "function_targets_subsumed_by_file": len(subsumed_function_targets),
        "duplicate_target_merges": duplicate_target_merges,
        "parse_failures": (
            symbol_context.get("counts", {}).get("parse_failures", 0)
            if symbol_context is not None else 0
        ),
    }

    truncated = bool(
        context.get("truncated")
        or source_relationships.get("truncated")
        or (symbol_context is not None and symbol_context.get("truncated"))
        or scenario_context.get("truncated")
    )

    gaps: list[dict[str, Any]] = []
    if symbol_context is None:
        gaps.append({
            "category": "symbol_context",
            "status": "NOT_ASSESSED",
            "note": "No symbol context was returned. Direct test functions and guard "
                    "scenarios were not assessed; this is not evidence that none exist.",
        })
    elif not symbol_defined:
        gaps.append({
            "category": "symbol",
            "status": "NOT_DEFINED",
            "note": f"No top-level definition named {plan_symbol!r} was observed in the "
                    "target at this revision. Direct test functions and guard scenarios "
                    "were not assessed for that name.",
        })
    if not verification_records:
        gaps.append({
            "category": "authored_verification",
            "status": "NOT_ASSESSED",
            "note": "No authored verification record was returned for this file. This is "
                    "not evidence that no verification obligation exists.",
        })
    if file_scope_claim_ids:
        gaps.append({
            "category": "authored_verification",
            "status": "FILE_LEVEL_ONLY",
            "count": len(file_scope_claim_ids),
            "claim_ids": file_scope_claim_ids,
            "note": "These records support whole test files. They do not identify a test "
                    "function or prove that a given test exercises this symbol.",
        })
    if unmapped_authored:
        gaps.append({
            "category": "authored_verification",
            "status": "NO_TEST_FILE",
            "count": len(unmapped_authored),
            "claim_ids": [
                item["claim_id"] for item in unmapped_authored
                if item.get("claim_id") is not None
            ],
            "note": "These records did not identify a tests/*.py file, so no pytest "
                    "target was derived from them.",
        })
    if symbol_context is not None and symbol_defined and not direct_candidates:
        gaps.append({
            "category": "direct_test_functions",
            "status": "NONE_OBSERVED",
            "note": "No test function directly mentions the symbol in its own body. "
                    "Fixture, helper, parameterized and indirect coverage is NOT ASSESSED.",
        })
    if reexport_context.get("status") in {"NOT_ASSESSED", "PARTIAL"}:
        gaps.append({
            "category": "package_reexport",
            "status": reexport_context["status"],
            "note": "The bounded one-hop package syntax inquiry is incomplete or "
                    "unavailable. Inspect original source; absence is not proof of no use.",
        })
    if scenario_candidates:
        gaps.append({
            "category": "guard_scenarios",
            "status": "NO_EXECUTABLE_TEST",
            "count": len(scenario_candidates),
            "lines": [
                item["line"] for item in scenario_candidates
                if item.get("line") is not None
            ],
            "note": "Each guard scenario is a candidate condition, not a test. No test was "
                    "generated or mapped; inspect the pytest candidates or add a focused "
                    "test if the condition is not exercised.",
        })
    if truncated:
        gaps.append({
            "category": "limits",
            "status": "TRUNCATED",
            "note": "One or more source lists were truncated. The candidate set may be "
                    "incomplete; raise the limit or inspect the original sources.",
        })
    gaps.extend([
        {
            "category": "execution",
            "status": "NOT_RUN",
            "note": "No test was executed by this consumer. Pass/fail, failure and "
                    "behavioural status are NOT ESTABLISHED.",
        },
        {
            "category": "coverage",
            "status": "NOT_ASSESSED",
            "note": "Candidate presence is not coverage. Helpers, fixtures, "
                    "parameterization and indirect execution are not mapped.",
        },
    ])

    return {
        "artifact": "change_verification_plan",
        "target": {
            "path": target_path,
            "target_ref": target_meta.get("target_ref"),
            "sha256": target_meta.get("sha256"),
            "symbol": plan_symbol,
            "symbol_defined": symbol_defined,
            "definition_lines": sorted({
                item["line"] for item in definitions
                if isinstance(item.get("line"), int)
            }),
        },
        "selection_basis": {
            "authored_verification": "context.verification_refs",
            "direct_test_functions": "symbol_context.test_candidates",
            "package_reexport_test_functions": "symbol_context.package_reexport_context.test_candidates",
            "guard_scenarios": "symbol_context.verification_scenarios.scenarios",
        },
        "pytest_candidates": pytest_candidates,
        "workflow_candidates": [workflow_candidates[path] for path in sorted(workflow_candidates)],
        "suggested_pytest": {
            "test_files": file_targets,
            "test_functions": suggested_function_targets,
            "subsumed_function_candidates": subsumed_function_targets,
            "argv": (
                ["python", "-m", "pytest", *suggested_targets]
                if suggested_targets else None
            ),
            "execution_status": "NOT_RUN",
            "note": "Candidate invocation only. It was not executed; pytest "
                    "collection, pass status and coverage are NOT ASSESSED.",
        },
        "scenario_candidates": scenario_candidates,
        "unmapped_authored_verification": unmapped_authored,
        "counts": counts,
        "gaps": gaps,
        "limits": list(_LIMITS),
        "truncated": truncated,
        "tests_executed": False,
        "test_analysis_established": False,
        "test_results_established": False,
        "coverage_established": False,
        "semantic_truth_established": False,
        "action_authorized": False,
    }
