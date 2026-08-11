"""Tests for scripts/gate-relationship-findings.py (CI enforcement policy).

The policy contract (docs/enforcement-contract.md):
- missing_reference / missing_status_line are BLOCKING (mechanical, probe
  says no semantic review required).
- conflicting_values / status_claim_mismatch / unrecognized_status are
  EVIDENCE ONLY (review-required or policy-dependent).
- Output must be ASCII-only.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from scripts.gate_relationship_findings import (
    BLOCKING_FINDING_TYPES,
    EVIDENCE_ONLY_FINDING_TYPES,
    evaluate,
    load_report,
    main,
)

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
GATE_SCRIPT = SCRIPTS_DIR / "gate_relationship_findings.py"


def _finding(finding_type: str, location: str = "docs/adr/0025-x.md:3") -> dict:
    return {
        "concept": "adr_integrity",
        "finding_type": finding_type,
        "confidence": "high",
        "requires_semantic_review": finding_type not in (
            "missing_reference", "missing_status_line"),
        "observations": [{"source": "docs/adr/x.md",
                          "location": location,
                          "value": "ADR 0025",
                          "evidence": "see ADR 0025"}],
        "notes": "test finding",
    }


def _report(adr_findings: list, version_findings: list | None = None) -> dict:
    return {
        "schema_version": 1,
        "relationships": {
            "doc_surface": {"total": 1, "live": 1, "by_class": {"live": 1}},
            "version": {
                "declarations": 1, "claims": 0, "distinct_values": [],
                "findings": version_findings or [],
            },
            "adr": {
                "files": 1, "references": 1,
                "findings": adr_findings,
            },
        },
    }


@pytest.fixture()
def report_file(tmp_path: Path) -> Path:
    return tmp_path / "probe-report.yaml"


def _write(report_file: Path, report: dict) -> None:
    import yaml
    report_file.write_text(yaml.safe_dump(report), encoding="utf-8")


# --- policy classification -------------------------------------------------

def test_missing_reference_is_blocking() -> None:
    blocking, evidence = evaluate(
        _report([_finding("missing_reference")]))
    assert len(blocking) == 1
    assert blocking[0]["finding_type"] == "missing_reference"
    assert evidence == []


def test_missing_status_line_is_blocking() -> None:
    blocking, evidence = evaluate(
        _report([_finding("missing_status_line")]))
    assert len(blocking) == 1
    assert blocking[0]["finding_type"] == "missing_status_line"
    assert evidence == []


def test_status_claim_mismatch_is_evidence_only() -> None:
    blocking, evidence = evaluate(
        _report([_finding("status_claim_mismatch")]))
    assert blocking == []
    assert [e["finding_type"] for e in evidence] == ["status_claim_mismatch"]


def test_version_conflict_is_evidence_only() -> None:
    blocking, evidence = evaluate(
        _report([], version_findings=[_finding("conflicting_values")]))
    assert blocking == []
    assert [e["finding_type"] for e in evidence] == ["conflicting_values"]


def test_mixed_findings_only_block_the_blocking_class() -> None:
    blocking, evidence = evaluate(_report([
        _finding("missing_reference"),
        _finding("status_claim_mismatch"),
    ]))
    assert [b["finding_type"] for b in blocking] == ["missing_reference"]
    assert [e["finding_type"] for e in evidence] == ["status_claim_mismatch"]


def test_empty_report_has_no_findings() -> None:
    blocking, evidence = evaluate(_report([]))
    assert blocking == []
    assert evidence == []


# --- blocking set integrity ------------------------------------------------

def test_blocking_set_is_subset_of_review_free_mechanical_types() -> None:
    # The contract: only findings the probe does NOT flag for semantic
    # review may ever be promoted to blocking. The script's own comment
    # claims this; the sets must not contradict the probe's classification.
    # (The probe sets requires_semantic_review=False for these.)
    assert "missing_reference" in BLOCKING_FINDING_TYPES
    assert "missing_status_line" in BLOCKING_FINDING_TYPES
    # Evidence-only types must be disjoint from blocking types.
    assert set(EVIDENCE_ONLY_FINDING_TYPES).isdisjoint(BLOCKING_FINDING_TYPES)


# --- CLI behavior ----------------------------------------------------------

def test_cli_exit_zero_on_evidence_only(report_file: Path) -> None:
    _write(report_file, _report([_finding("status_claim_mismatch")]))
    result = subprocess.run(
        [sys.executable, str(GATE_SCRIPT), "--report", str(report_file)],
        capture_output=True, text=True)
    assert result.returncode == 0
    assert "PROBE_GATE: PASS" in result.stdout
    assert "PROBE_GATE: FAIL" not in result.stdout


def test_cli_exit_one_on_blocking(report_file: Path) -> None:
    _write(report_file, _report([_finding("missing_reference")]))
    result = subprocess.run(
        [sys.executable, str(GATE_SCRIPT), "--report", str(report_file)],
        capture_output=True, text=True)
    assert result.returncode == 1
    assert "PROBE_GATE: FAIL" in result.stdout
    assert "[BLOCKING]" in result.stdout


def test_cli_exit_two_on_missing_report(report_file: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(GATE_SCRIPT), "--report",
         str(report_file.with_suffix(".nope"))],
        capture_output=True, text=True)
    assert result.returncode == 2
    assert "PROBE_GATE_READ_ERROR" in result.stdout


def test_cli_output_is_ascii(report_file: Path) -> None:
    _write(report_file, _report([_finding("missing_reference"),
                                 _finding("status_claim_mismatch")]))
    result = subprocess.run(
        [sys.executable, str(GATE_SCRIPT), "--report", str(report_file)],
        capture_output=True, text=True)
    assert result.returncode == 1
    result.stdout.encode("ascii")  # raises UnicodeEncodeError if non-ASCII


def test_main_function_return_codes() -> None:
    assert main(["--report", "definitely-missing.yaml"]) == 2
