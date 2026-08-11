"""Gate policy for probe relationship findings (CI enforcement gate).

Runs the probe REPORT (not the probe itself) through an explicit policy:
which mechanically decidable finding types block the merge gate, and which
remain evidence for repo-sensemaker interpretation.

Division of labor (must stay stable; see docs/enforcement-contract.md):
- The Probe Engine acquires evidence candidates with provenance. The probe
  never decides policy.
- THIS script is the only place that decides which finding types are
  blocking. The set is deliberately small and each entry must be earned:
  a finding type may be promoted to blocking only if it is mechanically
  decidable AND the probe classifies it as not requiring semantic review.
- repo-sensemaker remains the interpreter for everything else; findings
  marked requires_semantic_review are NEVER blocking here.

Current blocking set (earned mechanical invariants):
- missing_reference: an ADR reference points at an ADR id that does not
  exist (e.g. "ADR 0025" with no docs/adr/0025-*.md). Pure lookup.
- missing_status_line: an ADR file has no **Status** line, breaking the
  convention every consumer (including this probe) relies on. Pure shape.

Not blocking (evidence only), even though mechanically detected:
- conflicting_values (product version): declaration roles (package.json
  vs pyproject vs __init__) need a policy decision before any value can
  block.
- status_claim_mismatch / unrecognized_status: the probe itself flags
  these as requiring semantic review (which side is stale is
  interpretation); per the contract, review-required findings never block.

Output is ASCII-only (the repository convention: no non-ASCII on stdout).

Exit codes: 0 = no blocking findings (report may still contain evidence
findings); 1 = at least one blocking finding; 2 = usage/read error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List

import yaml

BLOCKING_FINDING_TYPES: Dict[str, str] = {
    "missing_reference": "referenced ADR id does not exist",
    "missing_status_line": "ADR file missing a **Status** line",
}

# Finding types that are mechanically detected but deliberately NOT
# blocking (evidence only). Kept explicit so the contract is greppable.
EVIDENCE_ONLY_FINDING_TYPES: List[str] = [
    "conflicting_values",
    "status_claim_mismatch",
    "unrecognized_status",
]


def load_report(path: Path) -> dict:
    """Load a probe-report.yaml, raising ValueError if malformed."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise ValueError(f"cannot read report {path}: {exc}") from exc
    try:
        report = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ValueError(f"report {path} is not valid YAML: {exc}") from exc
    if not isinstance(report, dict):
        raise ValueError(f"report {path} is not a YAML mapping")
    return report


def iter_findings(report: dict):
    """Yield (section, finding) for every relationship finding."""
    relationships = report.get("relationships")
    if not isinstance(relationships, dict):
        return
    for section in ("version", "adr"):
        block = relationships.get(section)
        if not isinstance(block, dict):
            continue
        findings = block.get("findings")
        if isinstance(findings, list):
            for finding in findings:
                if isinstance(finding, dict):
                    yield section, finding


def _location(finding: dict) -> str:
    observations = finding.get("observations")
    if isinstance(observations, list) and observations:
        first = observations[0]
        if isinstance(first, dict) and first.get("location"):
            return str(first["location"])
    return ""


def evaluate(report: dict) -> tuple[List[dict], List[dict]]:
    """Return (blocking_findings, evidence_findings) for the report."""
    blocking: List[dict] = []
    evidence: List[dict] = []
    for section, finding in iter_findings(report):
        entry = {
            "section": section,
            "finding_type": finding.get("finding_type", "?"),
            "concept": finding.get("concept", section),
            "location": _location(finding),
            "notes": str(finding.get("notes", ""))[:200],
        }
        if entry["finding_type"] in BLOCKING_FINDING_TYPES:
            blocking.append(entry)
        else:
            evidence.append(entry)
    return blocking, evidence


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Apply the probe-report blocking policy (CI gate).")
    parser.add_argument("--report", required=True,
                        help="path to probe-report.yaml")
    args = parser.parse_args(argv)

    try:
        report = load_report(Path(args.report))
    except ValueError as exc:
        print(f"PROBE_GATE_READ_ERROR: {exc}")
        return 2

    blocking, evidence = evaluate(report)

    print("PROBE_GATE: relationship findings summary")
    print(f"  blocking findings: {len(blocking)}")
    print(f"  evidence findings (non-blocking): {len(evidence)}")
    for entry in evidence:
        print(f"  [evidence] {entry['section']}/{entry['finding_type']} "
              f"{entry['location']} {entry['notes']}")
    for entry in blocking:
        reason = BLOCKING_FINDING_TYPES.get(entry["finding_type"], "blocked")
        print(f"  [BLOCKING] {entry['section']}/{entry['finding_type']} "
              f"{entry['location']} - {reason}")

    if blocking:
        print("PROBE_GATE: FAIL - blocking relationship findings present "
              "(these are evidence for separate repair decisions; this "
              "script never decides how to fix them)")
        return 1
    print("PROBE_GATE: PASS - no blocking relationship findings")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
