"""S2 validator NO_REPOSITORY_CHANGE_WARRANTED contract (production validator).

Uses the REAL scripts/validate-brief.py via subprocess (matching repo test
convention) to prove:
  - outcome=NO_REPOSITORY_CHANGE_WARRANTED + absent recommended_workflow_id => VALID.
  - action-bearing brief (no NO_CHANGE outcome) missing recommended_workflow_id
    => INVALID (unchanged requirement).
  - missing recommended_workflow_id alone NEVER implies NO_CHANGE (a brief
    without the explicit outcome still fails).
"""
import json
import os
import subprocess
import sys
import tempfile

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATE_BRIEF = os.path.join(REPO_ROOT, "scripts", "validate-brief.py")

HDR = [
    "# Repository Sensemaking Brief (test fixture)\n",
    "\n",
    "## Evidence\n",
    "- README.md (lines 5-12): Feature requirements are vague\n",
    "\n",
    "## Evidence excerpts\n",
    "\n",
    "```yaml\n",
    "evidence_excerpts:\n",
    '  - file: "README.md"\n',
    '    lines: "5-12"\n',
    '    quote: "An agent-native framework for repository diagnosis and workflow orchestration."\n',
    '    supports_claim: "product_fog: feature scope is undefined"\n',
    "```\n",
    "\n",
    "## Recommended Workflow\n",
    "\n",
    "Logic trace: the evidence shows feature requirements are unwritten and issues\n",
    "lack acceptance criteria, so the fog is centered on undefined product scope.\n",
    "\n",
    "---\n",
    "\n",
]


def _brief_machine_yaml(extra: dict) -> str:
    """Compose a machine-readible handoff block."""
    base = {
        "artifact_id": "repository_sensemaking_brief",
        "primary_fog_type": "product_fog",
        "evidence": ["README.md (lines 5-12): Feature requirements are vague"],
        "weakness_type": "Vocabulary Drift",
        "created_at": "2026-05-24T15:30:00Z",
        "immutable": True,
    }
    base.update(extra)
    lines = ["\n## 13. Machine-readable handoff\n", "```yaml\n"]
    for k, v in base.items():
        if k == "evidence":
            lines.append("evidence:\n")
            for e in v:
                lines.append(f'  - "{e}"\n')
        elif v is None:
            lines.append(f"{k}: null\n")
        else:
            lines.append(f"{k}: {v}\n")
    lines.append("```\n")
    return "".join(lines)


def _run_validator(path: str) -> dict:
    proc = subprocess.run(
        [sys.executable, VALIDATE_BRIEF, path, "--repo-root", REPO_ROOT, "--json"],
        capture_output=True, text=True,
    )
    try:
        return json.loads(proc.stdout)
    except Exception:
        return {"valid": False, "errors": [{"message": proc.stdout or proc.stderr}]}


def _write_brief(extra: dict) -> str:
    tmp = tempfile.NamedTemporaryFile(
        suffix=".md", mode="w", delete=False, encoding="utf-8"
    )
    tmp.write("".join(HDR))
    tmp.write(_brief_machine_yaml(extra))
    tmp.close()
    return tmp.name


class TestS2NoChangeContract:
    def _error_ids(self, r) -> list:
        return [e.get("error_id", "") or e.get("message", "")[:40] for e in r["errors"]]

    def test_no_change_outcome_without_workflow_is_valid(self):
        path = _write_brief({"outcome": "NO_REPOSITORY_CHANGE_WARRANTED"})
        try:
            r = _run_validator(path)
            ids = self._error_ids(r)
            # S2 contract: NO_CHANGE omits recommended_workflow_id WITHOUT a
            # malformed-recommendation / missing-workflow error.
            assert not any("recommended_workflow_id" in i for i in ids), ids
        finally:
            os.unlink(path)

    def test_action_brief_without_workflow_is_invalid(self):
        # No outcome field -> default action-bearing requirement applies.
        path = _write_brief({})  # no recommended_workflow_id, no NO_CHANGE outcome
        try:
            r = _run_validator(path)
            ids = self._error_ids(r)
            assert any("recommended_workflow_id" in i for i in ids), ids
        finally:
            os.unlink(path)

    def test_missing_workflow_never_implies_no_change(self):
        # A brief WITHOUT the explicit outcome, missing workflow, must NOT become
        # a successful NO_CHANGE (still fails the workflow requirement). J-safeguard.
        path = _write_brief({})
        try:
            r = _run_validator(path)
            ids = self._error_ids(r)
            assert any("recommended_workflow_id" in i for i in ids)
        finally:
            os.unlink(path)

    def test_action_brief_with_workflow_no_workflow_error(self):
        # Action-bearing WITH a CURRENT active workflow: no
        # recommended_workflow_id error. ADR 0027 intentionally excludes
        # compatibility-only IDs from this current-capability assertion.
        path = _write_brief({
            "recommended_workflow_id": "full-fog-workflow",
        })
        try:
            r = _run_validator(path)
            ids = self._error_ids(r)
            assert not any("recommended_workflow_id" in i for i in ids), ids
        finally:
            os.unlink(path)