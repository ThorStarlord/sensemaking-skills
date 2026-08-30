"""Artifact-contract agreement (directive #28 P1 #5): generic + specialized
validators agree on the final brief machine semantics:
- normal ACTION brief : recommended_workflow_id required, valid registry id
- explicit NO_CHANGE   : recommended_workflow_id absent/null VALID (affirmative-only)
- malformed combos     : fail (missing workflow on action / outcome inconsistency)
representation_sufficiency + outcome are declared among the brief's machine fields.
"""
import importlib.util
import os
import subprocess
import sys
import unittest

_SCRIPTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)


def _run_script(name, args):
    return subprocess.run(
        [sys.executable, os.path.join(_SCRIPTS, name)] + args,
        capture_output=True, text=True, cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
    )


def _brief(machine_lines):
    return (
        "# Repository Sensemaking Brief\n\n"
        "## 13. Machine-readable handoff\n\n```yaml\n"
        + "\n".join(machine_lines) + "\n```\n"
    )


_ACTION_BRIEF = _brief([
    "artifact_id: repository_sensemaking_brief",
    "schema_version: 1",
    "source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md",
    "user_implied_fog_type: architecture_fog",
    "primary_fog_type: architecture_fog",
    "diagnosis_conflict: false",
    "escalation_recommended: false",
    "evidence:\n  - \"a.py:1 x\"",
    "recommended_workflow_id: architecture-implementation-workflow",
    "recommended_execution_mode: guided_execution",
    "weakest_boundary: version-drift",
    "weakness_type: Contract Mismatch",
    "weakness_type_explanation: null",
    "required_inputs:\n  - repository_state",
    "created_at: \"2026-08-29T00:00:00Z\"",
    "immutable: true",
    "outcome: ACTION_REQUIRED",
    "representation_sufficiency:\n  status: sufficient",
])

_NO_CHANGE_BRIEF = _brief([
    "artifact_id: repository_sensemaking_brief",
    "schema_version: 1",
    "source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md",
    "primary_fog_type: architecture_fog",
    "evidence:\n  - \"a.py:1 x\"",
    "outcome: NO_REPOSITORY_CHANGE_WARRANTED",
    "recommended_workflow_id: null",
    "created_at: \"2026-08-29T00:00:00Z\"",
    "immutable: true",
])

_MALFORMED_ACTION = _brief([
    "artifact_id: repository_sensemaking_brief",
    "primary_fog_type: architecture_fog",
    "evidence:\n  - \"a.py:1 x\"",
    # ACTION but NO recommended_workflow_id -> malformed
    "outcome: ACTION_REQUIRED",
    "created_at: \"2026-08-29T00:00:00Z\"",
    "immutable: true",
])

_MALFORMED_NO_CHANGE = _brief([
    "artifact_id: repository_sensemaking_brief",
    "primary_fog_type: architecture_fog",
    "evidence:\n  - \"a.py:1 x\"",
    # explicit NO_CHANGE but also a workflow -> inconsistency
    "outcome: NO_REPOSITORY_CHANGE_WARRANTED",
    "recommended_workflow_id: architecture-implementation-workflow",
    "created_at: \"2026-08-29T00:00:00Z\"",
    "immutable: true",
])


