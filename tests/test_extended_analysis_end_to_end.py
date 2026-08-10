"""End-to-end producer/consumer handoff proof for Section 15 (ADR 0024).

Per CLAUDE.md's verification discipline: "'Done' requires running the
real path... exercise it end-to-end against realistic artifacts." The
per-module tests (test_brief_skeleton_extended_analysis.py,
test_validate_brief_extended_analysis.py) each prove their own half in
isolation. This test proves the actual handoff: a realistic model
response, run through brief_skeleton.reconcile() (the real producer),
written to disk, and validated through BOTH validators in the real
verification chain declared in artifact-contracts.yaml
(generic_validator then specialized_validators) -- not a hand-authored
fixture that assumes the shape rather than exercising it.
"""

import importlib.util
import os
import sys
import tempfile
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import brief_skeleton as bs  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))


def _load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SCRIPTS_DIR, filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate_brief_module = _load_module("validate_brief", "validate-brief.py")
validate_artifact_module = _load_module("validate_artifact", "validate-artifact.py")


REALISTIC_MODEL_OUTPUT = """
<!-- MODEL_SECTION:repository_goal:BEGIN -->
This repository builds sensemaking skills for AI agents.
<!-- MODEL_SECTION:repository_goal:END -->

<!-- MODEL_SECTION:weakest_boundary_prose:BEGIN -->
**Weakness type:** Zero Validation
<!-- MODEL_SECTION:weakest_boundary_prose:END -->

<!-- MODEL_SECTION:evidence_prose:BEGIN -->
scripts/brief_skeleton.py:52 shows the artifact_id constant.

Logic trace: the constant is read directly, which is the chain from
evidence to the weakest-boundary conclusion.
<!-- MODEL_SECTION:evidence_prose:END -->

<!-- MODEL_SECTION:evidence_excerpts:BEGIN -->
```yaml
evidence_excerpts:
  - file: scripts/brief_skeleton.py
    lines: L52
    quote: "see file/lines"
    supports_claim: "artifact_id is defined here"
```
<!-- MODEL_SECTION:evidence_excerpts:END -->

<!-- MODEL_SECTION:extended_analysis:BEGIN -->
```yaml
extended_analysis:
  schema_version: 1
  domain:
    - architecture
  consequential_boundary:
    description: "The skeleton mechanism is now production-real."
    rationale: "reconcile() only splices declared holes."
    is_demonstrated_weakness: false
  uncertainty:
    source: repository_evidence
    question: "None outstanding for this excerpt."
  owner_intent_state:
    known: "N/A for this end-to-end test."
    status: sufficient
```
<!-- MODEL_SECTION:extended_analysis:END -->

```yaml
primary_fog_type: product_fog
recommended_workflow_id: product-implementation-workflow
escalation_recommended: false
weakness_type: Zero Validation
evidence:
  - "scripts/brief_skeleton.py (lines L52): artifact_id constant"
```
"""
# recommended_workflow_id deliberately uses product-implementation-workflow,
# not architecture-implementation-workflow: the latter is valid per
# workflow-registry.yaml (what validate-brief.py checks) but is missing from
# docs/canonical-vocabulary.yaml's workflow_ids list (what validate-artifact.py
# checks) -- a real, pre-existing drift between the two registries, unrelated
# to Section 15/extended_analysis. Using a workflow id present in both keeps
# this test isolated to what it's actually verifying.


class TestExtendedAnalysisEndToEnd(unittest.TestCase):
    def test_reconciled_brief_with_section_15_passes_full_validator_chain(self):
        # Real producer: brief_skeleton.reconcile(), not a hand-authored fixture.
        artifact_text = bs.reconcile(REALISTIC_MODEL_OUTPUT, target_root=REPO_ROOT)
        self.assertIn("schema_version: 1", artifact_text)
        self.assertIn("## 15. Extended analysis", artifact_text)

        fd, path = tempfile.mkstemp(suffix=".md")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(artifact_text)

            # Real consumer #1: the generic validator (per artifact-contracts.yaml's
            # verification.generic_validator). Returns plain formatted-string
            # errors, not structured dicts -- unlike validate-brief.py.
            generic_errors = validate_artifact_module.validate_artifact(
                "repository_sensemaking_brief", path, REPO_ROOT
            )
            self.assertEqual(
                generic_errors, [],
                f"generic validator reported errors: {generic_errors}",
            )

            # Real consumer #2: the specialized validator (per
            # artifact-contracts.yaml's verification.specialized_validators).
            specialized_errors = validate_brief_module.validate_brief(path, REPO_ROOT)
            specialized_blocking = [
                e for e in specialized_errors if validate_brief_module._is_blocking(e)
            ]
            self.assertEqual(
                specialized_blocking, [],
                f"validate-brief.py reported blocking errors: {specialized_blocking}",
            )

            # Section 15's own fields must have produced zero warnings too --
            # this fixture's extended_analysis content is entirely valid.
            extended_analysis_warnings = [
                e for e in specialized_errors if "EXTENDED_ANALYSIS" in e["message"]
            ]
            self.assertEqual(extended_analysis_warnings, [])
        finally:
            os.remove(path)

    def test_reconciled_brief_without_section_15_is_unaffected(self):
        # Same real producer/consumer chain, minus the extended_analysis
        # MODEL_SECTION entirely -- confirms the mechanism is
        # additive, not load-bearing for the pre-existing contract.
        without_section_15 = REALISTIC_MODEL_OUTPUT.replace(
            REALISTIC_MODEL_OUTPUT[
                REALISTIC_MODEL_OUTPUT.index("<!-- MODEL_SECTION:extended_analysis:BEGIN -->"):
                REALISTIC_MODEL_OUTPUT.index("<!-- MODEL_SECTION:extended_analysis:END -->")
                + len("<!-- MODEL_SECTION:extended_analysis:END -->")
            ],
            "",
        )
        artifact_text = bs.reconcile(without_section_15, target_root=REPO_ROOT)
        self.assertNotIn("The skeleton mechanism is now production-real.", artifact_text)

        fd, path = tempfile.mkstemp(suffix=".md")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(artifact_text)
            specialized_errors = validate_brief_module.validate_brief(path, REPO_ROOT)
            specialized_blocking = [
                e for e in specialized_errors if validate_brief_module._is_blocking(e)
            ]
            self.assertEqual(specialized_blocking, [])
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
