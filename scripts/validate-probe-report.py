"""Validator for probe-report.yaml produced by scripts/probe-repo.py.

Error codes (substrings matched by tests/fixtures/validate-probe-report/):
  PROBE_REPORT_NOT_FOUND
  PROBE_REPORT_PARSE_ERROR
  PROBE_REPORT_SCHEMA_VERSION
  PROBE_REPORT_MISSING_KEY
  PROBE_REPORT_VG_RANGE
  PROBE_REPORT_CE_NEGATIVE
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

import yaml

REQUIRED_KEYS = (
    "schema_version",
    "probe_tool",
    "generated_at",
    "repo_root",
    "git_state",
    "verification_gap",
    "context_entropy",
    "test_collection",
    "fixtures_coverage",
    "churn",
)

FRONTMATTER_RE = re.compile(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n", re.DOTALL)


def load_report(path: Path) -> Optional[dict]:
    """Load a probe report, tolerating the harness's frontmatter convention."""
    if not path.is_file():
        print("[PROBE_REPORT_NOT_FOUND] report file not found: " + str(path))
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"[PROBE_REPORT_PARSE_ERROR] unreadable: {exc}")
        return None
    body = FRONTMATTER_RE.sub("", text, count=1)
    try:
        data = yaml.safe_load(body)
    except yaml.YAMLError as exc:
        print(f"[PROBE_REPORT_PARSE_ERROR] invalid YAML: {exc}")
        return None
    if not isinstance(data, dict):
        print("[PROBE_REPORT_PARSE_ERROR] report is not a mapping")
        return None
    return data


def validate_report(data: dict) -> bool:
    ok = True

    if data.get("schema_version") != 1:
        print("[PROBE_REPORT_SCHEMA_VERSION] expected schema_version 1")
        ok = False

    for key in REQUIRED_KEYS:
        if key not in data:
            print(f"[PROBE_REPORT_MISSING_KEY] missing required key: {key}")
            ok = False

    vg = (data.get("verification_gap") or {}).get("vg")
    if vg is not None and not isinstance(vg, (int, float)):
        print("[PROBE_REPORT_VG_RANGE] vg must be numeric")
        ok = False
    elif vg is not None and not (0.0 <= float(vg) <= 1.0):
        print(f"[PROBE_REPORT_VG_RANGE] vg out of range [0,1]: {vg}")
        ok = False

    ce = (data.get("context_entropy") or {}).get("ce")
    if ce is not None and isinstance(ce, (int, float)) and float(ce) < 0.0:
        print(f"[PROBE_REPORT_CE_NEGATIVE] ce must be >= 0: {ce}")
        ok = False

    return ok


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate a probe-report.yaml")
    parser.add_argument("report_path", help="Path to the probe report (or negative fixture)")
    parser.add_argument("--repo-root", default=".", help="Unused by this validator; harness contract")
    args = parser.parse_args(argv)

    data = load_report(Path(args.report_path))
    if data is None:
        return 1
    return 0 if validate_report(data) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))