class TestContractAgreement(unittest.TestCase):
    def _generic(self, text, name):
        d = os.path.join("tests", "fixtures", "contract_agreement")
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        r = _run_script("validate-artifact.py", ["repository_sensemaking_brief", p])
        return r.returncode, (r.stdout or r.stderr)

    def _specialized(self, text):
        import tempfile
        d = tempfile.mkdtemp()
        p = os.path.join(d, "brief.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        r = _run_script("validate-brief.py", [p, "--repo-root", "..", "--json"])
        import json
        try:
            j = json.loads(r.stdout)
        except Exception:
            j = {"valid": False, "errors": [{"message": (r.stdout or r.stderr)[:200]}]}
        return r.returncode, j

    def test_normal_action_brief(self):
        # A normal ACTION brief carries a valid workflow; the generic validator must
        # NOT fail on the now-recommended recommended_workflow_id nor the declared
        # optional representation_sufficiency/outcome fields.
        ec, out = self._generic(_ACTION_BRIEF, "action.md")
        errs = (out or "").lower()
        self.assertNotIn("missing required machine field", errs)

    def test_explicit_no_change_brief_valid(self):
        # Explicit NO_CHANGE with no workflow: the generic validator must NOT require
        # recommended_workflow_id (it is now recommended, required only by the
        # specialized validator for ACTION), and the specialized validator must NOT
        # reject the brief specifically for a missing workflow under NO_CHANGE.
        ec, out = self._generic(_NO_CHANGE_BRIEF, "nochange.md")
        self.assertNotIn("recommended_workflow_id", (out or "").lower(),
                         "generic validator must not require workflow on explicit NO_CHANGE")
        _, j = self._specialized(_NO_CHANGE_BRIEF)
        wf_errors = [e for e in j.get("errors", []) if "recommended_workflow_id" in e.get("message", "")]
        self.assertEqual([], wf_errors,
                         f"specialized validator must not reject NO_CHANGE for missing workflow: {wf_errors}")

    def test_malformed_action_missing_workflow(self):
        # ACTION without a workflow must FAIL the specialized validator.
        ec, j = self._specialized(_MALFORMED_ACTION)
        self.assertFalse(j.get("valid"), "ACTION brief missing workflow must fail")
        wf_errors = [e for e in j.get("errors", [])
                     if "recommended_workflow_id" in e.get("message", "")]
        self.assertTrue(wf_errors, "ACTION+missing-workflow must report a workflow error")

    def test_action_null_workflow_without_escalation_rejected(self):
        # ACTION + null recommended_workflow_id WITHOUT escalation_recommended: true
        # is a contract violation (truthful no-match requires escalation, ADR 0014).
        brief = _brief([
            "artifact_id: repository_sensemaking_brief",
            "primary_fog_type: architecture_fog",
            "evidence:\n  - \"a.py:1 x\"",
            "outcome: ACTION_REQUIRED",
            "recommended_workflow_id: null",
            "escalation_recommended: false",
            "created_at: \"2026-08-29T00:00:00Z\"",
            "immutable: true",
        ])
        ec, j = self._specialized(brief)
        self.assertFalse(j.get("valid"),
                         "ACTION+null workflow without escalation must be rejected")

    def test_action_unknown_workflow_rejected(self):
        # ACTION + unknown (hallucinated) workflow id must be rejected.
        brief = _brief([
            "artifact_id: repository_sensemaking_brief",
            "primary_fog_type: architecture_fog",
            "evidence:\n  - \"a.py:1 x\"",
            "outcome: ACTION_REQUIRED",
            "recommended_workflow_id: bogus-not-in-registry",
            "created_at: \"2026-08-29T00:00:00Z\"",
            "immutable: true",
        ])
        ec, j = self._specialized(brief)
        self.assertFalse(j.get("valid"),
                         "ACTION+unknown workflow must be rejected")

    def test_no_change_null_workflow_valid(self):
        # Explicit NO_CHANGE + null workflow is valid wrt the workflow/outcome invariant.
        brief = _brief([
            "artifact_id: repository_sensemaking_brief",
            "primary_fog_type: architecture_fog",
            "evidence:\n  - \"a.py:1 x\"",
            "outcome: NO_REPOSITORY_CHANGE_WARRANTED",
            "recommended_workflow_id: null",
            "created_at: \"2026-08-29T00:00:00Z\"",
            "immutable: true",
        ])
        _, j = self._specialized(brief)
        wf_errors = [e for e in j.get("errors", [])
                     if "NO_CHANGE_WORKFLOW_CONFLICT" in e.get("message", "")]
        self.assertEqual([], wf_errors,
                         "NO_CHANGE+null workflow must not be a workflow conflict")

    def test_no_change_nonnull_workflow_rejected(self):
        # Explicit NO_CHANGE + NON-null workflow MUST be rejected with the stable
        # NO_CHANGE_WORKFLOW_CONFLICT code (directive #29).
        _, j = self._specialized(_MALFORMED_NO_CHANGE)
        self.assertFalse(j.get("valid"),
                         "NO_CHANGE+non-null workflow must be invalid")
        conflict = [e for e in j.get("errors", [])
                    if "NO_CHANGE_WORKFLOW_CONFLICT" in e.get("message", "")]
        self.assertTrue(conflict,
                        f"expected NO_CHANGE_WORKFLOW_CONFLICT, got {j.get('errors')}")

    def test_missing_workflow_alone_never_no_change(self):
        # A missing/null recommended_workflow_id alone NEVER means NO_CHANGE:
        # without the explicit outcome, a brief with a missing workflow is still an
        # (invalid) ACTION brief, not a NO_CHANGE terminal.
        brief = _brief([
            "artifact_id: repository_sensemaking_brief",
            "primary_fog_type: architecture_fog",
            "evidence:\n  - \"a.py:1 x\"",
            # no outcome, no recommended_workflow_id
            "created_at: \"2026-08-29T00:00:00Z\"",
            "immutable: true",
        ])
        _, j = self._specialized(brief)
        # Must NOT be treated as a valid NO_CHANGE terminal; it is an invalid action
        # brief (missing workflow), never a NO_CHANGE success.
        self.assertNotIn("NO_REPOSITORY_CHANGE_WARRANTED",
                         " ".join(e.get("message", "") for e in j.get("errors", [])),
                         "missing workflow alone must not be reported as NO_CHANGE")
        wf_errors = [e for e in j.get("errors", [])
                     if "recommended_workflow_id" in e.get("message", "")]
        self.assertTrue(wf_errors, "missing workflow (no outcome) must be rejected")

    def test_representation_sufficiency_declared_in_contract(self):
        # representation_sufficiency + outcome must be declared among the brief's
        # machine fields (ADR 0015: programmatically-consumed fields belong there).
        import yaml
        contracts = yaml.safe_load(open(
            os.path.join("skills", "workflow-planner", "references", "artifact-contracts.yaml"),
            encoding="utf-8"))
        brief = next(a for a in contracts["artifacts"]
                     if a.get("id") == "repository_sensemaking_brief")
        fields = set(brief.get("required_machine_fields", [])) | \
                 set(brief.get("recommended_machine_fields", []))
        self.assertIn("representation_sufficiency", fields)
        self.assertIn("outcome", fields)
        self.assertIn("recommended_workflow_id", fields)  # still declared (recommended)


if __name__ == "__main__":
    unittest.main()
